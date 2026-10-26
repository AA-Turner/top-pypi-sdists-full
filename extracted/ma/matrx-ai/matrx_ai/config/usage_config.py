from __future__ import annotations

import asyncio
import math
import time
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime
from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint

if TYPE_CHECKING:  # matrx_ai.providers imports matrx_ai.config — type-only here.
    from matrx_ai.providers.resolved_capabilities import ResolvedModelCapabilities

# Synthetic token conventions for non-text billing (see TokenUsage.calculate_cost).
# Prices in tiers remain "per million" of the token field they bill against.
#
# The full, authoritative basis taxonomy is USAGE_BASIS_SPECS below (one entry per
# usage_basis on a PricingTier) — billing, the cost-calc guard, the pricing
# validator, and the admin pricing editor all read it. Add a basis THERE.


def _safe_to_dict(obj: Any) -> dict[str, Any]:
    """Coerce a provider usage object to a plain JSON-safe dict, defensively.

    Anthropic and OpenAI SDKs return Pydantic models; Gemini returns a typed
    dataclass-like object. ``raw_usage`` on TokenUsage is purely observational
    — never block a request because of a serialisation hiccup. Falls back to
    ``str(obj)`` wrapped under ``_raw`` when nothing better is available.
    """
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return {str(key): _json_safe_usage_value(value) for key, value in obj.items()}
    # Native protobuf usage objects (notably xAI SamplingUsage) do not expose a
    # useful __dict__; MessageToDict preserves fields such as cost_in_usd_ticks.
    if hasattr(obj, "DESCRIPTOR") and hasattr(obj, "ListFields"):
        try:
            from google.protobuf.json_format import MessageToDict

            return _safe_to_dict(MessageToDict(obj, preserving_proto_field_name=True))
        except Exception:
            pass
    if hasattr(obj, "model_dump"):
        try:
            return _safe_to_dict(obj.model_dump(exclude_none=False))
        except Exception:
            pass
    if hasattr(obj, "to_dict"):
        try:
            return _safe_to_dict(obj.to_dict())
        except Exception:
            pass
    if hasattr(obj, "__dict__"):
        try:
            return {
                k: _json_safe_usage_value(v)
                for k, v in vars(obj).items()
                if not k.startswith("_")
            }
        except Exception:
            pass
    try:
        return {"_raw": str(obj)}
    except Exception:
        return {}


def _json_safe_usage_value(value: Any) -> Any:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, dict):
        return _safe_to_dict(value)
    if isinstance(value, list | tuple):
        return [_json_safe_usage_value(item) for item in value]
    nested = _safe_to_dict(value)
    return nested.get("_raw") if set(nested) == {"_raw"} else nested


def serialize_provider_usage(obj: Any) -> dict[str, Any]:
    """Return a JSON-safe, lossless-enough provider usage record for billing audit."""
    return _safe_to_dict(obj)


def openai_compatible_usage_counts(usage: Any) -> tuple[int, int, int]:
    """Return non-cached input, output, and cached-input tokens from Chat Completions usage.

    OpenAI-compatible providers use ``prompt_tokens`` / ``completion_tokens`` but
    have evolved more than one name for cache reads. Treat a reported cache-read
    count as a component of prompt tokens and split it before pricing; otherwise
    automatic caching (including Moonshot K3's) is billed at the full input rate.
    Unknown shapes deliberately degrade to zero cache reads rather than invent a
    provider discount.
    """
    raw = _safe_to_dict(usage)

    def _count(value: Any) -> int:
        try:
            return max(0, int(value or 0))
        except (TypeError, ValueError):
            return 0

    prompt_tokens = _count(raw.get("prompt_tokens", raw.get("input_tokens")))
    completion_tokens = _count(raw.get("completion_tokens", raw.get("output_tokens")))
    details = raw.get("prompt_tokens_details") or raw.get("input_tokens_details") or {}
    if not isinstance(details, dict):
        details = {}
    cached_tokens = _count(
        details.get("cached_tokens")
        or details.get("cache_read_input_tokens")
        or raw.get("cached_tokens")
        or raw.get("cache_read_input_tokens")
        or raw.get("prompt_cache_hit_tokens")
        or raw.get("cached_prompt_text_tokens")  # xAI (a subset of prompt_tokens)
    )
    return prompt_tokens - min(prompt_tokens, cached_tokens), completion_tokens, min(
        prompt_tokens, cached_tokens
    )


def provider_charge_from_usage(obj: Any) -> ProviderCharge | None:
    """Extract an explicit USD charge from a provider usage object.

    Several OpenAI-compatible gateways add a monetary amount to their otherwise
    standard usage block (most notably ``usage.cost``).  That field used to be
    preserved in ``raw_usage`` but ignored by billing, causing us to recompute a
    catalog estimate even though the provider had returned the authoritative
    charge.  Keep the allow-list deliberately narrow: token counts, timing, and
    arbitrary numeric usage fields must never be mistaken for money.
    """
    raw = _safe_to_dict(obj)
    if not raw:
        return None

    currency = str(raw.get("currency") or raw.get("cost_currency") or "USD").upper()
    candidates: tuple[tuple[str, Any], ...] = (
        ("usage.total_cost_usd", raw.get("total_cost_usd")),
        ("usage.cost_usd", raw.get("cost_usd")),
        ("usage.total_cost", raw.get("total_cost")),
        ("usage.cost", raw.get("cost")),
    )
    for field_path, value in candidates:
        if value is None or isinstance(value, bool):
            continue
        try:
            amount = float(value)
        except (TypeError, ValueError):
            continue
        return ProviderCharge(
            amount_usd=amount,
            raw_amount=value,
            raw_unit="usd",
            field_path=field_path,
            currency=currency,
        )
    return None


@dataclass(frozen=True)
class ProviderCharge:
    """A monetary charge explicitly reported by the provider for one call."""

    amount_usd: float
    raw_amount: int | float | str
    raw_unit: str
    field_path: str
    source: str = "response"
    currency: str = "USD"
    is_final: bool = True

    @property
    def authoritative_usd(self) -> float | None:
        if (
            not self.is_final
            or self.currency.upper() != "USD"
            or not math.isfinite(self.amount_usd)
            or self.amount_usd < 0
        ):
            return None
        return self.amount_usd

    @classmethod
    def combine(
        cls, left: ProviderCharge | None, right: ProviderCharge | None
    ) -> ProviderCharge | None:
        if left is None:
            return right
        if right is None or left == right:
            return left
        left_usd = left.authoritative_usd
        right_usd = right.authoritative_usd
        if left_usd is None or right_usd is None:
            return None
        return cls(
            amount_usd=left_usd + right_usd,
            raw_amount=f"{left.raw_amount}+{right.raw_amount}",
            raw_unit="combined_provider_charges",
            field_path=f"{left.field_path}+{right.field_path}",
            source=left.source if left.source == right.source else "combined",
        )


@dataclass(frozen=True)
class UsageBasisSpec:
    """One billing basis — how a pricing tier's price maps to a real-world unit.

    The cost formula is ALWAYS ``billing_tokens / 1_000_000 * price``. Each basis
    fixes (a) which token field carries the billable count (``billing_field``),
    (b) how many synthetic "tokens" one real unit is worth (``tokens_per_unit``),
    and (c) whether that unit count must be COMPUTED from the generated media
    (pixels, seconds) rather than read off the asset count (``computed``).

    THE SINGLE SOURCE OF TRUTH for billing units. Billing (BaseMediaGeneration),
    the cost-calc guard, the pricing validator, and the admin pricing editor all
    read this — add a basis HERE and everything downstream learns about it.
    """

    billing_field: str  # "input_tokens" | "output_tokens"
    tokens_per_unit: int  # synthetic tokens per real unit (1, 100, or 1_000_000)
    unit: str  # token | character | image | clip | megapixel | second | minute | audio_decisecond
    computed: bool  # True → unit count comes from media (pixels/seconds), not asset count
    price_label: str  # human label for the price field (admin UI / docs)
    description: str


# Keyed by the usage_basis string (None = plain token billing). Mirror in the
# matrx-frontend admin pricing editor (features/ai-models) — keep them in sync.
USAGE_BASIS_SPECS: dict[str | None, UsageBasisSpec] = {
    None: UsageBasisSpec(
        "output_tokens",
        1,
        "token",
        False,
        "$ / 1M tokens",
        "Standard LLM token billing — input/output/cached are real provider tokens.",
    ),
    "image_output": UsageBasisSpec(
        "output_tokens",
        1_000_000,
        "image",
        False,
        "$ / image",
        "One generated image = 1 unit. output_price is $/image.",
    ),
    "megapixel_output": UsageBasisSpec(
        "output_tokens",
        1_000_000,
        "megapixel",
        True,
        "$ / megapixel",
        "Billed by output megapixels (width×height/1e6). output_price is $/MP.",
    ),
    "video_unit_output": UsageBasisSpec(
        "output_tokens",
        1_000_000,
        "clip",
        False,
        "$ / clip",
        "One generated clip = 1 unit. output_price is $/clip.",
    ),
    "video_second_output": UsageBasisSpec(
        "output_tokens",
        1_000_000,
        "second",
        True,
        "$ / second",
        "Billed by output seconds. output_price is $/second.",
    ),
    "audio_unit_output": UsageBasisSpec(
        "output_tokens",
        1_000_000,
        "track",
        False,
        "$ / generated track",
        "Music generation (Lyria): one generated track = 1 unit whatever its length. output_price is $/track. "
        "The Google chat translator records the unit (apply_track_billing) because the provider reports tokens, not tracks.",
    ),
    "audio_second_output": UsageBasisSpec(
        "output_tokens",
        1_000_000,
        "second",
        True,
        "$ / second of audio",
        "Music generation billed by generated seconds (ElevenLabs Eleven Music: $0.15 / minute = $0.0025 / second). "
        "output_tokens = seconds x 1M; output_price is $/second. The ElevenLabs music adapter records the seconds "
        "(apply_audio_seconds_billing) because the provider returns raw audio with no usage object.",
    ),
    "minute": UsageBasisSpec(
        "input_tokens",
        1_000_000,
        "minute",
        True,
        "$ / minute",
        "Billed by session minutes (e.g. realtime voice). input_price is $/minute. "
        "Requires the session to REPORT its duration — realtime metering is not yet wired.",
    ),
    "character_input": UsageBasisSpec(
        "input_tokens",
        1,
        "character",
        False,
        "$ / 1M characters",
        "TTS — input_tokens = character count. input_price is $/1M characters.",
    ),
    "audio_second_input": UsageBasisSpec(
        "input_tokens",
        100,
        "audio_decisecond",
        False,
        "$ / 1M units (0.01s each)",
        "Transcription — input_tokens = floor(seconds×100). input_price is $/1M of those units.",
    ),
    "audio_hour_input": UsageBasisSpec(
        "input_tokens",
        1_000_000,
        "audio_hour",
        True,
        "$ / audio hour",
        "Transcription priced per hour of audio (e.g. ElevenLabs Scribe). "
        "input_tokens = hours × 1M; input_price is $/hour. Requires the STT path "
        "to report audio duration — not yet wired for ElevenLabs/xAI STT.",
    ),
}

# ---------------------------------------------------------------------------
# PROVIDER SERVICE COMPONENTS — paid provider units that are NOT tokens.
#
# A server-side tool the provider runs and bills PER CALL (Anthropic's hosted web
# search: $10 per 1,000 searches). ``from_<provider>`` records the unit count in
# ``TokenUsage.billing_components``; ``ai.offering.pricing[].component_prices``
# carries its price. Like every other component price the value is **per MILLION
# units** — $10/1,000 searches is stored as ``10_000.0``.
#
# A component with NO price is NOT billed as zero: calculate_cost_breakdown returns
# None (cost NULL, ``metadata.cost_reconciliation = "unknown_component_price"``),
# because a token-only figure on a call that also incurred a service fee is a wrong
# number recorded silently. That is exactly how seven Opus-5 web-search calls
# recorded NULL cost (2026-08-18/19): the model's offering shipped without the
# component price. ``validate_model_pricing`` now flags that gap BEFORE the spend.
#
# Keys are (wire_format, capability-feature) -> component name. Add an entry ONLY
# together with the ``from_<provider>`` code that counts its units.
PROVIDER_SERVICE_COMPONENTS: dict[tuple[str, str], str] = {
    ("anthropic_chat", "web_search"): "service.web_search",
    # Google's Deep Research agents (Interactions API) bill Grounding with Google
    # Search per search request ($14 per 1,000 on Gemini 3.x -> 14000); counted by
    # matrx_ai/providers/google/google_research_agent.research_usage.
    ("google_interactions", "web_search"): "service.google_search",
}


