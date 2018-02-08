
from django.contrib.auth.models import User
from django.db import models


class UserToken(models.Model):
    owner = models.ForeignKey(User, related_name='keys')
    token = models.CharField(max_length=255)
