from django.db import models

from users.models import Account

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="user_account")
    company =  models.ForeignKey(Account,on_delete=models.CASCADE,related_name="user_company")