import datetime
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
# from .choices import UserState


class UserState(models.TextChoices):
    ACTIVATED = "A", "Activated"
    DEACTIVATED = "D", "Deactivated"



class CustomUser(AbstractUser):
    state = models.CharField(max_length=1, choices=UserState.choices, default=UserState.ACTIVATED)

    def __str__(self):
        return str(self.id) +" " + self.first_name + " " + self.last_name
