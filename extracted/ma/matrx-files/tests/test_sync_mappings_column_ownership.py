"""Two writers, split by what they OWN (C4) — enforced, not documented.

The race this removes, in one sentence: the user taps Pause
(``desired_state='paused'``), the daemon's next heartbeat writes
``state='syncing'``, and the pause SURVIVES — because they are different columns
owned by different writers. Before the split, the daemon's heartbeat silently
un-paused the mapping and the Pause control was a button that lied.

So the database refuses the wrong writer on the wrong column:

* the direct-to-Supabase lane (``auth.uid()`` non-null — the browser and the
  desktop UI) cannot write ``state``, ``state_reason``, ``state_changed_at`` or
  any counter;
* the service lane (the daemon, through ``PATCH /files/sync/mappings/{id}``)
  cannot write ``desired_state``.

Every row created here is deleted in a ``finally``.
"""

from __future__ import annotations

import os
import uuid

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")

DAEMON_COLUMNS = (
    "state",
    "state_reason",
    "state_changed_at",
    "last_seen_at",
    "last_synced_at",
    "items_total",
    "bytes_total",
)


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


async def _conn():
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    return acquire_connection(bootstrap_db())


async def _seed() -> tuple[str, str]:
    """(mapping_id, owner_user_id) — committed, so RLS sessions can see it."""
    async with await _conn() as conn:
        row = await conn.fetchrow(
            "SELECT id::text AS device, user_id::text AS owner, organization_id::text AS org "
            "FROM public.app_instances "
            "WHERE deleted_at IS NULL AND organization_id IS NOT NULL LIMIT 1"
        )
        if row is None:
            pytest.skip("no registered devices on this database")
        mapping_id = await conn.fetchval(
            "INSERT INTO files.sync_mappings "
            "(created_by, organization_id, device_id, local_path, desired_state, state) "
            "VALUES ($1::uuid,$2::uuid,$3::uuid,$4,'paused','syncing') "
            "RETURNING id::text",
            row["owner"],
            row["org"],
            row["device"],
            f"/Users/probe/{uuid.uuid4().hex[:8]}",
        )
    return mapping_id, row["owner"]


async def _cleanup(mapping_id: str) -> None:
    async with await _conn() as conn:
        await conn.execute("DELETE FROM files.sync_mappings WHERE id = $1::uuid", mapping_id)


@pytest.mark.parametrize("column", DAEMON_COLUMNS)
async def test_the_browser_lane_cannot_write_a_daemon_column(column: str) -> None:
    _skip_without_db()
    import asyncpg

    from matrx_orm import rls_session
    from matrx_orm.core.transaction import get_active_connection

    from matrx_files.db import bootstrap_db

    mapping_id, owner = await _seed()
    try:
        literal = (
            "1"
            if column in ("items_total", "bytes_total")
            else ("now()" if column.endswith("_at") else "'idle'")
        )
        async with rls_session(
            {"sub": owner, "role": "authenticated"},
            role="authenticated",
            database=bootstrap_db(),
        ):
            conn = get_active_connection()
            with pytest.raises(asyncpg.InsufficientPrivilegeError) as exc:
                await conn.execute(
                    f"UPDATE files.sync_mappings SET {column} = {literal} WHERE id = $1::uuid",
                    mapping_id,
                )
        assert column in str(exc.value)
        assert "PATCH /files/sync/mappings" in str(exc.value), (
            "the refusal must name the remedy, not just say no"
        )
    finally:
        await _cleanup(mapping_id)


async def test_the_browser_lane_can_still_write_its_own_intent() -> None:
    """desired_state, direction and knobs are the user's, and stay writable."""
    _skip_without_db()
    from matrx_orm import rls_session
    from matrx_orm.core.transaction import get_active_connection

    from matrx_files.db import bootstrap_db

    mapping_id, owner = await _seed()
    try:
        async with rls_session(
            {"sub": owner, "role": "authenticated"},
            role="authenticated",
            database=bootstrap_db(),
        ):
            conn = get_active_connection()
            await conn.execute(
                "UPDATE files.sync_mappings SET desired_state='active', direction='upload_only', "
                "knobs='{\"knowledge.index_for_knowledge\": true}'::jsonb WHERE id = $1::uuid",
                mapping_id,
            )
        async with await _conn() as conn:
            row = await conn.fetchrow(
                "SELECT desired_state, direction, knobs FROM files.sync_mappings "
                "WHERE id = $1::uuid",
                mapping_id,
            )
        assert row["desired_state"] == "active"
        assert row["direction"] == "upload_only"
    finally:
        await _cleanup(mapping_id)


async def test_the_service_lane_cannot_write_desired_state() -> None:
    """The daemon reports what IS; it never decides what the user WANTS."""
    _skip_without_db()
    import asyncpg

    mapping_id, _owner = await _seed()
    try:
        async with await _conn() as conn:
            with pytest.raises(asyncpg.InsufficientPrivilegeError) as exc:
                await conn.execute(
                    "UPDATE files.sync_mappings SET desired_state='active' WHERE id = $1::uuid",
                    mapping_id,
                )
        assert "converge state toward it" in str(exc.value)
    finally:
        await _cleanup(mapping_id)


