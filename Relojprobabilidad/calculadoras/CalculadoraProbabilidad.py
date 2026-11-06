import math
from modelos.Objetoobjetivo import EntidadSistema, ProbabilidadInvalidaError

class CalculadoraProbabilidad(EntidadSistema):
    def __init__(self, probabilidad_base: float):
        self.probabilidad_base = probabilidad_base

    @property
    def probabilidad_base(self) -> float:
        return self._probabilidad_base

    @probabilidad_base.setter
    def probabilidad_base(self, valor: float):
        valor = float(valor)
        if valor < 0 or valor > 1:
            raise ProbabilidadInvalidaError("La probabilidad base debe estar entre 0 y 1.")
        self._probabilidad_base = valor

    def calcular_probabilidad(self, tiene_potenciador: bool = False) -> float:
        """Probabilidad BASE por intento (no acumulativa)."""
        p = self._probabilidad_base
        if tiene_potenciador:
            p = min(1.0, p * 2)
        return p

    def intentos_para_objetivo(self, objetivo: float, tiene_potenciador: bool = False) -> float:
        """Solo para planificación previa (usa fórmula acumulada)."""
        p = self.calcular_probabilidad(tiene_potenciador)
        if objetivo <= 0: return 0
        if objetivo >= 1: return math.inf
        if p <= 0: return math.inf
        if p >= 1: return 1
        return math.ceil(math.log(1 - objetivo) / math.log(1 - p))

    def describir(self) -> str:
        return f"CalculadoraProbabilidad(p_base={self.probabilidad_base:.2%})"