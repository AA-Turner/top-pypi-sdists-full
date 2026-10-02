"""Spend and quota enforcement — WS-7 (docs/handoffs/seo-vertical.md item 7).

The ONE choke point every provider call passes through is
``SeoCollectionService._execute_claimed`` (service.py) — this module is
called from there, right after a run is claimed and before any credential
resolution or provider I/O. Every check reads existing cost evidence
(``seo.collection_run.reported_cost`` / ``estimated_cost``, rolled up per run
by ``OrmSeoRepository._merge_provider_call`` already) through the ONE
:meth:`SeoRepository.spend_summary` aggregate — no second rollup table, no
raw SQL, no new persistence framework.

🚨 **Every ceiling here is a KNOB, not a constant.** The five ``ARMAN_TBD``
module constants this file used to carry were deleted on 2026-08-20 under
``common-docs/policies/limits-are-knobs-agents-set-them.md``. Operational
ceilings now resolve from ``platform.feature_knob`` (:mod:`matrx_seo.knobs`),
and the per-ACCOUNT monthly allowance resolves from the platform's ONE tier
authority through :func:`set_account_ceiling_resolver`. Restoring a default
value to this file would make the admin UI a lie, so a missing knob RAISES.

Two ceilings, two different questions
-------------------------------------
* **"How much is this ORGANIZATION allowed to spend this month?"** — a
  per-account allowance. The host injects a resolver
  (:func:`set_account_ceiling_resolver`) that asks
  ``billing.resolve_capability(user, 'seo.provider_spend', org)``. With no
  resolver installed (a standalone matrx-seo install, which has no billing
  system), or when billing has no opinion for that org, the knob
  ``seo.org_provider_monthly_ceiling_usd`` is the answer. That is a declared
  layer of the same registry, not a silent fallback to a constant.
* **"At what point does the PLATFORM stop paying this provider?"** — an
  operational backstop belonging to no account. Always a knob.

Unpriced runs — why ``effective_cost`` alone is not spend
---------------------------------------------------------
A provider that reports no cost and carries no estimate used to count as
``$0.00`` against every ceiling: 112 live SerpAPI runs had NULL in both cost
columns, so a SerpAPI-only organization could never reach any ceiling at all.
A run that *reports* ``0.00`` (Search Console, Bing Webmaster, PageSpeed, our
own crawl) is measured as genuinely free and is never charged — free
first-party data stays unmetered, as the policy requires. A run with no cost
evidence at all is charged ``seo.unpriced_run_assumed_cost_usd`` per run. The
distinction is NULL-versus-zero, which is why
:attr:`~matrx_seo.contracts.SpendSummary.unpriced_run_count` exists and why
the aggregate may never coalesce an unknown cost to zero.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

from .config import person_cost_text
from .contracts import CollectionRequest, SpendQuery, SpendSummary
from .knobs import usd_knob
from .repository import SeoRepository

#: The feature these knobs belong to (``platform.feature_knob.feature``).
KNOB_FEATURE = "seo"

#: Resolves ONE organization's monthly allowance for ONE provider, in USD.
#: Returns ``None`` when the account system has no opinion, which hands the
#: answer to the ``seo.org_provider_monthly_ceiling_usd`` knob.
AccountCeilingResolver = Callable[[str, str], Awaitable[Decimal | None]]

_account_ceiling_resolver: AccountCeilingResolver | None = None


def set_account_ceiling_resolver(resolver: AccountCeilingResolver | None) -> None:
    """Install the host's per-account allowance resolver.

    aidream wires this to ``billing.resolve_capability`` at startup so the SEO
    vertical never carries its own idea of what a plan includes — the rule that
    keeps the platform from growing a second level ladder
    (``common-docs/systems/platform/entitlements-knobs/PLAN_MODEL.md``)."""
    global _account_ceiling_resolver
    _account_ceiling_resolver = resolver


async def request_headroom_usd() -> Decimal:
    """Head-room added to measured spend before every ceiling comparison.

    NOT a per-call price cap: it is what makes "one more call cannot silently
    cross the ceiling" true. Because it is *added* to the projection, a ceiling
    at or below it rejects the very first call of the period — which is exactly
    what the retired ``$5.00`` placeholder did to the ``$1.00`` caller-daily
    ceiling."""
    return await usd_knob(KNOB_FEATURE, "max_per_request_cost_usd")


async def unpriced_run_cost_usd() -> Decimal:
    """What one run against a paid provider costs when nothing measured it."""
    return await usd_knob(KNOB_FEATURE, "unpriced_run_assumed_cost_usd")


async def org_monthly_ceiling_usd(organization_id: str, provider: str) -> Decimal:
    """This organization's monthly allowance for this provider.

    The account system first (what their plan includes), the operational knob
    when it has no opinion."""
    if _account_ceiling_resolver is not None:
        allowance = await _account_ceiling_resolver(organization_id, provider)
        if allowance is not None:
            return allowance
    return await usd_knob(KNOB_FEATURE, "org_provider_monthly_ceiling_usd")


@dataclass
class _SeoErrorInfo:
    """Duck-typed to match the ``error_info`` shape
    ``matrx_connect.streaming.response`` looks for (``error_type`` /
    ``message`` / ``user_message`` / ``status_code``) so a budget rejection
    streams as a named, typed ``fatal_error`` instead of a generic crash."""

    error_type: str
    message: str
    user_message: str
    status_code: int = 402


class BudgetExceededError(RuntimeError):
    """Raised BEFORE any paid provider call when proceeding would exceed a
    spend ceiling. Always names exactly which ceiling fired and the numbers
    behind it — never a bare 'budget exceeded'."""

    def __init__(
        self,
        *,
        ceiling: str,
        limit_usd: Decimal,
        spent_usd: Decimal,
        projected_usd: Decimal,
        scope: dict[str, Any],
    ) -> None:
        self.ceiling = ceiling
        self.limit_usd = limit_usd
        self.spent_usd = spent_usd
        self.projected_usd = projected_usd
        self.scope = scope
        message = (
            f"SEO spend ceiling '{ceiling}' would be exceeded: "
            f"spent_usd={spent_usd} projected_usd<={projected_usd} > limit_usd={limit_usd} "
            f"scope={scope}"
        )
        super().__init__(message)
        self.error_info = _SeoErrorInfo(
            error_type="seo_budget_exceeded",
            message=message,
            user_message=(
                f"SEO spend limit reached ({ceiling.replace('_', ' ')}: "
                f"{person_cost_text(spent_usd)} of {person_cost_text(limit_usd)} spent). "
                "This work was skipped before any "
                "paid provider call — try again later or ask an admin to raise the ceiling."
            ),
        )

    def as_event_payload(self) -> dict[str, Any]:
        return {
            "ceiling": self.ceiling,
            "limit_usd": str(self.limit_usd),
            "spent_usd": str(self.spent_usd),
            "projected_usd": str(self.projected_usd),
            "scope": self.scope,
        }

    def as_error_payload(self) -> dict[str, Any]:
        return {
            "type": type(self).__name__,
            "message": str(self),
            **self.as_event_payload(),
        }


# ─────────────────────────────────────────────────────────────────────────────
# Spend APPROVALS (OPENSEO-TOOLS-SPEC §6.1). A person approved a number on the
# host's ask-a-person surface; the host stores it (aidream: billing.spend_approval)
# and this package reaches it only through an injected resolver — exactly the
# shape of ``set_account_ceiling_resolver``. With NO resolver installed (a
# standalone matrx-seo), an approval id is an ERROR, never "approved".
# ─────────────────────────────────────────────────────────────────────────────
#: The billing capability provider money is capped under (the host's key; the same
#: string ``billing.capability`` and the SEO allowance use).
PROVIDER_SPEND_CAPABILITY = "seo.provider_spend"


@dataclass(frozen=True)
class SpendApprovalState:
    """What an approval allows right now. USD throughout."""

    approval_id: str
    status: str  # open | exhausted | closed
    ceiling_usd: Decimal
    spent_usd: Decimal  # provider + model drawn so far
    expires_at: datetime | None
    covers: str = "provider"
    #: The guardrail capability the approval was minted for; a collection spends
    #: provider money, so only a ``seo.provider_spend`` approval can fund it.
    capability: str = PROVIDER_SPEND_CAPABILITY
    #: The site the approval was minted for (``scope.site_id``), or None when the
    #: approval named no site.
    site_id: str | None = None
    #: The person who approved it. Only that person's own collections draw on it.
    approved_by: str | None = None
    #: The job the person approved (``scope.tool`` / ``scope.action``). Only a
    #: collection built by that same tool action draws on it.
    tool: str | None = None
    action: str | None = None

    @property
    def remaining_usd(self) -> Decimal:
        return max(self.ceiling_usd - self.spent_usd, Decimal(0))

    def usable_at(self, now: datetime) -> bool:
        if self.status != "open":
            return False
        return self.expires_at is None or self.expires_at > now


class SpendApprovalResolver:
    """The host's reader and charger for approvals. Subclass and install with
    :func:`set_spend_approval_resolver`."""

    async def read(self, approval_id: str, request: CollectionRequest) -> SpendApprovalState | None:
        """The approval as it stands, or ``None`` when it does not exist or does
        not belong to ``request``'s organization."""
        raise NotImplementedError

    async def charge(self, approval_id: str, amount_usd: Decimal, *, run_id: str) -> None:
        """Record provider money a run under this approval actually spent. The
        money is gone by the time this runs, so it records even past the
        ceiling (and the approval becomes exhausted)."""
        raise NotImplementedError


