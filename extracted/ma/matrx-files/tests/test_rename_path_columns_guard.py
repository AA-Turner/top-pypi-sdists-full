"""A file's name and location are written by the PRIMITIVES or not at all.

`scripts/check_single_rename_path.py` is a grep. The hostile re-verify planted
five shapes inside its own scan roots and it missed all five: a dict built in
another function, ORM `.update(file_name=…)` kwargs, a module-constant key, raw
SQL, and `updates.update({...})`. A guard that a five-line edit walks past is a
tripwire, not a proof — and the thing it is guarding is the unique key and the
field every replica holds on disk.

Migration 038 makes it STRUCTURAL, in the database, where shape and arity cannot
help you: a BEFORE UPDATE trigger on `files.files` refuses any change to
`file_name`, `file_path` or `parent_folder_id` unless the transaction-local GUC
that ONLY `public.rename_file`, `public.move_file` and `public.rename_folder` set
is present — the same pattern as the tombstone floor. Raw SQL, a new ORM call, a
psql session and a future helper nobody told the grep about are all refused
identically.

ONE allowance, narrow and deliberate: back-filling a NULL `parent_folder_id` with
the folder whose `folder_path` already equals the row's own directory. 1,666
alive rows carry a nested path with no parent pointer, and reconciling those is
not a move. It is tested both ways.

Every row here is created inside a transaction that is ALWAYS rolled back.
"""

from __future__ import annotations

import os
import uuid

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


async def _conn():
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    return acquire_connection(bootstrap_db())


async def _seed(conn, *, path_suffix: str = "original.txt", parent: str | None = None):
    row = await conn.fetchrow(
        "SELECT user_id::text AS owner, organization_id::text AS org "
        "FROM public.app_instances WHERE deleted_at IS NULL "
        "AND organization_id IS NOT NULL LIMIT 1"
    )
    if row is None:
        pytest.skip("no seed identity available")
    tag = uuid.uuid4().hex[:10]
    folder_path = f"GuardProbe/{tag}"
    file_id = await conn.fetchval(
        "INSERT INTO files.files (created_by, organization_id, file_path, file_name, "
        "storage_uri, mime_type, size_bytes, parent_folder_id) "
        "VALUES ($1::uuid,$2::uuid,$3,$4,$5,'text/plain',3,$6::uuid) RETURNING id::text",
        row["owner"], row["org"], f"{folder_path}/{path_suffix}",
        path_suffix, f"s3://probe/{tag}", parent,
    )
    return file_id, row["owner"], row["org"], folder_path


@pytest.mark.parametrize(
    ("column", "value"),
    [("file_name", "'hacked.txt'"), ("file_path", "'elsewhere/hacked.txt'")],
)
async def test_a_raw_update_of_the_path_columns_is_refused(column, value) -> None:
    """THE shape the grep cannot see: raw SQL, no dict, no helper."""
    _skip_without_db()
    import asyncpg

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            file_id, *_ = await _seed(conn)
            sp = conn.transaction()
            await sp.start()
            with pytest.raises(asyncpg.InsufficientPrivilegeError) as exc:
                await conn.execute(
                    f"UPDATE files.files SET {column} = {value} WHERE id = $1::uuid", file_id
                )
            await sp.rollback()
            assert "public.rename_file" in str(exc.value)
            name = await conn.fetchval(
                "SELECT file_name FROM files.files WHERE id = $1::uuid", file_id
            )
            assert name == "original.txt"
        finally:
            await tx.rollback()


async def test_an_ordinary_update_of_other_columns_is_untouched() -> None:
    """The guard must not become a tax on every write to the table."""
    _skip_without_db()
    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            file_id, *_ = await _seed(conn)
            await conn.execute(
                "UPDATE files.files SET size_bytes = 99, mime_type='text/csv' "
                "WHERE id = $1::uuid", file_id
            )
            assert await conn.fetchval(
                "SELECT size_bytes FROM files.files WHERE id = $1::uuid", file_id
            ) == 99
        finally:
            await tx.rollback()


