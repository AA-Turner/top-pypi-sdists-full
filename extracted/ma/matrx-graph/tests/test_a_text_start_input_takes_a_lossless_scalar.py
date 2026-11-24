"""Guard (2026-11-09, Tule Creek "Send to vendor"): a start input declared as text that is handed
a yes/no or a number is written as its canonical text and the step says so; an object or list
still fails with the plain per-field message (validation offers, never blocks).

Live: workflow 23fadd5b declares needs_owner_approval as text; the dispatch card sent ``true`` and
the strict start check refused with "True is not of type 'string'".
"""

from __future__ import annotations

from typing import Any

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph, run_log
from matrx_graph.nodes import register_builtin_nodes
from matrx_graph.text_inputs import text_scalars_as_text
from tests._fixtures import FakeEmitter, make_app_context

_SCHEMA = {"properties": {"needs_owner_approval": {"type": "string"}, "n": {"type": "string"}, "ok": {"type": "boolean"}}}


def test_scalars_become_canonical_text() -> None:
    out, done = text_scalars_as_text({"needs_owner_approval": True, "n": 3, "ok": True}, _SCHEMA)
    assert out == {"needs_owner_approval": "true", "n": "3", "ok": True}
    assert [d[0] for d in done] == ["needs_owner_approval", "n"]
    out, _ = text_scalars_as_text({"needs_owner_approval": False}, _SCHEMA)
    assert out["needs_owner_approval"] == "false"


def test_objects_are_left_for_the_gate_to_refuse() -> None:
    out, done = text_scalars_as_text({"n": {"a": 1}}, _SCHEMA)
    assert out == {"n": {"a": 1}} and done == []


async def _run(value: Any):
    flags: list[dict[str, Any]] = []

    async def record(**kw: Any) -> Any:
        flags.append(kw)
        return run_log.RunLogEntry(recorded=True, entry_id=str(len(flags)), label=kw["label"], needs_review=kw["needs_review"])

    reg = NodeRegistry()
    register_builtin_nodes(reg)
    node = {
        "id": "start", "type": "io.user_input", "position": {"x": 0, "y": 0},
        "data": {"config": {"fields": [{"key": "needs_owner_approval", "label": "Needs approval", "type": "text", "required": True}]}},
    }
    run_log.configure_run_log_writer(record)
    try:
        graph = compile_graph(Definition.model_validate({"nodes": [node], "edges": []}), registry=reg)
        res = await Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=reg).run(
            run_id="scalar-text", node_inputs={"start": {"needs_owner_approval": value}}
        )
    finally:
        run_log.configure_run_log_writer(None)
    return res, flags


async def test_a_yes_no_into_a_text_start_input_runs_and_says_so() -> None:
    res, flags = await _run(True)
    assert res.status is RunStatus.COMPLETED, res.error
    assert "'true'" in str(res.last_outputs), res.last_outputs
    assert any(f["label"] == "engine.sent_scalar_as_text.needs_owner_approval" for f in flags), flags


async def test_an_object_into_a_text_start_input_still_fails_plainly() -> None:
    res, _ = await _run({"a": 1})
    assert res.status is not RunStatus.COMPLETED
    assert "needs_owner_approval" in str(res.error) or "don't match" in str(res.error)
