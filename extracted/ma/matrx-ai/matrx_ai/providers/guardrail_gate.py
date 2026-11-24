"""The automation guardrail gate — every automatic run stops at its limits (Arman, 2026-10-09:
"Any AI task that runs automatically ALWAYS has max cost and max turns set, even if very high.
Without them it cannot run automatically").

Same seam as the usage, run-approval and readiness gates: ``UnifiedAIClient._dispatch_with_billing_net``,
the one place every paid provider call passes. Unlike the run-approval gate it is asked on EVERY
paid call, because the limits it enforces are reached MID-run:

* max turns per run — the next paid call of a conversation that already used its turns;
* max cost per run — the next paid call of a run that already spent its budget;
* daily / weekly / monthly caps — the next paid call that would run past the automation's cap
  (the host pauses the automation);
* missing limits — an automation that uses AI but carries no max turns / max cost is refused.

A stop is a CALLER refusal (``is_caller_refusal``): never retried, rerouted or filed as a provider
failure. Every turn already taken keeps its output — the gate only refuses the NEXT call.

THE DECISION IS THE HOST'S. matrx-ai never imports aidream: the host registers, with
:func:`set_guardrail_host`, a synchronous ``(ctx) -> bool`` "is this run guarded" read, a
synchronous ``(ctx, profile) -> GuardrailStopError | None`` resolver (memory only — it also counts
the admitted call as a turn), a synchronous ``(ctx, cost_usd) -> None`` accrual, and the run budget's
``budget_reserve(ctx, quote)`` (reserve each call's worst case before it is sent; § THE RUN BUDGET
RESERVATION below). With none registered nothing is gated (announced once).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

from matrx_utils import vcprint

from matrx_ai.providers.errors import RetryableError

AUTOMATION_GUARDRAIL = "automation_guardrail"
FIX_ACTION_RAISE_LIMIT = "raise_automation_limit"


class GuardrailStopError(Exception):
    """An automatic run reached (or lacks) one of its guardrail limits. The next call was not made."""

    is_caller_refusal = True
    http_status = 429

    def __init__(
        self,
        *,
        kind: str,
        subject_kind: str,
        subject_id: str,
        limit: float | int | None,
        observed: float | int | None,
        message: str,
        run_key: str = "",
        pauses: bool = False,
    ) -> None:
        self.kind = kind
        self.subject_kind = subject_kind
        self.subject_id = subject_id
        self.limit = limit
        self.observed = observed
        self.run_key = run_key
        self.pauses = pauses
        self.message = message
        self.code = AUTOMATION_GUARDRAIL
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
            "fix_action": FIX_ACTION_RAISE_LIMIT,
            "guardrail": self.kind,
            "limit": self.limit,
            "observed": self.observed,
            "subject_kind": self.subject_kind,
            "subject_id": self.subject_id,
            "pauses": self.pauses,
        }


Guarded = Callable[[Any], bool]
Resolver = Callable[[Any, Any], "GuardrailStopError | None"]
Accrue = Callable[[Any, float], None]
#: ``(ctx, profile, config) -> GuardrailStopError | None`` — asked on EVERY paid call, automation or
#: not: the platform kill switch, per-account daily ceilings, the per-call input-size cap.
EveryCall = Callable[[Any, Any, Any], "GuardrailStopError | None"]

_guarded: Guarded | None = None
_resolver: Resolver | None = None
_accrue: Accrue | None = None
_every_call: EveryCall | None = None
_every_call_tracked: Guarded | None = None
_every_call_accrue: Accrue | None = None
#: ``(ctx, usage) -> None`` — the provider's own token figures after a call (calibrates estimates).
_every_call_usage: Callable[[Any, Any], None] | None = None
#: ``(ctx, usage, estimate_usd) -> None`` — a paid call whose price is UNKNOWN (no resolvable
#: catalog price). The host alarms; caps and run limits accrue ``estimate_usd`` (conservative).
_every_call_unpriced: Callable[[Any, Any, float], None] | None = None
_unwired_announced = False
#: ``(ctx) -> str | None`` — asked at each tool-round boundary of a guarded run: the directive for its ONE tool-less
#: closing turn when only one more call fits its per-run budget (the executor switches tools off, as at the
#: iteration ceiling), else None. The budget stop then never lands past the line with no word from the model.
_budget_wrap_up: Callable[[Any], str | None] | None = None
#: ``(ctx) -> str | None`` — asked at the same boundary: once per run, a few calls before the wrap-up, the directive
#: (tools stay ON) to finish the unit in hand and start nothing new, so the stop lands at a natural boundary.
_budget_finish_unit: Callable[[Any], str | None] | None = None


def _ask_budget_host(resolver: Callable[[Any], str | None] | None, what: str) -> str | None:
    if resolver is None:
        return None
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None or not _is_guarded(ctx):
        return None
    try:
        return resolver(ctx)
    except Exception as exc:  # noqa: BLE001 — a broken memory read never blocks a run; the hard stop still holds
        vcprint(f"[GuardrailGate] budget {what} resolver raised ({type(exc).__name__}: {exc}).", color="red",
                log_level="ERROR")
        return None


def budget_finish_unit_notice() -> str | None:
    """The host's finish-the-unit directive for the current run, or None (unwired, unguarded, room left)."""
    return _ask_budget_host(_budget_finish_unit, "finish-unit")


def budget_wrap_up_notice() -> str | None:
    """The host's budget wrap-up directive for the current run, or None (unwired, unguarded, room left)."""
    if _budget_wrap_up is None:
        return None
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None or not _is_guarded(ctx):
        return None
    try:
        return _budget_wrap_up(ctx)
    except Exception as exc:  # noqa: BLE001 — a broken memory read never blocks a run; the hard stop still holds
        vcprint(f"[GuardrailGate] budget wrap-up resolver raised ({type(exc).__name__}: {exc}).", color="red",
                log_level="ERROR")
        return None


