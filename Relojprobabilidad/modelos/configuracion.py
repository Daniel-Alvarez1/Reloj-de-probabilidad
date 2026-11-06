from .Objetoobjetivo import EntidadSistema, ProbabilidadInvalidaError
from calculadoras.CalculadoraTiempo import formatear_tiempo

class Configuracion(EntidadSistema):
    """Almacena los parámetros. Único booleano: tiene_potenciador."""
    def __init__(self, tiempo_limite: float, probabilidad_objetivo: float = 0.95,
                 cantidad_objetivo: int = 1, tiene_potenciador: bool = False):
        self.tiempo_limite = tiempo_limite
        self.probabilidad_objetivo = probabilidad_objetivo
        self.cantidad_objetivo = cantidad_objetivo
        self._tiene_potenciador = bool(tiene_potenciador)

    @property
    def tiene_potenciador(self) -> bool:
        return self._tiene_potenciador

    @property
    def probabilidad_objetivo(self) -> float:
        return self._probabilidad_objetivo

    @probabilidad_objetivo.setter
    def probabilidad_objetivo(self, valor: float):
        valor = float(valor)
        if valor <= 0 or valor > 1:
            raise ProbabilidadInvalidaError("El objetivo de probabilidad debe estar entre 0 y 1.")
        self._probabilidad_objetivo = valor

    def describir(self) -> str:
        return (f"Configuracion(límite={formatear_tiempo(self.tiempo_limite)}, "
                f"objetivo={self.probabilidad_objetivo:.0%}, "
                f"cantidad={self.cantidad_objetivo}, potenciador={self.tiene_potenciador})")