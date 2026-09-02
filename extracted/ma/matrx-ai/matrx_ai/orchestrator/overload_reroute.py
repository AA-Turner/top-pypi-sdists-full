"""Overload-class provider failure rerouting — the decision core.

PROVIDER-REROUTABLE means the provider refused the call before doing the work. It is
defined EXPLICITLY off the classified ``RetryableError`` that
``providers/errors.py`` produces from the provider SDK exceptions — never a
bare except / string sniff here:

  • ``error_type == "rate_limit"``        — HTTP 429. SDK sources:
    ``anthropic.RateLimitError``, ``openai.RateLimitError`` (+ every
    OpenAI-compatible SDK: groq/cerebras/together/xai/fireworks),
    Google GenAI ``ClientError`` 429 / RESOURCE_EXHAUSTED,
    ``elevenlabs`` 429, generic SDK ``RateLimitError``.
  • ``error_type == "provider_overloaded"`` — HTTP 529 / "overloaded". SDK
    sources: ``anthropic.OverloadedError`` (and any APIStatusError 529),
    Google GenAI ``ServerError`` 503 / UNAVAILABLE, generic status 529.
  • ``error_type == "server_error"`` with ``status_code == 503`` — a
    service-unavailable shed from any OpenAI-compatible provider.

Model-level policy (``ai.model_definition``): ``retry_max_attempts`` caps
SAME-model retries for overload-class failures; ``retry_fallback_id`` names
the model the request reroutes to when they are exhausted. The reroute swaps
``config.model`` and lets the normal resolution pipeline
(``resolve_call_profile`` inside ``UnifiedAIClient.execute``) re-translate the
SAME canonical config for the new model — no second translation path.

Offering-level rung (2026-07, "the exact call" doctrine): BEFORE the
model-level hop, the SAME model's other available ai.offering rows are tried
in priority order (``load_offering_ladder`` + action ``reroute_offering``).
The executor sets ``config.runtime_offering_id`` — a per-request routing pin
that resolve_call_profile honors exactly and that is never persisted, so a
user's own ``offering_id`` pin survives the deviation. A PINNED offering
deviates through this rung too — these predetermined endpoint-specific error
classes are the one sanctioned deviation from a pin.

Billing rule: a paid call that produced output is never re-run — the reroute
gate requires ``produced_output=False`` (nothing streamed from the failing
model), so only calls that failed BEFORE producing output reroute.

  • ``error_type == "billing_error"`` — the selected provider account cannot
    fund the call. This skips same-route retries and proceeds directly to a
    funded sibling offering or the model's configured fallback.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from matrx_ai.providers.errors import RetryableError

# Classified error types / statuses that count as overload-class (see module
# docstring for the per-provider SDK exceptions behind each).
OVERLOAD_ERROR_TYPES: frozenset[str] = frozenset({"rate_limit", "provider_overloaded"})
OVERLOAD_STATUS_CODES: frozenset[int] = frozenset({429, 503, 529})

# ai.model_definition.retry_max_attempts default (matches the column default).
DEFAULT_RETRY_MAX_ATTEMPTS: int = 2
# Hard ceiling on fallback hops in one iteration — a mis-configured fallback
# chain must never spin the retry loop forever.
MAX_FALLBACK_HOPS: int = 3
# Ceiling on SIBLING-OFFERING hops (same model, different endpoint/api) in one
# iteration. Cycles are structurally impossible (each offering is tried at most
# once via ``offerings_tried``), but a model with many offerings must not eat
# the whole retry budget re-dialing every route.
MAX_SIBLING_OFFERING_HOPS: int = 4


class OverloadPolicy(BaseModel):
    """The model row's overload-retry policy (ai.model_definition columns)."""

    model_config = ConfigDict(frozen=True)

    retry_max_attempts: int = DEFAULT_RETRY_MAX_ATTEMPTS
    fallback_ref: str | None = None  # retry_fallback_id, stringified


