from plotter_oop import MotorPasoAPaso, LimiteMotorError

class BaseCobotCNC():
    def __init__(self, nombre):
        self.nombre = nombre
        self.herramienta_actual = None

        self.motor_x = MotorPasoAPaso("X", limite_max_mm=200.0)
        self.motor_y = MotorPasoAPaso("Y", limite_max_mm=200.0)

    def equipar(self, nueva_herramienta):
        self.herramienta_actual = nueva_herramienta
        nombre_herramienta = type(nueva_herramienta).__name__
        print(f"[Hardware] ----> {nombre_herramienta} equipado")

    def home(self):
        print("Iniciar secuencia de HOming de la base")

        self.motor_x.ir_a_origen()
        self.motor_y.ir_a_origen()

        print("Homing completado")
        return "G28; OK"

    def Mover_operar(self, destino_x, destino_y, parametros_herramientas):
        pass