"""LITR_ReviewsProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

# Import views
import authentication_app.views
import reviews_app.views

# For pictures display
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # -Path for view based on function ; '' because at root theof the project
    # path('', authentication_app.views.login_page, name='login'),
    # -Path for view based on class
    path('', authentication_app.views.LoginPageView.as_view(), name='login'),

    path('logout/', authentication_app.views.logout_user, name='logout'),
    path('signup/', authentication_app.views.signup_page, name='signup'),

    path('home/', reviews_app.views.home, name='home'),
    path('my_posts/', reviews_app.views.my_posts, name='my-posts'),

    path('tickets/add/', reviews_app.views.ticket_create, name='ticket-create'),
    path('reviews_and_tickets/add', reviews_app.views.review_and_ticket_upload, 
        name='review_and_ticket-create'),
    path('reviews/add_for_a_given_ticket/<int:ticket_id>',
        reviews_app.views.review_for_a_given_ticket_create, name='review-create-for-a-ticket'),

    path('tickets/update/<int:ticket_id>/', reviews_app.views.ticket_update, name='ticket-update'),
    path('reviews/update/<int:review_id>/', reviews_app.views.review_update, name='review-update'),

    path('tickets/delete/<int:ticket_id>/', reviews_app.views.ticket_delete, name='ticket-delete'),
    path('reviews/delete/<int:review_id>/', reviews_app.views.review_delete, name='review-delete'),

    path('follow-users/', reviews_app.views.follow_users, name='follow_users'),
    path('follow-users/delete/<int:followed_user_id>/', reviews_app.views.follow_user_delete,
        name='follow_user_delete'),
]


# This method is only adapted to a development environment ; for production : web server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
