from django.shortcuts import render

def index(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        print(phone)
        password = request.POST.get('password')
        print(password)

        if phone == '123' and password == '123':
            return render(request, 'customer/home.html')
        else:
            phone == '321' and password == '321'
            return render(request, 'engineer/home.html')

    return render(request, 'index.html')