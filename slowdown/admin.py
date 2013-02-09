# coding: utf-8

from django.contrib import admin

from slowdown.models import UserSlowDown


class UserSlowDownAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'slowdown_type']
    list_filter = ['slowdown_type']


admin.site.register(UserSlowDown, UserSlowDownAdmin)
