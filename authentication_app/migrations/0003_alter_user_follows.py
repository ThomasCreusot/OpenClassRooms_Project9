# Generated by Django 4.1 on 2022-09-02 14:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0002_user_follows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='follows',
            field=models.ManyToManyField(related_name='follow_users', through='reviews_app.UserFollows', to=settings.AUTH_USER_MODEL),
        ),
    ]
