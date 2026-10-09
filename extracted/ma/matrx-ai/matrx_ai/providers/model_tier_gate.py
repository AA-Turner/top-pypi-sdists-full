"""The top-tier model gate — a model rated 6 (Claude Mythos, Claude Fable, GPT-6 Astra, every
"-max") runs only for a person whose top-tier access is on (Arman, 2026-10-08:
"The only user who should be able to run those is me ... everyone is off").

Same seam as the usage gate and the run-approval gate: ``UnifiedAIClient._dispatch_with_billing_net``,
the one place every paid provider call passes, BEFORE any money is spent. Unlike those two it
is asked on EVERY paid call, not once per request: one run may hand a sub-agent or a workflow
step a different model, and that call is judged on its own model.

WHO IS ASKED ABOUT. The person the run belongs to — ``AppContext.user_id``. A person's chat,
their sub-agents, mandates, workflows, scheduled jobs and API calls all carry that id. A system
or bot run carries the system account's id and is refused unless that account itself is on.
No origin is exempt: a person typing in their own chat is gated exactly like an automation.

NO FALLBACK. A refusal is a caller refusal (``is_caller_refusal``): never retried, rerouted to
another model or filed as a provider failure. The run fails with one plain sentence.

THE DECISION IS THE HOST'S. matrx-ai never imports aidream: the host registers a SYNCHRONOUS
``user_id -> bool | None`` memory read with :func:`set_top_tier_access_resolver` (None = "I do
not know yet", which refuses). With none registered, top-tier calls are admitted and that is
announced once — a standalone install has no people to gate.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from matrx_utils import vcprint

from matrx_ai.providers.errors import RetryableError

#: ai.model_definition.cost_rating of the top tier.
TOP_TIER_COST_RATING = 6
TOP_TIER_MODEL_REFUSED = "top_tier_model_refused"
TOP_TIER_MESSAGE = "This model is limited to approved accounts"


class TopTierModelRefusedError(Exception):
    """The run's person does not have top-tier model access."""

    is_caller_refusal = True
    http_status = 403

    def __init__(self, *, model_name: str, model_id: str, user_id: str) -> None:
        self.model_name = model_name
        self.model_id = model_id
        self.user_id = user_id
        self.code = TOP_TIER_MODEL_REFUSED
        self.message = f"{TOP_TIER_MESSAGE} ({model_name or model_id}). Not run; no other model was used."
        self.error_info = RetryableError(
            error_type=self.code,
            message=self.message,
            status_code=self.http_status,
            is_retryable=False,
            user_message=self.message,
            details=self.envelope(),
        )
        super().__init__(self.message)

    def envelope(self) -> dict[str, Any]:
        return {
            "error": self.code,
            "message": self.message,
            "model_id": self.model_id,
            "model_name": self.model_name,
            "user_id": self.user_id,
        }


Resolver = Callable[[str], "bool | None"]

_resolver: Resolver | None = None
_unwired_announced = False


def set_top_tier_access_resolver(resolver: Resolver | None) -> None:
    """Host wiring: a SYNCHRONOUS ``user_id -> bool | None`` memory read (None = unknown → refused)."""
    global _resolver
    _resolver = resolver


def is_top_tier(profile: Any) -> bool:
    rating = getattr(profile, "model_cost_rating", None)
    return rating is not None and int(rating) >= TOP_TIER_COST_RATING


def refusal_for(profile: Any, ctx: Any) -> TopTierModelRefusedError | None:
    """The refusal this call would get right now, or None. No side effect."""
    global _unwired_announced
    if not is_top_tier(profile):
        return None
    if _resolver is None:
        if not _unwired_announced:
            _unwired_announced = True
            vcprint(
                "[TopTierGate] no resolver wired by the host — top-tier models are NOT "
                "limited to approved accounts in this process.",
                color="red",
                log_level="WARNING",
            )
        return None
    user_id = str(getattr(ctx, "user_id", "") or "") if ctx is not None else ""
    allowed: bool | None
    if not user_id:
        allowed = False
    else:
        try:
            allowed = _resolver(user_id)
        except Exception as exc:  # noqa: BLE001 — an unreadable answer refuses (fail closed)
            vcprint(
                f"[TopTierGate] resolver raised ({type(exc).__name__}: {exc}) — call refused.",
                color="red",
                log_level="ERROR",
            )
            allowed = None
    if allowed is True:
        return None
    return TopTierModelRefusedError(
        model_name=str(getattr(profile, "model_name", "") or ""),
        model_id=str(getattr(profile, "model_id", "") or ""),
        user_id=user_id,
    )


def admit_model_tier(profile: Any) -> None:
    """Admit or refuse the paid call about to be made on ``profile``'s model."""
    from matrx_ai.context.app_context import try_get_app_context

    refusal = refusal_for(profile, try_get_app_context())
    if refusal is not None:
        vcprint(
            f"[TopTierGate] refused user={refusal.user_id or '<none>'} model={refusal.model_name}",
            color="yellow",
            log_level="WARNING",
        )
        raise refusal


__all__ = [
    "TOP_TIER_COST_RATING",
    "TOP_TIER_MESSAGE",
    "TOP_TIER_MODEL_REFUSED",
    "TopTierModelRefusedError",
    "admit_model_tier",
    "is_top_tier",
    "refusal_for",
    "set_top_tier_access_resolver",
]
