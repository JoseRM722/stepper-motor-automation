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
            print(f"¡ALERTA! Movimiento bloqueado. El motor {self.nombre_eje} excedería el límite físico.")

        elif posicion_futura < self.limite_max_pasos:
            print(f"¡ALERTA! Movimiento bloqueado. El motor {self.nombre_eje} echocaría el límite físico.")
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
class LimiteMotorError(Exception):
    "Excepción lanzada cuando el motor intenta exceder sus límites físicos"
    pass

# ==========================================
# ÁREA DE PRUEBAS
# ==========================================

motor_y = MotorPasoAPaso("Y", pasos_por_mm=100.0, limite_max_mm=50)

try:
    print("\n--- Iniciando movimientos ---")
    motor_y.dar_pasos(3000)
    motor_y.dar_pasos(-1000)

    print("Intentando paso peligroso")
    motor_y.dar_pasos(-5000)

    print("Este mensaje no se mostrará")
except LimiteMotorError as error_detectado:
    print(f"Paro de emergencia activado, motivo: {error_detectado}")

print(f"Posición real protegida: {motor_y.obtener_posicion_mm()} mm")
