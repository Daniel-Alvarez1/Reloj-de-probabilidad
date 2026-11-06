import random
from .metodoObtencion import MetodoObtencion
from modelos.intento import Intento

class AperturaCofre(MetodoObtencion):
    def realizar_intento(self, numero_intento: int, tiene_potenciador: bool = False) -> Intento:
        tiempo = self._tiempo_por_intento + random.uniform(0, 2)
        return self._resolver_intento(numero_intento, tiempo, tiene_potenciador)