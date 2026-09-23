"""Controls as first-class variables — resolve variable-bound controls into the config.

A model control (aspect ratio, quality, voice, speed, temperature, …) on an agent is
either a LITERAL in ``settings`` or BOUND to one of the agent's variables. A bound
control is declared on the variable itself::

    {"name": "aspect_ratio", "defaultValue": "16:9",
     "customComponent": {"type": "pill-toggle", "options": [...]},
     "control": {"key": "aspect_ratio"}}

and the key is ABSENT from ``settings`` while bound (the variable's default IS the
agent's literal — one source of truth; unbinding writes it back). The variable is an
input on the run page and in chat exactly like a text variable, and a headless
caller (API / MCP / workflow) passes it in the same ``variables`` payload.

Resolution happens BEFORE the catalog compile: the resolved value is applied to the
``UnifiedConfig`` through ``LLMParams`` + ``apply_overrides`` — the SAME door a
``config_overrides`` request uses — so alias remaps (``quality`` → ``render_quality``)
run, and later ``CompiledControlsMap.outbound`` applies the equivalence map
(value_map / nearest / clamp) to the resolved value and reports every conversion as
an ``Adjustment``.

Nothing is silent:
  * a value the canonical vocabulary refuses (``LLMParams`` rejects it) is never
    forwarded — the author's default is used instead and an UNEXPECTED
    ``unsupported_value`` Adjustment reaches the client as the existing warning;
  * a control the organization has not made bindable
    (``agents.controls / variable_bindable_keys``) ignores the caller's value, uses the
    author's default, and says so the same way.

Common-docs: systems/agents/typed-messages/FEATURE.md (the Slot).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint
from pydantic import ValidationError

if TYPE_CHECKING:
    from matrx_ai.agents.variables import AgentVariable
    from matrx_ai.catalog.models import Adjustment
    from matrx_ai.config.unified_config import UnifiedConfig

# The platform default of the org knob ``agents.controls / variable_bindable_keys``
# (seeded by aidream/db/migrations/ai_089_controls_variable_bindable_keys.sql).
# Used by hosts that have no knob register (matrx-ai standalone); aidream resolves
# the live, org-scoped value and passes it in.
DEFAULT_BINDABLE_POLICY: dict[str, list[str]] = {
    "allow": ["*"],
    "deny": [
        "moderation",
        "disable_safety_checker",
        "safety_tolerance",
        "safety_filter_level",
        "safety_settings",
        "person_generation",
        "include_rai_reason",
    ],
}


@dataclass
class ControlBindingResolution:
    """What happened to each bound control on this run."""

    applied: dict[str, Any] = field(default_factory=dict)
    adjustments: list[Adjustment] = field(default_factory=list)


def control_key_of(variable: AgentVariable) -> str | None:
    """The control key a variable is bound to, or None."""
    control = variable.control
    if not isinstance(control, dict):
        return None
    key = control.get("key")
    return key if isinstance(key, str) and key else None


def control_bindings_from_variables(
    variable_defaults: dict[str, AgentVariable] | None,
) -> dict[str, str]:
    """``{control_key: variable_name}`` for every variable bound to a control."""
    out: dict[str, str] = {}
    for name, variable in (variable_defaults or {}).items():
        key = control_key_of(variable)
        if key is not None:
            out[key] = name
    return out


def control_is_bindable(key: str, policy: Any) -> bool:
    """Apply the org policy ``{"allow": [...], "deny": [...]}`` ("*" = every key).

    A malformed policy falls back to the platform default, loudly — a broken knob
    must never silently expose safety controls.
    """
    if not isinstance(policy, dict):
        if policy is not None:
            vcprint(
                f"[control_bindings] variable_bindable_keys is not an object ({policy!r}); "
                "using the platform default policy.",
                color="yellow",
            )
        policy = DEFAULT_BINDABLE_POLICY
    deny = policy.get("deny") or []
    allow = policy.get("allow") or []
    if key in deny:
        return False
    return "*" in allow or key in allow


def coerce_control_value(value: Any) -> Any:
    """Variables travel as text; controls are typed. "" means unset."""
    if isinstance(value, str):
        text = value.strip()
        if text == "":
            return None
        lowered = text.lower()
        if lowered in ("true", "false"):
            return lowered == "true"
        try:
            return int(text)
        except ValueError:
            pass
        try:
            return float(text)
        except ValueError:
            return text
    return value


_TOGGLE_WORDS = {"on": True, "yes": True, "off": False, "no": False}


def _validated(key: str, value: Any) -> Any:
    """Validate ``{key: value}`` through LLMParams; returns the params or raises.

    A boolean control's run input is a toggle whose labels are "On"/"Off"; those
    words become booleans only when the field refuses them as text, so an enum
    that legitimately contains "off" keeps its string value.
    """
    from matrx_ai.config.llm_params import LLMParams

    try:
        return LLMParams.model_validate({key: value})
    except ValidationError:
        if isinstance(value, str) and value.strip().lower() in _TOGGLE_WORDS:
            return LLMParams.model_validate({key: _TOGGLE_WORDS[value.strip().lower()]})
        raise


def resolve_control_bindings(
    config: UnifiedConfig,
    variable_defaults: dict[str, AgentVariable] | None,
    variables: dict[str, Any] | None,
    *,
    policy: Any = None,
    model: Any = None,
) -> ControlBindingResolution:
    """Apply every variable-bound control's resolved value to ``config``.

    ``variables`` is the run's composed variable dict (agent defaults under caller
    values). Call this BEFORE the provider call (the catalog compile) and BEFORE
    ``config_overrides`` are applied, so an explicit override still wins.
    """
    from matrx_ai.catalog.models import Adjustment

    result = ControlBindingResolution()
    bindings = control_bindings_from_variables(variable_defaults)
    if not bindings:
        return result
    values = variables or {}
    effective_policy = DEFAULT_BINDABLE_POLICY if policy is None else policy
    model_label = model if model is not None else getattr(config, "model", "?")

    for key, var_name in bindings.items():
        variable = (variable_defaults or {})[var_name]
        author_value = coerce_control_value(variable.default_value)
        requested = coerce_control_value(values.get(var_name, variable.default_value))

        if not control_is_bindable(key, effective_policy):
            if requested != author_value:
                result.adjustments.append(
                    Adjustment(
                        key=key,
                        action="dropped",
                        canonical_value=requested,
                        sent_value=author_value,
                        expected=False,
                        reason=(
                            f"'{key}' is not a variable-bindable control in this "
                            f"organization — the agent's own value {author_value!r} was used"
                        ),
                    )
                )
            requested = author_value

        if requested is None:
            continue
        try:
            params = _validated(key, requested)
        except ValidationError as exc:
            fallback = author_value
            try:
                fallback_params = _validated(key, fallback) if fallback is not None else None
            except ValidationError:
                fallback_params = None
            result.adjustments.append(
                Adjustment(
                    key=key,
                    action="unsupported_value",
                    canonical_value=requested,
                    sent_value=fallback if fallback_params is not None else None,
                    expected=False,
                    reason=(
                        f"'{key}'={requested!r} (from variable '{var_name}') is not a "
                        f"value this setting accepts ({exc.errors()[0].get('msg', 'invalid')}) — "
                        + (
                            f"the agent's own value {fallback!r} was used"
                            if fallback_params is not None
                            else "the model's default was used"
                        )
                    ),
                )
            )
            if fallback_params is None:
                continue
            params = fallback_params
            requested = fallback
        config.apply_overrides(params)
        result.applied[key] = requested

    if result.applied or result.adjustments:
        vcprint(
            data={
                "applied": result.applied,
                "adjusted": [
                    {"key": a.key, "action": a.action, "requested": a.canonical_value,
                     "sent": a.sent_value, "reason": a.reason}
                    for a in result.adjustments
                ],
            },
            title=f"[control_bindings] variable-bound controls resolved [{model_label}]",
            color="yellow" if result.adjustments else "cyan",
            verbose=True,
        )
    if result.adjustments:
        from matrx_ai.providers.outbound_params import warn_client_about_dropped_settings

        warn_client_about_dropped_settings(result.adjustments, model=model_label)
    return result


__all__ = [
    "DEFAULT_BINDABLE_POLICY",
    "ControlBindingResolution",
    "coerce_control_value",
    "control_bindings_from_variables",
    "control_is_bindable",
    "control_key_of",
    "resolve_control_bindings",
]
