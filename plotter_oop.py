class MotorPasoAPaso: #Esto es el plano que nos va a decir que hacer paso a paso, es el layout

    def __init__(self, eje): #Eetas son las acciones que hará nuestra máquina, se llaman atributos
        self.nombre_eje = eje
        self.posicion_actual = 0 

    def dar_pasos(self, cantidad_pasos):
        self.posicion_actual = self.posicion_actual + cantidad_pasos

        print (f"Motor {self.nombre_eje} se movió {cantidad_pasos}")
        print (f"Nueva posición del motor {self.nombre_eje}: {self.posicion_actual}")

    def ir_a_origen(self):
        self.posicion_actual = 0
        print(f"La posición del motor {self.nombre_eje} es: {self.posicion_actual}")

# ============ #
#    PRUEBAS   #
# ============ #         
motor_x = MotorPasoAPaso("X")
motor_y = MotorPasoAPaso("L")

motor_x.dar_pasos(200)
motor_y.dar_pasos(50)

motor_x.dar_pasos(100)

motor_x.ir_a_origen()
motor_y.ir_a_origen()

