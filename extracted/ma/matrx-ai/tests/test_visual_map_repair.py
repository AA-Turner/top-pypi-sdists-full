"""The visual-map repair loop's stop rules, knob reads and stamping (legible-diagrams L4).

Each test names the naive loop it catches: one that always runs to the round ceiling, one that
ignores the knob rows, one that trusts the model's own ``verified``, one that delivers the last spec
instead of the best, one that lets a review pass a diagram.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from matrx_ai.orchestrator import visual_map_repair as vmr
from matrx_ai.orchestrator.visual_map_repair import (
    CallPointResult,
    RepairKnobs,
    knobs_from,
    run_repair_loop,
    stop_reason,
)

SPEC = {"schema_version": 1, "diagram_type": "sequence", "meta": {"title": "t"}, "participants": [], "messages": []}


def _err(n: int) -> list[dict[str, Any]]:
    return [{"code": f"layout/e{i}", "severity": "error", "message": "x", "subject": {}, "evidence": {},
             "supportedFixes": []} for i in range(n)]


class FakeDelivery:
    """A scripted engine: ``counts[i]`` errors on the i-th validate."""

    def __init__(self, counts: list[int], *, bound_repair: bool = False, review: CallPointResult | None = None,
                 deliver: dict[str, Any] | None = None, knobs: dict[str, Any] | None = None) -> None:
        self.counts = list(counts)
        self.validated: list[dict[str, Any]] = []
        self.persisted: list[int] = []
        self.repairs: list[dict[str, Any]] = []
        self.delivered: list[tuple[dict[str, Any], int]] = []
        self.bound_repair = bound_repair
        self._review = review or CallPointResult(bound=False)
        self._deliver = deliver
        self._knobs = knobs or {}

    async def read_knobs(self, *, organization_id, user_id):
        return self._knobs

    async def validate(self, type, spec, *, quality):
        i = len(self.validated)
        self.validated.append(spec)
        return {"ok": self.counts[i] == 0, "diagnostics": _err(self.counts[i])}

    async def deliver(self, type, spec, *, organization_id, subject_ref, round, quality):
        self.delivered.append((spec, round))
        if self._deliver is not None:
            return self._deliver
        errors = self.counts[self.validated.index(spec)] if spec in self.validated else 0
        return {"ok": True, "receipt": {"type": type}, "inspection_id": "insp-1", "verified": errors == 0,
                "issues": errors, "screenshot_file_id": "file-1", "diagnostics": _err(errors)}

    async def persist_round(self, *, organization_id, subject_ref, round, spec, diagnostics):
        self.persisted.append(round)
        return f"row-{round}"

    async def repair(self, provision, *, organization_id):
        self.repairs.append(provision)
        if self.bound_repair:
            return CallPointResult(bound=True, value={"__kind": "visual_map", "type": "sequence",
                                                      "spec": {**SPEC, "meta": {"title": f"r{len(self.repairs)}"}}})
        return CallPointResult(bound=False, snapshot_id=f"snap-{provision['round']}")

    async def review(self, provision, *, organization_id):
        return self._review


def _fallback(calls: list[dict[str, Any]]):
    async def _repair(provision):
        calls.append(provision)
        return {"__kind": "visual_map", "type": "sequence",
                "spec": {**SPEC, "meta": {"title": f"m{len(calls)}"}}, "verified": True}
    return _repair


def _run(delivery: FakeDelivery, knobs: RepairKnobs, fallback=None):
    return asyncio.run(run_repair_loop(
        {"__kind": "visual_map", "type": "sequence", "spec": SPEC, "verified": True, "issues": 0},
        delivery=delivery, knobs=knobs, organization_id="org", subject_ref="request:r#0",
        user_request="draw the chat flow", fallback_repair=fallback,
    ))


K4 = RepairKnobs(max_rounds=4, stall_rounds=2, quality="showcase")


def test_stops_when_errors_do_not_fall_for_two_rounds():
    """Naive loop: always runs to max_rounds. Here errors stay at 3, so it must stop after round 3."""
    calls: list[dict[str, Any]] = []
    d = FakeDelivery([3, 3, 3, 3, 3])
    out = _run(d, K4, _fallback(calls))
    assert out.stop_reason == "stalled"
    assert len(d.validated) == 3
    assert len(calls) == 2


def test_stops_clean_at_first_zero_and_delivers_that_round():
    calls: list[dict[str, Any]] = []
    d = FakeDelivery([2, 1, 0, 0])
    out = _run(d, K4, _fallback(calls))
    assert out.stop_reason == "clean"
    assert len(d.validated) == 3
    assert d.delivered[-1][1] == 3  # the last round calls deliver
    assert d.persisted == [1, 2]  # earlier rounds are diagnostics-only rows
    assert out.value["verified"] is True and out.value["issues"] == 0
    assert out.value["inspection_id"] == "insp-1"


def test_round_knob_from_the_host_is_obeyed():
    """Naive loop: hard-coded 4 rounds. The knob row says 2."""
    knobs, missing = knobs_from({"repair_max_rounds": 2, "repair_stall_rounds": 5, "quality": "standard",
                                 "repair_group_max": 3, "repair_model": ""})
    assert knobs == RepairKnobs(2, 5, "standard", 3, "") and missing == []
    calls: list[dict[str, Any]] = []
    d = FakeDelivery([5, 4, 3, 2, 1])
    out = _run(d, knobs, _fallback(calls))
    assert out.stop_reason == "max_rounds"
    assert len(d.validated) == 2 and len(calls) == 1


def test_missing_knob_rows_are_named_not_silent():
    knobs, missing = knobs_from({"repair_max_rounds": 3})
    assert knobs.max_rounds == 3
    assert knobs.stall_rounds == vmr.DECLARED_KNOBS.stall_rounds
    assert set(missing) == {"repair_stall_rounds", "quality", "repair_group_max", "repair_model"}


def test_unbound_repair_falls_back_to_the_authoring_model_and_bound_agent_wins():
    calls: list[dict[str, Any]] = []
    d = FakeDelivery([2, 0])
    out = _run(d, K4, _fallback(calls))
    assert out.rounds[0].repaired_by == "authoring_model" and len(calls) == 1
    assert out.rounds[0].repair_snapshot_id == "snap-1"
    provision = d.repairs[0]
    for name in ("user_request", "spec", "diagnostics", "measurements", "receipt", "round", "prior_rounds"):
        assert name in provision
    calls2: list[dict[str, Any]] = []
    d2 = FakeDelivery([2, 0], bound_repair=True)
    out2 = _run(d2, K4, _fallback(calls2))
    assert out2.rounds[0].repaired_by == "agent" and calls2 == []


def test_delivers_the_best_spec_not_the_last():
    """Naive loop: delivers whatever the last repair wrote, even when it got worse."""
    calls: list[dict[str, Any]] = []
    d = FakeDelivery([3, 1, 2, 2, 2])
    out = _run(d, RepairKnobs(6, 2, "showcase"), _fallback(calls))
    assert out.stop_reason == "stalled"
    assert d.delivered[-1][0] == d.validated[1]
    assert out.value["issues"] == 1


def test_model_never_stamps_verified_and_review_cannot_pass():
    # The model wrote verified=True; the engine says 2 errors after the round knob.
    calls: list[dict[str, Any]] = []
    d = FakeDelivery([2, 2], deliver={"ok": True, "receipt": {}, "inspection_id": "i", "verified": False,
                                      "issues": 2, "screenshot_file_id": "f"})
    out = _run(d, RepairKnobs(2, 2, "showcase"), _fallback(calls))
    assert out.value["verified"] is False and out.value["issues"] == 2
    # A bound review can add findings and fail a clean diagram — never pass one.
    review = CallPointResult(bound=True, value={"findings": [{"severity": "error", "message": "unreadable"}]})
    d2 = FakeDelivery([0], review=review)
    out2 = _run(d2, K4, None)
    assert out2.value["verified"] is False and out2.value["issues"] == 1
    # Unbound review is skipped and the round log says so.
    out3 = _run(FakeDelivery([0]), K4, None)
    assert out3.value["verified"] is True
    assert any("review skipped" in n for n in out3.notes)


def test_service_down_is_honest():
    class Down(FakeDelivery):
        async def validate(self, type, spec, *, quality):
            return {"ok": False, "verified": False, "unavailable": True}

    out = _run(Down([0]), K4, None)
    assert out.stop_reason == "unavailable"
    assert out.value["verified"] is False and "receipt" not in out.value


@pytest.mark.parametrize(
    ("counts", "expected"),
    [([0], "clean"), ([3], None), ([3, 2], None), ([3, 3, 3], "stalled"), ([3, 2, 2], None),
     ([3, 2, 2, 2], "max_rounds"), ([4, 3, 2, 1], "max_rounds")],
)
def test_stop_rule_table(counts, expected):
    assert stop_reason(counts, K4) == expected


def test_corrector_neutralizes_model_stamps_and_keeps_server_ones():
    model_value = {"__kind": "visual_map", "type": "tree", "spec": {}, "verified": True, "issues": 0,
                   "inspection_id": "fake"}
    fixed, notes = vmr.neutralize_model_stamps(model_value)
    assert fixed["verified"] is False and "inspection_id" not in fixed and notes
    server = {"__kind": "visual_map", "type": "tree", "spec": {}, "verified": True, "issues": 0,
              "inspection_id": "real"}

    def _in_ctx():
        vmr.mark_server_stamped(server)
        return vmr.neutralize_model_stamps(server)

    import contextvars

    same, notes2 = contextvars.copy_context().run(_in_ctx)
    assert same is server and notes2 == []


def test_finds_visual_map_in_fenced_and_bare_text():
    text = 'Here:\n```json\n{"__kind": "visual_map", "type": "tree", "spec": {"a": 1}, "verified": false, "issues": 0}\n```\n'
    found = vmr.find_visual_maps(text)
    assert len(found) == 1 and found[0][2]["type"] == "tree"
    assert vmr.coerce_visual_map(text, "tree") == ("tree", {"a": 1})


def test_gate_never_runs_inside_its_own_repair_child(monkeypatch):
    """Naive gate: the repair child's answer is a visual_map, so the gate re-ran the whole loop inside it."""
    from matrx_connect.context.app_context import AppContext, set_app_context

    calls: list[str] = []

    class Spy:
        def __getattr__(self, name):
            calls.append(name)
            raise AssertionError("delivery must not be touched inside a repair child")

    from types import SimpleNamespace

    import matrx_ai._ext as ext

    part = SimpleNamespace(text='{"__kind": "visual_map", "type": "tree", "spec": {"a": 1}, "verified": false, "issues": 0}',
                           metadata={})
    monkeypatch.setattr(vmr, "_assistant_text_parts", lambda *_: [part])

    def _in_ctx():
        from matrx_connect.emitters import SilentEmitter
        set_app_context(AppContext(emitter=SilentEmitter(), user_id="u", metadata={vmr.REPAIR_CHILD_KEY: True}))
        ext._registry["visual_map_delivery"] = Spy()
        try:
            return asyncio.run(vmr.visual_map_gate(None, None, None))
        finally:
            ext._registry.pop("visual_map_delivery", None)

    import contextvars

    assert contextvars.copy_context().run(_in_ctx) == [] and calls == []
    assert '"verified": false' in part.text  # untouched


