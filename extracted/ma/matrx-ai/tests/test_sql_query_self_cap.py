"""The `sql` tool bounds its own query result — it never hands the size gate a blob.

Production evidence (ops.ops_issue_class ``tool_result_overflow:sql``, 37 events
2026-07-28 → 2026-09-24): every firing was ``action='query'`` — e.g.
``projects.tasks`` with ``limit=1000`` and a ``metadata`` column (1,814,404 chars),
``chat.message`` with ``limit=10`` and ``content`` (55,774 chars),
``admin.feature_docs`` with ``fields=['*']`` (667,638 chars). The generic gate then
sliced the serialized JSON mid-object. These tests drive both read paths (the
super-admin ORM path and the RLS runner path) through the real producer and
through the real size gate.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from matrx_ai import _ext
from matrx_ai.tools.implementations import database
from matrx_ai.tools.models import ToolContext
from matrx_ai.tools.output_caps import TOOL_RESULT_SOFT_CAP_CHARS
from matrx_ai.tools.result_gate import apply_size_gate


def _tasks(n: int, meta_chars: int) -> list[dict[str, Any]]:
    return [
        {"id": f"task-{i:04d}", "title": f"Task {i}", "metadata": {"blob": "x" * meta_chars}}
        for i in range(n)
    ]


def _serialized(output: Any) -> str:
    return json.dumps(output, ensure_ascii=False)


async def _run_rls(monkeypatch, rows: list[dict[str, Any]], **args: Any):
    async def runner(**kwargs: Any) -> list[dict[str, Any]]:
        return rows

    monkeypatch.setattr(_ext, "get_scoped_query_runner", lambda: runner)
    return await database._sql_query_scoped(
        {"table": "projects.tasks", **args}, ToolContext(call_id="c-rls"), 1.0, "developer"
    )


async def _run_super(monkeypatch, rows: list[dict[str, Any]], **args: Any):
    async def select(*a: Any, **kw: Any) -> list[dict[str, Any]]:
        return rows

    monkeypatch.setattr("matrx_orm.operations.dynamic_crud.dynamic_select", select)
    return await database.db_query({"table": "projects.tasks", **args}, ToolContext(call_id="c-su"))


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["rls", "super"])
async def test_large_query_is_self_capped_with_an_exact_continuation(monkeypatch, path) -> None:
    rows = _tasks(1000, 1500)  # ~1.6 MB serialized — the 2026-09-13 production shape
    run = _run_rls if path == "rls" else _run_super
    result = await run(monkeypatch, rows, limit=1000, offset=0)

    assert result.success is True
    out = result.output
    # Bounded, and the tool declares it (so the generic gate stands down honestly).
    assert result.output_self_capped is True
    assert len(_serialized(out)) < TOOL_RESULT_SOFT_CAP_CHARS
    # Honest marker + an exact way to get the rest.
    assert out["truncated"] is True
    shown = out["count"]
    assert 0 < shown < 1000
    assert out["total"] == 1000
    assert out["next_offset"] == shown
    assert "offset=" in out["truncation_notice"]
    # Rows returned are whole, valid, in order — never a sliced object.
    assert [r["id"] for r in out["rows"]] == [f"task-{i:04d}" for i in range(shown)]


@pytest.mark.asyncio
async def test_continuation_offset_is_absolute(monkeypatch) -> None:
    result = await _run_rls(monkeypatch, _tasks(200, 1500), limit=200, offset=400)
    out = result.output
    assert out["truncated"] is True
    assert out["next_offset"] == 400 + out["count"]


@pytest.mark.asyncio
async def test_one_fat_cell_is_trimmed_and_named_not_the_whole_page(monkeypatch) -> None:
    rows = [
        {"id": f"m-{i}", "role": "user", "content": ("word " * 4000) if i == 3 else "short"}
        for i in range(10)
    ]
    result = await _run_rls(monkeypatch, rows, limit=10)
    out = result.output
    assert result.output_self_capped is True
    assert out["count"] == 10  # every row still delivered
    assert len(out["rows"][3]["content"]) < 20_000
    assert out["truncated_cells"] == [
        {"row_index": 3, "column": "content", "total_chars": 20_000,
         "shown_chars": len(out["rows"][3]["content"])}
    ]
    assert "content" in out["truncation_notice"]
    assert len(_serialized(out)) < TOOL_RESULT_SOFT_CAP_CHARS


@pytest.mark.asyncio
async def test_single_row_single_column_read_gets_the_larger_cell_allowance(monkeypatch) -> None:
    """The documented way to read a trimmed cell in full actually returns more."""
    big = "y" * 30_000
    result = await _run_rls(monkeypatch, [{"content": big}], limit=1, fields=["content"])
    out = result.output
    assert out["rows"][0]["content"] == big
    assert "truncated_cells" not in out


@pytest.mark.asyncio
async def test_small_result_shape_is_unchanged(monkeypatch) -> None:
    result = await _run_rls(monkeypatch, [{"id": "a"}], limit=10)
    assert result.output == {"rows": [{"id": "a"}], "count": 1}
    assert result.output_self_capped is True


@pytest.mark.asyncio
async def test_full_page_hints_that_more_rows_may_exist(monkeypatch) -> None:
    result = await _run_rls(monkeypatch, [{"id": str(i)} for i in range(5)], limit=5, offset=10)
    out = result.output
    assert out["count"] == 5
    assert out["more_may_exist"] is True
    assert out["next_offset"] == 15


@pytest.mark.asyncio
async def test_the_real_size_gate_does_not_fire(monkeypatch) -> None:
    """End to end through the gate: no soft_fired event for a self-capped sql result."""
    from matrx_ai.tools import result_gate

    events: list[Any] = []
    monkeypatch.setattr(result_gate, "_emit", lambda e: events.append(e))
    result = await _run_rls(monkeypatch, _tasks(1000, 1500), limit=1000)
    content = {"call_id": "c-rls", "content": _serialized(result.output)}
    gated, truncated = apply_size_gate(
        content,
        output_self_capped=result.output_self_capped,
        tool_name="sql",
        tool_kind="native",
        conversation_id=None,
        user_id=None,
    )
    assert truncated is False
    assert gated["content"] == content["content"]
    assert [e for e in events if e.tier == "soft_fired"] == []


def test_sql_kind_declares_every_cap_key() -> None:
    from matrx_ai.tools.kinds.database_tools import SqlToolResult

    for key in ("total", "truncated", "truncation_notice", "next_offset",
                "more_may_exist", "truncated_cells"):
        assert key in SqlToolResult.model_fields, key


@pytest.mark.asyncio
async def test_public_sql_entry_keeps_the_bound_after_kind_stamping(monkeypatch) -> None:
    """Through `database.sql` (the registered tool): stamped kind, still bounded."""

    async def runner(**kwargs: Any) -> list[dict[str, Any]]:
        return _tasks(1000, 1500)

    monkeypatch.setattr(_ext, "get_scoped_query_runner", lambda: runner)
    monkeypatch.setattr(database, "_current_admin_level", lambda: "developer")

    async def resolve(table: str):
        return table, None

    monkeypatch.setattr(database, "_resolve_read_target", resolve)
    result = await database.sql(
        {"action": "query", "table": "projects.tasks", "limit": 1000},
        ToolContext(call_id="c-pub"),
    )
    assert result.success is True
    assert result.output["__kind"] == "sql_tool_result"
    assert result.output_self_capped is True
    assert result.output["truncated"] is True
    assert len(_serialized(result.output)) < TOOL_RESULT_SOFT_CAP_CHARS
