"""Moved to `probe.mcp.tools.reads.listings`; this package stays importable for one release."""

# restructure-shim: probe.mcp.tools.reads.listings
import importlib
import importlib.util

_moved = importlib.import_module("probe.mcp.tools.reads.listings")
__all__ = getattr(_moved, "__all__", [n for n in dir(_moved) if not n.startswith("_")])


def __getattr__(name):
    # A module stub beside this file wins: `x.py` moved into `x/` leaves the moved package's
    # `x` a subpackage, and `from <old> import x` must still give the moved module.
    if importlib.util.find_spec(f"{__name__}.{name}") is not None:
        return importlib.import_module(f"{__name__}.{name}")
    return getattr(_moved, name)
