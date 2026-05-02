"""Components for Reflex Enterprise."""

from __future__ import annotations

from reflex.utils import lazy_loader

_SUBMODULES: set[str] = {
    "ag_grid",
    "ag_charts",
    "flow",
    "mantine",
    "dnd",
    "map",
}

_SUBMOD_ATTRS: dict[str, list[str]] = {}

__getattr__, __dir__, __all__ = lazy_loader.attach(
    __name__,
    submodules=_SUBMODULES,
    submod_attrs=_SUBMOD_ATTRS,
)