class RerouteNote(BaseModel):
    """Adjustment-style record of one overload reroute — lands in the request
    metadata (persisted on the usual call record) and in the stream event."""

    model_config = ConfigDict(frozen=True)

    kind: Literal["overload_reroute"] = "overload_reroute"
    # "offering" = same model, different ai.offering (endpoint × api) — the
    # first rung of the ladder; "model" = the classic retry_fallback_id hop.
    scope: Literal["model", "offering"] = "model"
    from_model: str
    to_model: str
    from_offering_id: str | None = None
    to_offering_id: str | None = None
    attempts_on_model: int
    error_type: str
    status_code: int | None = None
    reason: str


class RerouteDecision(BaseModel):
    model_config = ConfigDict(frozen=True)

    action: Literal["retry_same", "reroute_offering", "reroute", "give_up"]
    to_model: str | None = None
    to_offering_id: str | None = None
    note: RerouteNote | None = None
    reason: str


class OfferingLadder(BaseModel):
    """The same-model offering picture for the failing dispatch: which exact
    offering just failed, and which available siblings (priority order, not yet
    tried this iteration) remain. Built by ``load_offering_ladder``."""

    model_config = ConfigDict(frozen=True)

    canonical_model_id: str
    current_offering_id: str | None = None
    sibling_offering_ids: list[str] = []


class OverloadRerouteState:
    """Per-iteration bookkeeping for the executor's retry loop.

    ``attempt_base`` is the global retry_attempt index at which the CURRENT
    model started (0 until the first reroute); attempts-on-current-model are
    counted relative to it so the fallback model gets its own fresh budget.
    """

    __slots__ = (
        "attempt_base",
        "hops",
        "models_tried",
        "notes",
        "offering_hops",
        "offerings_tried",
        "policies",
    )

    def __init__(self) -> None:
        self.attempt_base: int = 0
        self.hops: int = 0
        self.models_tried: list[str] = []
        self.notes: list[RerouteNote] = []
        self.offering_hops: int = 0
        self.offerings_tried: list[str] = []
        self.policies: dict[str, OverloadPolicy] = {}

    def record_reroute(self, *, from_model: str, note: RerouteNote, next_base: int) -> None:
        if from_model not in self.models_tried:
            self.models_tried.append(from_model)
        self.hops += 1
        self.notes.append(note)
        self.attempt_base = next_base

    def record_offering_reroute(
        self, *, from_offering_id: str | None, note: RerouteNote, next_base: int
    ) -> None:
        """A sibling-offering hop: the MODEL stays current (not appended to
        models_tried — it was not abandoned), the failed offering is burned,
        and the sibling gets its own fresh same-model retry budget."""
        if from_offering_id and from_offering_id not in self.offerings_tried:
            self.offerings_tried.append(from_offering_id)
        self.offering_hops += 1
        self.notes.append(note)
        self.attempt_base = next_base


def is_overload_error(error_info: RetryableError) -> bool:
    """True only for the explicitly enumerated overload-class classifications."""
    if error_info.error_type in OVERLOAD_ERROR_TYPES:
        return True
    return (
        error_info.error_type == "server_error"
        and error_info.status_code == 503
        and error_info.is_retryable
    )


def is_reroutable_provider_error(error_info: RetryableError) -> bool:
    """Failures safe to reroute only when the failed call produced no output."""
    return is_overload_error(error_info) or error_info.error_type == "billing_error"


