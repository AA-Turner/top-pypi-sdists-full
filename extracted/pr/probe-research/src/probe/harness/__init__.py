"""Moved to `probe.foundation.harness_registry` (agent:3); this package stays importable for one release."""

# restructure-shim: probe.foundation.harness_registry
import importlib

_moved = importlib.import_module("probe.foundation.harness_registry")
__all__ = getattr(_moved, "__all__", [n for n in dir(_moved) if not n.startswith("_")])


def __getattr__(name):
    return getattr(_moved, name)
