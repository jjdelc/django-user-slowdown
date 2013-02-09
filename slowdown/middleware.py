# coding: utf-8

from slowdown.models import UserSlowDown


class SlowDownMiddleware(object):
    def process_request(self, request):
        user = request.user
        if not user.is_authenticated():
            return

        if UserSlowDown.objects.shouldslowdown(user):
            try:
                slowdown = UserSlowDown.objects.get_slowdown(user)
                slowdown.slowdown()
            except UserSlowDown.DoesNotExist:
                pass