def set_guardrail_host(
    *,
    guarded: Guarded | None,
    resolver: Resolver | None,
    accrue: Accrue | None,
    every_call: EveryCall | None = None,
    every_call_tracked: Guarded | None = None,
    every_call_accrue: Accrue | None = None,
    every_call_usage: Callable[[Any, Any], None] | None = None,
    every_call_unpriced: Callable[[Any, Any, float], None] | None = None,
    budget_wrap_up: Callable[[Any], str | None] | None = None,
    budget_finish_unit: Callable[[Any], str | None] | None = None,
    budget_reserve: BudgetReserve | None = None,
    budget_room_wait: Callable[[Any, CallQuote | None], float | None] | None = None,
    route_worst: Callable[[Any], Awaitable[float | None]] | None = None,
    prime_run: Callable[[Any], Awaitable[None]] | None = None,
) -> None:
    """Host wiring: SYNCHRONOUS memory reads/writes. ``None`` everywhere unwires.

    ``guarded`` / ``resolver`` / ``accrue`` — the automation subject's own limits.
    ``every_call`` / ``every_call_tracked`` / ``every_call_accrue`` — platform-wide limits asked on
    every paid call (kill switch, account ceilings, input size)."""
    global _guarded, _resolver, _accrue, _every_call, _every_call_tracked, _every_call_accrue, _every_call_usage
    global _every_call_unpriced, _budget_wrap_up, _budget_finish_unit, _budget_reserve
    _budget_reserve = budget_reserve
    global _budget_room_wait
    _budget_room_wait = budget_room_wait
    global _route_worst, _prime_run
    _route_worst = route_worst
    _prime_run = prime_run
    _budget_wrap_up = budget_wrap_up
    _budget_finish_unit = budget_finish_unit
    _every_call_usage = every_call_usage
    _every_call_unpriced = every_call_unpriced
    _guarded = guarded
    _resolver = resolver
    _accrue = accrue
    _every_call = every_call
    _every_call_tracked = every_call_tracked
    _every_call_accrue = every_call_accrue


_prime_run: Callable[[Any], Awaitable[None]] | None = None


async def prime_guardrails() -> None:
    """Await the host's per-run preparation (``prime_run``: the run's spend banked by earlier processes) before
    the admission of EVERY paid call, so a direct dispatch outside a model step (STT, rerank, media) is admitted
    against the run's real total too (cost adversary pass 5, F6). After the first call of a run it is a lookup.
    Never raises."""
    if _prime_run is None:
        return
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None or not _is_guarded(ctx):
        return
    try:
        await _prime_run(ctx)
    except Exception as exc:  # noqa: BLE001 — the in-process count still holds
        vcprint(f"[guardrail] could not prime the run budget: {exc!r}", color="red", log_level="ERROR")


def _is_guarded(ctx: Any) -> bool:
    if ctx is None or _guarded is None:
        return False
    try:
        return bool(_guarded(ctx))
    except Exception as exc:  # noqa: BLE001 — a broken read never blocks a run, loudly
        vcprint(
            f"[GuardrailGate] guarded() raised ({type(exc).__name__}: {exc}) — call admitted.",
            color="red",
            log_level="ERROR",
        )
        return False


def _tracked(ctx: Any) -> bool:
    if ctx is None or _every_call_tracked is None:
        return False
    try:
        return bool(_every_call_tracked(ctx))
    except Exception:  # noqa: BLE001
        return False


# --------------------------------------------------------------------------- #
# THE PER-CALL SPEND CAP (2026-10-27)                                          #
# --------------------------------------------------------------------------- #
#
# A caller that must keep EACH call cheap (a workflow AI step's ``max_call_cost_usd``) opens
# :func:`call_spend_cap_scope`; every paid call made inside it is priced BEFORE it is sent — the
# exact outgoing request's estimated input tokens plus its output ceiling (``max_output_tokens``)
# at the model's catalog price — and refused over the cap. A call that cannot be priced (no
# output ceiling, no catalog price) is refused too: a cap that cannot be checked is not a cap.
# Nothing is spent on a refused call. No scope: one ContextVar read.

CALL_SPEND_CAP = "call_spend_cap"
FIX_ACTION_RAISE_CALL_CAP = "raise_call_spend_cap"


@dataclass(frozen=True)
class CallSpendCap:
    max_usd: float
    subject: str


_CALL_SPEND_CAP: ContextVar[CallSpendCap | None] = ContextVar("matrx_call_spend_cap", default=None)


@contextmanager
def call_spend_cap_scope(max_usd: float | None, *, subject: str) -> Iterator[CallSpendCap | None]:
    """Cap every paid call inside the block at ``max_usd`` (``None`` / ``<= 0``: no cap)."""
    if max_usd is None or max_usd <= 0:
        yield None
        return
    cap = CallSpendCap(max_usd=float(max_usd), subject=subject)
    token = _CALL_SPEND_CAP.set(cap)
    try:
        yield cap
    finally:
        _CALL_SPEND_CAP.reset(token)


def current_call_spend_cap() -> CallSpendCap | None:
    """The per-call cap open around this call, if any (the send boundary bounds its document
    ceiling by it — ``send_boundary._bound_ceiling_by_spend_cap``)."""
    return _CALL_SPEND_CAP.get()


def _call_cap_stop(cap: CallSpendCap, message: str, observed: float | None) -> GuardrailStopError:
    stop = GuardrailStopError(
        kind=CALL_SPEND_CAP,
        subject_kind="workflow_step",
        subject_id=cap.subject,
        limit=cap.max_usd,
        observed=observed,
        message=message,
    )
    stop.error_info.details["fix_action"] = FIX_ACTION_RAISE_CALL_CAP
    return stop


