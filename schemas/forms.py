from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={
            "autofocus": True,
            "placeholder": "Username",
            "class": "form-control font-weight-light"
        }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "placeholder": "Password",
            "class": "form-control font-weight-light"
        }),
    )