from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy
from ..lib._resource_runs import install_resource_run_methods  # boltz-api-custom-line

# <boltz-api-custom-code>
install_resource_run_methods()
# </boltz-api-custom-code>


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `boltz_api.resources` module.

    This is used so that we can lazily import `boltz_api.resources` only when
    needed *and* so that users can just import `boltz_api` and reference `boltz_api.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("boltz_api.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
