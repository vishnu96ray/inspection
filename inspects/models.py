from django.db import models
from asyncio.windows_events import NULL
from inspects import managers
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone
# Create your models here.
from .choices import *

class railwayLocationMaster(models.Model):
    rly_unit_code = models.AutoField(primary_key=True)
    location_code = models.CharField(max_length=10,null=True)
    location_type = models.CharField(max_length=5,null=True)
    location_description = models.CharField(max_length=50)
    parent_location_code = models.CharField(max_length=5)
    last_update = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=30,null=True)
    station_code= models.CharField(max_length=5,null=True)
    rstype= models.CharField(max_length=15,null=True)
    location_type_desc= models.CharField(max_length=10,null=True)




    
class Level_Desig(models.Model):
    id=models.AutoField(primary_key=True)  
    cat_id=models.IntegerField(null=True)    
    designation=models.CharField(max_length=100,null=True)  
    department=models.CharField(max_length=50,null=True)   
    effectdate=models.CharField(max_length=20,null=True)
    un_officer_id=models.IntegerField(null=True)
    level=models.CharField(max_length=2,null=True)
    designation_code = models.CharField(max_length=15,null=True)
    parent_desig_code= models.CharField(max_length=15,null=True)
    department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
    rly_unit=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    pc7_level = models.CharField(max_length=2,null=True)
    



class departMast(models.Model):
    
    department_code = models.CharField(primary_key=True, max_length =10)
    department_name=models.CharField(null = True,max_length =50, blank=True,unique=True)
    rly_unit_code=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
    delete_flag=models.BooleanField(default=False)
    modified_by = models.CharField( max_length=20, blank=True, null=True)
    modified_on=models.DateTimeField(auto_now=True, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)



class error_Table(models.Model):
    log_no=models.BigAutoField(primary_key=True)
    fun_name=models.CharField(max_length=255,null=True,blank=True)
    user_id=models.CharField(max_length=40,null=True,blank=True)
    err_details=models.TextField(null=True,blank=True)
    err_date=models.DateField(auto_now_add=True)

    class meta:
        db_table="error_Table"
#till here Ritika 02-09

class MyUser(AbstractBaseUser):

    username = models.CharField(
        max_length=50, blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    aadhaar_no = models.CharField(max_length=12, null=True)
    email = models.EmailField(verbose_name='email address', unique=True)
    personal_emailID=  models.EmailField(verbose_name='email address', unique=True,null=True)
    official_mobileNo = models.CharField(max_length=10, unique=True,null=True)
    personal_mobileNo= models.CharField(max_length=10, unique=True,null=True)
    faxNo = models.CharField(max_length=10, unique=True,null=True)
    date_of_birth = models.DateField(null=True)
    user_role = models.CharField(max_length=30)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    last_update = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = managers.MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_no', ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name



class Inspection_details(models.Model):
    inspection_no=models.BigAutoField(primary_key=True)
    inspection_note_no=models.CharField(max_length=40, blank=True, null=True)
    inspection_officer=models.CharField(max_length=20, blank=False, null=True)
    inspection_title=models.CharField(max_length=20, blank=False, null=True)
    zone=models.CharField(max_length=10, blank=False, null=False)
    division=models.CharField(max_length=10, blank=False, null=False)
    dept=models.CharField(max_length=10, blank=False, null=True)
    location=models.CharField(max_length=20, blank=False, null=False)
    inspected_on=models.DateTimeField(auto_now=False, null=False)
    modified_on=models.DateTimeField(auto_now=False, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    modified_by=models.CharField(max_length=10, blank=False, null=True)
    created_by=models.CharField(max_length=10, blank=False, null=True)
    report_path=models.CharField(max_length=10, blank=False, null=True)

class Item_details(models.Model):
    item_no=models.BigAutoField(primary_key=True)   
    inspection_no=models.ForeignKey('Inspection_details', on_delete=models.CASCADE, null=True)
    status=models.CharField(max_length=10, blank=False, null=True)
    status_flag=models.IntegerField()
    observation=models.CharField(max_length=500, blank=False, null=True)
    modified_on=models.DateTimeField(auto_now=False, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    modified_by=models.CharField(max_length=10, blank=False, null=True)
    created_by=models.CharField(max_length=10, blank=False, null=True)
    
    
    

class Marked_Officers(models.Model):
    marked_no=models.BigAutoField(primary_key=True)
    marked_to=models.ForeignKey('Designation_Master', on_delete=models.CASCADE, null=True)
    item_no=models.ForeignKey('Item_details', on_delete=models.CASCADE, null=True)
    compliance=models.CharField(max_length=10, blank=False, null=True)
    compliance_recieved_on=models.DateTimeField(auto_now=False, null=True)
    modified_on=models.DateTimeField(auto_now=False, null=True)
    created_on=models.DateTimeField(auto_now=False, null=True)
    modified_by=models.CharField(max_length=10, blank=False, null=True)
    created_by=models.CharField(max_length=10, blank=False, null=True)
    myuser_id=models.ForeignKey('MyUser', on_delete=models.CASCADE, null=True)



class Designation_Master(models.Model):
    designation_master_no=models.BigAutoField(primary_key=True)
    master_name=models.CharField(max_length=40, blank=False, null=False)
    master_email=models.EmailField(verbose_name='email address', unique=True)
    railway_location=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)



class Inspection_Checklist(models.Model):
    checklist_id=models.AutoField(primary_key=True)  
    checklist_title=models.CharField(max_length=100, blank=False, null=False)
    inspection_type=models.CharField(max_length=15, choices=INSPECTION_TYPE, default = '1' )
    status=models.CharField(max_length=10, blank=False, null=False)
    delete_flag=models.BooleanField(default=False)
    created_by=models.CharField(max_length=10, blank=False, null=True)
    created_on=models.DateTimeField(auto_now_add=True,null=True)
    last_modified_by=models.CharField(max_length=10, blank=False, null=True)
    last_modified_on=models.DateTimeField(auto_now_add=True, null=True)
    


class Inspection_Activity(models.Model):
    activity_id=models.AutoField(primary_key=True)  
    checklist_id=models.ForeignKey('Inspection_Checklist', on_delete=models.CASCADE)
    activities=models.CharField(max_length=200, blank=False, null=False)
    delete_flag=models.BooleanField(default=False)
    created_by=models.CharField(max_length=10, blank=False, null=True)
    created_on=models.DateTimeField(auto_now_add=True, null=True)
    last_modified_by=models.CharField(max_length=10, blank=False, null=True)
    last_modified_on=models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.checklist_id)
    

    
    



# class Search_Division(models.Model):
#     inspection_no=models.ForeignKey('Inspection_details', on_delete=models.CASCADE, null=True)
#     department_code=models.ForeignKey('departMast', on_delete=models.CASCADE, null=True)
#     Level_Desig=models.ForeignKey('Level_Desig', on_delete=models.CASCADE, null=True)
#     railway_location=models.ForeignKey('railwayLocationMaster', on_delete=models.CASCADE, null=True)
#     master_name=models.CharField(max_length=40, blank=False, null=False)
#     person_name=models.CharField(max_length=40, blank=False, null=False)
    
    

    
    
    
    