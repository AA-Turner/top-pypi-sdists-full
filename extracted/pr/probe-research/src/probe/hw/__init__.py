"""Moved to `probe.sdk.hardware` (agent:6); this package stays importable for one release."""

# restructure-shim: probe.sdk.hardware
import importlib

_moved = importlib.import_module("probe.sdk.hardware")
__all__ = getattr(_moved, "__all__", [n for n in dir(_moved) if not n.startswith("_")])


def __getattr__(name):
    return getattr(_moved, name)
