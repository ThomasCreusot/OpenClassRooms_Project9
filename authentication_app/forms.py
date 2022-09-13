from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    """Represents a login form"""

    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')


class SignupForm(UserCreationForm):
    """Represents a sign up form"""

    class Meta(UserCreationForm.Meta):
        # get_user_model() allows to get the User model without importing it directly
        model = get_user_model()
        fields = ('username',)