_spend_approval_resolver: SpendApprovalResolver | None = None


def set_spend_approval_resolver(resolver: SpendApprovalResolver | None) -> None:
    """Install the host's approval resolver (aidream binds it in
    ``package_integration.py``)."""
    global _spend_approval_resolver
    _spend_approval_resolver = resolver


def get_spend_approval_resolver() -> SpendApprovalResolver | None:
    return _spend_approval_resolver


class SpendApprovalExceededError(RuntimeError):
    """Raised BEFORE a run starts when a request carries an approval that cannot
    cover it: closed, expired, unknown, or ``spent + estimate > ceiling``.

    Sibling of :class:`BudgetExceededError` — same ``error_info`` /
    ``as_event_payload`` / ``as_error_payload`` shape — plus ``recovery``, the
    handle the agent calls again with once the person approves a new amount."""

    def __init__(
        self,
        *,
        approval_id: str,
        reason: str,
        limit_usd: Decimal,
        spent_usd: Decimal,
        projected_usd: Decimal,
        new_estimate_usd: Decimal,
        scope: dict[str, Any],
        usable_approval: bool = True,
    ) -> None:
        self.approval_id = approval_id
        self.reason = reason
        #: False when the id names no approval this call may draw on at all —
        #: unknown, not this organization's or person's, another job or site,
        #: expired or closed. Then there are no amounts to quote and nothing to
        #: resume: ``recovery`` is None and the next step is a NEW approval
        #: (verification F: a bogus id read "$0 of $0 used" with a "(paid)"
        #: recovery handle naming the bogus id).
        self.usable_approval = usable_approval
        self.ceiling = "spend_approval"
        self.limit_usd = limit_usd
        self.spent_usd = spent_usd
        self.projected_usd = projected_usd
        self.new_estimate_usd = new_estimate_usd
        self.scope = scope
        #: What the agent does next, in one sentence (both cases: a new approval).
        self.next_step = (
            "Call the same tool action again WITHOUT spend_approval_id, so the person is "
            "asked to approve a new amount."
        )
        if not usable_approval:
            self.recovery: dict[str, Any] | None = None
            message = (
                f"Spend approval {approval_id} cannot be used for this call: {reason}. "
                "Nothing was spent."
            )
            user_message = (
                f"That spending approval can't be used here — {reason}. Nothing was spent; "
                "the person needs to approve a new amount."
            )
        else:
            self.recovery = {
                "handle_type": "spend_approval",
                "handle": approval_id,
                "resume_cost": "paid",
                "new_estimate_usd": str(new_estimate_usd),
            }
            message = (
                f"Spend approval {approval_id} cannot cover this collection ({reason}): "
                f"spent_usd={spent_usd} + estimate_usd={new_estimate_usd} = {projected_usd} "
                f"> approved_usd={limit_usd} scope={scope}"
            )
            user_message = (
                f"The approved amount does not cover this ({person_cost_text(spent_usd)} of "
                f"{person_cost_text(limit_usd)} used, this needs about "
                f"{person_cost_text(new_estimate_usd)}). Nothing was spent — approve a new "
                "amount to continue."
            )
        super().__init__(message)
        self.error_info = _SeoErrorInfo(
            error_type=(
                "seo_spend_approval_exceeded" if usable_approval else "seo_spend_approval_unusable"
            ),
            message=message,
            user_message=user_message,
        )

    def as_event_payload(self) -> dict[str, Any]:
        return {
            "ceiling": self.ceiling,
            "reason": self.reason,
            "limit_usd": str(self.limit_usd),
            "spent_usd": str(self.spent_usd),
            "projected_usd": str(self.projected_usd),
            "scope": self.scope,
            "usable_approval": self.usable_approval,
            "next_step": self.next_step,
            "recovery": self.recovery,
        }

    def as_error_payload(self) -> dict[str, Any]:
        return {
            "type": type(self).__name__,
            "message": str(self),
            **self.as_event_payload(),
        }


