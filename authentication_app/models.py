from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    # We just got Users, without any specific 'Role' (as 'creator' or 'subscriber')
    pass