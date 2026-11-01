"""Moved to `probe.generated` (agent:2); this package stays importable for one release."""

# restructure-shim: probe.generated
import importlib

_moved = importlib.import_module("probe.generated")
__all__ = getattr(_moved, "__all__", [n for n in dir(_moved) if not n.startswith("_")])


def __getattr__(name):
    return getattr(_moved, name)