async def check_spend_approval(
    request: CollectionRequest,
    estimate_usd: Decimal,
    *,
    now: datetime | None = None,
) -> SpendApprovalState | None:
    """Pre-flight (and choke-point re-check) for a request carrying an approval.

    Returns ``None`` when the request carries none (the ordinary ceilings still
    apply). Raises :class:`SpendApprovalExceededError` when the approval is
    unknown, not open, expired, or ``spent + estimate`` exceeds its ceiling.
    """
    approval_id = request.spend_approval_id
    if approval_id is None:
        return None
    approval_key = str(approval_id)
    scope = {"organization_id": request.organization_id, "operation": request.operation}

    def refuse(
        reason: str, state: SpendApprovalState | None, *, usable: bool = False
    ) -> SpendApprovalExceededError:
        """``usable=True`` only for an approval this call may draw on whose
        remaining headroom is too small; every other refusal is "no such
        usable approval" — no amounts, no recovery handle."""
        limit = state.ceiling_usd if state else Decimal(0)
        spent = state.spent_usd if state else Decimal(0)
        return SpendApprovalExceededError(
            approval_id=approval_key,
            reason=reason,
            limit_usd=limit,
            spent_usd=spent,
            projected_usd=spent + estimate_usd,
            new_estimate_usd=estimate_usd,
            scope=scope,
            usable_approval=usable,
        )

    resolver = _spend_approval_resolver
    if resolver is None:
        # Standalone posture: nothing here can read an approval, so an id is an
        # error — never treated as approved.
        raise refuse("no spend-approval resolver is installed on this host", None)
    state = await resolver.read(approval_key, request)
    if state is None:
        raise refuse(
            "no such approval exists for this organization, or it is not yours", None
        )
    # AN APPROVAL FUNDS ONLY WHAT IT WAS MINTED FOR (verification D2): provider
    # money, the site it named, and the collections of the person who approved it.
    if state.capability != PROVIDER_SPEND_CAPABILITY:
        raise refuse(f"the approval caps {state.capability}, not provider spend", state)
    # THE JOB: the tool + action the person approved, and nothing else.
    if not state.tool or not state.action:
        raise refuse("the approval names no job (tool and action)", state)
    if (request.spend_tool, request.spend_action) != (state.tool, state.action):
        raise refuse(
            f"the approval was for {state.tool}.{state.action}, not "
            f"{request.spend_tool}.{request.spend_action}",
            state,
        )
    # THE SITE: a site approval funds that site only; a site-less approval funds
    # only a call that itself had no site.
    if (str(state.site_id) if state.site_id else None) != (
        str(request.site_id) if request.site_id else None
    ):
        raise refuse("the approval was minted for a different site", state)
    if state.approved_by is not None and str(state.approved_by) != str(request.created_by):
        raise refuse("the approval belongs to a different person", state)
    moment = (now or datetime.now(UTC)).astimezone(UTC)
    if not state.usable_at(moment):
        reason = (
            "the approval has expired"
            if state.status == "open"
            else f"the approval is {state.status} (fully used or closed)"
        )
        raise refuse(reason, state)
    if state.spent_usd + estimate_usd > state.ceiling_usd:
        raise refuse("the estimate is larger than what remains", state, usable=True)
    return state


