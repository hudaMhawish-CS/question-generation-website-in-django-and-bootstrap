from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control mt-4 input',
        }
    ))
    email = forms.CharField(max_length=50,required=True,widget=forms.EmailInput(
        attrs={
            'class': 'form-control mt-4 input',
        }
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control input',
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control input',
        }
    ))


    class Meta:
        model = User
        fields = ['username','email','password1','password2']