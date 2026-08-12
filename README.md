# Python CNC Controller

This repository contains scripts in Python developed with object orientes programming to automate and control a mini plotter CNC.
## Características del Código
* **Generation of G-Code:** Methods to automating movement commands (G0, G1, G28).
* **Axis con:** Independent classes to keep empirical records of the position of stepper motors in X, Y and Z.
* **Automatic routines:** Methods integration to draw complex geometric shapes.

## Main files
* `plotter_oop.py`: Defines the top class that groups the engines and generates the final G-Code.

## Use and execution
To test code generation, run the following command in the terminal:
```bash
python3 plotter_oop.py
