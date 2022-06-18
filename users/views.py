from datetime import datetime
from distutils.ccompiler import gen_lib_options
import email
from unicodedata import category
from django.shortcuts import redirect, render
from grpc import services
from psutil import users
from pytz import utc
from config.sms import send_otp_to_validate_phone
from likes.models import Likes
from otp.models import Otps
from otp.views import random_number_generator
from ratings.models import Rattings, calculate_rating
from users.forms import UserUpdateForm

from users.models import Account, Company

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

@login_required
def profile(request):
    return render(request, 'customer/profile.html')

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
            if user.is_activated == False:
                messages.error(request, 'Account Not Activated Visit Support')
                return redirect('users:index')
            if user.role == "Customer":
                return redirect('users:customer_home')
            if user.role == "Engeneer":
                return redirect('users:engeneer_home')

        # for acc in acc:
        #     print(acc.phone_number)
        #     if acc.phone_number == phone_number:
        #         print(acc.is_parent)
        #         if acc.is_parent == True:
        #             return redirect("users:customer-home")
        #         if acc.is_child == True:
        #             return redirect("users:engineer-home")

    return render(request, 'index.html')

@login_required
def customer_home(request):
    campanies = Company.objects.all()
    


    
    engeneers = Company.objects.all().order_by('-id')
    data = {
        "engeneers" : engeneers,
    }

    return render(request, 'customer/home.html',data)

def company_details(request,company_id):
    if request.method == "POST":
        rating = request.POST.get('rate')
        comment = request.POST.get('comment')
        print(rating)
        print(comment)
        user = Account.objects.get(id=request.user.id)
        company = Company.objects.get(id=company_id)

        #Check if user has already rated the company and decline the request if they have
        if Rattings.objects.filter(user=user,company=company):
            cal_rate = calculate_rating(company_id=company_id)
            Company.objects.filter(id=company_id).update(rating=cal_rate)
            print("Already Rated")
            messages.error(request, 'You have already rated this company')
            return redirect('users:company_details',company_id=company_id)

        try:
            Rattings(
            rating = rating,
            comment = comment,
            user = user,
            company = company
            ).save()
            print("Saved")

            messages.error(request, 'Thanks For Rating Us')

            cal_rate = calculate_rating(company_id=company_id)
            Company.objects.filter(id=company_id).update(rating=cal_rate)


        except:
            cal_rate = calculate_rating(company_id=company_id)
            Company.objects.filter(id=company_id).update(rating=cal_rate)
            print("Failed")


    company = Company.objects.get(id=company_id)
    ratings = Rattings.objects.all().filter(company=company)



    #Print number of ratings
    print(len(ratings))

    #Calculate average rating
    cal_rate = calculate_rating(company_id=company_id)
    print("Rating", cal_rate)

    data = {
        "company" : company,
        "ratings" : ratings,
        "cal_rate" : cal_rate
    }
    return render(request,'customer/company_details.html',data)

@login_required
def engeneer_home(request):
    data = {
    }
    return render(request, 'engeneer/home.html',data)

@login_required
def chat(request):
    return render(request, 'customer/chat.html')

@login_required
def admin_home(request):
    female = Account.objects.filter(gender="Female")
    male = Account.objects.filter(gender="Male")
    users = Account.objects.all().order_by('-id')
    data = {
        'users':users,
        'male':male,
        'female':female
    }
    return render(request, 'admin/home.html',data)


