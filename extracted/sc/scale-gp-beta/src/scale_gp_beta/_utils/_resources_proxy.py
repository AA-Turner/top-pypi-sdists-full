from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `scale_gp_beta.resources` module.

    This is used so that we can lazily import `scale_gp_beta.resources` only when
    needed *and* so that users can just import `scale_gp_beta` and reference `scale_gp_beta.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("scale_gp_beta.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
