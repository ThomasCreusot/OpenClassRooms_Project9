from django.contrib import admin

# Register your models here.
from reviews_app.models import Ticket, Review
admin.site.register(Ticket)
admin.site.register(Review)
