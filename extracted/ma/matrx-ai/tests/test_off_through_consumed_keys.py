"""Settings-translation C7b — OFF reaches the processors from ANY key they consume.

Owner's words (GROUND-TRUTH.md): "the difference between something being set to none
and something not being included at all". Before C7b an off arriving through a key a
thinking processor CONSUMES (thinking_budget=0, thinking_level="none") or through the
number->scale conversion never met the cell's ``off`` rule: the wire equalled "not set"
and the model's default thinking ran (T3: 82 findings on Anthropic, Google, Together).

Rules pinned here:
  * an off from a consumed depth key is decided by the cell's ``off`` exactly like an
    off on the owner key (send / floor / omit-with-why);
  * with no ``off`` declared the processor's own off path runs — and when that path
    puts nothing on the wire it is VOICED, never silent;
  * a key the caller set directly beats a consumed sibling's off;
  * hiding thoughts (visibility) is never depth: it never turns thinking off or
    changes the effort; it hides where thinking happens;
  * K6 ``context``: a rule that applies only on one operation (gpt-image-1.5
    input_fidelity is edit-only) is a declared drop elsewhere.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from matrx_ai.catalog.canonicalize import canonical_settings_from_config
from matrx_ai.catalog.controls import ControlRule, compile_controls, flatten_dotted

CONSUMES = ["thinking_budget", "thinking_level", "include_thoughts", "reasoning_summary"]


def _anthropic(*, mode: str = "adaptive", off: dict | None = None, **config: Any):
    rule: dict[str, Any] = {
        "provider_key": "thinking",
        "processor": "anthropic_thinking",
        "processor_config": {
            "mode": mode,
            "order": 100,
            "consumes": CONSUMES,
            "default_max_tokens": 64000,
            **config,
        },
    }
    if off is not None:
        rule["off"] = off
    return compile_controls(
        {
            "reasoning_effort": ControlRule.model_validate(rule),
            "max_output_tokens": ControlRule.model_validate({"provider_key": "max_tokens"}),
        },
        {},
    )


def _google_legacy(off: dict | None = None):
    rule: dict[str, Any] = {
        "provider_key": "thinking_config.thinking_budget",
        "processor": "google_thinking",
        "processor_config": {"mode": "legacy", "order": 100, "consumes": CONSUMES},
    }
    if off is not None:
        rule["off"] = off
    return compile_controls({"reasoning_effort": ControlRule.model_validate(rule)}, {})


def _together():
    return compile_controls(
        {
            "reasoning_effort": ControlRule.model_validate(
                {
                    "processor": "together_reasoning",
                    "processor_config": {"order": 100, "consumes": CONSUMES},
                }
            )
        },
        {},
    )


def _wire(controls: Any, context: dict[str, Any] | None = None, **config: Any):
    canonical = canonical_settings_from_config(SimpleNamespace(**config))
    params, adjustments = controls.outbound(canonical, context=context)
    return flatten_dotted(params), adjustments


# ── depth off through a consumed key ─────────────────────────────────────────
def test_budget_zero_meets_the_owner_cells_off_send() -> None:
    controls = _anthropic(off={"send": {"type": "disabled"}})
    wire, adjustments = _wire(controls, thinking_budget=0)
    unset, _ = _wire(controls)
    assert wire["thinking.type"] == "disabled"
    assert wire != unset
    assert any(a.key == "thinking_budget" and a.action == "mapped" for a in adjustments)


def test_budget_zero_on_budget_mode_meets_off_send() -> None:
    wire, _ = _wire(_anthropic(mode="budget", off={"send": {"type": "disabled"}}), thinking_budget=0)
    assert wire["thinking.type"] == "disabled"


def test_google_budget_zero_sends_the_declared_zero() -> None:
    wire, _ = _wire(_google_legacy(off={"send": 0}), thinking_budget=0)
    assert wire == {"thinking_config.thinking_budget": 0}


def test_no_off_declared_runs_the_processors_own_off_path() -> None:
    # Together's own off is reasoning.enabled=false; before C7b a budget of 0 was a
    # "converted" effort the processor treated as unset -> reasoning_effort "high".
    wire, _ = _wire(_together(), thinking_budget=0)
    assert wire == {"reasoning.enabled": False}


def test_thinking_level_none_is_an_off_too() -> None:
    wire, _ = _wire(_together(), thinking_level="none")
    assert wire == {"reasoning.enabled": False}


def test_owner_omit_decides_a_consumed_off_and_says_so() -> None:
    controls = _google_legacy(off={"omit": True, "why": "this model does not think unless asked"})
    wire, adjustments = _wire(controls, thinking_budget=0)
    unset, _ = _wire(controls)
    assert wire == unset
    assert any(a.action == "omitted" and a.expected for a in adjustments)
    # T3 reads the same deciding rule the engine uses.
    assert controls.off_rule_for("thinking_budget").off.omit is True


def test_undeclared_off_that_reaches_nothing_is_voiced_not_silent() -> None:
    # google legacy with NO off: its own path for none is "send nothing".
    wire, adjustments = _wire(_google_legacy(), reasoning_effort="none")
    unset, _ = _wire(_google_legacy())
    assert wire == unset
    voiced = [a for a in adjustments if a.key == "reasoning_effort" and a.action == "dropped"]
    assert voiced and voiced[0].expected is False and voiced[0].provenance == "computed"


def test_a_depth_the_caller_set_beats_a_consumed_off() -> None:
    controls = _anthropic(off={"send": {"type": "disabled"}})
    wire, _ = _wire(controls, reasoning_effort="high", thinking_level="none")
    assert wire["thinking.type"] == "adaptive"
    assert wire["output_config.effort"] == "high"


def test_a_positive_budget_is_not_an_off() -> None:
    wire, _ = _wire(_anthropic(off={"send": {"type": "disabled"}}), thinking_budget=5000)
    assert wire["thinking.type"] == "adaptive"


# ── visibility is never depth ───────────────────────────────────────────────
def test_hiding_thoughts_keeps_the_depth_the_caller_asked_for() -> None:
    wire, _ = _wire(_anthropic(), reasoning_effort="high", include_thoughts=False)
    assert wire["thinking.type"] == "adaptive"
    assert wire["thinking.display"] == "omitted"
    assert wire["output_config.effort"] == "high"


def test_hiding_thoughts_on_an_always_on_model_never_lowers_the_effort() -> None:
    wire, _ = _wire(_anthropic(thinking_always_on=True), include_thoughts=False)
    assert wire["thinking.type"] == "adaptive"
    assert wire["thinking.display"] == "omitted"
    assert "output_config.effort" not in wire  # the model's own default depth


def test_hiding_thoughts_on_a_model_that_thinks_by_default() -> None:
    wire, _ = _wire(_anthropic(thinks_by_default=True), reasoning_summary="never")
    assert wire["thinking.type"] == "adaptive"
    assert wire["thinking.display"] == "omitted"
    assert "output_config.effort" not in wire


def test_hiding_thoughts_of_a_model_that_is_not_thinking_turns_nothing_on() -> None:
    wire, _ = _wire(_anthropic(), include_thoughts=False)
    unset, _ = _wire(_anthropic())
    assert wire == unset


def test_declared_visibility_omit_is_voiced_and_never_unhides_real_thinking() -> None:
    controls = compile_controls(
        {
            "reasoning_effort": _anthropic().rules["reasoning_effort"],
            "include_thoughts": ControlRule.model_validate(
                {"off": {"omit": True, "why": "nothing to hide when not thinking"}}
            ),
        },
        {},
    )
    _, adjustments = _wire(controls, include_thoughts=False)
    assert any(a.key == "include_thoughts" and a.action == "omitted" for a in adjustments)
    wire, _ = _wire(controls, include_thoughts=False, reasoning_effort="medium")
    assert wire["thinking.display"] == "omitted"


# ── K6 context: a rule for one operation only ───────────────────────────────
def _image():
    return compile_controls(
        {
            "input_fidelity": ControlRule.model_validate(
                {"context": {"operation": "edit"}, "why": "images.generate rejects it"}
            )
        },
        {},
    )


def test_context_rule_applies_on_its_operation() -> None:
    params, _ = _image().outbound({"input_fidelity": "high"}, context={"operation": "edit"})
    assert params == {"input_fidelity": "high"}


def test_context_rule_is_a_declared_drop_elsewhere() -> None:
    for context in ({"operation": "generate"}, {}, None):
        params, adjustments = _image().outbound({"input_fidelity": "high"}, context=context)
        assert params == {}
        drop = [a for a in adjustments if a.key == "input_fidelity"]
        assert drop and drop[0].action == "dropped" and drop[0].expected is True
