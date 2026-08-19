import math
class LimiteMotorError(Exception):
    pass
class MotorPasoAPaso:
    def __init__(self, eje, pasos_por_mm=100.0, limite_max_mm=200.0):
        self.nombre_eje = eje
        self.factor_conversion = pasos_por_mm
        
        # 1. ENCAPSULAMIENTO: Al usar '__', la variable se vuelve privada.
        # No se puede acceder a ella directamente desde fuera de la clase.
        self.__posicion_actual_pasos = 0 
        
        # Límite físico de la máquina para evitar colisiones
        self.limite_max_pasos = limite_max_mm * pasos_por_mm

    def dar_pasos(self, cantidad_pasos):
        """
        Única forma permitida de modificar la posición privada.
        Incluye lógica intuitiva de topes de seguridad.
        """

        posicion_futura = self.__posicion_actual_pasos + cantidad_pasos
        
        if posicion_futura > self.limite_max_pasos:
            raise LimiteMotorError(f"El motor {self.nombre_eje} excedería el límite físico máximo.")

        elif posicion_futura < 0:
            raise LimiteMotorError(f"El motor {self.nombre_eje} chocaría con el orígen.")
        else:
            self.__posicion_actual_pasos = posicion_futura
            print(f"Motor {self.nombre_eje}: se movió {cantidad_pasos} pasos. Posición validada.")

    def ir_a_origen(self):
        self.__posicion_actual_pasos = 0
        print(f"El motor {self.nombre_eje} ha vuelto al origen de forma segura.")

    def obtener_posicion_mm(self):
        """
        Método 'Getter': Permite consultar el valor de la variable privada
        desde afuera, pero convirtiéndola a milímetros sin permitir alterarla.
        """
        return round(self.__posicion_actual_pasos / self.factor_conversion, 3)

class MiniPLotterCNC:
    def home(self):
        self.motor_x.ir_a_origen()
        self.motor_y.ir_a_origen()
    def __init__(self):
        self.motor_x = MotorPasoAPaso("X", limite_max_mm=200.0)
        self.motor_y = MotorPasoAPaso("Y", limite_max_mm=200.0)
    def mover_absoluto(self, destino_x_mm, destino_y_mm):
        delta_x = destino_x_mm - self.motor_x.obtener_posicion_mm()
        delta_y = destino_y_mm - self.motor_y.obtener_posicion_mm()

        pasos_x = int(delta_x * self.motor_x.factor_conversion)
        pasos_y = int(delta_y * self.motor_y.factor_conversion) 

        try:
            self.motor_x.dar_pasos(pasos_x)
            self.motor_y.dar_pasos(pasos_y)
            return f"G1 X{destino_x_mm} Y{destino_y_mm} ; OK"
        except LimiteMotorError as e:
            print("Error del sistema: Movimiento abortado por seguridad")
            return f"; ERROR: {e}"
    def perforar_puntos(self, lista_coordenadas):
        for x, y in lista_coordenadas:
            resultado = self.mover_absoluto(x, y)

            print(resultado)

            print("    -> [Eje Z]: Bajando broca... Perforando... Subiendo broca")
    def ejecutar_comando_gcode(self, comando_texto):
        comando_texto = comando_texto.strip()
        print(f"\n[Lector G-Code] Analizando instrucción: '{comando_texto}'")

        partes = comando_texto.split()

        if not partes:
            return

        if partes[0] == "G1":
            x_destino = None
            y_destino = None
            z_destino = None
            e_destino = None

            for parte in partes:
                if parte.startswith("X"):
                    x_destino = float(parte[1:])
                elif parte.startswith("Y"):
                    y_destino = float(parte[1:])
                elif parte.startswith("Z"):
                    z_destino = float(parte[1:])
                elif parte.startswith("E"):
                    e_destino = float(parte[1:])

            if x_destino is not None and y_destino is not None:
                self.mover_absoluto(x_destino, y_destino)

            if z_destino is not None:
                print (f"   -> [Eje Z]: Moviendo a la capa / profundidad {z_destino} mm")

            if e_destino is not None:
                print(f"   -> [Extrusor]: Empujando {e_destino} mm de filamento")
        elif partes[0] == "G28":
            self.home()
        else:
            print("ERROR: Comando no reconocido en la simulación")

# ==========================================
# ÁREA DE PRUEBAS
# ==========================================
mi_plotter = MiniPLotterCNC()

# Simulación de un archivo G-Code de una Impresora 3D
print("\n--- SIMULANDO IMPRESIÓN 3D ---")
mi_plotter.ejecutar_comando_gcode("G28") # Homing
mi_plotter.ejecutar_comando_gcode("G1 Z0.2") # Sube a la primera capa
mi_plotter.ejecutar_comando_gcode("G1 X10 Y10 E1.5") # Dibuja extruyendo plástico
mi_plotter.ejecutar_comando_gcode("G1 X20 Y10 E3.0") # Sigue dibujando

# Simulación de un archivo G-Code de una Fresadora CNC (SolidWorks)
print("\n--- SIMULANDO FRESADORA CNC ---")
mi_plotter.ejecutar_comando_gcode("G28")
mi_plotter.ejecutar_comando_gcode("G1 X50 Y50") # Se posiciona sobre la pieza
mi_plotter.ejecutar_comando_gcode("G1 Z-5.0") # La broca baja 5mm hacia adentro del material
mi_plotter.ejecutar_comando_gcode("G1 X60 Y50") # Realiza un corte lateral