def estimate_call_usd(profile: Any, config: Any) -> tuple[float | None, str, int, int]:
    """``(usd | None, model, input_tokens, output_tokens)`` for the call about to be sent: the
    ONE prompt estimator over the exact config, plus its output ceiling, at the catalog price."""
    from matrx_ai.config.context_preflight import estimate_prompt_tokens
    from matrx_ai.config.usage_config import TokenUsage, _get_db_pricing_lookup

    model = str(
        getattr(profile, "model_name", None)
        or getattr(config, "matrx_model_name", None)
        or getattr(config, "model", None)
        or ""
    )
    input_tokens = max(1, int(estimate_prompt_tokens(config)))
    output_tokens = int(getattr(config, "max_output_tokens", None) or 0)
    if not model or output_tokens <= 0:
        return None, model, input_tokens, output_tokens
    usage = TokenUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        matrx_model_name=model,
        offering_id=str(getattr(profile, "offering_id", None) or ""),
    )
    cost = usage.calculate_catalog_cost(_get_db_pricing_lookup())
    return (None if cost is None else float(cost)), model, input_tokens, output_tokens


def admit_call_spend_cap(profile: Any = None, config: Any = None) -> None:
    """Refuse the call about to be sent when it is estimated over the open per-call cap."""
    cap = _CALL_SPEND_CAP.get()
    if cap is None:
        return
    from matrx_ai.cost_text import person_cost_text

    cap_text = person_cost_text(cap.max_usd)  # a person reads this stop: points, never dollars (law 14)
    if config is None:
        raise _call_cap_stop(
            cap,
            f"{cap.subject} has a {cap_text} cap per AI call, but this call carries no "
            "request to price. Nothing was sent or charged.",
            None,
        )
    try:
        usd, model, input_tokens, output_tokens = estimate_call_usd(profile, config)
    except Exception as exc:  # noqa: BLE001 — an unpriceable call is refused, never waved through
        usd, model, input_tokens, output_tokens = None, "", 0, 0
        vcprint(f"[GuardrailGate] call spend cap could not price the call: {exc!r}", color="red")
    if output_tokens <= 0:
        raise _call_cap_stop(
            cap,
            f"{cap.subject} has a {cap_text} cap per AI call, but the call has no longest-"
            "answer limit, so its price cannot be checked. Set the step's max output tokens. "
            "Nothing was sent or charged.",
            None,
        )
    if usd is None:
        raise _call_cap_stop(
            cap,
            f"{cap.subject} has a {cap_text} cap per AI call, but {model or 'its model'} has "
            "no catalog price, so the call cannot be checked. Nothing was sent or charged.",
            None,
        )
    if usd > cap.max_usd:
        raise _call_cap_stop(
            cap,
            f"{cap.subject} would cost about {person_cost_text(usd)} on {model} ({input_tokens:,} tokens in, up "
            f"to {output_tokens:,} out), over its {cap_text} cap per AI call. Nothing was "
            "sent or charged.",
            round(usd, 6),
        )


# --------------------------------------------------------------------------- #
# THE RUN BUDGET RESERVATION (P8-RUNS, 2026-11-17)                             #
# --------------------------------------------------------------------------- #
#
# A guarded run never STARTS a call it cannot afford, counting what it spent plus what is reserved
# for calls in flight. Before each paid call (the first included) the gate prices the call's WORST
# CASE from the exact request — the input tokens at send time at the cache-read rate for the prefix
# the provider holds warm and the higher of the input / cache-write rate for the rest, plus
# ``max_output_tokens`` at the output rate — and the HOST reserves it against the run
# (``budget_reserve``). When the worst case does not fit but a smaller answer would, the host caps
# the call's ``max_output_tokens`` (down to its floor knob) and the run is told so; only when even
# the floor does not fit is the call refused. On completion the reservation is replaced by the
# actual cost (``note_paid_result``); a call that errors, is stopped or whose task ends without a
# result releases it (the dispatch task's done callback, the next admission in the same task, and
# the host's lease). The ledger and its math live in the host; this module only prices and carries.


@dataclass(frozen=True)
class CallQuote:
    """The worst case of ONE paid call, priced from its exact request before it is sent (USD per token)."""

    model: str
    input_tokens: int
    max_output_tokens: int
    cold_input_rate: float
    warm_input_rate: float
    output_rate: float

    def input_usd(self, warm_tokens: int = 0) -> float:
        warm = max(0, min(int(warm_tokens), self.input_tokens))
        return warm * self.warm_input_rate + (self.input_tokens - warm) * self.cold_input_rate

    def worst_usd(self, warm_tokens: int = 0, output_tokens: int | None = None) -> float:
        out = self.max_output_tokens if output_tokens is None else output_tokens
        return self.input_usd(warm_tokens) + max(0, int(out)) * self.output_rate

    def output_tokens_affordable(self, usd: float, warm_tokens: int = 0) -> int:
        """The most output tokens ``usd`` buys after this call's input (never above its own ceiling)."""
        left = usd - self.input_usd(warm_tokens)
        if left <= 0:
            return 0
        if self.output_rate <= 0:
            return self.max_output_tokens
        return min(self.max_output_tokens, int(left / self.output_rate))


#: ``(ctx, quote | None) -> reservation | GuardrailStopError | None`` — the host's run-budget door, asked
#: on every paid call of a guarded run. A reservation has ``max_output_tokens`` (the capped answer ceiling,
#: or None when the asked one fits), ``notice`` (the sentence the run is told, or None), ``settle(cost, usage)``
#: and ``release()``; both are idempotent.
BudgetReserve = Callable[[Any, "CallQuote | None"], Any]
_budget_reserve: BudgetReserve | None = None
#: The reservation of the call this context is dispatching (settled by ``note_paid_result``).
_OPEN_RESERVATION: ContextVar[tuple[Any, Any] | None] = ContextVar("matrx_run_budget_reservation", default=None)
_unpriced_quote_announced: set[str] = set()
_NOTICE_TASKS: set[Any] = set()