# ADVISORY modality counts. A provider that reports its usage split by modality (Gemini's
# ``promptTokensDetails`` / ``candidatesTokensDetails`` / ``cacheTokensDetails``) records each
# non-text share as ``modality.<input|output|cached_input>.<audio|image|video>``. Unlike a
# plain component, an advisory count with no catalog price is NOT a pricing gap: those tokens
# simply stay in the base ``input_price`` / ``output_price`` pool (the price is the same until
# the catalog says otherwise). When the tier prices ``input.audio`` (``component_prices`` or
# ``modality_prices``) the audio share bills at that rate instead.
ADVISORY_COMPONENT_PREFIX = "modality."
#: Modalities that may carry their own price; text (and document) is the base rate.
PRICED_MODALITIES: tuple[str, ...] = ("audio", "image", "video")


def _modality_name(raw: Any) -> str:
    value = getattr(raw, "value", raw)
    text = str(value or "").strip()
    if "." in text:
        text = text.rsplit(".", 1)[-1]
    return text.lower()


def _modality_counts(details: Any) -> dict[str, int]:
    """``[{modality: "AUDIO", token_count: N}, …]`` (dicts in either spelling, or SDK
    ``ModalityTokenCount`` objects) -> ``{"audio": N, …}``."""
    out: dict[str, int] = {}
    for entry in details or []:
        if isinstance(entry, dict):
            modality = _modality_name(entry.get("modality"))
            count = entry.get("token_count") or entry.get("tokenCount") or 0
        else:
            modality = _modality_name(getattr(entry, "modality", None))
            count = getattr(entry, "token_count", 0) or 0
        try:
            count = int(count)
        except (TypeError, ValueError):
            count = 0
        if modality and count > 0:
            out[modality] = out.get(modality, 0) + count
    return out


def gemini_modality_counts(usage_metadata: Any) -> dict[str, int]:
    """Gemini usage (generateContent ``candidates*`` or Live ``response*``; SDK object or
    dict, snake or camel case) -> ``{"input.audio": n, "cached_input.audio": n,
    "output.image": n, …}`` for the priced modalities. Cached counts come off the uncached
    ones so no token is counted twice."""

    def read(*names: str) -> Any:
        for name in names:
            value = usage_metadata.get(name) if isinstance(usage_metadata, dict) else getattr(usage_metadata, name, None)
            if value:
                return value
        return None

    prompt = _modality_counts(read("prompt_tokens_details", "promptTokensDetails"))
    cached = _modality_counts(read("cache_tokens_details", "cacheTokensDetails"))
    response = _modality_counts(
        read(
            "response_tokens_details",
            "responseTokensDetails",
            "candidates_tokens_details",
            "candidatesTokensDetails",
        )
    )
    counts: dict[str, int] = {}
    for modality in PRICED_MODALITIES:
        uncached = prompt.get(modality, 0) - cached.get(modality, 0)
        if uncached > 0:
            counts[f"input.{modality}"] = uncached
        if cached.get(modality, 0) > 0:
            counts[f"cached_input.{modality}"] = cached[modality]
        if response.get(modality, 0) > 0:
            counts[f"output.{modality}"] = response[modality]
    return counts


# Derived views — DO NOT edit directly; change USAGE_BASIS_SPECS instead.
# "synthetic" = any non-None basis (price is not plain $/1M-real-tokens).
SYNTHETIC_USAGE_BASES: frozenset[str] = frozenset(b for b in USAGE_BASIS_SPECS if b is not None)
# Which token field each non-None basis bills against — used by calculate_cost to
# detect "we have a price but not the units to apply it" (the silent-$0 bug).
_BASIS_BILLING_FIELD: dict[str, str] = {
    b: s.billing_field for b, s in USAGE_BASIS_SPECS.items() if b is not None
}

# Once-per-(api, model, problem) dedup so a missing-units / bad-basis condition
# SCREAMS clearly but does not flood the logs on every request.
_billing_warned: set[str] = set()

MISSING_BILLING_UNIT_KIND = "media_billing_unit_missing"


class MissingBillingUnitError(RuntimeError):
    """A paid media response lacks the quantity its pricing tier requires."""


def _capture_missing_billing_unit(
    *, model: str, api: str, problem: str, detail: str
) -> None:
    """Best-effort structured capture for a cost that cannot be computed."""
    try:
        from matrx_ai._ext import get_ext

        record_error = get_ext("record_error")
    except Exception:
        return

    error = MissingBillingUnitError(problem)
    try:
        pending = record_error(
            error,
            kind=MISSING_BILLING_UNIT_KIND,
            error_type=MISSING_BILLING_UNIT_KIND,
            error_text=f"media billing unit missing: {problem}",
            route="media/billing",
            payload={"provider": api, "model": model, "problem": problem, "detail": detail},
        )
        import inspect

        if inspect.isawaitable(pending):
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                pending.close()
                return
            from matrx_utils import detached_task

            detached_task(pending, name=MISSING_BILLING_UNIT_KIND)
    except Exception:
        return


def _warn_billing_once(model: str, api: str, problem: str, detail: str) -> None:
    """Loud, specific, deduped diagnostic for an un-computable cost.

    Fires the FIRST time a given (api, model, problem) is seen this process, so
    the exact gap is impossible to miss without drowning the logs.
    """
    key = f"{api}::{model}::{problem}"
    if key in _billing_warned:
        return
    _billing_warned.add(key)
    _capture_missing_billing_unit(model=model, api=api, problem=problem, detail=detail)
    vcprint(
        f"\n\n🚨 [Cost calc] Cannot compute a correct cost for "
        f"'{model}' (api: {api}) — {problem}.\n    {detail}\n",
        color="red",
        log_level="error",
    )


def _warn_recovered_once(model: str, api: str, problem: str, detail: str) -> None:
    """Deduped diagnostic for a cost we DID compute after repairing bad inputs.

    Distinct from ``_warn_billing_once`` (which means "no cost recorded"): here
    the number is billed, but the provider usage disagreed with itself and we
    had to choose. Loud recovery — never a silent adjustment.
    """
    key = f"recovered::{api}::{model}::{problem}"
    if key in _billing_warned:
        return
    _billing_warned.add(key)
    vcprint(
        f"\n\n⚠️  [Cost calc] Recovered a billable quantity for '{model}' "
        f"(api: {api}) — {problem}.\n    {detail}\n",
        color="yellow",
        log_level="warning",
    )


@dataclass
class PricingTier:
    max_tokens: int | None  # None means unlimited (highest tier)
    input_price: float  # price per million tokens (or per million chars for character_input)
    output_price: float  # price per million tokens (or synthetic units; see usage_basis)
    cached_input_price: float  # price per million tokens
    usage_basis: str | None = None  # None = standard token billing; see SYNTHETIC_USAGE_BASES

    # Anthropic-specific cache pricing
    cache_write_5m_price: float | None = None  # 5-minute cache writes
    cache_write_1h_price: float | None = None  # 1-hour cache writes
    cache_hit_price: float | None = None  # Cache hits & refreshes
    # Optional exact rates for provider usage components whose modalities are
    # priced differently (for example GPT Image text input vs image input).
    # Keys are canonical component names such as ``input.text``,
    # ``input.image``, ``cached_input.text``, ``output.image``, and paid
    # provider units such as ``service.web_search``. A tier's ``modality_prices``
    # ({"audio": {"input_price", "output_price", "cached_input_price"}, …}) is the
    # same price written per modality; it is folded into these keys at parse.
    component_prices: dict[str, float] = field(default_factory=dict)
    # ISO-8601 UTC instant this tier takes effect (a bare date is midnight UTC);
    # None = always in effect. Per ``max_tokens`` threshold the tier with the
    # latest ``effective_from`` at or before the request time wins.
    effective_from: str | None = None

    def effective_instant(self) -> datetime | None:
        return _parse_effective_from(self.effective_from, "effective_from") if self.effective_from else None


@dataclass(frozen=True)
class UsageCostBreakdown:
    input_cost: float
    output_cost: float
    cached_input_cost: float
    cache_write_5m_cost: float
    cache_write_1h_cost: float
    total_cost: float
    input_tokens: int
    output_tokens: int
    cached_input_tokens: int
    cache_write_5m_tokens: int
    cache_write_1h_tokens: int
    component_costs: dict[str, float] = field(default_factory=dict)


@dataclass
class ModelPricing:
    model_name: str
    api: str
    tiers: list[PricingTier]

    def current_tiers(self, at: datetime | None = None) -> list[PricingTier]:
        """The tiers in effect at ``at`` (default now, UTC), one per ``max_tokens`` threshold.

        A tier without ``effective_from`` is in effect from the beginning of time, so a
        pricing list with no dated tier is returned unchanged (today's behavior). Per
        threshold, the tier with the latest ``effective_from`` at or before ``at`` wins
        (a later list entry wins a tie); thresholds keep their first-listed order.
        """
        if not any(t.effective_from for t in self.tiers):
            return self.tiers
        when = _as_utc(at) if at is not None else datetime.now(UTC)
        chosen: dict[int | None, tuple[datetime | None, PricingTier]] = {}
        for tier in self.tiers:
            start = tier.effective_instant()
            if start is not None and start > when:
                continue
            held = chosen.get(tier.max_tokens)
            if held is None or held[0] is None or (start is not None and start >= held[0]):
                chosen[tier.max_tokens] = (start, tier)
        # A dated tier may add a threshold listed after the catch-all; order thresholds
        # ascending (None = unlimited last) so get_tier's first match is the right one.
        ordered = sorted(chosen.values(), key=lambda pair: (pair[1].max_tokens is None, pair[1].max_tokens or 0))
        return [tier for _, tier in ordered]

    def upcoming_tiers(self, at: datetime | None = None) -> list[PricingTier]:
        """Announced tiers that are not in effect yet at ``at`` (default now), soonest first."""
        when = _as_utc(at) if at is not None else datetime.now(UTC)
        future = [t for t in self.tiers if (start := t.effective_instant()) is not None and start > when]
        return sorted(future, key=lambda t: t.effective_instant() or when)

    def get_tier(self, total_input_tokens: int, at: datetime | None = None) -> PricingTier | None:
        tiers = self.current_tiers(at)
        if not tiers:
            return None
        synthetic_only = all(t.usage_basis in SYNTHETIC_USAGE_BASES for t in tiers)
        if synthetic_only and len(tiers) == 1:
            return tiers[0]
        for tier in tiers:
            if tier.max_tokens is None or total_input_tokens <= tier.max_tokens:
                return tier
        return tiers[-1]


_pricing_lookup_cache: dict[str, ModelPricing] | None = None
_pricing_warm_task: asyncio.Task[dict[str, ModelPricing]] | None = None

# CLIENT-HOST pricing mode: set when the pricing lookup was built from a
# host-injected model catalog (or when the ORM path is unavailable in a client
# host). In this mode uncomputed costs are EXPECTED — pricing misses degrade to
# a single INFO notice instead of a red error per request.
_client_host_pricing_mode = False
_client_host_pricing_notice_shown = False


def _client_host_pricing_notice(reason: str) -> None:
    """Log the one-time INFO notice that cost tracking is degraded client-side."""
    global _client_host_pricing_notice_shown
    if _client_host_pricing_notice_shown:
        return
    _client_host_pricing_notice_shown = True
    vcprint(
        f"[Pricing] Cost tracking unavailable in this client host: {reason}. "
        f"Costs will be uncomputed locally (the server remains the billing "
        f"source of truth). This notice is shown once.",
        color="yellow",
        log_level="info",
    )


class PricingShapeError(ValueError):
    """One pricing field holds a value that is not a price (e.g. a dict where a number belongs).

    Raised per OFFERING, never per warm: one malformed catalog row makes THAT model unpriced
    (loudly), it must never take pricing away from every other model. 2026-10-15: a single
    offering with nested ``component_prices`` ({"service": {"web_search": 14000}}) aborted the
    whole warm and every call on the platform recorded NULL cost.
    """


def _price(value: Any, field_name: str) -> float:
    """A required price: number or numeric string; missing/None = 0. Anything else raises."""
    if value is None or value == "":
        return 0.0
    if isinstance(value, bool) or not isinstance(value, int | float | str):
        raise PricingShapeError(
            f"{field_name} must be a number, got {type(value).__name__}: {str(value)[:120]}"
        )
    try:
        price = float(value)
    except (TypeError, ValueError) as exc:
        raise PricingShapeError(f"{field_name} is not numeric: {str(value)[:120]}") from exc
    if not math.isfinite(price) or price < 0:
        raise PricingShapeError(f"{field_name} must be a finite, non-negative price: {value}")
    return price


