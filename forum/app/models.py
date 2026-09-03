from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.fields import CharField, DateTimeField, TextField
from django.db.models.fields.related import ForeignKey

class Forum(models.Model):
    name: CharField = models.CharField(max_length=100, unique=True)
    created_at: DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    forum: ForeignKey = models.ForeignKey(
        Forum,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    author: ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    message: TextField = models.TextField()

    created_at: DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author.username}: {self.message[:50]}"