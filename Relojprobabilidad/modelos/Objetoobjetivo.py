from abc import ABC, abstractmethod

class ProbabilidadInvalidaError(ValueError):
    """Se lanza cuando la probabilidad no está entre 0 y 1."""
    pass

class EntidadSistema(ABC):
    """Clase padre raíz. Sin factores booleanos."""
    @abstractmethod
    def describir(self) -> str:
        pass

class ObjetoObjetivo(EntidadSistema):
    def __init__(self, nombre: str, probabilidad_obtencion: float, cantidad_deseada: int = 1):
        self._nombre = nombre
        self.probabilidad_obtencion = probabilidad_obtencion
        self.cantidad_deseada = cantidad_deseada

    @property
    def probabilidad_obtencion(self) -> float:
        return self._probabilidad_obtencion

    @probabilidad_obtencion.setter
    def probabilidad_obtencion(self, valor: float):
        valor = float(valor)
        if valor < 0 or valor > 1:
            raise ProbabilidadInvalidaError(f"Probabilidad inválida: {valor}. Debe estar entre 0 y 1.")
        self._probabilidad_obtencion = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def cantidad_deseada(self) -> int:
        return self._cantidad_deseada

    @cantidad_deseada.setter
    def cantidad_deseada(self, valor: int):
        if valor < 1:
            raise ValueError("La cantidad a conseguir debe ser al menos 1.")
        self._cantidad_deseada = int(valor)

    def describir(self) -> str:
        return f"ObjetoObjetivo('{self._nombre}', p_base={self.probabilidad_obtencion:.2%}, cantidad={self.cantidad_deseada})"