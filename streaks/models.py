from django.db import models  #django.db: This is Django's database module that contains all database-related functionality and  models This is the specific part of Django that contains the Model class and all field types you'll use to define your database tables

# Create your models here
from django.contrib.auth.models import User #Django's built-in authentication module that provides a User model for handling user accounts

class Streak(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    last_completed = models.DateField(null=True, blank=True)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
    
