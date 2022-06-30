"""inspection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inspects import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('login/',views.loginUser,name='loginUser'),
    path('forgotPassword/',views.forgotPassword,name='forgotPassword'),

    #bharti start
    path('created_checklist/',views.created_checklist,name="created_checklist"),
    path('create_inspection_form/',views.create_inspection_form,name="create_inspection_form"),
    path('save_draft_data/',views.save_draft_data,name="save_draft_data"),
    path('nominate_officer/',views.nominate_officer,name="nominate_officer"),
    path('compliance_form/',views.compliance_form,name="compliance_form"),
    path('compliance_filterdata/',views.compliance_filterdata,name="compliance_filterdata"),
    path('compliance_filterdata_ajax',views.compliance_filterdata_ajax,name="compliance_filterdata_ajax"),
    #bharti end
    path('search_location/',views.search_location,name="search_location"),
    path('keyword_location_search/',views.keyword_location_search,name="keyword_location_search"),
    path('search_desig_ajax/',views.search_desig_ajax, name='search_desig_ajax'),
    path('search_locat_ajax/',views.search_locat_ajax, name='search_locat_ajax'),
    path('fetch_desig_ajax',views.fetch_desig_ajax, name='fetch_desig_ajax'),
    
    path('search_location_detail/<str:pk>/',views.search_location_detail,name="search_location_detail"),
    path('search_createchecklist/',views.search_createchecklist,name="search_createchecklist"),
    path('search_editchecklist/<str:pk>/',views.search_editchecklist,name="search_editchecklist"),
    path('search_delete_flag/<str:pk>/',views.search_delete_flag,name="search_delete_flag"),
    path('search_list_created_checklist/',views.search_list_created_checklist,name="search_list_created_checklist"),
    path('search_checklist_detail/<str:pk>/',views.search_checklist_detail,name="search_checklist_detail"),
    path('search_checklist_views/<str:pk>/',views.search_checklist_views,name="search_checklist_views"),

    
    # path('search_location_detail/',views.search_location_detail,name="search_location_detail"),
   



    

]
