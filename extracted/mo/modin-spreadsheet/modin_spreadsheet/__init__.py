try:
    import modin.pandas as pd
except ImportError:
    raise ImportError("Please run `pip install modin`")

from .grid import (
    enable,
    disable,
    set_defaults,
    on,
    off,
    set_grid_option,
    show_grid,
    SpreadsheetWidget,
)
from ._version import get_versions


def _jupyter_nbextension_paths():
    return [
        {
            "section": "notebook",
            "src": "static",
            "dest": "modin_spreadsheet",
            "require": "modin_spreadsheet/extension",
        }
    ]


__all__ = [
    "enable",
    "disable",
    "set_defaults",
    "on",
    "off",
    "set_grid_option",
    "show_grid",
    "SpreadsheetWidget",
]

__version__ = get_versions()["version"]
del get_versions