async def test_a_pause_survives_a_daemon_heartbeat() -> None:
    """The whole point, end to end: intent and observation do not overwrite each other."""
    _skip_without_db()
    mapping_id, _owner = await _seed()  # seeded desired_state='paused'
    try:
        async with await _conn() as conn:
            # One ordinary heartbeat from the daemon lane.
            await conn.execute(
                "UPDATE files.sync_mappings SET state='syncing', last_seen_at=now(), "
                "items_total=42 WHERE id = $1::uuid",
                mapping_id,
            )
            row = await conn.fetchrow(
                "SELECT desired_state, state, items_total FROM files.sync_mappings "
                "WHERE id = $1::uuid",
                mapping_id,
            )
        assert row["desired_state"] == "paused", (
            "the daemon's heartbeat un-paused the mapping — the Pause control lies"
        )
        assert row["state"] == "syncing"
        assert row["items_total"] == 42
    finally:
        await _cleanup(mapping_id)


# ---------------------------------------------------------------------------
# Finding 4b: PLACEMENT IS FIXED AT CREATION (migration 039).
#
# §6.3 stated this invariant plainly — "INSERT is the one place the browser may
# write local_path, and the trigger above allows it only on INSERT" — and the
# trigger never mentioned local_path at all. Re-pointing a LIVE mapping skips
# D20's admission entirely: the daemon is left watching a directory nobody
# confirmed, or syncing one the user never chose. organization_id is the same
# argument one layer up (a tenancy change with no admission — where the files are
# billed and scoped), and device_id likewise: moving a mapping to another machine
# is not an edit, it is a different mapping.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("column", "literal"),
    [
        ("local_path", "'/Users/probe/somewhere-else'"),
        # A value that is genuinely DIFFERENT from the row's own, or the trigger
        # correctly sees no change and the test would prove nothing.
        (
            "device_id",
            "(SELECT ai.id FROM public.app_instances ai WHERE ai.deleted_at IS NULL "
            "AND ai.id <> files.sync_mappings.device_id LIMIT 1)",
        ),
        (
            "organization_id",
            "(SELECT o.id FROM iam.organizations o "
            "WHERE o.id <> files.sync_mappings.organization_id LIMIT 1)",
        ),
    ],
)
async def test_placement_cannot_be_changed_by_the_browser_lane(column, literal) -> None:
    _skip_without_db()
    import asyncpg

    from matrx_orm import rls_session
    from matrx_orm.core.transaction import get_active_connection

    from matrx_files.db import bootstrap_db

    mapping_id, owner = await _seed()
    try:
        async with rls_session(
            {"sub": owner, "role": "authenticated"},
            role="authenticated",
            database=bootstrap_db(),
        ):
            conn = get_active_connection()
            with pytest.raises(asyncpg.InsufficientPrivilegeError) as exc:
                await conn.execute(
                    f"UPDATE files.sync_mappings SET {column} = {literal} WHERE id = $1::uuid",
                    mapping_id,
                )
        assert "fixed when the mapping is created" in str(exc.value)
        assert "desired_state" in str(exc.value), "the refusal must name the way out"
    finally:
        await _cleanup(mapping_id)


@pytest.mark.parametrize("column", ["local_path", "organization_id"])
async def test_placement_cannot_be_changed_by_the_service_lane_either(column) -> None:
    """Not a permissions split — nobody re-points a live mapping."""
    _skip_without_db()
    import asyncpg

    mapping_id, _owner = await _seed()
    try:
        literal = (
            "'/Users/probe/elsewhere'"
            if column == "local_path"
            else "(SELECT o.id FROM iam.organizations o "
                 "WHERE o.id <> files.sync_mappings.organization_id LIMIT 1)"
        )
        async with await _conn() as conn:
            with pytest.raises(asyncpg.InsufficientPrivilegeError):
                await conn.execute(
                    f"UPDATE files.sync_mappings SET {column} = {literal} WHERE id = $1::uuid",
                    mapping_id,
                )
    finally:
        await _cleanup(mapping_id)


async def test_the_user_can_still_remove_and_recreate_which_is_the_way_out() -> None:
    """The refusal names a remedy, and the remedy works."""
    _skip_without_db()
    from matrx_orm import rls_session
    from matrx_orm.core.transaction import get_active_connection

    from matrx_files.db import bootstrap_db

    mapping_id, owner = await _seed()
    try:
        async with rls_session(
            {"sub": owner, "role": "authenticated"},
            role="authenticated",
            database=bootstrap_db(),
        ):
            conn = get_active_connection()
            await conn.execute(
                "UPDATE files.sync_mappings SET desired_state='removed' WHERE id = $1::uuid",
                mapping_id,
            )
        async with await _conn() as conn:
            assert await conn.fetchval(
                "SELECT desired_state FROM files.sync_mappings WHERE id = $1::uuid", mapping_id
            ) == "removed"
    finally:
        await _cleanup(mapping_id)
