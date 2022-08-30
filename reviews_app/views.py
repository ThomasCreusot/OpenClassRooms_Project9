from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from reviews_app.forms import TicketForm, ReviewForm

# Create your views here.

@login_required
def home(request):
    return render(request, 'reviews_app/home.html')


@login_required
def ticket_create(request):
   form = TicketForm()
   return render(request,
            'reviews_app/ticket_create.html',
            {'form': form})

@login_required
def review_create(request):
   form = ReviewForm()
   return render(request,
            'reviews_app/review_create.html',
            {'form': form})
