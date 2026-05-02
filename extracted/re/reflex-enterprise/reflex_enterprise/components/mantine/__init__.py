"""Mantine sub-package."""

from reflex.utils import lazy_loader

from reflex_enterprise import _MANTINE_MAPPING

_SUBMODULES = set()
_SUBMOD_ATTRS = {
    "".join(k.split("components.mantine.")[-1]): v for k, v in _MANTINE_MAPPING.items()
}

_SUBMOD_ATTRS.update(
    {
        "base": ["base"],
    }
)

__getattr__, __dir__, __all__ = lazy_loader.attach(
    __name__,
    submodules=_SUBMODULES,
    submod_attrs=_SUBMOD_ATTRS,
)
