from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Represents a User"""
    # We just got Users, without any specific 'Role' (as 'creator' or 'subscriber')
    # Cours OC : "Pour établir une relation plusieurs-à-plusieurs entre les utilisateurs, vous
    # devez spécifier un  ManyToManyField  sur le modèle  User, qui lie à un autre  User. Appelons
    # ce champ 'follows' (suit)"


    follows = models.ManyToManyField(
        'self',
        symmetrical=False,
        # through : name of the class to refer (manually created intermediate table)
        through='reviews_app.UserFollows',
        # Cours OC : "...pour contourner ceci, donnez au champ un accesseur inversé personnalisé en
        # spécifiant l’argument 'related_name' "
        related_name='follow_users',
    )

