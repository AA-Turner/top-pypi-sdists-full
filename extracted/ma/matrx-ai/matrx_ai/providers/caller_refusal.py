"""ONE answer to "was this run refused by a gate, so a retry can never change it?"

A CALLER REFUSAL is a gate saying no before anything was spent: a spend approval waiting, a
protected account, a plan limit, an automation guardrail, a missing core input, a model the
person may not use. Retrying it changes nothing and pays for nothing, so every caller that
re-tries work (the inbox driver, a sweep, a funnel) must treat it as FINAL.

THE DEFECT THIS CLOSES (live 2026-10-18, 38 refused retries on one person's chat): the inbox
driver decided "refused?" by comparing the emitted error's code with its own hand-written list.
The list said ``account_protected``; the protected-account gate says
``protected_account_run_refused``. It said ``not_ready``; the readiness gate says
``automation_not_ready``. It never knew ``top_tier_model_refused`` at all. Every refusal it
could not name read as "the turn produced no text" and was retried.

THE RULE, by type and never by a caller's list:

* the refusal SOURCE marks itself: every refusal exception class sets ``is_caller_refusal =
  True`` (and ``is_retryable=False`` on its ``error_info``);
* when a refusal becomes an error EVENT (the executor contains it and emits it), the event's
  ``details`` carry ``caller_refusal: True`` (:data:`CALLER_REFUSAL_KEY`), derived from that
  type — so the classification survives the trip through an emitter;
* a consumer asks :func:`is_caller_refusal` — on an exception, an error event, or a bare code.
  A code-only consumer (a funnel that kept only words) is answered from
  :func:`caller_refusal_codes`, the ONE registry; every refusal class's code is in it
  (``aidream/services/tooling/tests/test_caller_refusals_are_final.py`` proves it by scanning
  every class that declares ``is_caller_refusal``).

A host refuser this package does not define (a sandbox that is offline) registers its code with
:func:`register_caller_refusal_code` where its class is defined.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from matrx_ai.providers.guardrail_gate import AUTOMATION_GUARDRAIL
from matrx_ai.providers.model_tier_gate import TOP_TIER_MODEL_REFUSED
from matrx_ai.providers.readiness_gate import AUTOMATION_NOT_READY
from matrx_ai.providers.run_approval_gate import (
    PROTECTED_ACCOUNT_RUN_REFUSED,
    RUN_APPROVAL_REQUIRED,
)
from matrx_ai.providers.usage_gate import GUEST_AI_ALLOWANCE_USED, USAGE_LIMIT_REACHED

#: The flag an error event's ``details`` carry when the error is a caller refusal.
CALLER_REFUSAL_KEY = "caller_refusal"

_codes: set[str] = {
    RUN_APPROVAL_REQUIRED,
    PROTECTED_ACCOUNT_RUN_REFUSED,
    AUTOMATION_GUARDRAIL,
    USAGE_LIMIT_REACHED,
    GUEST_AI_ALLOWANCE_USED,
    AUTOMATION_NOT_READY,
    TOP_TIER_MODEL_REFUSED,
    # providers/free_tier_models.FREE_TIER_MODEL_REFUSED — named here, not imported, so this
    # registry never depends on that gate's import order.
    "free_tier_model_refused",
    # providers/child_safety_gate.py — the COPPA refusal at the provider boundary (the same error
    # types the host's doors send).
    "education_coppa_consent_required",
    "education_age_declaration_required",
}


def register_caller_refusal_code(code: str) -> str:
    """Add a host refuser's code to the registry (call it where the refusal class is defined)."""
    text = str(code or "").strip()
    if not text:
        raise ValueError("a caller refusal code cannot be empty")
    _codes.add(text)
    return text


def caller_refusal_codes() -> frozenset[str]:
    """Every registered caller refusal code."""
    return frozenset(_codes)


def mark_caller_refusal(details: Mapping[str, Any] | None) -> dict[str, Any]:
    """``details`` with the caller-refusal flag set — for an emitter carrying a refusal."""
    out = dict(details or {})
    out[CALLER_REFUSAL_KEY] = True
    return out


def refusal_code(value: Any) -> str:
    """The stable code of an exception, an error event, or a bare code ('' when none)."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, BaseException):
        code = getattr(value, "code", None) or getattr(getattr(value, "error_info", None), "error_type", None)
        return str(code or "")
    if isinstance(value, Mapping):
        details = value.get("details")
        details = details if isinstance(details, Mapping) else {}
        for candidate in (value.get("code"), value.get("type"), value.get("error_type"), details.get("error")):
            if candidate:
                return str(candidate)
    return ""


def is_caller_refusal(value: Any) -> bool:
    """True when ``value`` is a caller refusal — never retried, never filed as a failure.

    An exception answers by its type (``is_caller_refusal``). An error event answers by the
    flag its source set (``details.caller_refusal``), else by its code in the registry. A bare
    string is a code.
    """
    if value is None:
        return False
    if isinstance(value, BaseException):
        return bool(getattr(value, "is_caller_refusal", False))
    if isinstance(value, Mapping):
        details = value.get("details")
        if isinstance(details, Mapping) and details.get(CALLER_REFUSAL_KEY) is True:
            return True
        if value.get(CALLER_REFUSAL_KEY) is True:
            return True
    return refusal_code(value) in _codes


__all__ = [
    "CALLER_REFUSAL_KEY",
    "caller_refusal_codes",
    "is_caller_refusal",
    "mark_caller_refusal",
    "refusal_code",
    "register_caller_refusal_code",
]
