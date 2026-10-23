"""Writers of a shared jsonb column change only their own keys — proven on the SQL.

THE INCIDENT (2026-10-22). ``_upsert_site_keyword_value`` wrote ``metadata={...}`` over
``seo.site_keyword_value.metadata``: every page-analysis / page-map write erased the
record's serp_cluster, classification, map_home and valuation. And a cluster writer
stored an expression object as data over 1,328 rows.

These tests run the REAL ORM compilation (model → executor → asyncpg adapter); only
``AsyncDatabaseManager`` — the wire to Postgres — is replaced, recording the SQL that
would run. So they fail when a writer compiles to a whole-column SET, whatever the
Python looks like. The static guard
against new whole-column writes is aidream/services/seo/tests/test_no_whole_jsonb_writes.py.
"""

from __future__ import annotations

import re
from typing import Any

import pytest
from matrx_orm import JsonbMerge, JsonbRemoveKeys
from matrx_orm.core.async_db_manager import AsyncDatabaseManager

import matrx_seo.artifact_writers as aw
from matrx_seo.db import models_seo as m

TABLE = "seo.site_keyword_value"


@pytest.fixture
def wire(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    from matrx_orm.adapters import AdapterRegistry
    from matrx_orm.adapters.async_postgresql import AsyncPostgreSQLAdapter

    seen: dict[str, Any] = {"writes": [], "rows": [], "reads": []}

    async def execute_write(cls, config: str, sql: str, *params: Any, **kw: Any):
        seen["writes"].append((sql, params))
        return [{"id": "rec-1", "keyword_id": "kw-1", "_matrx_inserted": False}]

    async def execute_query(cls, config: str, sql: str, *params: Any, **kw: Any):
        # Honour the one predicate these writers read by: live vs soft-deleted records.
        seen["reads"].append(sql)
        wants_deleted = "deleted_at IS NOT NULL" in sql
        rows = [r for r in seen["rows"] if (r.get("deleted_at") is not None) == wants_deleted]
        if "keyword_id = ANY(" in sql:  # honour the keyword filter too
            wanted = next(p for p in params if isinstance(p, list))
            rows = [r for r in rows if r["keyword_id"] in wanted]
        return rows

    monkeypatch.setattr(AsyncDatabaseManager, "execute_write", classmethod(execute_write))
    monkeypatch.setattr(AsyncDatabaseManager, "execute_query", classmethod(execute_query))
    monkeypatch.setattr(AdapterRegistry, "get", staticmethod(lambda db: AsyncPostgreSQLAdapter(db)))

    class _AsyncNull:
        async def __aenter__(self) -> None:
            return None

        async def __aexit__(self, *exc: Any) -> None:
            return None

    monkeypatch.setattr(aw, "transaction", lambda *_a, **_k: _AsyncNull())
    return seen


def _metadata_set(sql: str) -> str:
    """The SET expression the statement gives ``metadata`` (empty when it sets none)."""
    match = re.search(
        r"\bmetadata = (.*?)(?=, [a-z_]+ = | WHERE | RETURNING |$)", sql.split(" SET ", 1)[-1]
    )
    return f"metadata = {match.group(1)}" if match else ""


@pytest.mark.asyncio
async def test_the_page_writers_upsert_merges_metadata_never_overwrites_it(
    wire: dict[str, Any],
) -> None:
    await aw._upsert_site_keyword_value(
        site_id="site-1",
        keyword_id="kw-1",
        organization_id="org-1",
        created_by="user-1",
        fields={
            "content_role": "pillar",
            "workflow_status": "targeted",
            "metadata": {"page_id": "p-1"},
        },
    )
    assert len(wire["writes"]) == 1, "one statement: no SELECT-then-UPDATE race"
    sql, _ = wire["writes"][0]
    assert (
        sql.startswith(f"INSERT INTO {TABLE}")
        and "ON CONFLICT (site_id, keyword_id) DO UPDATE SET" in sql
    )
    assert _metadata_set(sql) == f"metadata = ({TABLE}.metadata || EXCLUDED.metadata)"
    assert "content_role = EXCLUDED.content_role" in sql
    # Columns the writer did not supply are never touched on conflict.
    assert "custom_fields = EXCLUDED" not in sql and "version = EXCLUDED" not in sql


@pytest.mark.asyncio
async def test_update_where_with_jsonb_merge_compiles_to_a_merge(wire: dict[str, Any]) -> None:
    await m.SiteKeywordValue.update_where(
        {"id": "rec-1"}, metadata=JsonbMerge("metadata", {"serp_cluster": {"a": 1}})
    )
    sql, params = wire["writes"][0]
    assert _metadata_set(sql).startswith("metadata = COALESCE(metadata, '{}'::jsonb) || $")
    assert '{"serp_cluster": {"a": 1}}' in params


@pytest.mark.asyncio
async def test_clearing_a_stale_cluster_removes_only_that_key(wire: dict[str, Any]) -> None:
    wire["rows"] = [
        {
            "id": "rec-old",
            "keyword_id": "kw-gone",
            "site_id": "site-1",
            "organization_id": "org-1",
            "metadata": {
                "classification": {"x": 1},
                "serp_cluster": {"status": "clustered", "cluster_id": "serp-1"},
            },
        },
        {
            "id": "rec-1",
            "keyword_id": "kw-1",
            "site_id": "site-1",
            "organization_id": "org-1",
            "metadata": {"valuation": {"y": 2}},
        },
    ]
    row = {
        "keyword_id": "kw-1",
        "status": "alone",
        "reason": "no other keyword shares enough top results",
    }
    out = await aw.apply_serp_clusters(
        [row], site_id="site-1", organization_id="org-1", created_by="u", settings={}
    )
    assert out == {"keywords_written": 1, "unchanged": 0, "records_created": 0, "skipped_deleted": 0, "stale_cleared": 1}
    sqls = [s for s, _ in wire["writes"]]
    upsert = next(s for s in sqls if s.startswith("INSERT"))
    assert _metadata_set(upsert) == f"metadata = ({TABLE}.metadata || EXCLUDED.metadata)"
    clear = next(s for s in sqls if s.startswith("UPDATE"))
    assert _metadata_set(clear).startswith("metadata = COALESCE(metadata, '{}'::jsonb) - $")
    assert ["serp_cluster"] in next(p for s, p in wire["writes"] if s.startswith("UPDATE"))


@pytest.mark.asyncio
async def test_a_rerun_with_the_same_clusters_writes_nothing(wire: dict[str, Any]) -> None:
    value = {
        "status": "alone",
        "settings": {},
        "reason": "no other keyword shares enough top results",
    }
    wire["rows"] = [
        {
            "id": "rec-1",
            "keyword_id": "kw-1",
            "site_id": "site-1",
            "organization_id": "org-1",
            "metadata": {"serp_cluster": {**value, "computed_at": "2026-10-22T00:00:00+00:00"}},
        }
    ]
    row = {"keyword_id": "kw-1", "status": "alone", "reason": value["reason"]}
    out = await aw.apply_serp_clusters(
        [row], site_id="site-1", organization_id="org-1", created_by="u", settings={}
    )
    assert out["unchanged"] == 1 and wire["writes"] == []


def test_jsonb_remove_keys_renders_a_key_removal() -> None:
    params: list[Any] = []
    assert (
        JsonbRemoveKeys("metadata", ["a", "b"]).as_sql(params)
        == "COALESCE(metadata, '{}'::jsonb) - $1::text[]"
    )
    assert params == [["a", "b"]]


# The static guard against whole-column writes of shared jsonb columns (this package and
# aidream/services/seo) lives once, in aidream/services/seo/tests/test_no_whole_jsonb_writes.py.


@pytest.mark.asyncio
async def test_a_soft_deleted_record_is_skipped_never_revived_or_counted_as_created(wire: dict[str, Any]) -> None:
    wire["rows"] = [
        {"id": "rec-dead", "keyword_id": "kw-dead", "site_id": "site-1", "organization_id": "org-1",
         "metadata": {"classification": {"x": 1}}, "deleted_at": "2026-10-01T00:00:00+00:00"},
    ]
    rows = [
        {"keyword_id": "kw-dead", "status": "alone", "reason": "r"},
        {"keyword_id": "kw-1", "status": "alone", "reason": "r"},
    ]
    out = await aw.apply_serp_clusters(rows, site_id="site-1", organization_id="org-1", created_by="u", settings={})
    assert out["skipped_deleted"] == 1
    assert out["keywords_written"] == 1 and out["records_created"] == 0  # the fake answers _matrx_inserted=False
    inserts = [p for s, p in wire["writes"] if s.startswith("INSERT")]
    assert len(inserts) == 1 and "kw-dead" not in inserts[0] and "kw-1" in inserts[0]
    assert any("deleted_at IS NOT NULL" in r for r in wire["reads"])


@pytest.mark.asyncio
async def test_insert_only_columns_seed_a_new_record_but_never_overwrite_one(wire: dict[str, Any]) -> None:
    await aw.merge_upsert_site_keyword_values(
        [{"organization_id": "o", "site_id": "site-1", "keyword_id": "kw-1", "created_by": "u",
          "workflow_status": "candidate", "metadata": {"provenance": 1}}],
        insert_only={"workflow_status"},
    )
    sql = next(s for s, _ in wire["writes"] if s.startswith("INSERT"))
    assert "workflow_status" in sql.split(" ON CONFLICT ")[0]
    assert "workflow_status = EXCLUDED" not in sql
    assert _metadata_set(sql) == f"metadata = ({TABLE}.metadata || EXCLUDED.metadata)"
