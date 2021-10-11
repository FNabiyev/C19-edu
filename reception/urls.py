from django.urls import path
from .views import *

urlpatterns = [
    path('', Home),
    path('group/<int:sts>', Group),
    path('students/<int:gr>', Students),
    path('add-group/', AddGroup),
    path('add-student/', AddStudent),
    path('kirim/', KirimView),
    path('add-kirim/', AddKirimView),
    path('chiqim/', ChiqimView),
    path('getdata/', GetData),
    path('getchart/', GetChart),
]