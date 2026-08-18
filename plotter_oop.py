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

# ==========================================
# ÁREA DE PRUEBAS
# ==========================================
mi_plotter = MiniPLotterCNC()

puntos_a_perforar = [
    (10,10), (25,10), (25,40), (250, 40)
]

mi_plotter.perforar_puntos(puntos_a_perforar)