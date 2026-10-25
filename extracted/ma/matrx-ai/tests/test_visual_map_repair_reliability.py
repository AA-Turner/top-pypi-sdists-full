"""Repair reliability (legible-diagrams REGISTER "After closing fixes", 2026-10-23).

Live on Haiku 5.5, S1–S6 went verified 1/6 and repair made diagrams worse: S2 1→11→6, S4 2→28→5,
S5 3→11→3, S6 1→9→8. Each test names the break it catches on the code before this lane:

1. Monotone: a worse round was used as the next round's starting spec (round 3 repaired round 2's 11 errors).
2. Mechanical fixes: a too-small sublabel, a conflicting pin, a ``type: null`` value went to the model (or
   nowhere) although the engine's own evidence determines the fix; ``render/tooSmall`` was shown as one
   diagnostic per text with "shorten this text", which cannot change a size set by the canvas scale.
3. Patches: the model rewrote the whole spec each round and changed items no diagnostic named; a long list
   was handed over whole.
4. D9: a delivered diagram that still leaves out first-draft content said nothing in the turn text.

The engine here is scripted BY SPEC CONTENT (never by call order), so the only way to reach the expected
value is for the loop to send the right spec.
"""

from __future__ import annotations

import asyncio
import contextvars
import json
from collections.abc import Callable
from types import SimpleNamespace
from typing import Any

from matrx_ai.orchestrator import visual_map_repair as vmr
from matrx_ai.orchestrator.visual_map_fixes import (
    apply_patch,
    mechanical_fixes,
    patch_from_whole_spec,
    prompt_diagnostics,
    scale_diagnostic,
)
from matrx_ai.orchestrator.visual_map_repair import CallPointResult, RepairKnobs, run_repair_loop

K4 = RepairKnobs(max_rounds=4, stall_rounds=2, quality="showcase")


def _errs(code: str, n: int, **subject: Any) -> list[dict[str, Any]]:
    return [{"code": code, "severity": "error", "message": f"{code} {i}", "subject": dict(subject),
             "evidence": {}, "supportedFixes": []} for i in range(n)]


class SpecEngine:
    """validate → ``validate_fn(spec)``; a clean spec is delivered and measured by ``measure_fn(spec)``."""

    def __init__(self, validate_fn: Callable[[dict], list], measure_fn: Callable[[dict], list] | None = None,
                 width: float = 1050.0) -> None:
        self.validate_fn = validate_fn
        self.measure_fn = measure_fn or (lambda s: [])
        self.width = width
        self.validated: list[dict[str, Any]] = []
        self.delivered: list[dict[str, Any]] = []

    async def read_knobs(self, *, organization_id, user_id):
        return {}

    async def schema_version(self, type):  # noqa: A002
        return 1

    async def validate(self, type, spec, *, quality):  # noqa: A002
        self.validated.append(json.loads(json.dumps(spec)))
        diags = self.validate_fn(spec)
        return {"ok": not diags, "diagnostics": diags}

    async def deliver(self, type, spec, *, organization_id, subject_ref, round, quality):  # noqa: A002
        self.delivered.append(json.loads(json.dumps(spec)))
        errors = self.validate_fn(spec)
        measured = [] if errors else self.measure_fn(spec)
        return {"ok": not errors, "verified": not errors and not measured, "issues": len(errors) + len(measured),
                "inspection_id": f"insp-{len(self.delivered)}", "receipt": {"viewBox": [0, 0, self.width, 500]},
                "screenshot_file_id": None, "diagnostics": errors, "measured_diagnostics": measured}

    async def persist_round(self, **_):
        return "row"

    async def repair(self, provision, *, organization_id):
        return CallPointResult(bound=False)

    async def review(self, provision, *, organization_id):
        return CallPointResult(bound=False)


def _run(engine, value, fallback, knobs=K4):
    return asyncio.run(run_repair_loop(value, delivery=engine, knobs=knobs, organization_id="org",
                                       subject_ref="request:r#0", user_request="draw it", fallback_repair=fallback))


WORKFLOW = {
    "schema_version": 1, "diagram_type": "workflow", "meta": {"title": "Kit"},
    "nodes": [{"id": "a", "label": "Upload", "sublabel": "your notes"},
              {"id": "b", "label": "Outline"}, {"id": "c", "label": "Pack"}],
    "edges": [{"id": "ab", "from": "a", "to": "b"}, {"id": "bc", "from": "b", "to": "c"}],
}


# ── 1. Monotone ──────────────────────────────────────────────────────────────────────────────────────