# ── The repair notice (2026-10-21 live stall: S2 on Haiku went [23, 16, 16, 16]) ──────────────────


def _diag(i: int) -> dict[str, Any]:
    return {"code": "schema/minimum", "severity": "error", "message": f"/messages/{i}/y must be >= 160",
            "subject": {"diagramType": "sequence", "path": f"/messages/{i}/y", "identity": f"m{i}"},
            "evidence": {"keyword": "minimum", "limit": 160, "value": i},
            "supportedFixes": [f"set y of m{i} to at least 160"]}


def test_notice_carries_every_error_whole_and_says_change_only_these():
    # A naive notice truncates the list, drops subject/evidence/supportedFixes, or forbids the very
    # field the schema requires ("never by adding coordinates" vs a required sequence `y`).
    diags = [_diag(i) for i in range(30)] + [{"code": "w", "severity": "warning", "message": "warn"}]
    text = vmr.repair_notice({"round": 2, "max_rounds": 4, "diagnostics": diags})
    assert "30 error(s) and 1 warning(s)" in text
    for i in range(30):
        assert f"/messages/{i}/y must be >= 160" in text
        assert f'"path": "/messages/{i}/y"' in text
        assert f"set y of m{i} to at least 160" in text
    assert '"limit": 160' in text
    assert "Change ONLY the fields they name" in text
    assert "coordinates" not in text


