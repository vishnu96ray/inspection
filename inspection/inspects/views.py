from __future__ import division
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from inspects import models

from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mass_mail
import math
user = get_user_model()
from datetime import datetime


def compliance_filterdata_ajax(request):
    if request.method == "GET" and request.is_ajax():
        str=request.GET.get('str')

        if(str=='filter'):
            print('b')
            rly_id=request.GET.get('rly_id')
            print(rly_id,'_________________________aaaaaa________________')
            if(rly_id==""):
                list3=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
            else:    
                list3=models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code=rly_id).values('location_code')
            list4=[]
            for i in list3:
                list4.append(i['location_code'])    
            print(list4,'__________________________llllllllll______________')
            return JsonResponse({'div':list4})
        if(str=='reply'):
            cuser=request.user
            myuserid=models.MyUser.objects.filter(email=cuser).values('id')
            print(cuser,'cuser')
            inspection_id=request.GET.get('inspection_id')
            print(inspection_id,'_________________')
            print(myuserid[0]['id'],'__________________________')
            list1=models.Inspection_details.objects.filter(inspection_no=inspection_id).values()
            list5=models.Marked_Officers.objects.filter(item_no__inspection_no_id=inspection_id,myuser_id_id=myuserid[0]['id']).values('item_no_id')
            print(list5,'_____________')
            list6=[]
            for i in list5:
                list6.append(i['item_no_id'])
            list2=models.Item_details.objects.filter(item_no__in=list6).values()
            list3=[]
            list4=[]
            for i in list1:
                temp={}
                temp['inspection_no']=i['inspection_no']
                temp['inspection_officer']=i['inspection_officer']
                temp['inspection_title']=i['inspection_title']
                temp['inspection_date']=i['inspected_on'].strftime("%d/%m/%y")
                list3.append(temp)
            for i in list2:
                temp={}
                temp['item_no']=i['item_no']  
                temp['observation']=i['observation']
                temp['compliance']=models.Marked_Officers.objects.filter(item_no=i['item_no'])[0].compliance
                list4.append(temp)  
            print(list3,'__________________________list3')
            print(list4,'__________________________________list4')    
            return JsonResponse({'idetails':list3,'itemdetails':list4})
        if(str=='save'):
            item_no=request.GET.get('item_no')
            compliance=request.GET.get('compliance')
            models.Marked_Officers.objects.filter(item_no_id=item_no).update(compliance=compliance)
            return JsonResponse({})    
def compliance_filterdata(request):
    print('a')
    if request.method == "GET" and request.is_ajax():
        print('b')
        div_id=request.GET.get('div_id')
        rly_id=request.GET.get('rly_id')
        dept_id=request.GET.get('dept_id')
        print(dept_id,'__________________________________________________')
        startDate=request.GET.get('startDate')
        print(startDate)
        startDate = datetime.strptime(startDate,'%Y-%m-%d')
        print(startDate)
        endDate=request.GET.get('endDate')
        print(endDate)
        endDate = datetime.strptime(endDate,'%Y-%m-%d')
        print(endDate)
        #inspect_details=models.Inspection_details.objects.filter(zone=rly_id,division=div_id,dept=dept_id,inspected_on__gte=startDate,inspected_on__lte=endDate).values()
        inspect_details=models.Inspection_details.objects.filter(zone=rly_id,division=div_id,dept=dept_id).values()
        print(inspect_details,'______________')
        list1=[]
        count=1
        for i in inspect_details:
            marked=models.Marked_Officers.objects.filter(item_no__inspection_no_id=i['inspection_no']).values()
            marked_to = set(mark['myuser_id_id'] for mark in marked)
            temp={}
            temp['sr_no']=count
            temp['inspection_no']=i['inspection_no']
            temp['inspection_officer']=i['inspection_officer']
            # temp['inspected_on']=', '.join(marked_to)
            temp['inspected_on']=i['inspected_on'].strftime("%d/%m/%y")
            temp['viewed_on']=i['modified_on'].strftime("%d/%m/%y")
            temp['file_path']=i['report_path']
            # temp['Complaince_Reaction']=i['compliance_recieved_on']
            list1.append(temp)

        return JsonResponse({'inspect_details':list1})
