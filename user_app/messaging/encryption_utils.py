# messaging/encryption_utils.py

from django.conf import settings
from cryptography.fernet import Fernet

# Retrieve the Fernet key from Django settings
FERNET_KEY = settings.FERNET_KEY
cipher_suite = Fernet(FERNET_KEY)


def encrypt_message(message_content):
    """Encrypt the message content."""
    return cipher_suite.encrypt(message_content.encode()).decode()

def decrypt_message(encrypted_content):
    """Decrypt the message content."""
    return cipher_suite.decrypt(encrypted_content.encode()).decode()
