from itertools import chain

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from reviews_app.forms import TicketForm, ReviewForm, FollowUsersForm

# Feed creation (flux)
from . import models

from django.db.models import Q

# Create your views here.



#UTILISER Q OBJECTS ICI POUR COMBINER L'EXCLUSION DES TICKETS ASSOCIES A DES REVIEWS ET UNE AUTRE CONDITION (relation avec user par exemple)

@login_required
def home(request):
    #LIMITER LES TICKETS AFFICHES A CEUX DES UTILISATEURS SUIVIS
    #code originel
    #reviews = models.Review.objects.all()
    reviews = models.Review.objects.filter(
        # the user can see the reviews writen by users he/she follows
        Q(user__in=request.user.follows.all())|
        # the user can see the reviews he/she wrote
        Q(user=request.user)|
        # the user can see the reviews in response to tickets he/she wrote (event if the response
        # was writen by a user he/she does not follow)
        Q(ticket__user=request.user)
    )

    #LIMITER LES TICKETS AFFICHES A CEUX DES UTILISATEURS SUIVIS
    #code originel
    #tickets = models.Ticket.objects.all()
    tickets = models.Ticket.objects.filter(
        # the user can see the tickets writen by users he/she follows
        Q(user__in=request.user.follows.all())|
        # the user can see the tickets he/she wrotes
        Q(user=request.user)
    )



    # We keep only ticket associated to a review
    #tickets_within_a_review = models.Ticket.objects.all().exclude(
    #    review__in=reviews
    #)

    # We keep only ticket not associated to a review
    # exclusion of tickets already associated to a review with __in (field name + __ + in) : without button in HTML
    tickets_without_review = models.Ticket.objects.filter(
        ~Q(review__in=reviews)  # ~ : NOT
    )

    #context = {
    #    'tickets': tickets, 
    #    'reviews': reviews
    #}
    tickets_and_reviews = sorted(
        # itertools.chain: group of querysets --> python: sorted() 
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    context = {'tickets_and_reviews': tickets_and_reviews, 'tickets_without_review':tickets_without_review}
    return render(request, 'reviews_app/home.html', context=context)


'''
@login_required
def review_create(request):
   form = ReviewForm()
   return render(request,
            'reviews_app/review_create.html',
            {'form': form})
'''

@login_required
def ticket_create(request):
    if request.method == 'POST':

        form = TicketForm(request.POST, request.FILES)
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
            # inversion because we save the ticket before the reviewe
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



@login_required
def review_for_a_given_ticket_create(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)  

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():

            # New instance but without saving in database, in order to attribute the user to the ForeignKey
            review = form.save(commit=False)
            # set the connected user to the user before saving the model
            review.user = request.user
            # set the ticket before saving the model
            review.ticket = ticket
            # Save
            review.save()

            # redirige vers la page de détail du groupe que nous venons de créer
            # nous pouvons fournir les arguments du motif url comme arguments à la fonction de redirection
            return redirect('home') # , band.id)
    else:
        form = ReviewForm()
    return render(request,
            'reviews_app/review_create_for_a_ticket.html',
            {'form': form, 'ticket': ticket})



#OLD
#View about following.
#ajouter : user.follows.add(choixDeUserDansLaListe)
#pas besoin d’un through_defaults={‘aaa': ‘blablabla’}) etant donné qu’on a pas encore d’information sur la relation
#Ou alors user.followed_user mais je pense pas


from authentication_app.models import User
from reviews_app.forms import FollowUsersForm_input

"""original code : FUNCTIONAL
    form = FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            #les utilisateurs auxquels on est déja abonnés sont dans request.user.follows.all()
            #print("1.request.user.follows.all()", request.user.follows.all())

            users_we_want_to_follow = form.cleaned_data['follows']

            #ancienne version : user_follow_form = form.save() mais cela effacait les abonnés qu'on avait déja
            #les nouveaux abonnements sont dans user_follow_form.follows.all(), sous forme de QuerySet
            #print("2.user_follow_form", user_follow_form.follows.all())

            request.user.follows.add(*users_we_want_to_follow, through_defaults=None)
            return redirect('home')


    subscriptions = request.user.follows.all()
"""

from django.core.exceptions import ValidationError


@login_required
def follow_users(request):
    #Added only because the client wishes to have an inputField and not a manyToMany field
    input_form = FollowUsersForm_input()

    #initial form for the manyToMany relationship
    form = FollowUsersForm(instance=request.user)

    if request.method == 'POST':
        form = FollowUsersForm(request.POST, instance=request.user)
        input_form = FollowUsersForm_input(request.POST)

        if form.is_valid():

            username_to_follow = request.POST['user_to_follow']

            # Following itself
            if username_to_follow == str(request.user.username):
                raise ValidationError("Vous ne pouvez pas vous abonner à vous même")

            # Already followed
            elif username_to_follow in [user.username for user in request.user.follows.all()]:
                raise ValidationError("Vous êtes déja abonné à {0}".format(username_to_follow))

            # Following
            elif username_to_follow in [user.username for user in User.objects.all()]:
                print("Abonnement de {0}  à {1} réussi".format(request.user.username, username_to_follow))
                
                #retrouver l'utilisateur que l'utilisateur connecté va suivre
                users_we_want_to_follow = User.objects.filter(username = username_to_follow)
                #ajout de l'utilisateur à suivre dans le champ follows de l'utilisateur connecté
                request.user.follows.add(*users_we_want_to_follow, through_defaults=None)

                return redirect('home')

            # User does not exists
            else:
                raise ValidationError("L'utilisateur {0} n'est pas inscrit sur ce site".format(username_to_follow))


            # Before the FollowUsersForm_input()
            # les utilisateurs auxquels on est déja abonnés sont dans request.user.follows.all()
            # print("1.request.user.follows.all()", request.user.follows.all())
            # CODE OK users_we_want_to_follow = form.cleaned_data['follows']

            # ancienne version : user_follow_form = form.save() mais cela effacait les abonnés qu'on avait déja
            # les nouveaux abonnements sont dans user_follow_form.follows.all(), sous forme de QuerySet
            # print("2.user_follow_form", user_follow_form.follows.all())
            # code OK request.user.follows.add(*users_we_want_to_follow, through_defaults=None)
            # code OK return redirect('home')


    subscriptions = request.user.follows.all()
    subscribers = User.objects.filter(follows=request.user)

    return render(request, 'reviews_app/follow_users_form.html', context={'input_form':input_form, 'form': form,'subscriptions': subscriptions, 'subscribers': subscribers})



@login_required
def my_posts(request):
    my_reviews = models.Review.objects.filter(user=request.user)
    my_tickets = models.Ticket.objects.filter(user=request.user)

    my_tickets_and_reviews = sorted(
        chain(my_tickets, my_reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )

    return render(request, 'reviews_app/my_posts.html', {'my_tickets_and_reviews': my_tickets_and_reviews})



@login_required
def ticket_update(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)  

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)  # préremplissage formulaire
        if form.is_valid():
            form.save()
            return redirect('my-posts')
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'reviews_app/ticket_update.html', {'form': form, 'ticket': ticket})


@login_required
def review_update(request, review_id):
    review = models.Review.objects.get(id=review_id)  
    ticket = review.ticket

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)  # préremplissage formulaire
        if form.is_valid():
            form.save()
            return redirect('my-posts')
    else:
        form = ReviewForm(instance=review)  # préremplissage formulaire

    return render(request, 'reviews_app/review_update.html',  {'form': form, 'ticket': ticket})




@login_required
def ticket_delete(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)  

    if request.method == 'POST':
        ticket.delete()
        return redirect('my-posts')
    #no need for else
    return render(request, 'reviews_app/ticket_delete.html', {'ticket': ticket})




@login_required
def review_delete(request, review_id):
    review = models.Review.objects.get(id=review_id)  

    if request.method == 'POST':
        review.delete()
        return redirect('my-posts')
    #no need for else
    return render(request, 'reviews_app/review_delete.html',  {'review': review})

