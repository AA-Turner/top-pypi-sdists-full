"""Tests for the random_wheel tool: uniformity, dedup, gate-safety, handler."""
import asyncio
from collections import Counter

from matrx_ai.tools._generated_declarations import RandomWheelArgs
from matrx_ai.tools.implementations.random_wheel import (
    IDEA_TOPICS,
    SHOWCASE_TOPICS,
    _build_plan,
    _gate_safe_text,
    _normalize_items,
    _pick_display,
    random_wheel,
)
from matrx_ai.tools.models import ToolContext


def _ctx() -> ToolContext:
    return ToolContext(call_id="wheel-test")


# ── Randomness ────────────────────────────────────────────────────────────────


def test_pick_display_uniform_and_reachable():
    labels = [f"i{n}" for n in range(50)]
    winners: Counter = Counter()
    faces: set = set()
    for _ in range(3000):
        disp, wi = _pick_display(labels, 10, [])
        assert len(disp) == 10 == len(set(disp)), "faces must be distinct"
        assert 0 <= wi < 10
        winners[disp[wi]] += 1
        faces.update(disp)
    assert len(faces) == 50, "every pool item must be reachable as a face"
    assert len(winners) > 40, "winners must spread across the pool"


def test_pick_display_respects_avoid():
    disp, _ = _pick_display(["a", "b", "c"], 2, ["a"])
    assert "a" not in disp


def test_pick_display_avoid_all_falls_back_to_full_pool():
    disp, wi = _pick_display(["a", "b"], 2, ["a", "b"])
    assert set(disp) == {"a", "b"} and 0 <= wi < 2


# ── Planning ──────────────────────────────────────────────────────────────────


def test_build_plan_list_dedupes_labels_and_keeps_first_value():
    args = RandomWheelArgs(
        mode="list",
        items=[
            {"label": "Red", "value": "first"},
            {"label": "Red", "value": "second"},
            {"label": "Blue", "value": "blue"},
        ],
        dramatize=False,
    )
    plan = _build_plan(args)
    assert not isinstance(plan, str)
    assert plan.pool_size == 2, "duplicate labels collapse to one face"
    assert plan.candidates.count("Red") <= 1
    if plan.winner_label == "Red":
        assert plan.chosen_value == "first", "first value wins for a duplicate label"


def test_build_plan_bare_uses_idea_pool():
    plan = _build_plan(RandomWheelArgs())
    assert not isinstance(plan, str)
    assert plan.pool_size == len(IDEA_TOPICS)
    assert plan.chosen_value == plan.winner_label  # idea topics: value == label


def test_build_plan_named_showcase_pool():
    plan = _build_plan(RandomWheelArgs(pool="showcase"))
    assert not isinstance(plan, str)
    assert plan.pool_size == len(SHOWCASE_TOPICS) >= 100
    assert plan.winner_label in SHOWCASE_TOPICS


def test_build_plan_unknown_pool_falls_back_to_ideas():
    plan = _build_plan(RandomWheelArgs(pool="does-not-exist"))
    assert not isinstance(plan, str)
    assert plan.pool_size == len(IDEA_TOPICS)


def test_build_plan_web_and_image_seed():
    p = _build_plan(RandomWheelArgs(mode="web"))
    assert not isinstance(p, str)
    assert p.seed in p.candidates and p.pool_size >= 10

    p = _build_plan(RandomWheelArgs(mode="image", keywords=["x", "y", "z"]))
    assert not isinstance(p, str)
    assert p.seed in p.candidates and p.pool_size == 3


# ── Helpers ───────────────────────────────────────────────────────────────────


def test_gate_safe_text_neutralizes_jsonish():
    assert _gate_safe_text('["a","b"]', "fallback") == "fallback"
    assert _gate_safe_text('{"x":1}', "fb") == "fb"
    assert _gate_safe_text("Pick a topic", "fb") == "Pick a topic"
    assert _gate_safe_text(None, None) is None


def test_normalize_items_handles_strings_and_dicts():
    out = _normalize_items(["hello", {"label": "K", "value": 7}, {"no_label": 1}])
    labels = [o["label"] for o in out]
    assert "hello" in labels and "K" in labels
    assert all("label" in o and "value" in o for o in out)


# ── Handler (no network: list mode, dramatize off) ────────────────────────────


def test_handler_list_mode_success_and_gate_safe_title():
    res = asyncio.run(
        random_wheel(
            {
                "mode": "list",
                "items": [
                    {"label": "Red", "value": {"hex": "#f00"}},
                    {"label": "Blue", "value": "b"},
                ],
                "title": '["json","title"]',  # would trip the output gate if unguarded
                "dramatize": False,
            },
            _ctx(),
        )
    )
    assert res.success, res.error
    assert res.output["chosen"]["label"] in ("Red", "Blue")
    assert res.output["title"] == "Spin the wheel"  # guarded fallback
    if res.output["chosen"]["label"] == "Red":
        assert res.output["chosen"]["value"] == {"hex": "#f00"}  # native, not stringified


def test_handler_bare_call_uses_idea_wheel():
    res = asyncio.run(random_wheel({"dramatize": False}, _ctx()))
    assert res.success and res.output["pool_size"] >= 20
