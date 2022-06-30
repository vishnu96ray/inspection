from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display=['username','first_name','last_name','aadhaar_no','email','personal_emailID',]

