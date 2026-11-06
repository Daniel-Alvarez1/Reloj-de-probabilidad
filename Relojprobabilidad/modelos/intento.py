import random
from .Objetoobjetivo import EntidadSistema

class Intento(EntidadSistema):
    def __init__(self, numero_intento: int, tiempo_intento: float, resultado: bool = False):
        self.numero_intento = numero_intento
        self.tiempo_intento = tiempo_intento
        self.resultado = bool(resultado)

    def describir(self) -> str:
        estado = "ÉXITO" if self.resultado else "fallo"
        return f"Intento #{self.numero_intento} -> {estado} ({self.tiempo_intento:.1f}s)"