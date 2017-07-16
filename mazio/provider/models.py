from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()
    language = models.CharField(max_length=2)
    currency = models.CharField(max_length=3)
