import React from "react";
import { Button, Form } from "semantic-ui-react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";
import { registerApi } from "../../api/user";
import { useNavigate, Link } from "react-router-dom";

export function Register() {
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: initialValues(),
    validationSchema: validationSchema(),
    onSubmit: async (formValues) => {
      try {
        const payload = {
          username: formValues.username,
          email: formValues.email,
          password: formValues.password,
          carrera: formValues.carrera,
        };
        await registerApi(payload);
        toast.success("¡Usuario registrado con éxito! Ahora puedes iniciar sesión.");
        navigate("/login");
      } catch (error) {
        toast.error(error.message);
      }
    },
  });

  return (
    <div className="login-admin">
      <div className="login-admin__content">
        <h1>Registro de Usuario</h1>

        <Form className="login-form-admin" onSubmit={formik.handleSubmit}>
          <label style={{ fontWeight: "bold" }}>Username</label>
          <Form.Input
            name="username"
            placeholder="Nombre de usuario"
            value={formik.values.username}
            onChange={(e) => {
              const value = e.target.value.replace(/\s+/g, "");
              formik.setFieldValue("username", value);
            }}
            onBlur={formik.handleBlur}
            error={formik.errors.username}
          />

          <label style={{ fontWeight: "bold" }}>Correo electrónico</label>
          <Form.Input
            name="email"
            placeholder="Correo electrónico"
            value={formik.values.email}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={formik.errors.email}
          />

          <label style={{ fontWeight: "bold" }}>Carrera</label>
          <Form.Input
            name="carrera"
            placeholder="Ej. Tecnologías de la Información"
            value={formik.values.carrera}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={formik.errors.carrera}
          />

          <label style={{ fontWeight: "bold" }}>Contraseña</label>
          <Form.Input
            name="password"
            type="password"
            placeholder="Mínimo 8 caracteres"
            value={formik.values.password}
            onChange={formik.handleChange}
            error={formik.errors.password}
            autoComplete="new-password"
          />

          <label style={{ fontWeight: "bold" }}>Confirmar Contraseña</label>
          <Form.Input
            name="password_confirm"
            type="password"
            placeholder="Repite la contraseña"
            value={formik.values.password_confirm}
            onChange={formik.handleChange}
            error={formik.errors.password_confirm}
            autoComplete="new-password"
          />

          <Button type="submit" content="Registrarse" primary fluid loading={formik.isSubmitting} />
        </Form>

        <div style={{ marginTop: "20px", textAlign: "center" }}>
          ¿Ya tienes cuenta? <Link to="/login">Inicia sesión aquí</Link>
        </div>
      </div>
    </div>
  );
}

function initialValues() {
  return {
    username: "",
    email: "",
    carrera: "",
    password: "",
    password_confirm: "",
  };
}

function validationSchema() {
  return Yup.object({
    username: Yup.string().required("El username es obligatorio"),
    email: Yup.string()
      .email("Correo electrónico no válido")
      .required("El correo electrónico es obligatorio"),
    carrera: Yup.string(),
    password: Yup.string()
      .min(8, "La contraseña debe tener al menos 8 caracteres")
      .required("La contraseña es obligatoria"),
    password_confirm: Yup.string()
      .oneOf([Yup.ref("password"), null], "Las contraseñas no coinciden")
      .required("Debes confirmar la contraseña"),
  });
}
