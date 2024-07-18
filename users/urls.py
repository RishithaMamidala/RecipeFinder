from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('userprofile/', views.user_profile, name='user_profile'),
    path('logout/', views.logout_view, name='logout'),
    # Add other API endpoints as needed
]
