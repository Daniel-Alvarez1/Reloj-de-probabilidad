from .metodoObtencion import MetodoObtencion
from modelos.intento import Intento

class RecompensaMision(MetodoObtencion):
    def realizar_intento(self, numero_intento: int, tiene_potenciador: bool = False) -> Intento:
        return self._resolver_intento(numero_intento, self._tiempo_por_intento, tiene_potenciador)