"""The admin surface is READ. An admin may not write another person's mappings.

SPEC-SERVER §6.2's access table says an organization admin **"May write: nothing"**.
S22 protected the *read* of ``local_path`` and left the WRITE lane wide open:
``files.sync_mapping_admin_status`` is a simple, therefore AUTO-UPDATABLE view,
owned by a BYPASSRLS role, and ``authenticated`` held INSERT/UPDATE/DELETE on it.
So any org owner/admin — and any platform admin — could UPDATE or DELETE rows of
``files.sync_mappings`` through the view, bypassing all four owner-only policies.
An admin could silently stop or re-home somebody else's folder sync.

The base table's own RLS is not the defense here and never was: the view's owner
bypasses it. The defense is that nobody but the view's owner holds a write
privilege ON THE VIEW.

These tests use a REAL org admin who is not the mapping's owner, and every row
they create is deleted in a ``finally``.
"""

from __future__ import annotations

import os
import uuid

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")

VIEW = "files.sync_mapping_admin_status"
WRITE_PRIVILEGES = ("INSERT", "UPDATE", "DELETE")
#: Every role that must NOT be able to write through an admin-read surface.
NON_OWNER_ROLES = ("authenticated", "anon", "service_role")


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


async def _conn():
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    return acquire_connection(bootstrap_db())


async def _seed_owned_by_someone_else() -> tuple[str, str, str]:
    """(mapping_id, owner_user_id, org_admin_user_id) — admin is NOT the owner."""
    async with await _conn() as conn:
        row = await conn.fetchrow(
            """
            SELECT ai.id::text AS device, ai.user_id::text AS owner,
                   ai.organization_id::text AS org, om.user_id::text AS admin
              FROM public.app_instances ai
              JOIN iam.organization_member om ON om.organization_id = ai.organization_id
             WHERE ai.deleted_at IS NULL AND ai.organization_id IS NOT NULL
               AND om.role IN ('admin','owner') AND om.user_id <> ai.user_id
             LIMIT 1
            """
        )
        if row is None:
            pytest.skip("no organization with an admin who is not a device owner")
        mapping_id = await conn.fetchval(
            "INSERT INTO files.sync_mappings "
            "(created_by, organization_id, device_id, local_path, desired_state) "
            "VALUES ($1::uuid,$2::uuid,$3::uuid,$4,'active') RETURNING id::text",
            row["owner"],
            row["org"],
            row["device"],
            f"/Users/probe/{uuid.uuid4().hex[:8]}",
        )
    return mapping_id, row["owner"], row["admin"]


async def _cleanup(mapping_id: str) -> None:
    async with await _conn() as conn:
        await conn.execute("DELETE FROM files.sync_mappings WHERE id = $1::uuid", mapping_id)


async def _as_admin(admin: str):
    from matrx_orm import rls_session
    from matrx_orm.core.transaction import get_active_connection

    from matrx_files.db import bootstrap_db

    return rls_session(
        {"sub": admin, "role": "authenticated"},
        role="authenticated",
        database=bootstrap_db(),
    ), get_active_connection


async def test_no_role_but_the_owner_holds_a_write_privilege_on_the_view():
    """The catalog check — the one that would have caught this on day one."""
    _skip_without_db()
    async with await _conn() as conn:
        rows = await conn.fetch(
            "SELECT r.rolname, p.priv, has_table_privilege(r.rolname, $1, p.priv) AS held "
            "FROM unnest($2::text[]) AS r(rolname), unnest($3::text[]) AS p(priv)",
            VIEW,
            list(NON_OWNER_ROLES),
            list(WRITE_PRIVILEGES),
        )
    held = [f"{r['rolname']}:{r['priv']}" for r in rows if r["held"]]
    assert not held, (
        f"{VIEW} is auto-updatable and these roles can write through it: {held}. "
        "The view's owner bypasses RLS, so a write privilege here is a write to "
        "files.sync_mappings that the four owner-only policies never see. "
        "SPEC-SERVER §6.2: an organization admin may write NOTHING."
    )


async def test_an_org_admin_can_still_read_the_path_free_status():
    """The fix must not silently kill the surface it is protecting."""
    _skip_without_db()
    mapping_id, _owner, admin = await _seed_owned_by_someone_else()
    try:
        session, get_conn = await _as_admin(admin)
        async with session:
            conn = get_conn()
            seen = await conn.fetchval(
                f"SELECT count(*) FROM {VIEW} WHERE id = $1::uuid", mapping_id
            )
        assert seen == 1, (
            "the org admin can no longer see the device status this view exists to "
            "show — the write fix broke the read."
        )
    finally:
        await _cleanup(mapping_id)


async def test_an_org_admin_update_through_the_view_is_refused():
    _skip_without_db()
    import asyncpg

    mapping_id, _owner, admin = await _seed_owned_by_someone_else()
    try:
        session, get_conn = await _as_admin(admin)
        with pytest.raises(asyncpg.InsufficientPrivilegeError):
            async with session:
                conn = get_conn()
                await conn.execute(
                    f"UPDATE {VIEW} SET desired_state='paused' WHERE id = $1::uuid",
                    mapping_id,
                )
        async with await _conn() as conn:
            still = await conn.fetchval(
                "SELECT desired_state FROM files.sync_mappings WHERE id = $1::uuid",
                mapping_id,
            )
        assert still == "active", "an admin paused another member's folder sync"
    finally:
        await _cleanup(mapping_id)


async def test_an_org_admin_delete_through_the_view_is_refused():
    _skip_without_db()
    import asyncpg

    mapping_id, _owner, admin = await _seed_owned_by_someone_else()
    try:
        session, get_conn = await _as_admin(admin)
        with pytest.raises(asyncpg.InsufficientPrivilegeError):
            async with session:
                conn = get_conn()
                await conn.execute(f"DELETE FROM {VIEW} WHERE id = $1::uuid", mapping_id)
        async with await _conn() as conn:
            alive = await conn.fetchval(
                "SELECT count(*) FROM files.sync_mappings WHERE id = $1::uuid", mapping_id
            )
        assert alive == 1, "an admin deleted another member's mapping outright"
    finally:
        await _cleanup(mapping_id)


async def test_the_class_no_writable_definer_view_over_files():
    """The CLASS, not the instance.

    Any ``security_invoker=false`` view over ``files.*`` runs as its BYPASSRLS
    owner, so every write privilege granted on one is an RLS bypass. This
    enumerates them all rather than pinning the one we happen to know about.
    """
    _skip_without_db()
    async with await _conn() as conn:
        rows = await conn.fetch(
            """
            SELECT n.nspname || '.' || c.relname AS view_name,
                   COALESCE(c.reloptions::text, '') AS opts,
                   has_table_privilege('authenticated', c.oid, 'UPDATE') AS a_upd,
                   has_table_privilege('authenticated', c.oid, 'DELETE') AS a_del,
                   has_table_privilege('authenticated', c.oid, 'INSERT') AS a_ins,
                   has_table_privilege('anon', c.oid, 'UPDATE') AS n_upd
              FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE c.relkind = 'v' AND n.nspname = 'files'
            """
        )
    offenders = [
        r["view_name"]
        for r in rows
        if "security_invoker=true" not in r["opts"]
        and (r["a_upd"] or r["a_del"] or r["a_ins"] or r["n_upd"])
    ]
    assert not offenders, (
        f"writable definer view(s) over files.*: {offenders}. A view owned by a "
        "BYPASSRLS role is a hole the base table's policies cannot close; grant "
        "SELECT only."
    )
