"""A hub table's `schema` answer bounds its FK lists itself, so the platform size gate never cuts it.

Live: db_read(action='schema', table='iam.organizations') on 2026-11-12 returned 55,503 chars —
51,831 of them `referenced_by` (1,107 referencing columns) — and tripped
``tool_result_overflow:db_read``. SUT: the real ``db_schema`` with only the catalog seam stubbed.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from matrx_ai.tools.implementations import database
from matrx_ai.tools.models import ToolContext
from matrx_ai.tools.output_caps import TOOL_RESULT_SOFT_CAP_CHARS


def _stub_catalog(monkeypatch: pytest.MonkeyPatch, fk_rows: list[dict[str, str]]) -> None:
    import matrx_orm.catalog as catalog

    async def resolve(requested: str) -> tuple[str, str, list[str]]:
        return "iam", "organizations", []

    async def columns(database_name: str, *, schema: str, table: str) -> list[dict[str, Any]]:
        return [{"column_name": "id"}, {"column_name": "name"}]

    async def checks(database_name: str, *, schema: str, table: str) -> list[dict[str, str]]:
        return []

    async def fks(database_name: str, *, schema: str, table: str) -> list[dict[str, str]]:
        return fk_rows

    monkeypatch.setattr(database, "_resolve_table", resolve)
    monkeypatch.setattr(database, "_get_database_name", lambda: "x")
    monkeypatch.setattr(catalog, "describe_relation_columns", columns)
    monkeypatch.setattr(catalog, "relation_check_constraints", checks)
    monkeypatch.setattr(catalog, "relation_foreign_key_columns", fks)


@pytest.mark.asyncio
async def test_a_hub_tables_referenced_by_is_cut_and_says_so(monkeypatch: pytest.MonkeyPatch) -> None:
    rows = [
        {"direction": "in", "local_col": "organization_id", "other_table": f"some_schema.feature_table_{i}", "other_col": "id"}
        for i in range(1107)
    ]
    _stub_catalog(monkeypatch, rows)

    result = await database.db_schema({"table": "iam.organizations"}, ToolContext(call_id="c"))

    assert result.success
    out = result.output
    assert len(json.dumps(out)) < TOOL_RESULT_SOFT_CAP_CHARS
    assert 0 < len(out["referenced_by"]) < 1107
    assert f"referenced_by shows {len(out['referenced_by'])} of 1107" in out["note"]


@pytest.mark.asyncio
async def test_a_small_tables_fk_lists_are_whole_and_carry_no_note(monkeypatch: pytest.MonkeyPatch) -> None:
    _stub_catalog(
        monkeypatch,
        [{"direction": "out", "local_col": "org_id", "other_table": "iam.organization", "other_col": "id"}],
    )

    result = await database.db_schema({"table": "iam.organizations"}, ToolContext(call_id="c"))

    assert result.output["foreign_keys"] == ["org_id -> iam.organization.id"]
    assert result.output["referenced_by"] == []
    assert "note" not in result.output
