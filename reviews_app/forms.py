
from django import forms
from reviews_app.models import Ticket, Review

from django.contrib.auth import get_user_model 



class TicketForm(forms.ModelForm):
   class Meta:
     model = Ticket
     # exclusion of user field, as it is the connected user by default (see views.py) 
     # fields = '__all__'
     exclude = ('user',)


class ReviewForm(forms.ModelForm):
   class Meta:
     model = Review
     # exclusion of user field, as it is the connected user by default (see views.py) 
     #fields = '__all__'
     exclude = ('user', 'ticket',)

"""
class DisplayTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
"""


# Cours OC : méthode utilitaire  get_user_model, qui vous permet d’obtenir le modèle  User sans 
# l’importer directement
# Pour créer la relation plusieurs-à-plusieurs dans la vue, vous devez d’abord définir le
# formulaire approprié. Comme les champs sont dans le modèle User, vous pouvez utiliser un
# modelForm.

# https://docs.djangoproject.com/fr/4.1/topics/forms/modelforms/
# the Field 'follows' is a ManyToManyField, then : 
# by default : ModelMultipleChoiceField in the form
# Permet la sélection d’un ou de plusieurs objets de modèles, adapté à la représentation de relations plusieurs-à-plusieurs. 


"""original code : FUNCTIONAL"""
User = get_user_model()
class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['follows']





"""attempt

from reviews_app.models import UserFollows

User = get_user_model()
class FollowUsersForm(forms.ModelForm):  
    class Meta:
        model = UserFollows
        fields = ['user', 'followed_user']
        labels = {'followed_user': 'Utilisateur à suivre : ne marche pas encore avec le username, il faut rentrer son ID, par exemple 5 pour le utilisateur1'}
        exclude = ['user']
        widgets = {'followed_user': forms.TextInput}

#-->"Sélectionnez un choix valide. Ce choix ne fait pas partie de ceux disponibles."
#Si j'enleve la ligne         widgets = {'followed_user': forms.TextInput} --> je peux selectionner, mais je n'ai pas d'enregistrement de la relation many to many


#sinon utiliser form ? et non pas modelform ?
#->du coup il faut définir user et followed_user ?
#->utiliser User.followed_user.add() ??

"""
