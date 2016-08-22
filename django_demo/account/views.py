from django.contrib import messages
from django.contrib.auth import logout, login, authenticate, password_validation
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from .models import Role


# Create your views here.


def user_login(request):
    errors = []
    username = None
    password = None
    if request.method == 'POST':
        if not request.POST.get('username'):
            errors.append('Please Enter username')
        else:
            username = request.POST.get('username')
        if not request.POST.get('password'):
            errors.append('Please Enter password')
        else:
            password = request.POST.get('password')
        if username is not None and password is not None :
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    roles = list(Role.objects.filter(user=user).values('role'))
                    current_role = roles[0]['role']
                    request.session['current_role'] = current_role
                    messages.success(request, 'Login Success as '+user.first_name+' '+user.last_name+' with '+current_role+' role.')
                    return redirect('/')
                else:
                    errors.append('disabled account')
            else:
                errors.append('invaild user')
        return render(request, 'page-login.html', {'has_error': True, 'errors':errors})
    return render(request, 'page-login.html')


@login_required(login_url='/account/login')
def user_logout(request):
    logout(request)
    request.session.clear()
    return redirect(reverse('account_profile'))


@login_required(login_url='/account/login')
def switch_role(request, new_role):
    user = request.user
    roles = list(Role.objects.filter(user=user).values('role'))
    current_role = request.session['current_role']
    for role in roles:
        if new_role == role['role']:
            current_role = new_role
            request.session['current_role'] = current_role
            messages.success(request, 'Switch role success to '+current_role)

    if new_role == current_role:
        messages.success(request, 'Switch role success to ' + current_role)
    else:
        messages.error(request, r"You don't have role " + new_role)

    return redirect(reverse('account_profile'))


@login_required(login_url='/account/login')
def user_profile(request):
    user = request.user
    roles = list(Role.objects.filter(user=user).values('role'))
    msgs = messages.get_messages(request)

    msg_level = ''
    msg_content = ''

    for msg in msgs:
        msg_level = msg.tags
        msg_content = msg

    return render(request, 'profile.html', {'roles': roles, 'current_page':'Profile', 'msg_level': msg_level, 'msg_content': msg_content})


def redirect_to_index(request):
    return redirect(
        reverse('account_profile')
    )


@login_required(login_url='/account/login')
def user_update(request):
    user = request.user
    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')
    email = request.POST.get('email')
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.save()
    messages.success(request, 'Profile details are updated.')
    return redirect('account_profile')


@login_required(login_url='/account/login')
def user_changePWD(request):
    user = request.user
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    new_password_r = request.POST.get('new_password_r')

    if not user.check_password(old_password):
        messages.error(request, 'Old password is not correct, password is not changed.')
        return redirect('account_profile')
    if new_password != new_password_r:
        messages.error(request, r"The new password doesn't match.")
        return redirect('account_profile')

    try:
        password_validation.validate_password(new_password)
        user.set_password(new_password)
        messages.success(request, 'Password has been changed.')
    except ValidationError as e:
        print(e.messages)
        errorMessage = 'Password validation is failed because: '
        for i in e.messages:
            errorMessage += i
        print(errorMessage)
        messages.error(request, errorMessage)

    return redirect('account_profile')