async def charge_spend_approval(
    request: CollectionRequest, amount_usd: Decimal, *, run_id: str
) -> None:
    """Record what a run under an approval actually cost. No-op without one."""
    if request.spend_approval_id is None or _spend_approval_resolver is None:
        return
    await _spend_approval_resolver.charge(
        str(request.spend_approval_id), max(amount_usd, Decimal(0)), run_id=run_id
    )


def current_month_bounds(now: datetime | None = None) -> tuple[datetime, datetime]:
    now = (now or datetime.now(UTC)).astimezone(UTC)
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = (
        start.replace(year=start.year + 1, month=1)
        if start.month == 12
        else start.replace(month=start.month + 1)
    )
    return start, end


def current_day_bounds(now: datetime | None = None) -> tuple[datetime, datetime]:
    now = (now or datetime.now(UTC)).astimezone(UTC)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return start, start + timedelta(days=1)


async def _spend(
    repository: SeoRepository,
    *,
    organization_id: str | None,
    provider: str | None,
    created_by: str | None,
    period_start: datetime,
    period_end: datetime,
) -> SpendSummary:
    return await repository.spend_summary(
        SpendQuery(
            organization_id=organization_id,
            provider=provider,
            created_by=created_by,
            period_start=period_start,
            period_end=period_end,
        )
    )