def _tiers_from_pricing_field(pricing_field: Any) -> list[PricingTier]:
    """Parse a pricing jsonb field (list of tier dicts) into PricingTier objects.

    Shared by the ORM (ai.offering.pricing) and host-catalog (model dict
    'pricing' key) warm paths. A string field is json-decoded; an absent/empty
    field yields []. A field that IS present but malformed raises
    ``PricingShapeError`` — the caller isolates it to that one offering."""
    import json

    if pricing_field is None:
        return []
    if isinstance(pricing_field, str):
        try:
            pricing_field = json.loads(pricing_field)
        except Exception as exc:
            raise PricingShapeError(f"pricing is not valid JSON: {pricing_field[:120]}") from exc
    if isinstance(pricing_field, dict):
        # A single tier object stored without its list wrapper ({} = no pricing, never a $0 tier).
        pricing_field = [pricing_field] if pricing_field else []
    if not isinstance(pricing_field, list):
        raise PricingShapeError(f"pricing must be a list of tiers, got {type(pricing_field).__name__}")
    tiers: list[PricingTier] = []
    for index, tier_data in enumerate(pricing_field):
        if not isinstance(tier_data, dict):
            raise PricingShapeError(f"pricing[{index}] must be an object, got {type(tier_data).__name__}")
        where = f"pricing[{index}]"
        max_tokens = tier_data.get("max_tokens")
        tiers.append(
            PricingTier(
                max_tokens=None if max_tokens is None else int(_price(max_tokens, f"{where}.max_tokens")),
                input_price=_price(tier_data.get("input_price"), f"{where}.input_price"),
                output_price=_price(tier_data.get("output_price"), f"{where}.output_price"),
                cached_input_price=_price(tier_data.get("cached_input_price"), f"{where}.cached_input_price"),
                usage_basis=tier_data.get("usage_basis") or None,
                cache_write_5m_price=_optional_float(tier_data.get("cache_write_5m_price"), f"{where}.cache_write_5m_price"),
                cache_write_1h_price=_optional_float(tier_data.get("cache_write_1h_price"), f"{where}.cache_write_1h_price"),
                cache_hit_price=_optional_float(tier_data.get("cache_hit_price"), f"{where}.cache_hit_price"),
                component_prices=_component_prices(tier_data, where),
                effective_from=_effective_from_field(tier_data.get("effective_from"), f"{where}.effective_from"),
            )
        )
    return tiers


def _as_utc(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def _parse_effective_from(value: Any, field_name: str) -> datetime:
    """An ISO date (midnight UTC) or ISO datetime (naive = UTC). Anything else raises."""
    if isinstance(value, datetime):
        return _as_utc(value)
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day, tzinfo=UTC)
    if not isinstance(value, str) or not value.strip():
        raise PricingShapeError(f"{field_name} must be an ISO date or datetime, got {str(value)[:120]!r}")
    text = value.strip()
    try:
        if len(text) == 10:
            parsed = date.fromisoformat(text)
            return datetime(parsed.year, parsed.month, parsed.day, tzinfo=UTC)
        return _as_utc(datetime.fromisoformat(text.replace("Z", "+00:00")))
    except ValueError as exc:
        raise PricingShapeError(f"{field_name} is not an ISO date or datetime: {text[:120]!r}") from exc


def _effective_from_field(value: Any, field_name: str) -> str | None:
    """Validated and normalized to an ISO UTC instant string (JSON-safe in pricing_snapshot)."""
    if value is None or value == "":
        return None
    return _parse_effective_from(value, field_name).isoformat()


#: ``modality_prices`` field -> the component-price prefix it fills.
_MODALITY_PRICE_FIELDS: dict[str, str] = {
    "input_price": "input",
    "output_price": "output",
    "cached_input_price": "cached_input",
}


def _component_prices(tier_data: dict[str, Any], where: str) -> dict[str, float]:
    """``component_prices`` plus ``modality_prices`` folded into the same canonical keys.

    ``{"modality_prices": {"audio": {"input_price": 3, "output_price": 12}}}`` is exactly
    ``{"component_prices": {"input.audio": 3, "output.audio": 12}}``. Writing one price twice
    with two different values is refused (the offering goes unpriced, loudly) — never a guess
    about which one the catalog meant.
    """
    prices = _float_map(tier_data.get("component_prices"), f"{where}.component_prices")
    modality_prices = tier_data.get("modality_prices")
    if modality_prices is None:
        return prices
    if not isinstance(modality_prices, dict):
        raise PricingShapeError(f"{where}.modality_prices must be an object, got {type(modality_prices).__name__}")
    for modality, fields in modality_prices.items():
        name = str(modality).strip().lower()
        if not isinstance(fields, dict):
            raise PricingShapeError(f"{where}.modality_prices.{name} must be an object of prices")
        for field_name, value in fields.items():
            prefix = _MODALITY_PRICE_FIELDS.get(field_name)
            if prefix is None:
                raise PricingShapeError(
                    f"{where}.modality_prices.{name}.{field_name} is not a price field "
                    f"(one of {sorted(_MODALITY_PRICE_FIELDS)})"
                )
            if value is None:
                continue
            key = f"{prefix}.{name}"
            price = _price(value, f"{where}.modality_prices.{name}.{field_name}")
            if key in prices and prices[key] != price:
                raise PricingShapeError(
                    f"{where} prices {key} twice: component_prices={prices[key]} vs "
                    f"modality_prices.{name}.{field_name}={price}"
                )
            prices[key] = price
    return prices


def _optional_float(value: Any, field_name: str = "price") -> float | None:
    if value is None:
        return None
    return _price(value, field_name)


def _float_map(value: Any, field_name: str = "component_prices") -> dict[str, float]:
    """Component prices, keyed by canonical dotted name (``service.web_search``).

    A nested object is flattened to dotted keys — ``{"service": {"web_search": 14000}}`` is the
    same price as ``{"service.web_search": 14000}`` (the catalog has held both shapes)."""
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise PricingShapeError(f"{field_name} must be an object, got {type(value).__name__}")
    flat: dict[str, float] = {}

    def walk(prefix: str, node: dict[str, Any]) -> None:
        for key, price in node.items():
            name = f"{prefix}.{key}" if prefix else str(key)
            if price is None:
                continue
            if isinstance(price, dict):
                walk(name, price)
                continue
            flat[name] = _price(price, f"{field_name}.{name}")

    walk("", value)
    return flat


#: Offerings whose pricing could not be parsed on the last warm: offering label -> problem.
_pricing_invalid_offerings: dict[str, str] = {}
#: The last whole-warm failure ("" when the last warm succeeded).
_pricing_warm_error: str = ""
_pricing_warm_at: float = 0.0


def pricing_warm_health() -> dict[str, Any]:
    """Readiness view of the price table. ``ok`` is False when the table never loaded, the last
    warm failed, or any offering's pricing could not be parsed (those models are unpriced)."""
    warm = _pricing_lookup_cache is not None
    return {
        "ok": warm and not _pricing_warm_error and not _pricing_invalid_offerings,
        "warm": warm,
        "priced_entries": len(_pricing_lookup_cache or {}),
        "last_error": _pricing_warm_error or None,
        "invalid_offerings": dict(_pricing_invalid_offerings),
        "client_host_mode": _client_host_pricing_mode,
    }


def _capture_pricing_problem(kind: str, message: str, payload: dict[str, Any]) -> None:
    """Durable, structured capture (system_error via the host ``record_error`` sink). Never raises."""
    try:
        from matrx_ai._ext import get_ext, has_ext

        if not has_ext("record_error"):
            return
        error = PricingShapeError(message) if kind == "pricing_shape_invalid" else RuntimeError(message)
        pending = get_ext("record_error")(
            error,
            kind=kind,
            route="matrx_ai.config.usage_config.warm_pricing_lookup",
            error_type=kind,
            error_text=message[:1000],
            payload=payload,
        )
        import inspect

        if inspect.isawaitable(pending):
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                pending.close()
                return
            from matrx_utils import detached_task

            detached_task(pending, name=kind)
    except Exception:  # noqa: BLE001 — diagnostics never break pricing
        return


#: Conservative per-million prices used ONLY to count an unpriced call against spend caps when the
#: price table holds nothing to compare with (the table failed to load). Opus-class on purpose: an
#: unknown cost must trip a cap early, never late.
UNPRICED_FALLBACK_INPUT_PER_M = 20.0
UNPRICED_FALLBACK_OUTPUT_PER_M = 75.0


@dataclass(frozen=True)
class UnpricedEstimate:
    """How an unpriced call was estimated. ``kind`` is ``"tokens"`` (real provider tokens, priced at
    the highest token rate), ``"units"`` (non-token usage priced in its OWN unit: ``unit`` x
    ``units``), or ``"unknown_units"`` (non-token usage with no known unit price: ``cost_usd`` is 0.0
    and the caller must announce it as unpriced; it is never priced as tokens)."""

    cost_usd: float
    kind: str
    unit: str = ""
    units: float = 0.0
    usage_basis: str | None = None


def _usage_int(usage: Any, name: str) -> int:
    try:
        return max(0, int(getattr(usage, name, 0) or 0))
    except (TypeError, ValueError):
        return 0


def _non_token_basis(usage: Any) -> tuple[bool, str | None]:
    """``(is_non_token, usage_basis)``: do this usage's token fields hold synthetic UNITS
    (video seconds, images, tracks, minutes, characters) rather than real provider tokens?

    Sources, strongest first: the media builder's recorded ``metadata.billing_kind``
    (``synthetic:<basis>`` / ``synthetic_unpriced``), then the model's resolved price tier."""
    meta = getattr(usage, "metadata", None)
    kind = str(meta.get("billing_kind") or "") if isinstance(meta, dict) else ""
    if kind.startswith("synthetic:"):
        return True, kind.split(":", 1)[1] or None
    if kind == "synthetic_unpriced":
        return True, None
    model = str(getattr(usage, "matrx_model_name", "") or "")
    if model:
        known, basis = resolve_usage_basis(
            model, str(getattr(usage, "api", "") or ""), str(getattr(usage, "offering_id", "") or "")
        )
        if known and basis is not None:
            return True, basis
    return False, None


def estimate_unpriced_call(usage: Any) -> UnpricedEstimate:
    """THE one estimate for a call whose real price is unknown (spend caps, run limits, alarms).

    Real provider tokens: a deliberately HIGH estimate at the highest token prices in the loaded
    price table (Opus-class fallback when the table is empty). Non-token usage (the token fields
    carry video seconds / images / tracks / minutes / characters): priced by its OWN unit, at the
    highest price any tier of the same ``usage_basis`` charges, never at a token rate (21,000,000
    video units x $75/M read as $1,575 and refused every call, 2026-10-18). With no known unit
    price it returns ``unknown_units`` at $0.00 so the caller announces it instead of inventing
    a number. The ledger keeps NULL either way; this number only keeps caps counting."""
    if usage is None:
        return UnpricedEstimate(0.0, "tokens")
    non_token, basis = _non_token_basis(usage)
    if non_token:
        spec = USAGE_BASIS_SPECS.get(basis) if basis is not None else None
        field_name = spec.billing_field if spec is not None else "output_tokens"
        per_unit = spec.tokens_per_unit if spec is not None else 1_000_000
        units = _usage_int(usage, field_name) / per_unit
        best = 0.0
        for pricing in (_pricing_lookup_cache or {}).values():
            for tier in pricing.tiers:
                if basis is None:
                    if tier.usage_basis is None:
                        continue
                elif tier.usage_basis != basis:
                    continue
                best = max(best, tier.input_price if field_name == "input_tokens" else tier.output_price)
        unit = spec.unit if spec is not None else "unit"
        if best <= 0 or units <= 0:
            return UnpricedEstimate(0.0, "unknown_units", unit, units, basis)
        return UnpricedEstimate(units * best, "units", unit, units, basis)

    max_in = max_out = 0.0
    for pricing in (_pricing_lookup_cache or {}).values():
        for tier in pricing.tiers:
            if tier.usage_basis is not None:
                continue
            max_in = max(max_in, tier.input_price, tier.cached_input_price)
            max_out = max(max_out, tier.output_price)
    if max_in <= 0 and max_out <= 0:
        max_in, max_out = UNPRICED_FALLBACK_INPUT_PER_M, UNPRICED_FALLBACK_OUTPUT_PER_M

    tokens_in = _usage_int(usage, "input_tokens") + _usage_int(usage, "cached_input_tokens")
    for extra in ("cache_write_5m_tokens", "cache_write_1h_tokens"):
        tokens_in += _usage_int(usage, extra)
    tokens_out = _usage_int(usage, "output_tokens")
    return UnpricedEstimate((tokens_in * max_in + tokens_out * max_out) / 1_000_000, "tokens")


