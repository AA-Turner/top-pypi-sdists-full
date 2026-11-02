"""`rename_file` validates the NAME before it normalizes it (SPEC-SERVER §4.3).

The shipped body trimmed first and checked second:

    p_new_name := trim(both '/' from coalesce(p_new_name,''));
    IF p_new_name = '' OR position('/' in p_new_name) > 0 THEN RAISE ...

so the single-segment test only ever saw the ALREADY-TRIMMED string. A caller
sending a path fragment got it silently normalized into a different name than it
asked for, and a whitespace-only name was accepted and written:

    'a/b'        -> rejected  (the only one that worked)
    'trailing/'  -> accepted, renamed to 'trailing'
    '/leading'   -> accepted, renamed to 'leading'
    '   '        -> accepted, written as three spaces

Silently renaming a file to something the caller did not ask for is the same
class of defect as the silent path drift migration 031 had to repair. The order
is now: reject any '/' in what the CALLER SENT, then normalize (NFC + whitespace
trim), then reject empty.

Every row here is created inside a transaction that is ALWAYS rolled back.
"""

from __future__ import annotations

import os
import uuid

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")

#: The four cases the §4.3 amendment names. Every one must be REFUSED.
REFUSED_NAMES = ["a/b", "trailing/", "/leading", "   "]


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


async def _conn():
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    return acquire_connection(bootstrap_db())


async def _seed(conn) -> str:
    row = await conn.fetchrow(
        "SELECT user_id::text AS owner, organization_id::text AS org "
        "FROM public.app_instances "
        "WHERE deleted_at IS NULL AND organization_id IS NOT NULL LIMIT 1"
    )
    if row is None:
        pytest.skip("no seed identity available on this database")
    tag = uuid.uuid4().hex[:10]
    return await conn.fetchval(
        "INSERT INTO files.files (created_by, organization_id, file_path, file_name, "
        "storage_uri, mime_type, size_bytes) "
        "VALUES ($1::uuid,$2::uuid,$3,$4,$5,'text/plain',3) RETURNING id::text",
        row["owner"],
        row["org"],
        f"RenameProbe/{tag}/original.txt",
        "original.txt",
        f"s3://probe/{tag}",
    )


@pytest.mark.parametrize("bad_name", REFUSED_NAMES)
async def test_a_name_that_is_not_one_segment_is_refused(bad_name: str) -> None:
    _skip_without_db()
    import asyncpg

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            file_id = await _seed(conn)
            # A savepoint: the refusal aborts its own subtransaction, so the
            # outer one stays usable for the "nothing was written" check below.
            sp = conn.transaction()
            await sp.start()
            with pytest.raises(asyncpg.PostgresError) as exc:
                await conn.fetchval(
                    "SELECT public.rename_file($1::uuid, $2)", file_id, bad_name
                )
            await sp.rollback()
            assert exc.value.sqlstate == "22023", (
                f"{bad_name!r} raised {exc.value.sqlstate} instead of invalid_parameter_value"
            )
            name, path = await conn.fetchrow(
                "SELECT file_name, file_path FROM files.files WHERE id = $1::uuid", file_id
            )
            assert name == "original.txt", f"the refused rename still wrote {name!r}"
            assert path.endswith("/original.txt")
        finally:
            await tx.rollback()


async def test_the_error_names_what_the_caller_actually_sent() -> None:
    """A message quoting the TRIMMED name tells the caller nothing about its bug."""
    _skip_without_db()
    import asyncpg

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            file_id = await _seed(conn)
            sp = conn.transaction()
            await sp.start()
            with pytest.raises(asyncpg.PostgresError) as exc:
                await conn.fetchval(
                    "SELECT public.rename_file($1::uuid, $2)", file_id, "trailing/"
                )
            await sp.rollback()
            assert "trailing/" in str(exc.value), (
                f"the error quotes a name the caller never sent: {exc.value}"
            )
        finally:
            await tx.rollback()


async def test_an_ordinary_rename_still_works_and_recomputes_the_path() -> None:
    _skip_without_db()
    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            file_id = await _seed(conn)
            receipt = await conn.fetchval(
                "SELECT public.rename_file($1::uuid, $2)", file_id, "renamed.txt"
            )
            assert "renamed.txt" in str(receipt)
            name, path = await conn.fetchrow(
                "SELECT file_name, file_path FROM files.files WHERE id = $1::uuid", file_id
            )
            assert name == "renamed.txt"
            assert path.endswith("/renamed.txt"), f"file_path was not recomputed: {path}"
        finally:
            await tx.rollback()


async def test_surrounding_whitespace_is_refused_not_silently_trimmed() -> None:
    """Amended by migration 037: edge whitespace is REFUSED, not trimmed.

    035 trimmed it. The re-verify's name-safety class made that wrong: Windows
    silently strips trailing spaces when it creates a file, so a name the server
    trimmed differently from the device is a name the two disagree about forever
    — and " report.txt" against "report.txt" is invisible on screen. Refusing is
    the only outcome the daemon can honor.
    """
    _skip_without_db()
    import asyncpg

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            file_id = await _seed(conn)
            sp = conn.transaction()
            await sp.start()
            with pytest.raises(asyncpg.PostgresError) as exc:
                await conn.fetchval(
                    "SELECT public.rename_file($1::uuid, $2)", file_id, "  spaced.txt  "
                )
            await sp.rollback()
            assert exc.value.sqlstate == "22023"
            assert "whitespace" in str(exc.value)
            name = await conn.fetchval(
                "SELECT file_name FROM files.files WHERE id = $1::uuid", file_id
            )
            assert name == "original.txt"
        finally:
            await tx.rollback()
