"""Route provider-vs-catalog cost disagreement onto the ops issue-class surface.

**What existed before this module.** `matrx_ai.config.usage_config` already
extracts what the provider says a call cost (`provider_charge_from_usage`), and
`matrx_ai.orchestrator.requests.to_storage_dict` already computes all three
numbers per iteration — `catalog_cost_usd`, `provider_charge_usd`, and
`provider_catalog_variance_usd` — and writes them into `chat.request.metadata`.
Nothing read them. Not one query, alert, patrol or agent: the platform had been
measuring its own pricing drift into a jsonb column nobody opens. (The other
pricing check, `scripts/validate_model_pricing.py`, is a units/usage_basis lint
with no scheduled caller, and never compares against a provider at all.)

**What this module does.** It turns that measurement into a durable row on the
platform's EXISTING issue-class surface (`ops.ops_issue_class` /
`ops.ops_issue_event` — the `issue_class` surface of the one `errors` tool), so
the repair patrol and the codex agents can pick it up like any other issue.
No new table, no new queue.

- **One event per model per day.** A drifting price drifts on every single call;
  a row per call would bury the surface. The day guard is an in-process set
  (hot path, zero DB cost) backed by a `ops.ops_issue_event` existence check for
  today, so a restart or a second worker does not re-file the same model.
- **The event carries what a repairer needs**: the offering id, the catalog
  dollars, the provider dollars, the variance, and the model/provider names.
- **Never raises into the request path.** A failure here screams and returns.

Tolerance: a call is reported when the variance exceeds BOTH a relative share of
the catalog cost and an absolute floor (rounding noise on a $0.00002 call is not
a pricing defect). The two numbers live here as the single definition.
"""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from matrx_utils import detached_task, vcprint

#: The `ops.ops_issue_class.key` every pricing-drift event rolls up under.
#: Seeded explicitly by db/migrations/0625_pricing_drift_issue_class.sql so the
#: class carries a real name/category/severity instead of the auto-register guess.
PRICING_DRIFT_ISSUE_KEY = "ai.pricing.provider_catalog_drift"

#: `ops.ops_issue_event.error_type` for these rows.
PRICING_DRIFT_ERROR_TYPE = "provider_catalog_cost_drift"

#: Variance must exceed this share of the catalog-priced cost…
PRICING_DRIFT_RELATIVE_TOLERANCE = 0.02  # 2%

#: …AND this many dollars. Below it the disagreement is rounding, not pricing.
PRICING_DRIFT_ABSOLUTE_TOLERANCE_USD = 0.0005

#: (model-or-offering, UTC date) already filed by THIS process today.
_filed_today: set[tuple[str, date]] = set()


def _tolerance_for(catalog_cost_usd: float) -> float:
    return max(
        PRICING_DRIFT_ABSOLUTE_TOLERANCE_USD,
        abs(catalog_cost_usd) * PRICING_DRIFT_RELATIVE_TOLERANCE,
    )


def exceeds_tolerance(catalog_cost_usd: float, provider_cost_usd: float) -> bool:
    """True when the two costs disagree by more than the tolerance."""
    return abs(provider_cost_usd - catalog_cost_usd) > _tolerance_for(catalog_cost_usd)


def _day_key(model: str | None, offering_id: str | None) -> str:
    return (model or "").strip() or (offering_id or "").strip() or "unknown_model"


