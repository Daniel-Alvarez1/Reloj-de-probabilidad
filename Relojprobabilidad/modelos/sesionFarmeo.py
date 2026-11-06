from .Objetoobjetivo import EntidadSistema
from .intento import Intento
from calculadoras.CalculadoraTiempo import formatear_tiempo

class SesionFarmeo(EntidadSistema):
    def __init__(self, fecha: str, objeto, metodo, configuracion):
        self._fecha = fecha
        self._objeto = objeto
        self._metodo = metodo
        self._configuracion = configuracion
        self._intentos = []
        self._objetos_obtenidos = 0
        self._tiempo_total = 0.0
        self._activa = True

    @property
    def fecha(self): return self._fecha
    @property
    def objeto(self): return self._objeto
    @property
    def metodo(self): return self._metodo
    @property
    def configuracion(self): return self._configuracion
    @property
    def objetos_obtenidos(self): return self._objetos_obtenidos
    @property
    def tiempo_total(self): return self._tiempo_total
    @property
    def cantidad_intentos(self) -> int: return len(self._intentos)

    @property
    def probabilidad_actual(self) -> float:
        # Probabilidad base por intento (no acumulativa)
        return self._metodo.probabilidad_efectiva(self._configuracion.tiene_potenciador)

    def objetivo_cantidad_alcanzado(self) -> bool:
        return self._objetos_obtenidos >= self._configuracion.cantidad_objetivo

    def registrar_intento(self, intento: Intento) -> None:
        self._intentos.append(intento)
        self._tiempo_total += intento.tiempo_intento
        if intento.resultado:
            self._objetos_obtenidos += 1

    def resumen(self) -> str:
        pot = "SÍ" if self._configuracion.tiene_potenciador else "NO"
        return (f"Sesión {self._fecha} | Objeto: {self._objeto.nombre} | "
                f"Intentos: {self.cantidad_intentos} | "
                f"Obtenidos: {self._objetos_obtenidos}/{self._configuracion.cantidad_objetivo} | "
                f"Tiempo: {formatear_tiempo(self._tiempo_total)} | "
                f"Prob. base/intento: {self.probabilidad_actual:.2%} | "
                f"Potenciador 100%: {pot}")

    def describir(self) -> str:
        return self.resumen()