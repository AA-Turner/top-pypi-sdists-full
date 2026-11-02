"""THE user-visibility predicate, case by case, against live data (§10.1).

``test_user_visible_declaration_parity.py`` proves the SQL function and the ORM
filter set agree with each other. That is necessary and not sufficient: two
shapes of the same rule can agree and both be WRONG. This file pins what the
rule must actually decide, and the D16 equivalence the whole design rests on.

SELECT only. Nothing here writes a row.
"""

from __future__ import annotations

import os

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


@pytest.mark.parametrize(
    ("path", "visible", "why"),
    [
        ("My Files/report.txt", True, "an ordinary user file"),
        ("My Files/nested/deep/report.txt", True, "depth is not a visibility signal"),
        ("Docs", True, "a bare top-level name"),
        ("system-files/x.png", False, "app-managed: derived or fetched content"),
        ("system-files", False, "the root itself, not just what is under it"),
        ("generations/img.png", False, "app-managed: the system produced these bytes"),
        ("generations", False, "the root itself"),
        (".matrx-tmp/upload.part", False, "ephemeral staging the user never sees"),
        (".matrx-tmp", False, "the root itself"),
        ("my-system-files/x", True, "a PREFIX match is not a SEGMENT match"),
        ("generationsX/x", True, "a prefix match is not a segment match"),
        ("a/system-files/b", True, "only the FIRST segment is app-managed"),
        ("/system-files/x", False, "a leading slash does not smuggle it through"),
        ("coding-sessions/claude_code/s1/log.md", False, "machine namespace: the coding-session recorder"),
        ("tool-images/1/v/shot.png", False, "machine namespace: AI tool screenshots"),
        ("/coding-sessions/x", False, "a leading slash does not smuggle a machine namespace through"),
        ("My Files/coding-sessions/x", True, "only the FIRST segment is a machine namespace"),
    ],
)
async def test_the_path_half_decides_each_case(path: str, visible: bool, why: str) -> None:
    _skip_without_db()
    async with await _conn() as conn:
        got = await conn.fetchval("SELECT files.is_user_visible_path($1)", path)
    assert got is visible, f"{path!r} -> {got}, expected {visible} ({why})"


async def test_a_null_path_is_not_visible() -> None:
    """NULL is never a user's file. file_path is NOT NULL, so this is belt and braces."""
    _skip_without_db()
    async with await _conn() as conn:
        assert await conn.fetchval("SELECT files.is_user_visible_path(NULL)") is not True


async def test_parentless_variants_are_excluded_by_the_row_half() -> None:
    """The 824-row case the row half exists for.

    ``derivation_kind='variant'`` with ``parent_file_id IS NULL`` is why BOTH
    columns are tested: neither alone excludes derivatives, and a thumbnail
    syncing to somebody's Desktop as a file is the visible failure.
    """
    _skip_without_db()
    async with await _conn() as conn:
        rows = await conn.fetch(
            "SELECT id, files.is_user_visible(f.*) AS visible "
            "FROM files.files f "
            "WHERE f.deleted_at IS NULL AND f.parent_file_id IS NULL "
            "  AND f.derivation_kind IS NOT NULL LIMIT 200"
        )
    assert rows, "no parentless derivative on this database — the test proves nothing"
    leaked = [str(r["id"]) for r in rows if r["visible"]]
    assert not leaked, (
        f"{len(leaked)} parentless derivative(s) passed the row half (e.g. {leaked[:3]}) "
        "— the derivation_kind conjunct is not doing its job and thumbnails will sync "
        "to somebody's Desktop as files."
    )


async def test_the_predicate_is_immutable_so_it_can_carry_an_index() -> None:
    """If this stops being IMMUTABLE, both partial indexes silently die.

    The whole design — one expression, matchable against a partial index — rests
    on it, which is also why it may never read a table.
    """
    _skip_without_db()
    async with await _conn() as conn:
        volatility = await conn.fetchval(
            "SELECT provolatile::text FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace "
            "WHERE n.nspname='files' AND p.proname='is_user_visible_path'"
        )
    assert volatility == "i", (
        f"files.is_user_visible_path is provolatile={volatility!r}, not IMMUTABLE; "
        "it can no longer appear in an index predicate."
    )


async def test_is_system_equals_the_path_predicate_over_every_live_folder() -> None:
    """D16's equivalence — the reason a PATH predicate may stand in for the tree.

    ``folders_set_is_system()`` derives ``is_system`` from ``folder_path`` by
    trigger. If a future migration ever lets the two disagree, the predicate has
    to become a table-reading STABLE function and both partial indexes are lost.
    """
    _skip_without_db()
    async with await _conn() as conn:
        drifted = await conn.fetchval(
            "SELECT count(*) FROM files.folders d WHERE d.deleted_at IS NULL "
            "AND d.is_system IS DISTINCT FROM files.is_system_path(d.folder_path)"
        )
    assert drifted == 0, (
        f"{drifted} folder(s) have is_system disagreeing with "
        "is_system_path(folder_path); SPEC-SERVER §1.1's equivalence no longer holds."
    )
