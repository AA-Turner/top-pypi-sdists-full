from __future__ import annotations

import importlib
import pkgutil
from importlib.metadata import packages_distributions, version
from typing import TYPE_CHECKING, NamedTuple, cast

from mistralai.workflows.core._logger import get_logger

if TYPE_CHECKING:
    from typing import Type

    from temporalio.worker import Interceptor

PLUGIN_NAMESPACE = cast(str, __package__)  # cast so it's not typed as optional str
SELF = __name__.split(".")[-1]

logger = get_logger(__name__)


class ContributionInfo(NamedTuple):
    name: str
    ispkg: bool
    dist_name: str | None
    dist_version: str | None


def list_plugins() -> list[ContributionInfo]:
    """List names and versions of all installed plugins."""
    pkg_to_dist = packages_distributions()
    results: list[ContributionInfo] = []
    for module_info in pkgutil.iter_modules(importlib.import_module(PLUGIN_NAMESPACE).__path__):
        if module_info.name != SELF:
            import_name = f"{PLUGIN_NAMESPACE}.{module_info.name}"
            dist_names = pkg_to_dist.get(import_name, [])
            (dist_name, dist_version) = (dist_names[0], version(dist_names[0])) if dist_names else (None, None)
            results.append(ContributionInfo(module_info.name, module_info.ispkg, dist_name, dist_version))
    return results


def collect_plugin_interceptors(workflows: list[Type]) -> list[Interceptor]:
    """Discover and collect worker interceptors from installed plugins.

    Each plugin can expose a ``get_worker_interceptors(workflows)`` callable
    at its top-level package.  This function imports every discovered plugin
    and, when the hook exists, calls it to obtain interceptor instances.
    """
    interceptors: list[Interceptor] = []
    for plugin in list_plugins():
        module_name = f"{PLUGIN_NAMESPACE}.{plugin.name}"
        mod = importlib.import_module(module_name)

        hook = getattr(mod, "get_worker_interceptors", None)
        if not callable(hook):
            continue

        plugin_interceptors = hook(workflows)
        interceptors.extend(plugin_interceptors)
        logger.info(
            "Plugin contributed worker interceptors",
            plugin=plugin.name,
            count=len(plugin_interceptors),
        )
    return interceptors
