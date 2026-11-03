from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'carrera', 'password', 'is_active', 'is_staff']
        # FIX seguridad #1: la contraseña (hash) nunca se devuelve en respuestas
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'carrera']
        extra_kwargs = {
            'password': {'write_only': True},
            'carrera': {'required': False},
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
