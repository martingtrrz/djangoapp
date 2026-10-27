from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from users.models import User
from users.serializers import UserSerializer


class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        # No se muta request.data (puede ser inmutable); se trabaja sobre una copia
        data = request.data.copy()
        if 'password' in data and data['password']:
            data['password'] = make_password(data['password'])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        return self._update_hashing(request, partial=kwargs.pop('partial', False), **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self._update_hashing(request, partial=True, **kwargs)

    def _update_hashing(self, request, partial, **kwargs):
        # FIX seguridad #2: solo se cambia la contraseña si viene en la petición.
        # Si no viene, se quita del payload para conservar la actual del usuario
        # editado (el manual le asignaba la contraseña de quien hacía la petición).
        data = request.data.copy()
        if 'password' in data and data['password']:
            data['password'] = make_password(data['password'])
        else:
            data.pop('password', None)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
