import os
from datetime import date

import pythoncom
import win32com
from account.models import Role
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from win32com.client import Dispatch

from .models import Candidate


# Create your views here.
@login_required(login_url='/account/login')
def offer_index(request):
    user = request.user
    roles = list(Role.objects.filter(user=user).values('role'))
    msgs = messages.get_messages(request)

    msg_level = ''
    msg_content = ''

    candidates = Candidate.objects.all()

    if request.session['current_role'] in ['Authorizer', ]:
        candidates = Candidate.objects.filter(offer_generated=True)
    elif request.session['current_role'] in ['Recruiter', ]:
        candidates = Candidate.objects.filter(recruiter=user)
    else:
        pass

    candidates = list(candidates)

    for msg in msgs:
        msg_level = msg.tags
        msg_content = msg
    return render(request, 'offer.html',
                  {'roles': roles, 'current_page': 'Offer', 'msg_level': msg_level, 'msg_content': msg_content,
                   'candidates': candidates})


@login_required(login_url='/account/login')
def offer_add(request):
    user = request.user
    roles = list(Role.objects.filter(user=user).values('role'))
    msgs = messages.get_messages(request)

    msg_level = ''
    msg_content = ''

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        grade = request.POST.get('grade')
        location = request.POST.get('location')
        addiLoc = request.POST.get('addiLoc')
        account = request.POST.get('account')
        probation = request.POST.get('probation')
        salary = request.POST.get('salary')
        var_pay = request.POST.get('var_pay')

        candidate = Candidate.objects.create(name=name,
                                             email=email,
                                             mobile=mobile,
                                             grade=grade,
                                             location=location,
                                             additional_location=addiLoc,
                                             account=account,
                                             probation=probation,
                                             salary=salary,
                                             var_pay=var_pay,
                                             create_date=date.today(),
                                             recruiter=user)

        if candidate:
            messages.success(request, r"Candidate info is saved.")
            return redirect(reverse('offer_index'))
        else:
            messages.error(request, r"Candidate information is not correct, the data isn't saved")
            return redirect(reverse('offer_index'))
    else:
        if request.session['current_role'] in ['Recruiter', ]:
            for msg in msgs:
                msg_level = msg.tags
                msg_content = msg
            return render(request, 'offer-add.html',
                          {'roles': roles, 'current_page': 'Offer', 'msg_level': msg_level,
                           'msg_content': msg_content,})
        else:
            messages.error(request, r"You don't have access to create offer.")
            return redirect(reverse('offer_index'))


@login_required(login_url='/account/login')
def offer_details(request, offer_id):
    user = request.user
    roles = list(Role.objects.filter(user=user).values('role'))
    msgs = messages.get_messages(request)
    current_role = request.session['current_role']

    msg_level = ''
    msg_content = ''

    if request.method == 'POST':
        candidate = Candidate.objects.get(id=offer_id)
        if (not candidate.offer_generated) and current_role == 'Recruiter':
            name = request.POST.get('name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            grade = request.POST.get('grade')
            location = request.POST.get('location')
            addiLoc = request.POST.get('addiLoc')
            account = request.POST.get('account')
            probation = request.POST.get('probation')
            salary = request.POST.get('salary')
            var_pay = request.POST.get('var_pay')
            candidate.name = name
            candidate.email = email
            candidate.mobile = mobile
            candidate.grade = grade
            candidate.location = location
            candidate.additional_location = addiLoc
            candidate.account = account
            candidate.probation = probation
            candidate.salary = salary
            candidate.var_pay = var_pay
            candidate.save()

        if candidate and (not candidate.offer_generated) and current_role == 'Recruiter':
            messages.success(request, r"Candidate info is saved.")

        return redirect(reverse('offer_index'))
    else:
        candidate = Candidate.objects.get(id=offer_id)

        if candidate:
            for msg in msgs:
                msg_level = msg.tags
                msg_content = msg
            return render(request, 'offer-details.html',
                          {'roles': roles, 'current_page': 'Offer', 'msg_level': msg_level, 'msg_content': msg_content,
                           'candidate': candidate})
        else:
            messages.error(request, r"Candidate information is not correct, the data isn't loaded")
            return redirect(reverse('offer_index'))


@login_required(login_url='/account/login')
def offer_generate(request, offer_id):

    candidate = Candidate.objects.get(id=offer_id)
    candidate.offer_generated = True
    candidate.save()

    messages.success(request, r"Offer for "+candidate.name+" is generated.")
    return redirect(reverse('offer_index'))


@login_required(login_url='/account/login')
def offer_sign(request, offer_id):

    candidate = Candidate.objects.get(id=offer_id)
    if candidate and candidate.offer_generated:

        basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_path = os.path.join(basepath, 'offer_template/')
        offer_path = os.path.join(basepath, 'offer_files/')

        if candidate.probation == '0':
            template_name = 'Offer letter-'+candidate.location+'-no probation.docx'
        elif candidate.probation == '3':
            template_name = 'Offer letter-'+candidate.location+'-3 months probation.docx'
        else:
            template_name = 'Offer letter-'+candidate.location+'-6 months probation.docx'

        # offer_name = 'TCS'

        pythoncom.CoInitialize()
        w = win32com.client.DispatchEx('Word.Application')
        w.Visible = 0
        w.DisplayAlerts = 0

        doc = w.Documents.Open(FileName=template_path+template_name)
        doc.SaveAs(r'Offer letter-BJ-3 months probation.pdf', FileFormat=17)
        doc.Close()
        w.Quit()
        pythoncom.CoUninitialize()

        messages.success(request, r"Offer for "+candidate.name+" is signed.")
    else:
        messages.error(request, r"Offer is not signed")

    return redirect(reverse('offer_index'))