def test_a_worse_round_is_never_adopted_and_the_next_round_restarts_from_the_best():
    # The spec's x on node b decides the error count: 1 at the start, 11 after the first (bad) answer,
    # 0 after a good answer. Only an answer applied to the BEST spec (x unset → set 2) reaches 0.
    def validate(spec):
        b = next(n for n in spec["nodes"] if n["id"] == "b")
        return _errs("layout/overlap", {None: 1, 1: 11, 2: 0}.get(b.get("x"), 5), id="b")

    provisions: list[dict[str, Any]] = []

    async def fallback(provision):
        provisions.append(provision)
        x = 1 if len(provisions) == 1 else 2
        return json.dumps({"changes": [{"list": "nodes", "id": "b", "set": {"x": x}}]})

    engine = SpecEngine(validate)
    out = _run(engine, {"__kind": "visual_map", "type": "workflow", "spec": WORKFLOW}, fallback)
    log = out.log()
    assert log["error_counts"] == [1, 11, 0]
    assert log["adopted_counts"] == [1, 1, 0]
    assert all(b <= a for a, b in zip(log["adopted_counts"], log["adopted_counts"][1:]))
    # Round 2's repair started from round 1's spec, not from the 11-error answer, and was told so.
    assert "x" not in next(n for n in provisions[1]["spec"]["nodes"] if n["id"] == "b")
    assert provisions[1]["last_attempt_errors"] == 11
    assert "starting again from the best version" in vmr.repair_notice(provisions[1])
    assert out.verified and engine.delivered[-1]["nodes"][1]["x"] == 2


def test_when_every_answer_is_worse_the_first_spec_is_delivered_and_counts_stay_flat():
    def validate(spec):
        return _errs("layout/overlap", 9 if spec.get("meta", {}).get("title") != "Kit" else 2, id="b")

    async def fallback(provision):
        return json.dumps({"changes": [{"key": "meta", "set": {"title": "Other"}}]})

    engine = SpecEngine(validate)
    out = _run(engine, {"__kind": "visual_map", "type": "workflow", "spec": WORKFLOW}, fallback)
    assert out.log()["adopted_counts"] == [2, 2, 2]
    assert out.stop_reason == "stalled"
    assert engine.delivered[-1]["meta"]["title"] == "Kit" and out.value["issues"] == 2


# ── 2. Mechanical fixes ──────────────────────────────────────────────────────────────────────────────


def _too_small(ident: str, text: str, px: float = 4.7) -> dict[str, Any]:
    return {"code": "render/tooSmall", "severity": "error",
            "message": f'Text "{text}" ({ident}) is drawn at {px}px, below the 6px legibility floor, at the 736:dark capture',
            "subject": {"id": ident}, "evidence": {"px": px, "floor_px": 6, "captures": ["736:dark"]}}


def test_a_too_small_sublabel_moves_into_a_card_without_asking_the_model():
    def measure(spec):
        return [_too_small("node:a#2", n["sublabel"]) for n in spec["nodes"] if n.get("sublabel")]

    calls: list[Any] = []

    async def fallback(provision):
        calls.append(provision)
        return "{}"

    engine = SpecEngine(lambda s: [], measure)
    out = _run(engine, {"__kind": "visual_map", "type": "workflow", "spec": WORKFLOW}, fallback)
    assert out.verified and calls == []
    spec = out.value["spec"]
    assert "sublabel" not in spec["nodes"][0]
    assert spec["cards"] == [{"dot": "emerald", "title": "Details", "items": ["Upload: your notes"]}]
    assert [r.stage for r in out.rounds] == ["validate", "mechanical", "deliver"]


def test_a_conflicting_pin_is_deleted_and_a_suggested_label_spot_is_used():
    spec = {**WORKFLOW, "edges": [{"id": "ab", "from": "a", "to": "b", "route": "outside-right", "label": "notes"},
                                  {"id": "bc", "from": "b", "to": "c"}]}
    diags = [
        {"code": "workflow/explicit-pin-conflict", "severity": "error", "message": "pin", "subject": {"edge": "ab"},
         "evidence": {"conflictingPins": [{"edge": "ab", "path": "/edges/0/route", "field": "route"}]}},
        {"code": "layout/constraint", "severity": "error", "subject": {}, "evidence": {},
         "message": 'Label "notes" overlaps node "b" — adjust.\n  Suggested fix: set labelAt [853, 429] or set labelDx 1'},
    ]
    fixed, edits = mechanical_fixes("workflow", spec, diags)
    assert "route" not in fixed["edges"][0] and fixed["edges"][0]["labelAt"] == [853.0, 429.0]
    assert len(edits) == 2 and "route" in spec["edges"][0]  # the input is never mutated


