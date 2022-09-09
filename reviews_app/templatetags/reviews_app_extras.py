from django import template
from django.utils import timezone


# To garantee accessibility of filtres in templates : creation of an instance of Library class
register = template.Library()
 
@register.filter
def model_type(value):
    return type(value).__name__


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context['user']:
        return 'vous'
    return user.username


@register.filter
def get_posted_at_display(posted_at):
    return f'{posted_at.strftime("%H:%M, %d %B %Y")}'
