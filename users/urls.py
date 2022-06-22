
from django.contrib import admin
from django.urls import path, include
from users.views import admin_home, chat, company_details, customer_home, edit_profile, engeneer_home, index, logout_view, otp, profile, register, engeneer_infor, register_as_engineer,social_media_update
app_name = 'users'

urlpatterns = [
    path('',index, name='index'),
    path('company/<int:company_id>/',company_details, name='company_details'),
    path('customer/home/',customer_home, name='customer_home'),
    path('engeneer/home/',engeneer_home, name='engeneer_home'),
    path('engeneer/more_infor/',engeneer_infor, name='engeneer_infor'),
    #social Media Update
    path('engeneer/social_media_update/',social_media_update, name='social-media'),
    path('super/home/',admin_home, name='admin_home'),
    path('customer/chat',chat, name='chat'),
    path('register/',register, name='register'),
    path('register_engeneer/',register_as_engineer, name='register_as_engineer'),
    path('user/profile/',profile, name='profile'),
    path('user/profile/edit/',edit_profile, name='profile_edit'),
    path('logout/',logout_view, name='logout_view'),
    path('otp/',otp, name='otp'),
]
