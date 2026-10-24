"""Closing fixes for the visual-map repair loop (legible-diagrams closing verification, 2026-10-23).

Each test names the defect it catches on the code before the fix:

- D1: the gate ran AFTER the per-turn commit barrier, so the stored turn kept the model's draft; and the
  checked event carried no position a client could use to replace the drawn draft.
- D2: a spec without ``schema_version`` / ``diagram_type`` (Haiku, S3) was sent to validate as-is, so every
  repair round chased the schema.
- D9: a repair that removed states to pass layout was stamped verified (S4: 9 of 11 states).
"""

from __future__ import annotations

import asyncio
import contextvars
import inspect
from types import SimpleNamespace
from typing import Any

from matrx_ai.orchestrator import visual_map_repair as vmr
from matrx_ai.orchestrator.visual_map_repair import CallPointResult, RepairKnobs, run_repair_loop

K4 = RepairKnobs(max_rounds=4, stall_rounds=2, quality="showcase")

LIFECYCLE = {
    "schema_version": 3, "diagram_type": "lifecycle", "meta": {"title": "Run states"},
    "states": [{"id": s, "label": s.title()} for s in ("queued", "running", "pausing", "paused", "done")],
    "transitions": [{"from": "queued", "to": "running"}, {"from": "running", "to": "done"}],
}


class Engine:
    """Validate answers from a script; deliver says verified when the spec validated clean."""

    def __init__(self, errors_by_round: list[int], *, version: int | None = 1) -> None:
        self.errors = list(errors_by_round)
        self.validated: list[dict[str, Any]] = []
        self.version = version

    async def read_knobs(self, *, organization_id, user_id):
        return {}

    async def schema_version(self, type):  # noqa: A002
        return self.version

    async def validate(self, type, spec, *, quality):  # noqa: A002
        self.validated.append(spec)
        n = self.errors[min(len(self.validated) - 1, len(self.errors) - 1)]
        return {"ok": n == 0, "diagnostics": [{"code": "layout/overlap", "severity": "error", "message": "x"}] * n}

    async def deliver(self, type, spec, *, organization_id, subject_ref, round, quality):  # noqa: A002
        return {"ok": True, "verified": True, "issues": 0, "inspection_id": "insp", "receipt": {"type": type},
                "screenshot_file_id": None, "diagnostics": []}

    async def persist_round(self, **_):
        return "row"

    async def repair(self, provision, *, organization_id):
        return CallPointResult(bound=False)

    async def review(self, provision, *, organization_id):
        return CallPointResult(bound=False)


def _loop(engine: Engine, value: dict[str, Any], fallback=None):
    return asyncio.run(run_repair_loop(
        value, delivery=engine, knobs=K4, organization_id="org", subject_ref="request:r#0",
        user_request="draw it", fallback_repair=fallback,
    ))


# ── D2 ────────────────────────────────────────────────────────────────────────────────────────────


def test_missing_schema_version_and_diagram_type_are_filled_before_validate():
    engine = Engine([0], version=3)
    spec = {k: v for k, v in LIFECYCLE.items() if k not in ("schema_version", "diagram_type")}
    out = _loop(engine, {"__kind": "visual_map", "type": "lifecycle", "spec": spec})
    first = engine.validated[0]
    assert first["diagram_type"] == "lifecycle" and first["schema_version"] == 3
    assert out.value["spec"]["schema_version"] == 3 and out.verified
    assert any("schema_version" in n for n in out.notes)


def test_a_written_schema_version_is_never_overwritten():
    engine = Engine([0], version=3)
    out = _loop(engine, {"__kind": "visual_map", "type": "workflow",
                         "spec": {"schema_version": 1, "diagram_type": "workflow", "nodes": []}})
    assert engine.validated[0]["schema_version"] == 1 and out.value["spec"]["schema_version"] == 1


def test_a_repair_answer_that_drops_the_fields_gets_them_back():
    engine = Engine([2, 0], version=3)

    async def fallback(provision):
        bare = {k: v for k, v in provision["spec"].items() if k not in ("schema_version", "diagram_type")}
        return {"__kind": "visual_map", "type": "lifecycle", "spec": bare}

    _loop(engine, {"__kind": "visual_map", "type": "lifecycle", "spec": LIFECYCLE}, fallback)
    assert engine.validated[1]["schema_version"] == 3 and engine.validated[1]["diagram_type"] == "lifecycle"


# ── D9 ────────────────────────────────────────────────────────────────────────────────────────────


def _dropping_fallback(explain: bool):
    async def fallback(provision):
        spec = dict(provision["spec"])
        spec["states"] = [s for s in spec["states"] if s["id"] not in ("pausing", "paused")]
        if explain:
            spec["cards"] = [{"title": "Not drawn", "items": ["Pausing and Paused are rare; left out"]}]
        return {"__kind": "visual_map", "type": "lifecycle", "spec": spec}
    return fallback


