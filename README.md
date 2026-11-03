# Biblioteca Universitaria — Django REST & ReactJS (RA2)

Proyecto integral para el **Resultado de Aprendizaje (Unidades 2 y 3)**:
- **Backend:** Django 6, Django REST Framework, Autenticación JWT (`djangorestframework-simplejwt`), Documentación Swagger / OpenAPI (`drf-yasg`), Consumo de Web Service SOAP con `zeep`, y control de CORS (`django-cors-headers`).
- **Frontend:** React 18 con Vite, Semantic UI React, React Router v6, Formularios con Formik y Yup, Notificaciones con React Toastify, Manejo de estado de autenticación global con `AuthContext` y Custom Hooks (`useAuth`, `useUser`).
- **Integraciones:**
  - **API de Terceros:** Widget en Dashboard que consume dinámicamente citas/consejos con `fetch()` desde `api.adviceslip.com`.
  - **Web Service SOAP:** Endpoint en Django (`/api/v1/soap/country/`) que consume el servicio público SOAP `CountryInfoService` mediante `zeep`.

---

## 🚀 Requisitos Previos

- **Python:** 3.10 o superior
- **Node.js:** v18 o superior (con npm)
- **MySQL Server:** Servicio en ejecución (base de datos `django_api` en `localhost:3306`, usuario `root`, sin contraseña)

---

## 🛠️ Instalación y Puesta en Marcha

### 1. Backend (Django)

1. Abrir una terminal en la raíz del proyecto:
   ```bash
   # Activar el entorno virtual existente
   .\venv\Scripts\activate   # En Windows PowerShell
   ```

2. Instalar dependencias si es necesario:
   ```bash
   pip install -r requirements.txt
   ```

3. Aplicar las migraciones a la base de datos MySQL:
   ```bash
   python manage.py migrate
   ```

4. Crear un superusuario (si aún no se ha creado):
   ```bash
   python manage.py createsuperuser
   ```

5. Iniciar el servidor de desarrollo del Backend:
   ```bash
   python manage.py runserver
   ```
   *El backend estará disponible en `http://localhost:8000/` y la documentación interactiva en `http://localhost:8000/swagger/`.*

---

### 2. Frontend (React + Vite)

1. En otra terminal, entrar a la carpeta `frontend`:
   ```bash
   cd frontend
   ```

2. Instalar las dependencias de Node:
   ```bash
   npm install
   ```

3. Iniciar el servidor de desarrollo de Vite:
   ```bash
   npm run dev
   ```
   *El frontend estará disponible en `http://localhost:5173/`.*

---

## 📚 Endpoints Principales del Backend

| Método | Endpoint | Descripción | Acceso |
|---|---|---|---|
| `POST` | `/api/v1/auth/token/` | Obtención de tokens JWT (Access & Refresh) | Público |
| `POST` | `/api/v1/auth/register/` | Registro de nuevos usuarios | Público |
| `GET` | `/api/v1/auth/me/` | Datos del usuario autenticado (Web Service Propio) | Bearer Token |
| `POST` | `/api/v1/auth/token/refresh/` | Refresco de token de acceso | Público |
| `GET` | `/api/v1/soap/country/?code=MX` | Web Service SOAP de países consumido con `zeep` | Público |
| `GET` | `/swagger/` | Documentación interactiva Swagger UI | Público |
| `GET` | `/admin/` | Panel de administración de Django | Superusuario |

---

## 🧪 Pruebas Unitarias

Para ejecutar la suite de pruebas unitarias del backend:
```bash
python manage.py test users
```
Verifica:
- Creación de usuarios con contraseña hasheada y oculta en respuestas.
- Actualización parcial segura sin alterar la contraseña.
- Endpoint protegido `/api/v1/auth/me/`.
- Login con email y obtención de JWT.
- Registro público de nuevos usuarios (`/api/v1/auth/register/`).
- Consumo del servicio SOAP de países (`/api/v1/soap/country/`).