def decide_overload_action(
    *,
    error_info: RetryableError,
    current_model: str,
    attempts_on_model: int,
    policy: OverloadPolicy,
    models_tried: list[str],
    hops: int,
    produced_output: bool,
    current_offering_id: str | None = None,
    sibling_offering_ids: list[str] | None = None,
    offering_hops: int = 0,
) -> RerouteDecision:
    """The ONE decision function for an overload-class provider failure.

    ``attempts_on_model`` counts FAILED provider calls on the current model in
    this iteration, INCLUDING the one that just failed (1-based). The ladder:

      1. retry_same       — while the failed-call count is within
                            1 + retry_max_attempts on the CURRENT offering.
      2. reroute_offering — the SAME model's next available sibling offering
                            (priority order, ``sibling_offering_ids``). The
                            exact same canonical config re-resolves through the
                            sibling's api rules. A PINNED offering deviates this
                            way too — predetermined endpoint-specific error
                            classes are the owner's one sanctioned deviation.
      3. reroute          — the classic model-level retry_fallback_id hop.
      4. give_up          — to the existing suspend/fail machinery.

    Rungs 2-4 all require ``produced_output=False`` — a paid call that produced
    output is never re-run anywhere.
    """
    if not is_reroutable_provider_error(error_info):
        return RerouteDecision(
            action="give_up",
            reason=f"error_type '{error_info.error_type}' is not provider-reroutable",
        )

    # Credit exhaustion is stable for the credential/endpoint. Repeating the
    # same paid route cannot recover, so enter the sibling/fallback ladder on
    # the first refusal. Transient overload retains its bounded retry budget.
    if error_info.error_type != "billing_error" and attempts_on_model <= policy.retry_max_attempts:
        return RerouteDecision(
            action="retry_same",
            reason=(
                f"{attempts_on_model} failed attempt(s) on '{current_model}' — model allows "
                f"{policy.retry_max_attempts} retry(ies) after the initial call"
            ),
        )

    if produced_output:
        return RerouteDecision(
            action="give_up",
            reason=(
                "the failing call already streamed output — a paid call that produced "
                "output is never re-run on another model"
            ),
        )

    # ── Rung 2: sibling offerings of the SAME model, before any model hop ──
    if sibling_offering_ids:
        if offering_hops >= MAX_SIBLING_OFFERING_HOPS:
            pass  # burned the offering budget — fall through to the model rung
        else:
            to_offering = sibling_offering_ids[0]
            note = RerouteNote(
                scope="offering",
                from_model=current_model,
                to_model=current_model,
                from_offering_id=current_offering_id,
                to_offering_id=to_offering,
                attempts_on_model=attempts_on_model,
                error_type=error_info.error_type,
                status_code=error_info.status_code,
                reason=(
                    f"offering '{current_offering_id or 'preferred'}' of '{current_model}' "
                    f"refused the call ({error_info.error_type}"
                    f"{f', HTTP {error_info.status_code}' if error_info.status_code else ''}) "
                    f"after {attempts_on_model} attempt(s) — rerouting to sibling offering "
                    f"'{to_offering}' of the SAME model"
                ),
            )
            return RerouteDecision(
                action="reroute_offering",
                to_model=current_model,
                to_offering_id=to_offering,
                note=note,
                reason=note.reason,
            )

    if not policy.fallback_ref:
        return RerouteDecision(
            action="give_up",
            reason=f"model '{current_model}' has no retry_fallback_id configured",
        )
    if hops >= MAX_FALLBACK_HOPS:
        return RerouteDecision(
            action="give_up",
            reason=f"fallback hop ceiling reached ({MAX_FALLBACK_HOPS})",
        )
    if policy.fallback_ref == current_model or policy.fallback_ref in models_tried:
        return RerouteDecision(
            action="give_up",
            reason=(
                f"fallback '{policy.fallback_ref}' was already tried in this iteration "
                "(cycle in the retry_fallback_id chain)"
            ),
        )

    note = RerouteNote(
        from_model=current_model,
        to_model=policy.fallback_ref,
        attempts_on_model=attempts_on_model,
        error_type=error_info.error_type,
        status_code=error_info.status_code,
        reason=(
            f"'{current_model}' refused the call ({error_info.error_type}"
            f"{f', HTTP {error_info.status_code}' if error_info.status_code else ''}) after "
            f"{attempts_on_model} attempt(s) — rerouting to retry_fallback '{policy.fallback_ref}'"
        ),
    )
    return RerouteDecision(
        action="reroute",
        to_model=policy.fallback_ref,
        note=note,
        reason=note.reason,
    )


