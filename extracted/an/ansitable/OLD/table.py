import importlib.util
import os

# Load implementation from src/ansitable/table.py when present so local imports
# work with the src layout during development.
_here = os.path.dirname(__file__)
_src_table = os.path.normpath(os.path.join(_here, "..", "src", "ansitable", "table.py"))

if os.path.isfile(_src_table):
    spec = importlib.util.spec_from_file_location("ansitable._table_impl", _src_table)
    _mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_mod)
    for _name in getattr(_mod, "__all__", [n for n in dir(_mod) if not n.startswith("_")]):
        globals()[_name] = getattr(_mod, _name)
else:
    raise ImportError("src/ansitable/table.py not found; install package or run from src layout")
