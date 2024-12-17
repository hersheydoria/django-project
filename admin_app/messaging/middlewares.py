from django.utils.deprecation import MiddlewareMixin
from cryptography.fernet import Fernet
from django.conf import settings
from .models import Message

# Retrieve the Fernet key from settings
FERNET_KEY = settings.FERNET_KEY
cipher_suite = Fernet(FERNET_KEY)

class EncryptionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.async_mode = False  # Django 5.x compatibility

    def __call__(self, request):
        # Handle request decryption before it reaches the view
        self.decrypt_request(request)
        
        # Process the request and get the response
        response = self.get_response(request)
        
        # Handle response encryption before it is returned
        self.encrypt_response(response)

        return response

    
