from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from boreas_web.models import Client,Device

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','email',)

class SignUpForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ('phone','country','city','zipcode','address', 'password1', 'password2', )

class CreateDeviceForm(forms.ModelForm):
    class Meta:
        model=Device
        fields=('uuid','name','aka','country','description','zipcode')

class EditDeviceForm(forms.ModelForm):
    class Meta:
        model=Device
        fields=('uuid','name','aka','country','description','zipcode')