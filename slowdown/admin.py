# coding: utf-8

from django.contrib import admin

from slowdown.models import UserSlowdown


class UserSlowdownAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'slowdown_type']
    list_filter = ['slowdown_type']


admin.site.register(UserSlowdown, UserSlowdownAdmin)
