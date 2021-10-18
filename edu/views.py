from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from reception.models import Users

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_reception:
                login(request, user)
                return redirect('/reception/')
            elif user.is_student:
                login(request, user)
                return redirect('/student/')
            elif user.is_director:
                login(request, user)
                return redirect('/director/')
            else:
                return render(request, 'login.html')
        else:
            messages.error(request, 'Login yoki Parol notogri kiritildi!')
            return redirect('/login/')
    else:
        return render(request, 'login.html')

def Logout(request):
    logout(request)
    messages.success(request, "Tizimdan chiqish muvaffaqiyatli yakunlandi!")
    return redirect('/login/')

def Register(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        birthday = request.POST['birthday']
        address = request.POST['address']
        photo = request.FILES['photo']
        # student = request.POST['student']
        student = request.POST.get('student')
        teacher = request.POST.get('teacher')
        reception = request.POST.get('reception')
        print(student, teacher, reception)

        user = authenticate(request, username=username, password=make_password(password))
        if user is None:
            if student:
                Users.objects.create(username=username, password=password, first_name=first_name, last_name=last_name, phone=phone, birthday=birthday, address=address, photo=photo, is_student=True)
            elif teacher:
                Users.objects.create(username=username, password=password, first_name=first_name, last_name=last_name, phone=phone, birthday=birthday, address=address, photo=photo, is_teacher=True)
            elif reception:
                Users.objects.create(username=username, password=password, first_name=first_name, last_name=last_name, phone=phone, birthday=birthday, address=address, photo=photo, is_reception=True)

        return redirect('/login/')
    elif request.method =="GET":
        # username = request.GET.get('username')
        # password = request.GET.get('password')
        # age = request.GET.get('age')
        # print(username, password, age)

        return render(request, 'register.html')