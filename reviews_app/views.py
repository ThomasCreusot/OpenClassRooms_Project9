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
            {'form': form})



#OLD
#View about following.
#ajouter : user.follows.add(choixDeUserDansLaListe)
#pas besoin d’un through_defaults={‘aaa': ‘blablabla’}) etant donné qu’on a pas encore d’information sur la relation
#Ou alors user.followed_user mais je pense pas


from authentication_app.models import User

"""original code : FUNCTIONAL"""
@login_required
def follow_users(request):
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

    # all Users : 
    # subscribers = User.objects.all()

    subscribers = User.objects.filter(
        Q(followed_by__in=str(request.user.id))  # other solution with xxx_set.all() ? https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_many/
        )



    all_users = User.objects.all()

    #les subscribers sont des utilisateurs dont les followers correspondant à l'utilisateur connecté c'est à dire request.user
    # follow_users :  'User' object is not iterable
    # followed_by :  Cannot query "utilisateur2": Must be "UserFollows" instance.
    # following :   Cannot query "utilisateur2": Must be "UserFollows" instance.
    # follows : 'User' object is not iterable
    # d'ou viennent followed by et following ? ce sont les termes de mon modele UserFollows (la table de la relation many to many): 
        #user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        #                    related_name='following')
        #followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        #                    related_name='followed_by')
    # je veux que le followed_by (terme correspondant à followed_user) d'un autre utilisateur que celui est est connecté CORRESPONDE à l'utilisateur connecté   : ce sont les abonnés

    #ok fonc on me dit que je dois avoir une 'UserFollows' instance et donc c'est maintenant mon request.user qui ne va pas, il me foaut son nom ou son id, je sais pas, mais quelque chose.add()
    #c'est l'ID qu'il me faut, si je mets         Q(followed_by__in="a") ; j'ai la phrase d'erreur : Field 'id' expected a number but got 'a'.

    #la ou je bugue : si je mets         Q(followed_by__in=request.user.id); j'ai le message 'int is not iterable'
    #????????????????????????????
    #l'ID n'est pas de type int ? peut etre un type PrimaryKey ? 

    #je tente de trier avec         Q(followed_by__username="utilisateur3")  Related Field got invalid lookup: username

    # SOLUTION? :         Q(followed_by__in=str(request.user.id))
    # NON : marche pour l'utilisateur 2 mais pas les autres, je comprends pas.
    # wow.. je créée de nouveaux utilisateur u4,u5 et u6 : avant que je ne fasse quoi que ce soit, 'utilisateur1' est abonné à u5 ? wtf.
    # ma théorie: rien de sur mais je pense qu'il ne tient compte que tu premier chiffre de l'ID.

    return render(request, 'reviews_app/follow_users_form.html', context={'form': form, 'subscriptions': subscriptions, 'subscribers': subscribers, 'all_users': all_users})




"""
@login_required
def follow_users(request):
    form = FollowUsersForm(instance=request.user)
    if request.method == 'POST':
        form = FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():

            follow_form = form.save(commit=False)
            # set the connected user to the user before saving the model
            follow_form.user = request.user
            # set the ticket before saving the model
            # Save
            follow_form.save()

            return redirect('home')
    return render(request, 'reviews_app/follow_users_form.html', context={'form': form})

"""
    