def _tier_rates(tier: Any) -> tuple[float, float, float]:
    """``(cold, warm, output)`` USD per token from a catalog tier: a token not in the cache costs the
    higher of the input and cache-write rate; a warm token the cache-read rate."""
    m = 1_000_000.0
    input_price = float(tier.input_price or 0.0)
    write = float(getattr(tier, "cache_write_5m_price", None) or 0.0)
    read = getattr(tier, "cache_hit_price", None)
    if read is None:
        read = getattr(tier, "cached_input_price", None)
    read = input_price if read is None else float(read)
    return max(input_price, write) / m, min(read, input_price) / m, float(tier.output_price or 0.0) / m


def _route_tier(profile: Any, units: int, *, synthetic_ok: bool) -> Any:
    """The catalog pricing tier of ``profile``'s route at ``units``, or None. Never raises."""
    from matrx_ai.config.usage_config import (
        SYNTHETIC_USAGE_BASES,
        _get_db_pricing_lookup,
        lookup_model_pricing,
    )

    model = str(getattr(profile, "model_name", None) or "")
    if not model:
        return None
    pricing = lookup_model_pricing(
        _get_db_pricing_lookup(),
        offering_id=str(getattr(profile, "offering_id", None) or ""),
        model_name=model,
        provider_model_name=str(getattr(profile, "provider_model_id", None) or ""),
        api=str(getattr(profile, "vendor", None) or ""),
    )
    tier = pricing.get_tier(max(1, int(units))) if pricing else None
    if tier is None:
        return None
    if not synthetic_ok and tier.usage_basis is not None and tier.usage_basis in SYNTHETIC_USAGE_BASES:
        return None
    return tier


def quote_tokens(profile: Any, input_tokens: int, output_tokens: int) -> CallQuote | None:
    """The worst case of a token-priced call with no chat config (embeddings, decisions, extraction): ``input_tokens``
    at the cold rate plus ``output_tokens`` at the output rate, from the route's catalog tier. None when unpriced."""
    try:
        tier = _route_tier(profile, input_tokens, synthetic_ok=False)
        if tier is None:
            return None
        cold, warm, out = _tier_rates(tier)
        return CallQuote(str(profile.model_name), max(1, int(input_tokens)), max(0, int(output_tokens)), cold, warm, out)
    except Exception as exc:  # noqa: BLE001
        vcprint(f"[GuardrailGate] run budget could not price a token call: {exc!r}", color="red", log_level="ERROR")
        return None


def quote_units(profile: Any, units: int) -> CallQuote | None:
    """The worst case of a call billed in the route's own synthetic units (STT audio units, rerank search units):
    ``units`` at the tier's input price, exactly as the settle prices ``TokenUsage(input_tokens=units)``. None when
    the route has no catalog price."""
    try:
        tier = _route_tier(profile, units, synthetic_ok=True)
        if tier is None:
            return None
        rate = float(tier.input_price or 0.0) / 1_000_000.0
        if rate <= 0.0:
            # A per-search service (Cohere rerank) is priced by ``component_prices["search_units"]`` with
            # ``input_price`` 0 (so its units are never billed twice at settle); quoting that tier at its input
            # price would hold $0 for a call that costs real money.
            rate = float((getattr(tier, "component_prices", None) or {}).get("search_units") or 0.0) / 1_000_000.0
        return CallQuote(str(profile.model_name), max(1, int(units)), 0, rate, rate, 0.0)
    except Exception as exc:  # noqa: BLE001
        vcprint(f"[GuardrailGate] run budget could not price a unit call: {exc!r}", color="red", log_level="ERROR")
        return None


#: ``(profile) -> usd | None`` (async) — what the host holds for a call of a route from its recorded calls (a high
#: percentile of its recent priced calls, never below the unpriced amount when some were unpriced).
_route_worst: Callable[[Any], Awaitable[float | None]] | None = None


def fixed_quote(model: str, usd: float) -> CallQuote:
    """A worst case known only as an amount (what a route's recorded calls say one call can cost)."""
    usd = max(0.0, float(usd))
    return CallQuote(model, 1, 0, usd, usd, 0.0)


async def route_history_quote(profile: Any) -> CallQuote | None:
    """The worst case of a call that cannot be priced from its request: what the route's recorded calls say one call
    can cost (the host reads them, cached). None when the route has no history (the host then reserves its
    unpriced amount). Never raises."""
    if _route_worst is None or profile is None:
        return None
    try:
        usd = await _route_worst(profile)
    except Exception as exc:  # noqa: BLE001
        vcprint(f"[GuardrailGate] route cost history read failed ({exc!r}); the unpriced amount is held.",
                color="red", log_level="ERROR")
        return None
    return None if usd is None else fixed_quote(str(getattr(profile, "model_name", "") or ""), usd)


def _config_text_characters(config: Any) -> int:
    """The characters of text a request sends (system prompt and every text part): what a TTS route bills."""
    total = len(str(getattr(config, "system_instruction", None) or ""))
    for message in getattr(config, "messages", None) or ():
        content = getattr(message, "content", None)
        if isinstance(content, str):
            total += len(content)
            continue
        for part in content or ():
            text = getattr(part, "text", None)
            if isinstance(text, str):
                total += len(text)
    return total


def provider_default_duration_seconds(profile: Any) -> int | None:
    """The seconds of media ``profile``'s provider makes when a request names no duration, read from the provider
    class that applies it (``BaseMediaGeneration.DEFAULT_DURATION_SECONDS``, e.g. Veo's 8 in
    ``google_video_api.py``): one home, so the quote and the wire agree. None when the route's provider class has no
    such default or cannot be resolved. Never raises."""
    attr = str(getattr(profile, "client_attr", None) or "")
    if not attr:
        return None
    try:
        import matrx_ai.providers as providers
        from matrx_ai.providers.unified_client import UnifiedAIClient

        factory = UnifiedAIClient._PROVIDER_FACTORIES.get(attr)
        cls = getattr(providers, factory) if factory else None
        seconds = getattr(cls, "DEFAULT_DURATION_SECONDS", None) if cls is not None else None
        return int(seconds) if seconds and int(seconds) > 0 else None
    except Exception as exc:  # noqa: BLE001 — unresolved: the route's history prices the call instead
        vcprint(f"[GuardrailGate] could not read the provider's default duration for {attr!r}: {exc!r}",
                color="red", log_level="ERROR")
        return None


