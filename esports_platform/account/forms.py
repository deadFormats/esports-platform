from django import forms
from django.forms import BoundField
from django.utils.safestring import mark_safe
from django.templates.loader import get_template



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    