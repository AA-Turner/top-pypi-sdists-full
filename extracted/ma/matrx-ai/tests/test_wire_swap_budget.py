"""Layer-2 wire-swap budget backstop (2026-07-07).

``build_wire_config`` is the ONE seam where referenced fence values expand into
the provider payload, and it runs on EVERY loop iteration — so an oversized
referenced value is re-billed to the model on every send (the tool-result
size-gate cost-bomb class, at the reference seam). The aidream host budgets
fence swaps at STAGING time (Layer 1); this is the independent Layer-2 backstop
at the materialization seam that fires even when Layer 1 is bypassed/broken.

Pins:
  * an oversized SINGLE fence value → truncated + exactly one alarm;
  * total over budget across several fences → truncated + one alarm;
  * everything under budget → untouched, no alarm;
  * picklist (non-fence) swaps are EXEMPT from truncation (server-minted short
    tokens, never a cost bomb).
"""

from __future__ import annotations

import pytest

from matrx_ai.config import picklist_runtime as pr
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.picklist_runtime import (
    WIRE_SWAP_SINGLE_VALUE_MAX_CHARS,
    WIRE_SWAP_TOTAL_MAX_CHARS,
    WireSwapBudgetEvent,
    build_wire_config,
    redact_wire_payload,
    set_wire_swaps,
)
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent

_FENCE_A = '```matrx\n{"kind":"reference","items":[{"key":"a"}]}\n```'
_FENCE_B = '```matrx\n{"kind":"reference","items":[{"key":"b"}]}\n```'
_FENCE_C = '```matrx\n{"kind":"reference","items":[{"key":"c"}]}\n```'


@pytest.fixture()
def sink_events(monkeypatch):
    """Inject a fake budget sink and capture its firings (no DB)."""
    events: list[WireSwapBudgetEvent] = []
    monkeypatch.setattr(pr, "_WIRE_SWAP_BUDGET_SINKS", [events.append])
    return events


def _cfg(*fences: str) -> UnifiedConfig:
    body = " ".join(f"use {f}" for f in fences)
    return UnifiedConfig(
        model="test-model",
        messages=[UnifiedMessage(role="user", content=[TextContent(text=body)])],
    )


def _user_text(config) -> str:
    return config.messages[0].content[0].text


def test_oversized_single_value_truncated_and_one_alarm(sink_events):
    big = "X" * (WIRE_SWAP_SINGLE_VALUE_MAX_CHARS + 5000)
    set_wire_swaps({_FENCE_A: big})
    try:
        wire = build_wire_config(_cfg(_FENCE_A))
        assert wire is not None
        text = _user_text(wire)
        # The fence expanded (it is not left verbatim)…
        assert _FENCE_A not in text
        # …but the materialized value is capped, not the full oversized blob.
        assert len(text) < len(big)
        assert "value truncated by the per-send wire-swap budget" in text
        # Exactly one alarm, naming the single-value cap.
        assert len(sink_events) == 1
        evt = sink_events[0]
        assert evt.truncated_count == 1
        assert "single_value_capped" in evt.reasons
        assert evt.largest_value_chars == len(big)
    finally:
        set_wire_swaps({})


