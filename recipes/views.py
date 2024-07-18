import json
from django.shortcuts import render
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_random_recipes(request):
    api_key = settings.SPOONACULAR_API_KEY
    url = f'https://api.spoonacular.com/recipes/random?apiKey={api_key}&number=6'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)

@csrf_exempt
def get_recipes_by_ingredients(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ingredients = data.get('ingredients')
        print(ingredients)
        #ingredients = request.POST.get('ingredients')
        if not ingredients:
            return JsonResponse({'error': 'No ingredients provided'}, status=400)

        # Proceed with API call using ingredients

        api_key = settings.SPOONACULAR_API_KEY
        url = f'https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={ingredients}&number=6'
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'error': 'Failed to fetch recipes from Spoonacular API'}, status=response.status_code)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def get_recipes_information(request, id):
    api_key = settings.SPOONACULAR_API_KEY
    url = f'https://api.spoonacular.com/recipes/{id}/information?apiKey={api_key}'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Failed to fetch recipes from Spoonacular API'}, status=response.status_code)

