from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
import zeep

from users.models import User
from users.serializers import UserSerializer, RegisterUserSerializer


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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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


class RegisterUserView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Usuario registrado exitosamente',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'carrera': user.carrera,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ── Web Service SOAP (Unidad 3) ──────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([AllowAny])
def soap_country_info(request):
    """
    Consume el servicio Web SOAP público CountryInfoService usando zeep.
    Ejemplo de uso: /api/v1/soap/country/?code=MX
    """
    country_code = request.query_params.get('code', 'MX').upper()
    wsdl_url = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
    try:
        client = zeep.Client(wsdl=wsdl_url)
        country_name = client.service.CountryName(sCountryISOCode=country_code)
        capital = client.service.CapitalCity(sCountryISOCode=country_code)
        currency = client.service.CountryCurrency(sCountryISOCode=country_code)
        phone_code = client.service.CountryIntPhoneCode(sCountryISOCode=country_code)

        return Response({
            'soap_service': 'CountryInfoService (SOAP)',
            'wsdl': wsdl_url,
            'country_code': country_code,
            'country_name': country_name,
            'capital_city': capital,
            'currency_iso': currency.sISOCode if hasattr(currency, 'sISOCode') else str(currency),
            'currency_name': currency.sName if hasattr(currency, 'sName') else '',
            'phone_code': phone_code,
            'status': 'success'
        })
    except Exception as e:
        return Response({
            'soap_service': 'CountryInfoService (SOAP)',
            'status': 'error',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
