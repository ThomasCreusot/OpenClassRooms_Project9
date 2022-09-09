
from dataclasses import field, fields

from turtle import textinput
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
    
    rating_CHOICES = [('0', '-0'), 
               ('1', '-1'),
               ('2', '-2'),
               ('3', '-3'),
               ('4', '-4'),
               ('5', '-5')]
    rating_choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=rating_CHOICES)

    class Meta:
        model = Review
        # exclusion of user field, as it is the connected user by default (see views.py) 
        #fields = '__all__'
        fields = ['headline', 'rating', 'body', "rating_choice_field"]
        #rating excluded for radio buttons presentation
        exclude = ('user', 'ticket', 'rating')
    

     

"""
class DisplayTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
"""


# https://docs.djangoproject.com/fr/4.1/topics/forms/modelforms/
# the Field 'follows' is a ManyToManyField, then : 
# by default : ModelMultipleChoiceField in the form

User = get_user_model()
class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['follows']
        # excluded as widgets = {'follows': forms.TextInput} does not work and I need an input form
        exclude = ('follows',)

# Role is to get an input field and not a many to many field 
class FollowUsersForm_input(forms.Form):
    user_to_follow = forms.CharField(max_length=100)