async def _billable(summary: SpendSummary) -> Decimal:
    """What this slice actually cost us, unpriced runs included.

    ``effective_cost`` only sums runs that carried cost evidence. A run with
    NULL in both cost columns is *unmeasured*, never free, so it is charged the
    ``seo.unpriced_run_assumed_cost_usd`` knob. A run that reported ``0.00`` —
    every free first-party provider — carries evidence and is charged nothing."""
    if summary.unpriced_run_count == 0:
        return summary.effective_cost
    unit = await unpriced_run_cost_usd()
    return summary.effective_cost + unit * summary.unpriced_run_count


async def billable_usd(summary: SpendSummary) -> Decimal:
    """Public door to :func:`_billable` — what a spend slice cost, unpriced runs
    charged the knob. Hosts computing headroom against the same ledger use this
    so they can never count spend differently from the budget gate."""
    return await _billable(summary)


async def _headroom(max_request_usd: Decimal | None) -> Decimal:
    return max_request_usd if max_request_usd is not None else await request_headroom_usd()


async def check_org_provider_monthly_budget(
    repository: SeoRepository,
    *,
    organization_id: str,
    provider: str,
    ceiling_usd: Decimal | None = None,
    max_request_usd: Decimal | None = None,
    now: datetime | None = None,
) -> SpendSummary:
    """Raise :class:`BudgetExceededError` (``ceiling='org_provider_monthly'``)
    if this organization's month-to-date spend on this provider, plus one
    more conservative worst-case call, would exceed the organization's monthly
    allowance. Returns the spend summary on success (callers stream it as a
    cost estimate)."""
    ceiling = (
        ceiling_usd
        if ceiling_usd is not None
        else await org_monthly_ceiling_usd(organization_id, provider)
    )
    max_request = await _headroom(max_request_usd)
    start, end = current_month_bounds(now)
    summary = await _spend(
        repository,
        organization_id=organization_id,
        provider=provider,
        created_by=None,
        period_start=start,
        period_end=end,
    )
    spent = await _billable(summary)
    projected = spent + max_request
    if projected > ceiling:
        raise BudgetExceededError(
            ceiling="org_provider_monthly",
            limit_usd=ceiling,
            spent_usd=spent,
            projected_usd=projected,
            scope={"organization_id": organization_id, "provider": provider, "period": "month"},
        )
    return summary


async def check_global_provider_monthly_budget(
    repository: SeoRepository,
    *,
    provider: str,
    ceiling_usd: Decimal | None = None,
    max_request_usd: Decimal | None = None,
    now: datetime | None = None,
) -> SpendSummary:
    """Raise :class:`BudgetExceededError` (``ceiling='global_platform_monthly'``)
    if the WHOLE platform's month-to-date spend on this provider, across every
    organization, plus one more worst-case call, would exceed the knob."""
    ceiling = (
        ceiling_usd
        if ceiling_usd is not None
        else await usd_knob(KNOB_FEATURE, "global_provider_monthly_ceiling_usd")
    )
    max_request = await _headroom(max_request_usd)
    start, end = current_month_bounds(now)
    summary = await _spend(
        repository,
        organization_id=None,
        provider=provider,
        created_by=None,
        period_start=start,
        period_end=end,
    )
    spent = await _billable(summary)
    projected = spent + max_request
    if projected > ceiling:
        raise BudgetExceededError(
            ceiling="global_platform_monthly",
            limit_usd=ceiling,
            spent_usd=spent,
            projected_usd=projected,
            scope={"provider": provider, "period": "month"},
        )
    return summary


