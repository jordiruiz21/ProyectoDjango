from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

class MyUserAdmin(UserAdmin):
    model = MyUser

    list_display = ('email', 'username', 'is_active', 'is_staff', 'create_date')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    ordering = ('email',)
    search_fields = ('email', 'username')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('username', 'birthdate')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'create_date', 'update_date')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'username', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    readonly_fields = ('create_date', 'update_date', 'last_login')

admin.site.register(MyUser, MyUserAdmin)
