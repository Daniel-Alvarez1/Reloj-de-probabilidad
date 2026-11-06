import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

# =====================================================================
# 1. CAPA DE LÓGICA Y NEGOCIO (POO, Encapsulamiento y Abstracción)
# =====================================================================

class ObjetoObjetivo:
    """Representa el objeto que el usuario desea conseguir."""
    def __init__(self, nombre, probabilidad_obtencion):
        self.nombre = nombre
        # Encapsulamiento: validamos la probabilidad al asignar
        self.__probabilidad_obtencion = self.validar_probabilidad(probabilidad_obtencion)

    @property
    def probabilidad_obtencion(self):
        return self.__probabilidad_obtencion

    def validar_probabilidad(self, valor):
        if valor <= 0 or valor > 100:
            raise ValueError("La probabilidad debe estar entre 0% y 100%.")
        return valor / 100.0  # Convertimos a formato decimal (0.0 a 1.0)


class SimuladorFarmeo:
    """Abstracción para realizar la simulación basada en tiempo y probabilidad base."""
    @staticmethod
    def simular_intentos(probabilidad_base, tiempo_maximo_horas, tiempo_por_intento_segundos, cantidad_deseada):
        # Convertimos las horas disponibles a segundos totales
        tiempo_restante_segundos = tiempo_maximo_horas * 3600.0
        cantidad_obtenida = 0
        tiempo_utilizado_segundos = 0

        # Simulamos intento por intento mientras quede tiempo y no hayamos conseguido la cantidad deseada
        while tiempo_restante_segundos >= tiempo_por_intento_segundos and cantidad_obtenida < cantidad_deseada:
            tiempo_restante_segundos -= tiempo_por_intento_segundos
            tiempo_utilizado_segundos += tiempo_por_intento_segundos
            
            # Determinamos si el objeto cae según su probabilidad base
            if random.random() < probabilidad_base:
                cantidad_obtenida += 1

        tiempo_utilizado_horas = tiempo_utilizado_segundos / 3600.0
        return cantidad_obtenida, tiempo_utilizado_horas


# =====================================================================
# 2. CAPA DE INTERFAZ GRÁFICA (RelojFarmeo)
# =====================================================================

