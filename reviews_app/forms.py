from django import forms
from reviews_app.models import Ticket, Review


class TicketForm(forms.ModelForm):
   class Meta:
     model = Ticket
     fields = '__all__'


class ReviewForm(forms.ModelForm):
   class Meta:
     model = Review
     fields = '__all__'
