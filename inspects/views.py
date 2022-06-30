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
from django.db.models import Q
from django.contrib import messages
from inspects.utils import render_to_pdf
from .choices import *





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

from xhtml2pdf import pisa
from django.template.loader import get_template
#vishnu  location searching function

def search_location(request):
    # if request.method== 'POST':
    #     query = request.POST.get('query')
    #     que=Q()
    #     for word in query.split():
    #         que &=Q(observation__icontains=word)
            
    #     des_location=models.Item_details.objects.filter(que)
        
    #     #des_location=models.Item_details.objects.filter(Q(observation__icontains=query) |Q(item_no__icontains=query) |Q(inspection_no__division__icontains=query) |Q(inspection_no__zone__icontains=query) )
    #     # render(request,'keyword_location_search.html', {'des_location':des_location})
    #     return redirect('keyword_location_search.html', {'des_location':des_location})
    # else:
    #     query = False
        
    #Find railway location/Zone
    list1=models.railwayLocationMaster.objects.filter(location_type='ZR').values('location_code')
    list2=[]
    for i in list1:
        # print(i['location_code'],'_________')
        list2.append(i['location_code'])
    
    list3=models.railwayLocationMaster.objects.filter(location_type='DIV').values('location_code')
    list4=[]
    for i in list3:
        # print(i['location_code'],'_________')
        list4.append(i['location_code'])  
    list5=models.departMast.objects.all().values('department_name')
    list6=[]
    for i in list5:
        # print(i['department_name'],'_________')
        list6.append(i['department_name'])
    
    list7=models.Level_Desig.objects.all().values('designation')
    list8=[]
    for i in list7:
        # print(i['designation'],'_________')
        list8.append(i['designation'])
    
    
    
    # design=models.Item_details.objects.filter().values('item_no','inspection_no__inspected_on','inspection_no__inspection_officer','inspection_no__inspection_note_no','modified_on','observation','inspection_no__division','inspection_no__zone')
    context={'zone':list2,'division':list4,'dept':list6, 'desi':list8, }
    return render(request, 'search_location.html', context)


    

