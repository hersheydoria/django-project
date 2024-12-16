from django.utils.deprecation import MiddlewareMixin
import logging

class RequestValidationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.headers.get('Authorization'):
            logging.warning('Unauthorized request blocked')
            return Response({'error': 'Unauthorized'}, status=401)
