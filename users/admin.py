from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('email', 'username', 'carrera', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Información académica', {'fields': ('carrera',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'carrera')}),
    )
