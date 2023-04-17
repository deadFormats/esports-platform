from django import forms


class LoginForm(forms.Form):
    """This is the base login form for authentication. Username will be for auth via
    actual username and via email."""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)