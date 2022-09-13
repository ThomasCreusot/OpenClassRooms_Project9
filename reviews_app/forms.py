
from dataclasses import field, fields
from turtle import textinput
from django import forms
from reviews_app.models import Ticket, Review
from django.contrib.auth import get_user_model 


class TicketForm(forms.ModelForm):
    """Reprensents a form to create a ticket"""

    class Meta:
        model = Ticket
        # exclusion of user field, as it is the connected user by default (see views.py) 
        exclude = ('user',)


class ReviewForm(forms.ModelForm):
    """Reprensents a form to create a review"""

    RATING_CHOICES = [('0', '-0'), ('1', '-1'), ('2', '-2'), ('3', '-3'), ('4', '-4'), ('5', '-5')]
    rating_choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=RATING_CHOICES)

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body', "rating_choice_field"]
        # exclusion of user field, as it is the connected user by default (see views.py) 
        # rating field excluded for radio buttons presentation
        exclude = ('user', 'ticket', 'rating')

# https://docs.djangoproject.com/fr/4.1/topics/forms/modelforms/
# the Field 'follows' is a ManyToManyField, then, by default, ModelMultipleChoiceField in the form

user_model = get_user_model()

class FollowUsersForm(forms.ModelForm):
    """Reprensents a form which allows to follow users"""

    class Meta:
        model = user_model
        fields = ['follows']
        # follows field excluded as widgets = {'follows': forms.TextInput} does not work: 
        # need an input form
        exclude = ('follows',)

 
class FollowUsersForm_input(forms.Form):
    """Role: get an input field and not a many to many field"""

    user_to_follow = forms.CharField(max_length=100)
