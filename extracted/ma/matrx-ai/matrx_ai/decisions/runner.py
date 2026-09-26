"""Catalog-routed, non-chat decision runner.

The provider adapter owns its retry policy.  This module owns admission,
catalog routing, credential selection, and the common result/cost shape used by
HTTP and direct consumers.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from matrx_ai.catalog import CatalogRoutingError, ResolvedCallProfile, resolve_call_profile
from matrx_ai.config import TokenUsage
from matrx_ai.config.usage_config import ensure_pricing_lookup
from matrx_ai.providers.admission import admit_provider_call
from matrx_ai.providers.errors import (
    attach_billed_usage,
    get_billed_usage,
    report_unbilled_provider_failure,
)
from matrx_ai.providers.keys import resolve_api_key
from matrx_ai.providers.typesafe import (
    DEFAULT_BASE_URL,
    SystemOneRequest,
    SystemOneResult,
    call_system_one,
)
from matrx_ai.providers.typesafe.client import Answer, Question, SystemOneState


class DecisionAdmissionError(CatalogRoutingError):
    """Raised before a provider call when a catalog route is not a decision route."""


@dataclass(frozen=True)
class DecisionRequest:
    """A model reference plus atomic provider-native state/questions."""

    model: str
    state: SystemOneState
    questions: dict[str, Question]


@dataclass(frozen=True)
class DecisionExecutionResult:
    """The stable result shape shared by every decision consumer."""

    model: str
    answers: dict[str, Answer]
    usage: TokenUsage
    request_id: str | None
    cost_usd: float
    offering_id: str
    route: str
    profile: ResolvedCallProfile

    def model_dump(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "answers": {key: answer.model_dump(mode="json") for key, answer in self.answers.items()},
            "usage": {
                "input_tokens": self.usage.input_tokens,
                "output_tokens": self.usage.output_tokens,
            },
            "request_id": self.request_id,
            "cost_usd": self.cost_usd,
            "offering_id": self.offering_id,
            "route": self.route,
        }


def _require_decision_profile(profile: ResolvedCallProfile) -> None:
    if profile.wire_format != "typesafe_systemone":
        raise DecisionAdmissionError(
            f"Offering {profile.offering_id!r} is not a native decision route."
        )
    # Capability vocabulary rollout may represent decision as a new interaction.
    # Do not coerce a normal turn route into this transport while old rows exist.
    if getattr(profile.capabilities, "interaction", None) != "decision":
        raise DecisionAdmissionError(
            f"Offering {profile.offering_id!r} is not declared for decision interaction."
        )


async def execute_decision(
    request: DecisionRequest,
    *,
    offering_id: str | None = None,
    profile: ResolvedCallProfile | None = None,
    profile_resolver: Callable[..., Awaitable[ResolvedCallProfile]] = resolve_call_profile,
    caller: Callable[..., Awaitable[SystemOneResult]] | None = None,
) -> DecisionExecutionResult:
    """Resolve and execute exactly one native decision provider call.

    THIS IS THE ENGINE, and it now has two callers: the standalone decision
    route (HTTP + the workflow action) and ``UnifiedAIClient.execute``'s
    ``typesafe_systemone`` translator, which hands in the profile it already
    resolved. Both paths get the same admission, credential selection, pricing
    and billed-usage handling from here — there is exactly one place that pays
    TypeSafe.

    MANDATES (2026-09-25): this is PROVIDER-LAYER machinery, not a decision
    maker — it chooses no model and no questions; both arrive on ``request``.
    Its callers are the ones held: ``UnifiedAIClient`` (below an already-held
    funnel call), the ``ai.decision`` workflow step (held by
    ``workflow.step_intelligence``), and the ``/ai/decisions`` API (a declared
    pass-through — the API caller names the model).

    Invalid request bodies are validated by ``SystemOneRequest`` before any
    credential lookup or transport activity.  This function intentionally does
    not instantiate ``UnifiedConfig`` or use ``UnifiedAIClient``.
    """
    # Resolved at CALL time, not bound as a default at import time: a default
    # argument freezes the module attribute, so a caller (or a guard) that
    # replaces ``call_system_one`` would be silently ignored and a test would
    # reach the real transport.
    caller = caller or call_system_one
    wire_request = SystemOneRequest(
        state=request.state,
        model=request.model,
        questions=request.questions,
    )
    # ``profile`` is passed by UnifiedAIClient, which has already resolved the
    # catalog route for this call. Re-resolving would be a second catalog read
    # that could legally disagree with the one the client dispatched on.
    if profile is None:
        profile = await profile_resolver(request.model, offering_id=offering_id)
    _require_decision_profile(profile)

    # A per-offering BYOK key is resolved through the normal host/AppContext
    # resolver.  The platform key remains the adapter's canonical fallback.
    api_key = resolve_api_key(profile.byok_secret_key) if profile.byok_secret_key else None
    dispatched = wire_request.model_copy(update={"model": profile.provider_model_id})
    pricing = await ensure_pricing_lookup()
    if profile.offering_id not in pricing:
        raise DecisionAdmissionError(
            f"Offering {profile.offering_id!r} has no resolved catalog pricing."
        )
    raw: SystemOneResult | None = None
    try:
        async with admit_provider_call(profile):
            raw = await caller(
                dispatched,
                api_key=api_key,
                # The vendor host belongs to the provider adapter, never this engine.
                base_url=profile.base_url or DEFAULT_BASE_URL,
            )
    except Exception as exc:
        billed = get_billed_usage(exc)
        if billed is not None:
            billed.matrx_model_name = profile.model_name
            billed.provider_model_name = profile.provider_model_id
            billed.api = profile.vendor
            billed.offering_id = profile.offering_id
            billed.offering_route = profile.resolution_route
        else:
            report_unbilled_provider_failure(
                exc, provider=profile.vendor, model=profile.provider_model_id
            )
        raise
    if raw is None:
        raise DecisionAdmissionError("Decision transport ended without a provider response.")
    usage = TokenUsage(
        input_tokens=raw.usage.input_tokens or 0,
        output_tokens=raw.usage.output_tokens or 0,
        matrx_model_name=profile.model_name,
        provider_model_name=raw.model,
        api=profile.vendor,
        response_id=raw.request_id or "",
        offering_id=profile.offering_id,
        offering_route=profile.resolution_route,
        raw_usage={
            "input_tokens": raw.usage.input_tokens,
            "output_tokens": raw.usage.output_tokens,
        },
    )
    cost = usage.calculate_catalog_cost(pricing)
    if cost is None:
        error = DecisionAdmissionError("Catalog pricing could not price the decision response.")
        attach_billed_usage(error, usage)
        raise error
    return DecisionExecutionResult(
        model=raw.model,
        answers=raw.answers,
        usage=usage,
        request_id=raw.request_id,
        cost_usd=cost,
        offering_id=profile.offering_id,
        route=profile.resolution_route,
        profile=profile,
    )
