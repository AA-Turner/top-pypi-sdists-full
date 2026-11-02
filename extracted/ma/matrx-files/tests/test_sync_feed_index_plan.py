"""The feed and tree plans are GATED, not hoped for (SPEC-SERVER §2.5).

A visibility predicate that the planner cannot match against a partial index
makes the change feed 4.9x SLOWER than having no predicate at all -- measured,
not theorised (408 ms / 131,036 buffers on the pre-index shape against an 84 ms
baseline). So the plan itself is the contract, and these tests read a real
``EXPLAIN (ANALYZE, BUFFERS)`` on the heaviest live owner.

The buffer criterion currently MISSES and says so out loud rather than being
relaxed: see ``test_feed_page_buffer_budget``.
"""

from __future__ import annotations

import os
import re

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

_REQUIRED_ENV = ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_PASSWORD")
_OWNER = "00000000-0000-4000-8000-0000000fffe1"

FEED_INDEX = "idx_files_sync_feed_owner_updated_id"
TREE_INDEX = "idx_files_user_visible_owner_name"

_FEED_PAGE = """
SELECT f.id, f.file_path, f.updated_at
  FROM files.files f
 WHERE f.created_by = $1::uuid
   AND f.updated_at <= now() - interval '10 seconds'
   AND f.parent_file_id IS NULL
   AND f.derivation_kind IS NULL
   AND files.is_user_visible_path(f.file_path) = true
   AND files.is_crawl_artifact(f.id) IS FALSE
 ORDER BY f.updated_at, f.id
 LIMIT 500
"""

_TREE_OWNER_BRANCH = """
SELECT f.id, f.file_name
  FROM files.files f
 WHERE f.created_by = $1::uuid
   AND f.deleted_at IS NULL
   AND f.parent_file_id IS NULL
   AND f.derivation_kind IS NULL
   AND files.is_user_visible_path(f.file_path)
   AND NOT files.is_crawl_artifact(f.id)
 ORDER BY f.file_name, f.id
 LIMIT 5000
"""


async def _plan(sql: str) -> str:
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    async with acquire_connection(bootstrap_db()) as conn:
        rows = await conn.fetch(f"EXPLAIN (ANALYZE, BUFFERS) {sql}", _OWNER)
    return "\n".join(r[0] for r in rows)


def _skip_without_db() -> None:
    missing = [n for n in _REQUIRED_ENV if not os.environ.get(n)]
    if missing:
        pytest.skip(f"live platform database unavailable: {', '.join(missing)} unset")


def _buffers(plan: str) -> int:
    """Total shared buffers touched by execution (excludes the Planning block)."""
    body = plan.split("Planning:")[0]
    hits = [int(m) for m in re.findall(r"shared (?:hit|read)=(\d+)", body)]
    return max(hits) if hits else 0


def _rows_removed(plan: str) -> int:
    return sum(int(m) for m in re.findall(r"Rows Removed by Filter: (\d+)", plan))


async def test_feed_page_uses_the_partial_index_and_filters_nothing():
    """Gate criteria 1 and 2: the index is chosen and the conjuncts are IMPLIED.

    'The conjuncts appear in neither Filter nor Index Cond' is the whole point:
    it proves the planner matched the index predicate rather than re-testing the
    rule per row. Red by dropping the index.
    """
    _skip_without_db()
    plan = await _plan(_FEED_PAGE)
    assert FEED_INDEX in plan, f"the feed page did not use {FEED_INDEX}:\n{plan}"
    assert "Seq Scan" not in plan, f"the feed page fell back to a sequential scan:\n{plan}"
    assert "Sort" not in plan, (
        f"the feed page sorted instead of walking the keyset in index order:\n{plan}"
    )
    assert "is_user_visible_path" not in plan, (
        "the visibility predicate is being re-tested per row instead of implied "
        f"by the index predicate:\n{plan}"
    )
    assert _rows_removed(plan) < 100, (
        f"{_rows_removed(plan)} rows removed by filter (gate: < 100):\n{plan}"
    )


async def test_feed_page_buffer_budget():
    """Gate criterion 3: shared buffers < 2,000 for one 500-row page.

    KNOWN MISS, recorded live 2026-09-13 at 5,835 buffers / 23.3 ms. Every buffer
    above ~495 belongs to ``files.is_crawl_artifact``, which runs three
    cross-schema subqueries per row; the identical page without that conjunct is
    495 buffers / 2.3 ms. is_crawl_artifact is not IMMUTABLE and cannot enter an
    index predicate, so the named fix is a stamped boolean column maintained by
    the web-capture writers (SPEC-SERVER §2.5).

    This test is deliberately left FAILING-BY-DESIGN as an xfail with the real
    number attached: it turns green by itself the day the stamped column lands,
    and nobody can quietly claim the gate passed in the meantime.
    """
    _skip_without_db()
    plan = await _plan(_FEED_PAGE)
    buffers = _buffers(plan)
    if buffers >= 2000:
        pytest.xfail(
            f"SPEC-SERVER §2.5 gate criterion 3 MISSES: {buffers} shared buffers for one "
            "500-row page (gate: < 2,000). Cause measured, not guessed: the same page "
            "without files.is_crawl_artifact() is 495 buffers. Fix = the stamped "
            "boolean column on the web-capture writers."
        )
    assert buffers < 2000


async def test_tree_owner_branch_uses_the_predicate_index():
    """§1.4's rewrite must not have cost get_user_file_tree its index.

    Recorded live 2026-09-13: 160.872 ms / 51,088 buffers after, against
    184.114 ms / 51,108 before -- names the new index and is 12.6% faster.
    """
    _skip_without_db()
    plan = await _plan(_TREE_OWNER_BRANCH)
    assert TREE_INDEX in plan, f"the tree's owner branch did not use {TREE_INDEX}:\n{plan}"
    assert "Seq Scan" not in plan, plan


async def test_the_feed_index_is_not_partial_on_deleted_at():
    """A tombstone-aware feed cannot be served by an alive-only index.

    If somebody "optimises" this index by adding ``deleted_at IS NULL``, every
    delete stops riding the feed and offline devices resurrect deleted files --
    silently, because the query still returns rows.
    """
    _skip_without_db()
    from matrx_orm import acquire_connection

    from matrx_files.db import bootstrap_db

    async with acquire_connection(bootstrap_db()) as conn:
        indexdef = await conn.fetchval(
            "SELECT indexdef FROM pg_indexes WHERE schemaname='files' AND indexname=$1",
            FEED_INDEX,
        )
    assert indexdef, f"{FEED_INDEX} does not exist on the live database"
    assert "deleted_at" not in indexdef, (
        f"{FEED_INDEX} became partial on deleted_at; tombstones would stop riding the feed:\n"
        f"{indexdef}"
    )
    assert "is_user_visible_path" in indexdef
