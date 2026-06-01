"""Flow-action → SDK ActionType lookup table.

Bridges the platform's flow-step vocabulary (the names enumerated in
``backend/src/monitor/remediation/actions/registry.py``) to the SDK's
internal :class:`ActionType` enum and the parameter shapes the in-process
interventions expect.

The platform speaks in *recovery strategies* ("retry_with_backoff",
"switch_model", …) but the SDK speaks in *enforcement tiers*
("in-step retry", "trajectory force-fallback", …). One platform step maps
to exactly one SDK directive; this module is the single place that
translation lives.

Actions explicitly marked ``unsupported`` here are platform-side concerns
(human escalation, async validation) that the SDK cannot apply locally —
the FlowEvaluator must skip these steps and let them stay on the manual
remediation queue.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from aigie.autonomous.adapters import ActionType

# Defaults applied when a flow step omits a parameter the SDK needs.
_DEFAULT_MAX_RETRIES = 3
_DEFAULT_BACKOFF_MS = 200
_RETRY_NO_BACKOFF_MS = 0


# ---------------------------------------------------------------------------
# Param builders — each takes the step's ``parameters`` dict and returns the
# canonical kwargs the SDK directive will carry.
# ---------------------------------------------------------------------------


def _params_retry_immediate(parameters: dict[str, Any]) -> dict[str, Any]:
    return {
        "max_retries": int(parameters.get("max_retries", _DEFAULT_MAX_RETRIES)),
        "backoff_ms": _RETRY_NO_BACKOFF_MS,
    }


def _params_retry_with_backoff(parameters: dict[str, Any]) -> dict[str, Any]:
    return {
        "max_retries": int(parameters.get("max_retries", _DEFAULT_MAX_RETRIES)),
        "backoff_ms": int(parameters.get("backoff_ms", _DEFAULT_BACKOFF_MS)),
    }


def _params_switch_model(parameters: dict[str, Any]) -> dict[str, Any]:
    model = parameters.get("model") or parameters.get("fallback_model") or ""
    return {"model": str(model)}


def _params_rewrite_args(parameters: dict[str, Any]) -> dict[str, Any]:
    # modify_prompt / reduce_context: the platform doesn't standardize the
    # parameter shape, so the entire parameters dict is passed through as
    # ``args_overrides`` for the intervention to interpret.
    return {"args_overrides": dict(parameters)}


def _params_fallback_tool(parameters: dict[str, Any]) -> dict[str, Any]:
    tool = parameters.get("tool") or parameters.get("fallback_tool") or ""
    return {"tool": str(tool)}


def _params_break_loop(action_name: str) -> Callable[[dict[str, Any]], dict[str, Any]]:
    def _build(parameters: dict[str, Any]) -> dict[str, Any]:
        reason = parameters.get("reason") or action_name
        return {"reason": str(reason)}

    return _build


# ---------------------------------------------------------------------------
# Mapping
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ActionMapping:
    """SDK-side resolution of a flow step.

    Attributes:
        action_type: The SDK ActionType this flow action maps to.
        params:      The kwargs to attach to the synthesised Directive.
    """

    action_type: ActionType
    params: dict[str, Any]


# Canonical names mirror ``ALL_ACTIONS`` in
# ``backend/src/monitor/remediation/actions/registry.py``. Keep this list
# in lockstep with the platform registry — the parity test guards it.
KNOWN_PLATFORM_ACTIONS: frozenset[str] = frozenset(
    {
        "retry",
        "retry_with_backoff",
        "switch_model",
        "reduce_context",
        "refresh_credentials",
        "rate_limit_wait",
        "modify_prompt",
        "fallback_tool",
        "skip_and_log",
        "circuit_break",
        "validate_output",
    }
)

# Actions the SDK cannot apply locally — they remain platform-side.
# refresh_credentials → operator must rotate keys.
# validate_output    → server-side LLM judge re-runs validation.
UNSUPPORTED_ACTIONS: frozenset[str] = frozenset({"refresh_credentials", "validate_output"})

# (action_type, param_builder) for each supported name. Param builder is
# called with the step's ``parameters`` dict at evaluation time.
_SUPPORTED: dict[str, tuple[ActionType, Callable[[dict[str, Any]], dict[str, Any]]]] = {
    "retry": (ActionType.IN_STEP_RETRY, _params_retry_immediate),
    "retry_with_backoff": (ActionType.IN_STEP_RETRY, _params_retry_with_backoff),
    "rate_limit_wait": (ActionType.IN_STEP_RETRY, _params_retry_with_backoff),
    "switch_model": (ActionType.TRAJECTORY_FORCE_FALLBACK, _params_switch_model),
    "modify_prompt": (ActionType.IN_STEP_REWRITE_ARGS, _params_rewrite_args),
    "reduce_context": (ActionType.IN_STEP_REWRITE_ARGS, _params_rewrite_args),
    "fallback_tool": (ActionType.TRAJECTORY_FORCE_FALLBACK, _params_fallback_tool),
    "skip_and_log": (ActionType.TRAJECTORY_BREAK_LOOP, _params_break_loop("skip_and_log")),
    "circuit_break": (ActionType.TRAJECTORY_BREAK_LOOP, _params_break_loop("circuit_break")),
}


def is_known_action(name: str) -> bool:
    """True if *name* is recognised by the platform registry (supported or not)."""
    return (name or "").lower() in KNOWN_PLATFORM_ACTIONS


def is_supported_action(name: str) -> bool:
    """True if the SDK can apply this action locally."""
    return (name or "").lower() in _SUPPORTED


def resolve_step(step: dict[str, Any]) -> ActionMapping | None:
    """Resolve a flow step to an :class:`ActionMapping`, or ``None`` if unsupported.

    A return of ``None`` means one of:
      * the step has no ``action`` key, or
      * the action name is unknown (not in the platform registry), or
      * the action is explicitly marked unsupported in the SDK.

    The caller (FlowEvaluator) should treat ``None`` as "skip this step".
    """
    if not isinstance(step, dict):
        return None
    name = str(step.get("action", "")).lower()
    if not name:
        return None
    entry = _SUPPORTED.get(name)
    if entry is None:
        return None
    action_type, build = entry
    parameters = step.get("parameters", {})
    if not isinstance(parameters, dict):
        parameters = {}
    return ActionMapping(action_type=action_type, params=build(parameters))
