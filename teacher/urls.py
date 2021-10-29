from django.urls import path
from .views import *

urlpatterns = [
    path('', Home),
    path('guruhlarim/', Guruhlarim),
    path('students/<str:nomi>/', Students),
    path('students2/', Students2),
    path('resource/<str:nomi>/', Resource),
    path('create-resource/', CreateResource),
]
