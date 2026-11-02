"""The rename/move contract, pinned against the live database (SPEC-SERVER §4.2, §10.1).

Every test here creates its OWN rows inside a transaction that is ALWAYS rolled
back, as ``admin@admin.com`` — never Arman's account and never a pre-existing
row. Nothing a test touches survives it.

What is pinned, and why each one is load-bearing:

* ``file_id`` never changes. A rename implemented as delete-and-recreate would
  orphan every version, share, RAG job and grant hanging off the id.
* ``file_path`` is always recomputed. It is ``NOT NULL``, is half of
  ``cld_files_owner_id_file_path_key``, and is what every replica holds on disk;
  writing ``file_name`` or ``parent_folder_id`` without it corrupts the row
  silently (22 live rows did exactly that — migration 031).
* ``23505 -> 409``, ``no_data_found -> 404``, ``42501 -> 403``, ``22023 -> 400``.
  A conflict that overwrites is data loss.
* A cross-org move is refused BEFORE the write, by name (S19).
* A flattening move REPORTS both paths (S20).
* ``FileService.mutate_file`` RAISES instead of returning 200 with ``errors[]``.
"""

from __future__ import annotations

import os
import uuid

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")

# The shared canonical admin test account (repo CLAUDE.md). Resolved by email at
# runtime rather than pinned as a uuid, so the test cannot silently start
# writing as somebody else if the account is ever re-created.
_ADMIN_EMAIL = "admin@admin.com"


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


class _Rollback(Exception):
    """Raised to unwind the test transaction. Never escapes ``_tx``."""


async def _tx(body):
    """Run ``body(conn)`` inside a transaction that is ALWAYS rolled back."""
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
    """``(admin user id, an organization that user may write files in)``.

    The organization comes from admin's own ACTIVE organization membership (owner/admin first) —
    the fact every write in this file needs. It used to be borrowed from a file admin already
    owned, which made the whole file red on any database where admin had not uploaded anything
    yet (the rehearsal branch holds no files at all), for a reason that has nothing to do with
    rename or move.
    """
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
    # Never skip on a missing admin: that is a broken environment, not an
    # unavailable one, and skipping would hide the contract going unchecked.
    assert row is not None, f"the canonical admin test account {_ADMIN_EMAIL} does not exist"
    assert row["org"] is not None, f"{_ADMIN_EMAIL} has no active organization membership"
    return str(row["uid"]), str(row["org"])


async def _make_folder(conn, owner: str, org: str, path: str) -> str:
    fid = str(uuid.uuid4())
    await conn.execute(
        """
        INSERT INTO files.folders (id, created_by, organization_id, folder_path, folder_name)
        VALUES ($1::uuid, $2::uuid, $3::uuid, $4, $5)
        """,
        fid, owner, org, path, path.rsplit("/", 1)[-1],
    )
    return fid


async def _make_file(
    conn, owner: str, org: str, path: str, *, name: str | None = None, parent: str | None = None
) -> str:
    fid = str(uuid.uuid4())
    await conn.execute(
        """
        INSERT INTO files.files
          (id, created_by, organization_id, file_path, file_name, parent_folder_id, storage_uri,
           created_at, updated_at)
        VALUES ($1::uuid, $2::uuid, $3::uuid, $4, $5, $6::uuid, $7,
                now() - interval '1 hour', now() - interval '1 hour')
        """,
        fid, owner, org, path, name or path.rsplit("/", 1)[-1], parent, f"s3://test/{fid}",
    )
    return fid


async def _expect_error(conn, sql: str, *args):
    """Run ``sql`` expecting it to RAISE, inside a SAVEPOINT.

    Without the savepoint the failed statement aborts the whole test
    transaction and every assertion after it dies with
    ``InFailedSQLTransactionError`` — so the test could never inspect the row
    the refusal was supposed to leave untouched.
    """
    import asyncpg

    try:
        async with conn.transaction():
            await conn.fetchval(sql, *args)
    except asyncpg.PostgresError as exc:
        return exc
    return None


async def _row(conn, file_id: str) -> dict:
    return dict(
        await conn.fetchrow(
            "SELECT id, file_name, file_path, parent_folder_id, organization_id, updated_at,"
            "       version, now() AS tx_now"
            "  FROM files.files WHERE id = $1::uuid",
            file_id,
        )
    )


def _prefix() -> str:
    return f".matrx-tmp/fs-c6b-{uuid.uuid4().hex[:12]}"


# ---------------------------------------------------------------------------
# rename_file
# ---------------------------------------------------------------------------


