from .models import NewUser
from django import forms


class NewUserForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = ['username','email']