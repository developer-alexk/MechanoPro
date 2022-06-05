from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    is_engeneer = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
