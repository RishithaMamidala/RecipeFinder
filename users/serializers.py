from rest_framework import serializers
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    initials = serializers.CharField(source='get_initials', read_only=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'initials', 'is_staff', 'is_superuser')
