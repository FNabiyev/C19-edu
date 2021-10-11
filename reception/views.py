from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from django.db.models import Sum, Count


def GetChart(request):
    data = {
        'kirim':[28, 58, 39, 45, 10, 55, 68, 39, 45, 30, 55, 68],
        'chiqim':[40, 28, 50, 48, 50, 39, 41, 50, 48, 63, 39, 41]
    }

    return JsonResponse({'data': data})


def Home(request):
    date = datetime.now()
    month1 = date.month
    year1 = date.year
    if month1 == 12:
        month2 = 1
        year2 = year1 + 1
    else:
        month2 = month1 + 1
        year2 = year1

    date1 = datetime(year1, month1, 1)
    date2 = datetime(year2, month2, 1)

    kirimlar = Kirim.objects.filter(date__gte=date1, date__lt=date2).aggregate(kirim=Sum('summa'))
    chiqimlar = Chiqim.objects.filter(date__gte=date1, date__lt=date2).aggregate(chiqim=Sum('summa'))
    student1 = Membership.objects.filter(group__status=1).annotate(oquvchi=Count('student')).count()
    student2 = Membership.objects.filter(group__status=2).annotate(oquvchi=Count('student')).count()
    data = {
        'kirim': kirimlar,
        'chiqim': chiqimlar,
        'student1': student1,
        'student2': student2
    }
    context = {
        'classhome': 'active open',
        'groups': Groups.objects.all(),
        'data': data
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


def GetData(request):
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    print(date1, date2)

    kirim = Kirim.objects.filter(date__gte=date1, date__lt=date2)
    kirims = []
    for i in kirim:
        t = {
            'summa': i.summa,
            'izoh': i.izoh,
            'first_name': i.student.first_name,
            'last_name': i.student.last_name,
            'date': i.date.strftime('%H:%M %d.%m.%Y'),
        }
        kirims.append(t)
    dt = {
        'kirimlar': kirims
    }
    return JsonResponse(dt)
