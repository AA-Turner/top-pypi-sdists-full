"""THE user-visibility rule has exactly one declaration — proven, not promised.

Folder sync's core promise (D16) is that the browser tree and a device's disk
replica can never disagree about which files a user has. That holds only while
three artifacts stay identical: the declaration in ``matrx_files.user_visible``,
the live SQL functions, and the matrx-orm filter set the change feed applies.

The design deliberately accepts two SHAPES of the one rule (a SQL function and
an ORM ``Q`` set) in exchange for index-matchable plans, so the drift between
them is TESTED every commit rather than argued. These tests are the guard:
edit either side alone and they go red.

Marked ``integration``: they read the live platform database (SELECT only —
nothing here writes a row).
"""

from __future__ import annotations

import os

import pytest

from matrx_files.user_visible import (
    PATH_PREDICATE_FUNCTION,
    RECENT_PATH_FUNCTION,
    RECENT_ROW_FUNCTION,
    ROW_PREDICATE_FUNCTION,
    path_visible_filters,
    row_visible_filters,
    sql_is_recent_activity_path_body,
    sql_is_recent_activity_row_body,
    sql_is_user_visible_path_body,
    sql_is_user_visible_row_body,
    user_visible_filters,
)

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")

# The heaviest live owner (81,863 rows, ~10.8% user-visible) — the corpus that
# actually exercises every conjunct: parentless variants, system paths,
# .matrx-tmp rows and tombstones all exist under it.
_CORPUS_OWNER = "00000000-0000-4000-8000-0000000fffe1"


def _skip_without_db() -> None:
    missing = [name for name in _REQUIRED_ENV if not os.environ.get(name)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


async def _fetch(sql: str, *args) -> list[dict]:
    """SELECT-only catalogue/parity read.

    matrx-orm deliberately exposes no raw-SQL query API — all production access
    is Models or Managers. These assertions read ``pg_proc`` and compare two
    renderings of one predicate, neither of which has (or should have) a model,
    so the test takes a pooled connection directly. Nothing here writes.
    """
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    async with acquire_connection(bootstrap_db()) as conn:
        return [dict(r) for r in await conn.fetch(sql, *args)]


async def test_live_function_bodies_equal_the_generated_text():
    """The live ``pg_proc.prosrc`` is byte-identical to what the declaration emits.

    Red the moment somebody edits the function in the database (or in a later
    migration) without changing the declaration the ORM half is generated from.
    """
    _skip_without_db()
    rows = await _fetch(
        """
        SELECT p.oid::regprocedure::text AS signature, p.prosrc AS body
          FROM pg_proc p
          JOIN pg_namespace n ON n.oid = p.pronamespace
         WHERE n.nspname = 'files'
           AND p.proname IN ('is_user_visible_path', 'is_user_visible', 'is_recent_activity_path', 'is_recent_activity')
        """
    )
    bodies = {r["signature"]: r["body"] for r in rows}
    assert f"{PATH_PREDICATE_FUNCTION}(text)" in bodies, (
        f"{PATH_PREDICATE_FUNCTION}(text) is missing from the live database; "
        "migration 025_user_visible_predicate.sql has not been applied."
    )
    assert f"{ROW_PREDICATE_FUNCTION}(files.files)" in bodies, (
        f"{ROW_PREDICATE_FUNCTION}(files.files) is missing from the live database."
    )
    assert bodies[f"{PATH_PREDICATE_FUNCTION}(text)"] == sql_is_user_visible_path_body()
    assert bodies[f"{ROW_PREDICATE_FUNCTION}(files.files)"] == sql_is_user_visible_row_body()
    assert bodies[f"{RECENT_PATH_FUNCTION}(text)"] == sql_is_recent_activity_path_body()
    # The Recents ROW rule (050: a system_artifact file is never Recents) was unpinned until 2026-09-29.
    assert bodies[f"{RECENT_ROW_FUNCTION}(files.files)"] == sql_is_recent_activity_row_body()


async def test_the_orm_filter_set_and_the_sql_function_select_the_same_rows():
    """Both shapes of the rule, over the same live corpus, return one id set."""
    _skip_without_db()
    from matrx_files.db import bootstrap_db, models_files

    bootstrap_db()

    sql_rows = await _fetch(
        """
        SELECT f.id::text AS id
          FROM files.files f
         WHERE f.created_by = $1::uuid
           AND files.is_user_visible(f.*)
        """,
        _CORPUS_OWNER,
    )
    sql_ids = {r["id"] for r in sql_rows}

    orm_rows = await (
        models_files.Files.filter(created_by=_CORPUS_OWNER)
        .filter(**user_visible_filters())
        .values("id")
    )
    orm_ids = {str(r["id"]) for r in orm_rows}

    assert sql_ids, "the corpus owner has no user-visible rows — the test proves nothing"
    only_sql = sql_ids - orm_ids
    only_orm = orm_ids - sql_ids
    assert not only_sql and not only_orm, (
        "THE RULE HAS DRIFTED between its SQL and ORM shapes. "
        f"{len(only_sql)} row(s) only the SQL function accepts "
        f"(e.g. {sorted(only_sql)[:3]}), {len(only_orm)} row(s) only the ORM filter set "
        f"accepts (e.g. {sorted(only_orm)[:3]})."
    )


async def test_the_orm_lookup_emits_the_index_matchable_expression():
    """The path half is ONE expression — the same call both partial indexes carry.

    Spelled as ``NOT LIKE`` conjuncts the planner cannot match the index
    (measured live 2026-09-13: 11,177 with a Sort against 13.83 for an Index
    Only Scan), so the emitted SQL text is pinned here.
    """
    _skip_without_db()
    from matrx_files.db import bootstrap_db, models_files

    bootstrap_db()
    query = (
        models_files.Files.filter(created_by=_CORPUS_OWNER)
        .filter(**row_visible_filters())
        .filter(**path_visible_filters())
        ._build_query()
    )
    from matrx_orm.query.executor import QueryExecutor

    sql = QueryExecutor(query).query
    assert f"{PATH_PREDICATE_FUNCTION}(" in sql, sql
    assert "LIKE" not in sql.upper(), (
        "the path half was expanded into LIKE conjuncts; the partial index is lost"
    )


async def test_is_system_equals_the_path_predicate_over_the_folder_tree():
    """D16's equivalence, checked against live data rather than asserted.

    ``folders_set_is_system()`` derives ``is_system`` from ``folder_path`` by
    trigger, which is the ONLY reason a path predicate may stand in for "not
    under a protected system folder" while staying IMMUTABLE and index-usable.
    If a future migration ever lets the two disagree, this goes red and the
    predicate has to become a table-reading STABLE function.
    """
    _skip_without_db()
    rows = await _fetch(
        """
        SELECT count(*) AS drifted
          FROM files.folders d
         WHERE d.deleted_at IS NULL
           AND d.is_system IS DISTINCT FROM files.is_system_path(d.folder_path)
        """
    )
    assert rows[0]["drifted"] == 0, (
        f"{rows[0]['drifted']} folder row(s) have is_system disagreeing with "
        "is_system_path(folder_path). SPEC-SERVER §1.1's equivalence — the whole "
        "basis for an IMMUTABLE, index-usable visibility predicate — no longer holds."
    )
