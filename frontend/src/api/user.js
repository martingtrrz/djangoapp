const API_URL = import.meta.env.VITE_BASE_API_URL || 'http://localhost:8000';

export async function loginApi(formData) {
  try {
    const url = `${API_URL}/api/v1/auth/token/`;
    const params = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    };

    const response = await fetch(url, params);
    if (response.status !== 200) {
      throw new Error('Usuario o contraseña incorrecta');
    }

    const result = await response.json();
    return result;
  } catch (error) {
    throw error;
  }
}

export async function registerApi(formData) {
  try {
    const url = `${API_URL}/api/v1/auth/register/`;
    const params = {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    };

    const response = await fetch(url, params);
    const result = await response.json();

    if (response.status !== 201) {
      const errMsg =
        result.email?.[0] ||
        result.username?.[0] ||
        result.password?.[0] ||
        result.detail ||
        'No se puede crear el usuario';
      throw new Error(errMsg);
    }

    return result;
  } catch (error) {
    throw error;
  }
}

export async function getMeApi(token) {
  try {
    const url = `${API_URL}/api/v1/auth/me/`;
    const params = {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };

    const response = await fetch(url, params);
    if (response.status !== 200) {
      throw new Error('Error al obtener datos del usuario');
    }
    const result = await response.json();
    return result;
  } catch (error) {
    throw error;
  }
}
