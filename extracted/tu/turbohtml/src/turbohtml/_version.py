from pathlib import Path as _Path
from typing import Final

from . import __file__ as _PACKAGE_FILE

__version__: Final[str]
if _Path(__file__).parent == _Path(_PACKAGE_FILE).parent:
    __version__ = "1.13.1"
else:
    # Editable rebuilds can change Meson's version without replacing installed metadata.
    from importlib.metadata import version as _installed_version

    __version__ = _installed_version("turbohtml")

__all__ = ["__version__"]
