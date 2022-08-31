from django.shortcuts import render, redirect
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

"""Nous voulons assigner au champ  uploader  de la  Photo  l’utilisateur connecté à ce moment-là.
Vous pouvez créer l’objet  Photo  sans le sauvegarder dans la base de données, en enregistrant le
formulaire avec l’argument commit=False . Ensuite, assignez la valeur correcte à  uploader, et
 enfin, sauvegardez le modèle pour le stocker dans la base de données."""
@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():

            # New instance but without saving in database, in order to attribute the user to the ForeignKey
            ticket = form.save(commit=False)
            # set the connected user to the user before saving the model
            ticket.user = request.user
            # Save
            ticket.save()

            # nous pouvons fournir les arguments du motif url comme arguments à la fonction de redirection
            return redirect('home')  # , band.id)
    else:
        form = TicketForm()
    return render(request,
            'reviews_app/ticket_create.html',
            {'form': form})


@login_required
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():

            # New instance but without saving in database, in order to attribute the user to the ForeignKey
            review = form.save(commit=False)
            # set the connected user to the user before saving the model
            review.user = request.user
            # Save
            review.save()

            # redirige vers la page de détail du groupe que nous venons de créer
            # nous pouvons fournir les arguments du motif url comme arguments à la fonction de redirection
            return redirect('home') # , band.id)
    else:
        form = ReviewForm()
    return render(request,
            'reviews_app/review_create.html',
            {'form': form})

# blog <=> review et photo <=> ticket 
@login_required
def review_and_ticket_upload(request):
    review_form = ReviewForm()
    ticket_form = TicketForm()
    if request.method == 'POST':
        # handle the POST request here
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            # inversion car on save d'abord le ticket
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')

    context = {
        'review_form': review_form,
        'ticket_form': ticket_form,
    }
    return render(request, 'reviews_app/review_and_ticket_create.html', context=context)