async def test_rename_recomputes_path_and_keeps_the_id() -> None:
    _skip_without_db()

    async def body(conn):
        owner, org = await _admin(conn)
        root = _prefix()
        file_id = await _make_file(conn, owner, org, f"{root}/dir/before.txt")
        before = await _row(conn, file_id)

        receipt = await conn.fetchval(
            "SELECT public.rename_file($1::uuid, $2)", file_id, "after.txt"
        )
        after = await _row(conn, file_id)
        return before, after, receipt, file_id, root

    before, after, receipt, file_id, root = await _tx(body)

    assert str(after["id"]) == file_id, "rename must never delete-and-recreate the row"
    assert after["file_name"] == "after.txt"
    assert after["file_path"] == f"{root}/dir/after.txt", "only the last segment moves"
    assert after["organization_id"] == before["organization_id"], "rename never changes the org"
    # `updated_at` is owned by the platform `_touch_row` BEFORE trigger, and
    # Postgres `now()` is TRANSACTION time — so inside one rolled-back
    # transaction the insert and the RPC stamp the identical value and a strict
    # `>` is structurally unprovable. The same trigger bumps `version` on every
    # UPDATE, so the version moving IS the proof that the row was written and
    # re-stamped, which is what makes the change ride the feed.
    assert after["version"] > before["version"], "the row must actually be re-written"
    assert after["updated_at"] == after["tx_now"], "the change must ride the feed"
    assert receipt["old_path"] == f"{root}/dir/before.txt"
    assert receipt["new_path"] == f"{root}/dir/after.txt"
    assert receipt["file_name"] == "after.txt"


async def test_rename_of_a_root_level_file_has_no_directory_to_keep() -> None:
    _skip_without_db()

    async def body(conn):
        owner, org = await _admin(conn)
        name = f"fs-c6b-{uuid.uuid4().hex[:12]}.txt"
        file_id = await _make_file(conn, owner, org, name)
        await conn.fetchval("SELECT public.rename_file($1::uuid, $2)", file_id, "renamed.txt")
        return await _row(conn, file_id)

    row = await _tx(body)
    assert row["file_path"] == "renamed.txt"
    assert row["file_name"] == "renamed.txt"


async def test_rename_conflict_raises_23505_so_the_caller_gets_409() -> None:
    _skip_without_db()

    async def body(conn):
        owner, org = await _admin(conn)
        root = _prefix()
        await _make_file(conn, owner, org, f"{root}/taken.txt")
        victim = await _make_file(conn, owner, org, f"{root}/victim.txt")
        exc = await _expect_error(
            conn, "SELECT public.rename_file($1::uuid, $2)", victim, "taken.txt"
        )
        return exc, await _row(conn, victim)

    exc, row = await _tx(body)
    assert exc is not None, "a name collision must RAISE, never silently overwrite"
    assert exc.sqlstate == "23505", f"expected a unique violation, got {exc.sqlstate}"
    assert row["file_name"] == "victim.txt", "the refused rename must leave the row untouched"
    assert row["file_path"].endswith("/victim.txt")


async def test_rename_of_a_missing_file_is_no_data_found_not_a_silent_noop() -> None:
    """`USING ERRCODE='no_data_found'` inside plpgsql is SQLSTATE **P0002**, the
    PL/pgSQL NO_DATA_FOUND condition — NOT the SQL-standard 02000 the spelling
    suggests. The wrapper maps both; this test is what caught it."""
    _skip_without_db()

    async def body(conn):
        return await _expect_error(
            conn, "SELECT public.rename_file($1::uuid, $2)", str(uuid.uuid4()), "x.txt"
        )

    exc = await _tx(body)
    assert exc is not None, "renaming a file that does not exist must RAISE, never no-op"
    assert exc.sqlstate in ("P0002", "02000"), exc.sqlstate


@pytest.mark.parametrize("bad_name", ["", "/", "///", "a/b", "a/b/c"])
async def test_rename_refuses_a_name_that_is_not_a_single_segment(bad_name: str) -> None:
    _skip_without_db()

    async def body(conn):
        owner, org = await _admin(conn)
        file_id = await _make_file(conn, owner, org, f"{_prefix()}/f.txt")
        return await _expect_error(
            conn, "SELECT public.rename_file($1::uuid, $2)", file_id, bad_name
        )

    exc = await _tx(body)
    assert exc is not None, f"{bad_name!r} must be refused, not accepted as a file name"
    assert exc.sqlstate == "22023", f"{bad_name!r} -> {exc.sqlstate}, expected 22023"


