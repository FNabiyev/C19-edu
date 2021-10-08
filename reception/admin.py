from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'birthday', 'phone', 'address')}),
        (_('Permissions'), {
            'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_director', 'is_manager', 'is_teacher', 'is_reception', 'is_student'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = (
        'id', 'username', 'first_name', 'last_name', 'phone', 'birthday', 'is_superuser',
        'is_director',
        'is_manager', 'is_teacher', 'is_reception', 'is_student')
    list_display_links = ('id', 'username')


admin.site.register(Users, UserAdmin)
admin.site.register(Direction)
admin.site.register(Groups)
admin.site.register(Membership)
admin.site.register(Kirim)
admin.site.register(Chiqim)