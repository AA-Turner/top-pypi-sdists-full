import importlib.metadata
__version__ = importlib.metadata.version("mi_proyecto_joaquin_vft")
from .voftools import voftools_dim3d
(ns,nv) = voftools_dim3d()
stack_usage = ns * nv * 60 / (1024 * 1024)
if stack_usage > 7:
    print("----------------------------------------------------------")
    print(f"WARNING: High stack usage detected ({stack_usage:.2f} MB).")
    print("Ensure 'ulimit -s' or 'OMP_STACKSIZE' is set correctly.   ")
    print("----------------------------------------------------------")
