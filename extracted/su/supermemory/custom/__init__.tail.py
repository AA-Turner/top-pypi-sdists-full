# ---------------------------------------------------------------------------
# Hand-written 3.x-compatible surface (custom/supermemory/_compat.py), appended
# by scripts/apply_custom.py, which also drops these names from the lazy-import
# tables above so `supermemory.Supermemory`, `supermemory.NotFoundError`, … are
# the compatible versions.
from importlib.metadata import version as _package_version

from ._compat import *
from ._compat import __all__ as _compat_all

__title__ = "supermemory"
__version__ = _package_version("supermemory")
__all__ += [name for name in _compat_all if name not in __all__]
__all__ += ["__title__", "__version__"]
