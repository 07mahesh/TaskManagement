from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In progress', 'In progress'),
        ('Completed', 'Completed')
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(default="No description")
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

from django.utils import timezone

from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    joined_date = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"   
    


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}-->{self.receiver}:{self.content[:20]}"   