
from django.contrib import admin
from django.urls import path, include
from users.views import customer_home, engineer_home, index, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('users.urls')),
]
