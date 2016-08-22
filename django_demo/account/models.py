from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Role(models.Model):
    user = models.ForeignKey(User)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.role

