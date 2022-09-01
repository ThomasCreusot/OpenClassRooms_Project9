from django import template

# To garantee accessibility of filtres in templates : creation of an instance of Library class
register = template.Library()
 
@register.filter
def model_type(value):
    return type(value).__name__
