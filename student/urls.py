from django.urls import path
from .views import *

urlpatterns = [
    path('', Home),
    path('resource/', Resource),
    path('homework/', Homework),
]