from django.urls import path
from . import views

urlpatterns = [
    path('random_recipes/', views.get_random_recipes, name='random_recipes'),
    path('recipes_by_ingredients/', views.get_recipes_by_ingredients, name='recipes_by_ingredients'),
    path('recipes_information/<int:id>/', views.get_recipes_information, name='recipes_information'),
    # Add other API endpoints as needed
]
