#!/usr/bin/env python
# coding: utf-8

import os
from distutils.core import setup

version = '0.0.1'

root_dir = os.path.dirname(__file__)
if not root_dir:
    root_dir = '.'

long_desc = open(os.path.join(root_dir, 'README.md')).read()

setup(
    name='Django user slowdown',
    version=version,
    url='https://github.com/jjdelc/django-user-slowdown',
    author=u'Jesús Del Carpio',
    author_email='jjdelc@gmail.com',
    license='BSD License',
    py_modules=['slowdown'],
    packages=[
        'slowdown',
    ],
    description='Middleware to slow down pageloads for unwanted users',
    long_description=long_desc,
)
