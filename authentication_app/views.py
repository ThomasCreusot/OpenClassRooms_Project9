from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout

from django.views.generic import View

# Create your views here.

# Login page : based on functions
# ->Modification of urls.py: path('', authentication_app.views.login_page, name='login'), # '' because at root the of the project
"""
def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')  # Link between authentication_app and reviews_app
            else:
                message = 'Identifiants invalides.'
    return render(request, 'authentication_app/login.html', context={'form': form, 'message': message})
"""

# Login page : based on class 
# ->Modification of urls.py: path('', authentication.views.LoginPageView.as_view(), name='login'),
class LoginPageView(View):
    template_name = 'authentication_app/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})


def logout_user(request):
    logout(request)
    return redirect('login')