def test_notice_attaches_the_types_card_and_names_a_stall():
    prior = [{"round": 1, "stage": "validate", "error_count": 16}]
    text = vmr.repair_notice({"round": 2, "max_rounds": 4, "diagnostics": [_diag(0)] * 16, "prior_rounds": prior,
                              "authoring_card": "Rules for a sequence spec:\n- messages[]: required y (number >= 160)"})
    assert "Rules for a sequence spec" in text and "required y (number >= 160)" in text
    assert "round 1: 16 errors" in text and "did not reduce the errors" in text
    assert text.rstrip().endswith("No prose.")


def test_loop_hands_the_hosts_card_to_every_repair_round():
    class CardDelivery(FakeDelivery):
        async def authoring_card(self, type):
            return f"card for {type}"

    calls: list[dict[str, Any]] = []
    d = CardDelivery([3, 2, 0])
    asyncio.run(run_repair_loop({"type": "sequence", "spec": SPEC}, delivery=d, knobs=RepairKnobs(4, 2, "showcase"),
                                organization_id="o", subject_ref="s", user_request="u", fallback_repair=_fallback(calls)))
    assert [p["authoring_card"] for p in calls] == ["card for sequence", "card for sequence"]
    # A host without cards still repairs; the notice just has no card.
    calls.clear()
    asyncio.run(run_repair_loop({"type": "sequence", "spec": SPEC}, delivery=FakeDelivery([3, 0]),
                                knobs=RepairKnobs(4, 2, "showcase"), organization_id="o", subject_ref="s",
                                user_request="u", fallback_repair=_fallback(calls)))
    assert calls[0]["authoring_card"] is None


