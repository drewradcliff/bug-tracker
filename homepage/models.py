from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class MyUser(AbstractUser):
    display_name = models.CharField(max_length=240)


class Ticket(models.Model):
    title = models.CharField(max_length=240)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    NEW = 'NE'
    IN_PROGRESS = 'IP'
    DONE = 'DO'
    INVALID = 'IN'
    STATUS_CHOICES = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done'),
        (INVALID, 'Invalid'),
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=NEW,
    )
    # assigned_user = models.ForeignKey(
    #     MyUser,
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    # )
    # completed_user = models.ForeignKey(
    #     MyUser,
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    # )
