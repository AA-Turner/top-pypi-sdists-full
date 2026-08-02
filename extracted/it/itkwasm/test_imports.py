#!/usr/bin/env python3

try:
    from itkwasm import TransformList
    print("TransformList import: SUCCESS")
except ImportError as e:
    print(f"TransformList import: FAILED - {e}")

try:
    from itkwasm.pyodide import to_js, to_py
    print("Pyodide imports: SUCCESS")
except ImportError as e:
    print(f"Pyodide imports: FAILED - {e}")

try:
    from itkwasm import Transform, TransformType, TransformParameterizations, FloatTypes
    print("Transform related imports: SUCCESS")
except ImportError as e:
    print(f"Transform related imports: FAILED - {e}")

print("All imports completed")