def conservative_unpriced_cost(usage: Any) -> float:
    """Dollar figure of ``estimate_unpriced_call`` (kept for callers that only need the number)."""
    return estimate_unpriced_call(usage).cost_usd


async def _warm_pricing_from_host_catalog(catalog: Any) -> dict[str, ModelPricing]:
    """Build the pricing lookup from the host-injected model catalog.

    Client hosts have no ai.offering rows — pricing comes straight off each
    model dict's ``pricing`` key when present. Models without pricing are
    simply uncosted (expected client-side; no error spam)."""
    global _pricing_lookup_cache, _client_host_pricing_mode
    from matrx_ai.catalog.host_catalog import CatalogModel, list_runtime_models

    models: list[Any] = [CatalogModel(d) for d in await catalog.list_models()]
    models.extend(list_runtime_models())

    lookup: dict[str, ModelPricing] = {}
    for model in models:
        name = str(getattr(model, "name", "") or "")
        if not name:
            continue
        try:
            tiers = _tiers_from_pricing_field(model.get("pricing"))
        except PricingShapeError as exc:
            vcprint(f"[Pricing] host catalog model '{name}' has unusable pricing: {exc}", color="yellow")
            continue
        if not tiers:
            continue
        model_pricing = ModelPricing(
            model_name=name,
            api=str(model.get("provider") or ""),
            tiers=tiers,
        )
        lookup[name] = model_pricing
        lookup[f"catalog:{name}"] = model_pricing

    _client_host_pricing_mode = True
    _pricing_lookup_cache = lookup
    if lookup:
        vcprint(f"[Pricing] Warmed {len(lookup)} models from host catalog", color="green")
    else:
        _client_host_pricing_notice("the host model catalog carries no pricing data")
    return lookup


def _schedule_pricing_warm() -> None:
    """Fire-and-forget: schedule warm_pricing_lookup() if an event loop is running."""
    global _pricing_warm_task
    if _pricing_warm_task is not None and not _pricing_warm_task.done():
        return
    try:
        loop = asyncio.get_running_loop()
        _pricing_warm_task = loop.create_task(warm_pricing_lookup())
    except RuntimeError:
        pass  # No running loop yet; will self-schedule on the next access from an async context


async def warm_pricing_lookup() -> dict[str, ModelPricing]:
    """Build and cache the pricing lookup. Safe to call multiple times; always refreshes.

    Loads pricing data from the AiModel DB cache and indexes it by model.name. Each
    model's pricing + vendor tag come from its routing offering when it has one
    (``ai.offering.pricing`` / ``ai.endpoint.vendor``); an unroutable model
    (deprecated, kept for history/cost lookups) falls back to the model row's own
    pricing and carries no vendor tag.

    Exceptions are logged loudly and the cache is left at its previous value so the
    next access can re-attempt the warm.
    """
    global _pricing_lookup_cache, _client_host_pricing_mode, _pricing_warm_error, _pricing_warm_at
    # CLIENT HOST: a host-injected model catalog replaces the ORM path entirely
    # — pricing comes off the catalog's model dicts. Never touches
    # ai_catalog_manager (which needs host DB config).
    from matrx_ai.catalog.host_catalog import get_model_catalog

    host_catalog = get_model_catalog()
    if host_catalog is not None:
        try:
            return await _warm_pricing_from_host_catalog(host_catalog)
        except Exception as exc:  # noqa: BLE001 — degrade once, never spam
            _client_host_pricing_mode = True
            _pricing_lookup_cache = {}
            _client_host_pricing_notice(f"host catalog pricing warm failed ({exc})")
            return {}

    try:
        from matrx_ai.catalog.manager import ai_catalog_manager
        from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance

        if ai_model_manager_instance is None:
            _pricing_lookup_cache = {}
            return {}

        models = await ai_model_manager_instance.load_all_models()
        await ai_catalog_manager.ensure_loaded()

        lookup: dict[str, ModelPricing] = {}
        # (vendor, provider_model_id) → pricing, for callers that only know the
        # name the PROVIDER was called with (a browser-held realtime session
        # reports the wire model it connected with). Exact, never a prefix; a
        # wire id two offerings bill differently is dropped, not guessed.
        wire_pricing: dict[str, ModelPricing] = {}
        ambiguous_wire: set[str] = set()
        orphan_models: list[str] = []
        parked_models: list[str] = []
        invalid: dict[str, str] = {}
        for model in models:
            offerings = ai_catalog_manager.offerings_for(str(model.id))
            if not offerings:
                # Deprecated/retired + unroutable is an expected state — never an orphan.
                # But a deprecated model WITH offerings still ROUTES (ruled 2026-09-09),
                # so it MUST be priced: skipping it here recorded $0 cost on real
                # provider-billed calls.
                if not getattr(model, "is_deprecated", False) and not getattr(
                    model, "retired_at", None
                ):
                    label = f"{getattr(model, 'name', '') or '<unnamed>'} ({model.id})"
                    # PARKED is not ORPHANED. A model whose real offering exists and
                    # was deliberately marked unavailable (no harness yet, invite-only
                    # access — the reason lives in ai.offering.notes) is a recorded
                    # decision every picker already honors; "INSERT an offering" is
                    # the wrong remedy for it. Only a model with NO well-formed
                    # offering at all is a dead row.
                    if ai_catalog_manager.parked_offerings_for(str(model.id)):
                        parked_models.append(label)
                    else:
                        orphan_models.append(label)
                continue
            priced_offerings: list[ModelPricing] = []
            for offering in offerings:
                endpoint = ai_catalog_manager.endpoint(offering.endpoint_id)
                try:
                    tiers = _tiers_from_pricing_field(offering.pricing)
                except PricingShapeError as exc:
                    # ONE bad row makes ONE offering unpriced — never the whole table.
                    invalid[f"{model.name} (offering {offering.id})"] = str(exc)
                    continue
                if not tiers:
                    continue
                api = endpoint.vendor if endpoint else ""
                model_pricing = ModelPricing(model_name=model.name, api=api, tiers=tiers)
                lookup[str(offering.id)] = model_pricing
                priced_offerings.append(model_pricing)
                wire = str(offering.provider_model_id or "")
                if wire and api:
                    key = _wire_key(api, wire)
                    existing = wire_pricing.get(key)
                    if existing is not None and existing.tiers != model_pricing.tiers:
                        ambiguous_wire.add(key)
                    elif existing is None:
                        wire_pricing[key] = model_pricing

            # A name-only lookup is safe only when every route bills the same.
            # Exact offering IDs are always indexed and always win at use time.
            if priced_offerings and all(item == priced_offerings[0] for item in priced_offerings):
                lookup[model.name] = priced_offerings[0]

        for key, model_pricing in wire_pricing.items():
            if key not in ambiguous_wire:
                lookup[key] = model_pricing
        if ambiguous_wire:
            vcprint(
                f"[Pricing] {len(ambiguous_wire)} provider wire id(s) are billed differently by "
                f"different offerings and resolve only by offering id: {', '.join(sorted(ambiguous_wire))}",
                color="yellow",
            )

        if parked_models:
            vcprint(
                f"[Pricing] {len(parked_models)} model(s) parked — offering deliberately "
                f"unavailable (reason in ai.offering.notes): {', '.join(parked_models)}",
                color="cyan",
            )
        if orphan_models:
            detail = "\n".join(f"    ● {name}" for name in orphan_models)
            vcprint(
                f"{len(orphan_models)} active ai.model_definition row(s) have NO available "
                f"ai.offering — the catalog CANNOT route them, but pickers that read "
                f"model_definition alone will still show them as selectable:\n{detail}\n"
                f"  Fix: INSERT an ai.offering linking each model to an ai.endpoint + ai.api "
                f"(provider_model_id = the wire id). A model without an offering is not "
                f"a model — it is a dead row.",
                title="🚨 AI CATALOG ORPHAN MODELS",
                color="red",
            )
            await _capture_orphan_models(orphan_models)

        if invalid:
            detail = "\n".join(f"    ● {label}: {problem}" for label, problem in invalid.items())
            vcprint(
                f"{len(invalid)} offering(s) have pricing that cannot be read — those calls are "
                f"UNPRICED (counted against caps at a conservative estimate) until the row is fixed:\n{detail}",
                title="🚨 AI CATALOG PRICING SHAPE INVALID",
                color="red",
                log_level="error",
            )
            if invalid != _pricing_invalid_offerings:
                _capture_pricing_problem(
                    "pricing_shape_invalid",
                    f"{len(invalid)} offering(s) have unreadable pricing and are unpriced: "
                    + "; ".join(f"{k}: {v}" for k, v in invalid.items()),
                    {"invalid_offerings": invalid, "invalid_count": len(invalid)},
                )
        _pricing_invalid_offerings.clear()
        _pricing_invalid_offerings.update(invalid)
        _pricing_warm_error = ""
        _pricing_warm_at = time.time()
        _pricing_lookup_cache = lookup
        vcprint(
            f"[Pricing] Warmed {len(lookup)} models",
            color="green",
        )
        return lookup
    except Exception as e:
        from matrx_ai.db._registry import DBNotConfiguredError

        if isinstance(e, DBNotConfiguredError):
            # client host with no model catalog either: pricing simply cannot
            # be resolved here. Mark the cache WARM-EMPTY (not None) so this is
            # decided ONCE — leaving it None re-attempted the warm and re-raised
            # this error on EVERY request (the client-host error-spam defect).
            _client_host_pricing_mode = True
            _pricing_lookup_cache = {}
            _client_host_pricing_notice(
                "no database and no host model_catalog configured"
            )
            return {}

        import traceback

        vcprint(
            {"error": str(e), "traceback": traceback.format_exc()},
            "[Pricing Lookup] Warm FAILED — costs will not be calculated",
            color="red",
            log_level="error",
        )
        message = f"pricing lookup warm failed: {type(e).__name__}: {e}"
        if message != _pricing_warm_error:
            _capture_pricing_problem(
                "pricing_lookup_warm_failed",
                message + (" — every call is unpriced until it succeeds" if _pricing_lookup_cache is None
                           else " — the previous price table is still in use"),
                {"error_type": type(e).__name__, "had_previous_table": _pricing_lookup_cache is not None},
            )
        _pricing_warm_error = message
        return _pricing_lookup_cache or {}


class CatalogOrphanModelsError(RuntimeError):
    """Active model definitions exist without a routable catalog offering."""


async def _capture_orphan_models(orphan_models: list[str]) -> None:
    """Durably capture the catalog-integrity failure at its detection seam.

    Console ERROR logs are useful for operators watching a process, but the
    persistence patrol cannot repair a failure that never reaches its
    structured queue.  The host-injected sink keeps this package independent
    while giving server hosts one actionable ``system_error`` class.
    """
    from matrx_ai._ext import get_ext, has_ext

    if not has_ext("record_error"):
        return
    error = CatalogOrphanModelsError(
        f"{len(orphan_models)} active model definition(s) have no available offering: "
        + ", ".join(orphan_models)
    )
    try:
        await get_ext("record_error")(
            error,
            kind="ai_catalog_orphan_models",
            route="matrx_ai.config.usage_config.warm_pricing_lookup",
            error_type=type(error).__name__,
            payload={"orphan_models": orphan_models, "orphan_count": len(orphan_models)},
        )
    except Exception as capture_exc:  # noqa: BLE001 — diagnostics never break pricing warm
        vcprint(
            f"[Pricing] structured orphan-model capture failed: {capture_exc!r}",
            color="red",
            log_level="error",
        )


def is_pricing_lookup_warm() -> bool:
    """True once the pricing lookup has been loaded from the DB at least once
    (even if zero models carried pricing).

    The distinction this enables is the whole point: when the cache is cold
    (this returns False), a model "missing" from the lookup means *the data was
    never fetched* — NOT that the model has no pricing. Only when the cache is
    warm does an absent model genuinely mean "no pricing row in the DB".
    """
    return _pricing_lookup_cache is not None


