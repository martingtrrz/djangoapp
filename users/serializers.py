from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'carrera', 'password', 'is_active', 'is_staff']
        # FIX seguridad #1: la contraseña (hash) nunca se devuelve en respuestas
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }
