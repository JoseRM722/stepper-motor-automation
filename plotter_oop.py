import math

class MotorLimitError(Exception):
    pass

class StepperMotor:
    def __init__(self, axis, steps_per_mm=100.0, max_limit_mm=200.0):
        self.axis_name = axis
        self.conversion_factor = steps_per_mm

        # 1. ENCAPSULATION: Using '__' makes the variable private.
        # It cannot be accessed directly from outside the class.
        self.__current_position_steps = 0

        # Physical machine limit to prevent collisions
        self.max_limit_steps = max_limit_mm * steps_per_mm

    def take_steps(self, step_count):
        """
        The only allowed way to modify the private position.
        Includes built-in safety limit checks.
        """

        future_position = self.__current_position_steps + step_count

        if future_position > self.max_limit_steps:
            raise MotorLimitError(f"Motor {self.axis_name} would exceed the maximum physical limit.")

        elif future_position < 0:
            raise MotorLimitError(f"Motor {self.axis_name} would crash into the origin.")
        else:
            self.__current_position_steps = future_position
            print(f"Motor {self.axis_name}: moved {step_count} steps. Position validated.")

    def go_to_origin(self):
        self.__current_position_steps = 0
        print(f"Motor {self.axis_name} has safely returned to origin.")

    def get_position_mm(self):
        """
        'Getter' method: Allows querying the value of the private variable
        from outside, converting it to millimeters without allowing it to be altered.
        """
        return round(self.__current_position_steps / self.conversion_factor, 3)

class MiniPlotterCNC:
    def home(self):
        self.motor_x.go_to_origin()
        self.motor_y.go_to_origin()

    def __init__(self):
        self.motor_x = StepperMotor("X", max_limit_mm=200.0)
        self.motor_y = StepperMotor("Y", max_limit_mm=200.0)
        self.gcode_history = []

    def move_absolute(self, target_x_mm, target_y_mm):
        delta_x = target_x_mm - self.motor_x.get_position_mm()
        delta_y = target_y_mm - self.motor_y.get_position_mm()

        steps_x = int(delta_x * self.motor_x.conversion_factor)
        steps_y = int(delta_y * self.motor_y.conversion_factor)

        try:
            self.motor_x.take_steps(steps_x)
            self.motor_y.take_steps(steps_y)
            generated_line = f"G1 X{target_x_mm} Y{target_y_mm} F1000"
            self.gcode_history.append(generated_line)
            return f"G1 X{target_x_mm} Y{target_y_mm} ; OK"
        except MotorLimitError as e:
            print("System error: Movement aborted for safety")
            return f"; ERROR: {e}"

    def drill_points(self, coordinate_list):
        for x, y in coordinate_list:
            result = self.move_absolute(x, y)

            print(result)

            print("    -> [Z Axis]: Lowering bit... Drilling... Raising bit")

    def export_file(self, file_name="cnc_trajectory.gcode"):
        with open(file_name, 'w') as file:
            for line in self.gcode_history:
                file.write(f"{line}\n")
        print(f"[Hardware] File {file_name} exported successfully.")

    def execute_gcode_command(self, command_text):
        command_text = command_text.strip()
        print(f"\n[G-Code Reader] Parsing instruction: '{command_text}'")

        parts = command_text.split()

        if not parts:
            return

        if parts[0] == "G1":
            x_target = None
            y_target = None
            z_target = None
            e_target = None

            for part in parts:
                if part.startswith("X"):
                    x_target = float(part[1:])
                elif part.startswith("Y"):
                    y_target = float(part[1:])
                elif part.startswith("Z"):
                    z_target = float(part[1:])
                elif part.startswith("E"):
                    e_target = float(part[1:])

            if x_target is not None and y_target is not None:
                self.move_absolute(x_target, y_target)

            if z_target is not None:
                print(f"   -> [Z Axis]: Moving to layer / depth {z_target} mm")

            if e_target is not None:
                print(f"   -> [Extruder]: Pushing {e_target} mm of filament")
        elif parts[0] == "G28":
            self.home()
        else:
            print("ERROR: Command not recognized in the simulation")

# ==========================================
# TEST AREA
# ==========================================
my_plotter = MiniPlotterCNC()

# Simulating a G-Code file from a 3D Printer
print("\n--- SIMULATING 3D PRINTING ---")
my_plotter.execute_gcode_command("G28")  # Homing
my_plotter.execute_gcode_command("G1 Z0.2")
my_plotter.execute_gcode_command("G1 X10 Y10 E1.5")
my_plotter.execute_gcode_command("G1 X20 Y10 E3.0")

# Simulating a G-Code file from a CNC Mill (SolidWorks)
print("\n--- SIMULATING CNC MILLING ---")
my_plotter.execute_gcode_command("G28")
my_plotter.execute_gcode_command("G1 X50 Y50")
my_plotter.execute_gcode_command("G1 Z-5.0")
my_plotter.execute_gcode_command("G1 X60 Y50")

my_plotter.export_file()