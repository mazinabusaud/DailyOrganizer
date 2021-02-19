from django.db import models
from django.contrib.auth.models import User
import datetime

class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=128)
    date = models.DateField(auto_now=True)
    entry = models.TextField(max_length=500)

    @property
    def track(self):
        return (datetime.date.today() - self.date).days
