from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class MyUser(AbstractUser):
    pass


class Ticket(models.Model):
    title = models.CharField(max_length=240)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    filed_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
