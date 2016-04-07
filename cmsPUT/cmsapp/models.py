from __future__ import unicode_literals

from django.db import models

# Create your models here.
class WebPageDB(models.Model):
    URL = models.CharField(max_length=128)
    HTMLCode = models.TextField
