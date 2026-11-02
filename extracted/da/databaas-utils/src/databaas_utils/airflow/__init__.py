"""Airflow-facing helpers.

Everything under this subpackage may import Airflow freely — these modules only
exist in a process where Airflow is installed. Nothing *outside* it may, and CI
enforces that with an import-linter contract rather than a runtime try/except.

Re-exports are lazy for the same reason as the top-level package: resolving a
deployment target must not drag pyiceberg and obstore into the dag-processor.
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

_LAZY: dict[str, str] = {
    "ConnectionData": "databaas_utils.airflow.connection",
    "DEFAULT_CONN_ID": "databaas_utils.airflow.connection",
    "get_settings": "databaas_utils.airflow.connection",
    "resolve_connection": "databaas_utils.airflow.connection",
    "settings_from_connection": "databaas_utils.airflow.connection",
    "get_catalog": "databaas_utils.airflow.helpers",
    "get_index": "databaas_utils.airflow.helpers",
    "get_store": "databaas_utils.airflow.helpers",
    "get_zarr_group": "databaas_utils.airflow.helpers",
    "LakehouseHook": "databaas_utils.airflow.hook",
    "DeploymentTarget": "databaas_utils.airflow.target",
    "target": "databaas_utils.airflow.target",
    "target_for": "databaas_utils.airflow.target",
    "current_slug": "databaas_utils.airflow.scoping",
    "scoped": "databaas_utils.airflow.scoping",
}

__all__ = [
    "DEFAULT_CONN_ID",
    "ConnectionData",
    "DeploymentTarget",
    "LakehouseHook",
    "current_slug",
    "get_catalog",
    "get_index",
    "get_settings",
    "get_store",
    "get_zarr_group",
    "resolve_connection",
    "scoped",
    "settings_from_connection",
    "target",
    "target_for",
]


def __getattr__(name: str) -> Any:
    module = _LAZY.get(name)
    if module is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return getattr(import_module(module), name)


def __dir__() -> list[str]:
    return list(__all__)


if TYPE_CHECKING:
    from databaas_utils.airflow.connection import (
        DEFAULT_CONN_ID,
        ConnectionData,
        get_settings,
        resolve_connection,
        settings_from_connection,
    )
    from databaas_utils.airflow.helpers import (
        get_catalog,
        get_index,
        get_store,
        get_zarr_group,
    )
    from databaas_utils.airflow.hook import LakehouseHook
    from databaas_utils.airflow.scoping import current_slug, scoped
    from databaas_utils.airflow.target import DeploymentTarget, target, target_for