def note_pricing_drift(
    *,
    catalog_cost_usd: float | None,
    provider_cost_usd: float | None,
    offering_id: str | None = None,
    model: str | None = None,
    provider: str | None = None,
) -> bool:
    """Report one model's provider-vs-catalog cost disagreement, at most daily.

    Sync on purpose: the one seam that holds both numbers
    (``RequestSummary.to_storage_dict``) is sync, and this must never make the
    request path wait on the issue surface. Ambient identity is read HERE, while
    the caller's context still exists, and passed down explicitly — the recorder
    runs in a detached (context-free) task.

    Returns True when an event was dispatched for filing.
    """
    if catalog_cost_usd is None or provider_cost_usd is None:
        return False
    try:
        catalog = float(catalog_cost_usd)
        provider_cost = float(provider_cost_usd)
    except (TypeError, ValueError):
        return False

    if not exceeds_tolerance(catalog, provider_cost):
        return False

    key = (_day_key(model, offering_id), datetime.now(tz=UTC).date())
    if key in _filed_today:
        return False
    # Claim BEFORE dispatch: a burst of drifting calls must file once, not once
    # per call that happens to land before the first write commits.
    _filed_today.add(key)

    user_id = organization_id = conversation_id = request_id = None
    try:
        from matrx_connect import try_get_app_context

        ctx = try_get_app_context()
        if ctx is not None:
            user_id = ctx.user_id or None
            organization_id = ctx.organization_id
            conversation_id = ctx.conversation_id
            request_id = ctx.request_id or None
    except Exception:
        pass

    coro = _record_pricing_drift(
        catalog_cost_usd=round(catalog, 6),
        provider_cost_usd=round(provider_cost, 6),
        offering_id=offering_id,
        model=model,
        provider=provider,
        user_id=user_id,
        organization_id=organization_id,
        conversation_id=conversation_id,
        request_id=request_id,
    )
    try:
        detached_task(coro, name=f"pricing_drift:{key[0]}")
    except RuntimeError as exc:
        # No running loop — do not swallow it, and do not hold the day claim on
        # a filing that never happened.
        coro.close()
        _filed_today.discard(key)
        vcprint(
            f"[pricing_drift] could not dispatch the drift filing for {key[0]}: {exc}",
            color="red",
        )
        return False
    return True


async def _already_filed_today(model: str | None, offering_id: str | None) -> bool:
    """True when ops.ops_issue_event already carries today's row for this model."""
    from matrx_ai.db._registry import get_model

    OpsIssueEvent = get_model("OpsIssueEvent")
    start_of_day = datetime.combine(datetime.now(tz=UTC).date(), datetime.min.time(), tzinfo=UTC)
    filters: dict[str, Any] = {
        "error_type": PRICING_DRIFT_ERROR_TYPE,
        "occurred_at__gte": start_of_day,
        # ``model`` on the event row is the DAY KEY the in-process guard uses —
        # the model name, or the offering id when a call never named a model.
        # Deduping on a plain column keeps this one indexable equality check.
        "model": _day_key(model, offering_id),
    }
    return await OpsIssueEvent.exists(**filters)


async def _record_pricing_drift(
    *,
    catalog_cost_usd: float,
    provider_cost_usd: float,
    offering_id: str | None,
    model: str | None,
    provider: str | None,
    user_id: str | None,
    organization_id: str | None,
    conversation_id: str | None,
    request_id: str | None,
) -> None:
    try:
        if await _already_filed_today(model, offering_id):
            return
    except Exception as exc:
        # A failed dedupe read must not lose the finding — file it and say so.
        vcprint(
            f"[pricing_drift] day-dedupe read failed ({type(exc).__name__}: {exc}); filing anyway",
            color="yellow",
        )

    variance = round(provider_cost_usd - catalog_cost_usd, 6)
    try:
        from matrx_ai.ops.issue_capture import capture_issue

        await capture_issue(
            PRICING_DRIFT_ISSUE_KEY,
            error_type=PRICING_DRIFT_ERROR_TYPE,
            provider=provider,
            model=_day_key(model, offering_id),
            user_id=user_id,
            organization_id=organization_id,
            conversation_id=conversation_id,
            request_id=request_id,
            detail={
                "offering_id": offering_id,
                "model": model,
                "catalog_cost_usd": catalog_cost_usd,
                "provider_cost_usd": provider_cost_usd,
                "variance_usd": variance,
                "relative_tolerance": PRICING_DRIFT_RELATIVE_TOLERANCE,
                "absolute_tolerance_usd": PRICING_DRIFT_ABSOLUTE_TOLERANCE_USD,
                "remedy": (
                    "The provider billed a different amount than ai.offering.pricing predicts. "
                    "Verify the offering's pricing against the provider's pricing page, correct it, "
                    "and set ai.offering.pricing_verified_at."
                ),
            },
        )
    except Exception as exc:
        vcprint(
            f"[pricing_drift] failed to file the drift issue for {model or offering_id}: "
            f"{type(exc).__name__}: {exc}",
            color="red",
        )


def _reset_day_guard_for_tests() -> None:
    """Clear the in-process day guard. Tests only."""
    _filed_today.clear()


__all__ = [
    "PRICING_DRIFT_ABSOLUTE_TOLERANCE_USD",
    "PRICING_DRIFT_ERROR_TYPE",
    "PRICING_DRIFT_ISSUE_KEY",
    "PRICING_DRIFT_RELATIVE_TOLERANCE",
    "exceeds_tolerance",
    "note_pricing_drift",
]
