"""
Database models for Personal Budget Tracker
Converted from Flask-SQLAlchemy to Django ORM
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile with admin flag"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Transaction(models.Model):
    """Transaction model for income and expenses"""
    TYPE_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]
    
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=50)
    amount = models.FloatField()
    note = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.type}: {self.category} - {self.amount}"
    
    @property
    def get_type(self):
        return self.type
