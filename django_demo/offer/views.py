import os
import pythoncom
import win32com

from datetime import date, time
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from win32com.client import Dispatch
from django.http import StreamingHttpResponse


from .models import Candidate
from account.models import Role


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
            offer_number = request.POST.get('offer_number')
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
            candidate.offer_number = offer_number
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

        # offer_name_doc = 'TCSC EP2016 ' + candidate.offer_number + ' ' + candidate.name + ' ' + candidate.location + '.docx'
        offer_name_pdf = 'TCSC EP2016 ' + candidate.offer_number + ' ' + candidate.name + ' ' + candidate.location + '.pdf'

        candidate.offer_date = date.today()

        offer_year = candidate.offer_date.year
        if candidate.offer_date.month == 1:
            offer_month = 'Jan'
        elif candidate.offer_date.month == 2:
            offer_month = 'Feb'
        elif candidate.offer_date.month == 3:
            offer_month = 'Mar'
        elif candidate.offer_date.month == 4:
            offer_month = 'Apr'
        elif candidate.offer_date.month == 5:
            offer_month = 'May'
        elif candidate.offer_date.month == 6:
            offer_month = 'Jun'
        elif candidate.offer_date.month == 7:
            offer_month = 'Jul'
        elif candidate.offer_date.month == 8:
            offer_month = 'Aug'
        elif candidate.offer_date.month == 9:
            offer_month = 'Sep'
        elif candidate.offer_date.month == 10:
            offer_month = 'Oct'
        elif candidate.offer_date.month == 11:
            offer_month = 'Nov'
        elif candidate.offer_date.month == 12:
            offer_month = 'Dec'

        offer_day = candidate.offer_date.day
        offer_date = str(offer_year) +'-'+ str(offer_month)+'-'+str(offer_day)


        try:
            pythoncom.CoInitialize()
            w = win32com.client.DispatchEx('Word.Application')
            w.Visible = 0
            w.DisplayAlerts = 0

            doc = w.Documents.Open(FileName=template_path+template_name)

            w.Selection.Find.Execute('[Candidate_Name]', False, False, False, False, False, True, 1, True, candidate.name, 2)
            w.Selection.Find.Execute('[Candidate_Grade]', False, False, False, False, False, True, 1, True, candidate.grade, 2)
            w.Selection.Find.Execute('[Candidate_Ref_No]', False, False, False, False, False, True, 1, True, candidate.offer_number, 2)
            w.Selection.Find.Execute('[Candidate_Date]', False, False, False, False, False, True, 1, True, offer_date, 2)
            if candidate.location == 'SH':
                location = 'Shanghai'
            elif candidate.location == 'BJ':
                location = 'Beijing'
            elif candidate.location == 'TJ':
                location = 'Tianjing'
            elif candidate.location == 'DL':
                location = 'Dalian'
            elif candidate.location == 'HZ':
                location = 'Hangzhou'
            elif candidate.location == 'SZ':
                location = 'Shenzhen'

            w.Selection.Find.Execute('[Work_Location]', False, False, False, False, False, True, 1, True, location, 2)
            if candidate.additional_location:
                w.Selection.Find.Execute('[Other_Location]', False, False, False, False, False, True, 1, True, 'and '+candidate.additional_location, 2)
            else:
                w.Selection.Find.Execute('[Other_Location]', False, False, False, False, False, True, 1, True, '', 2)

            w.Selection.Find.Execute('[Probation_Pay]', False, False, False, False, False, True, 1, True, str(candidate.salary*0.95)+'0', 2)
            w.Selection.Find.Execute('[Base_Pay]', False, False, False, False, False, True, 1, True, str(candidate.salary)+'.00', 2)
            w.Selection.Find.Execute('[Valid_Date]', False, False, False, False, False, True, 1, True, offer_date, 2)
            w.Selection.Find.Execute('[Variable_Pay]', False, False, False, False, False, True, 1, True, str(candidate.var_pay)+'0', 2)
            w.Selection.Find.Execute('[13_Salary]', False, False, False, False, False, True, 1, True, str(candidate.salary)+'.00', 2)

            doc.SaveAs(offer_path+offer_name_pdf, FileFormat=17)

            candidate.offer_signed = True
            candidate.save()

        finally:
            doc.Close(0)
            w.Quit()
            pythoncom.CoUninitialize()

        messages.success(request, r"Offer for "+candidate.name+" is signed.")
    else:
        messages.error(request, r"Offer is not signed")

    return redirect(reverse('offer_index'))


@login_required(login_url='/account/login')
def offer_download(request, offer_id):

    candidate = Candidate.objects.get(id=offer_id)
    if candidate and candidate.offer_signed:

        basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        offer_path = os.path.join(basepath, 'offer_files/')

        offer_name_pdf = 'TCSC EP2016 ' + candidate.offer_number + ' ' + candidate.name + ' ' + candidate.location + '.pdf'

        def file_iterator(fn, buf_size=512):
            with open(fn,'rb') as f:
                while True:
                    c = f.read(buf_size)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iterator(offer_path+offer_name_pdf))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="'+offer_name_pdf+'"'
        messages.success(request, r"Offer for "+candidate.name+" is signed.")
        return response

    else:
        messages.error(request, r"Offer is not signed")

    return redirect(reverse('offer_index'))
