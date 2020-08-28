from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class MyUser(AbstractUser):
    display_name = models.CharField(max_length=240)
    REQUIRED_FIELDS = ['display_name']


class Ticket(models.Model):
    title = models.CharField(max_length=240)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    user_filed = models.ForeignKey(
        MyUser,
        related_name='filed',
        on_delete=models.CASCADE,
    )
    user_assigned = models.ForeignKey(
        MyUser,
        related_name='assigned',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user_completed = models.ForeignKey(
        MyUser,
        related_name='completed',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
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

    def status_verbose(self):
        return dict(Ticket.STATUS_CHOICES)[self.status]
