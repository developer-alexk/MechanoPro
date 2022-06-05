from django.shortcuts import redirect, render

from users.models import Account

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth.hashers import make_password

#create logout logic
from django.contrib.auth.decorators import login_required

@login_required
def logout_view(request):
    logout(request)
    return redirect('users:index')

def index(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        print(phone)
        password = request.POST.get('password')
        print(password)

        if phone == '123' and password == '123':
            return redirect('/customer/home')
        else:
            phone == '321' and password == '321'
            return redirect('/engineer/home')

    return render(request, 'index.html')

def customer_home(request):
    engineer = Account.objects.filter(is_engeneer=True)
    data = {
        'engineer': engineer
    }
    return render(request, 'customer/home.html',data)

def engineer_home(request):
    return render(request, 'engineer/home.html')