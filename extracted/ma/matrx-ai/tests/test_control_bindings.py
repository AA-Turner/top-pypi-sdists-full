"""Controls as first-class variables — a bound control resolves BEFORE the catalog compile.

Forcing functions (each fails if resolution is skipped, runs after the compile, or
silently mutates an out-of-set value):

1. A variable-bound aspect_ratio / quality reaches the canonical dict the compile reads,
   with the RUN's value — not the author's default and not nothing.
2. A resolved value the offering does not map is converted by the equivalence map and
   the conversion is reported as an Adjustment (never a silent rewrite).
3. A value the canonical vocabulary refuses is never forwarded: the author's value is
   used and an UNEXPECTED ``unsupported_value`` Adjustment names it.
4. A control the org's policy does not make bindable ignores the caller's value, loudly.
"""

from __future__ import annotations

from matrx_ai.agents.control_bindings import (
    DEFAULT_BINDABLE_POLICY,
    coerce_control_value,
    control_is_bindable,
    resolve_control_bindings,
)
from matrx_ai.catalog.canonicalize import canonical_settings_from_config
from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ControlRule
from matrx_ai.client_host.agent_source import (
    ExecutionAgentDefinition,
    definition_to_agent_config,
)


def _image_agent(settings: dict | None = None):
    definition = ExecutionAgentDefinition(
        definition_id="00000000-0000-0000-0000-000000000001",
        agent_id="00000000-0000-0000-0000-000000000001",
        name="Product shot",
        model_id="gpt-image-2",
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": "A {{subject}} in {{style}} style"}],
            }
        ],
        settings=settings or {},
        variable_definitions=[
            {"name": "subject", "defaultValue": "ceramic mug"},
            {"name": "style", "defaultValue": "studio photo"},
            {
                "name": "aspect_ratio",
                "defaultValue": "1:1",
                "customComponent": {"type": "pill-toggle", "options": ["1:1", "16:9", "21:9"]},
                "control": {"key": "aspect_ratio"},
            },
            {
                "name": "quality",
                "defaultValue": "medium",
                "customComponent": {"type": "select", "options": ["low", "medium", "high"]},
                "control": {"key": "quality"},
            },
        ],
    )
    return definition_to_agent_config(definition)


def _offering_rules() -> CompiledControlsMap:
    # An offering that only carries three aspect ratios — 21:9 is NOT mapped.
    return CompiledControlsMap(
        rules={
            "aspect_ratio": ControlRule.model_validate(
                {"value_map": {"1:1": "1:1", "16:9": "16:9", "9:16": "9:16"}}
            ),
            "quality": ControlRule.model_validate({}),
        }
    )


def test_bound_controls_are_absent_until_resolved_and_carry_the_run_value():
    agent = _image_agent()
    # The literal is NOT in settings while bound — without resolution nothing is sent.
    before = canonical_settings_from_config(agent.config)
    assert "aspect_ratio" not in before
    assert "quality" not in before

    result = resolve_control_bindings(
        agent.config,
        agent.variable_defaults,
        {"subject": "mug", "aspect_ratio": "16:9", "quality": "high"},
    )

    assert result.applied == {"aspect_ratio": "16:9", "quality": "high"}
    after = canonical_settings_from_config(agent.config)
    assert after["aspect_ratio"] == "16:9"
    # `quality` rides LLMParams' alias remap (→ render_quality) and lands back under the
    # compile's canonical key "quality" — the same door a config_overrides request uses.
    assert agent.config.render_quality == "high"
    assert after["quality"] == "high"
    params, adjustments = _offering_rules().outbound(after)
    assert params == {"aspect_ratio": "16:9", "quality": "high"}
    assert adjustments == []


def test_default_is_used_when_the_caller_sends_nothing():
    agent = _image_agent()
    resolve_control_bindings(agent.config, agent.variable_defaults, {})
    after = canonical_settings_from_config(agent.config)
    assert after["aspect_ratio"] == "1:1"
    assert after["quality"] == "medium"


def test_out_of_offering_value_is_converted_by_the_compile_and_announced():
    agent = _image_agent()
    resolve_control_bindings(
        agent.config, agent.variable_defaults, {"aspect_ratio": "21:9"}
    )
    canonical = canonical_settings_from_config(agent.config)
    assert canonical["aspect_ratio"] == "21:9"  # resolved BEFORE compile, untouched
    params, adjustments = _offering_rules().outbound(canonical)
    assert params["aspect_ratio"] == "16:9"  # nearest by ratio
    assert [(a.key, a.action, a.canonical_value, a.sent_value) for a in adjustments] == [
        ("aspect_ratio", "mapped", "21:9", "16:9")
    ]


def test_value_outside_the_canonical_vocabulary_is_never_forwarded_silently():
    agent = _image_agent()
    result = resolve_control_bindings(
        agent.config, agent.variable_defaults, {"aspect_ratio": "7:3"}
    )
    assert agent.config.aspect_ratio == "1:1"  # the author's value, not the bad one
    assert len(result.adjustments) == 1
    adj = result.adjustments[0]
    assert adj.key == "aspect_ratio"
    assert adj.action == "unsupported_value"
    assert adj.expected is False
    assert adj.canonical_value == "7:3"
    assert adj.sent_value == "1:1"


def test_non_bindable_control_ignores_the_callers_value_loudly():
    agent = _image_agent()
    policy = {"allow": ["*"], "deny": ["aspect_ratio"]}
    result = resolve_control_bindings(
        agent.config, agent.variable_defaults, {"aspect_ratio": "16:9"}, policy=policy
    )
    assert agent.config.aspect_ratio == "1:1"
    assert [(a.key, a.action) for a in result.adjustments] == [("aspect_ratio", "dropped")]


def test_default_policy_locks_safety_controls():
    assert not control_is_bindable("moderation", DEFAULT_BINDABLE_POLICY)
    assert not control_is_bindable("disable_safety_checker", DEFAULT_BINDABLE_POLICY)
    assert control_is_bindable("aspect_ratio", DEFAULT_BINDABLE_POLICY)
    # A malformed policy never opens a safety control.
    assert not control_is_bindable("moderation", "everything")


def test_text_variables_coerce_to_typed_controls():
    assert coerce_control_value("0.7") == 0.7
    assert coerce_control_value("2") == 2
    assert coerce_control_value("true") is True
    assert coerce_control_value("16:9") == "16:9"
    assert coerce_control_value("") is None


def test_an_agent_without_bound_controls_is_untouched():
    agent = _image_agent(settings={"aspect_ratio": "9:16"})
    agent.variable_defaults = {
        k: v for k, v in agent.variable_defaults.items() if v.control is None
    }
    result = resolve_control_bindings(agent.config, agent.variable_defaults, {"aspect_ratio": "1:1"})
    assert result.applied == {}
    assert agent.config.aspect_ratio == "9:16"


def test_a_boolean_controls_toggle_words_become_booleans():
    from matrx_ai.agents.variables import AgentVariable

    agent = _image_agent()
    variables = dict(agent.variable_defaults)
    variables["web"] = AgentVariable.from_dict(
        {"name": "web", "defaultValue": "Off", "control": {"key": "internal_web_search"}}
    )
    resolve_control_bindings(agent.config, variables, {"web": "On"})
    assert agent.config.internal_web_search is True
