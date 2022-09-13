from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import ValidationError

from itertools import chain

from reviews_app.forms import TicketForm, ReviewForm, FollowUsersForm, FollowUsersForm_input

from authentication_app.models import User
from reviews_app.models import UserFollows

# Feed creation (flux)
from . import models


@login_required
def home(request):
    """Return an objetHttpResponse corresponding to the home page"""

    # Limit displayed reviews to the tickets by followed users
    reviews = models.Review.objects.filter(
        # the user can see the reviews writen by users he/she follows
        Q(user__in=request.user.follows.all())|
        # the user can see the reviews he/she wrote
        Q(user=request.user)|
        # the user can see the reviews in response to tickets he/she wrote (event if the response
        # was writen by a user he/she does not follow)
        Q(ticket__user=request.user)
    )

    for review in reviews:
        review.rating = "".join((review.rating * "★", (5 - review.rating)*"☆"))

    # Limit displayed tickets to the tickets by followed users
    tickets = models.Ticket.objects.filter(
        # the user can see the tickets writen by users he/she follows
        Q(user__in=request.user.follows.all())|
        # the user can see the tickets he/she wrotes
        Q(user=request.user)
    )

    # We keep only ticket not associated to a review : exclusion of tickets already associated to
    # a review with __in (field name + __ + in) : without button in HTML
    tickets_without_review = models.Ticket.objects.filter(
        ~Q(review__in=reviews)  # ~ : NOT
    )

    tickets_and_reviews = sorted(
        # itertools.chain: group of querysets --> python: sorted() 
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    context = {
        'tickets_and_reviews': tickets_and_reviews, 
        'tickets_without_review':tickets_without_review
        }
    return render(request, 'reviews_app/home.html', context=context)


@login_required
def ticket_create(request):
    """Return an objetHttpResponse corresponding to the ticket creation page"""

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            # New instance but without saving in database, in order to attribute the user to 
            # the ForeignKey
            ticket = form.save(commit=False)
            # set the connected user to the user before saving the model
            ticket.user = request.user
            # Save
            ticket.save()
            return redirect('home')
    else:
        form = TicketForm()

    return render(request, 'reviews_app/ticket_create.html', {'form': form})


@login_required
def review_and_ticket_upload(request):
    """Return an objetHttpResponse corresponding to the ticket and review creation page"""

    review_form = ReviewForm()
    ticket_form = TicketForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)

        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.rating = review_form['rating_choice_field'].data
            review.save()

            return redirect('home')

    context = {
        'review_form': review_form,
        'ticket_form': ticket_form,
    }
    return render(request, 'reviews_app/review_and_ticket_create.html', context=context)


@login_required
def review_for_a_given_ticket_create(request, ticket_id):
    """Return an objetHttpResponse corresponding to the review creation page"""

    ticket = models.Ticket.objects.get(id=ticket_id)  

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.rating = form['rating_choice_field'].data
            review.save()

            return redirect('home')

    else:
        form = ReviewForm()

    return render(request,
            'reviews_app/review_create_for_a_ticket.html',
            {'form': form, 'ticket': ticket})


@login_required
def follow_users(request):
    """Return an objetHttpResponse corresponding to the page dedicated to following users"""

    # Added because the client wishes to have an inputField and not a manyToMany field
    input_form = FollowUsersForm_input(initial={'user_to_follow': "Nom d'utilisateur"})

    # Initial form for the manyToMany relationship
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
                print("Abonnement de {0}  à {1} réussi".format(request.user.username,
                username_to_follow))
                
                # Find the user that the connected user will follow
                users_we_want_to_follow = User.objects.filter(username = username_to_follow)
                # Adding the user to follow in the field 'follows" of the connected user
                request.user.follows.add(*users_we_want_to_follow, through_defaults=None)

            # User does not exists
            else:
                raise ValidationError("L'utilisateur {0} n'est pas inscrit sur ce site".format(
                    username_to_follow))

    subscriptions = request.user.follows.all()
    subscribers = User.objects.filter(follows=request.user)

    return render(request, 'reviews_app/follow_users_form.html', context={'input_form':input_form,
                  'form': form,'subscriptions': subscriptions, 'subscribers': subscribers})


@login_required
def my_posts(request):
    """Return an objetHttpResponse corresponding to the page which displays posts of the connected
    user"""

    my_reviews = models.Review.objects.filter(user=request.user)
    my_tickets = models.Ticket.objects.filter(user=request.user)

    for my_review in my_reviews:
        my_review.rating = "".join((my_review.rating * "★", (5 - my_review.rating)*"☆"))

    my_tickets_and_reviews = sorted(
        chain(my_tickets, my_reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    return render(request, 'reviews_app/my_posts.html',
                  {'my_tickets_and_reviews': my_tickets_and_reviews})


@login_required
def ticket_update(request, ticket_id):
    """Return an objetHttpResponse corresponding to the ticket update page"""

    ticket = models.Ticket.objects.get(id=ticket_id)  

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)  # form pre-filling
        if form.is_valid():
            form.save()
            return redirect('my-posts')
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'reviews_app/ticket_update.html', {'form': form, 'ticket': ticket})


@login_required
def review_update(request, review_id):
    """Return an objetHttpResponse corresponding to the review update page"""

    review = models.Review.objects.get(id=review_id)  
    ticket = review.ticket

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)  # form pre-filling
        if form.is_valid():
            review = form.save(commit=False)
            review.rating = form['rating_choice_field'].data
            review.save()
            return redirect('my-posts')
    else:
        form = ReviewForm(instance=review)  # form pre-filling

    return render(request, 'reviews_app/review_update.html',  {'form': form, 'ticket': ticket})


@login_required
def ticket_delete(request, ticket_id):
    """Return an objetHttpResponse corresponding to the ticket deletion page"""

    ticket = models.Ticket.objects.get(id=ticket_id)  

    if request.method == 'POST':
        ticket.delete()
        return redirect('my-posts')

    return render(request, 'reviews_app/ticket_delete.html', {'ticket': ticket})


@login_required
def review_delete(request, review_id):
    """Return an objetHttpResponse corresponding to the review deletion page"""

    review = models.Review.objects.get(id=review_id)  

    if request.method == 'POST':
        review.delete()
        return redirect('my-posts')

    return render(request, 'reviews_app/review_delete.html',  {'review': review})


@login_required
def follow_user_delete(request, followed_user_id):
    """Return an objetHttpResponse corresponding to the following relation deletion page"""

    followed_user = User.objects.get(id=followed_user_id)  
    ConnectedUser_FollowedUser_relation = UserFollows.objects.get(user = request.user,
                                                                  followed_user = followed_user)  

    if request.method == 'POST':
        ConnectedUser_FollowedUser_relation.delete()
        return redirect('follow_users')

    return render(request, 'reviews_app/follow_user_delete.html', {'followed_user': followed_user})