async def ensure_pricing_lookup() -> dict[str, ModelPricing]:
    """Fetch-if-not-fetched: guarantee the pricing lookup is loaded from the DB.

    This is the root primitive for the "check, then fetch if missing" contract.
    Call it from any async context (request finalization, persistence, media
    generation) BEFORE the synchronous TokenUsage.calculate_cost() so cost
    calculation can never run against a cold cache and emit a false
    "pricing not found" warning.

    - Cache already warm  → returns it immediately, no DB hit.
    - Warm already in flight → awaits and shares that single load (no stampede).
    - Cold (never fetched, or a prior warm failed) → starts a warm and awaits it.

    Never raises: warm_pricing_lookup() swallows + logs DB errors and returns
    the best lookup it could build (possibly empty).
    """
    global _pricing_warm_task
    if _pricing_lookup_cache is not None:
        return _pricing_lookup_cache
    if _pricing_warm_task is None or _pricing_warm_task.done():
        _pricing_warm_task = asyncio.ensure_future(warm_pricing_lookup())
    return await _pricing_warm_task


def _get_db_pricing_lookup() -> dict[str, ModelPricing]:
    """Return the cached pricing lookup, scheduling a lazy warm on first cold access.

    This is called synchronously from TokenUsage.calculate_cost(). On first call
    when the cache is None, schedule an async warm and return {} — the caller
    detects the cold state via is_pricing_lookup_warm() and logs a "not fetched
    yet" notice (NOT a "missing pricing" error). The eager warm in the FastAPI
    lifespan, plus ensure_pricing_lookup() at the orchestrator finalization
    chokepoints, populate this before any cost calc in normal flows; this lazy
    path is the last-resort fallback for ad-hoc tests, scripts, and workers.
    """
    if _pricing_lookup_cache is not None:
        return _pricing_lookup_cache
    _schedule_pricing_warm()
    return {}


def _pricing_miss(model_name: str, api: str) -> None:
    """A pricing lookup missed. SCREAM — never guess.

    This used to fall back to ``model_name.startswith(key)`` over the lookup dict,
    taking the FIRST prefix hit in insertion order. On live data that is a billing
    lottery, not a fallback:

        gpt-5-nano        ($0.40/M out)  ->  gpt-5      ($10.00/M out)   25x overcharge
        gpt-4o-mini       ($0.60/M out)  ->  gpt-4o     ($10.00/M out)   16x overcharge
        google/veo-3.0-fast ($0.80/s)    ->  veo-3.0    ($1.60/s)         2x overcharge

    A wrong cost recorded silently is strictly worse than a missing cost recorded
    loudly: the first is discovered by a customer, the second by us. A model name
    may never decide how a customer is billed — the recorded fact is
    ``ai.offering.pricing``, keyed exactly.

    CLIENT-HOST exception: when the lookup was built from a host model catalog
    (no ai.offering rows exist), uncosted models are EXPECTED — degrade to the
    one-time INFO notice instead of a red error per request.
    """
    if _client_host_pricing_mode:
        _client_host_pricing_notice(
            f"no pricing for '{model_name}' in the host catalog (expected client-side)"
        )
        return
    vcprint(
        f"[Pricing Lookup] MISS for model '{model_name}' (api: '{api or 'unknown'}'). "
        f"No cost will be recorded for this call. This means the model has no "
        f"ai.offering.pricing row, or the name sent to the provider does not match "
        f"the catalog. Fix the catalog row — do NOT add a prefix/name fallback.",
        title="🚨 PRICING LOOKUP MISS — COST NOT RECORDED",
        color="red",
        log_level="error",
    )


def _wire_key(api: str, provider_model_id: str) -> str:
    return f"wire:{api}:{provider_model_id}"


def lookup_model_pricing(
    lookup: dict[str, ModelPricing],
    *,
    offering_id: str = "",
    model_name: str = "",
    provider_model_name: str = "",
    api: str = "",
) -> ModelPricing | None:
    """The ONE pricing resolution — every key is exact, tried in this order:

    1. the offering id (the exact route that served the call) — when given, it
       is the only answer;
    2. the catalog model name (``ai.model_definition.name``);
    3. the provider's wire id under its vendor (``ai.offering.provider_model_id``
       on an endpoint of ``api``) — for a caller that only knows the name the
       provider was called with, e.g. a browser-held realtime session.

    Never a prefix or a fuzzy match — see ``_pricing_miss``.
    """
    if offering_id:
        return lookup.get(offering_id)
    if model_name and model_name in lookup:
        return lookup[model_name]
    if api:
        for wire in (provider_model_name, model_name):
            if wire:
                hit = lookup.get(_wire_key(api, wire))
                if hit is not None:
                    return hit
    return None


def resolve_usage_basis(
    model_name: str, api: str = "", offering_id: str = ""
) -> tuple[bool, str | None]:
    """``(pricing_known, usage_basis)`` for ``model_name`` from the warm pricing
    lookup. ``pricing_known`` is False when the lookup is cold or the model is
    absent — callers MUST NOT infer a billing basis from that.

    EXACT match only. See ``_pricing_miss`` for why a prefix fallback is forbidden.

    The single basis resolver — image/video (BaseMediaGeneration) and audio/TTS
    (build_character_billed_usage) both route through here so the rule lives once.
    """
    if not model_name or not is_pricing_lookup_warm():
        return (False, None)
    lookup = _get_db_pricing_lookup()
    model_pricing = lookup_model_pricing(
        lookup, offering_id=offering_id, model_name=model_name, api=api
    )
    if model_pricing is None:
        _pricing_miss(model_name, api)
        return (False, None)
    current = model_pricing.current_tiers()
    if not current:
        return (False, None)
    return (True, current[0].usage_basis)


@dataclass
class ModelUsageSummary:
    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0
    total_tokens: int = 0
    api: str = ""
    request_count: int = 0
    cost: float | None = 0.0


@dataclass
class UsageTotals:
    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0
    total_tokens: int = 0
    total_requests: int = 0
    unique_models: int = 0
    total_cost: float | None = None
    known_cost_subtotal: float = 0.0
    provider_reported_requests: int = 0
    catalog_priced_requests: int = 0
    unknown_cost_requests: int = 0