def compliance_form(request):
    
    list1=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
    list2=[]
    for i in list1:
        print(i['location_code'],'_________')
        list2.append(i['location_code'])
    list3=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
    list4=[]
    for i in list3:
        print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().values('department_name')
    list6=[]
    for i in list5:
        print(i['department_name'],'_________')
        list6.append(i['department_name'])        
    context={
        'zone':list2 ,
        'division':list4,
        'dept':list6,
    }
    print(list2,'_____________')
    return render(request,'compliance_form.html',context)



def home(request):
    if request.method == "POST":
        firstName=request.POST.get('firstName')
        middleName=request.POST.get('middleName')
        lastName=request.POST.get('lastName')
        email=request.POST.get('official_emailID')
        official_mobileNo=request.POST.get('official_mobileNo')
        personal_emailID=request.POST.get('personal_emailID')
        personal_mobileNo=request.POST.get('personal_mobileNo')
        faxNo=request.POST.get('faxNo')
        aadhaarNo=request.POST.get('aadhaarNo')
        password=request.POST.get('password')
        user.objects.create_user(first_name=firstName,middle_name=middleName,last_name=lastName
        ,email=email,official_mobileNo=official_mobileNo,personal_emailID=personal_emailID,
        personal_mobileNo=personal_mobileNo,faxNo=faxNo,aadhaar_no=aadhaarNo,password=password)
    return render(request, 'home.html')

def MailSend(subject,email_body1,To):
    try:
        # subject = "Verify Your Mail"
        email = 'amisha.kri491@gmail.com'

        html_content= MIMEText(email_body1+'<br><div class="container"><img src="cid:myimage"/></div><div style="text-align:center"><a href="#"> Unsubscribe</a></div>', _subtype='html')
        text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.

        text_file = open("mail.txt", "a") # opening my file
        time=datetime.now()
        date_time=time.strftime("%m/%d/%Y,%H:%M:%S")

        text_file.write("\n\n"+date_time+"\n"+email+'\n'+To+"\n"+subject+"\n"+text_content) 
        text_file.write(text_content) 
        text_file.close() #file close

        img_data = open('rkvy/static/rkvy/images/logo_rkvy.png', 'rb').read()

        html_part = MIMEMultipart(_subtype='related')

        # Create the body with HTML. Note that the image, since it is inline, is 
        # referenced with the URL cid:myimage... you should take care to make
        # "myimage" unique
        html_part.attach(html_content)

        # Now create the MIME container for the image
        img = MIMEImage(img_data, 'png')
        img.add_header('Content-Id', '<myimage>')  # angle brackets are important
        img.add_header("Content-Disposition", "inline", filename="myimage") # David Hess recommended this edit
        html_part.attach(img)

        # Configure and send an EmailMessage
        # Note we are passing None for the body (the 2nd parameter). You could pass plain text
        # to create an alternative part for this message
        msg = EmailMessage(subject, None, email, [To])
        msg.attach(html_part) # Attach the raw MIMEBase descendant. This is a public method on EmailMessage
        msg.send()
    except Exception as e: 
        try:
            models.error_Table.objects.create(fun_name="MailSend",err_details=str(e))
        except:
            print("Internal Error!!!")


