"""`public.rename_folder` survives a subtree — the thing it exists to do.

Until migration 045 it did not. The descendant-folder UPDATE carried a
`RETURNING id INTO v_descendants_folders` where `id` is a UUID and the variable
is an INT, and PL/pgSQL is strict about arity for a data-modifying statement's
RETURNING. So the primitive raised on ANY subtree:

    0 descendant folders -> works by luck (nothing is returned, nothing assigned)
    1 descendant folder  -> 22P02 invalid input syntax for type integer: "<uuid>"
    2 or more            -> P0003 query returned more than one row

Every test and every census in the campaign until now renamed a FLAT folder,
which is exactly the one shape that never executes the broken line.

So this file renames a THREE-LEVEL tree with a file at every level and asserts
the receipt's own counts as well as the paths — an off-by-one in the subtree
walk cannot hide behind "it didn't raise". Everything runs inside a transaction
that is always rolled back.
"""

from __future__ import annotations

import os
import uuid as _uuid

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


async def _seed(conn):
    """admin@admin.com and an organization it belongs to — never anyone else.

    Resolved from the data on whatever database this run reaches (since
    2026-09-23 pytest is repointed off the live database by
    matrx_orm.pytest_live_db_guard), never a hardcoded uuid, never an arbitrary
    device owner. The organization is passed explicitly on every write.
    """
    row = await conn.fetchrow(
        "SELECT u.id::text AS owner, m.organization_id::text AS org "
        "FROM auth.users u JOIN iam.memberships m ON m.user_id = u.id "
        "WHERE u.email = 'admin@admin.com' AND m.deleted_at IS NULL "
        "AND m.organization_id IS NOT NULL ORDER BY m.created_at LIMIT 1"
    )
    if row is None:
        pytest.skip("admin@admin.com has no organization membership on this database")
    return row


async def _folder(conn, owner: str, org: str, path: str, parent: str | None) -> str:
    """Every org-scoped write names organization_id explicitly (no-db-assigned-org)."""
    return await conn.fetchval(
        "INSERT INTO files.folders (created_by, organization_id, folder_path, folder_name, parent_id) "
        "VALUES ($1::uuid, $2::uuid, $3, $4, $5::uuid) RETURNING id::text",
        owner, org, path, path.rsplit("/", 1)[-1], parent,
    )


async def _file(conn, owner: str, org: str, path: str, folder_id: str) -> str:
    return await conn.fetchval(
        "INSERT INTO files.files (created_by, organization_id, file_path, file_name, "
        "parent_folder_id, storage_uri, mime_type, size_bytes) "
        "VALUES ($1::uuid,$2::uuid,$3,$4,$5::uuid,$6,'text/plain',3) RETURNING id::text",
        owner, org, path, path.rsplit("/", 1)[-1], folder_id,
        f"s3://probe/{_uuid.uuid4().hex}",
    )


async def _build_tree(conn, owner: str, org: str, root: str) -> dict[str, str]:
    """root/ > mid/ > leaf/, one file in each. Three levels, two descendants."""
    top = await _folder(conn, owner, org, root, None)
    mid = await _folder(conn, owner, org, f"{root}/mid", top)
    leaf = await _folder(conn, owner, org, f"{root}/mid/leaf", mid)
    return {
        "top": top, "mid": mid, "leaf": leaf,
        "a": await _file(conn, owner, org, f"{root}/a.txt", top),
        "b": await _file(conn, owner, org, f"{root}/mid/b.txt", mid),
        "c": await _file(conn, owner, org, f"{root}/mid/leaf/c.txt", leaf),
    }


