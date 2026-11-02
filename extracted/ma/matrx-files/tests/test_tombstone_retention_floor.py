"""The tombstone retention floor, proven against the live database (SPEC-SERVER §7, D23).

Migration 033 put a ``BEFORE DELETE`` row trigger on ``files.files``: a row whose
``deleted_at`` is younger than ``files.min_tombstone_retention_days()`` (90 days,
floor) may not be deleted, so an offline device converges on the tombstone instead
of resurrecting the delete. A deliberate delete-forever escapes it by setting
``matrx.purge_root_id`` — transaction-local — to the ROOT of the operation.

The escape covers the purge TREE and not one row, and that is the whole point:
``files.hard_delete_file`` recurses into ``parent_file_id`` children FIRST and
soft-stamps every row it is about to delete, so a delete-forever of a
never-trashed parent stamps ``now()`` on its children and a single-id escape
aborts on the first one. ``test_a_single_id_escape_aborts_on_the_first_child``
installs exactly that broken variant inside a rolled-back transaction and proves
it red; ``test_delete_forever_of_a_parent_with_two_children_succeeds_in_one_call``
proves the shipped tree escape green on the same shape.

Every row these tests create is created inside a transaction that is ALWAYS
rolled back — nothing is ever left in ``files.files``, and no pre-existing row is
modified. The owner and organization are read, never written.
"""

from __future__ import annotations

import os
import re
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[1]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")
_RESTRICT_VIOLATION = "23001"

# The single-id escape SPEC-SERVER §7 rejected: it permits only the escaped row
# itself, never its descendants. Installed inside a rolled-back transaction so a
# test can watch the real cascade abort on the first never-trashed child.
_SINGLE_ID_GUARD = """
CREATE OR REPLACE FUNCTION files.guard_tombstone_retention() RETURNS trigger
LANGUAGE plpgsql AS $guard$
DECLARE v_root uuid := nullif(current_setting('matrx.purge_root_id', true), '')::uuid;
BEGIN
  IF OLD.deleted_at IS NULL
     OR OLD.deleted_at <= now() - (files.min_tombstone_retention_days() || ' days')::interval
     OR v_root = OLD.id
  THEN
    RETURN OLD;
  END IF;
  RAISE EXCEPTION 'tombstone retention: file % is inside the window', OLD.id
    USING ERRCODE = 'restrict_violation';
END; $guard$;
"""


@pytest.mark.asyncio
async def test_central_retention_uses_the_package_owned_purge_transaction(monkeypatch) -> None:
    """Host lifecycle code receives a callback API, never the low-level GUC escape."""
    from matrx_files import retention

    events: list[object] = []

    async def fake_purge_escaped(root: object, operation):
        events.append(("package-open", root))
        result = await operation()
        events.append(("package-close", root))
        return result

    async def operation() -> str:
        events.append("operation")
        return "complete"

    monkeypatch.setattr(retention, "purge_escaped", fake_purge_escaped)
    result = await retention.run_retention_purge_transaction(
        "00000000-0000-0000-0000-000000000111", operation
    )

    assert result == "complete"
    assert events == [
        ("package-open", "00000000-0000-0000-0000-000000000111"),
        "operation",
        ("package-close", "00000000-0000-0000-0000-000000000111"),
    ]


def _skip_without_live_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable (unset: {', '.join(missing)})")


@asynccontextmanager
async def _rolled_back():
    """A connection inside a transaction that is ALWAYS rolled back.

    Nothing these tests insert survives the test, and the DDL one of them
    installs over ``files.guard_tombstone_retention`` is undone with it —
    function definitions are transactional in Postgres.
    """
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    async with acquire_connection(bootstrap_db()) as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            yield conn
        finally:
            await tx.rollback()


async def _owner_and_org(conn) -> tuple[uuid.UUID, uuid.UUID]:
    """Read (never write) an owner and the organization to stamp on test rows.

    Both come from a row that already exists, so the FKs to ``auth.users`` and
    ``iam.organizations`` are satisfied without inventing an identity — and the
    source row itself is only read.
    """
    row = await conn.fetchrow(
        "SELECT created_by, organization_id FROM files.files "
        "WHERE created_by IS NOT NULL AND organization_id IS NOT NULL LIMIT 1"
    )
    if row is None:
        pytest.skip("files.files has no owned row to borrow an owner/organization from")
    return row["created_by"], row["organization_id"]