def register(request):
    data = {}
    if request.method == "POST":
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        pin = request.POST.get('password')
        role = request.POST.get('role')
        print(role)
        print(username)
        print(phone)

        #if phone number starts with 07 remove the 0 and add +254
        if phone[0] == '0':
            phone = phone[1:]
            phone = '+254'+phone
        
        #if phone number does not start with + append + 
        elif phone[0] != '+':
            phone = '+'+phone

        #check if the phone number is already registered
        if Account.objects.filter(phone_number=phone).exists():
            print("phone number already registered")
            messages.info(request, f"Phone number already registered")
            return redirect('users:register')

    

        #     create a custom user with the phone number as the username and email backend as the password
        parent = Account(
            phone_number = phone,
            user_name = username,
            password=make_password(pin),
            role = role,
        )
        
        parent.save()
        
        messages.info(request, f"You are now registered as {username}")

        user = authenticate(request,username=phone,password=pin)
        login(request,parent)

        if request.user.role == "Customer":
            Account.objects.filter(id=request.user.id).update(is_activated=True)
            return redirect('users:customer_home')

        if request.user.role == "Engeneer":
            return redirect('users:engeneer_infor')
            # return redirect('users:engeneer_home')

        

    #     phonenumber = phone
    #     otp_number = random_number_generator(size=4)
    #     try:
    #         #Check number if it exist
    #         check_number_if_otp_exists = Otps.objects.filter(phone_number=phone)
    #     except:
    #         check_number_if_otp_exists = {}
            
    #     if bool(check_number_if_otp_exists) == False:
    #         otp = Otps(
    #                 phone_number = phone,
    #                 otp = otp_number
    #         )
    #         print(otp_number)
    #         send_otp_to_validate_phone(
    #             phone=phone,
    #             otp=otp_number
    #         )
    #         otp.save()
    #         print("OTP Saved Sucessfull")

    #             # add otp id to the user model to authenticate before login
    #         try:
    #             Account.objects.filter(phone_number=phone).update(
    #                     otp=Otps.objects.filter(otp=otp_number))
    #         except:
    #             print("none")

    #     elif bool(check_number_if_otp_exists) == True:
    #         new_otp = Otps.objects.filter(phone_number=phone).update(otp=otp_number)
    #         print(otp)
    #         print("OTP updated")
    #         send_otp_to_validate_phone(
    #             phone=phone,
    #             otp=otp_number
    #         )
    #         messages.info(request, f"OTP has been sent to your phone number")

    #     return redirect('otp/?phone='+phone)

    # # except:
    # #     return redirect('users:ptc-register')
    # print("Done")

    return render(request,'customer/register.html',data)

def engeneer_infor(request):
    if request.method == "POST":
        bio = request.POST.get('bio')
        service = request.POST.get('service')
        name = request.POST.get('name')
        location = request.POST.get('location')
        avatar = request.POST.get('avatar')
        print(service)
        print(bio)
        print(name)
        print(location)
        print(avatar)

        user = Account.objects.get(id=request.user.id)

        try:
            company = Company.objects.create(
            service = service,
            bio = bio,
            name = name,
            location = location,
            avatar = avatar,
            user = user
            )
            company.save()
            print("Saved")
            Account.objects.filter(id=request.user.id).update(is_activated=True)
            print("Done")

            return redirect('users:engeneer_home')
        except:
            print("Failed")

    return render(request,'engeneer/infor.html')

@login_required
def otp(request):
    if request.method == "POST":
        phone = request.GET.get('phone')
        otp = request.POST.get('otp')
        phone = str(phone)
        phone = phone[len(phone)-12:]
        print(phone)

        #Validate otp to authenticate the user
        validate_otp = Otps.objects.all()
        print("test1")
        for otps in validate_otp:
            print(otps.otp)
            db_phone = str(otps.phone_number)
            print(db_phone)
            new_db_phone = db_phone.replace('+', '')
            if  str(otp) == str(otps.otp) and str(phone)==new_db_phone:
                print("test3")
                if datetime.now().replace(tzinfo=utc) <= (otps.expire_at.replace(tzinfo=utc)):
                    print("test4")
                # update validation and mark the otp was successfully validated
                    Otps.objects.filter(otp=otp).update(is_otp_authenticated=True)

                    print("Authenticated")
                    return redirect('users:customer_home')
                else:
                    print("Fail")
                    

            else:
                print("fail2")
    return render(request,'customer/otp.html')

from django.contrib.auth.decorators import login_required
@login_required
def edit_profile(request):
    if request.method == 'POST':
        avatar = request.POST.get('avatar')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        try:
            #update the account details of the loged in user
            Account.objects.filter(phone_number=request.user.phone_number).update(
               avatar=avatar,
                phone_number=phone,
                email=email
            )
            messages.info(request, f"Profile updated")
            return redirect('users:profile_edit')
        except:
            messages.info(request, f"Profile Not Updated")

        

    return render(request,'customer/edit_profile.html')