@dataclass
class AggregatedUsage:
    by_model: dict[str, ModelUsageSummary] = field(default_factory=dict)
    total: UsageTotals = field(default_factory=UsageTotals)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TokenUsage:
    input_tokens: int
    output_tokens: int
    cached_input_tokens: int = 0
    matrx_model_name: str = ""
    provider_model_name: str = ""
    api: str = ""
    response_id: str = ""
    # The EXACT call that served this usage — the ai.offering uuid resolved for
    # the dispatch, plus HOW it was chosen: "pinned" (caller pinned it),
    # "preferred" (priority order), or "sibling_fallback" (overload-class
    # sibling-offering reroute deviated from the pin/preferred). Stamped
    # centrally by UnifiedAIClient.execute; persisted into cx_request.metadata
    # by CompletedRequest.to_storage_dict.
    offering_id: str = ""
    offering_route: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    # Verbatim provider usage block (dict-form). Preserves every field that
    # ``from_<provider>`` normalizes away — Anthropic's cache_creation,
    # service_tier, server_tool_use; OpenAI's reasoning_tokens; Gemini's
    # thoughtsTokenCount; modality breakdowns; etc. Persisted to
    # cx_request.raw_usage so any downstream consumer can recover the truth.
    raw_usage: dict[str, Any] | None = None
    billing_components: dict[str, int] = field(default_factory=dict)
    provider_charge: ProviderCharge | None = None

    def __post_init__(self) -> None:
        # Provider-specific adapters may supply a richer charge (for example
        # xAI's integer USD ticks). Otherwise recover standard explicit dollar
        # fields centrally so every current and future adapter gets the same
        # behavior without duplicating fragile extraction logic.
        if self.provider_charge is None and self.raw_usage:
            self.provider_charge = provider_charge_from_usage(self.raw_usage)

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens + self.cached_input_tokens

    @property
    def cache_write_tokens(self) -> int:
        """Prompt-cache WRITE tokens this call paid for (all lifetimes), from the verbatim
        usage: Anthropic ``cache_creation_input_tokens``; OpenAI
        ``input_tokens_details.cache_write_tokens``. 0 when the provider reports none."""
        raw = self.raw_usage if isinstance(self.raw_usage, dict) else {}
        value = raw.get("cache_creation_input_tokens")
        if value is None:
            details = raw.get("input_tokens_details")
            value = details.get("cache_write_tokens") if isinstance(details, dict) else None
        try:
            return max(0, int(value or 0))
        except (TypeError, ValueError):
            return 0

    def calculate_cost(
        self, pricing_lookup: dict[str, ModelPricing] | None = None, at: datetime | None = None
    ) -> float | None:
        """Return our canonical catalog-calculated cost for this call.

        ``provider_charge`` is independent reconciliation evidence. It must
        never replace the amount written to request/runtime cost columns.
        ``at`` is the request time the dated tiers are chosen for (default now).
        """
        if self.metadata.get("billed_to_own_key"):
            # The call ran on the person's (or organization's) own provider key:
            # the platform paid nothing, so it costs no points. The list price
            # stays visible through calculate_catalog_cost (evidence only).
            return 0.0
        if self.device_served:
            # The call ran on the person's own computer (served_via, wire
            # device_chat): nobody was billed, there is no offering and no price.
            vcprint(
                f"[Pricing] device-served: {self.matrx_model_name or '?'} costs 0.0 "
                f"({self.input_tokens} in / {self.output_tokens} out tokens)",
                color="cyan",
            )
            return 0.0
        breakdown = self.calculate_cost_breakdown(pricing_lookup, at)
        return breakdown.total_cost if breakdown is not None else None

    @property
    def device_served(self) -> bool:
        """True for a call a person's own device served (``providers/device/``)."""
        return bool(self.metadata.get("device_served")) or self.api == "device_chat"

    def calculate_catalog_cost(
        self, pricing_lookup: dict[str, ModelPricing] | None = None, at: datetime | None = None
    ) -> float | None:
        """Return the catalog-derived estimate even when a provider charge exists."""
        breakdown = self.calculate_cost_breakdown(pricing_lookup, at)
        return breakdown.total_cost if breakdown is not None else None

    def calculate_cost_breakdown(
        self, pricing_lookup: dict[str, ModelPricing] | None = None, at: datetime | None = None
    ) -> UsageCostBreakdown | None:
        if self.device_served:
            # No price exists for a device-served call and none is missing: it is a real
            # zero (no pricing lookup, so no pricing-miss alarm).
            return UsageCostBreakdown(
                input_cost=0.0, output_cost=0.0, cached_input_cost=0.0,
                cache_write_5m_cost=0.0, cache_write_1h_cost=0.0, total_cost=0.0,
                input_tokens=self.input_tokens, output_tokens=self.output_tokens,
                cached_input_tokens=self.cached_input_tokens,
                cache_write_5m_tokens=0, cache_write_1h_tokens=0,
            )
        if not self.matrx_model_name:
            return None

        if pricing_lookup is not None:
            lookup = pricing_lookup
            lookup_is_warm = True
        else:
            lookup = _get_db_pricing_lookup()
            lookup_is_warm = is_pricing_lookup_warm()

        # EXACT match only — a prefix fallback here is a billing lottery. See _pricing_miss.
        model_pricing = lookup_model_pricing(
            lookup,
            offering_id=self.offering_id,
            model_name=self.matrx_model_name,
            provider_model_name=self.provider_model_name,
            api=self.api,
        )

        if not model_pricing:
            if not lookup_is_warm:
                # The lookup was never loaded from the DB — this is a
                # "not fetched yet" condition, NOT "this model has no pricing".
                # Kick off a warm so the next cost calc resolves, and stay quiet
                # (yellow notice, not a red error pointing at the DB record).
                _schedule_pricing_warm()
                vcprint(
                    f"[Pricing Lookup] Cost deferred for {self.matrx_model_name} "
                    f"(api: {self.api}) — pricing data not fetched yet; warming "
                    f"the lookup from the DB. Use ensure_pricing_lookup() before "
                    f"cost calculation in async contexts to avoid this.",
                    color="yellow",
                    log_level="warning",
                )
                return None
            # Cache IS warm (we have the full set of models from the DB) and this
            # model is genuinely absent → real missing-pricing condition.
            _pricing_miss(self.matrx_model_name, self.api)
            return None

        # A multi-call answer (long-decode hops, segmented TTS) is priced at the tier its
        # LARGEST single call reached — each call is its own request to the provider, so the
        # summed prompt of N hops never crosses a context-length price break no hop crossed.
        total_input = int(
            self.metadata.get("tier_input_tokens") or (self.input_tokens + self.cached_input_tokens)
        )
        tier = model_pricing.get_tier(total_input, at)
        if not tier:
            vcprint(
                f"\n\n⚠️  Pricing tier not found for model: {self.matrx_model_name} (total_input: {total_input:,} tokens)\n\n",
                color="red",
            )
            return None

        self.metadata["pricing_snapshot"] = asdict(tier)
        self.metadata["pricing_offering_id"] = self.offering_id or None

        if self.metadata.get("cost_reconciliation") == "unknown_missing_provider_usage":
            return None

        unallocated_components = {
            name: count
            for name, count in self.billing_components.items()
            if name.startswith("unallocated.") and count > 0
        }
        if unallocated_components:
            _warn_billing_once(
                self.matrx_model_name,
                self.api,
                "provider usage component allocation is incomplete",
                f"cannot apply component-specific prices to {unallocated_components}; "
                "cost remains unknown instead of using an invented blended rate.",
            )
            self.metadata["cost_reconciliation"] = "unknown_component_allocation"
            return None
        unpriced_components = {
            name: count
            for name, count in self.billing_components.items()
            if count > 0
            and not name.startswith(ADVISORY_COMPONENT_PREFIX)
            and name not in tier.component_prices
        }
        if unpriced_components:
            _warn_billing_once(
                self.matrx_model_name,
                self.api,
                "provider usage component has no catalog price",
                f"cannot price {unpriced_components}; add exact component_prices "
                "to ai.offering.pricing. Cost remains unknown instead of silently "
                "recording a token-only underestimate.",
            )
            self.metadata["cost_reconciliation"] = "unknown_component_price"
            return None

        # We have a price — verify we also have the UNITS to apply it. A tier
        # with a synthetic usage_basis bills off a specific token field; if that
        # field is empty the cost silently collapses to $0 (the TTS bug class).
        # An unrecognized usage_basis means the formula below is being applied to
        # an unknown unit. Either way: SCREAM with the exact, actionable problem.
        basis = tier.usage_basis
        if basis in _BASIS_BILLING_FIELD:
            field = _BASIS_BILLING_FIELD[basis]
            price = tier.input_price if field == "input_tokens" else tier.output_price
            if getattr(self, field) <= 0:
                _warn_billing_once(
                    self.matrx_model_name,
                    self.api,
                    f"missing billable units for usage_basis={basis!r}",
                    f"the pricing tier bills off {field} (price {price}/1M) but "
                    f"{field}=0 — the unit count (characters / seconds / images) "
                    f"was never recorded when TokenUsage was built, so cost "
                    f"computes to $0. Populate {field} at the call site (see "
                    f"build_character_billed_usage / BaseMediaGeneration._build_usage).",
                )
        elif basis is not None and basis not in SYNTHETIC_USAGE_BASES:
            _warn_billing_once(
                self.matrx_model_name,
                self.api,
                f"unknown usage_basis={basis!r}",
                "calculate_cost applies the standard $/1M-token formula, which is "
                f"almost certainly wrong for unit {basis!r}. Add it to "
                "SYNTHETIC_USAGE_BASES + _BASIS_BILLING_FIELD with a documented "
                "unit and populate that unit at the call site, or fix the pricing row.",
            )

        # Same formula for real tokens and synthetic units (megapixels-as-output_tokens, etc.).
        input_tokens = self.input_tokens
        cached_input_tokens = self.cached_input_tokens
        cache_write_5m_tokens = 0
        cache_write_1h_tokens = 0
        if self.api == "anthropic" and isinstance(self.raw_usage, dict):
            raw_input = int(self.raw_usage.get("input_tokens") or 0)
            raw_cache_read = int(self.raw_usage.get("cache_read_input_tokens") or 0)
            cache_creation = self.raw_usage.get("cache_creation") or {}
            if not isinstance(cache_creation, dict):
                cache_creation = {}
            has_duration_split = (
                "ephemeral_5m_input_tokens" in cache_creation
                or "ephemeral_1h_input_tokens" in cache_creation
            )
            cache_write_5m_tokens = int(
                cache_creation.get("ephemeral_5m_input_tokens", 0)
                if has_duration_split
                else self.raw_usage.get("cache_creation_input_tokens", 0)
            )
            cache_write_1h_tokens = int(cache_creation.get("ephemeral_1h_input_tokens", 0))
            # ``cache_creation_input_tokens`` is the authoritative total; the nested
            # duration split is a breakdown of it. They can disagree on a MERGED
            # usage record (TokenUsage.__add__ sums the flat total on every
            # iteration, but replaces the nested dict when an iteration omits it),
            # and trusting the smaller split silently drops billable cache writes —
            # 36,085 of 42,709 tokens on one observed Opus-5 run. Attribute any
            # remainder to the 5m default TTL rather than losing it.
            if has_duration_split:
                raw_cache_write_total = int(
                    self.raw_usage.get("cache_creation_input_tokens", 0) or 0
                )
                unattributed = raw_cache_write_total - (
                    cache_write_5m_tokens + cache_write_1h_tokens
                )
                if unattributed > 0:
                    cache_write_5m_tokens += unattributed
                    _warn_recovered_once(
                        self.matrx_model_name,
                        self.api,
                        "anthropic cache-write duration split short of its total",
                        f"cache_creation_input_tokens={raw_cache_write_total} but the "
                        f"ephemeral_5m/1h split accounts for only "
                        f"{raw_cache_write_total - unattributed}; billing the "
                        f"{unattributed}-token remainder at the 5m (default TTL) rate "
                        f"instead of dropping it.",
                    )
            input_tokens = raw_input
            cached_input_tokens = raw_cache_read

        component_costs: dict[str, float] = {}
        component_input = component_cached = component_output = 0
        for component, count in self._priced_components(tier).items():
            price = tier.component_prices.get(component)
            if price is None:
                continue
            normalized_count = max(0, int(count))
            component_costs[component] = (normalized_count / 1_000_000) * price
            if component.startswith("input."):
                component_input += normalized_count
            elif component.startswith("cached_input."):
                component_cached += normalized_count
            elif component.startswith("output."):
                component_output += normalized_count

        input_cost = (
            max(0, input_tokens - component_input) / 1_000_000
        ) * tier.input_price + sum(
            cost for name, cost in component_costs.items() if name.startswith("input.")
        )
        output_cost = (
            max(0, self.output_tokens - component_output) / 1_000_000
        ) * tier.output_price + sum(
            cost for name, cost in component_costs.items() if name.startswith("output.")
        )
        cache_hit_price = tier.cache_hit_price
        if cache_hit_price is None:
            cache_hit_price = tier.cached_input_price
        cached_cost = (
            max(0, cached_input_tokens - component_cached) / 1_000_000
        ) * cache_hit_price + sum(
            cost
            for name, cost in component_costs.items()
            if name.startswith("cached_input.")
        )
        cache_write_5m_cost = (cache_write_5m_tokens / 1_000_000) * (
            tier.cache_write_5m_price
            if tier.cache_write_5m_price is not None
            else tier.input_price
        )
        cache_write_1h_cost = (cache_write_1h_tokens / 1_000_000) * (
            tier.cache_write_1h_price
            if tier.cache_write_1h_price is not None
            else tier.input_price
        )
        total_cost = (
            input_cost
            + output_cost
            + cached_cost
            + cache_write_5m_cost
            + cache_write_1h_cost
            + sum(
                cost
                for name, cost in component_costs.items()
                if not name.startswith(("input.", "output.", "cached_input."))
            )
        )
        return UsageCostBreakdown(
            input_cost=input_cost,
            output_cost=output_cost,
            cached_input_cost=cached_cost,
            cache_write_5m_cost=cache_write_5m_cost,
            cache_write_1h_cost=cache_write_1h_cost,
            total_cost=total_cost,
            input_tokens=input_tokens,
            output_tokens=self.output_tokens,
            cached_input_tokens=cached_input_tokens,
            cache_write_5m_tokens=cache_write_5m_tokens,
            cache_write_1h_tokens=cache_write_1h_tokens,
            component_costs=component_costs,
        )

    def _priced_components(self, tier: PricingTier) -> dict[str, int]:
        """Exact components, plus each advisory modality count the tier prices.

        An advisory count the tier does not price is dropped here, so its tokens stay in
        the base pool. An exact component of the same name wins over the advisory one.
        """
        out: dict[str, int] = {}
        for name, count in self.billing_components.items():
            if not name.startswith(ADVISORY_COMPONENT_PREFIX):
                out[name] = out.get(name, 0) + count
        for name, count in self.billing_components.items():
            if not name.startswith(ADVISORY_COMPONENT_PREFIX):
                continue
            base = name[len(ADVISORY_COMPONENT_PREFIX) :]
            if base in tier.component_prices and base not in out:
                out[base] = count
        return out

    def __add__(self, other: TokenUsage) -> TokenUsage:
        def merge_raw(left: Any, right: Any) -> Any:
            if isinstance(left, dict) and isinstance(right, dict):
                keys = left.keys() | right.keys()
                return {key: merge_raw(left.get(key), right.get(key)) for key in keys}
            if isinstance(left, int | float) and isinstance(right, int | float):
                return left + right
            return right if right is not None else left

        model = (
            self.matrx_model_name if self.matrx_model_name == other.matrx_model_name else "mixed"
        )
        api = self.api if self.api == other.api else "mixed"
        components = dict(self.billing_components)
        for name, count in other.billing_components.items():
            components[name] = components.get(name, 0) + count
        return TokenUsage(
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            cached_input_tokens=self.cached_input_tokens + other.cached_input_tokens,
            matrx_model_name=model,
            provider_model_name=self.provider_model_name,
            api=api,
            response_id="",
            offering_id=self.offering_id if self.offering_id == other.offering_id else "",
            offering_route=(
                self.offering_route if self.offering_route == other.offering_route else ""
            ),
            raw_usage=merge_raw(self.raw_usage, other.raw_usage),
            provider_charge=ProviderCharge.combine(
                self.provider_charge, other.provider_charge
            ),
            billing_components=components,
        )

    @classmethod
    def from_gemini(
        cls,
        usage_metadata: Any,
        matrx_model_name: str = "",
        provider_model_name: str = "",
        response_id: str = "",
    ) -> TokenUsage:
        # ``prompt_token_count`` INCLUDES cached content (mirrors the image
        # path's ``google_image_api._token_usage``), so the cached share is
        # split out and billed at the cached rate, never double-counted into
        # plain input. ``thoughts_token_count`` is billed as output by Google
        # but is NOT part of ``candidates_token_count``, so it is added in.
        #
        # The per-modality split rides as ADVISORY components (``modality.input.audio``…):
        # priced at the tier's modality rate when the catalog sets one, else billed at the
        # base rate exactly as before.
        raw = _safe_to_dict(usage_metadata)
        prompt = int(usage_metadata.prompt_token_count or 0)
        cached = int(usage_metadata.cached_content_token_count or 0)
        thoughts = int(getattr(usage_metadata, "thoughts_token_count", 0) or 0)
        candidates = int(usage_metadata.candidates_token_count or 0)
        return cls(
            input_tokens=max(0, prompt - cached),
            output_tokens=candidates + thoughts,
            cached_input_tokens=cached,
            matrx_model_name=matrx_model_name,
            provider_model_name=provider_model_name,
            api="google",
            response_id=response_id,
            raw_usage=raw,
            billing_components={
                f"{ADVISORY_COMPONENT_PREFIX}{name}": count
                for name, count in gemini_modality_counts(usage_metadata).items()
            },
        )

    @classmethod
    def from_openai(
        cls,
        usage: Any,
        matrx_model_name: str,
        provider_model_name: str,
        response_id: str = "",
    ) -> TokenUsage:
        cached = usage.input_tokens_details.cached_tokens if usage.input_tokens_details else 0
        raw = _safe_to_dict(usage)
        return cls(
            input_tokens=usage.input_tokens - cached,
            output_tokens=usage.output_tokens,
            cached_input_tokens=cached,
            matrx_model_name=matrx_model_name,
            provider_model_name=provider_model_name,
            api="openai",
            response_id=response_id,
            raw_usage=raw,
        )

    @classmethod
    def from_anthropic(cls, usage: Any, matrx_model_name: str, response_id: str = "") -> TokenUsage:
        # ``usage`` is sometimes a dict, sometimes the SDK's Usage pydantic model.
        # Normalize to dict for raw capture; read tokens via both shapes.
        #
        # CRITICAL: Anthropic's ``input_tokens`` already EXCLUDES both cache
        # reads and cache writes (unlike OpenAI/Gemini, whose prompt totals
        # INCLUDE cached tokens). So we must NOT subtract cache_read from it.
        # And cache_creation (cache-write) tokens are a real, billed cost — if
        # we drop them the bill silently under-records once caching is on. Fold
        # them into input_tokens. DECISION (2026-10-16): ``input_tokens`` stays
        # INCLUSIVE (uncached + cache write) on Anthropic, as every consumer
        # (total_tokens, ledgers, dashboards) already expects. The write portion is
        # recorded separately via ``cache_write_tokens`` (-> chat.request.cache_write_tokens
        # and runtime._ai_calls.tokens_cache_write), with the 5m/1h split kept in raw_usage.
        # ``calculate_cost_breakdown`` re-derives uncached input from raw_usage and prices
        # writes at the 5m/1h write rates, so the fold is NOT double counted in cost.
        raw = _safe_to_dict(usage)
        cache_read = raw.get("cache_read_input_tokens", 0) or 0
        cache_write = raw.get("cache_creation_input_tokens", 0) or 0
        input_t = raw.get("input_tokens", 0) or 0
        output_t = raw.get("output_tokens", 0) or 0
        server_tool_use = raw.get("server_tool_use") or {}
        web_search_requests = (
            int(server_tool_use.get("web_search_requests", 0) or 0)
            if isinstance(server_tool_use, dict)
            else 0
        )
        return cls(
            input_tokens=input_t + cache_write,
            output_tokens=output_t,
            cached_input_tokens=cache_read,
            matrx_model_name=matrx_model_name,
            provider_model_name=matrx_model_name,
            api="anthropic",
            response_id=response_id,
            raw_usage=raw,
            billing_components=(
                {"service.web_search": web_search_requests} if web_search_requests else {}
            ),
        )

    @staticmethod
    def aggregate_by_model(usage_list: list[TokenUsage]) -> AggregatedUsage:
        if not usage_list:
            return AggregatedUsage()

        model_usage: dict[str, ModelUsageSummary] = {}

        provider_reported_requests = 0
        catalog_priced_requests = 0
        unknown_cost_requests = 0
        known_cost_subtotal = 0.0

        for usage in usage_list:
            model_key = usage.matrx_model_name or "unknown"
            if model_key not in model_usage:
                model_usage[model_key] = ModelUsageSummary(api=usage.api)

            summary = model_usage[model_key]
            summary.input_tokens += usage.input_tokens
            summary.output_tokens += usage.output_tokens
            summary.cached_input_tokens += usage.cached_input_tokens
            summary.total_tokens += usage.total_tokens
            summary.request_count += 1

            cost = usage.calculate_cost()
            if (
                usage.provider_charge is not None
                and usage.provider_charge.authoritative_usd is not None
            ):
                provider_reported_requests += 1
            if cost is not None:
                known_cost_subtotal += cost
                catalog_priced_requests += 1
                if summary.cost is not None:
                    summary.cost += cost
            else:
                unknown_cost_requests += 1
                # Any unknown call makes this model's complete cost unknown.
                # Keep known partial value only at aggregate.known_cost_subtotal;
                # never present a per-model subtotal as the model total.
                summary.cost = None

        total_input = sum(m.input_tokens for m in model_usage.values())
        total_output = sum(m.output_tokens for m in model_usage.values())
        total_cached = sum(m.cached_input_tokens for m in model_usage.values())
        total_requests = sum(m.request_count for m in model_usage.values())

        return AggregatedUsage(
            by_model=model_usage,
            total=UsageTotals(
                input_tokens=total_input,
                output_tokens=total_output,
                cached_input_tokens=total_cached,
                total_tokens=total_input + total_output + total_cached,
                total_requests=total_requests,
                unique_models=len(model_usage),
                # A partial subtotal must never masquerade as the complete bill.
                # ``known_cost_subtotal`` remains available for observability.
                total_cost=(known_cost_subtotal if unknown_cost_requests == 0 else None),
                known_cost_subtotal=known_cost_subtotal,
                provider_reported_requests=provider_reported_requests,
                catalog_priced_requests=catalog_priced_requests,
                unknown_cost_requests=unknown_cost_requests,
            ),
        )


