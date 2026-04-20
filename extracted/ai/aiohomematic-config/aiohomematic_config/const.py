"""
Constants and version for aiohomematic-config.

Public API of this module is defined by __all__.
"""

import inspect
from typing import Final

VERSION: Final = "2026.4.4"

# Widget slider threshold: if an integer range is <= this value, use a slider
SLIDER_RANGE_THRESHOLD: Final = 20

# Widget radio group threshold: if an enum has <= this many options, use radio buttons
RADIO_GROUP_THRESHOLD: Final = 4

# Default locale
DEFAULT_LOCALE: Final = "en"

__all__ = tuple(
    sorted(
        name
        for name, obj in globals().items()
        if not name.startswith("_")
        and (name.isupper() or inspect.isfunction(obj) or inspect.isclass(obj))
        and getattr(obj, "__module__", __name__) == __name__
    )
)
