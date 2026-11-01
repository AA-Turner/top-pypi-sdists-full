"""Moved to `probe.shared.harness.lookup` (agent:13); this package stays importable for one release."""

# restructure-shim: probe.shared.harness.lookup
import importlib

_moved = importlib.import_module("probe.shared.harness.lookup")
__all__ = getattr(_moved, "__all__", [n for n in dir(_moved) if not n.startswith("_")])


def __getattr__(name):
    return getattr(_moved, name)
