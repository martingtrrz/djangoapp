# products/services.py
# ── Capa de Servicios ─────────────────────────────────────────────────────────
# Aquí vive la lógica de negocio, separada de las vistas (views.py).
# Implementa el Patrón de Comportamiento: Strategy


class EstrategiaDescuento:
    """Clase base abstracta para las estrategias de descuento."""
    def calcular(self, precio):
        raise NotImplementedError


class DescuentoElectronica(EstrategiaDescuento):
    """Aplica un 10 % de descuento (paga el 90 %) para productos de Electrónica."""
    def calcular(self, precio):
        return precio * 0.90


class DescuentoRopa(EstrategiaDescuento):
    """Aplica un 20 % de descuento (paga el 80 %) para productos de Ropa."""
    def calcular(self, precio):
        return precio * 0.80


class SinDescuento(EstrategiaDescuento):
    """No aplica ningún descuento (precio completo)."""
    def calcular(self, precio):
        return precio

#DESCUENTO
def obtener_estrategia(categoria_nombre):
    """
    Devuelve la estrategia de descuento correspondiente al nombre de la categoría.
    Si la categoría no tiene estrategia definida, devuelve SinDescuento.
    """
    estrategias = {
        'Electronica': DescuentoElectronica(),
        'Electrónica': DescuentoElectronica(),  
        'Ropa': DescuentoRopa(),
    }
    return estrategias.get(categoria_nombre, SinDescuento())
