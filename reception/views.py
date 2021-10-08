import json

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *


def Home(request):
    context = {
        'classhome': 'active open',
        'groups': Groups.objects.all(),
    }

    return render(request, 'reception/home.html', context)


def Group(request, sts):
    if sts == 0:
        context = {
            'classgroup': 'active open',
            'groups': Groups.objects.all(),
            'directions': Direction.objects.all(),
            'teachers': Users.objects.filter(is_teacher=True),
        }
    else:
        context = {
            'classgroup': 'active open',
            'groups': Groups.objects.filter(status=sts),
            'directions': Direction.objects.all(),
            'teachers': Users.objects.filter(is_teacher=True),
        }
    return render(request, 'reception/group.html', context)


def Students(request, gr):
    context = {
        'classgroup': 'active open',
        'group': Groups.objects.get(id=gr),
        'students': Membership.objects.filter(group__id=gr),
    }
    return render(request, 'reception/students.html', context)


def AddGroup(request):
    if request.method == "POST":
        group_name = request.POST['group_name']
        kvota = request.POST['kvota']
        direct = request.POST['direct']
        teacher = request.POST['teacher']

        Groups.objects.create(name=group_name, kvota=kvota, direction_id=direct, teacher_id=teacher)
        url = '/reception/group/1'
        return redirect(url)
    else:
        context = {
            'classgroup': 'active open',
            'directions': Direction.objects.all(),
            'teachers': Users.objects.filter(is_teacher=True),
        }
        return render(request, 'reception/add-group.html', context)


def AddStudent(request):
    login = request.POST['login']
    parol = request.POST['parol']
    ism = request.POST['ism']
    fam = request.POST['fam']
    phone = request.POST['phone']
    address = request.POST['address']
    birthday = request.POST['birthday']
    group = request.POST['group']

    usr = Users.objects.create(username=login, password=make_password(parol), first_name=ism, last_name=fam,
                               phone=phone, address=address, birthday=birthday)
    Membership.objects.create(group_id=group, student=usr)

    url = '/reception/students/{}'.format(group)
    return redirect(url)


def KirimView(request):
    context = {
        'classhisob': 'active open',
        'kirimlar': Kirim.objects.all().order_by('-id'),
        'students': Users.objects.filter(is_student=True),
    }
    return render(request, 'reception/kirim.html', context)


def AddKirimView(request):
    summa = request.POST['summa']
    student = request.POST['student']
    izoh = request.POST['izoh']

    Kirim.objects.create(summa=summa, student_id=student, izoh=izoh)

    return redirect('/reception/kirim/')


def ChiqimView(request):
    context = {
        'classhisob': 'active open',
    }
    return render(request, 'reception/chiqim.html', context)


def GetKirim(request):
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    kr = Kirim.objects.filter(date__gte=date1, date__lte=date2).order_by('-id')
    kirim = []
    for i in kr:
        t = {
            'summa':i.summa,
            'first_name':i.student.first_name,
            'last_name':i.student.last_name,
            'izoh':i.izoh,
            'date':i.date.strftime("%H:%M %d.%m.%Y")
        }
        kirim.append(t)
    dt = {
        'kirim':kirim
    }
    return JsonResponse(dt)
