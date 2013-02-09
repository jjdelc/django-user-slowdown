# coding: utf-8

from time import sleep
from random import random

from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.contrib.auth.models import User


SLOWDOWN_USER_IDS_CACHE_KEY = getattr(settings,
    'SLOWDOWN_USER_IDS_CACHE_KEY', 'django-user-slowdown:slow-users')
SLOWDOWN_USER_VALUES_CACHE_KEY = getattr(settings,
    'SLOWDOWN_USER_VALUES_CACHE_KEY', 'django-user-slowdown:slow-users-values')
SLOWDOWN_USER_CACHE_TIMEOUT = getattr(settings,
    'SLOWDOWN_USER_CACHE_TIMEOUT', 60 * 60 * 24 * 7) # 1 week


def _populate_cache():
    val = list(UserSlowDown.objects.all().values_list('user__id', flat=True))
    cache.set(SLOWDOWN_USER_IDS_CACHE_KEY, val, SLOWDOWN_USER_CACHE_TIMEOUT)


def _slowed_down_user_ids():
    val = cache.get(SLOWDOWN_USER_IDS_CACHE_KEY)
    if val is None:
        _populate_cache()
        val = cache.get(SLOWDOWN_USER_IDS_CACHE_KEY)

    return val


class UserSlowDownManager(models.Manager):

    def shouldslowdown(self, user):
        return user.id in _slowed_down_user_ids()

    def get_slowdown(self, user):
        return self.get(user=user)


class UserSlowDown(models.Model):
    FIXED_SLOWDOWN = 1
    RANDOM_SLOWDOWN = 2
    SLOWDOWN_TYPES = [
        (FIXED_SLOWDOWN, 'Fixed slowdown'),
        (RANDOM_SLOWDOWN, 'Random slowdown'),
    ]

    user = models.ForeignKey(User)
    slowdown_type = models.PositiveIntegerField(choices=SLOWDOWN_TYPES,
        default=RANDOM_SLOWDOWN)
    slowdown_value = models.FloatField(default=1.0)
    slowdown_min_value = models.FloatField(default=0.0,
        help_text='Only used with random slowdowns')
    sporadic_failure = models.BooleanField(default=False)
    failure_rate = models.FloatField(help_text='% float between 0 and 1',
        default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserSlowDownManager()

    def get_slowdown(self):
        if self.is_fixed_slowdown():
            return self._fixed_slowdown(self.slowdown_value)
        return self._random_slowdown(self.slowdown_min_value,
            self.slowdown_value)

    def _fixed_slowdown(self, value):
        return value

    def _random_slowdown(self, min_val, max_val):
        return min_val + random() * (max_val - min_val)

    def is_fixed_slowdown(self):
        return self.slowdown_type == self.FIXED_SLOWDOWN

    def slowdown(self):
        timeout = self.get_slowdown()
        sleep(timeout)

    def save(self, *args, **kwargs):
        super(UserSlowDown, self).save(*args, **kwargs)
        _populate_cache()

    def delete(self, *args, **kwargs):
        super(UserSlowDown, self).delete(*args, **kwargs)
        _populate_cache()

    def get_failure_response(self):
        return HttpResponse('Error, Try again', status=400)

    def should_fail(self):
        if not self.sporadic_failure:
            return False
        return random() < self.failure_rate        

