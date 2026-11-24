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

from matrx_ai.providers.baa_gate import HIPAA_NOT_COVERED
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
    # HIPAA mode: a provider/route with no BAA (baa_gate) — the host's compliance gate emits
    # the same code (aidream/services/compliance/hipaa.py HIPAA_ERROR_CODE).
    HIPAA_NOT_COVERED,
    # providers/free_tier_models.FREE_TIER_MODEL_REFUSED — named here, not imported, so this
    # registry never depends on that gate's import order.
    "free_tier_model_refused",
    # providers/child_safety_gate.py — the COPPA refusal at the provider boundary (the same error
    # types the host's doors send).
    "education_coppa_consent_required",
    "education_age_declaration_required",
    # matrx_batch.router.BATCH_REFUSED — an explicit batch job the host's batch admission hook
    # refused (HIPAA mode). matrx-batch sits below this package, so it is named, not imported.
    "batch_refused",
    # client_host/agent_source.AgentHasNoMessages — a saved agent with zero authored messages.
    "agent_has_no_messages",
    # client_host/agent_source.AgentHasNoModel — a saved agent whose model_id is NULL (written
    # through a door that does not fill the platform default).
    "agent_has_no_model",
    # providers/model_channel_gate.MODEL_NOT_FOR_CHAT — a realtime / embedding / transcription
    # model asked to answer a typed turn (an agent bound to a live voice model, opened in chat).
    "model_not_for_chat",
    # catalog/lifecycle.DEPRECATED_MODEL_UNSERVED — a deprecated model with no offering left,
    # asked for by name (a stale pick); named, not imported (catalog sits beside providers).
    "deprecated_model_unserved",
    # config/send_boundary.EmptyConversationError — the call carries no message to send (only a
    # system prompt, or nothing); named, not imported (config sits below providers).
    "empty_conversation",
    # mandate_taps.MandateReplayRefused — test mode refused a mandate step (nothing asked, nothing bought);
    # ``no_stand_in`` is the stand-in pass's own code for an unpinned mandate (aidream
    # services/runtime/ai_test_mode.NO_STAND_IN). Named, not imported.
    "mandate_replay_refused",
    "no_stand_in",
    # providers/errors.PROVIDER_INPUT_REFUSED — the provider could not read an attached image; named, not imported.
    "provider_input_refused",
}

#: Refusals that HOLD a run on a limit or approval someone set (each with its own human path: the
#: approval queue, the usage dialog) — expected, never a defect. The one place this split is written.
RUN_HOLD_CODES: frozenset[str] = frozenset({RUN_APPROVAL_REQUIRED, AUTOMATION_GUARDRAIL})
EXPECTED_HOLD_CODES: frozenset[str] = RUN_HOLD_CODES | {USAGE_LIMIT_REACHED}


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
        code = getattr(value, "code", None) or getattr(
            getattr(value, "error_info", None), "error_type", None
        )
        return str(code or "")
    if isinstance(value, Mapping):
        details = value.get("details")
        details = details if isinstance(details, Mapping) else {}
        for candidate in (
            value.get("code"),
            value.get("type"),
            value.get("error_type"),
            details.get("error"),
        ):
            if candidate:
                return str(candidate)
    return ""


def expected_hold_code(exc: BaseException | None) -> str:
    """The EXPECTED_HOLD_CODES code behind ``exc`` ('' when it is not a hold).

    Walks the exception and its ``__cause__`` / ``__context__`` chain, so a hold a client layer
    re-raised wrapped (``RuntimeError(...) from GuardrailStopError``, an ``AiTurnFailedError``
    carrying its turn's code) is still recognised. A background helper (the conversation
    labeler, an observational-memory pass) stopped by a hold records a refusal with this code
    and the gate's reason — never a ``system_error``: the gate already recorded the hold and
    gave it a human path (live 2026-11-14/18: "daily spend cap reached" filed as
    conversation_labeler_failed / observational_memory_pass_failed).
    """
    seen: set[int] = set()
    current: BaseException | None = exc
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        code = refusal_code(current)
        if code in EXPECTED_HOLD_CODES:
            return code
        current = current.__cause__ or current.__context__
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
    "EXPECTED_HOLD_CODES",
    "RUN_HOLD_CODES",
    "caller_refusal_codes",
    "expected_hold_code",
    "is_caller_refusal",
    "mark_caller_refusal",
    "refusal_code",
    "register_caller_refusal_code",
]
