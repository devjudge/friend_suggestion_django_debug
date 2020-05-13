# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class friend_suggestor(models.Model):
    username = models.CharField(max_length=200, unique=True)
    friends = models.TextField()
    friend_request = models.TextField()
    request_pending = models.TextField()
