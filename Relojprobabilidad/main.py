import sys
from datetime import datetime

from modelos.Objetoobjetivo import ObjetoObjetivo, ProbabilidadInvalidaError
from modelos.configuracion import Configuracion
from modelos.sesionFarmeo import SesionFarmeo
from calculadoras.CalculadoraProbabilidad import CalculadoraProbabilidad
from calculadoras.CalculadoraTiempo import CalculadoraTiempo, formatear_tiempo
from metodos.derrotaEnemigo import DerrotaEnemigo

class Usuario:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.sesiones = []

    def crear_sesion(self, objeto, metodo, config):
        sesion = SesionFarmeo(datetime.now().strftime("%Y-%m-%d %H:%M"), objeto, metodo, config)
        self.sesiones.append(sesion)
        return sesion

class RelojFarmeo:
    def __init__(self, sesion: SesionFarmeo):
        self.sesion = sesion
        self.tiempo_transcurrido = 0.0
        self.corriendo = False

    def simular_farmeo(self, imprimir_cada: int = 10):
        self.corriendo = True
        self.tiempo_transcurrido = 0.0
        pot = self.sesion.configuracion.tiene_potenciador
        limite = self.sesion.configuracion.tiempo_limite
        meta = self.sesion.configuracion.cantidad_objetivo

        print("\n⏱  Reloj iniciado.")
        
        while self.corriendo:
            if self.tiempo_transcurrido >= limite:
                print("\n⌛ Se agotó el tiempo límite de farmeo.")
                break

            intento = self.sesion.metodo.realizar_intento(self.sesion.cantidad_intentos + 1, pot)
            self.sesion.registrar_intento(intento)
            self.tiempo_transcurrido += intento.tiempo_intento

            if intento.resultado:
                print(f"\n🎉 ¡'{self.sesion.objeto.nombre}' obtenido! "
                      f"({self.sesion.objetos_obtenidos}/{meta}) "
                      f"en el intento #{intento.numero_intento}")
                
                if self.sesion.objetivo_cantidad_alcanzado():
                    print(f"✅ ¡Meta de {meta} objeto(s) alcanzada!")
                    break

            if intento.numero_intento % imprimir_cada == 0:
                pct = min(1.0, self.tiempo_transcurrido / limite)
                print(f"  Progreso: {pct:.0%} | Tiempo: {formatear_tiempo(self.tiempo_transcurrido)} | "
                      f"Obtenidos: {self.sesion.objetos_obtenidos}/{meta} | p_base: {self.sesion.probabilidad_actual:.2%}")

        self.corriendo = False
        print("\n⏸  Reloj detenido.")
        print("\n--- RESUMEN DE LA SESIÓN ---")
        print(self.sesion.resumen())


# ==========================================
# FLUJO PRINCIPAL Y PREGUNTAS
# ==========================================
def pedir_datos():
    print("=" * 70)
    print(" RELOJ DE APROXIMACIÓN DE LA PROBABILIDAD")
    print("=" * 70)
    print("Introduce los datos del farmeo:\n")

    nombre = input("1) Nombre del objeto a conseguir: ").strip() or "Objeto Misterioso"

    while True:
        try:
            p = float(input("2) Probabilidad base por intento (ej. 0.02 = 2%): ").strip() or "0.02")
            if not 0 <= p <= 1: raise ProbabilidadInvalidaError("Debe estar entre 0 y 1.")
            break
        except (ValueError, ProbabilidadInvalidaError) as e:
            print(f"   ❌ Error: {e}. Intenta de nuevo.")

    while True:
        try:
            t_intento = float(input("3) Tiempo por intento en segundos (ej. 90): ").strip() or "90")
            if t_intento <= 0: raise ValueError("El tiempo debe ser > 0.")
            break
        except ValueError as e:
            print(f"   ❌ Error: {e}. Intenta de nuevo.")

    while True:
        try:
            cantidad = int(input("4) Cantidad a conseguir (ej. 1): ").strip() or "1")
            if cantidad < 1: raise ValueError("La cantidad debe ser al menos 1.")
            break
        except ValueError as e:
            print(f"   ❌ Error: {e}. Intenta de nuevo.")

    resp = input("5) ¿Hay potenciador de recursos del 100% activo? (s/n): ").strip().lower()
    tiene_potenciador = resp == "s"

    try:
        t_limite = float(input("6) Tiempo límite disponible en minutos (ej. 120): ").strip() or "120") * 60
    except ValueError:
        t_limite = 7200

    try:
        p_obj = float(input("7) Probabilidad objetivo acumulada (ej. 0.95): ").strip() or "0.95")
        if not 0 < p_obj <= 1: p_obj = 0.95
    except ValueError:
        p_obj = 0.95

    return nombre, p, t_intento, cantidad, tiene_potenciador, t_limite, p_obj


def main():
    try:
        nombre, p, t_intento, cantidad, tiene_potenciador, t_limite, p_obj = pedir_datos()

        # --- Crear Objetos ---
        objeto = ObjetoObjetivo(nombre, p, cantidad_deseada=cantidad)
        config = Configuracion(t_limite, p_obj, cantidad, tiene_potenciador)
        usuario = Usuario("Jugador1")
        metodo = DerrotaEnemigo("Farmeo principal", p, t_intento)
        
        calc_prob = CalculadoraProbabilidad(p)
        calc_tiempo = CalculadoraTiempo(t_intento, t_limite)

        # --- Mostrar Resumen y Planificación ---
        print("\n" + "=" * 70)
        print(" DATOS INGRESADOS")
        print("=" * 70)
        print(f"  Objeto:               {nombre}")
        print(f"  Probabilidad base:    {p:.2%} por intento")
        print(f"  Tiempo por intento:   {formatear_tiempo(t_intento)}")
        print(f"  Cantidad a conseguir: {cantidad}")
        print(f"  Potenciador 100%:     {'SÍ (x2)' if tiene_potenciador else 'NO'}")
        print(f"  Tiempo límite:        {formatear_tiempo(t_limite)}")

        p_ef = calc_prob.calcular_probabilidad(tiene_potenciador)
        print(f"\n  Probabilidad efectiva por intento: {p_ef:.2%}")

        print("\n📐 PLANIFICACIÓN (solo referencia, cálculo acumulado)")
        print("-" * 70)
        for objetivo in (0.90, 0.95, 0.99):
            n = calc_prob.intentos_para_objetivo(objetivo, tiene_potenciador)
            t = calc_tiempo.calcular_tiempo_necesario(n)
            t_total = t * cantidad
            print(f"  Para {objetivo:.0%} x1 objeto  -> {n} intentos (~{formatear_tiempo(t)})")
            if cantidad > 1:
                print(f"  Para {objetivo:.0%} x{cantidad} objetos -> {n * cantidad} intentos (~{formatear_tiempo(t_total)})")

        # --- Simulación ---
        sesion = usuario.crear_sesion(objeto, metodo, config)
        reloj = RelojFarmeo(sesion)
        
        print("\n🔁 SIMULACIÓN DE FARMEO")
        print("-" * 70)
        reloj.simular_farmeo(imprimir_cada=10)

    except ProbabilidadInvalidaError as e:
        print(f"\n❌ Error crítico de probabilidad: {e}")
    except KeyboardInterrupt:
        print("\n\n👋 Programa cancelado por el usuario.")
        sys.exit(0)

if __name__ == "__main__":
    main()