from django.utils.deprecation import MiddlewareMixin
from cryptography.fernet import Fernet
from django.conf import settings
from .models import Message

# Retrieve the Fernet key from settings
FERNET_KEY = settings.FERNET_KEY
cipher_suite = Fernet(FERNET_KEY)

class EncryptionMiddleware(MiddlewareMixin):

    def decrypt_request(self, request):
        """Decrypt message content in the request body."""
        if request.method in ['POST', 'PUT', 'PATCH'] and request.body:
            try:
                # Assuming the content is JSON encoded
                request._body = decrypted_data  # Modify the request body with decrypted data
            except Exception as e:
                print(f"Error decrypting request body: {e}")

    def encrypt_response(self, response):
        """Encrypt message content in the response."""
        if response.content and response['Content-Type'] == 'application/json':
            try:
                encrypted_data = cipher_suite.encrypt(response.content)
                response.content = encrypted_data  # Modify the response content with encrypted data
            except Exception as e:
                print(f"Error encrypting response body: {e}")
