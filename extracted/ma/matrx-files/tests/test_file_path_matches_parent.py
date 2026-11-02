"""``files.file_path_matches_parent`` — the guard for the SECOND drift shape.

``file_path`` disagreeing with its own ``parent_folder_id``'s ``folder_path`` is
what the bulk move produced (SPEC-SERVER §4.3 path 2), and the ``file_name``-vs-
basename census of §4.4 cannot see it: the name matches the path perfectly while
the path points at a folder the row no longer belongs to. There were 0 such rows
at migration time, so the shape gets a GUARD, not a repair.

A guard nobody has seen fail is not a guard, so the first test plants one drifted
row inside a transaction that is always rolled back and proves the function RED,
then green on a correct row in the same transaction.
"""

from __future__ import annotations

import os
import uuid

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")
_ADMIN_EMAIL = "admin@admin.com"


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


class _Rollback(Exception):
    pass


async def _tx(body):
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    captured: dict = {}
    async with acquire_connection(bootstrap_db()) as conn:
        try:
            async with conn.transaction():
                captured["result"] = await body(conn)
                raise _Rollback
        except _Rollback:
            pass
    return captured.get("result")


async def _admin(conn) -> tuple[str, str]:
    row = await conn.fetchrow(
        """
        SELECT u.id AS uid,
               (SELECT m.organization_id FROM iam.memberships m
                 WHERE m.user_id = u.id AND m.container_type = 'organization'
                   AND m.status = 'active' AND m.deleted_at IS NULL
                 ORDER BY (m.role IN ('owner', 'admin')) DESC, m.created_at
                 LIMIT 1) AS org
          FROM auth.users u WHERE u.email = $1
        """,
        _ADMIN_EMAIL,
    )
    # admin's own active membership — not "an organization admin already has a file in", which
    # made this file red on any database where admin had uploaded nothing (the rehearsal branch).
    assert row is not None, f"the canonical admin test account {_ADMIN_EMAIL} does not exist"
    assert row["org"] is not None, f"{_ADMIN_EMAIL} has no active organization membership"
    return str(row["uid"]), str(row["org"])


async def test_guard_is_red_for_a_drifted_row_and_green_for_a_correct_one() -> None:
    _skip_without_db()

    async def body(conn):
        owner, org = await _admin(conn)
        root = f".matrx-tmp/fs-c6b-{uuid.uuid4().hex[:12]}"
        folder = str(uuid.uuid4())
        await conn.execute(
            "INSERT INTO files.folders (id, created_by, organization_id, folder_path, folder_name)"
            " VALUES ($1::uuid, $2::uuid, $3::uuid, $4, 'here')",
            folder, owner, org, f"{root}/here",
        )

        # THE DRIFTED ROW: parent says {root}/here, file_path says {root}/elsewhere.
        drifted = str(uuid.uuid4())
        await conn.execute(
            "INSERT INTO files.files (id, created_by, organization_id, file_path, file_name,"
            " parent_folder_id, storage_uri)"
            " VALUES ($1::uuid, $2::uuid, $3::uuid, $4, 'doc.txt', $5::uuid, $6)",
            drifted, owner, org, f"{root}/elsewhere/doc.txt", folder, f"s3://test/{drifted}",
        )

        # THE CORRECT ROW: same folder, path agrees.
        correct = str(uuid.uuid4())
        await conn.execute(
            "INSERT INTO files.files (id, created_by, organization_id, file_path, file_name,"
            " parent_folder_id, storage_uri)"
            " VALUES ($1::uuid, $2::uuid, $3::uuid, $4, 'ok.txt', $5::uuid, $6)",
            correct, owner, org, f"{root}/here/ok.txt", folder, f"s3://test/{correct}",
        )

        return (
            await conn.fetchval("SELECT files.file_path_matches_parent($1::uuid)", drifted),
            await conn.fetchval("SELECT files.file_path_matches_parent($1::uuid)", correct),
        )

    drifted_result, correct_result = await _tx(body)
    assert drifted_result is False, "the guard did not see a row whose path contradicts its parent"
    assert correct_result is True, "the guard must not fire on a row that agrees with its parent"


async def test_a_parent_that_does_not_exist_cannot_be_created_at_all() -> None:
    """The guard returns false for a dangling parent, but the database refuses to
    produce one: ``cld_files_parent_folder_id_fkey`` rejects the insert.

    That is the STRONGER guarantee, so the test pins the structural refusal
    rather than pretending to exercise an unreachable branch. The guard's
    dangling-parent branch stays as defense in depth for a future in which the
    FK is ever relaxed.
    """
    _skip_without_db()
    import asyncpg

    async def body(conn):
        owner, org = await _admin(conn)
        file_id = str(uuid.uuid4())
        try:
            async with conn.transaction():
                await conn.execute(
                    "INSERT INTO files.files (id, created_by, organization_id, file_path,"
                    " file_name, parent_folder_id, storage_uri)"
                    " VALUES ($1::uuid, $2::uuid, $3::uuid, $4, 'x.txt', $5::uuid, $6)",
                    file_id, owner, org, "a/x.txt", str(uuid.uuid4()), f"s3://test/{file_id}",
                )
        except asyncpg.exceptions.ForeignKeyViolationError as exc:
            return exc.constraint_name
        return None

    assert await _tx(body) == "cld_files_parent_folder_id_fkey"


async def test_a_file_with_no_parent_makes_no_claim() -> None:
    """The 1,666 alive parentless-nested rows are S20's shape, not this guard's.
    Folding them in would make the guard permanently red and therefore useless."""
    _skip_without_db()

    async def body(conn):
        owner, org = await _admin(conn)
        file_id = str(uuid.uuid4())
        await conn.execute(
            "INSERT INTO files.files (id, created_by, organization_id, file_path, file_name,"
            " parent_folder_id, storage_uri)"
            " VALUES ($1::uuid, $2::uuid, $3::uuid, $4, 'deep.txt', NULL, $5)",
            file_id, owner, org, f"a/b/c/{uuid.uuid4().hex[:8]}-deep.txt", f"s3://test/{file_id}",
        )
        return await conn.fetchval("SELECT files.file_path_matches_parent($1::uuid)", file_id)

    assert await _tx(body) is True


async def test_a_missing_file_raises_rather_than_returning_null() -> None:
    """A silent NULL vanishes from every ``WHERE NOT ...`` census this guard feeds.

    ``USING ERRCODE='no_data_found'`` in plpgsql is SQLSTATE **P0002** (the
    PL/pgSQL NO_DATA_FOUND condition), not the SQL-standard 02000.
    """
    _skip_without_db()
    import asyncpg

    async def body(conn):
        try:
            async with conn.transaction():
                await conn.fetchval(
                    "SELECT files.file_path_matches_parent($1::uuid)", str(uuid.uuid4())
                )
        except asyncpg.PostgresError as exc:
            return exc.sqlstate
        return None

    assert await _tx(body) in ("P0002", "02000")


async def test_the_live_table_is_green() -> None:
    """0 rows today — and the whole-table sweep is the standing check's query."""
    _skip_without_db()

    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    async with acquire_connection(bootstrap_db()) as conn:
        drifted = await conn.fetchval(
            "SELECT count(*) FROM files.files"
            " WHERE deleted_at IS NULL AND NOT files.file_path_matches_parent(id)"
        )
    assert drifted == 0, f"{drifted} alive row(s) have a file_path their parent contradicts"
