from django.db import models

from django.contrib.auth.models import User


class AppUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='appUser'
    )  # user_id
    nickname = models.CharField(max_length=20, null=False)
    phone = models.CharField(max_length=20, null=False)
    birthdate = models.DateField(null=False)
    date_created = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_user'
