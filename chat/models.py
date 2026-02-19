from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('voice', 'Voice'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    voice_note = models.FileField(upload_to='voice_notes/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        if self.message_type == 'voice':
            return f'{self.user.username}: [Voice Note]'
        return f'{self.user.username}: {self.content[:50]}'