async def check_caller_daily_budget(
    repository: SeoRepository,
    *,
    created_by: str,
    provider: str | None = None,
    ceiling_usd: Decimal | None = None,
    max_request_usd: Decimal | None = None,
    now: datetime | None = None,
) -> SpendSummary:
    """Enforce one caller's UTC-day ceiling before public-tool work."""
    ceiling = (
        ceiling_usd
        if ceiling_usd is not None
        else await usd_knob(KNOB_FEATURE, "caller_daily_ceiling_usd")
    )
    max_request = await _headroom(max_request_usd)
    start, end = current_day_bounds(now)
    summary = await _spend(
        repository,
        organization_id=None,
        provider=provider,
        created_by=created_by,
        period_start=start,
        period_end=end,
    )
    spent = await _billable(summary)
    projected = spent + max_request
    if projected > ceiling:
        raise BudgetExceededError(
            ceiling="caller_daily",
            limit_usd=ceiling,
            spent_usd=spent,
            projected_usd=projected,
            scope={"created_by": created_by, "provider": provider, "period": "day"},
        )
    return summary


async def check_global_daily_budget(
    repository: SeoRepository,
    *,
    provider: str | None = None,
    ceiling_usd: Decimal | None = None,
    max_request_usd: Decimal | None = None,
    now: datetime | None = None,
) -> SpendSummary:
    """Enforce the platform UTC-day ceiling before public-tool work."""
    ceiling = (
        ceiling_usd
        if ceiling_usd is not None
        else await usd_knob(KNOB_FEATURE, "global_daily_ceiling_usd")
    )
    max_request = await _headroom(max_request_usd)
    start, end = current_day_bounds(now)
    summary = await _spend(
        repository,
        organization_id=None,
        provider=provider,
        created_by=None,
        period_start=start,
        period_end=end,
    )
    spent = await _billable(summary)
    projected = spent + max_request
    if projected > ceiling:
        raise BudgetExceededError(
            ceiling="global_daily",
            limit_usd=ceiling,
            spent_usd=spent,
            projected_usd=projected,
            scope={"provider": provider, "period": "day"},
        )
    return summary


async def enforce_collection_budget(
    repository: SeoRepository, request: CollectionRequest, provider: str
) -> SpendSummary:
    """The default gate ``SeoCollectionService._execute_claimed`` calls before
    ANY paid provider work — the organization's monthly allowance (the tighter,
    more actionable scope; named first) and the platform-wide monthly backstop
    are both independently sufficient to reject. Neither ceiling
    check mutates state, so a rejected run's lease is released by the normal
    ``fail_run`` path the caller already runs on any exception."""
    org_summary = await check_org_provider_monthly_budget(
        repository, organization_id=request.organization_id, provider=provider
    )
    await check_global_provider_monthly_budget(repository, provider=provider)
    return org_summary


__all__ = [
    "KNOB_FEATURE",
    "PROVIDER_SPEND_CAPABILITY",
    "AccountCeilingResolver",
    "BudgetExceededError",
    "SpendApprovalExceededError",
    "billable_usd",
    "SpendApprovalResolver",
    "SpendApprovalState",
    "charge_spend_approval",
    "check_spend_approval",
    "get_spend_approval_resolver",
    "set_spend_approval_resolver",
    "check_caller_daily_budget",
    "check_global_daily_budget",
    "check_global_provider_monthly_budget",
    "check_org_provider_monthly_budget",
    "current_day_bounds",
    "current_month_bounds",
    "enforce_collection_budget",
    "org_monthly_ceiling_usd",
    "request_headroom_usd",
    "set_account_ceiling_resolver",
    "unpriced_run_cost_usd",
]
