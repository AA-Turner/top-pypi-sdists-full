"""`toolcomp_list_tools` group_by mode is a bounded discovery view.

Production (ops ``tool_result_overflow:toolcomp_list_tools``, 08-31 and 09-04):
``group_by='prefix'`` returned every full row of all ~500 tools — 169,438 chars —
ignoring ``limit``. Grouped mode now returns each group's count and tool NAMES,
plus a note naming the per-family call for the rows.
"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from matrx_ai.tools.implementations import tool_component
from matrx_ai.tools.output_caps import TOOL_RESULT_SOFT_CAP_CHARS
from matrx_ai.tools.result_gate import _SINKS, apply_size_gate, register_tool_result_gate_sink

PREFIXES = [f"fam{i:02d}" for i in range(60)]


def _rows() -> list[SimpleNamespace]:
    rows = []
    for i in range(500):
        values = {
            "id": f"00000000-0000-0000-0000-{i:012d}",
            "name": f"{PREFIXES[i % 60]}_tool_{i:03d}",
            "description": "Does a thing. " * 40,
            "category": "core",
            "tags": ["alpha", "beta", "gamma"],
            "is_active": True,
            "source_kind": "native",
        }
        rows.append(SimpleNamespace(_fields=values, **values))
    return sorted(rows, key=lambda r: r.name)


class _Query:
    def __init__(self, rows):
        self._rows = rows

    def filter(self, *a, **kw):
        return self

    def order_by(self, *a):
        return self

    def limit(self, n):
        return _Query(self._rows[:n])

    async def all(self):
        return self._rows


class _ToolDefinition:
    @classmethod
    def filter(cls, **kw):
        return _Query(_rows())


@pytest.fixture
def fake_db(monkeypatch):
    monkeypatch.setattr(tool_component, "get_db_model", lambda name: _ToolDefinition)


@pytest.fixture
def gate_events():
    events = []
    register_tool_result_gate_sink(events.append)
    yield events
    _SINKS.remove(events.append)


def _wire(result) -> str:
    cd, truncated = apply_size_gate(
        result.to_tool_result_content(),
        output_self_capped=result.output_self_capped,
        tool_name="toolcomp_list_tools",
        tool_kind="native",
        conversation_id="c",
        user_id="u",
    )
    assert truncated is False
    return cd["content"]


@pytest.mark.asyncio
async def test_grouped_mode_is_names_only_and_under_the_cap(fake_db, gate_events) -> None:
    r = await tool_component.toolcomp_list_tools({"group_by": "prefix", "limit": 60}, SimpleNamespace())
    assert r.success and r.output_self_capped
    wire = _wire(r)
    assert len(wire) < TOOL_RESULT_SOFT_CAP_CHARS
    assert gate_events == []
    out = json.loads(wire)
    assert out["group_count"] == 60 and out["total_tools"] == 500
    fam = out["groups"]["fam00"]
    assert fam["count"] == len(fam["names"]) == 9  # every name, nothing silently dropped
    assert sum(g["count"] for g in out["groups"].values()) == 500
    assert "prefix=<group>" in out["note"]


@pytest.mark.asyncio
async def test_flat_mode_is_paginated_and_bounded(fake_db) -> None:
    r = await tool_component.toolcomp_list_tools({"limit": 100}, SimpleNamespace())
    assert r.output_self_capped
    assert len(_wire(r)) < TOOL_RESULT_SOFT_CAP_CHARS
    assert r.output.has_more is True and r.output.next_offset == 100
