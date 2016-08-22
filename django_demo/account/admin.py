from django.contrib import admin

from .models import Role


# Register your models here.


class RoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ['user']


admin.site.register(Role, RoleAdmin)
