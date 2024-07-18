# middleware.py

from django.http import JsonResponse
from django.contrib.auth import logout
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class TokenExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, (InvalidToken, TokenError)):
            logout(request)
            response = JsonResponse({'error': 'Token expired or invalid. Please log in again.'}, status=401)
            response.delete_cookie('jwt_access_token')
            response.delete_cookie('csrftoken')
            response.delete_cookie('sessionid')
            return response
        return None
