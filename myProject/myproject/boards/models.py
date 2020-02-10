from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics')
    starter =  models.ForeignKey(User, related_name='topics')


class Post(models.Model):
    message = models.TextField(max_length=40000)
    topic = models.ForeignKey(Topic, related_name='posts')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)
    created_by = models.ForeignKey(User, related_name='posts')
    updated_by = models.ForeignKey(User, null=True, related_name='+')