def _unit_priced_worst_usd(tier: Any, config: Any, input_tokens: int, profile: Any = None) -> float | None:
    """The worst case of a call its catalog prices per unit, from the units the request asks for, exactly as the
    settle prices them (units x ``tokens_per_unit`` synthetic tokens at the basis's $/1M rate), plus its prompt at
    the input rate when the basis bills output units. A per-second request that names no duration is priced at the
    duration its provider makes by default (:func:`provider_default_duration_seconds`; cost adversary pass 6, N4: a
    Veo request leaves it to the provider's 8 s). None when the units are still unknown (a computed basis with no
    duration and no provider default, megapixels, minutes): the route's history is used instead."""
    from matrx_ai.config.usage_config import USAGE_BASIS_SPECS

    spec = USAGE_BASIS_SPECS.get(tier.usage_basis)
    if spec is None:
        return None
    count = max(1, int(getattr(config, "count", None) or 1))
    seconds = int(getattr(config, "duration_seconds", None) or 0)
    if seconds <= 0 and spec.unit == "second":
        seconds = provider_default_duration_seconds(profile) or 0
    if spec.unit in ("image", "clip", "track"):
        units = count
    elif spec.unit == "second":
        if seconds <= 0:
            return None
        units = seconds * count
    elif spec.unit == "character":
        units = _config_text_characters(config)
        if units <= 0:
            return None
    else:
        return None
    m = 1_000_000.0
    if spec.billing_field == "output_tokens":
        rate = float(tier.output_price or 0.0) / m
        prompt = max(0, int(input_tokens)) * float(tier.input_price or 0.0) / m
    else:
        rate = float(tier.input_price or 0.0) / m
        prompt = 0.0
    return units * spec.tokens_per_unit * rate + prompt


async def quote_for_dispatch(profile: Any, config: Any, quote: CallQuote | None) -> CallQuote | None:
    """The quote the dispatch seam hands :func:`admit_guardrails` for a GUARDED run's call: the caller's own, else the
    request's (:func:`quote_call`: tokens, or units x unit price for a per-image / per-second / per-character route),
    else the route's recorded calls (:func:`route_history_quote`), else None (the host holds its unpriced amount).
    An unguarded call is not priced here (nothing would reserve it). Then, in a guarded run, it waits while the call
    misfits only because sibling calls in flight hold the room (:func:`wait_for_run_budget_room`). Never raises."""
    found = await _price_for_dispatch(profile, config, quote)
    await wait_for_run_budget_room(profile, found)
    return found


#: ``(ctx, quote | None) -> seconds | None`` — the host's room door: the most seconds a guarded call should wait for
#: room its sibling calls in flight hold (they settle at their real cost), or None to go to admission now.
_budget_room_wait: Callable[[Any, CallQuote | None], float | None] | None = None
#: How often a waiting call asks again (seconds).
ROOM_POLL_SECONDS = 0.25  # protocol-constant: internal wait-for-room poll tick, a latency/CPU trade-off with no admin-facing meaning


async def wait_for_run_budget_room(profile: Any, quote: CallQuote | None) -> None:
    """Wait, bounded by the host, while this guarded call does not fit its run's budget only because calls in flight
    in OTHER tasks hold the room (2026-11-18: a sibling helper's call held $2.56 of a $3 run budget for 5 seconds and
    the parent's step, $0.44 really spent, stopped the run). Admission then decides on the real numbers. Loud when it
    waits and when it gives up. Never raises."""
    if _budget_room_wait is None or _budget_reserve is None:
        return
    import asyncio
    import time

    try:
        from matrx_ai.context.app_context import try_get_app_context
        from matrx_ai.providers.usage_gate import costs_nothing_on_a_device

        ctx = try_get_app_context()
        if ctx is None or not _is_guarded(ctx):
            return
        if profile is not None and costs_nothing_on_a_device(profile):
            return
    except Exception as exc:  # noqa: BLE001
        vcprint(f"[GuardrailGate] could not read whether the run is guarded: {exc!r}", color="red", log_level="ERROR")
        return
    deadline: float | None = None
    started = time.monotonic()
    while True:
        try:
            limit = _budget_room_wait(ctx, quote)
        except Exception as exc:  # noqa: BLE001 — admission still decides
            vcprint(f"[GuardrailGate] budget room door raised ({type(exc).__name__}: {exc}).", color="red",
                    log_level="ERROR")
            return
        now = time.monotonic()
        if not limit:
            if deadline is not None:
                vcprint(f"[GuardrailGate] run budget room freed after {now - started:.1f}s; admitting.",
                        color="yellow", log_level="INFO")
            return
        if deadline is None:
            deadline = now + float(limit)
            vcprint(
                f"[GuardrailGate] run budget: this step waits up to {float(limit):.0f}s for room its sibling calls "
                "still hold (holds are replaced by real cost when they finish).",
                color="yellow",
                log_level="WARNING",
            )
        if now >= deadline:
            vcprint(f"[GuardrailGate] run budget: waited {now - started:.0f}s for room; admission decides now.",
                    color="red", log_level="WARNING")
            return
        await asyncio.sleep(ROOM_POLL_SECONDS)


async def _price_for_dispatch(profile: Any, config: Any, quote: CallQuote | None) -> CallQuote | None:
    if quote is not None:
        return quote
    try:
        from matrx_ai.context.app_context import try_get_app_context

        if _budget_reserve is None or not _is_guarded(try_get_app_context()):
            return None
        from matrx_ai.providers.usage_gate import costs_nothing_on_a_device

        if profile is not None and costs_nothing_on_a_device(profile):
            return None  # reserve_run_budget holds $0 for it
    except Exception as exc:  # noqa: BLE001
        vcprint(f"[GuardrailGate] could not read whether the run is guarded: {exc!r}", color="red", log_level="ERROR")
        return None
    found = quote_call(profile, config)
    if found is None:
        found = await route_history_quote(profile)
    return found


