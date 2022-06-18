from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import Account



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Account
        fields = ['user_name','email','avatar','phone_number']
