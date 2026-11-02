"""Zarr groups backed by a Lakekeeper generic table.

Iceberg models tables; numerical weather output is multidimensional gridded
arrays, so the payload itself is written as zarr into a generic table and the
Iceberg side only records what landed (see `databaas_utils.index`).

This is the same signed object store `GenericTableStore` uses — zarr just gets a
`zarr.storage.ObjectStore` wrapper around it instead of put/get. It lives in its
own module because zarr is the heaviest optional dependency here and nothing
else needs it.

**Install plain ``zarr``, never ``zarr[remote]``.** That extra depends on upstream
`obstore`, which shares a top-level module name with `obstore-databaas` and
would silently overwrite it — taking `RemoteSignedS3Store`, and every signed
write, with it. The object store is supplied here, so the extra buys nothing.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Literal

from databaas_utils.catalog import CatalogClient
from databaas_utils.generic import resolve, signed_store
from databaas_utils.settings import LakehouseSettings

if TYPE_CHECKING:
    from zarr import Group

__all__ = ["local_zarr_group", "open_zarr_group"]


def _mode(*, read_only: bool, create: bool) -> Literal["r", "r+", "a"]:
    if read_only:
        return "r"
    return "a" if create else "r+"


def open_zarr_group(
    settings: LakehouseSettings,
    table: str,
    *,
    path: str = "",
    read_only: bool = False,
    create: bool = True,
    doc: str = "Zarr store",
    client: CatalogClient | None = None,
) -> Group:
    """Open a zarr group stored under `settings.namespace`.`table`.

    Reads and writes are remote-signed by Lakekeeper; no S3 credentials are
    involved. `create` is ignored when `read_only` is set — opening a reader
    should never create a table as a side effect. Needs the ``zarr`` extra.

    Args:
        settings: Which warehouse and namespace, as which identity.
        table: Generic table holding the zarr store; created if missing when
            ``create`` is true.
        path: Group path within the store.
        read_only: Open for reading only.
        create: Create the table and group if missing.
        doc: Description recorded on a newly created table.
        client: A ``CatalogClient`` to reuse.

    Returns:
        A ``zarr.Group``.

    Example:
        >>> group = open_zarr_group(settings, "harmonie_zarr", read_only=True)
        >>> list(group.keys())
    """
    # Absolute import: this module is `databaas_utils.zarr`, but Python 3
    # resolves this to the top-level zarr package, not to itself.
    import zarr
    from zarr.storage import ObjectStore

    create = create and not read_only
    resolved = resolve(settings, table, create=create, doc=doc, client=client)
    store = ObjectStore(signed_store(settings, resolved), read_only=read_only)
    return zarr.open_group(
        store=store, path=path or "", mode=_mode(read_only=read_only, create=create)
    )


def local_zarr_group(
    root: str | Path,
    table: str,
    *,
    path: str = "",
    read_only: bool = False,
    create: bool = True,
) -> Group:
    """A zarr group on the local filesystem, for laptop runs and tests.

    Explicit, never a fallback: a missing catalog connection raises rather than
    silently redirecting a production write to an ephemeral pod disk.

    Args:
        root: Directory that plays the role of the warehouse.
        table: Subdirectory holding the zarr store.
        path: Group path within the store.
        read_only: Open for reading only.
        create: Create the directory and group if missing.
    """
    import zarr
    from zarr.storage import LocalStore

    create = create and not read_only
    directory = Path(root) / table
    if create:
        directory.mkdir(parents=True, exist_ok=True)
    store = LocalStore(directory, read_only=read_only)
    return zarr.open_group(
        store=store, path=path or "", mode=_mode(read_only=read_only, create=create)
    )