def test_total_over_budget_across_several_fences_alarms(sink_events):
    # Each value is comfortably UNDER the single cap, but together they blow the
    # TOTAL budget — this isolates the total-budget branch from the single-value
    # branch (a bug where total fires only after single-capping would slip past a
    # test whose values also trip the single cap).
    each = (WIRE_SWAP_TOTAL_MAX_CHARS // 3) + 50_000
    assert each < WIRE_SWAP_SINGLE_VALUE_MAX_CHARS  # guard: pure total-budget case
    set_wire_swaps({_FENCE_A: "A" * each, _FENCE_B: "B" * each, _FENCE_C: "C" * each})
    try:
        wire = build_wire_config(_cfg(_FENCE_A, _FENCE_B, _FENCE_C))
        assert wire is not None
        text = _user_text(wire)
        # A fine value squeezed by the TOTAL budget is SKIPPED (left verbatim),
        # never mangled — its ```matrx fence survives intact in the wire text.
        assert _FENCE_C in text
        # Nothing was TRUNCATED (all values were under the single cap).
        assert "value truncated by the per-send wire-swap budget" not in text
        assert len(sink_events) == 1
        evt = sink_events[0]
        assert "total_budget_capped" in evt.reasons
        # The single-value cap must NOT have fired — this is the pure total case.
        assert "single_value_capped" not in evt.reasons
        assert evt.truncated_count == 0
        assert evt.skipped_count >= 1
        assert evt.fence_swap_count == 3
    finally:
        set_wire_swaps({})


def test_under_budget_untouched_no_alarm(sink_events):
    small = "hello world " * 100
    set_wire_swaps({_FENCE_A: small})
    try:
        wire = build_wire_config(_cfg(_FENCE_A))
        assert wire is not None
        text = _user_text(wire)
        assert small in text
        assert "value truncated" not in text
        assert sink_events == []
    finally:
        set_wire_swaps({})


def test_picklist_tokens_exempt_from_budget(sink_events):
    # A picklist token value larger than the single cap is server-minted and must
    # NEVER be truncated by the fence budget (it is not a fence-shaped key).
    token = "⁣matrx:picklist:huge⁣"
    big = "P" * (WIRE_SWAP_SINGLE_VALUE_MAX_CHARS + 1000)
    set_wire_swaps({token: big})
    try:
        cfg = UnifiedConfig(
            model="test-model",
            messages=[UnifiedMessage(role="assistant", content=[TextContent(text=f"ctx {token}")])],
        )
        wire = build_wire_config(cfg)
        assert wire is not None
        # Full value substituted — no truncation, no alarm.
        assert big in wire.messages[0].content[0].text
        assert sink_events == []
    finally:
        set_wire_swaps({})


def test_materialized_total_never_exceeds_budget_bug_repro(sink_events):
    # Regression for the 2026-07-07 adversarial finding: two oversized giants
    # exhaust the total budget, then a tiny value sorts last. The tiny value must
    # be SKIPPED verbatim (not nuked to a fetch-notice that GROWS it and pushes
    # the materialized total OVER the ceiling). Pins two invariants at once:
    # (a) total materialized fence bytes never exceed WIRE_SWAP_TOTAL_MAX_CHARS;
    # (b) truncation only ever reduces bytes — a small value never grows.
    giant = "G" * (WIRE_SWAP_SINGLE_VALUE_MAX_CHARS + 500_000)  # 1.5M, over single cap
    small = "s" * 50
    out = pr._apply_wire_swap_budget({_FENCE_A: giant, _FENCE_B: giant, _FENCE_C: small})

    # The small value is skipped (key dropped → fence stays verbatim), NOT grown.
    assert _FENCE_C not in out
    # Both giants truncated within the single cap…
    assert len(out[_FENCE_A]) <= WIRE_SWAP_SINGLE_VALUE_MAX_CHARS
    assert len(out[_FENCE_B]) <= WIRE_SWAP_SINGLE_VALUE_MAX_CHARS
    # …and the total materialized fence bytes never exceed the per-send ceiling.
    materialized = sum(len(v) for k, v in out.items() if k.startswith("```matrx"))
    assert materialized <= WIRE_SWAP_TOTAL_MAX_CHARS

    assert len(sink_events) == 1
    evt = sink_events[0]
    assert evt.truncated_count == 2
    assert evt.skipped_count == 1
    assert set(evt.reasons) == {"single_value_capped", "total_budget_capped"}


def test_repeated_fence_across_messages_is_occurrence_budgeted(sink_events):
    # Regression for the 2026-07-07 adversarial finding #1: a value that is UNDER
    # the single cap AND under the distinct-map total, but referenced in several
    # messages, materializes once per message — the true wire size multiplies past
    # the ceiling. The budget must count occurrences, skip the over-budget value
    # (leaving its fence verbatim), and the alarm must report the TRUE re-billed
    # size (weighted), not the distinct-map sum.
    # Comfortably under the single cap, but three copies blow the total.
    val = "Z" * ((WIRE_SWAP_TOTAL_MAX_CHARS // 2) - 50_000)  # ~950K, < single cap
    assert len(val) < WIRE_SWAP_SINGLE_VALUE_MAX_CHARS
    set_wire_swaps({_FENCE_A: val})
    try:
        # Same fence in THREE separate user messages → weight 3 → ~2.85M materialized.
        cfg = UnifiedConfig(
            model="test-model",
            messages=[
                UnifiedMessage(role="user", content=[TextContent(text=f"first {_FENCE_A}")]),
                UnifiedMessage(role="user", content=[TextContent(text=f"second {_FENCE_A}")]),
                UnifiedMessage(role="user", content=[TextContent(text=f"third {_FENCE_A}")]),
            ],
        )
        wire = build_wire_config(cfg)
        assert wire is not None
        # Over the occurrence-weighted total → SKIPPED verbatim in every message.
        for m in wire.messages:
            assert _FENCE_A in m.content[0].text
            assert val not in m.content[0].text
        assert len(sink_events) == 1
        evt = sink_events[0]
        assert "total_budget_capped" in evt.reasons
        assert evt.skipped_count == 1
        # The alarm reports the TRUE re-billed size (3 × ~950K), not one copy.
        assert evt.total_fence_chars == 3 * len(val)
    finally:
        set_wire_swaps({})


def test_single_reference_unaffected_by_occurrence_weighting(sink_events):
    # A value that fits when counted ONCE must still pass untouched even though the
    # weighting machinery now runs — guards against the weighting over-counting a
    # single occurrence.
    val = "Q" * (WIRE_SWAP_SINGLE_VALUE_MAX_CHARS - 1)  # just under single cap
    set_wire_swaps({_FENCE_A: val})
    try:
        wire = build_wire_config(_cfg(_FENCE_A))  # one occurrence
        assert wire is not None
        assert val in _user_text(wire)
        assert sink_events == []
    finally:
        set_wire_swaps({})


def test_swap_text_is_single_pass_no_cross_reference_injection():
    # Regression for adversarial finding #2: one referenced value contains the
    # LITERAL fence-key text of another reference. A naive multi-pass replace loop
    # would, after substituting fence B, re-scan B's value and expand fence A that
    # sits inside it (cross-reference injection / double-substitution). The
    # single-pass substitution must replace each fence exactly once with its own
    # value and never re-expand inserted content.
    fence_a = _FENCE_A
    fence_b = _FENCE_B
    # B's resolved value literally embeds A's fence text.
    val_b = f"B-start {fence_a} B-end"
    val_a = "AAA"
    set_wire_swaps({fence_a: val_a, fence_b: val_b})
    try:
        cfg = UnifiedConfig(
            model="test-model",
            messages=[UnifiedMessage(role="user", content=[TextContent(text=f"x {fence_b} y")])],
        )
        wire = build_wire_config(cfg)
        text = _user_text(wire)
        # B expanded to its value verbatim — the A-fence INSIDE B's value is NOT
        # re-expanded to val_a (it was inserted, not part of the original text).
        assert text == f"x B-start {fence_a} B-end y"
        assert val_a not in text
    finally:
        set_wire_swaps({})


def test_redact_reverses_a_budget_truncated_value_to_its_key(sink_events):
    # Regression for the 2026-07-07 deferred-LOW finding: when the per-send budget
    # TRUNCATES a fence value, the wire carries the truncated HEAD, not the full
    # value. Snapshot redaction must reverse that head back to the fence key —
    # reversing against the full original (the old behavior) would miss it and
    # leave partial reference content in cx_request_snapshot.
    big = "X" * (WIRE_SWAP_SINGLE_VALUE_MAX_CHARS + 5000)
    set_wire_swaps({_FENCE_A: big})
    try:
        wire = build_wire_config(_cfg(_FENCE_A))
        materialized_text = _user_text(wire)  # head + notice, NOT the full big value
        assert big not in materialized_text  # it was truncated
        # A captured provider payload carrying that materialized (truncated) text …
        payload = {"messages": [{"role": "user", "content": [{"text": materialized_text}]}]}
        redacted = redact_wire_payload(payload)
        # … redacts back to the fence KEY, and no fragment of the value survives.
        assert redacted is not None, "truncated value must still be redactable (not dropped)"
        redacted_text = redacted["messages"][0]["content"][0]["text"]
        assert redacted_text == f"use {_FENCE_A}"  # the key is restored, exactly
        assert "XXXXX" not in redacted_text  # no reference-content fragment left behind
    finally:
        set_wire_swaps({})


def test_apply_budget_unit_preserves_small_swaps():
    # The budget function itself: oversized fence trimmed, small fence intact,
    # picklist token intact — deterministic, no config machinery.
    token = "⁣matrx:picklist:x⁣"
    swaps = {
        _FENCE_A: "A" * (WIRE_SWAP_SINGLE_VALUE_MAX_CHARS + 250_000),
        _FENCE_B: "small",
        token: "the description",
    }
    out = pr._apply_wire_swap_budget(swaps)
    assert out[_FENCE_B] == "small"
    assert out[token] == "the description"
    # Truncation is a net reduction AND the notice fits within the ceiling.
    assert len(out[_FENCE_A]) < len(swaps[_FENCE_A])
    assert len(out[_FENCE_A]) <= WIRE_SWAP_SINGLE_VALUE_MAX_CHARS
    assert "value truncated" in out[_FENCE_A]
