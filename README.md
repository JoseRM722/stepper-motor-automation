# Python CNC Controller

A Python driver for hardware automation of stepper-motor-based machines — mini CNC plotters, 3D-printer-style motion, and simple cobot tool-heads — built with an object-oriented architecture.

The project simulates a G-code-driven motion controller: it tracks stepper motor positions, enforces physical safety limits, generates G-code from movement commands, and can parse G-code back into simulated motion.

## Features

- **G-code generation & parsing** — Supports core movement commands (`G0`, `G1`, `G28`) and can both emit and interpret G-code lines.
- **Per-axis motor control** — Independent `StepperMotor` objects track the real-time position of the X and Y axes in steps and millimeters.
- **Encapsulated position tracking** — Motor position is a private attribute; it can only be changed through validated methods, never set directly.
- **Built-in safety limits** — Every movement is checked against a configurable maximum travel distance before it's applied. Out-of-range moves raise a `MotorLimitError` instead of silently corrupting position data.
- **G-code export** — Movement history can be written out to a `.gcode` file for reuse or inspection.
- **Extensible base for tool-equipped machines** — `BaseCobotCNC` provides a foundation for machines that swap tools (e.g. pen, drill, spindle) on top of the same motion system.

## Project structure

| File | Description |
|---|---|
| `plotter_oop.py` | Core motion engine. Defines `StepperMotor` (per-axis position & safety logic) and `MiniPlotterCNC` (the top-level controller that drives the motors and generates/parses G-code). |
| `cobot_oop.py` | Extends the motion system with `BaseCobotCNC`, a base class for tool-equipped machines (drilling, milling, etc.) built on top of the same `StepperMotor` components. |

## How it works

```
StepperMotor        →  tracks one axis (X or Y): position, limits, safety checks
MiniPlotterCNC       →  owns motor_x + motor_y, exposes move_absolute() / drill_points()
                         and both generates and parses G-code
BaseCobotCNC          →  owns motor_x + motor_y, adds tool-equipping (equip())
                         on top of the same motor components
```

Both `MiniPlotterCNC` and `BaseCobotCNC` are built by *composing* `StepperMotor` instances rather than inheriting from them — each machine "has" motors, it isn't one itself. This keeps axis logic (steps, limits, position) fully decoupled from machine-level behavior (drilling, tool changes, G-code parsing).

## Usage

Run the plotter simulation directly:

```bash
python3 plotter_oop.py
```

This will:
1. Home the X/Y axes
2. Simulate a 3D-printer-style G-code sequence (`G1` moves with extrusion)
3. Simulate a CNC-mill-style G-code sequence (`G1` moves with Z-depth)
4. Export all executed moves to `cnc_trajectory.gcode`

### Example: driving the plotter programmatically

```python
from plotter_oop import MiniPlotterCNC

plotter = MiniPlotterCNC()
plotter.home()
plotter.move_absolute(50, 50)
plotter.drill_points([(10, 10), (20, 10), (20, 20)])
plotter.export_file("my_job.gcode")
```

### Example: safety limits in action

```python
from plotter_oop import StepperMotor, MotorLimitError

motor = StepperMotor("X", max_limit_mm=200.0)

try:
    motor.take_steps(999999)  # exceeds the 200mm limit
except MotorLimitError as e:
    print(f"Blocked unsafe move: {e}")
```

## Requirements

- Python 3.8+
- No external dependencies — the standard library is sufficient for the simulation.

*(If this project later drives real hardware — e.g. via `RPi.GPIO`, `pyserial`, or a stepper driver board — list those dependencies here along with wiring notes.)*

## Roadmap / known limitations

- Z-axis and extruder commands are currently logged but not backed by a real `StepperMotor` instance.
- `BaseCobotCNC.move_operate()` is an unimplemented stub — subclasses must override it.
- No unit tests yet.