def loginUser(request):
    # try:
        if request.method == "POST":
            _email = request.POST.get('email').strip()
            _password = request.POST.get('password').strip()
            print(_email,'____')
            print(_password,'_____')
            # obj3=models.rkvy_userEnrollment.objects.filter(user_id__email=_email).values('pending_stage')
            # check for existence
            userObj = authenticate(username=_email, password=_password)

            print("22222222222222222222222227777777777777777777777777777777777777777777777^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",userObj)
            if userObj is not None:
                login(request, userObj)
                print("inside login&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                if userObj.user_role == 'rkvy_superadmin':
                    return HttpResponseRedirect('/rkvy_superAdminHome')
                elif userObj.user_role == 'rkvy_headquarteradmin':
                    return HttpResponseRedirect('/rkvy_headquarterAdminHome')
                elif userObj.user_role == 'rkvy_instituteadmin':
                    
                    return HttpResponseRedirect('/rkvy_instituteAdminHome')
                elif userObj.user_role == 'rkvy_instructor':
                    return HttpResponseRedirect('/rkvy_instructorHome')
                else:
                    return render(request,"list_create_inspection_report.html")
                    
            else:
                #change 21-10
                if user.objects.filter(email=_email,user_role='rkvy_trainee',is_active=False).exists():
                    messages.error(request, 'Email is not verified yet. Please verify first then login again.')
                else:
                    messages.error(request, 'Invalid Credentials.')#till here 21-10
                #return HttpResponseRedirect('/rkvy_login')
                return render(request, "login.html")

        return render(request, "login.html")
    # except Exception as e: 
    #     try:
    #         models.error_Table.objects.create(fun_name="login",user_id=request.user,err_details=str(e))
    #     except:
            
    #         print("Internal Error->>>>>>>>>4!!!")
    #     #messages.error(request, 'Error : '+str(e))
    #     return render(request, "login.html", {})


def forgotPassword(request):
    # try:
        if request.method == "POST":
            _email = request.POST.get('email').strip()

            try:
                userObj = user.objects.get(email=_email)
                #print(userObj)
            except Exception as e:
                messages.error(request, 'Please enter registed email.')
                return HttpResponseRedirect('/forgotPassword')

            email_context = {
                "email": userObj.email,
                'domain': 'railkvy.indianrailways.gov.in',
                'site_name': 'Kaushal Vikas',
                "uid": urlsafe_base64_encode(force_bytes(userObj.pk)),
                "user": userObj,
                'token': default_token_generator.make_token(userObj),
                'protocol': 'http',
            }
            email_template_name = "email_forgotPassword_body.txt"
            email_body = render_to_string(email_template_name, email_context)
            try:
                #print("trying to send mail")
                #print(userObj.email)
                try:
                    # send_mail("Verify Your Mail", email_body, 'crisdlwproject@gmail.com',
                    #          [f'{userObj.email}'], fail_silently=False)


                    #saud faisal (28-08-2021) -----
                    subject="Reset password for RKVY login"
                    To=userObj.email
                    email_body1='<p>'+email_body+'</p>'
                    MailSend(subject,email_body1,To)
                    #end here
                    return HttpResponse('Verification Email has been successfully sent.(see also spam folder)')
                except:
                    print("error on sending")
                    messages.error(
                        request, 'Verification Email failed. Please Try Again.')
            except:
                messages.error(
                    request, 'Something went wrong.')
            return render(request, "inspects_forgotPassword.html")

        return render(request, "inspects_forgotPassword.html")
    # except Exception as e: 
    #     try:
    #         models.error_Table.objects.create(fun_name="forgotPassword",user_id=request.user,err_details=str(e))
    #     except:
    #         print("Internal Error!!!")
    #     #messages.error(request, 'Error : '+str(e))
    #     return render(request, "commanerrorpage.html", {})


#bhartistart

def created_checklist(request):
    try:
        print('@@@@@@@@@@@@@')
        context={
            
        }
        return render(request,"list_create_inspection_report.html",context)
    except Exception as e:
        print("e==",e)  
        return render(request, "commonerrorpage.html", {})

def create_inspection_form(request):
    # try:
      
        print('###########')
        list1=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
        list2=[]
        for i in list1:
            print(i['location_code'],'_________')
            list2.append(i['location_code'])
        list3=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
        list4=[]
        for i in list3:
            print(i['location_code'],'_________')
            list4.append(i['location_code'])    
        context={
           'Zone':list2 ,
           'division':list4,
        }
        print(list2,'_____________')
        # zone_loc_submit=request.POST.get('zone_loc_submit')
        # if(zone_loc_submit='zone_loc_submit'):
        #     models.
        return render(request,"create_inspection_form.html",context)
    # except Exception as e:
    #     print("e==",e)  
    #     return render(request, "commonerrorpage.html", {})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def save_draft_data(request):
    try:
        if request.method == "POST" and request.is_ajax():
            print("inside savedraft method")
            btnvalue= request.POST.get('_btnvalue')
            zone= request.POST.get('_zone')
            department=request.POST.get('department_')
            location=request.POST.get('_location')
            print("btnvale--",zone,location,department,btnvalue)
           
            return JsonResponse({"status": 1 })
        return JsonResponse({"success":False}, status=400)
    except Exception as e:
        print("e==",e)  
        return render(request, "commonerrorpage.html", {})

def nominate_officer(request):
    try:
        print("$%^%*()&*^%")
        context={
            
        }
    except Exception as e:
        print("e==",e)  
        return render(request, "commonerrorpage.html", {})


#bhartiend


