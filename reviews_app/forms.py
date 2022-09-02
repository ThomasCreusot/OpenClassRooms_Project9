from django import forms
from reviews_app.models import Ticket, Review

from django.contrib.auth import get_user_model 


class TicketForm(forms.ModelForm):
   class Meta:
     model = Ticket
     # exclusion of user field, as it is the connected user by default (see views.py) 
     # fields = '__all__'
     exclude = ('user',)


class ReviewForm(forms.ModelForm):
   class Meta:
     model = Review
     # exclusion of user field, as it is the connected user by default (see views.py) 
     #fields = '__all__'
     exclude = ('user', 'ticket',)

"""
class DisplayTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
"""

User = get_user_model()
class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['follows']