def test_an_unreadable_legend_is_hidden_and_text_tags_move_too():
    spec = {**WORKFLOW, "nodes": [{"id": "a", "label": "Upload", "tag": "PDF · DOCX"}]}
    fixed, edits = mechanical_fixes("workflow", spec, [_too_small("text:31", "3"), _too_small("node:a#2", "PDF · DOCX")])
    assert fixed["meta"]["legend"] == {"mode": "hidden"} and "tag" not in fixed["nodes"][0]
    assert fixed["cards"][0]["items"] == ["Upload: PDF · DOCX"]
    # A primary label is never moved or cut.
    same, none = mechanical_fixes("workflow", spec, [_too_small("node:a", "Upload")])
    assert same is spec and none == []


def test_a_value_with_type_null_is_read_from_its_spec():
    spec = {"meta": {"title": "RAG"}, "stages": [{"label": "In"}], "nodes": [{"id": "x", "label": "X", "stage": 0}],
            "flows": []}
    engine = SpecEngine(lambda s: [])
    out = _run(engine, {"__kind": "visual_map", "type": None, "spec": spec}, None)
    assert out.stop_reason == "clean" and out.value["type"] == "dataflow"
    assert engine.validated[0]["diagram_type"] == "dataflow"
    assert any("the spec draws stages, flows" in n for n in out.notes)


def test_too_small_texts_become_one_computed_canvas_instruction():
    diags = [_too_small(f"edge:a->b#{i}", f"label {i}", px=4.83) for i in range(9)] + [_too_small("node:c", "C", 5.9)]
    scale = scale_diagnostic(diags, 1050.0)
    assert scale["evidence"]["max_canvas_width"] == 845  # 1050 x 4.83 / 6
    assert "845" in scale["supportedFixes"][0] and scale["evidence"]["texts"] == 10
    shown, group = prompt_diagnostics(diags, canvas_width=1050.0, group_max=6)
    assert [d["code"] for d in shown] == ["render/scale"] and group == "render/scale"


# ── 3. Patches and groups ────────────────────────────────────────────────────────────────────────────


def test_a_long_list_goes_to_the_model_one_group_at_a_time():
    diags = _errs("composition/ambiguous-corridor", 7, id="ab") + _errs("layout/overlap", 3, id="b")
    shown, group = prompt_diagnostics(diags, canvas_width=None, group_max=6)
    assert group == "composition/ambiguous-corridor" and {d["code"] for d in shown} == {group}
    assert len(shown) == 6
    few, none = prompt_diagnostics(diags[:5], canvas_width=None, group_max=6)
    assert none is None and len(few) == 5


def test_a_patch_changes_only_the_named_items_of_the_best_spec():
    out, applied, refused = apply_patch(WORKFLOW, [
        {"list": "nodes", "id": "b", "set": {"label": "Outline it", "id": "zz"}, "unset": ["label"]},
        {"list": "edges", "add": {"id": "ac", "from": "a", "to": "c"}},
        {"key": "diagram_type", "set": {"x": 1}},
    ])
    assert out["nodes"][1] == {"id": "b", "label": "Outline it"}  # id kept, label never unset
    assert out["nodes"][0] == WORKFLOW["nodes"][0] and len(out["edges"]) == 3
    assert any("id cannot change" in r for r in refused) and any("diagram_type" in r for r in refused)
    assert WORKFLOW["nodes"][1] == {"id": "b", "label": "Outline"}  # the best spec is never mutated


def test_a_whole_spec_answer_keeps_only_changes_to_named_items():
    answer = json.loads(json.dumps(WORKFLOW))
    answer["nodes"][1]["x"] = 300            # named by the diagnostic: kept
    answer["nodes"][2]["label"] = "Packed"   # named by nothing: reverted
    del answer["nodes"][0]                   # removal: never applied
    changes, reverted = patch_from_whole_spec(WORKFLOW, answer, _errs("layout/overlap", 1, id="b"))
    out, _, _ = apply_patch(WORKFLOW, changes)
    assert [n["id"] for n in out["nodes"]] == ["a", "b", "c"]
    assert out["nodes"][1]["x"] == 300 and out["nodes"][2]["label"] == "Pack"
    assert reverted == ["nodes/c"]


