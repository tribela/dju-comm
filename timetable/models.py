from dju_comm.classrating.models import Class

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    course = models.ManyToManyField(Class)
