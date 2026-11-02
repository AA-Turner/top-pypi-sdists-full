"""One-line entry points for DAG code.

Every one takes `conn_id=` so a DAG needing different Lakekeeper permissions can
point at a second service account, and `namespace=` so a pipeline can keep its
tables somewhere other than the connection's default.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from databaas_utils.airflow.connection import DEFAULT_CONN_ID, get_settings

if TYPE_CHECKING:
    from pyiceberg.catalog import Catalog
    from zarr import Group

    from databaas_utils.generic import BlobStore
    from databaas_utils.index import Index
    from databaas_utils.settings import LakehouseSettings

__all__ = [
    "get_catalog",
    "get_index",
    "get_settings",
    "get_store",
    "get_zarr_group",
]


def get_catalog(
    *, conn_id: str = DEFAULT_CONN_ID, namespace: str | None = None
) -> Catalog:
    """A pyiceberg REST catalog, signing through Lakekeeper.

    Args:
        conn_id: The Airflow connection to authenticate with.
        namespace: Overrides the connection's default namespace.

    Example:
        >>> catalog = get_catalog()
        >>> catalog.load_table("open_meteo.daily_summary")
    """
    from databaas_utils.catalog import rest_catalog

    return rest_catalog(get_settings(conn_id, namespace=namespace))


def get_store(
    *,
    conn_id: str = DEFAULT_CONN_ID,
    namespace: str | None = None,
    local_root: str | None = None,
) -> BlobStore:
    """Blob access under generic tables.

    `local_root` is an explicit opt-in to the filesystem stand-in. It is never
    reached by falling back: a missing connection raises, because a silent
    local write that reports success is worse than a failed task.

    Args:
        conn_id: The Airflow connection to authenticate with.
        namespace: Overrides the connection's default namespace.
        local_root: Directory to use instead of the lakehouse (local runs).

    Example:
        >>> store = get_store()
        >>> store.put("grib", "2026/09/30/run.grib2", Path("run.grib2"))
    """
    if local_root is not None:
        from pathlib import Path

        from databaas_utils.generic import LocalStore

        return LocalStore(Path(local_root))

    from databaas_utils.generic import GenericTableStore

    return GenericTableStore(get_settings(conn_id, namespace=namespace))


def get_index(
    *,
    conn_id: str = DEFAULT_CONN_ID,
    namespace: str | None = None,
    table: str = "files",
) -> Index:
    """The Iceberg index of what landed in the generic tables.

    Args:
        conn_id: The Airflow connection to authenticate with.
        namespace: Overrides the connection's default namespace.
        table: Index table name.
    """
    from databaas_utils.index import FileIndex

    return FileIndex(get_settings(conn_id, namespace=namespace), table=table)


def get_zarr_group(
    table: str,
    *,
    conn_id: str = DEFAULT_CONN_ID,
    namespace: str | None = None,
    path: str = "",
    read_only: bool = False,
    create: bool = True,
    doc: str = "Zarr store",
    local_root: str | None = None,
) -> Group:
    """A zarr group under a generic table.

    `local_root` is an explicit opt-in to the filesystem, as with `get_store`.

    Args:
        table: Generic table holding the zarr store.
        conn_id: The Airflow connection to authenticate with.
        namespace: Overrides the connection's default namespace.
        path: Group path within the store.
        read_only: Open for reading only.
        create: Create the table and group if missing.
        doc: Description recorded on a newly created table.
        local_root: Directory to use instead of the lakehouse (local runs).

    Example:
        >>> group = get_zarr_group("harmonie_zarr", path="2026093000")
    """
    if local_root is not None:
        from databaas_utils.zarr import local_zarr_group

        return local_zarr_group(
            local_root, table, path=path, read_only=read_only, create=create
        )

    from databaas_utils.zarr import open_zarr_group

    return open_zarr_group(
        get_settings(conn_id, namespace=namespace),
        table,
        path=path,
        read_only=read_only,
        create=create,
        doc=doc,
    )


def get_lakehouse_settings(
    *, conn_id: str = DEFAULT_CONN_ID, namespace: str | None = None
) -> LakehouseSettings:
    """Settings alone, for callers building something the helpers do not cover.

    Args:
        conn_id: The Airflow connection to authenticate with.
        namespace: Overrides the connection's default namespace.
    """
    return get_settings(conn_id, namespace=namespace)
