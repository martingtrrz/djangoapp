import React, { useState, useEffect } from "react";
import { Button, Card, Icon, Loader, Message, Label } from "semantic-ui-react";
import { useAuth } from "../../hooks/useAuth";

export function Dashboard() {
  const { logout, auth } = useAuth();
  const user = auth?.me;

  // Estado para la API de Terceros (Frase inspiradora externa)
  const [quote, setQuote] = useState(null);
  const [loadingQuote, setLoadingQuote] = useState(false);
  const [quoteError, setQuoteError] = useState(null);

  // Estado para probar el Web Service SOAP de Django
  const [soapData, setSoapData] = useState(null);
  const [loadingSoap, setLoadingSoap] = useState(false);

  // Consumir API de terceros con fetch
  const fetchThirdPartyQuote = async () => {
    setLoadingQuote(true);
    setQuoteError(null);
    try {
      // Usamos una API gratuita de citas/consejos con CORS habilitado
      const res = await fetch("https://api.adviceslip.com/advice");
      if (!res.ok) throw new Error("Error al obtener datos externos");
      const data = await res.json();
      setQuote({
        text: data.slip.advice,
        id: data.slip.id,
      });
    } catch (err) {
      setQuoteError("No se pudo cargar la API de terceros.");
    } finally {
      setLoadingQuote(false);
    }
  };

  // Consumir el endpoint SOAP del backend Django
  const fetchSoapData = async () => {
    setLoadingSoap(true);
    try {
      const baseUrl = import.meta.env.VITE_BASE_API_URL || "http://localhost:8000";
      const res = await fetch(`${baseUrl}/api/v1/soap/country/?code=MX`);
      const data = await res.json();
      setSoapData(data);
    } catch (err) {
      console.error("Error al consumir servicio SOAP:", err);
    } finally {
      setLoadingSoap(false);
    }
  };

  useEffect(() => {
    fetchThirdPartyQuote();
  }, []);

  return (
    <div style={{ padding: "40px 20px", maxWidth: "900px", margin: "0 auto" }}>
      {/* Header del Dashboard */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "30px" }}>
        <div>
          <h1 style={{ margin: 0, color: "#2a2a72" }}>Panel de Control (Dashboard)</h1>
          <p style={{ color: "#666", marginTop: "5px" }}>Biblioteca Universitaria</p>
        </div>
        <Button color="red" icon labelPosition="left" onClick={logout}>
          <Icon name="sign out" />
          Cerrar Sesión
        </Button>
      </div>

      {/* Tarjeta de Datos del Usuario (AuthContext + /auth/me/) */}
      <Card fluid style={{ marginBottom: "25px", borderTop: "4px solid #0098d3" }}>
        <Card.Content>
          <Card.Header style={{ fontSize: "20px", color: "#2a2a72" }}>
            <Icon name="user circle" /> Bienvenido, {user?.username || user?.email}
          </Card.Header>
          <Card.Meta style={{ marginTop: "5px" }}>Sesión iniciada con JWT y AuthContext</Card.Meta>
          <Card.Description style={{ marginTop: "15px" }}>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "10px" }}>
              <p><strong>Email:</strong> {user?.email}</p>
              <p><strong>Carrera:</strong> {user?.carrera || "No especificada"}</p>
              <p><strong>Nombre completo:</strong> {(user?.first_name || user?.last_name) ? `${user.first_name} ${user.last_name}` : "Usuario registrado"}</p>
              <p>
                <strong>Rol:</strong>{" "}
                <Label color={user?.is_staff ? "green" : "blue"} size="small">
                  {user?.is_staff ? "Administrador" : "Estudiante"}
                </Label>
              </p>
            </div>
          </Card.Description>
        </Card.Content>
      </Card>

      {/* Widget API de Terceros (Unidad 3) */}
      <Card fluid style={{ marginBottom: "25px", borderTop: "4px solid #f2711c" }}>
        <Card.Content>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <Card.Header style={{ fontSize: "18px", color: "#d35400" }}>
              <Icon name="globe" /> API de Terceros (Consejo / Frase del Día)
            </Card.Header>
            <Button size="tiny" basic color="orange" onClick={fetchThirdPartyQuote} loading={loadingQuote}>
              <Icon name="refresh" /> Actualizar Frase
            </Button>
          </div>
          <Card.Meta style={{ marginTop: "4px" }}>
            Consumida directamente con <code>fetch()</code> desde <code>api.adviceslip.com</code>
          </Card.Meta>
          <Card.Description style={{ marginTop: "15px" }}>
            {loadingQuote ? (
              <Loader active inline="centered" content="Cargando datos externos..." />
            ) : quoteError ? (
              <Message negative content={quoteError} />
            ) : quote ? (
              <Message info style={{ fontSize: "16px", fontStyle: "italic" }}>
                <p>"{quote.text}"</p>
                <small style={{ color: "#666" }}>Consejo #{quote.id}</small>
              </Message>
            ) : null}
          </Card.Description>
        </Card.Content>
      </Card>

      {/* Sección Web Service SOAP (Unidad 3) */}
      <Card fluid style={{ borderTop: "4px solid #21ba45" }}>
        <Card.Content>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <Card.Header style={{ fontSize: "18px", color: "#21ba45" }}>
              <Icon name="server" /> Web Service SOAP (Consumido en Django con Zeep)
            </Card.Header>
            <Button size="tiny" basic color="green" onClick={fetchSoapData} loading={loadingSoap}>
              <Icon name="cloud download" /> Consultar SOAP
            </Button>
          </div>
          <Card.Meta style={{ marginTop: "4px" }}>
            Endpoint Backend: <code>/api/v1/soap/country/?code=MX</code>
          </Card.Meta>
          <Card.Description style={{ marginTop: "15px" }}>
            {soapData ? (
              <div style={{ background: "#f8f9fa", padding: "15px", borderRadius: "8px" }}>
                <p><strong>Servicio:</strong> {soapData.soap_service}</p>
                <p><strong>País:</strong> {soapData.country_name} ({soapData.country_code})</p>
                <p><strong>Capital:</strong> {soapData.capital_city}</p>
                <p><strong>Moneda:</strong> {soapData.currency_name} ({soapData.currency_iso})</p>
                <p><strong>Código telefónico:</strong> +{soapData.phone_code}</p>
              </div>
            ) : (
              <p style={{ color: "#888" }}>Haz clic en "Consultar SOAP" para probar el servicio SOAP de países.</p>
            )}
          </Card.Description>
        </Card.Content>
      </Card>
    </div>
  );
}
