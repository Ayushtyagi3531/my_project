from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    def clean(self):
        if self.date < timezone.now().date():
            raise ValidationError("The event date cannot be in the past.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures clean() is called before saving
        super().save(*args, **kwargs)

class RSVP(models.Model):
    STATUS_CHOICES = (
        ('going', 'Going'),
        ('maybe', 'Maybe'),
        ('declined', 'Declined'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event', 'user')  # Prevent duplicate RSVPs

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.status}"