async def test_renaming_a_three_level_tree_re_prefixes_every_descendant() -> None:
    """THE regression. Before 045 this raised P0003 and renamed nothing."""
    _skip_without_db()
    import json

    root = f"RenameTreeProbe{_uuid.uuid4().hex[:8]}"
    new_root = f"{root}Renamed"

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            seed = await _seed(conn)
            ids = await _build_tree(conn, seed["owner"], seed["org"], root)

            receipt = await conn.fetchval(
                "SELECT public.rename_folder($1::uuid, $2)", ids["top"], new_root
            )
            receipt = json.loads(receipt) if isinstance(receipt, str) else receipt

            assert receipt["old_path"] == root
            assert receipt["new_path"] == new_root
            assert receipt["descendant_folders"] == 2, (
                f"the subtree walk found {receipt['descendant_folders']} folders, not 2: "
                "mid and leaf both had to move"
            )
            assert receipt["descendant_files"] == 3, (
                f"the subtree walk found {receipt['descendant_files']} files, not 3"
            )

            folders = {
                r["id"]: r["folder_path"]
                for r in await conn.fetch(
                    "SELECT id::text AS id, folder_path FROM files.folders "
                    "WHERE id = ANY($1::uuid[])",
                    [ids["top"], ids["mid"], ids["leaf"]],
                )
            }
            assert folders[ids["top"]] == new_root
            assert folders[ids["mid"]] == f"{new_root}/mid"
            assert folders[ids["leaf"]] == f"{new_root}/mid/leaf"

            files = {
                r["id"]: r["file_path"]
                for r in await conn.fetch(
                    "SELECT id::text AS id, file_path FROM files.files "
                    "WHERE id = ANY($1::uuid[])",
                    [ids["a"], ids["b"], ids["c"]],
                )
            }
            assert files[ids["a"]] == f"{new_root}/a.txt"
            assert files[ids["b"]] == f"{new_root}/mid/b.txt"
            assert files[ids["c"]] == f"{new_root}/mid/leaf/c.txt"

            orphans = await conn.fetchval(
                "SELECT count(*) FROM files.files WHERE file_path LIKE $1", f"{root}/%"
            )
            assert orphans == 0, "a descendant file was left pointing at the old path"
        finally:
            await tx.rollback()


@pytest.mark.parametrize("descendants", [1, 2], ids=["one-subfolder", "two-subfolders"])
async def test_the_exact_arities_that_used_to_raise(descendants: int) -> None:
    """One descendant raised 22P02, two raised P0003 — different errors, one bug.

    Parameterised so a future change that fixes only the multi-row half (or only
    the cast half) cannot go green.
    """
    _skip_without_db()
    import json

    root = f"RenameArityProbe{_uuid.uuid4().hex[:8]}"

    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            seed = await _seed(conn)
            top = await _folder(conn, seed["owner"], seed["org"], root, None)
            parent = top
            path = root
            for level in range(descendants):
                path = f"{path}/d{level}"
                parent = await _folder(conn, seed["owner"], seed["org"], path, parent)

            receipt = await conn.fetchval(
                "SELECT public.rename_folder($1::uuid, $2)", top, f"{root}X"
            )
            receipt = json.loads(receipt) if isinstance(receipt, str) else receipt
            assert receipt["descendant_folders"] == descendants
        finally:
            await tx.rollback()


async def test_a_flat_folder_still_renames() -> None:
    """Falsifiability: the shape every earlier test used must keep working."""
    _skip_without_db()
    import json

    root = f"RenameFlatProbe{_uuid.uuid4().hex[:8]}"
    async with await _conn() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            seed = await _seed(conn)
            top = await _folder(conn, seed["owner"], seed["org"], root, None)
            await _file(conn, seed["owner"], seed["org"], f"{root}/only.txt", top)
            receipt = await conn.fetchval(
                "SELECT public.rename_folder($1::uuid, $2)", top, f"{root}X"
            )
            receipt = json.loads(receipt) if isinstance(receipt, str) else receipt
            assert receipt["descendant_folders"] == 0
            assert receipt["descendant_files"] == 1
        finally:
            await tx.rollback()


async def test_the_primitive_no_longer_carries_the_returning_into() -> None:
    """The class, read off the live function: a uuid RETURNING into an int."""
    _skip_without_db()
    async with await _conn() as conn:
        src = await conn.fetchval(
            "SELECT prosrc FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace "
            "WHERE n.nspname='public' AND p.proname='rename_folder'"
        )
    assert "RETURNING id INTO v_descendants_folders" not in src, (
        "rename_folder is back to assigning a uuid RETURNING into an int counter — "
        "it raises on any subtree, which is the only shape it exists for."
    )
    assert src.count("GET DIAGNOSTICS") == 2, (
        "both subtree counts must come from GET DIAGNOSTICS, which is what they "
        f"always really came from: {src.count('GET DIAGNOSTICS')} found"
    )