def quote_call(profile: Any, config: Any) -> CallQuote | None:
    """The worst case of the call about to be sent, or None when it cannot be priced (no config, no output
    ceiling, no catalog token price). Never raises."""
    if config is None:
        return None
    try:
        from matrx_ai.config.context_preflight import estimate_prompt_tokens
        from matrx_ai.config.usage_config import (
            SYNTHETIC_USAGE_BASES,
            _get_db_pricing_lookup,
            lookup_model_pricing,
        )

        model = str(
            getattr(profile, "model_name", None)
            or getattr(config, "matrx_model_name", None)
            or getattr(config, "model", None)
            or ""
        )
        input_tokens = max(1, int(estimate_prompt_tokens(config)))
        output_tokens = int(getattr(config, "max_output_tokens", None) or 0)
        if output_tokens <= 0:
            controls = getattr(profile, "controls", None)
            output_tokens = int(getattr(controls, "output_maximum", None) or 0)
        if not model:
            return None
        pricing = lookup_model_pricing(
            _get_db_pricing_lookup(),
            offering_id=str(getattr(profile, "offering_id", None) or ""),
            model_name=model,
            provider_model_name=str(getattr(profile, "provider_model_id", None) or ""),
            api=str(getattr(profile, "vendor", None) or ""),
        )
        tier = pricing.get_tier(input_tokens) if pricing else None
        if tier is not None and tier.usage_basis is not None and tier.usage_basis in SYNTHETIC_USAGE_BASES:
            # Priced by its own unit (images, clips, seconds, tracks, characters): the request's units x the catalog's
            # unit price, whatever its output ceiling (cost adversary pass 5, F3: a $8 video reserved the flat $3).
            usd = _unit_priced_worst_usd(tier, config, input_tokens, profile)
            return None if usd is None else fixed_quote(model, usd)
        if not model or output_tokens <= 0:
            return None
        if tier is None:
            return None
        cold, warm, out = _tier_rates(tier)
        return CallQuote(model, input_tokens, output_tokens, cold, warm, out)
    except Exception as exc:  # noqa: BLE001 — an unpriceable call is announced; the spent-line stop still holds
        vcprint(f"[GuardrailGate] run budget could not price the call: {exc!r}", color="red", log_level="ERROR")
        return None


def _still_in_flight(holder: Any) -> bool:
    try:
        from matrx_ai.providers.unified_client import _ACTIVE_DISPATCH_POOLS

        return holder in _ACTIVE_DISPATCH_POOLS.get()
    except Exception:  # noqa: BLE001
        return False


def _release_quietly(reservation: Any) -> None:
    try:
        reservation.release()
    except Exception as exc:  # noqa: BLE001 — a broken release is loud; the host lease still frees it
        vcprint(f"[GuardrailGate] run budget release raised ({type(exc).__name__}: {exc}).", color="red",
                log_level="ERROR")


def _announce_capped_answer(ctx: Any, notice: str, reservation: Any) -> None:
    """Say in the run that the answer's length was limited by its budget (a warning event + the log)."""
    vcprint(f"[GuardrailGate] {notice}", color="yellow", log_level="WARNING")
    emitter = getattr(ctx, "emitter", None)
    send = getattr(emitter, "send_warning", None)
    if send is None:
        return
    try:
        import asyncio

        from matrx_connect.context.events import WarningPayload

        payload = WarningPayload(
            code="run_budget_answer_limited",
            system_message=notice,
            user_message=notice,
            level="low",
            metadata={"max_output_tokens": getattr(reservation, "max_output_tokens", None)},
        )
        task = asyncio.get_running_loop().create_task(send(payload))
        _NOTICE_TASKS.add(task)
        task.add_done_callback(_NOTICE_TASKS.discard)
    except Exception as exc:  # noqa: BLE001 — the log line above already said it
        vcprint(f"[GuardrailGate] could not emit the budget notice: {exc!r}", color="red", log_level="ERROR")


def reserve_run_budget(ctx: Any, profile: Any = None, config: Any = None, quote: CallQuote | None = None) -> None:
    """Reserve the call's worst case against its run (guarded runs only), cap its answer when only a smaller
    one fits, or raise the host's stop. Called by :func:`admit_guardrails` after the resolver admitted it."""
    if _budget_reserve is None:
        return
    if quote is None and profile is not None:
        from matrx_ai.providers.usage_gate import costs_nothing_on_a_device

        if costs_nothing_on_a_device(profile):  # served on the person's own computer: costs nothing, holds nothing
            quote = CallQuote(str(getattr(profile, "model_name", "") or ""), 1, 0, 0.0, 0.0, 0.0)
    if quote is None:
        quote = quote_call(profile, config)
    if quote is None:
        model = str(getattr(profile, "model_name", None) or "")
        if model not in _unpriced_quote_announced:
            _unpriced_quote_announced.add(model)
            vcprint(
                f"[GuardrailGate] run budget cannot price a call on {model or 'an unnamed model'} before it is sent "
                "(no quote from its caller, no output ceiling or no catalog price): it reserves the host's per-call "
                "amount for unpriced calls instead.",
                color="red",
                log_level="WARNING",
            )
    import asyncio

    from matrx_ai.providers.admission import admission_key

    open_ = _OPEN_RESERVATION.get()
    if open_ is not None and not _still_in_flight(open_[1]):
        _release_quietly(open_[0])  # the previous call in this context ended without a result: free it first
        _OPEN_RESERVATION.set(getattr(open_[0], "_outer", None))
        open_ = _OPEN_RESERVATION.get()
    try:
        verdict = _budget_reserve(ctx, quote)
    except Exception as exc:  # noqa: BLE001 — a broken memory read never blocks a run; the spent line still holds
        vcprint(f"[GuardrailGate] budget_reserve raised ({type(exc).__name__}: {exc}) — call admitted.",
                color="red", log_level="ERROR")
        return
    if verdict is None:
        return
    if isinstance(verdict, GuardrailStopError):
        raise verdict
    capped = getattr(verdict, "max_output_tokens", None)
    if capped is not None and config is not None:
        config.max_output_tokens = int(capped)
    notice = getattr(verdict, "notice", None)
    if notice:
        _announce_capped_answer(ctx, notice, verdict)
    task = asyncio.current_task()
    holder = (task, admission_key(profile))
    verdict._outer = open_  # a nested dispatch restores the outer call's reservation when it settles
    _OPEN_RESERVATION.set((verdict, holder))
    if task is not None:
        task.add_done_callback(lambda _t, r=verdict: _release_quietly(r))


