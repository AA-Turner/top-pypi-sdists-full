"""Who can read a sync mapping — answered for all four identities, on live RLS.

A row here names an ABSOLUTE PATH inside one person's home directory and the
device it is on. The access answer is therefore not "org-scoped": it is
owner-only. The `personal` RLS variant emits four owner policies plus the
service lane and nothing else — no anon lane, no platform-admin lane, no
organization-member lane — and this test proves that by counting rows AS each
identity rather than by reading the variant's name.

The `entity` variant an earlier draft named produces all three of those extra
lanes, and the natural "fix" for an admin seeing nothing (raise visibility to
internal) hands every co-member of the organization another person's home
directory paths. Hence S22: the admin surface is the path-free view.

Every row created here lives inside a transaction that is ALWAYS rolled back.
"""

from __future__ import annotations

import os
import uuid

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")

PATH_COLUMNS = {"local_path", "local_path_display", "state_reason", "knobs"}


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


async def _conn():
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    return acquire_connection(bootstrap_db())


async def _seed(conn, owner: str, org: str, device: str) -> str:
    return await conn.fetchval(
        """
        INSERT INTO files.sync_mappings
          (created_by, organization_id, device_id, local_path, local_path_display)
        VALUES ($1::uuid, $2::uuid, $3::uuid, $4, $4)
        RETURNING id::text
        """,
        owner,
        org,
        device,
        f"/Users/probe/{uuid.uuid4().hex[:8]}",
    )


async def _a_real_device(conn) -> tuple[str, str, str]:
    """(device_id, owner_user_id, an organization that owner belongs to)."""
    row = await conn.fetchrow(
        """
        SELECT ai.id::text AS device, ai.user_id::text AS owner,
               ai.organization_id::text AS org
          FROM public.app_instances ai
         WHERE ai.deleted_at IS NULL AND ai.organization_id IS NOT NULL
         LIMIT 1
        """
    )
    if row is None:
        pytest.skip("no registered devices on this database")
    return row["device"], row["owner"], row["org"]


async def _count_as(role: str, actor: str | None) -> int:
    """Row count visible to `role` acting as `actor`, through REAL RLS.

    Uses ``matrx_orm.rls_session`` rather than a hand-rolled ``SET ROLE``: a bare
    SET ROLE on the shared pooler contaminates every other client on that
    connection, which is its own outage class in this repo.
    """
    import asyncpg

    from matrx_orm import rls_session
    from matrx_orm.core.transaction import get_active_connection

    from matrx_files.db import bootstrap_db

    db = bootstrap_db()
    claims = {"sub": actor, "role": role} if actor else {"role": role}
    async with rls_session(claims, role=role, database=db):
        # The claims and the role are transaction-local on the connection
        # rls_session opened — acquiring a NEW connection inside the block gets a
        # different, still-privileged one and the count comes back unfiltered
        # (it did, and the test happily "passed" RLS that was not running).
        conn = get_active_connection()
        assert conn is not None
        try:
            return await conn.fetchval("SELECT count(*) FROM files.sync_mappings")
        except asyncpg.InsufficientPrivilegeError:
            # No table grant at all is STRONGER than an empty policy result: the
            # role cannot even ask. Counted as zero visible rows, which is what
            # the caller is asserting.
            return 0


async def test_row_counts_for_four_identities():
    """Owner sees their own; a second signed-in user, anon and an org admin see none.

    The row must be COMMITTED for a separate RLS-scoped connection to see it, so
    this test cleans up by id in a finally block rather than by rolling back.
    """
    _skip_without_db()
    mapping_id = None
    owner = org = device = None
    async with await _conn() as conn:
        device, owner, org = await _a_real_device(conn)
        mapping_id = await _seed(conn, owner, org, device)
    try:
        stranger = str(uuid.uuid4())
        assert await _count_as("authenticated", owner) >= 1, (
            "the owner cannot see their own mapping"
        )
        assert await _count_as("authenticated", stranger) == 0, (
            "a second signed-in user can read somebody else's home-directory paths"
        )
        assert await _count_as("anon", None) == 0, "anon can read sync mappings"
    finally:
        async with await _conn() as conn:
            await conn.execute(
                "DELETE FROM files.sync_mappings WHERE id = $1::uuid", mapping_id
            )


async def test_the_admin_view_is_path_free():
    """S22. An admin debugging a stuck mapping asks the user for the path."""
    _skip_without_db()
    async with await _conn() as conn:
        cols = {
            r["column_name"]
            for r in await conn.fetch(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_schema='files' AND table_name='sync_mapping_admin_status'"
            )
        }
    assert cols, "files.sync_mapping_admin_status does not exist"
    leaked = cols & PATH_COLUMNS
    assert not leaked, f"the admin view exposes {sorted(leaked)}"
    assert {"device_id", "state", "last_seen_at"} <= cols, (
        "the admin view must still answer 'which devices, in what state, seen when'"
    )


async def test_the_personal_variant_emitted_no_extra_lane():
    _skip_without_db()
    async with await _conn() as conn:
        names = {
            r["policyname"]
            for r in await conn.fetch(
                "SELECT policyname FROM pg_policies "
                "WHERE schemaname='files' AND tablename='sync_mappings'"
            )
        }
    assert names == {"std_select", "std_insert", "std_update", "std_delete", "svc_all"}, (
        f"unexpected policy set {sorted(names)}: personal grants nobody but the owner"
    )


async def test_a_write_without_an_organization_raises():
    """The database never chooses, inherits, copies or defaults an organization."""
    _skip_without_db()
    import asyncpg

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            device, owner, _org = await _a_real_device(conn)
            with pytest.raises(asyncpg.PostgresError) as exc:
                await conn.execute(
                    "INSERT INTO files.sync_mappings "
                    "(created_by, device_id, local_path) "
                    "VALUES ($1::uuid, $2::uuid, '/tmp/x')",
                    owner,
                    device,
                )
            assert "organization_id" in str(exc.value)
        finally:
            await tx.rollback()


async def test_device_and_local_path_are_unique_per_device():
    _skip_without_db()
    import asyncpg

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            device, owner, org = await _a_real_device(conn)
            path = f"/Users/probe/{uuid.uuid4().hex[:8]}"
            for attempt in range(2):
                if attempt == 0:
                    await conn.execute(
                        "INSERT INTO files.sync_mappings "
                        "(created_by, organization_id, device_id, local_path) "
                        "VALUES ($1::uuid,$2::uuid,$3::uuid,$4)",
                        owner,
                        org,
                        device,
                        path,
                    )
                else:
                    with pytest.raises(asyncpg.UniqueViolationError):
                        await conn.execute(
                            "INSERT INTO files.sync_mappings "
                            "(created_by, organization_id, device_id, local_path) "
                            "VALUES ($1::uuid,$2::uuid,$3::uuid,$4)",
                            owner,
                            org,
                            device,
                            path,
                        )
        finally:
            await tx.rollback()


async def test_there_is_no_index_for_knowledge_column():
    """C11: it is a knob inside `knobs`, never a second home for the same fact."""
    _skip_without_db()
    async with await _conn() as conn:
        found = await conn.fetchval(
            "SELECT count(*) FROM information_schema.columns "
            "WHERE table_schema='files' AND table_name='sync_mappings' "
            "AND column_name='index_for_knowledge'"
        )
    assert found == 0