def test_repair_child_thinks_little_and_has_room_to_write():
    # 2026-10-21: the child inherited the run's 8,000-token limit and adaptive thinking, spent it all
    # thinking, and answered nothing. A naive copy of the parent config keeps both.
    from types import SimpleNamespace

    cfg = SimpleNamespace(reasoning_effort=None, thinking_budget=9000, thinking_level="high", max_output_tokens=8000)
    vmr._repair_budget(cfg)
    assert cfg.reasoning_effort == "low" and cfg.thinking_budget is None and cfg.thinking_level is None
    assert cfg.max_output_tokens == vmr.REPAIR_MIN_OUTPUT_TOKENS
    big = SimpleNamespace(reasoning_effort="high", max_output_tokens=64000)
    vmr._repair_budget(big)
    assert big.max_output_tokens == 64000 and big.reasoning_effort == "low"


def test_notice_marks_errors_the_last_change_caused():
    # 2026-10-21 live: S2 went 29 -> 3 -> 3 -> 3 with DIFFERENT errors each round (each local move hit a
    # neighbour). A notice that only shows counts cannot tell the model its fix caused the new ones.
    old = {"code": "layout/constraint", "severity": "error", "message": "segment edge runs along m6"}
    new = {"code": "layout/constraint", "severity": "error", "message": "m19 and m20 are less than 28px apart"}
    text = vmr.repair_notice({"round": 3, "max_rounds": 4, "diagnostics": [old, new], "previous_errors": [old]})
    assert "1 of these errors are NEW" in text
    assert "2. NEW [layout/constraint] m19 and m20" in text and "1. [layout/constraint] segment edge" in text
    assert "NEW" not in vmr.repair_notice({"round": 1, "max_rounds": 4, "diagnostics": [old]})