def test_the_model_is_asked_for_a_patch_not_a_whole_spec():
    text = vmr.repair_notice({"round": 1, "max_rounds": 4, "diagnostics": _errs("layout/overlap", 1, id="b")})
    assert '{"changes": [' in text and "Never remove an item" in text
    assert '"__kind": "visual_map", "type": ...' not in text


# ── 4. D9: what is not drawn is said ─────────────────────────────────────────────────────────────────


def test_the_turn_text_says_what_the_delivered_diagram_does_not_draw(monkeypatch):
    from matrx_connect.context.app_context import AppContext, set_app_context
    from matrx_connect.emitters import SilentEmitter

    import matrx_ai._ext as ext

    draft = {"schema_version": 1, "diagram_type": "lifecycle",
             "states": [{"label": "Queued"}, {"label": "Pausing"}], "transitions": []}
    part = SimpleNamespace(text="Here it is:\n" + json.dumps({"__kind": "visual_map", "type": "lifecycle", "spec": draft}),
                           metadata={})
    monkeypatch.setattr(vmr, "_assistant_text_parts", lambda *_: [part])

    async def relabel(provision):
        return '{"changes": [{"list": "states", "index": 1, "set": {"label": "Pause"}}]}'

    monkeypatch.setattr(vmr, "authoring_model_repairer", lambda _req: relabel)

    def validate(spec):
        return [] if spec["states"][1]["label"] == "Pause" else _errs("layout/overlap", 3)

    class Emitter:
        async def send_info(self, payload):
            pass

        async def send_warning(self, payload):
            pass

    def _in_ctx():
        set_app_context(AppContext(emitter=SilentEmitter(), user_id="u", organization_id="org", request_id="req"))
        ext._registry["visual_map_delivery"] = SpecEngine(validate)
        try:
            request = SimpleNamespace(config=SimpleNamespace(messages=[]), request_id="req")
            return asyncio.run(vmr.visual_map_gate(request, None, SimpleNamespace(emitter=Emitter())))
        finally:
            ext._registry.pop("visual_map_delivery", None)

    outcomes = contextvars.copy_context().run(_in_ctx)
    assert outcomes and outcomes[0].verified is False and outcomes[0].dropped == ["Pausing"]
    assert part.text.rstrip().endswith("Not drawn in this diagram: Pausing.")
    assert part.text.count("Not drawn in this diagram") == 1


def test_an_unsupported_property_and_an_impossible_route_preset_are_removed():
    spec = {**WORKFLOW, "legend": {"mode": "hidden"},
            "edges": [{"id": "ab", "from": "a", "to": "b", "route": "up-channel", "fromSide": "right", "label": "go"}]}
    diags = [
        {"code": "schema/additionalProperties", "severity": "error", "message": "/ must NOT have additional properties",
         "subject": {"path": "/"}, "evidence": {"additionalProperty": "legend"}},
        {"code": "workflow/route-preset-conflict", "severity": "error", "message": "cannot satisfy route preset",
         "subject": {"edge": "ab"}, "evidence": {}},
    ]
    fixed, edits = mechanical_fixes("workflow", spec, diags)
    assert "legend" not in fixed and fixed["edges"][0] == {"id": "ab", "from": "a", "to": "b", "label": "go"}
    assert len(edits) == 2


def test_a_patch_may_replace_a_grouping_list_and_regrouping_is_not_dropping():
    spec = {"schema_version": 1, "diagram_type": "dataflow", "stages": [{"label": s} for s in "ABCDEF"],
            "nodes": [{"id": "n", "label": "N", "stage": 5}], "flows": []}
    out, applied, refused = apply_patch(spec, [
        {"key": "stages", "value": [{"label": "A+B"}, {"label": "C"}, {"label": "D"}, {"label": "E"}, {"label": "F"}]},
        {"list": "nodes", "id": "n", "set": {"stage": 4}},
    ])
    assert len(out["stages"]) == 5 and out["nodes"][0]["stage"] == 4 and refused == []
    assert vmr.dropped_content(vmr.content_inventory(spec), out) == []


def test_a_misnamed_required_list_is_renamed_never_deleted():
    spec = {"schema_version": 1, "diagram_type": "dataflow", "stages": [], "nodes": [{"id": "a"}, {"id": "b"}],
            "edges": [{"from": "a", "to": "b", "label": "rows"}]}
    diags = [
        {"code": "schema/required", "severity": "error", "message": "/ must have required property 'flows'",
         "subject": {"path": "/"}, "evidence": {"missingProperty": "flows"}},
        {"code": "schema/additionalProperties", "severity": "error", "message": "/ must NOT have additional properties",
         "subject": {"path": "/"}, "evidence": {"additionalProperty": "edges"}},
    ]
    fixed, edits = mechanical_fixes("dataflow", spec, diags)
    assert fixed["flows"] == [{"from": "a", "to": "b", "label": "rows"}] and "edges" not in fixed
    assert edits == ["renamed edges to flows (the list this diagram type requires)"]


