from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `coreweave_evaluations.resources` module.

    This is used so that we can lazily import `coreweave_evaluations.resources` only when
    needed *and* so that users can just import `coreweave_evaluations` and reference `coreweave_evaluations.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("coreweave_evaluations.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
