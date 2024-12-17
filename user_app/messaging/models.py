from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from cryptography.fernet import Fernet

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    objects = UserManager() 

# Retrieve the Fernet key from settings
FERNET_KEY = settings.FERNET_KEY
cipher_suite = Fernet(FERNET_KEY)

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when the message is created

    def save(self, *args, **kwargs):
        # Encrypt the message content before saving to the database
        self.content = cipher_suite.encrypt(self.content.encode()).decode('utf-8')
        super().save(*args, **kwargs)

    def get_decrypted_content(self):
        # Decrypt the message content when retrieving from the database
        try:
            return cipher_suite.decrypt(self.content.encode()).decode('utf-8')
        except Exception:
            return "[Decryption Failed]"

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
