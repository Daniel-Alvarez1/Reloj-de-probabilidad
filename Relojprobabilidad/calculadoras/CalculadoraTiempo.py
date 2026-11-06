import math
from modelos.Objetoobjetivo import EntidadSistema

def formatear_tiempo(segundos: float) -> str:
    segundos = int(max(0, segundos))
    h, resto = divmod(segundos, 3600)
    m, s = divmod(resto, 60)
    if h: return f"{h}h {m}m {s}s"
    if m: return f"{m}m {s}s"
    return f"{s}s"

class CalculadoraTiempo(EntidadSistema):
    def __init__(self, tiempo_por_intento: float, tiempo_limite: float):
        self.tiempo_por_intento = tiempo_por_intento
        self.tiempo_limite = tiempo_limite

    def calcular_tiempo_necesario(self, intentos: float) -> float:
        if intentos == math.inf: return math.inf
        return intentos * self.tiempo_por_intento

    def calcular_intentos_posibles(self) -> int:
        if self.tiempo_por_intento <= 0: return 0
        return int(self.tiempo_limite // self.tiempo_por_intento)

    def describir(self) -> str:
        return f"CalculadoraTiempo(t/intento={formatear_tiempo(self.tiempo_por_intento)})"