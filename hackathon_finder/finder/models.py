from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class TechStack(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Hackathon(models.Model):
    LEVEL_CHOICES = [
        ('local', 'Local'),
        ('national', 'National'),
        ('international', 'International'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='other'
    )
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    tech_stack = models.ManyToManyField(TechStack, blank=True)
    interested_hackathons = models.ManyToManyField(Hackathon, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # New fields
    looking_for_team = models.BooleanField(
        default=False,
        verbose_name="Actively looking for team members"
    )
    college = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="College/University"
    )
    branch = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Branch of Study"
    )

    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()