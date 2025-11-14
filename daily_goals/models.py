from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Create your models here.
class UsersGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title