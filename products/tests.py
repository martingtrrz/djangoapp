from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Category, Product


class CategoryTestCase(TestCase):
    """Pruebas para el endpoint de Categorías."""

    def setUp(self):
        # Crear usuario de prueba y autenticar el cliente
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='test1234')
        self.client.force_authenticate(user=self.user)

        # Categoría inicial en la base de datos de prueba
        self.category = Category.objects.create(name='Electrónica')

    def test_create_category(self):
        """Verifica que se puede crear una nueva categoría (POST → 201)."""
        response = self.client.post('/api/v1/categories/', {'name': 'Ropa'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)

    def test_list_categories(self):
        """Verifica que se puede obtener la lista de categorías (GET → 200)."""
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ProductTestCase(TestCase):
    """Pruebas para el endpoint de Productos."""

    def setUp(self):
        # Crear usuario de prueba y autenticar el cliente
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='test1234')
        self.client.force_authenticate(user=self.user)

        # Categoría y producto iniciales en la base de datos de prueba
        self.category = Category.objects.create(name='Electrónica')
        self.product = Product.objects.create(
            name='Laptop',
            category=self.category,
            description='Laptop HP',
            price=15000.00
        )

    def test_create_product(self):
        """Verifica que se puede crear un nuevo producto (POST → 201)."""
        response = self.client.post('/api/v1/products/', {
            'name': 'Mouse',
            'category': self.category.id,
            'description': 'Mouse inalámbrico',
            'price': 500.00,
            'is_active': True,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)

    def test_list_products(self):
        """Verifica que se puede obtener la lista de productos (GET → 200)."""
        response = self.client.get('/api/v1/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_update_product(self):
        """Verifica que se puede actualizar un producto completo (PUT → 200)."""
        response = self.client.put(f'/api/v1/products/{self.product.id}/', {
            'name': 'Laptop Pro',
            'category': self.category.id,
            'description': 'Laptop HP actualizada',
            'price': 18000.00,
            'is_active': True,
        })
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Laptop Pro')
        self.assertEqual(float(self.product.price), 18000.00)

    def test_delete_product(self):
        """Verifica que se puede eliminar un producto (DELETE → 204)."""
        response = self.client.delete(f'/api/v1/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

    def test_precio_final_autenticado(self):
        """Verifica que el endpoint /precio-final/ responde 200 y devuelve 'precio_final'."""
        response = self.client.get(f'/api/v1/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('precio_final', response.data)

    def test_precio_final_sin_autenticar(self):
        """Verifica que sin token el endpoint /precio-final/ devuelve 401."""
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/v1/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 401)
