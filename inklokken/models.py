import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse


class Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    description = models.CharField(max_length=255)
    event_type = models.CharField(max_length=200)
    event_from = models.DateTimeField()
    event_to = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


class CompanyNews(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