async def load_overload_policy(model_ref: str, state: OverloadRerouteState) -> OverloadPolicy:
    """Read (and cache per-iteration) the model row's overload policy.

    Degrades to the default policy (retry_max_attempts=2, no fallback) when the
    model row cannot be read (client host without a DB-backed catalog, unknown
    ref) — the existing generic retry machinery then still applies.
    """
    cached = state.policies.get(model_ref)
    if cached is not None:
        return cached

    row = None
    try:
        from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance

        row = await ai_model_manager_instance.load_model(model_ref)
    except Exception as exc:  # noqa: BLE001 — policy lookup must never break the retry loop
        from matrx_utils import vcprint

        vcprint(
            f"[overload_reroute] could not read the model row for '{model_ref}' "
            f"({type(exc).__name__}: {exc}) — using the default overload policy "
            f"(retry_max_attempts={DEFAULT_RETRY_MAX_ATTEMPTS}, no fallback).",
            color="yellow",
        )

    raw_max = getattr(row, "retry_max_attempts", None)
    try:
        retry_max = int(raw_max) if raw_max is not None else DEFAULT_RETRY_MAX_ATTEMPTS
    except (TypeError, ValueError):
        retry_max = DEFAULT_RETRY_MAX_ATTEMPTS
    fallback = getattr(row, "retry_fallback_id", None)

    policy = OverloadPolicy(
        retry_max_attempts=max(retry_max, 0),
        fallback_ref=str(fallback) if fallback else None,
    )
    state.policies[model_ref] = policy
    return policy


async def load_offering_ladder(
    model_ref: str,
    *,
    routing_offering_id: str | None,
    offerings_tried: list[str],
) -> OfferingLadder | None:
    """Build the same-model offering picture for a failing dispatch.

    ``model_ref`` is whatever ``config.model`` holds at failure time (canonical
    name/uuid on the first attempt, the offering's provider_model_id after a
    dispatch rewrote it). ``routing_offering_id`` is the active pin (user pin or
    runtime sibling pin) — when unset the failing offering is the PREFERRED one
    (priority head). Siblings are the model's remaining available offerings in
    priority order, minus the current one and any already tried this iteration.

    Degrades to ``None`` (→ classic model-level behavior only) when the model or
    catalog cannot be read — the lookup must never break the retry loop.
    """
    try:
        from matrx_ai.catalog.manager import ai_catalog_manager
        from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance

        manager = ai_catalog_manager
        await manager.ensure_loaded()

        model = await ai_model_manager_instance.load_model(model_ref)
        model_id: str | None = str(model.id) if model is not None else None
        if model_id is None and routing_offering_id:
            pinned = manager.offering(routing_offering_id)
            if pinned is not None:
                model_id = str(pinned.model_id)
        if model_id is None:
            return None

        offerings = manager.offerings_for(model_id)
        if not offerings:
            return None

        current = routing_offering_id or offerings[0].id
        siblings = [
            o.id
            for o in offerings
            if o.id != current and o.id not in offerings_tried
        ]
        return OfferingLadder(
            canonical_model_id=model_id,
            current_offering_id=current,
            sibling_offering_ids=siblings,
        )
    except Exception as exc:  # noqa: BLE001 — ladder lookup must never break the retry loop
        from matrx_utils import vcprint

        vcprint(
            f"[overload_reroute] could not build the offering ladder for "
            f"'{model_ref}' ({type(exc).__name__}: {exc}) — sibling-offering "
            f"fallback unavailable for this failure; model-level policy still applies.",
            color="yellow",
        )
        return None


__all__ = [
    "DEFAULT_RETRY_MAX_ATTEMPTS",
    "MAX_FALLBACK_HOPS",
    "MAX_SIBLING_OFFERING_HOPS",
    "OVERLOAD_ERROR_TYPES",
    "OVERLOAD_STATUS_CODES",
    "OfferingLadder",
    "OverloadPolicy",
    "OverloadRerouteState",
    "RerouteDecision",
    "RerouteNote",
    "decide_overload_action",
    "is_overload_error",
    "load_offering_ladder",
    "load_overload_policy",
]
