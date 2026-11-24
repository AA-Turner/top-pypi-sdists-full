"""Gate-side queries for the external-object publication path.

The meet recording publication scope locks and reads ``files.files`` /
``files.folders`` rows inside ONE caller-owned transaction (``SELECT ... FOR
UPDATE``). The queries live here, in the gate package, so no host module
queries the files tables directly (scripts/check_file_access_gate.py). They
are internal-job primitives: the caller has already admitted the operation
(worker lease + custody checks); nothing here is a user-facing read.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import PurePosixPath
from typing import Any


async def file_ids_for_publication(*, storage_uri: str, owner_id: str | None = None, file_path: str | None = None) -> set[str]:
    """Ids of file rows at ``storage_uri`` plus (optionally) the owner's row at ``file_path``."""
    from matrx_files.db.models_files import Files

    ids: set[str] = set()
    for row in await Files.filter(storage_uri=storage_uri).values("id"):
        ids.add(str(row["id"]))
    if owner_id is not None and file_path is not None:
        for row in await Files.filter(created_by=owner_id, file_path=file_path).values("id"):
            ids.add(str(row["id"]))
    return ids


async def lock_publication_rows(file_ids: Iterable[str], *, owner_id: str | None = None, file_path: str | None = None) -> None:
    """Lock the file rows (ordered by id) then the owner's ancestor folders, in the open transaction."""
    from matrx_files.db.models_files import Files, Folders

    ids = sorted(set(file_ids))
    if ids:
        await Files.filter(id__in=ids).order_by("id").select_for_update().all(use_cache=False)
    if owner_id is not None and file_path is not None:
        paths = [str(p) for p in PurePosixPath(file_path).parents if str(p) != "."]
        await Folders.filter(created_by=owner_id, folder_path__in=paths).order_by("id").select_for_update().all(use_cache=False)


async def live_file_rows_at_path(*, owner_id: str, file_path: str) -> list[dict[str, Any]]:
    """The owner's non-deleted file rows at ``file_path`` with the custody columns."""
    from matrx_files.db.models_files import Files

    return await Files.filter(
        created_by=owner_id, file_path=file_path, deleted_at__isnull=True,
    ).values("id", "organization_id", "storage_uri", "metadata", "checksum", "size_bytes", "mime_type", "duplicate_of_file_id")