def _settle_open_reservation(ctx: Any, cost: float, usage: Any) -> bool:
    """Replace the open reservation with the actual cost. False when none is open (the caller accrues)."""
    open_ = _OPEN_RESERVATION.get()
    if open_ is None:
        return False
    reservation = open_[0]
    _OPEN_RESERVATION.set(getattr(reservation, "_outer", None))
    try:
        reservation.settle(cost, usage)
    except Exception as exc:  # noqa: BLE001
        vcprint(f"[GuardrailGate] run budget settle raised ({type(exc).__name__}: {exc}); accruing.", color="red",
                log_level="ERROR")
        _release_quietly(reservation)
        return False
    return True


async def _attempt_cost(usage: Any, profile: Any) -> float:
    """What one billed attempt cost (catalog price; the conservative estimate when unpriced). Never raises."""
    try:
        from matrx_ai.providers.unified_client import billable_usage, catalog_cost_or_none

        cost = await catalog_cost_or_none(billable_usage(usage))
        if cost is None:
            from matrx_ai.config.usage_config import conservative_unpriced_cost

            cost = conservative_unpriced_cost(usage)
        return max(0.0, float(cost or 0.0))
    except Exception as exc:  # noqa: BLE001
        vcprint(f"[GuardrailGate] could not price a billed attempt: {exc!r}", color="red", log_level="ERROR")
        return 0.0


async def note_billed_failure(exc: BaseException, profile: Any = None) -> None:
    """A paid call FAILED after the provider billed it (usage stamped on ``exc``): its cost counts against the run
    (the open reservation is settled with it, never just released). Marked so it is counted once. Never raises."""
    from matrx_ai.providers.errors import get_billed_usage

    usage = get_billed_usage(exc)
    if usage is None or getattr(exc, "_matrx_run_budget_counted", False):
        return
    try:
        setattr(exc, "_matrx_run_budget_counted", True)
    except Exception:  # noqa: BLE001
        pass
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if not (_accrue is not None and _is_guarded(ctx)):
        return
    cost = await _attempt_cost(usage, profile)
    if not _settle_open_reservation(ctx, cost, usage) and cost > 0:
        _accrue(ctx, cost)


async def note_discarded_attempt(usage: Any, profile: Any = None) -> GuardrailStopError | None:
    """A billed attempt the dispatch throws away and sends again (the empty-answer retry): its cost counts against
    the run while the call's reservation stays held for the resend; when the two no longer fit, the resend is not
    made (the stop is returned). Never raises."""
    if usage is None:
        return None
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if not (_accrue is not None and _is_guarded(ctx)):
        return None
    cost = await _attempt_cost(usage, profile)
    open_ = _OPEN_RESERVATION.get()
    spend = getattr(open_[0], "spend_attempt", None) if open_ is not None else None
    if spend is None:
        if cost > 0:
            _accrue(ctx, cost)
        return None
    try:
        return spend(cost)
    except Exception as exc:  # noqa: BLE001
        vcprint(f"[GuardrailGate] spend_attempt raised ({exc!r}); accruing.", color="red", log_level="ERROR")
        if cost > 0:
            _accrue(ctx, cost)
        return None


def admit_guardrails(profile: Any = None, config: Any = None, quote: CallQuote | None = None) -> None:
    """Admit or stop the paid call about to be made. Asked on EVERY paid call."""
    global _unwired_announced
    from matrx_ai.context.app_context import try_get_app_context

    admit_call_spend_cap(profile, config)
    ctx = try_get_app_context()
    if ctx is None:
        return
    if _every_call is not None:
        try:
            stop = _every_call(ctx, profile, config)
        except Exception as exc:  # noqa: BLE001 — a broken memory read never blocks a run
            vcprint(
                f"[GuardrailGate] every-call resolver raised ({type(exc).__name__}: {exc}) — call admitted.",
                color="red",
                log_level="ERROR",
            )
            stop = None
        if stop is not None:
            vcprint(f"[GuardrailGate] refused {stop.kind}: {stop.message}", color="yellow", log_level="WARNING")
            raise stop
    if _resolver is None:
        if not _unwired_announced:
            _unwired_announced = True
            vcprint(
                "[GuardrailGate] no host wired — automation turn / cost limits are NOT "
                "enforced in this process.",
                color="red",
                log_level="WARNING",
            )
        return
    if not _is_guarded(ctx):
        return
    try:
        stop = _resolver(ctx, profile)
    except Exception as exc:  # noqa: BLE001 — a broken memory read never blocks a run
        vcprint(
            f"[GuardrailGate] resolver raised ({type(exc).__name__}: {exc}) — call admitted.",
            color="red",
            log_level="ERROR",
        )
        return
    if stop is None:
        try:
            reserve_run_budget(ctx, profile, config, quote)
        except GuardrailStopError as reserved_stop:
            stop = reserved_stop
    if stop is not None:
        vcprint(
            f"[GuardrailGate] stopped {stop.subject_kind}={stop.subject_id} "
            f"{stop.kind} limit={stop.limit} observed={stop.observed}",
            color="yellow",
            log_level="WARNING",
        )
        raise stop