async def _seed(
    conn,
    owner: uuid.UUID,
    org: uuid.UUID,
    *,
    deleted_days_ago: float | None = None,
    parent_file_id: uuid.UUID | None = None,
) -> uuid.UUID:
    # ``cld_files_lineage_consistency``: a row with a parent must name how it was
    # derived from it, so a child row carries the neutral 'variant' kind.
    tag = uuid.uuid4()
    deleted_at = None if deleted_days_ago is None else f"{deleted_days_ago} days"
    return await conn.fetchval(
        """
        INSERT INTO files.files
            (created_by, organization_id, file_path, file_name, storage_uri,
             parent_file_id, derivation_kind, deleted_at)
        VALUES
            ($1, $2, $3, $4, $5, $6,
             CASE WHEN $6::uuid IS NULL THEN NULL ELSE 'variant' END,
             CASE WHEN $7::text IS NULL THEN NULL ELSE now() - $7::interval END)
        RETURNING id
        """,
        owner,
        org,
        f"retention-floor-test/{tag}.bin",
        f"{tag}.bin",
        f"s3://retention-floor-test/{tag}",
        parent_file_id,
        deleted_at,
    )


async def _alive(conn, *ids: uuid.UUID) -> int:
    return await conn.fetchval(
        "SELECT count(*) FROM files.files WHERE id = ANY($1::uuid[])", list(ids)
    )


async def _escape(conn, root: uuid.UUID | str) -> None:
    await conn.execute("SELECT set_config('matrx.purge_root_id', $1, true)", str(root))


# ---------------------------------------------------------------------------
# The tree escape — red with a single id, green with the shipped walk
# ---------------------------------------------------------------------------


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_forever_of_a_parent_with_two_children_succeeds_in_one_call() -> None:
    """ONE ``hard_delete_file`` call, one escape, three rows gone.

    Neither child was ever trashed, so ``hard_delete_file`` stamps ``now()`` on
    both on its way past. The trigger permits them because it walks
    ``parent_file_id`` up to the escaped root.
    """
    _skip_without_live_db()
    async with _rolled_back() as conn:
        owner, org = await _owner_and_org(conn)
        parent = await _seed(conn, owner, org)
        kid_a = await _seed(conn, owner, org, parent_file_id=parent)
        kid_b = await _seed(conn, owner, org, parent_file_id=parent)
        assert await _alive(conn, parent, kid_a, kid_b) == 3

        await _escape(conn, parent)
        await conn.fetchval("SELECT files.hard_delete_file($1)", parent)

        assert await _alive(conn, parent, kid_a, kid_b) == 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_a_single_id_escape_aborts_on_the_first_child() -> None:
    """The RED proof: the escape SPEC-SERVER §7 rejected, on the shape above."""
    _skip_without_live_db()
    import asyncpg

    async with _rolled_back() as conn:
        owner, org = await _owner_and_org(conn)
        await conn.execute(_SINGLE_ID_GUARD)
        parent = await _seed(conn, owner, org)
        kid_a = await _seed(conn, owner, org, parent_file_id=parent)
        await _seed(conn, owner, org, parent_file_id=parent)

        await _escape(conn, parent)
        with pytest.raises(asyncpg.PostgresError) as caught:
            await conn.fetchval("SELECT files.hard_delete_file($1)", parent)
        assert caught.value.sqlstate == _RESTRICT_VIOLATION
        assert str(kid_a) in str(caught.value), (
            "the single-id escape must abort on the first never-trashed CHILD — "
            f"it raised on something else: {caught.value}"
        )


# ---------------------------------------------------------------------------
# The floor itself
# ---------------------------------------------------------------------------


