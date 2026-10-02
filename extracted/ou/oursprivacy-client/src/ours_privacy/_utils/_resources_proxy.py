from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `ours_privacy.resources` module.

    This is used so that we can lazily import `ours_privacy.resources` only when
    needed *and* so that users can just import `ours_privacy` and reference `ours_privacy.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("ours_privacy.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
