import React from "react";
import { Button, Container, Header, Icon, Segment } from "semantic-ui-react";
import { Link } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

export function Home() {
  const { auth } = useAuth();

  return (
    <Container text style={{ marginTop: "80px", textAlign: "center" }}>
      <Segment padded="very" raised style={{ borderRadius: "15px" }}>
        <Header as="h1" icon style={{ color: "#2a2a72" }}>
          <Icon name="book" />
          Biblioteca Universitaria
          <Header.Subheader style={{ marginTop: "10px" }}>
            Sistema de Autenticación JWT y Servicios Web
          </Header.Subheader>
        </Header>

        <div style={{ marginTop: "30px" }}>
          {auth ? (
            <Button as={Link} to="/dashboard" primary size="large">
              <Icon name="dashboard" /> Ir al Dashboard
            </Button>
          ) : (
            <div>
              <Button as={Link} to="/login" primary size="large" style={{ marginRight: "10px" }}>
                <Icon name="sign in" /> Iniciar Sesión
              </Button>
              <Button as={Link} to="/register" secondary size="large">
                <Icon name="signup" /> Registrarse
              </Button>
            </div>
          )}
        </div>
      </Segment>
    </Container>
  );
}