def test_a_malformed_patch_entry_is_refused_not_raised():
    out, applied, refused = apply_patch(WORKFLOW, [{"list": "nodes", "id": "b", "unset": True, "set": "x"}])
    assert out["nodes"][1] == WORKFLOW["nodes"][1]


def test_a_corridor_conflict_drops_hand_set_routing_on_both_named_relationships():
    spec = {**WORKFLOW, "edges": [{"id": "ab", "from": "a", "to": "b", "route": "bottom-channel", "bias": 0.2},
                                  {"id": "bc", "from": "b", "to": "c", "channelX": 400}]}
    diag = {"code": "composition/ambiguous-corridor", "severity": "error", "message": "shares a corridor",
            "subject": {"id": "ab", "collection": "edges", "index": 0},
            "evidence": {"otherRelationship": {"id": "bc", "collection": "edges", "index": 1}}}
    fixed, edits = mechanical_fixes("workflow", spec, [diag])
    assert fixed["edges"] == [{"id": "ab", "from": "a", "to": "b"}, {"id": "bc", "from": "b", "to": "c"}]
    assert len(edits) == 2


def test_the_repair_model_knob_picks_the_childs_model_and_empty_keeps_the_authoring_one():
    cfg = SimpleNamespace(model="haiku-id")
    vmr._repair_model(cfg, {"repair_model": None})
    assert cfg.model == "haiku-id"
    vmr._repair_model(cfg, {"repair_model": " sonnet-id "})
    assert cfg.model == "sonnet-id"


def test_delivery_counts_each_defect_once_like_the_loop_did():
    class PerCapture(SpecEngine):
        async def deliver(self, type, spec, **kw):  # noqa: A002
            out = await super().deliver(type, spec, **kw)
            return {**out, "issues": out["issues"] * 2}  # one count per width x theme capture

    engine = PerCapture(lambda s: [], lambda s: [_too_small("edge:a->b#0", "rows"), _too_small("edge:b->c#1", "pack")])
    out = _run(engine, {"__kind": "visual_map", "type": "workflow", "spec": WORKFLOW}, None)
    assert out.value["issues"] == 2 and out.rounds[-1].error_count == 2


def test_mechanical_fixes_walk_one_reported_conflict_after_another():
    """The engine reports one impossible route preset at a time; clearing it reveals the next (S3/S6)."""
    spec = {**WORKFLOW, "edges": [{"id": "ab", "from": "a", "to": "b", "route": "up-channel"},
                                  {"id": "bc", "from": "b", "to": "c", "route": "bottom-channel"}]}

    def validate(s):
        pinned = [e["id"] for e in s["edges"] if e.get("route")]
        return [{"code": "workflow/route-preset-conflict", "severity": "error",
                 "message": f"edge {pinned[0]} cannot satisfy its preset", "subject": {"edge": pinned[0]}}] if pinned else []

    out = _run(SpecEngine(validate), {"__kind": "visual_map", "type": "workflow", "spec": spec}, None)
    assert out.verified and [r.stage for r in out.rounds] == ["validate", "mechanical", "mechanical", "deliver"]
    assert out.log()["adopted_counts"] == [1, 1, 0]


def test_a_sublabel_wider_than_its_node_moves_into_a_card():
    # 2026-10-23 live S6 (Haiku): the engine refused with layout/constraint naming the node only in the
    # message, so no mechanical fix applied and the picture was "could not be drawn".
    spec = {"lanes": [{"id": "l", "label": "L"}], "nodes": [
        {"id": "read", "lane": "l", "col": 0, "type": "backend", "label": "Read", "sublabel": "Paste text, attach a file, or share a link"},
    ], "edges": []}
    diagnostics = [{"code": "layout/constraint", "severity": "error", "subject": {}, "evidence": {},
                    "message": 'Workflow layout validation failed: Sublabel "Paste text, attach a file, or share a link" needs ~252px at the 6px legible minimum, but node "read" provides 192px — shorten the sublabel or increase node.width.'}]
    fixed, edits = mechanical_fixes("workflow", spec, diagnostics)
    assert "sublabel" not in fixed["nodes"][0]
    assert fixed["cards"][0]["items"] == ["Read: Paste text, attach a file, or share a link"]
    assert len(edits) == 1
