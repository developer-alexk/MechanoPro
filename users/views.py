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
    username = password = ''

    if request.method == "POST":
        password = request.POST['password']
        phone_number = request.POST['phone']
        #if phone number starts with 07 remove the 0 and add +254
        if phone_number[0] == '0':
            phone_number = phone_number[1:]
            phone_number = '+254'+phone_number
        
        #if phone_number number does not start with + append + 
        elif phone_number[0] != '+':
            phone_number = '+'+phone_number

        #if user does not exist to return a message to the user
        if not Account.objects.filter(phone_number=phone_number):
            messages.error(request, 'User does not exist')
            return redirect('users:index')
        

        # password = make_password('password')
        # print(password)
        user = authenticate(username=phone_number, password=password)
        # if user is not None:
        login(request,user)
        acc = Account.objects.all()

        

        if user.is_authenticated:
            if user.is_engineer == True:
                return redirect('users:engineer_home')
            if user.is_customer == True:
                return redirect('users:customer_home')

        # for acc in acc:
        #     print(acc.phone_number)
        #     if acc.phone_number == phone_number:
        #         print(acc.is_parent)
        #         if acc.is_parent == True:
        #             return redirect("users:customer-home")
        #         if acc.is_child == True:
        #             return redirect("users:engineer-home")

    return render(request, 'index.html')



def customer_home(request):
    engineer = Account.objects.filter(is_engeneer=True)
    data = {
        'engineer': engineer
    }
    return render(request, 'customer/home.html',data)

def engineer_home(request):
    return render(request, 'engineer/home.html')