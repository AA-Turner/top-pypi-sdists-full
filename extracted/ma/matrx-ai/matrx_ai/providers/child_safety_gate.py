"""The child-safety gate at the provider-call boundary. No call that reaches a model skips it.

THE GAP THIS CLOSES (lane L11f, 2026-10-18). The COPPA gate (an unconsented under-13 must not use
AI anywhere) and the minor safe-model swap (a minor never gets an operator-flagged
``age_restricted`` model) ran only in the host's two door families: ``run_ai_task`` and the
programmatic prepare hook. Every caller that went straight to ``execute_ai_request`` skipped both:
``orchestrator/parallel_executor.py``, the graph nodes (video, image, tts, llm, chat, extract),
image generation, speech, and the decision review. So did the direct paid-call seam callers (STT,
decisions, rerank, extraction).

THE RULE. The gate runs where the model is resolved, not where a door happens to be:

* :func:`admit_child_safety` with the request's ``config`` runs at the top of
  ``UnifiedAIClient._execute_dispatch``, before the catalog resolves the model. Every chat and
  media call passes there, whoever started it. The host refuses an unconsented under-13 and swaps
  an age-restricted model to its safe fallback in place on ``config.model``, so the swapped model
  is the one the catalog resolves.
* :func:`admit_child_safety` with no config runs in ``UnifiedAIClient._dispatch_with_billing_net``,
  the seam every paid call passes. There it only refuses (no model is left to swap). This covers
  the direct seam callers that never pass ``_execute_dispatch``.

The doors still run the same step first (``run_ai_task``, the prepare hook), so a refused run
assembles nothing. Here it is a cache hit: the status and the minor verdict are cached per account.

WHO IS ASKED ABOUT. The person the run belongs to: ``AppContext.user_id``. A system job (catalog
probe, indexing, embeddings) carries no person or the system account. The host's verdict for
those is "undeclared", so they pass. No call is exempt by path.

THE DECISION IS THE HOST'S. matrx-ai never imports aidream. The host registers one async
``(config | None) -> None`` step with :func:`set_child_safety_host`. The step raises
:class:`ChildSafetyRefusedError` to refuse. With no host registered, nothing is gated, and that is
announced once. A host step that fails for any other reason is logged loudly and the call is
admitted. The universal path never fails closed on a read error (the outage this posture
prevents is in ``education_compliance/coppa_gate.py``).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from matrx_utils import vcprint

from matrx_ai.providers.errors import RetryableError

#: The FE keys on these exact error types (aidream ``education_compliance/coppa_gate.py``,
#: ``CONSENT_REQUIRED_ERROR_TYPE`` / ``AGE_DECLARATION_REQUIRED_ERROR_TYPE``; a host test pins
#: the equality).
CHILD_CONSENT_REQUIRED = "education_coppa_consent_required"
AGE_DECLARATION_REQUIRED = "education_age_declaration_required"


class ChildSafetyRefusedError(Exception):
    """The run's person is an unconsented under-13 (or a guest that must declare an age first)."""

    is_caller_refusal = True
    http_status = 403

    def __init__(self, *, message: str, user_message: str, age_declaration: bool = False) -> None:
        self.code = AGE_DECLARATION_REQUIRED if age_declaration else CHILD_CONSENT_REQUIRED
        self.message = message
        self.user_message = user_message
        self.error_info = RetryableError(
            error_type=self.code,
            message=message,
            status_code=self.http_status,
            is_retryable=False,
            user_message=user_message,
            details={"error": self.code, "message": user_message},
        )
        super().__init__(message)


Gate = Callable[[Any], Awaitable[None]]

_gate: Gate | None = None
_unwired_announced = False


def set_child_safety_host(gate: Gate | None) -> None:
    """Host wiring: the async child-safety step, ``(config | None) -> None``. ``None`` unwires."""
    global _gate
    _gate = gate


def child_safety_host() -> Gate | None:
    """The registered step (the host's guard reads it to prove the wiring)."""
    return _gate


async def admit_child_safety(config: Any = None) -> None:
    """Refuse an unconsented under-13; with ``config``, also swap a minor's restricted model."""
    global _unwired_announced
    if _gate is None:
        if not _unwired_announced:
            _unwired_announced = True
            vcprint(
                "[ChildSafetyGate] no host wired. The COPPA gate and the minor model swap are NOT "
                "enforced at the provider boundary in this process.",
                color="red",
                log_level="WARNING",
            )
        return
    # A DEVICE-SERVED run (served_via) has one route: if the host's step swaps its model, the
    # run is REFUSED and the model put back — never moved to a cloud model (L5 R1).
    before_model = getattr(config, "model", None) if config is not None else None
    try:
        await _gate(config)
    except ChildSafetyRefusedError:
        raise
    except Exception as exc:  # noqa: BLE001 — a broken read never blocks a run, loudly
        vcprint(
            f"[ChildSafetyGate] host step raised ({type(exc).__name__}: {exc}). Call admitted.",
            color="red",
            log_level="ERROR",
        )
        return
    if config is not None:
        from matrx_ai.providers.device.route_guard import refuse_device_move

        refuse_device_move(config, before_model=before_model, site="the child-safety model swap")


__all__ = [
    "AGE_DECLARATION_REQUIRED",
    "CHILD_CONSENT_REQUIRED",
    "ChildSafetyRefusedError",
    "admit_child_safety",
    "child_safety_host",
    "set_child_safety_host",
]
