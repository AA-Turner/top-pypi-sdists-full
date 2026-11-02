"""One-line entry points that authenticate as the person running the code.

Mirrors ``databaas_utils.airflow``'s helpers, but the identity is the user,
not a pipeline's service account:

- inside a JupyterHub singleuser pod, the token the hub mints for the
  logged-in user (``LakehouseSettings.from_jupyterhub``);
- anywhere else (a laptop notebook, a script, a local app), the session saved
  by ``databaas login`` (``LakehouseSettings.from_profile``).

So the same code runs unchanged on the platform and on a laptop. DAGs must not
use this module: a task authenticates through its Airflow connection.
"""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

from databaas_utils.jupyterhub import in_jupyterhub
from databaas_utils.settings import LakehouseSettings

if TYPE_CHECKING:
    from pyiceberg.catalog import Catalog
    from zarr import Group

    from databaas_utils.generic import GenericTableStore
    from databaas_utils.index import FileIndex

__all__ = [
    "get_catalog",
    "get_index",
    "get_settings",
    "get_store",
    "get_zarr_group",
]


def get_settings(
    *,
    namespace: str | None = None,
    warehouse: str | None = None,
    profile: str | None = None,
) -> LakehouseSettings:
    """Settings for the current user.

    An explicit ``profile`` always means the ``databaas login`` session, even
    inside JupyterHub.

    Args:
        namespace: Default namespace for tables and generic tables.
        warehouse: Overrides the warehouse.
        profile: A ``databaas login`` profile name. Forces the local session.

    Raises:
        ConfigurationError: Outside JupyterHub, if no ``databaas login``
            profile exists.
        AuthenticationError: If a token cannot be obtained.

    Example:
        >>> settings = get_settings(namespace="knmi")
    """
    if profile is None and in_jupyterhub():
        return LakehouseSettings.from_jupyterhub(namespace=namespace, warehouse=warehouse)
    settings = LakehouseSettings.from_profile(profile, namespace=namespace)
    return replace(settings, warehouse=warehouse) if warehouse else settings


def get_catalog(
    *, warehouse: str | None = None, profile: str | None = None, **overrides: str
) -> Catalog:
    """A pyiceberg REST catalog, signing through Lakekeeper.

    Use fully qualified ``namespace.table`` identifiers with it. Needs the
    ``iceberg`` extra.

    Args:
        warehouse: Overrides the warehouse.
        profile: A ``databaas login`` profile name. Forces the local session.
        **overrides: pyiceberg catalog properties that replace the defaults.

    Example:
        >>> catalog = get_catalog()
        >>> catalog.load_table("open_meteo.daily_summary").scan(limit=10).to_arrow()
    """
    from databaas_utils.catalog import rest_catalog

    return rest_catalog(get_settings(warehouse=warehouse, profile=profile), **overrides)


def get_store(
    *,
    namespace: str | None = None,
    warehouse: str | None = None,
    profile: str | None = None,
) -> GenericTableStore:
    """Files under generic tables in ``namespace``, on remote-signed storage.

    Needs the ``obstore`` extra.

    Args:
        namespace: Namespace holding the generic tables.
        warehouse: Overrides the warehouse.
        profile: A ``databaas login`` profile name. Forces the local session.

    Example:
        >>> store = get_store(namespace="knmi")
        >>> store.get("harmonie", "2026/09/30/run.grib2", Path("run.grib2"))
    """
    from databaas_utils.generic import GenericTableStore

    return GenericTableStore(
        get_settings(namespace=namespace, warehouse=warehouse, profile=profile)
    )


def get_index(
    *,
    namespace: str | None = None,
    table: str = "files",
    warehouse: str | None = None,
    profile: str | None = None,
) -> FileIndex:
    """The Iceberg index of what landed in ``namespace``'s generic tables.

    Args:
        namespace: Namespace holding the index table.
        table: Index table name.
        warehouse: Overrides the warehouse.
        profile: A ``databaas login`` profile name. Forces the local session.

    Example:
        >>> get_index(namespace="knmi").scan(limit=10)
    """
    from databaas_utils.index import FileIndex

    return FileIndex(
        get_settings(namespace=namespace, warehouse=warehouse, profile=profile),
        table=table,
    )


def get_zarr_group(
    table: str,
    *,
    namespace: str | None = None,
    path: str = "",
    read_only: bool = False,
    create: bool = True,
    doc: str = "Zarr store",
    warehouse: str | None = None,
    profile: str | None = None,
) -> Group:
    """A zarr group stored under the generic table ``namespace.table``.

    Needs the ``zarr`` extra. Opening for write creates the table if missing,
    so pass ``read_only=True`` when you only want to look.

    Args:
        table: Generic table holding the zarr store.
        namespace: Namespace holding the table.
        path: Group path within the store.
        read_only: Open for reading only.
        create: Create the table and group if missing (ignored if ``read_only``).
        doc: Description recorded on a newly created table.
        warehouse: Overrides the warehouse.
        profile: A ``databaas login`` profile name. Forces the local session.

    Example:
        >>> group = get_zarr_group("harmonie_zarr", namespace="knmi", read_only=True)
        >>> list(group.keys())
    """
    from databaas_utils.zarr import open_zarr_group

    return open_zarr_group(
        get_settings(namespace=namespace, warehouse=warehouse, profile=profile),
        table,
        path=path,
        read_only=read_only,
        create=create,
        doc=doc,
    )