class AppRelojFarmeo(tk.Tk):
    """Clase principal que controla la ventana gráfica y coordina los objetos del sistema."""
    
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Reloj de Aproximación de la Probabilidad")
        self.geometry("520x650")
        self.lift()                          # Eleva la ventana sobre las demás
        self.attributes("-topmost", True)    # La mantiene al frente de todo
        self.after(1, lambda: self.attributes("-topmost", False)) # Libera el bloqueo al frente

        self.config(bg="#f5f5f5")
        
        # Estilos visuales básicos utilizando ttk
        style = ttk.Style()
        style.configure("TLabel", background="#f5f5f5", font=("Arial", 10))
        style.configure("TFrame", background="#f5f5f5")

        # --- TÍTULO PRINCIPAL ---
        self.lbl_titulo = tk.Label(
            self, text="⏰ Reloj de Aproximación de la Probabilidad", 
            font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#333333"
        )
        self.lbl_titulo.pack(pady=20)

        # --- FRAME DE CONFIGURACIÓN (Ingreso de Datos) ---
        self.frame_inputs = ttk.LabelFrame(self, text=" Configuración del Farmeo ", padding=15)
        self.frame_inputs.pack(fill="x", padx=25, pady=10)

        # Entrada: Nombre del Objeto
        ttk.Label(self.frame_inputs, text="Nombre del Objeto Objetivo:").pack(anchor="w", pady=(0, 2))
        self.txt_nombre = ttk.Entry(self.frame_inputs, font=("Arial", 10))
        self.txt_nombre.insert(0, "Espada Legendaria")
        self.txt_nombre.pack(fill="x", pady=(0, 10))

        # Entrada: Probabilidad Base (%)
        ttk.Label(self.frame_inputs, text="Probabilidad de Obtención por Intento (%):").pack(anchor="w", pady=(0, 2))
        self.txt_prob_base = ttk.Entry(self.frame_inputs, font=("Arial", 10))
        self.txt_prob_base.insert(0, "2.0")
        self.txt_prob_base.pack(fill="x", pady=(0, 10))

        # Entrada: Tiempo por Intento (Segundos)
        ttk.Label(self.frame_inputs, text="Tiempo por cada Intento (en segundos):").pack(anchor="w", pady=(0, 2))
        self.txt_tiempo_intento = ttk.Entry(self.frame_inputs, font=("Arial", 10))
        self.txt_tiempo_intento.insert(0, "45")
        self.txt_tiempo_intento.pack(fill="x", pady=(0, 10))

        # Entrada: Tiempo Máximo Disponible (Horas)
        ttk.Label(self.frame_inputs, text="Tiempo Máximo Disponible para Farmear (en horas):").pack(anchor="w", pady=(0, 2))
        self.txt_tiempo_maximo = ttk.Entry(self.frame_inputs, font=("Arial", 10))
        self.txt_tiempo_maximo.insert(0, "3.5")
        self.txt_tiempo_maximo.pack(fill="x", pady=(0, 10))

        # Entrada: Cantidad Deseada
        ttk.Label(self.frame_inputs, text="Cantidad Deseada de este Objeto:").pack(anchor="w", pady=(0, 2))
        self.txt_cantidad_deseada = ttk.Entry(self.frame_inputs, font=("Arial", 10))
        self.txt_cantidad_deseada.insert(0, "1")
        self.txt_cantidad_deseada.pack(fill="x", pady=(0, 15))

        # --- BOTÓN DE PROCESAMIENTO ---
        self.btn_calcular = tk.Button(
            self, text="Calcular Estimaciones de Farmeo", font=("Arial", 11, "bold"),
            bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white",
            relief="flat", padx=8, pady=8, command=self.ejecutar_analisis
        )
        self.btn_calcular.pack(fill="x", padx=25, pady=15)

        # --- FRAME DE RESULTADOS (Salida de Datos) ---
        self.frame_resultados = ttk.LabelFrame(self, text=" Métricas Estimadas y Resultados ", padding=15)
        self.frame_resultados.pack(fill="both", expand=True, padx=25, pady=10)

        self.lbl_res_objeto = tk.Label(self.frame_resultados, text="", font=("Arial", 11, "bold"), bg="#f5f5f5", fg="#2c3e50")
        self.lbl_res_objeto.pack(anchor="w", pady=5)

        self.lbl_res_tiempo_usado = tk.Label(self.frame_resultados, text="Tiempo total usado: --", font=("Arial", 10), bg="#f5f5f5")
        self.lbl_res_tiempo_usado.pack(anchor="w", pady=3)

        self.lbl_res_obtenidos = tk.Label(self.frame_resultados, text="Cantidad total obtenida: --", font=("Arial", 10), bg="#f5f5f5")
        self.lbl_res_obtenidos.pack(anchor="w", pady=3)

        self.lbl_res_nota = tk.Label(
            self.frame_resultados, 
            text="Nota: Los sistemas aleatorios no garantizan la obtención exacta,\npero optimizan la administración del tiempo.", 
            font=("Arial", 9, "italic"), bg="#f5f5f5", fg="#7f8c8d", justify="left"
        )
        self.lbl_res_nota.pack(anchor="w", pady=(15, 0))

    def ejecutar_analisis(self):
        """Captura los datos del formulario, gestiona las excepciones y actualiza la UI."""
        try:
            # 1. Extracción y validación inicial de datos de la GUI
            nombre = self.txt_nombre.get().strip()
            p_base = float(self.txt_prob_base.get())
            tiempo_seg = float(self.txt_tiempo_intento.get())
            t_max_horas = float(self.txt_tiempo_maximo.get())
            cant_deseada = int(self.txt_cantidad_deseada.get())

            if not nombre:
                nombre = "Objeto Desconocido"

            if t_max_horas < 0:
                messagebox.showerror("Error de Configuración", "El tiempo máximo disponible no puede ser negativo.")
                return

            if tiempo_seg <= 0:
                messagebox.showerror("Error de Configuración", "El tiempo por intento debe ser mayor a 0 segundos.")
                return

            if cant_deseada <= 0:
                messagebox.showerror("Error de Configuración", "La cantidad deseada debe ser al menos 1.")
                return

            # 2. Instanciación y uso del modelo Orientado a Objetos (Abstracción)
            objeto = ObjetoObjetivo(nombre, p_base)
            
            # 3. Simulación basada en la probabilidad base y el tiempo disponible
            obtenidos, tiempo_usado_horas = SimuladorFarmeo.simular_intentos(
                objeto.probabilidad_obtencion, t_max_horas, tiempo_seg, cant_deseada
            )

            # 4. Actualización de los componentes gráficos
            self.lbl_res_objeto.config(text=f"🎯 Objetivo: {objeto.nombre} (Probabilidad base: {p_base}%)")
            self.lbl_res_tiempo_usado.config(text=f"• Tiempo empleado en la sesión: {tiempo_usado_horas:.2f} horas ({tiempo_usado_horas * 60:.1f} minutos)")
            self.lbl_res_obtenidos.config(text=f"• Cantidad total obtenida: {obtenidos} de {cant_deseada} deseados")

        except ValueError as e:
            error_mensaje = str(e) if "La probabilidad" in str(e) else "Por favor, introduce valores numéricos válidos en los campos correspondientes."
            messagebox.showerror("Error de Entrada", error_mensaje)


# =====================================================================
# 3. INICIALIZADOR DE LA APLICACIÓN
# =====================================================================
if __name__ == "__main__":
    app = AppRelojFarmeo()
    app.mainloop()