async def test_rename_file_still_works_through_the_guard() -> None:
    _skip_without_db()
    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            file_id, *_ = await _seed(conn)
            await conn.fetchval(
                "SELECT public.rename_file($1::uuid, $2)", file_id, "renamed.txt"
            )
            name, path = await conn.fetchrow(
                "SELECT file_name, file_path FROM files.files WHERE id = $1::uuid", file_id
            )
            assert name == "renamed.txt"
            assert path.endswith("/renamed.txt")
        finally:
            await tx.rollback()


async def test_the_token_is_withdrawn_so_a_later_hand_update_still_fails() -> None:
    """Arity-proof AND scope-proof: one rename does not license the next write.

    A transaction-local GUC that stayed set would turn every successful rename
    into an open door for the rest of that transaction.
    """
    _skip_without_db()
    import asyncpg

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            file_id, *_ = await _seed(conn)
            await conn.fetchval(
                "SELECT public.rename_file($1::uuid, $2)", file_id, "renamed.txt"
            )
            sp = conn.transaction()
            await sp.start()
            with pytest.raises(asyncpg.InsufficientPrivilegeError):
                await conn.execute(
                    "UPDATE files.files SET file_name = 'sneaky.txt' WHERE id = $1::uuid",
                    file_id,
                )
            await sp.rollback()
        finally:
            await tx.rollback()


async def test_a_token_for_another_row_does_not_authorise_this_one() -> None:
    """The GUC carries a row id, so it cannot be borrowed sideways."""
    _skip_without_db()
    import asyncpg

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            victim, *_ = await _seed(conn)
            await conn.execute(
                "SELECT set_config('matrx.rename_primitive', $1, true)", str(uuid.uuid4())
            )
            sp = conn.transaction()
            await sp.start()
            with pytest.raises(asyncpg.InsufficientPrivilegeError):
                await conn.execute(
                    "UPDATE files.files SET file_name = 'sneaky.txt' WHERE id = $1::uuid",
                    victim,
                )
            await sp.rollback()
        finally:
            await tx.rollback()


async def test_backfilling_a_null_parent_pointer_is_allowed() -> None:
    """The one allowance: a NULL pointer filled with the row's OWN directory."""
    _skip_without_db()
    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            file_id, owner, org, folder_path = await _seed(conn)
            await conn.execute(
                "UPDATE files.files SET parent_folder_id = NULL WHERE id = $1::uuid", file_id
            )
            folder_id = await conn.fetchval(
                "INSERT INTO files.folders (created_by, organization_id, folder_path, folder_name) "
                "VALUES ($1::uuid,$2::uuid,$3,$4) RETURNING id::text",
                owner, org, folder_path, folder_path.rsplit("/", 1)[-1],
            )
            await conn.execute(
                "UPDATE files.files SET parent_folder_id = $2::uuid WHERE id = $1::uuid",
                file_id, folder_id,
            )
            assert await conn.fetchval(
                "SELECT parent_folder_id::text FROM files.files WHERE id = $1::uuid", file_id
            ) == folder_id
        finally:
            await tx.rollback()


async def test_repointing_to_a_folder_that_is_not_the_rows_directory_is_refused() -> None:
    """That is a MOVE wearing a back-fill's clothes, and it produces drift."""
    _skip_without_db()
    import asyncpg

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            file_id, owner, org, _folder_path = await _seed(conn)
            await conn.execute(
                "UPDATE files.files SET parent_folder_id = NULL WHERE id = $1::uuid", file_id
            )
            elsewhere = await conn.fetchval(
                "INSERT INTO files.folders (created_by, organization_id, folder_path, folder_name) "
                "VALUES ($1::uuid,$2::uuid,$3,'elsewhere') RETURNING id::text",
                owner, org, f"Elsewhere/{uuid.uuid4().hex[:8]}",
            )
            sp = conn.transaction()
            await sp.start()
            with pytest.raises(asyncpg.InsufficientPrivilegeError) as exc:
                await conn.execute(
                    "UPDATE files.files SET parent_folder_id = $2::uuid WHERE id = $1::uuid",
                    file_id, elsewhere,
                )
            await sp.rollback()
            assert "public.move_file" in str(exc.value)
        finally:
            await tx.rollback()
