from django.http import JsonResponse;
from django.views.decorators.csrf import csrf_exempt;
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from django.contrib.auth import login as django_login, authenticate,get_user_model
import json
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import logout
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


User = get_user_model()

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')
        confirm_password = data.get('confirmPassword')

        # Validate password using Django's built-in forms or custom logic
        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)

        try:
            user = User.objects.create_user(email=email, name=name, password=password)
            user.save()
            return JsonResponse({'message': 'User created successfully'}, status=201)
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
        

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        # Authenticate user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            django_login(request, user)
            access_token = AccessToken.for_user(user)
            response = JsonResponse({'message': 'Login successful', 'name': user.name, 'token': str(access_token)})
            access_token = AccessToken.for_user(user)
            response.set_cookie(key='jwt_access_token', value=str(access_token), httponly=True)
            return response
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user_profile = get_object_or_404(User, email=request.user.email)
    serializer = UserProfileSerializer(user_profile)    
    return Response(serializer.data)

@csrf_exempt
def logout_view(request):
    logout(request)
    response = JsonResponse({'message': 'Logout successful'})
    response.delete_cookie('jwt_access_token')
    response.delete_cookie('csrftoken')
    response.delete_cookie('sessionid')
    return response


def handle_token_expiry(request, exception):
    logout(request)
    response = JsonResponse({'message': 'Token expired or invalid. Please log in again.'}, status=401)
    response.delete_cookie('jwt_access_token')
    response.delete_cookie('csrftoken')
    response.delete_cookie('sessionid')
    return response