def test_a_pin_conflict_without_fixes_is_told_to_delete_the_pin():
    d = {"code": "workflow/explicit-pin-conflict", "severity": "error", "message": "edge read-kit pin conflict",
         "evidence": {"conflictingPins": [{"edge": "read-kit", "field": "channelX", "path": "/edges/3/channelX"}]}}
    text = vmr.repair_notice({"round": 1, "max_rounds": 4, "diagnostics": [d]})
    assert "supported fixes: delete /edges/3/channelX and let the engine route it" in text


def test_measured_defects_on_a_clean_spec_are_repaired_not_shipped():
    # 2026-10-21 S1: validate went [1, 0] (clean), the measured render had 4 clipped labels, and the
    # loop delivered it unverified with rounds left. A naive loop stops at the first clean validate.
    clipped = {"code": "render/clipped", "severity": "error", "message": 'Text "long sublabel" is clipped',
               "subject": {"id": "node:a#2"}, "evidence": {"captures": ["1440:dark"]},
               "supportedFixes": ["shorten this text"]}

    class MeasuredDelivery(FakeDelivery):
        async def deliver(self, type, spec, *, organization_id, subject_ref, round, quality):
            self.delivered.append((spec, round))
            bad = spec.get("meta", {}).get("title") == "t"  # the first draft clips; the repair does not
            return {"ok": True, "receipt": {"type": type}, "inspection_id": f"insp-{round}", "verified": not bad,
                    "issues": 2 if bad else 0, "screenshot_file_id": "file-1", "diagnostics": [],
                    "measured_diagnostics": [clipped, clipped] if bad else []}

    calls: list[dict[str, Any]] = []
    d = MeasuredDelivery([0, 0])
    out = _run(d, K4, _fallback(calls))
    assert out.verified and out.stop_reason == "clean"
    assert [r.error_count for r in out.rounds if r.stage == "validate"] == [2, 0]
    assert calls and calls[0]["diagnostics"][0]["code"] == "render/clipped"
    assert d.persisted == []  # a delivered round is its own ledger row; no second diagnostics-only row
    assert len(d.delivered) == 2  # each distinct spec rendered once, the final one reused


def test_the_repair_child_gets_a_new_config_and_the_run_keeps_its_own(monkeypatch):
    """The child call is built as a NEW config (three messages, no tools); the parent run's config and
    message list are never rewritten (the send-boundary guard keeps that seam closed)."""
    import contextvars
    from types import SimpleNamespace

    from matrx_connect.context.app_context import AppContext, set_app_context
    from matrx_connect.emitters import SilentEmitter

    from matrx_ai.config.message_config import MessageList, UnifiedMessage
    from matrx_ai.config.unified_config import UnifiedConfig
    from matrx_ai.config.unified_content import TextContent
    from matrx_ai.orchestrator import executor

    parent_messages = MessageList([UnifiedMessage(role="user", content=[TextContent(text="draw it")])])
    parent = UnifiedConfig(model="m", messages=parent_messages, tools=["web_search"], tool_choice="auto")
    seen: dict[str, Any] = {}

    async def fake_execute(config, **_kw):
        seen["config"] = config
        return SimpleNamespace(final_response=None)

    monkeypatch.setattr(executor, "execute_ai_request", fake_execute)
    monkeypatch.setattr(executor, "_assistant_text_from_response", lambda _r: "")

    def _in_ctx():
        set_app_context(AppContext(emitter=SilentEmitter(), user_id="u"))
        repair = vmr.authoring_model_repairer(SimpleNamespace(config=parent))
        return asyncio.run(repair({"user_request": "draw it", "round": 1}))

    contextvars.copy_context().run(_in_ctx)
    child = seen["config"]
    assert child is not parent and child.messages is not parent_messages
    assert len(child.messages) == 3 and child.tools == [] and child.tool_choice is None
    assert parent.messages is parent_messages and len(parent_messages) == 1
    assert parent.tools == ["web_search"] and parent.tool_choice == "auto"
