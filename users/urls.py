from django.contrib import admin
from django.urls import path, include
from users.views import customer_home, engineer_home, index, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name='index'),
    path('customer/home/',customer_home, name='customer_home'),
    path('engineer/home/',engineer_home, name='engineer_home'),
    path('logout/',logout_view, name='logout_view'),
]

admin.site.site_header == "JUA KALI"
