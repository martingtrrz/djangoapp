from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .services import obtener_estrategia


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# ── Patrón Estructural: Facade ────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def precio_final(request, pk):
    """
    Devuelve el precio con descuento aplicado según la categoría del producto.
    Facade: el cliente solo llama a este endpoint; no sabe nada de Strategy.
    """
    producto = get_object_or_404(Product, pk=pk)
    estrategia = obtener_estrategia(producto.category.name if producto.category else '')
    precio_con_descuento = estrategia.calcular(float(producto.price))
    return Response({
        'producto': producto.name,
        'categoria': producto.category.name if producto.category else 'Sin categoría',
        'precio_original': producto.price,
        'precio_final': round(precio_con_descuento, 2),
    })