def test_a_repair_that_drops_content_never_removes_it():
    """Repair-reliability lane: a whole-spec answer is diffed against the best spec; a removed item is put
    back, so a repair can no longer pass layout by deleting states (S4 drew 9 of 11)."""
    engine = Engine([3, 0])
    out = _loop(engine, {"__kind": "visual_map", "type": "lifecycle", "spec": LIFECYCLE}, _dropping_fallback(False))
    assert [s["id"] for s in out.value["spec"]["states"]] == ["queued", "running", "pausing", "paused", "done"]
    assert out.dropped == []


def _relabel_fallback():
    async def fallback(provision):
        return '{"changes": [{"list": "states", "index": 2, "set": {"label": "Pause"}}]}'
    return fallback


def test_content_that_still_is_not_drawn_is_never_verified():
    unnamed = {**LIFECYCLE, "states": [{"label": s.title()} for s in ("queued", "running", "pausing", "done")]}
    out = _loop(Engine([3, 0]), {"__kind": "visual_map", "type": "lifecycle", "spec": unnamed}, _relabel_fallback())
    assert out.verified is False
    assert out.value["issues"] >= 1
    assert out.dropped == ["Pausing"]
    assert any("content dropped: states: Pausing" in n for n in out.notes)
    dropped = [d for r in out.rounds for d in r.diagnostics if d.get("code") == "content/dropped"]
    assert dropped and "put back" in dropped[0]["supportedFixes"][0]


def test_a_drop_the_spec_explains_in_its_cards_may_be_verified():
    engine = Engine([3, 0])
    out = _loop(engine, {"__kind": "visual_map", "type": "lifecycle", "spec": LIFECYCLE}, _dropping_fallback(True))
    assert out.verified is True


def test_content_inventory_reads_every_drawn_list_not_the_notes():
    inv = vmr.content_inventory({**LIFECYCLE, "cards": [{"title": "x"}]})
    assert set(inv) == {"states", "transitions"} and len(inv["states"]) == 5
    assert "queued->running" in inv["transitions"]


# ── D1 ────────────────────────────────────────────────────────────────────────────────────────────


def test_the_gate_runs_before_the_turn_barrier_that_stores_the_text():
    """The barrier is the final turn's only write of its text; a gate after it changes nothing durable."""
    from matrx_ai.orchestrator import executor

    src = inspect.getsource(executor)
    gate = src.index("await visual_map_gate(current_request, response, exec_ctx)")
    barrier = src.index("# ── PER-TURN COMMIT BARRIER")
    final_branch = src.index("# Finish - no more tool calls needed")
    assert gate < barrier < final_branch
    assert src.count("await visual_map_gate(") == 1


class Emitter:
    def __init__(self) -> None:
        self.infos: list[Any] = []

    async def send_info(self, payload):
        self.infos.append(payload)

    async def send_warning(self, payload):
        pass


def test_checked_events_carry_document_order_and_the_text_holds_the_stamped_value(monkeypatch):
    import matrx_ai._ext as ext
    from matrx_connect.context.app_context import AppContext, set_app_context
    from matrx_connect.emitters import SilentEmitter

    one = '{"__kind": "visual_map", "type": "lifecycle", "spec": {"schema_version": 3, "diagram_type": "lifecycle", "states": [{"id": "a"}]}}'
    two = '{"__kind": "visual_map", "type": "lifecycle", "spec": {"schema_version": 3, "diagram_type": "lifecycle", "states": [{"id": "b"}]}}'
    part = SimpleNamespace(text=f"First:\n{one}\nSecond:\n{two}\n", metadata={})
    monkeypatch.setattr(vmr, "_assistant_text_parts", lambda *_: [part])
    monkeypatch.setattr(vmr, "authoring_model_repairer", lambda _req: None)
    emitter = Emitter()

    def _in_ctx():
        set_app_context(AppContext(emitter=SilentEmitter(), user_id="u", organization_id="org", request_id="req"))
        ext._registry["visual_map_delivery"] = Engine([0])
        try:
            request = SimpleNamespace(config=SimpleNamespace(messages=[]), request_id="req")
            return asyncio.run(vmr.visual_map_gate(request, None, SimpleNamespace(emitter=emitter)))
        finally:
            ext._registry.pop("visual_map_delivery", None)

    outcomes = contextvars.copy_context().run(_in_ctx)
    checked = [i.metadata for i in emitter.infos if i.code == vmr.CHECKED_CODE]
    assert sorted((c["ordinal"], c["total"]) for c in checked) == [(0, 2), (1, 2)]
    by_ordinal = {c["ordinal"]: c for c in checked}
    assert by_ordinal[0]["value"]["spec"]["states"] == [{"id": "a"}]
    assert by_ordinal[0]["subject_ref"].endswith("#0") and by_ordinal[1]["subject_ref"].endswith("#1")
    assert len(outcomes) == 2 and part.text.count('"inspection_id":"insp"') == 2
    assert part.text.index('"id":"a"') < part.text.index('"id":"b"')