@pytest.mark.parametrize(
    ("given", "becomes"),
    [
        ("/leading.txt", None),   # a LEADING slash is REFUSED, not trimmed
        ("trailing/", None),      # a TRAILING slash is REFUSED, not trimmed
        ("   ", None),            # whitespace-only is REFUSED
        ("  spaced.txt  ", None),  # 037: edge whitespace is REFUSED, not trimmed
    ],
)
async def test_rename_name_normalisation_follows_the_amended_order(
    given: str, becomes: str | None
) -> None:
    """The §4.3 amendment, shipped as migration 035.

    This test previously DOCUMENTED the defect: the frozen §4.2 body trimmed
    slashes BEFORE the single-segment check, so ``'trailing/'`` silently renamed
    to ``trailing`` and a whitespace-only name was written as-is. The spec owner
    amended the order — segment check first, on the caller's own string, then
    NFC + whitespace normalization, then the empty check — so the expectations
    here are inverted to the contract that now ships. Full red-then-green
    coverage lives in ``test_rename_file_validation_order.py``.
    """
    _skip_without_db()

    async def body(conn):
        owner, org = await _admin(conn)
        file_id = await _make_file(conn, owner, org, f"{_prefix()}/f.txt")
        exc = await _expect_error(conn, "SELECT public.rename_file($1::uuid, $2)", file_id, given)
        return exc, await _row(conn, file_id)

    exc, row = await _tx(body)
    if becomes is None:
        assert exc is not None, f"{given!r} was accepted; it must be refused"
        assert exc.sqlstate == "22023"
        assert row["file_name"] == "f.txt", "a refused rename still wrote the row"
    else:
        assert exc is None, f"{given!r} was refused ({exc}), expected it to normalize"
        assert row["file_name"] == becomes


# ---------------------------------------------------------------------------
# move_file
# ---------------------------------------------------------------------------


async def test_move_recomputes_path_from_the_target_folder() -> None:
    _skip_without_db()

    async def body(conn):
        owner, org = await _admin(conn)
        root = _prefix()
        src = await _make_folder(conn, owner, org, f"{root}/src")
        dst = await _make_folder(conn, owner, org, f"{root}/dst/deeper")
        file_id = await _make_file(conn, owner, org, f"{root}/src/doc.txt", parent=src)
        before = await _row(conn, file_id)
        receipt = await conn.fetchval("SELECT public.move_file($1::uuid, $2::uuid)", file_id, dst)
        return before, await _row(conn, file_id), receipt, dst, root, file_id

    before, after, receipt, dst, root, file_id = await _tx(body)

    assert str(after["id"]) == file_id
    assert after["file_path"] == f"{root}/dst/deeper/doc.txt"
    assert str(after["parent_folder_id"]) == dst
    assert after["file_name"] == "doc.txt", "a move never renames"
    assert after["organization_id"] == before["organization_id"], "move never changes the org"
    # `updated_at` is owned by the platform `_touch_row` BEFORE trigger, and
    # Postgres `now()` is TRANSACTION time — so inside one rolled-back
    # transaction the insert and the RPC stamp the identical value and a strict
    # `>` is structurally unprovable. The same trigger bumps `version` on every
    # UPDATE, so the version moving IS the proof that the row was written and
    # re-stamped, which is what makes the change ride the feed.
    assert after["version"] > before["version"], "the row must actually be re-written"
    assert after["updated_at"] == after["tx_now"], "the change must ride the feed"
    assert receipt["old_path"] == f"{root}/src/doc.txt"
    assert receipt["new_path"] == f"{root}/dst/deeper/doc.txt"
    assert str(receipt["folder_id"]) == dst


async def test_move_to_null_parent_flattens_and_reports_both_paths() -> None:
    """S20: 1,666 alive rows carry a nested path with no parent. Moving one to
    the root is CORRECT — its true parent IS the root — but it renames the file
    on every replica, so both paths come back and nothing is silent."""
    _skip_without_db()

    async def body(conn):
        owner, org = await _admin(conn)
        name = f"fs-c6b-{uuid.uuid4().hex[:12]}.txt"
        file_id = await _make_file(conn, owner, org, f"a/b/{name}", name=name, parent=None)
        receipt = await conn.fetchval("SELECT public.move_file($1::uuid, NULL)", file_id)
        return receipt, await _row(conn, file_id), name

    receipt, row, name = await _tx(body)

    assert receipt["old_path"] == f"a/b/{name}"
    assert receipt["new_path"] == name
    assert receipt["old_path"] != receipt["new_path"], "the flattening must be visible"
    assert row["file_path"] == name
    assert row["parent_folder_id"] is None


