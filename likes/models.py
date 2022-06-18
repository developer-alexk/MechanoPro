from django.db import models

from users.models import Account

class Likes(models.Model):
    user_liked = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="user_liked")
    liked_by = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="liked_by")