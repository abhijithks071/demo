"""
URL configuration for pwdnew project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from tkinter.font import names

from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('contact',views.contact),
    path('login',views.login),
    path('registration',views.registration),
    path('auth_log', views.auth_log),
    path('authority_reg',views.authority_reg),
    path('about',views.about),



    path('adminhome',views.adminhome,name='adminhome'),
    path('about_admin',views.about_admin),
    path('user_data',views.user_data,name='user_data'),
    path('add_workers/<int:id>',views.add_workers,name='add_workers'),

    path('authorityhome',views.authorityhome),
    path('view_comp',views.view_comp),

    path('logout',views.logout,name='logout'),
    # path('complaints',views.complaints),


    path('userhome',views.userhome),
    path('about_user',views.about_user),
    path('complaint_list_user',views.complaint_list_user,name='complaint_list_user'),
    path('edit_profile',views.edit_profile),






path('feedback', views.feedback_submit, name='feedback'),
path('feedback_list', views.feedback_list, name='feedback_list'),
path('complaints', views.complaint_submit, name='complaints'),
path('complaint_submit', views.complaint_submit, name='complaint_submit'),
path('complaint_list', views.complaint_list, name='complaint_list'),
path('progress_report', views.progress_submit, name='progress_report'),
path('progress_list', views.progress_list, name='progress_list'),
# path('progress_submit', views.progress_submit, name='progress_submit'),

path('make_payment/<int:complaint_id>/', views.make_payment, name='make_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),

path('forgot', views.forgot_password),
path('reset_password/<token>', views.reset_password),


]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
