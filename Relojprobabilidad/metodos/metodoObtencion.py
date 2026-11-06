from abc import ABC, abstractmethod
import random
from modelos.Objetoobjetivo import EntidadSistema
from modelos.intento import Intento

class MetodoObtencion(EntidadSistema, ABC):
    def __init__(self, nombre: str, probabilidad_base: float, tiempo_por_intento: float):
        self._nombre = nombre
        self._probabilidad_base = probabilidad_base
        self._tiempo_por_intento = tiempo_por_intento

    @property
    def nombre(self) -> str: return self._nombre
    @property
    def probabilidad_base(self) -> float: return self._probabilidad_base
    @property
    def tiempo_por_intento(self) -> float: return self._tiempo_por_intento

    def probabilidad_efectiva(self, tiene_potenciador: bool = False) -> float:
        p = self._probabilidad_base
        if tiene_potenciador:
            p = min(1.0, p * 2)
        return p

    @abstractmethod
    def realizar_intento(self, numero_intento: int, tiene_potenciador: bool = False) -> Intento:
        pass

    def _resolver_intento(self, numero_intento: int, tiempo: float, tiene_potenciador: bool) -> Intento:
        exito = random.random() < self.probabilidad_efectiva(tiene_potenciador)
        return Intento(numero_intento, tiempo, exito)

    def describir(self) -> str:
        return f"{self.__class__.__name__}('{self._nombre}', p_base={self._probabilidad_base:.2%})"