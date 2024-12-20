from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='matriapp_user_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='matriapp_user_permissions',
        blank=True,
    )

    def __str__(self):
        return self.username  # or return self.email if you prefer


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    religion = models.CharField(max_length=50, blank=True)
    caste = models.CharField(max_length=50, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    education = models.CharField(max_length=100, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class PartnerPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    min_age = models.IntegerField(null=True, blank=True)
    max_age = models.IntegerField(null=True, blank=True)
    min_height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max_height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    caste = models.CharField(max_length=50, blank=True)
    education = models.CharField(max_length=100, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Preferences"


class Match(models.Model):
    user = models.ForeignKey(User, related_name='matches', on_delete=models.CASCADE)
    matched_user = models.ForeignKey(User, related_name='matched_with', on_delete=models.CASCADE)
    match_score = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match between {self.user.username} and {self.matched_user.username}"


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    
    # Temporarily allow null values
    event_datetime = models.DateTimeField(null=True)  # Change this line

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the creator of the event
    participants = models.ManyToManyField(User, related_name='events', blank=True)  # Allow multiple participants

    def clean(self):
        # Ensure the event date is in the future
        if self.event_datetime and self.event_datetime < timezone.now():
            raise ValidationError('The event date must be in the future.')

    def __str__(self):
        return self.title


class EventResponse(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

   # True for accept; False for reject
    response = models.BooleanField()

    class Meta:
       unique_together = ('event', 'user')  # Ensure a user can respond only once to an event

    def __str__(self):
       return f"{self.user.username} responded {'accepted' if self.response else 'rejected'} to {self.event.title}"