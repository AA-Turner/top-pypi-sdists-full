"""`kind_get` and `kindcomp_get_context` bound a kind's schema + canonical example.

Production (ops ``tool_result_overflow:kind_get`` / ``:kindcomp_get_context``):
``agent_input_qme_report`` 58,651 / 70,087 chars and
``resale_intelligence_report`` 72,424 — a large schema plus a large canonical
example, returned whole. ``bound_kind_bodies`` keeps the schema (the contract)
whole when it fits, cuts the example to the room left as announced TEXT, holds
the complete bodies for ``fetch_tool_result`` under this call, and says so.
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.tools import output_overflow
from matrx_ai.tools.implementations import kind_authoring, kind_component
from matrx_ai.tools.output_caps import TOOL_RESULT_SOFT_CAP_CHARS
from matrx_ai.tools.result_gate import _SINKS, apply_size_gate, register_tool_result_gate_sink


def _schema(n_props: int) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            f"field_{i:03d}": {"type": "string", "description": "A QME report section. " * 6}
            for i in range(n_props)
        },
    }


def _example(chars: int) -> dict[str, Any]:
    return {"__kind": "agent_input_qme_report", "body": "Q" * chars}


class _Rows:
    def __init__(self, rows):
        self._rows = rows

    def filter(self, *a, **kw):
        return self

    def order_by(self, *a):
        return self

    def limit(self, n):
        return self

    async def all(self):
        return self._rows


def _install(monkeypatch, module, schema, example) -> None:
    kd = SimpleNamespace(
        id="aa11aa11-0000-4000-8000-000000000000",
        kind="agent_input_qme_report",
        version=3,
        is_active=True,
        emitted_json_schema=schema,
    )
    canonical = SimpleNamespace(
        id="ex-1", kind_version=3, label="canonical", source="agent", is_canonical=True,
        validation_status="valid", deleted_at=None, data=example,
    )

    async def resolve(ref, ctx):
        return kd, None

    async def allow(*a, **kw):
        return None

    async def editor(*a, **kw):
        return False

    models = {"KindExample": _Rows([canonical])}
    monkeypatch.setattr(module, "resolve_kind", resolve)
    monkeypatch.setattr(module, "ensure_can_view_kind", allow)
    if hasattr(module, "can_access_kind"):
        monkeypatch.setattr(module, "can_access_kind", editor)
    monkeypatch.setattr(module, "get_db_model", lambda name: models.get(name, _Rows([])))
    monkeypatch.setattr(module, "kind_summary", lambda k: {"id": k.id, "kind": k.kind})
    monkeypatch.setattr(module, "kind_title_key", lambda k: None, raising=False)


@pytest.fixture
def gate_events():
    events = []
    register_tool_result_gate_sink(events.append)
    yield events
    _SINKS.remove(events.append)


def _ctx() -> SimpleNamespace:
    queued: list[Any] = []
    return SimpleNamespace(
        call_id="call_kind_bodies",
        user_id="u",
        conversation_id="c",
        queued=queued,
        queue_tool_changes=lambda add=None, remove=None: queued.extend(add or []),
    )


def _wire(result, tool: str) -> str:
    cd, truncated = apply_size_gate(
        result.to_tool_result_content(),
        output_self_capped=result.output_self_capped,
        tool_name=tool,
        tool_kind="native",
        conversation_id="c",
        user_id="u",
    )
    assert truncated is False
    return cd["content"]


CASES = [
    (kind_authoring, "kind_get", {"kind": "agent_input_qme_report"}),
    (kind_component, "kindcomp_get_context", {"kind": "agent_input_qme_report"}),
]


@pytest.mark.parametrize(("module", "tool", "args"), CASES)
async def test_large_example_is_cut_announced_and_held(monkeypatch, gate_events, module, tool, args) -> None:
    schema, example = _schema(60), _example(45_000)  # ~15K schema + 45K example
    _install(monkeypatch, module, schema, example)
    ctx = _ctx()
    r = await getattr(module, tool)(args, ctx)
    assert r.success, r.error
    assert {"kind": "registered", "name": "fetch_tool_result"} in ctx.queued
    assert r.output_self_capped is True
    assert r.output.json_schema == schema  # the contract stays whole
    assert isinstance(r.output.canonical_example, str)  # cut → announced text
    assert "fetch_tool_result" in r.output.note and "call_kind_bodies" in r.output.note
    assert len(_wire(r, tool)) < TOOL_RESULT_SOFT_CAP_CHARS
    assert gate_events == []
    # The complete bodies really are fetchable under this call.
    sl = output_overflow.fetch_overflow(
        call_id="call_kind_bodies", user_id="u", conversation_id="c", offset=0, max_chars=10_000_000
    )
    assert sl is not None and json.loads(sl.content)["canonical_example"] == example


@pytest.mark.parametrize(("module", "tool", "args"), CASES)
async def test_oversized_schema_becomes_a_marked_stand_in(monkeypatch, module, tool, args) -> None:
    schema = _schema(400)  # ~100K schema
    _install(monkeypatch, module, schema, _example(100))
    r = await getattr(module, tool)(args, _ctx())
    assert r.output.json_schema["__truncated__"] is True
    assert len(r.output.json_schema["top_level_properties"]) == 400
    assert r.output.canonical_example is None
    assert "stand-in" in r.output.note
    assert len(_wire(r, tool)) < TOOL_RESULT_SOFT_CAP_CHARS


@pytest.mark.parametrize(("module", "tool", "args"), CASES)
async def test_small_bodies_are_untouched(monkeypatch, module, tool, args) -> None:
    schema, example = _schema(3), _example(200)
    _install(monkeypatch, module, schema, example)
    r = await getattr(module, tool)(args, _ctx())
    assert r.output.json_schema == schema and r.output.canonical_example == example
    assert r.output.note is None