async def test_move_refuses_every_cross_organization_move_by_name() -> None:
    """S19 — narrower than files_org_move_guard, deliberately, and the message
    says so, so the first person who hits it reads a decision, not a bug."""
    _skip_without_db()

    async def body(conn):
        owner, org = await _admin(conn)
        other_org = await conn.fetchval(
            "SELECT id FROM iam.organizations WHERE id <> $1::uuid LIMIT 1", org
        )
        if other_org is None:
            return "no-second-org", None, None
        root = _prefix()
        dst = await _make_folder(conn, owner, str(other_org), f"{root}/other-org")
        file_id = await _make_file(conn, owner, org, f"{root}/doc.txt")
        exc = await _expect_error(
            conn, "SELECT public.move_file($1::uuid, $2::uuid)", file_id, dst
        )
        return (exc.sqlstate if exc else None), (str(exc) if exc else ""), await _row(conn, file_id)

    sqlstate, message, row = await _tx(body)
    if sqlstate == "no-second-org":
        pytest.fail("the live database has only one organization; the S19 gate cannot be proven")

    assert sqlstate == "42501", "a cross-organization move must be refused"
    assert "cross-organization move refused" in message, (
        "the refusal must name the DECISION (S19), not read as a generic 'forbidden'"
    )
    assert row["parent_folder_id"] is None, "refused BEFORE the write — the row must be untouched"


async def test_move_into_a_missing_folder_is_no_data_found() -> None:
    _skip_without_db()

    async def body(conn):
        owner, org = await _admin(conn)
        file_id = await _make_file(conn, owner, org, f"{_prefix()}/doc.txt")
        exc = await _expect_error(
            conn, "SELECT public.move_file($1::uuid, $2::uuid)", file_id, str(uuid.uuid4())
        )
        return exc, await _row(conn, file_id)

    exc, row = await _tx(body)
    assert exc is not None and exc.sqlstate in ("P0002", "02000"), exc
    assert row["parent_folder_id"] is None, "the refused move must leave the row where it was"


async def test_move_conflict_raises_23505_so_the_caller_gets_409() -> None:
    _skip_without_db()

    async def body(conn):
        owner, org = await _admin(conn)
        root = _prefix()
        dst = await _make_folder(conn, owner, org, f"{root}/dst")
        await _make_file(conn, owner, org, f"{root}/dst/doc.txt", parent=dst)
        victim = await _make_file(conn, owner, org, f"{root}/src/doc.txt")
        exc = await _expect_error(
            conn, "SELECT public.move_file($1::uuid, $2::uuid)", victim, dst
        )
        return exc, await _row(conn, victim), root

    exc, row, root = await _tx(body)
    assert exc is not None, "a move onto an occupied path must RAISE, never overwrite"
    assert exc.sqlstate == "23505", exc.sqlstate
    assert row["file_path"] == f"{root}/src/doc.txt", "the refused move must not touch the path"
    assert row["parent_folder_id"] is None, "the refused move must leave the row where it was"


# ---------------------------------------------------------------------------
# The repoints — mutate_file RAISES, and every path writes through the RPCs
# ---------------------------------------------------------------------------


@pytest.mark.filterwarnings("ignore::pytest.PytestWarning")
def test_mutate_file_raises_instead_of_returning_200_with_errors() -> None:
    """Red against today's body: the rename/move stage used to do
    ``errors.append({"sub_op": "rename", ...})`` and return success.

    Read as source, not executed: the assertion is about the shape of the stage,
    and the executable half of the same contract is the live-DB tests above plus
    ``scripts/check_single_rename_path.py``.
    """
    from pathlib import Path

    from matrx_files import service as matrx_files_service

    source = Path(matrx_files_service.__file__).read_text()

    assert '{"sub_op": "rename"' not in source, (
        "a failed rename must RAISE (403/404/409/400), never be collected into errors[] "
        "behind a 200 — SPEC-SERVER §4.3"
    )
    assert '{"sub_op": "move"' not in source, (
        "a failed move must RAISE, never be collected into errors[] behind a 200"
    )
    assert "move_file_async" in source and "rename_file_async" in source, (
        "mutate_file must write through the two RPC wrappers"
    )


@pytest.mark.filterwarnings("ignore::pytest.PytestWarning")
def test_every_censused_write_path_goes_through_the_rpc_wrappers() -> None:
    """The executable form of 'exactly one rename path'.

    This is the pytest twin of ``aidream/scripts/check_single_rename_path.py``.
    It imports the guard and runs it over the real repository, so the package's
    test run fails the moment a fifth path appears — the guard already found
    three the spec's census of four had missed.
    """
    import importlib.util
    from pathlib import Path

    guard_path = (
        Path(__file__).resolve().parents[3] / "scripts" / "check_single_rename_path.py"
    )
    if not guard_path.exists():
        pytest.skip("aidream repository scripts unavailable in a standalone package install")

    spec = importlib.util.spec_from_file_location("_single_rename_path_guard", guard_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # The guard must be able to fail, or its silence means nothing.
    planted = module.scan_source(module._KNOWN_BAD, "synthetic/known_bad.py")
    assert planted, "the guard cannot detect the shapes it exists to catch"

    violations = module.collect_violations()
    assert not violations, "second rename path(s):\n" + "\n".join(str(v) for v in violations)
