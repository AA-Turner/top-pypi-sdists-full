"""The realtime publication's column list is an ALLOWLIST, and it cannot widen.

``files.files`` is published with an explicit 23-column list that EXCLUDES
``storage_uri``. That fixed list -- not a policy, not a view -- is how the
2026-07-06 storage-uri leak ruling is actually enforced, and it is why migration
028's two new columns (``origin_device_id``, ``client_modified_at``) do NOT
appear on realtime payloads: a fixed list does not grow when the table does.
That is harmless under D9 (the change feed is the only truth for sync) and it
must stay a DECISION, not an accident.

The failure mode this guard exists for: somebody notices the new fields are
missing from realtime and "fixes" it with
``ALTER PUBLICATION supabase_realtime ADD TABLE files.files`` -- no column list
-- which silently re-opens ``storage_uri`` to every subscriber. Or sets
``REPLICA IDENTITY FULL``, which publishes every column of the OLD row
regardless of the list. Both go red here.

Marked ``integration``: reads pg_publication_rel on the live database.
"""

from __future__ import annotations

import os

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")

#: The exact published set for files.files (live, 2026-09-13). Adding a name
#: here is a deliberate act with a leak review behind it, never a side effect.
FILES_ALLOWLIST = {
    "canonical_processed_document_id",
    "checksum",
    "created_at",
    "created_by",
    "current_version",
    "deleted_at",
    "derivation_kind",
    "derivation_metadata",
    "duplicate_of_file_id",
    "duration_ms",
    "file_name",
    "file_path",
    "height",
    "id",
    "metadata",
    "mime_type",
    "organization_id",
    "parent_file_id",
    "parent_folder_id",
    "size_bytes",
    "updated_at",
    "visibility",
    "width",
}

#: Never published. The bucket/key of the object is a credential-shaped value.
FORBIDDEN = {"storage_uri", "canonical_storage_uri"}

#: Never published from files.sync_mappings: a person's own filesystem.
PATH_PRIVATE = {"local_path", "local_path_display", "state_reason", "knobs"}


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


async def _published(schema: str, table: str) -> tuple[set[str] | None, str]:
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    async with acquire_connection(bootstrap_db()) as conn:
        row = await conn.fetchrow(
            """
            SELECT (SELECT array_agg(a.attname)
                      FROM unnest(pr.prattrs) k
                      JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = k) AS cols,
                   c.relreplident AS replident
              FROM pg_publication_rel pr
              JOIN pg_publication p ON p.oid = pr.prpubid
              JOIN pg_class c ON c.oid = pr.prrelid
              JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE p.pubname = 'supabase_realtime' AND n.nspname = $1 AND c.relname = $2
            """,
            schema,
            table,
        )
    if row is None:
        return None, ""
    cols = row["cols"]
    return (set(cols) if cols is not None else None), row["replident"]


async def test_files_is_published_with_the_exact_allowlist():
    _skip_without_db()
    published, _ = await _published("files", "files")
    assert published is not None, (
        "files.files is published with NO column list -- every column, including "
        "storage_uri, now reaches every realtime subscriber. Restore the explicit "
        "list with ALTER PUBLICATION supabase_realtime SET TABLE files.files (...)."
    )
    assert published == FILES_ALLOWLIST, (
        f"the published column set changed. Added: {sorted(published - FILES_ALLOWLIST)}; "
        f"removed: {sorted(FILES_ALLOWLIST - published)}. Widening this list is a leak "
        "review, not a migration side effect."
    )
    assert not (published & FORBIDDEN)


async def test_migration_028s_columns_are_deliberately_absent_from_the_wire():
    _skip_without_db()
    published, _ = await _published("files", "files")
    assert published is not None
    assert "origin_device_id" not in published
    assert "client_modified_at" not in published, (
        "If these are wanted on the wire, the change is SET TABLE with the whole "
        "23-column list named in full PLUS the two -- never ADD TABLE without a list."
    )


async def test_files_does_not_have_replica_identity_full():
    """REPLICA IDENTITY FULL publishes every column of the old row, list or not."""
    _skip_without_db()
    _, replident = await _published("files", "files")
    assert replident != "f", (
        "files.files is REPLICA IDENTITY FULL: the column allowlist no longer "
        "protects storage_uri on UPDATE/DELETE payloads."
    )


async def test_sync_mappings_publication_allowlist():
    """The §6.2 half — only the changing STATUS rides the wire.

    ``local_path`` / ``local_path_display`` / ``state_reason`` / ``knobs`` are
    absolute paths inside one person's home directory and the remedy text about
    their machine. The browser reads those over the ordinary owner-only RLS
    SELECT; they are never broadcast. A soft-delete still arrives as an UPDATE
    with ``deleted_at`` set, so removal remains visible on the wire.
    """
    _skip_without_db()
    published, replident = await _published("files", "sync_mappings")
    assert published is not None, (
        "files.sync_mappings is not published with a column list. Publishing it "
        "without one broadcasts local_path to every subscriber."
    )
    assert not (published & PATH_PRIVATE), (
        f"the wire now carries {sorted(published & PATH_PRIVATE)}"
    )
    assert published == {
        "id",
        "created_by",
        "device_id",
        "folder_id",
        "organization_id",
        "direction",
        "desired_state",
        "state",
        "state_changed_at",
        "last_seen_at",
        "last_synced_at",
        "items_total",
        "bytes_total",
        "version",
        "created_at",
        "updated_at",
        "deleted_at",
    }
    assert replident != "f"
