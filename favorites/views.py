from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Favorite
from .serializers import FavoriteSerializer
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from rest_framework import status
logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    print(request.user)
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required to access favorites list'}, status=401)

    user = request.user
    favorites = Favorite.objects.filter(user=user)
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data)

# @csrf_exempt
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_to_favorites(request):
#     try:
#         data = json.loads(request.body)
#         recipe_id = data.get('recipe_id')

#         if not recipe_id:
#             return Response({'error': 'Recipe ID is required'}, status=status.HTTP_400_BAD_REQUEST)

#         user = request.user
#         favorite, created = Favorite.objects.get_or_create(user=user, recipe_id=recipe_id)
#         serializer = FavoriteSerializer(favorite)
#         if created:
#             logger.info(f"Added favorite for user {user.email} and recipe {recipe_id}")
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             logger.info(f"Recipe {recipe_id} is already in favorites for user {user.email}")
#             return Response(serializer.data, status=status.HTTP_200_OK)
#     except json.JSONDecodeError:
#         return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         logger.error(f"Error adding favorite: {e}")
#         return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# views.py


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favorites(request):
    try:
        data = request.data
        recipe_id = data.get('recipe_id')

        if not recipe_id:
            return JsonResponse({'error': 'Recipe ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        # Check if the recipe is already in favorites for this user
        if Favorite.objects.filter(user=user, recipe_id=recipe_id).exists():
            logger.info(f"Recipe {recipe_id} is already in favorites for user {user.email}")
            return JsonResponse({'status': 'already_added', 'message': 'Recipe is already in favorites'}, status=status.HTTP_200_OK)

        # Add the recipe to favorites
        favorite = Favorite.objects.create(user=user, recipe_id=recipe_id)
        logger.info(f"Added favorite for user {user.email} and recipe {recipe_id}")
        return JsonResponse({'status': 'added', 'recipe_id': recipe_id}, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Error adding favorite: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_favorites(request):
    try:
        data = json.loads(request.body)
        recipe_id = data.get('recipe_id')

        print('backe', recipe_id)

        if not recipe_id:
            return Response({'error': 'Recipe ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        try:
            favorite = Favorite.objects.get(user=user, recipe_id=recipe_id)
            favorite.delete()
            logger.info(f"Removed favorite for user {user.email} and recipe {recipe_id}")
            return Response({'recipe_id': recipe_id, 'status': 'Recipe removed from favorites'})
        except Favorite.DoesNotExist:
            logger.warning(f"Recipe {recipe_id} not found in favorites for user {user.email}")
            return Response({'error': 'Recipe not found in favorites'}, status=status.HTTP_404_NOT_FOUND)
    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error removing favorite: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([])
def unauthorized_access(request):
    if request.method == 'GET':
        return Response({'error': 'Authentication required to access favorites list'}, status=401)
    elif request.method == 'POST':
        return Response({'error': 'Authentication required to perform this action'}, status=401)
