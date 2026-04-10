from __future__ import annotations

from typing import TYPE_CHECKING

# Lazy imports for faster subprocess startup (python -m kolo._emit_auto)
# The actual imports only happen when enable/enabled/etc are accessed.
# Uses PEP 562 module-level __getattr__ (Python 3.7+).

# TYPE_CHECKING block ensures IDEs and mypy know these attributes exist
if TYPE_CHECKING:
    from .core import enable, enabled


def __getattr__(name: str):
    if name in ("enable", "enabled"):
        from .core import enable, enabled

        globals()["enable"] = enable
        globals()["enabled"] = enabled
        return globals()[name]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    """Ensure dir(kolo) shows the lazy-loaded attributes."""
    return sorted(__all__ + list(globals().keys()))


__all__ = ["enable", "enabled"]
