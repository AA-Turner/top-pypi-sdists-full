"""Adversarial review of THE AGENT OUTPUT CONTRACT (KINDS_EVERYWHERE_PLAN.md §6).

Targets: matrx_ai.graph_nodes.shared._extract_content and
matrx_ai.processing.blocks.content_view.content_from_text.

Tests marked ``xfail(strict=True)`` are REPRODUCED HOLES; unmarked tests
document attacks that HELD.

Run: cd /Users/armanisadeghi/code/aidream && uv run pytest \
    packages/matrx-ai/tests/test_adversarial_content_contract.py -q
"""

from __future__ import annotations

import json
import time

import pytest

from matrx_ai.graph_nodes.shared import _extract_content
from matrx_ai.processing.blocks import content_view
from matrx_ai.processing.blocks.content_view import content_from_text

WIRE_KEY = "__kind"


def _fenced(payload: object) -> str:
    return "before prose\n```json\n" + json.dumps(payload) + "\n```\nafter prose"


# ---------------------------------------------------------------------------
# Attacks that HELD
# ---------------------------------------------------------------------------


def test_held_pure_prose_is_one_markdown_instance() -> None:
    out = content_from_text("Just some plain prose.\n\nWith two paragraphs.")
    assert len(out) == 1
    assert out[0][WIRE_KEY] == "markdown"
    assert "two paragraphs" in out[0]["text"]


def test_held_self_described_fence_interleaves_with_zero_prose_loss() -> None:
    out = content_from_text(_fenced({WIRE_KEY: "website", "url": "x"}))
    kinds = [i[WIRE_KEY] for i in out]
    assert kinds == ["markdown", "website", "markdown"]
    assert "before prose" in out[0]["text"]
    assert "after prose" in out[2]["text"]


@pytest.mark.parametrize(
    "bad_kind",
    [{"a": 1}, "", None, 7, ["website"], 3.5, True],
    ids=["dict", "empty", "none", "int", "list", "float", "bool"],
)
def test_held_non_string_or_empty_kind_degrades_to_prose_fold(bad_kind: object) -> None:
    """A malformed __kind never becomes an instance and never crashes — the
    fence folds back into markdown with its source intact (zero loss)."""
    out = content_from_text(_fenced({WIRE_KEY: bad_kind, "v": 1}))
    assert len(out) == 1
    assert out[0][WIRE_KEY] == "markdown"
    assert '"v": 1' in out[0]["text"]  # source preserved inside the fold


def test_held_envelope_stamped_and_self_described_block_yields_one_instance() -> None:
    """DUPLICATION attack: a block BOTH envelope-stamped (metadata.__ir) and
    self-described (payload __kind) must produce exactly one instance."""
    value = {WIRE_KEY: "website", "url": "x"}
    block = {
        "type": "code",
        "content": json.dumps(value),
        "data": {"language": "json", "code": json.dumps(value)},
        "metadata": {"__ir": {"kind": "website", "root": {"value": dict(value)}}},
    }
    original = content_view.process_complete_to_blocks
    content_view.process_complete_to_blocks = lambda _text: [block]
    try:
        out = content_from_text("irrelevant")
    finally:
        content_view.process_complete_to_blocks = original
    assert out == [value]


def test_held_five_megabyte_input_finishes_quickly_with_one_instance() -> None:
    text = (("word " * 200) + "\n\n") * 5000  # ~5MB of prose
    start = time.monotonic()
    out = content_from_text(text)
    elapsed = time.monotonic() - start
    assert elapsed < 30, f"pathological runtime: {elapsed:.1f}s"
    assert len(out) == 1 and out[0][WIRE_KEY] == "markdown"


def test_held_structured_dict_without_marker_yields_empty_content() -> None:
    """Documented behavior: schema-bound answer without __kind cannot be
    named; content stays empty, structured_output remains the access path."""
    assert _extract_content({"url": "x"}, "prose") == []


def test_held_extract_content_never_raises_on_hostile_final_text() -> None:
    hostile = "```json\n{" + '"a": ' * 5000 + "\n" + "\x00￿" + "```"
    assert isinstance(_extract_content(None, hostile), list)


# ---------------------------------------------------------------------------
# FINDING B1 (MEDIUM): structured_output as a LIST silences the entire
# content view. _extract_content returns [] for ANY non-dict structured
# output — even a list where every element is a self-described kind instance
# — AND skips final_text detection entirely, so kind-filtered edges see
# nothing from a turn that produced perfectly typed instances.
# ---------------------------------------------------------------------------


# FIXED (round-1 F11 triage, 2026-08-21): guards the fix now.
def test_list_structured_output_of_kind_instances_populates_content() -> None:
    instances = [
        {WIRE_KEY: "website", "url": "a"},
        {WIRE_KEY: "website", "url": "b"},
    ]
    out = _extract_content(instances, json.dumps(instances))
    assert out == instances


# ---------------------------------------------------------------------------
# FINDING B2 (MEDIUM): envelope/payload kind disagreement resolved silently
# in favor of the UNVALIDATED payload marker. metadata.__ir means "the
# detector VALIDATED this value as envelope.kind", but _envelope_value keeps
# a payload __kind that contradicts it — the instance sails downstream
# claiming an identity the validation never checked (fake-kind smuggling
# through a validated envelope).
# ---------------------------------------------------------------------------


# FIXED (round-1 F11 triage, 2026-08-21): guards the fix now.
def test_envelope_kind_beats_contradicting_payload_marker() -> None:
    block = {
        "type": "code",
        "metadata": {
            "__ir": {
                "kind": "website",
                "root": {"value": {WIRE_KEY: "totally_other_kind", "url": "z"}},
            }
        },
    }
    value = content_view._envelope_value(block)
    assert value is not None
    assert value[WIRE_KEY] == "website"


# ---------------------------------------------------------------------------
# FINDING B3 (LOW): __kind acceptance is "any non-empty str" — an emoji or a
# 10,000-character string becomes a routable typed instance with an
# unbounded, unvetted kind name. Downstream gates may validate, but the §6
# content list itself will happily carry and route on garbage identities.
# ---------------------------------------------------------------------------


def test_finding_b3_absurd_kind_names_become_routable_instances() -> None:
    """GREEN documentation of current behavior (not xfail): whether this is a
    hole depends on downstream gates — recorded so a future name-shape gate
    has a test to flip."""
    for absurd in ["\U0001f600", "x" * 10_000]:
        out = content_from_text(_fenced({WIRE_KEY: absurd, "v": 1}))
        kinds = [i[WIRE_KEY] for i in out]
        assert absurd in kinds  # accepted verbatim today


# ---------------------------------------------------------------------------
# Bound-agent prose: held BY DESIGN, recorded. §6 says a bound agent's
# content is [the bound instance]; prose around the JSON survives only in
# final_text, not in content. The "zero-loss prose folding" claim applies to
# the unbound text pipeline only.
# ---------------------------------------------------------------------------


def test_bound_agent_prose_survives_in_final_text_not_content() -> None:
    so = {WIRE_KEY: "website", "url": "a"}
    final_text = "Here is my analysis first.\n```json\n" + json.dumps(so) + "\n```"
    out = _extract_content(so, final_text)
    assert out == [so]
    # The prose is NOT in content — by §6 design. This assertion pins that
    # trade-off; if the contract ever promises prose retention on the bound
    # path, this test is the tripwire to update.
    assert all(i.get(WIRE_KEY) != "markdown" for i in out)
