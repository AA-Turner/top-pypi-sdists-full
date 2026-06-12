# The canonical urlManager / get_url / get_url_mgr live in .main (re-exported from
# abstract_webtools.imports.src.managers.urlManager). The .src package is an
# optional PyQt6/tiktoken GUI variant whose heavy deps are NOT declared runtime
# requirements, so importing it must never break the core package.
try:
    from .src import *  # optional GUI extras
except Exception:  # pragma: no cover - optional dependency surface
    pass
from .main import *
