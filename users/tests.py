from django.test import TestCase
from rest_framework.test import APIClient

from users.models import User


class UserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@ut.com', password='Admin1234!')
        self.client.force_authenticate(user=self.admin)

    def test_create_user_hashes_password_and_hides_it(self):
        r = self.client.post('/api/v1/users/', {
            'username': 'ana', 'email': 'ana@ut.com',
            'password': 'Secreta123!', 'carrera': 'TI'})
        self.assertEqual(r.status_code, 201)
        self.assertNotIn('password', r.data)
        self.assertEqual(r.data['carrera'], 'TI')
        user = User.objects.get(email='ana@ut.com')
        self.assertNotEqual(user.password, 'Secreta123!')
        self.assertTrue(user.check_password('Secreta123!'))

    def test_partial_update_without_password_keeps_user_password(self):
        user = User.objects.create_user(
            username='luis', email='luis@ut.com', password='Luis1234!')
        old_hash = user.password
        r = self.client.patch(f'/api/v1/users/{user.id}/', {'carrera': 'Software'})
        self.assertEqual(r.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.password, old_hash)            # no cambia
        self.assertNotEqual(user.password, self.admin.password)  # no es la del admin
        self.assertEqual(user.carrera, 'Software')

    def test_partial_update_with_password_changes_it(self):
        user = User.objects.create_user(
            username='eva', email='eva@ut.com', password='Eva1234!')
        self.client.patch(f'/api/v1/users/{user.id}/', {'password': 'Nueva1234!'})
        user.refresh_from_db()
        self.assertTrue(user.check_password('Nueva1234!'))

    def test_me_endpoint_hides_password(self):
        r = self.client.get('/api/v1/auth/me/')
        self.assertEqual(r.status_code, 200)
        self.assertNotIn('password', r.data)
        self.assertEqual(r.data['email'], 'admin@ut.com')

    def test_login_with_email_returns_tokens(self):
        r = APIClient().post('/api/v1/auth/login/', {
            'email': 'admin@ut.com', 'password': 'Admin1234!'})
        self.assertEqual(r.status_code, 200)
        self.assertIn('access', r.data)
