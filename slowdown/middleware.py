# coding: utf-8

from slowdown.models import UserSlowDown


class SlowDownMiddleware(object):
    def process_request(self, request):
        user = request.user
        if UserSlowDown.objects.shouldslowdown(user):
            slowdown = UserSlowDown.objects.get_slowdown(user)
            slowdown.slowdown()