def keyword_location_search(request):
    if request.method== 'POST':
        query = request.POST.get('query')
        que=Q()
        for word in query.split():
            que &=Q(observation__icontains=word)
            
        des_location=list(models.Item_details.objects.filter(que).values())
        print(des_location)
        
        # des_location=list(models.Item_details.objects.filter().values('modified_on'))
        for i in range(len(des_location)):
            if des_location[i]['modified_on']!=None:
                x=des_location[i]['modified_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
                des_location[i].update({'modified_on':x})

        #des_location=models.Item_details.objects.filter(Q(observation__icontains=query) |Q(item_no__icontains=query) |Q(inspection_no__division__icontains=query) |Q(inspection_no__zone__icontains=query) )
        # render(request,'keyword_location_search.html', {'des_location':des_location})
        
        context={'des_location':des_location}

        return render(request,'keyword_location_search.html',context )
    else:
        return render(request,'keyword_location_search.html')
        
    
    
        
    

def search_locat_ajax(request):
    try:
        if request.method== 'GET' and request.is_ajax():
            grou=request.GET.get("group")
            ins=list(models.railwayLocationMaster.objects.filter(location_type='DIV',parent_location_code=grou).values('location_code', 'rly_unit_code'))
            return JsonResponse({'ins':ins}, safe=False)
        return JsonResponse({'success':False}, status=400)
    except Exception as e:
        print(e)
        
    
def search_desig_ajax(request):
    try:
        if request.method== 'GET' and request.is_ajax():
            grou=request.GET.get("groupss")
            ins=list(models.Level_Desig.objects.filter(rly_unit=grou).values('designation'))
            return JsonResponse({'ins':ins}, safe=False)
        return JsonResponse({'success':False}, status=400)
    except Exception as e:
        print(e)



def fetch_desig_ajax(request):
    try:
        if request.method == 'GET' and request.is_ajax():
            location_code=request.GET.get("location_code")
            location_type=request.GET.get("location_type")
            dept=request.GET.get("dept")
            inspected_on=request.GET.get('inspected_on')
            print(inspected_on)
            mydata={}
            grou=(location_code, location_type, dept, inspected_on)
            print(grou,'tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt')
            ins=list(models.Inspection_details.objects.filter(zone=location_code).values('inspection_no','inspection_note_no','dept','division','zone','created_on','inspected_on'))
            for i in range(len(ins)):
                if ins[i]['inspected_on']!=None:
                    x=ins[i]['inspected_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
                    ins[i].update({'inspected_on':x})
            #print(ins, 'inspection_no')
            
            # ins_no=list(models.Inspection_details.objects.filter(zone=location_code, location=location_type,dept=dept,).values('inspection_no'))
            for i in ins:
                
                # ins_no=list(models.Item_details.objects.filter(inspection_no=i['inspection_no']).values('observation','inspection_no_id__zone','inspection_no_id__dept', 'inspection_no_id__division', 'inspection_no_id__location','inspection_no_id__inspected_on','inspection_no_id__created_on','inspection_no_id__inspection_no','inspection_no_id__inspection_note_no'))
                # print(ins_no, 'dddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
                mydata.update({'ins':ins,'grou':grou,'location_code':location_code, 'location_type':location_type,'dept':dept,})
            print(mydata,'444444444444444444444444444444444444444444444444444444')
            return JsonResponse(ins, safe=False)
        return JsonResponse({'success':False}, status=400)
    except Exception as e:
        print(e)


from xhtml2pdf import pisa

def search_location_detail(request, pk):
    info=list(models.Inspection_details.objects.filter(inspection_no=pk).values().distinct())
    #convert date dd-mm-yyyy
    for i in range(len(info)):
        if info[i]['inspected_on']!=None:
            x=info[i]['inspected_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
            info[i].update({'inspected_on':x})
    
    # pdf generate code
    # inspectionDetails=models.Inspection_details.objects.filter(inspection_no=pk)
    # itemDetails=models.Item_details.objects.filter(inspection_no=inspectionDetails[0].inspection_no)
    
    # print(itemDetails[0].observation)
    

    obj={}
    total=1
    for m2 in info:
        #convert date dd-mm-yyyy
        # x=models.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].inspected_on
        # x=x.strftime('%d'+'-'+'%m'+'-'+'%Y')
        inspectionDetails=models.Inspection_details.objects.filter(inspection_no=pk)
        itemDetails=models.Item_details.objects.filter(inspection_no=inspectionDetails[0].inspection_no)
    
        
        # print(itemDetails[0].modified_on)
        
        temdata = {str(total):{"inspection_no":m2['inspection_no'], 
                               'inspection_note_no':m2['inspection_note_no'],
                               'inspection_officer':m2['inspection_officer'],
                               'zone':m2['zone'],
                               'observation':itemDetails[0].observation,
                            #    'modified_on':itemDetails[0].modified_on,
                               'division':m2['division'],
                               'location':m2['location'],
                               'inspected_on':m2['inspected_on'],
                               'modified_on':m2['modified_on']}}
        print(temdata, 'gfggggggggggggggggggggggggggggggggg')
        
    
        
        obj.update(temdata)
        total=total+1
        # print(temdata,"********************") 
    
    # print(obj,'tyyytytytytytytytytyty')
    lent=len(obj)
    # print(lent, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    context={'info':info, 'obj': obj, 'lent':lent,}
    pdf=render_to_pdf('search_location_detail.html', context) 
    return HttpResponse(pdf, content_type='application/pdf')



def search_list_created_checklist(request):
    obj=models.Inspection_Checklist.objects.filter().values('checklist_id', 'checklist_title','inspection_type','status','created_by','created_on','delete_flag')[::-1]
    # print(obj)
    for i in range(len(obj)):
        if obj[i]['created_on']!=None:
            x=obj[i]['created_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
            obj[i].update({'created_on':x})
            
    context={'obj':obj}
    template_name='search_list_created_checklist.html'
        
    return render(request, template_name, context)

from .forms import *
import  json

# def search_createchecklist(request):
#     if request.method == "POST" and request.is_ajax():
#         from datetime import datetime
#         checklist_title=request.POST.get('checklist_title')
#         inspection_type=request.POST.get('inspection_type')
#         status=request.POST.get('status')
#         activities=request.POST.get('activities')

#         models.Inspection_details.objects.create(checklist_title=checklist_title,inspection_type=inspection_type,status=status,activities=activities)
#         inspection_id=models.Inspection_details.objects.all().last().inspection_no
       

#         return JsonResponse({"status": 1 })
#     return JsonResponse({"success":False}, status=400)


def search_createchecklist(request):
    if request.method =='POST':
        checklist_title=request.POST.get('checklist_title')
        inspection_type=request.POST.get('inspection_type')
        activities=request.POST.getlist('activities')
        status=request.POST.get('draft')
        createchecklist=models.Inspection_Checklist(checklist_title=checklist_title, inspection_type=inspection_type, status=status)
        createchecklist.save()
        for i in range(len(activities)):
            inspection_Activity=models.Inspection_Activity(activities=activities[i])
            inspection_Activity.checklist_id=Inspection_Checklist.objects.get(checklist_id=createchecklist.checklist_id)
            inspection_Activity.save()
        return redirect('/search_list_created_checklist/')
    return render(request, 'search_createchecklist.html', {"INSPECTION_TYPE":INSPECTION_TYPE })


def search_editchecklist(request, pk):    
    inspection_Checklist=models.Inspection_Checklist.objects.get(checklist_id=pk)
    ass=models.Inspection_Activity.objects.filter(checklist_id=int(inspection_Checklist.checklist_id)).values('activities')
    if request.method =='POST':
        checklist_title=request.POST.get('checklist_title')
        inspection_type=request.POST.get('inspection_type')
        activities=request.POST.getlist('activities')
        status=request.POST.get('draft')
        inspection_Checklist=models.Inspection_Checklist.objects.filter(checklist_id=pk).update(checklist_title=checklist_title, inspection_type=inspection_type, status=status)
        inspection_Activity
        for i in range(len(activities)):
            inspection_Activity=models.Inspection_Activity(activities=activities[i])
            inspection_Activity.checklist_id=Inspection_Checklist.objects.get(checklist_id=inspection_Checklist.checklist_id)
            inspection_Activity=models.Inspection_Activity.objects.filter(activity_id=pk).update(checklist_id=inspection_Checklist.checklist_id)
        return redirect('/search_list_created_checklist/')
    return render(request, 'search_createchecklist.html',{'ass':ass, 'inspection_Checklist':inspection_Checklist, "INSPECTION_TYPE":INSPECTION_TYPE })




def search_delete_flag(request, pk):
    flag=models.Inspection_Checklist.objects.get(checklist_id=pk)
    flag.delete_flag=True
    flag.save()
    return HttpResponseRedirect('/search_list_created_checklist/')  
 



def search_checklist_detail(request, pk):
    info=list(models.Inspection_Checklist.objects.filter(checklist_id=pk).values().distinct())
    #convert date dd-mm-yyyy
    for i in range(len(info)):
        if info[i]['created_on']!=None:
            x=info[i]['created_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
            info[i].update({'created_on':x})
            
    obj={}
    total=1
    for m2 in info:

        
        temdata = {str(total):{"checklist_id":m2['checklist_id'], 
                               'checklist_title':m2['checklist_title'],
                               'created_on':m2['created_on'],
                               'created_by':m2['created_by'],
                               
                               'inspection_type':m2['modified_on']}}
        print(temdata, 'gfggggggggggggggggggggggggggggggggg')
        obj.update(temdata)
        total=total+1
        # print(temdata,"********************") 
    
    # print(obj,'tyyytytytytytytytytyty')
    lent=len(obj)
    # print(lent, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    context={'info':info, 'obj': obj, 'lent':lent,}
    pdf=render_to_pdf('search_checklist_detail.html', context) 
    return HttpResponse(pdf, content_type='application/pdf')


def search_checklist_views(request, pk):
    inspection_Checklist=models.Inspection_Checklist.objects.get(checklist_id=pk)
    print(inspection_Checklist)
    ass=models.Inspection_Activity.objects.filter(checklist_id=int(inspection_Checklist.checklist_id)).values('activities')
    print(ass, 'ddddddddddddddddddddddddddddd')
    
    
    return render(request, 'search_checklist_views.html',{'ass':ass,'inspection_Checklist':inspection_Checklist, "INSPECTION_TYPE":INSPECTION_TYPE })
    


# def search_location_detail(request, pk):
       
#     # info=list(models.Item_details.objects.filter(item_no=pk).values().distinct())
#     # print(info,'shhhhhhhhhhhh')
#     info=list(models.Inspection_details.objects.filter(inspection_no=pk).values().distinct())

    
#     #convert date dd-mm-yyyy
#     for i in range(len(info)):
#         if info[i]['modified_on']!=None:
#             x=info[i]['modified_on'].strftime('%d'+'-'+'%m'+'-'+'%Y')
#             info[i].update({'modified_on':x})
    
    
    
#     # pdf generate code

#     obj={}
#     total=1
#     for m2 in info:
#         #convert date dd-mm-yyyy
#         x=models.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].inspected_on
#         x=x.strftime('%d'+'-'+'%m'+'-'+'%Y')
#         temdata = {str(total):{"item_no":m2['item_no'], 
#                                'inspection_note_no':models.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].inspection_note_no,
#                                'inspection_officer':models.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].inspection_officer,
#                                'zone':models.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].zone,
#                                'location':models.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].location,
#                                'division':models.Inspection_details.objects.filter(inspection_no=m2['inspection_no_id'])[0].division,
#                                'inspected_on':x,
                               
#                                'observation':m2['observation'], 'modified_on':m2['modified_on']}}
#         # print(temdata, 'gfggggggggggggggggggggggggggggggggg')
        
    
        
#         obj.update(temdata)
#         total=total+1
#         # print(temdata,"********************") 
    
#     # print(obj,'tyyytytytytytytytytyty')
#     lent=len(obj)
#     # print(lent, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx')

#     context={'info':info, 'obj': obj, 'lent':lent,}
#     pdf=render_to_pdf('search_location_detail.html', context) 
#     return HttpResponse(pdf, content_type='application/pdf')
    # return render(request, template_name, context)
# def search_location_detail(request, pk):
#     info=models.Item_details.objects.get(item_no=pk)
#     template_name='search_location_detail.html'
#     context={'info':info}
#     return render(request, template_name, context)

# def search_location_detail(request):
#     obj=models.Item_details.objects.all()
#     params={
#         'obj':obj
#     }
#     file_name, status=save_pdf(params)
#     if not status:
#         return Responce({'status': 400})
#     return Responce({'status':200, 'path':f'/media/{file_name}.pdf'})
#end here vishnu

# from django.http import FileResponse
# from io import BytesIO
# from django.template.loader import get_template
# from xhtml2pdf import pisa


# def render_to_pdf(template_src, context_dict={}):
#     template= get_template(template_src)
#     html=template.render(context_dict)
#     result=()
#     pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content)



# def keyword_location_search(request):
    
#     all_location=models.railwayLocationMaster.objects.all()
#     # all_location=models.railwayLocationMaster.objects.filter(location_description__icontains=query)
#     print(all_location, 'ggggggggggggggggggggggggggggggggg')

#     template_name='keyword_location_search.html'
#     context={'all_location':all_location}
#     return render(request, template_name ,context)



    # if request.method== 'POST':
    #     person = request.POST['person']
    #     print(person)
        
    #     des_location=models.MyUser.objects.filter(username__icontains=person )
    #     print('des_location', des_location)
    #     return render(request,'keyword_location_search.html', {'des_location':des_location})
    # else:
    #     person = False
    # all_location=models.railwayLocationMaster.objects.all()
        
    #     print('HELLO')
        
    #     # all_location=models.railwayLocationMaster.objects.none()
    # else:
    #     all_unit=models.railwayLocationMaster.objects.filter(rly_unit_code__icontains=query)
    #     all_location_code=models.railwayLocationMaster.objects.filter(location_code__icontains=query)
    #     all_location_type=models.railwayLocationMaster.objects.filter(location_type__icontains=query)
    #     all_location=all_unit.union(all_location_code).union(all_location_type)
    # # if all_location.count()== 0:
    #     messages.warning(request, "No search result found. Please refine your query ")
    
    #searching filter data
    # insp = []
    # if request.method == 'POST':
    #     q=request.POST.get('location')
    #     q1=request.POST.get('location1')
    #     multiple_q=Q(Q(location_description__contains=q) | Q(parent_location_code__contains=q1))
    #     insp=models.railwayLocationMaster.objects.filter(multiple_q, location_type__in=['DIV','ZR']).values('location_code','location_type','last_update','rly_unit_code')
    #     print('ghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh', insp)
    # else:
    #     print('hehhhhhhhhhhhhhhhhhhhhhh')
    
    #Find division
    # ins=[]
    # if request.method =="POST":
    #     s=request.POST.get('location')
    #     list3=models.railwayLocationMaster.objects.filter(location_type='DIV', parent_location_code=s).values('location_code', 'parent_location_code')
    #     list4=[]
    #     for i in list3:
    #         print(i['location_code'],'_________')
    #         list4.append(i['location_code'])
    #     print('dhhddddddddddddddddddd',ins)
    # else:
    #     print('hhhhhhhhhhhhhh',ins)
        
    #find all list data 
    # insp=models.Level_Desig.objects.filter(rly_unit__location_type__in=['DIV', 'ZR']).values('cat_id','designation','rly_unit__location_code','rly_unit__location_type','rly_unit__last_update','rly_unit__rly_unit_code','department_code__department_name')
    # insp=models.Level_Desig.objects.all().values('cat_id','rly_unit__location_type','designation','rly_unit__last_update','department_code__department_name')
    # print("insp",insp)


# def search_editchecklist(request, pk):    
#     inspection_Checklist=models.Inspection_Checklist.objects.get(checklist_id=pk)
#     ass=models.Inspection_Activity.objects.filter(checklist_id=int(inspection_Checklist.checklist_id)).values('activities')
#     if request.method =='POST':
#         inspection_Checklist.checklist_title=request.POST.get['checklist_title']
#         inspection_Checklist.inspection_type=request.POST.get['inspection_type']
#         ass.activities=request.POST.getlist['activities']
#         inspection_Checklist.status=request.POST.get['draft']
#         inspection_Checklist.save()
#         for i in range(len(ass.activities)):
#             ass.inspection_Activity=models.Inspection_Activity(activities=ass.activities[i])
#             ass.inspection_Activity.checklist_id=Inspection_Checklist.objects.get(checklist_id=inspection_Checklist.checklist_id)
#             ass.save()
#         return redirect('/search_list_created_checklist/')
#     return render(request, 'search_createchecklist.html',{'ass':ass, 'inspection_Checklist':inspection_Checklist, "INSPECTION_TYPE":INSPECTION_TYPE })
