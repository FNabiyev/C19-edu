from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    is_director = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_reception = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.is_student:
            text = 'Student ' + self.first_name + " " + self.last_name
        elif self.is_teacher:
            text = 'Teacher ' + self.first_name + " " + self.last_name
        else:
            text = self.first_name + " " + self.last_name
        return text

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

class Direction(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()

    def __str__(self):
        return self.name

class Groups(models.Model):
    name = models.CharField(max_length=255)
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, related_name='direct')
    kvota = models.IntegerField()
    teacher = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name='teach')
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Membership(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='group')
    student = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='student')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group.name


class Kirim(models.Model):
    summa = models.IntegerField()
    izoh = models.TextField()
    student = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.summa)


class Chiqim(models.Model):
    summa = models.IntegerField()
    izoh = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.summa)
