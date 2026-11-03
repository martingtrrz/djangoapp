import React from "react";
import { Container, Header, Icon, Button } from "semantic-ui-react";
import { Link } from "react-router-dom";

export function Error404() {
  return (
    <Container text style={{ marginTop: "100px", textAlign: "center" }}>
      <Header as="h1" icon style={{ color: "#2a2a72" }}>
        <Icon name="compass outline" />
        Error 404
        <Header.Subheader style={{ marginTop: "10px" }}>
          Página no encontrada
        </Header.Subheader>
      </Header>
      <Button as={Link} to="/" primary style={{ marginTop: "20px" }}>
        Volver al inicio
      </Button>
    </Container>
  );
}

export default Error404;