@pytest.mark.integration
@pytest.mark.asyncio
async def test_a_fresh_tombstone_is_refused_even_while_another_root_is_escaped() -> None:
    """An escape is scoped to ONE tree; it is not an open season on the table."""
    _skip_without_live_db()
    import asyncpg

    async with _rolled_back() as conn:
        owner, org = await _owner_and_org(conn)
        unrelated = await _seed(conn, owner, org, deleted_days_ago=1)
        other_root = await _seed(conn, owner, org)

        await _escape(conn, other_root)
        with pytest.raises(asyncpg.PostgresError) as caught:
            await conn.execute("DELETE FROM files.files WHERE id = $1", unrelated)
        assert caught.value.sqlstate == _RESTRICT_VIOLATION
        assert "folder-sync contract D23" in str(caught.value)
        assert "90 days" in str(caught.value)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_a_tombstone_older_than_the_floor_needs_no_escape() -> None:
    """What a lawful purge job does: wait, then delete with no escape at all."""
    _skip_without_live_db()
    async with _rolled_back() as conn:
        owner, org = await _owner_and_org(conn)
        expired = await _seed(conn, owner, org, deleted_days_ago=91)

        await conn.execute("DELETE FROM files.files WHERE id = $1", expired)
        assert await _alive(conn, expired) == 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_a_row_that_was_never_trashed_deletes_freely() -> None:
    """The floor retains tombstones, not rows: no ``deleted_at``, no window."""
    _skip_without_live_db()
    async with _rolled_back() as conn:
        owner, org = await _owner_and_org(conn)
        never_trashed = await _seed(conn, owner, org)

        await conn.execute("DELETE FROM files.files WHERE id = $1", never_trashed)
        assert await _alive(conn, never_trashed) == 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_a_parent_chain_cycle_stops_at_64_hops_and_refuses() -> None:
    """A cycle must cost 64 hops and a refusal — never a spinning backend."""
    _skip_without_live_db()
    import asyncpg

    async with _rolled_back() as conn:
        owner, org = await _owner_and_org(conn)
        first = await _seed(conn, owner, org, deleted_days_ago=1)
        second = await _seed(conn, owner, org, deleted_days_ago=1, parent_file_id=first)
        await conn.execute(
            "UPDATE files.files SET parent_file_id = $1, derivation_kind = 'variant' "
            "WHERE id = $2",
            second,
            first,
        )

        await _escape(conn, uuid.uuid4())  # a root neither row belongs to
        with pytest.raises(asyncpg.PostgresError) as caught:
            await conn.execute("DELETE FROM files.files WHERE id = $1", first)
        assert caught.value.sqlstate == _RESTRICT_VIOLATION


# ---------------------------------------------------------------------------
# Who is allowed to set the escape
# ---------------------------------------------------------------------------

# ``purge_escape.py`` owns the GUC; ``sync_engine.py`` and the migration record
# name it in prose; this test names it to assert the rule. Anything else that
# sets it is a second delete-forever route the guard was written to prevent.
_GUC_ALLOWED = {
    "packages/matrx-files/matrx_files/cloud_sync/purge_escape.py",
    "packages/matrx-files/matrx_files/cloud_sync/sql/033_tombstone_retention_floor.sql",
    "packages/matrx-files/tests/test_tombstone_retention_floor.py",
}
_SETS_THE_GUC = re.compile(r"""set_config\s*\(\s*["']matrx\.purge_root_id["']""")
_SEARCH_ROOTS = ("aidream", "packages", "apps", "scripts", "db", "standalone")
_SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}


def test_no_call_site_outside_the_purge_escape_sets_the_guc() -> None:
    """Red the moment a second route starts escaping the retention floor."""
    offenders: list[str] = []
    for root in _SEARCH_ROOTS:
        base = REPO_ROOT / root
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_dir() or path.suffix not in {".py", ".sql", ".ts", ".tsx", ".mjs"}:
                continue
            if any(part in _SKIP_DIRS for part in path.parts):
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            if rel in _GUC_ALLOWED:
                continue
            if _SETS_THE_GUC.search(path.read_text(encoding="utf-8", errors="replace")):
                offenders.append(rel)
    assert not offenders, (
        "matrx.purge_root_id is set outside the one delete-forever escape "
        f"({offenders}). Route the delete through "
        "SyncEngine.hard_delete_and_purge[_async], which reaches the escape via "
        "DatabaseClient.hard_delete_file[_fallback]_async, instead of opening a "
        "second way past the D23 retention floor."
    )
