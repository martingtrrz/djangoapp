from django.urls import path, include
from .views import CategoryViewSet, ProductViewSet, precio_final
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:pk>/precio-final/', precio_final, name='precio-final'),
]