# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

class DemoModel(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to="demo_images")

    def __str__(self):
        return self.title
class result(models.Model):
    ip = models.GenericIPAddressField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