def _usage_named_by_profile(usage: Any, profile: Any) -> Any:
    """``usage`` as a catalog-priceable ``TokenUsage`` named by the dispatched route.

    A provider whose wire usage carries only counters (TypeSafe's ``{input_tokens, output_tokens}``
    on a decision call) has no model name, so pricing it read "unknown model" and raised a false
    ``model_call_unpriced`` alarm on every decision call (2026-10-16, Jev decisions) while the
    same call was priced correctly a step later. The dispatcher already knows the route: name it."""
    if usage is None or profile is None or getattr(usage, "matrx_model_name", None):
        return usage
    model_name = getattr(profile, "model_name", None)
    if not model_name:
        return usage
    from matrx_ai.config.usage_config import TokenUsage

    input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
    output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
    return TokenUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        matrx_model_name=str(model_name),
        provider_model_name=str(getattr(profile, "provider_model_id", None) or model_name),
        api=str(getattr(profile, "vendor", "") or ""),
        offering_id=str(getattr(profile, "offering_id", None) or ""),
        offering_route=str(getattr(profile, "resolution_route", None) or ""),
        raw_usage={"input_tokens": input_tokens, "output_tokens": output_tokens},
    )


async def note_paid_result(result: Any, *, profile: Any = None, price: bool = False) -> float | None:
    """After a paid call: add its catalog cost to the guarded run, and return that catalog cost. Never raises.

    An UNPRICED call (no resolvable catalog price) is never accrued as $0: it accrues a
    conservative estimate (``conservative_unpriced_cost``) and is reported to the host's
    ``every_call_unpriced`` hook, which alarms. ``profile`` (the dispatched route) names a usage
    whose provider reported only counters, so it prices against the right offering.

    THE CALL IS PRICED ONCE (P8-RUNS, 2026-11-17): the return value is the catalog cost this function computed
    (``None`` when unpriced, never the estimate), so the dispatch seam's other reader (the meter backstop's filing)
    reuses it instead of asking the catalog a second time. ``price=True`` prices the call even when no guardrail
    hook is wired (the backstop needs the amount). The price runs through :func:`billable_usage` and the profile's
    offering, so an STT or media call is priced in its own basis's units, exactly as the settle prices it."""
    hooks_wired = not (
        _accrue is None
        and _every_call_accrue is None
        and _every_call_usage is None
        and _every_call_unpriced is None
    )
    if not hooks_wired and not price:
        return None
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if _every_call_usage is not None and ctx is not None:
        try:
            _every_call_usage(ctx, getattr(result, "usage", None))
        except Exception:  # noqa: BLE001
            pass
    guarded = _accrue is not None and _is_guarded(ctx)
    tracked = _every_call_accrue is not None and _tracked(ctx)
    if not (guarded or tracked or _every_call_unpriced is not None or price):
        return None
    priced: float | None = None
    try:
        from matrx_ai.providers.unified_client import catalog_cost_or_none

        usage = getattr(result, "usage", None)
        if usage is not None:
            from matrx_ai.providers.unified_client import billable_usage

            try:
                usage = billable_usage(usage)  # STT carries seconds: price it in its basis's units
            except Exception:  # noqa: BLE001 — an unconvertible usage stays unpriced and alarms
                pass
            usage = _usage_named_by_profile(usage, profile)
        found = await catalog_cost_or_none(usage)
        priced = None if found is None else float(found)
        if priced is None and usage is not None:
            from matrx_ai.config.usage_config import conservative_unpriced_cost

            cost = conservative_unpriced_cost(usage)
            if _every_call_unpriced is not None:
                try:
                    _every_call_unpriced(ctx, usage, cost)
                except Exception as exc:  # noqa: BLE001 — the alarm never breaks a finished call
                    vcprint(
                        f"[GuardrailGate] unpriced-call hook raised ({type(exc).__name__}: {exc}).",
                        color="red",
                        log_level="ERROR",
                    )
        else:
            cost = float(priced or 0.0)
        if not (guarded or tracked):
            return priced
        if guarded and not _settle_open_reservation(ctx, cost, usage):
            _accrue(ctx, cost)
        if tracked:
            _every_call_accrue(ctx, cost)
    except Exception as exc:  # noqa: BLE001
        vcprint(
            f"[GuardrailGate] could not accrue run cost ({type(exc).__name__}: {exc}).",
            color="red",
            log_level="ERROR",
        )
    return priced


def guardrail_stop_in(source: Any, *, _max_depth: int = 16) -> GuardrailStopError | None:
    """The guardrail stop inside ``source`` (exception chain or ``.exception``), or None."""
    seen: set[int] = set()
    stack: list[Any] = [source]
    while stack and len(seen) < _max_depth:
        node = stack.pop()
        if node is None or id(node) in seen:
            continue
        seen.add(id(node))
        if isinstance(node, GuardrailStopError):
            return node
        for attr in ("exception", "terminal_exception"):
            carried = getattr(node, attr, None)
            if isinstance(carried, BaseException):
                stack.append(carried)
        if isinstance(node, BaseException):
            stack.append(node.__cause__)
            stack.append(node.__context__)
            members = getattr(node, "exceptions", None)
            if isinstance(members, (list, tuple)):
                stack.extend(m for m in members if isinstance(m, BaseException))
    return None


__all__ = [
    "AUTOMATION_GUARDRAIL",
    "CallQuote",
    "quote_call",
    "quote_tokens",
    "quote_units",
    "note_billed_failure",
    "note_discarded_attempt",
    "reserve_run_budget",
    "wait_for_run_budget_room",
    "CALL_SPEND_CAP",
    "CallSpendCap",
    "admit_call_spend_cap",
    "call_spend_cap_scope",
    "current_call_spend_cap",
    "estimate_call_usd",
    "FIX_ACTION_RAISE_LIMIT",
    "GuardrailStopError",
    "admit_guardrails",
    "guardrail_stop_in",
    "note_paid_result",
    "set_guardrail_host",
    "budget_wrap_up_notice",
    "budget_finish_unit_notice",
]