def build_character_billed_usage(
    *,
    characters: int,
    matrx_model_name: str,
    provider_model_name: str,
    api: str,
    response_id: str = "",
    extra_metadata: dict[str, Any] | None = None,
) -> TokenUsage:
    """Basis-aware TokenUsage for TTS endpoints that return raw audio bytes with
    NO provider usage object (OpenAI tts-1/-hd, Groq Orpheus, xAI, ElevenLabs).

    The single billing builder for character-billed audio — resolves the model's
    pricing basis so the billable unit always matches the price:
      - ``character_input`` → ``input_tokens = characters`` (the billed chars,
        post-dictionary). Cost = characters / 1M × input_price.
      - pricing not loaded yet → record chars best-effort; cost defers until warm.
      - any other basis (e.g. token-priced gpt-4o-mini-tts, whose endpoint gives
        no usage) → cost CANNOT be derived from characters: leave billable tokens
        at 0 and SCREAM with the exact fix.

    ``characters`` MUST be the count actually sent to the provider (after
    ``apply_tts_dictionary``). Always returns a TokenUsage so the model flows
    through CompletedRequest even when cost is deferred or uncomputable.
    """
    chars = max(0, int(characters))
    pricing_known, basis = resolve_usage_basis(matrx_model_name, api)

    metadata: dict[str, Any] = {"modality": "audio", "input_characters": chars}
    if extra_metadata:
        metadata.update(extra_metadata)

    if basis == "character_input":
        input_tokens = chars
        metadata["billing_kind"] = "synthetic:character_input"
    elif not pricing_known:
        # Cold cache — record chars; calculate_cost defers until the lookup warms.
        input_tokens = chars
        metadata["billing_kind"] = "character_unpriced"
    else:
        # Token-priced or non-character basis on a usage-less audio endpoint —
        # characters are not the billing unit, so we cannot compute cost.
        input_tokens = 0
        metadata["billing_kind"] = "uncomputable_tts_no_usage"
        _warn_billing_once(
            matrx_model_name,
            api,
            f"TTS endpoint returns audio bytes with no token usage, but "
            f"usage_basis={basis!r} is not character-billed",
            f"cost set to $0 ({chars} input chars recorded in metadata). Fix: set "
            f"usage_basis='character_input' on this model's pricing row "
            f"(input_price as $/1M characters), or route it through an endpoint "
            f"that returns real token usage.",
        )

    return TokenUsage(
        input_tokens=input_tokens,
        output_tokens=0,
        cached_input_tokens=0,
        matrx_model_name=matrx_model_name,
        provider_model_name=provider_model_name,
        api=api,
        response_id=response_id,
        metadata=metadata,
    )


def apply_track_billing(usage: Any, *, tracks: int, matrx_model_name: str, api: str) -> bool:
    """Bill ``tracks`` generated music track(s) on a usage whose model prices ``audio_unit_output``.

    The provider (Lyria through the Gemini API) reports prompt/candidate TOKENS for a call that is priced per track.
    When the model's pricing tier is ``audio_unit_output`` the reported tokens are kept in ``metadata`` as evidence and
    the billable field becomes ``tracks`` units (1M synthetic tokens each). Any other basis is left untouched (a TTS or
    chat model that happens to return audio is not a music track). Returns True when it billed tracks.
    """
    if usage is None or tracks <= 0:
        return False
    _known, basis = resolve_usage_basis(matrx_model_name, api)
    if basis != "audio_unit_output":
        return False
    usage.metadata["provider_reported_tokens"] = {
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "cached_input_tokens": usage.cached_input_tokens,
    }
    usage.input_tokens = 0
    usage.cached_input_tokens = 0
    usage.output_tokens = int(tracks) * 1_000_000
    usage.metadata["billing_kind"] = "synthetic:audio_unit_output"
    usage.metadata["billed_tracks"] = int(tracks)
    return True


def build_audio_seconds_billed_usage(
    *,
    seconds: float,
    matrx_model_name: str,
    provider_model_name: str,
    api: str,
    response_id: str = "",
    extra_metadata: dict[str, Any] | None = None,
) -> TokenUsage:
    """Basis-aware TokenUsage for a music endpoint that returns raw audio with NO provider usage object.

    ``audio_second_output`` -> ``output_tokens = seconds x 1M`` (cost = seconds x $/second). Any other basis (or a
    pricing lookup that is not warm) records the seconds in metadata, leaves the billable tokens at 0 and SCREAMS with
    the exact fix, never a quiet $0 (the Lyria ``per_song`` bug of 2026-10-17 is why).
    """
    secs = max(0.0, float(seconds))
    pricing_known, basis = resolve_usage_basis(matrx_model_name, api)
    metadata: dict[str, Any] = {"modality": "audio", "billed_audio_seconds": round(secs, 3)}
    if extra_metadata:
        metadata.update(extra_metadata)
    output_tokens = 0
    if basis == "audio_second_output":
        output_tokens = int(round(secs * 1_000_000))
        metadata["billing_kind"] = "synthetic:audio_second_output"
    elif not pricing_known:
        output_tokens = int(round(secs * 1_000_000))
        metadata["billing_kind"] = "audio_seconds_unpriced"
    else:
        metadata["billing_kind"] = "uncomputable_music_no_usage"
        _warn_billing_once(
            matrx_model_name,
            api,
            f"music endpoint returns audio bytes with no usage, but usage_basis={basis!r} is not audio_second_output",
            f"cost set to $0 ({secs:.1f} s recorded in metadata). Fix: set usage_basis='audio_second_output' on this "
            f"model's pricing row (output_price as $/second).",
        )
    return TokenUsage(
        input_tokens=0,
        output_tokens=output_tokens,
        cached_input_tokens=0,
        matrx_model_name=matrx_model_name,
        provider_model_name=provider_model_name,
        api=api,
        response_id=response_id,
        metadata=metadata,
    )


async def build_audio_seconds_billed_usage_async(**kwargs: Any) -> TokenUsage:
    """``build_audio_seconds_billed_usage`` with a guaranteed-warm pricing lookup."""
    try:
        await ensure_pricing_lookup()
    except Exception:
        pass
    return build_audio_seconds_billed_usage(**kwargs)


async def build_character_billed_usage_async(
    *,
    characters: int,
    matrx_model_name: str,
    provider_model_name: str,
    api: str,
    response_id: str = "",
    extra_metadata: dict[str, Any] | None = None,
) -> TokenUsage:
    """``build_character_billed_usage`` with a guaranteed-warm pricing lookup —
    the form TTS providers call so the basis resolves (and the scream is
    reliable) even on a cold cache."""
    try:
        await ensure_pricing_lookup()
    except Exception:
        pass
    return build_character_billed_usage(
        characters=characters,
        matrx_model_name=matrx_model_name,
        provider_model_name=provider_model_name,
        api=api,
        response_id=response_id,
        extra_metadata=extra_metadata,
    )


# --------------------------------------------------------------------------- #
# Pricing validator — the drift guard for the hand-entered pricing JSONB.
#
# Catches, at the data layer, every bug class this module exists to prevent:
# missing usage_basis on a media model, a price entered in the wrong unit
# ($/char vs $/1M-char), an unknown basis, a billed field left at 0. Used by
# scripts/validate_model_pricing.py (loud, non-blocking) and mirrored byte-for-byte
# by the admin pricing editor's inline checks
# (matrx-frontend features/ai-models/usageBasis.ts). Both read the SAME two facts —
# the capabilities jsonb and ai.offering.token_billed — and NOTHING else. A model
# name, api_class, or wire_format may never decide how a customer is billed.
# --------------------------------------------------------------------------- #


def _is_media_model(caps: ResolvedModelCapabilities) -> bool:
    """A model billed per media UNIT (image / video-second / audio-second /
    character) rather than per real provider token: it emits a media modality, or it
    consumes audio and nothing else (speech-to-text). Such a model needs an explicit
    usage_basis unless its offering is ``token_billed``.

    Derived from the canonical ``capabilities`` shape ONLY — never a model name, an
    api_class, or a wire_format. Byte-identical to the client-side rule in
    matrx-frontend ``features/ai-models/usageBasis.ts::isMediaModel``; the two MUST
    stay in lockstep (they render the same verdict to the same admin).
    """
    return (
        caps.produces_image
        or caps.produces_video
        or caps.produces_audio
        or (caps.supports_audio_input and not caps.supports_text_input)
    )


@dataclass
class PricingIssue:
    model: str
    wire_format: str
    severity: str  # "error" | "warning"
    code: str
    message: str


