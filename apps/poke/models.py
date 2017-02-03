from __future__ import unicode_literals

from django.db import models
from ..login.models import User

# Create your models here.
class Poke(models.Model):
    person_poking = models.ForeignKey(User, related_name = "poker")
    being_poked = models.ForeignKey(User, related_name = "pokee")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