def _num(v: Any) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def validate_model_pricing(
    name: str,
    wire_format: str,
    capabilities: ResolvedModelCapabilities,
    pricing: Any,
    *,
    token_billed: bool,
    runs_on_device: bool = False,
    routable: bool = False,
    free_reason: str | None = None,
    price_unpublished: str | None = None,
) -> list[PricingIssue]:
    """Validate one model's pricing against USAGE_BASIS_SPECS. Returns a list of
    issues (empty = clean). Pure + dependency-free so it runs in scripts, the
    schema gate, or a test without a DB.

    ``token_billed`` is the RECORDED fact from ``ai.offering.token_billed``: this
    offering bills on real provider tokens, so a NULL ``usage_basis`` is intentional.
    It is never inferred from a wire_format / api_class / model name — that guess is
    how customers get mis-charged.

    ``runs_on_device`` is the RECORDED fact that the model has no ``ai.offering`` at all
    and ships as an ``ai.model_variant`` the user's own machine downloads and runs
    (whisper.cpp, Kokoro, wake words, local diffusion, LoRAs). No provider ever bills it,
    so "no pricing rows" is the truth, not a gap. The moment such a model gains a cloud
    offering the caller passes that offering's pricing with ``runs_on_device=False``.

    ``routable`` says this pricing belongs to a real ``ai.offering`` a call can be sent to.
    Such an offering carries a real price or a RECORDED reason it has none
    (``ai.offering.metadata``): ``free_reason`` (the provider charges nothing: a free-tier
    model, a test model) makes $0 the truth; ``price_unpublished`` (the provider publishes no
    rate) leaves its calls reading "cost unknown", a warning. Anything else empty or all-zero
    is an error: an unpriced call reads unknown, a $0-priced paid call bills nothing, and
    nobody finds out (2026-10-26: five GLiNER2 placeholders, a free Gemma recorded as nothing).
    """
    issues: list[PricingIssue] = []
    wire_format = wire_format or ""
    is_media = _is_media_model(capabilities)

    def add(sev: str, code: str, msg: str) -> None:
        issues.append(PricingIssue(name, wire_format, sev, code, msg))

    tiers = pricing if isinstance(pricing, list) else []
    priced = any(
        isinstance(t, dict)
        and (_num(t.get("input_price")) > 0 or _num(t.get("output_price")) > 0 or bool(t.get("component_prices")))
        for t in tiers
    )
    if routable and not runs_on_device and not priced and not free_reason:
        if price_unpublished:
            add("warning", "price_unpublished",
                f"offering has no price ({price_unpublished}) — its calls read cost unknown.")
        else:
            add("error", "zero_pricing" if tiers else "no_pricing",
                ("every tier prices $0" if tiers else "no pricing rows") + " on a routable offering — "
                "set the provider's real rate, or record metadata.free_reason (free) or "
                "metadata.price_unpublished (no published rate).")
    if not tiers:
        if is_media and not runs_on_device and not routable:
            if price_unpublished:
                add("warning", "price_unpublished",
                    f"media model has no price ({price_unpublished}) — its usage reads cost unknown.")
            else:
                add("error", "no_pricing", "media model has no pricing rows — cost will be $0/None.")
        return issues

    for idx, tier in enumerate(tiers):
        if not isinstance(tier, dict):
            add("error", "bad_tier", f"tier[{idx}] is not an object.")
            continue
        basis = tier.get("usage_basis") or None
        in_p = _num(tier.get("input_price"))
        out_p = _num(tier.get("output_price"))

        if basis is not None and basis not in USAGE_BASIS_SPECS:
            add(
                "error",
                "unknown_basis",
                f"tier[{idx}] usage_basis={basis!r} is not in USAGE_BASIS_SPECS — "
                f"cost will be computed with the wrong unit.",
            )
            continue

        if basis is None and is_media and not token_billed:
            add(
                "error",
                "missing_basis",
                f"tier[{idx}] is a media/audio model with NO usage_basis and its offering "
                f"is not flagged ai.offering.token_billed — billing will mis-charge (the "
                f"$30-image / $0-TTS class). Set a usage_basis (image_output / *_second / "
                f"character_input / …), or set token_billed if the provider really does "
                f"return a token usage object.",
            )

        spec = USAGE_BASIS_SPECS.get(basis)
        if spec is not None and basis is not None:
            price = in_p if spec.billing_field == "input_tokens" else out_p
            if price <= 0:
                add(
                    "warning",
                    "zero_price",
                    f"tier[{idx}] basis {basis!r} bills off {spec.billing_field} but its "
                    f"price is 0 — output will not be billed.",
                )
            # $/1M-character prices entered as $/character are off by ~1e6.
            if basis == "character_input" and 0 < price < 0.01:
                add(
                    "error",
                    "char_price_scale",
                    f"tier[{idx}] character_input input_price={price} looks like $/character, "
                    f"not $/1M characters (off by ~1,000,000×). Multiply by 1e6.",
                )

        for label, p in (("input_price", in_p), ("output_price", out_p)):
            if p > 100_000:
                add(
                    "warning",
                    "implausible_price",
                    f"tier[{idx}] {label}={p} is implausibly high — per-unit vs per-1M confusion?",
                )

        # A provider service the model can invoke and the provider bills per call
        # (hosted web search). Without a component price the WHOLE call prices to
        # NULL — not to a token-only estimate — so an unpriced component silently
        # erases the cost of every run that uses it.
        # Parsed exactly as the cost path parses it: nested and dotted component keys are the
        # same price, ``modality_prices`` folds in, ``effective_from`` must be a real instant.
        try:
            component_prices = _component_prices(tier, f"tier[{idx}]")
            _effective_from_field(tier.get("effective_from"), f"tier[{idx}].effective_from")
        except PricingShapeError as exc:
            add("error", "bad_tier_shape", f"{exc} — this offering is unpriced until fixed.")
            component_prices = {}
        for modality in PRICED_MODALITIES:
            if f"input.{modality}" in component_prices and f"cached_input.{modality}" not in component_prices:
                add(
                    "warning",
                    "cached_modality_unpriced",
                    f"tier[{idx}] prices input.{modality} but not cached_input.{modality} — cached "
                    f"{modality} tokens bill at cached_input_price (the text rate).",
                )
        for (component_wire, feature), component in PROVIDER_SERVICE_COMPONENTS.items():
            if wire_format != component_wire or feature not in capabilities.native_capabilities:
                continue
            if _num(component_prices.get(component)) <= 0:
                add(
                    "error",
                    "missing_service_price",
                    f"tier[{idx}] has no component_prices[{component!r}] but this model "
                    f"declares the {feature!r} feature, and {component_wire} bills that "
                    f"service PER CALL. Every request that uses it records NULL cost "
                    f"(cost_reconciliation=unknown_component_price) — token cost included. "
                    f"Add the price per MILLION units (Anthropic web search: $10 per "
                    f"1,000 searches -> 10000).",
                )

    return issues


# ---------------------------------------------------------------------------
# THE one way to turn measured usage into ledger meters.
#
# `UsageTotals.total_cost` is deliberately None whenever ANY call in a run was
# unpriceable (build_aggregated_usage, above): a partial subtotal must never
# masquerade as the complete bill. Every consumer then wrote the same line —
# `totals.total_cost or 0` — which converts that honest "unknown" into a silent,
# believable **$0** on the spend ledger. A $0 nobody can distinguish from "this
# really was free" is worse than no number at all: the dashboard under-reports
# real money and nothing anywhere screams.
#
# These two builders are the replacement. They record the money we DO know
# (`known_cost_subtotal`), count what we could not price, and make the gap a
# first-class meter the dashboard can surface — plus a loud line naming the
# model whose pricing row is missing, so the fix is the catalog, not the meter.
# ---------------------------------------------------------------------------

#: Meter key carrying the number of calls in a run whose cost could not be
#: derived from the catalog. Non-zero means `usd` is a FLOOR, not the bill.
UNPRICED_CALLS_METER = "unpriced_calls"


def cost_meters_from_totals(totals: Any, *, label: str = "") -> dict[str, Any]:
    """Ledger meters for a whole agent/model run, from its ``UsageTotals``.

    Returns ``{"usd", "input_tokens", "output_tokens"}`` and, only when some
    call could not be priced, ``{"unpriced_calls": n}``. ``usd`` is always the
    catalog-known subtotal — never a silent 0 standing in for an unknown bill.
    """
    if totals is None:
        return {}
    unknown = int(getattr(totals, "unknown_cost_requests", 0) or 0)
    total_cost = getattr(totals, "total_cost", None)
    known = float(getattr(totals, "known_cost_subtotal", 0.0) or 0.0)
    usd = float(total_cost) if total_cost is not None else known
    meters: dict[str, Any] = {
        "usd": usd,
        "input_tokens": int(getattr(totals, "input_tokens", 0) or 0),
        "output_tokens": int(getattr(totals, "output_tokens", 0) or 0),
    }
    if unknown > 0:
        meters[UNPRICED_CALLS_METER] = unknown
        vcprint(
            f"💸 UNPRICED SPEND{f' [{label}]' if label else ''}: {unknown} of "
            f"{int(getattr(totals, 'total_requests', 0) or 0)} calls in this run "
            f"could not be priced from the catalog. Recording the known subtotal "
            f"${usd:.6f} as a FLOOR plus meters.{UNPRICED_CALLS_METER}={unknown}; "
            f"the real bill is higher. Fix: add the missing ai.offering pricing row "
            f"for the model(s) this run used — never the meter.",
            color="red",
            log_level="warning",
        )
    return meters


def cost_meters_from_aggregate(aggregate: Any, *, label: str = "") -> dict[str, Any]:
    """Ledger meters for a whole run from its ``AggregatedUsage`` — the totals of
    :func:`cost_meters_from_totals` plus what a run that writes no ``chat.request``
    (internal agent runs, ``store=False`` work) otherwise loses: ``cached_tokens`` and the
    ``model`` / ``provider`` that cost the most. ``model`` and ``provider`` are strings, so
    they ride the meter payload and never become summed quantities."""
    if aggregate is None:
        return {}
    meters = cost_meters_from_totals(getattr(aggregate, "total", None), label=label)
    if not meters:
        return meters
    cached = int(getattr(getattr(aggregate, "total", None), "cached_input_tokens", 0) or 0)
    if cached:
        meters["cached_tokens"] = cached
    by_model = getattr(aggregate, "by_model", None) or {}
    if by_model:
        name, summary = max(
            by_model.items(),
            key=lambda kv: (
                float(getattr(kv[1], "cost", 0) or 0),
                int(getattr(kv[1], "output_tokens", 0) or 0),
                kv[0],
            ),
        )
        if name and name != "unknown":
            meters["model"] = name
        provider = str(getattr(summary, "api", "") or "")
        if provider:
            meters["provider"] = provider
    return meters


def cost_meters_from_usage(usage: Any, *, label: str = "", **extra: Any) -> dict[str, Any]:
    """Ledger meters for ONE metered call, from its ``TokenUsage``.

    The single-call sibling of :func:`cost_meters_from_totals` — used by the
    speech (STT/TTS) funnels, whose result carries one `TokenUsage` rather than
    an aggregate. ``calculate_cost()`` returning None means the catalog has no
    pricing row for this offering; that records ``usd`` 0 **with**
    ``unpriced_calls: 1`` and a scream, never a bare, believable 0.
    """
    if usage is None:
        vcprint(
            f"💸 UNPRICED SPEND{f' [{label}]' if label else ''}: the provider call "
            "returned NO usage object at all, so its cost cannot be derived. "
            f"Recording meters.{UNPRICED_CALLS_METER}=1 so the ledger shows a "
            "hole instead of a free call.",
            color="red",
            log_level="warning",
        )
        return {"usd": 0.0, UNPRICED_CALLS_METER: 1, **extra}
    # Name who spent it (strings: payload, never a summed quantity) — the usage rules read
    # these for a run that wrote no chat.request. A caller's own ``extra`` wins.
    attribution: dict[str, Any] = {}
    model_name = str(getattr(usage, "matrx_model_name", "") or "")
    api = str(getattr(usage, "api", "") or "")
    if model_name:
        attribution["model"] = model_name
    if api:
        attribution["provider"] = api
    cost = usage.calculate_cost()
    if cost is None:
        vcprint(
            f"💸 UNPRICED SPEND{f' [{label}]' if label else ''}: no catalog price "
            f"for model {getattr(usage, 'matrx_model_name', '?')!r} "
            f"(api {getattr(usage, 'api', '?')!r}, offering "
            f"{getattr(usage, 'offering_id', '') or '—'}). Recording "
            f"meters.{UNPRICED_CALLS_METER}=1 instead of a silent $0. Fix: add the "
            "missing ai.offering pricing row.",
            color="red",
            log_level="warning",
        )
        return {"usd": 0.0, UNPRICED_CALLS_METER: 1, **attribution, **extra}
    return {"usd": float(cost), **attribution, **extra}
