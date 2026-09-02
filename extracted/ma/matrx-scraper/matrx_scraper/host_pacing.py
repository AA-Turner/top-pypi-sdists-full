"""How fast may we crawl THIS host — detect first, then climb, never hammer.

**Arman, 2026-08-20**, ruling on the crawl-rate question (and rejecting the
question, which offered a choice of static defaults):

    "The first thing we need to do is try to detect the system. So if you're
    saying Shopify class has certain rules, well, then we better check if it's
    Shopify and if it is, then follow their rules. And I bet there are other
    known things as well. And then the other part is we should never hammer them
    first and then just see what happens. We should start low and then keep going
    up and keep pushing up higher and higher and higher until we figure out what
    the limit is and then back off from it."

The behaviour this replaces opened every crawl at a flat 4 rps, tripped
Shopify-class limiters on the first burst, and only then let the adaptive
throttle back off. The crawl finished; the host got hammered on the way.

## The order of authority

A pacing decision is made once per host, from the most authoritative source
available. Each source is a strictly better answer than the one below it:

1. **The user's explicit maximum.** A caller-supplied ``host_rps`` is a CEILING
   the ramp may never exceed. It is not a starting rate any more — that is the
   whole point of the ruling.
2. **``robots.txt`` ``Crawl-delay`` / ``Request-rate``.** The one place a site
   states its own pacing in machine-readable form. Honoured as an UPPER BOUND
   (see :data:`~matrx_scraper.robots_txt.MAX_HONOURED_CRAWL_DELAY_SECONDS` for
   the one clamp, which is reported and never silent).
3. **A published platform limit.** ``host_platform`` matched a profile whose
   ``basis`` is ``published`` — Shopify's 2/s, say. A documented number is a
   ceiling, not an opening guess, so the ramp holds at it.
4. **A remembered ceiling.** What the last run against this host actually
   discovered. Re-probing from zero on every crawl is the same wasted politeness
   as hammering is rudeness, so the next run opens near what we learned — at
   :attr:`PacingKnobs.remembered_start_fraction` of it, never AT it.
5. **A platform's observed/conservative rate.** An opening rate only; the ramp
   is expected to climb past it.
6. **Nothing.** Open at the floor and climb.

## The ramp

Climb by :attr:`PacingKnobs.ramp_factor` after every
:attr:`PacingKnobs.ramp_after_clean` consecutive clean responses; stop climbing
at the ceiling. A rate-limit signal (429/503) or a latency inflection is the
host saying "that was too much": back off, and RECORD the rate that provoked it
so neither this run nor the next one climbs back into it.

Discovery is deliberately conservative in one direction only. We would rather
under-use a host that could take more than find its limit twice.

Pure policy — no network, no DB, no sibling matrx imports. Durable memory of a
discovered ceiling is the HOST's job, handed in as :class:`RememberedPacing` and
handed back through :meth:`HostRamp.snapshot`.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Literal

from matrx_scraper.host_platform import PlatformMatch, detect_platform, profile_for
from matrx_scraper.robots_txt import MAX_HONOURED_CRAWL_DELAY_SECONDS

logger = logging.getLogger(__name__)

__all__ = [
    "PacingKnobs",
    "PacingSource",
    "HostPacingPlan",
    "RememberedPacing",
    "HostRamp",
    "resolve_plan",
    "DEFAULT_KNOBS",
]

PacingSource = Literal[
    "floor",
    "platform_published",
    "platform_observed",
    "robots_crawl_delay",
    "remembered",
    "user_max",
]


@dataclass(frozen=True)
class PacingKnobs:
    """Every tunable number in the ramp, in ONE place, per feature.

    **Agent-set limits (blind approval).** Set by the crawler-pacing session on
    2026-08-20. Basis: a crawl must not trip a Shopify-class limiter on its
    opening burst (measured: 4 rps did, immediately), while a 500-page crawl of
    a healthy host must still finish in minutes. At these values a host with no
    known rules is fetched at 0.5/s for the first 10 pages and reaches 8+ rps
    after roughly 70 clean responses — under a minute of ramp for a crawl that
    would otherwise have opened by hammering. Arman approved this class of
    decision in advance (2026-08-20) and has NOT reviewed these specific
    numbers. **Review due 2026-10-15**, once real crawl telemetry exists.

    These are DEFAULTS, not constants: the host fills this dataclass from the
    site's saved crawl settings, so every value is admin-adjustable per site
    without a deploy (`limits-are-knobs-agents-set-them.md`).
    """

    #: Opening rate against a host we know nothing about. One request every 2s.
    floor_rps: float = 0.5
    #: The ramp never climbs past this, whatever it discovers. Protects the host
    #: AND the shared scraper box, which is burstable-CPU.
    max_rps: float = 12.0
    #: Multiplier applied on each successful climb step.
    ramp_factor: float = 1.5
    #: Consecutive clean responses required before the next climb.
    ramp_after_clean: int = 10
    #: Multiplier applied when the host signals a limit (429/503/latency).
    backoff_factor: float = 0.5
    #: The rate that provoked a limit is remembered at this fraction of itself —
    #: we hold BELOW the discovered ceiling, never at it.
    ceiling_hold: float = 0.75
    #: A later run opens at this fraction of the remembered ceiling.
    remembered_start_fraction: float = 0.8
    #: Rolling response latency this many times the baseline measured at the
    #: opening rate counts as the host straining, even without a 429.
    latency_inflection_factor: float = 2.5
    #: Latency below this is noise, not a signal — a 40 ms page going to 100 ms
    #: says nothing about load.
    latency_floor_ms: float = 250.0
    #: The ramp never drops below this, however hard a host pushes back. Below
    #: it the crawl is not slow, it is broken, and the truncation gate is the
    #: honest answer instead.
    min_rps: float = 0.1

    def bounded(self, rps: float) -> float:
        return max(self.min_rps, min(self.max_rps, rps))


DEFAULT_KNOBS = PacingKnobs()


@dataclass(frozen=True)
class RememberedPacing:
    """What a previous run discovered about this host. Supplied by the host."""

    host: str
    ceiling_rps: float
    #: Where that ceiling came from, so a remembered PLATFORM rule is not
    #: mistaken for something we measured.
    source: PacingSource
    platform: str | None = None
    observed_at: str | None = None  # ISO-8601, display only
    limit_hits: int = 0


@dataclass(frozen=True)
class HostPacingPlan:
    """The resolved opening rate and ceiling for one host, with its reasons."""

    host: str
    start_rps: float
    ceiling_rps: float
    source: PacingSource
    platform: str | None = None
    platform_display: str | None = None
    fronted_by: str | None = None
    crawl_delay_seconds: float | None = None
    #: Human-readable sentences, in the order they were decided. This is what
    #: the UI shows: a clamped setting the user cannot see is a defect
    #: (crawler vision point 8).
    notes: tuple[str, ...] = ()
    #: True when the user's requested rate was lowered by something we learned.
    #: The UI must say so rather than silently showing the requested number.
    user_max_reduced: bool = False

    def as_dict(self) -> dict[str, object]:
        """The wire/persistence shape. One spelling, every consumer."""
        return {
            "host": self.host,
            "start_rps": round(self.start_rps, 3),
            "ceiling_rps": round(self.ceiling_rps, 3),
            "source": self.source,
            "platform": self.platform,
            "platform_display": self.platform_display,
            "fronted_by": self.fronted_by,
            "crawl_delay_seconds": self.crawl_delay_seconds,
            "notes": list(self.notes),
            "user_max_reduced": self.user_max_reduced,
        }


def resolve_plan(
    host: str,
    *,
    user_max_rps: float | None = None,
    platform: PlatformMatch | None = None,
    crawl_delay_seconds: float | None = None,
    remembered: RememberedPacing | None = None,
    knobs: PacingKnobs = DEFAULT_KNOBS,
) -> HostPacingPlan:
    """Decide the opening rate and the ceiling, and say why for each.

    Every input is optional: the plan degrades to "open at the floor and climb",
    which is the correct answer when we know nothing and is never a hammer.
    """

    notes: list[str] = []
    ceiling = knobs.max_rps
    ceiling_source: PacingSource = "floor"
    start = knobs.floor_rps
    start_source: PacingSource = "floor"
    user_max_reduced = False

    # --- 3/5. platform ---------------------------------------------------
    platform_name = platform.name if platform else None
    platform_display = platform.profile.display_name if platform else None
    fronted_by = platform.fronted_by.display_name if platform and platform.fronted_by else None
    if platform is not None:
        notes.append(f"Detected {platform.describe()}.")
        rate = platform.profile.sustained_rps
        if rate is not None:
            if platform.profile.basis == "published":
                ceiling = min(ceiling, rate)
                ceiling_source = "platform_published"
                start = min(rate, knobs.max_rps)
                start_source = "platform_published"
                notes.append(
                    f"{platform.profile.display_name} publishes a limit — holding at "
                    f"{rate:g} req/s. {platform.profile.rationale}"
                )
            else:
                start = min(rate, knobs.max_rps)
                start_source = "platform_observed"
                notes.append(
                    f"Opening at {rate:g} req/s for {platform.profile.display_name} and "
                    f"climbing from there. {platform.profile.rationale}"
                )
        else:
            notes.append(platform.profile.rationale)

    # --- 4. what the last run learned ------------------------------------
    if remembered is not None and remembered.ceiling_rps > 0:
        learned = knobs.bounded(remembered.ceiling_rps)
        # A remembered ceiling never RAISES a published platform limit — the
        # platform's own documented rate outranks anything we measured against
        # one lucky host behind it.
        if ceiling_source == "platform_published":
            learned = min(learned, ceiling)
        ceiling = min(ceiling, learned) if ceiling_source != "floor" else learned
        ceiling_source = "remembered"
        start = knobs.bounded(learned * knobs.remembered_start_fraction)
        start_source = "remembered"
        notes.append(
            f"A previous crawl of {remembered.host} settled at {learned:.2f} req/s"
            f"{f' after {remembered.limit_hits} rate-limit signals' if remembered.limit_hits else ''}"
            f" — opening at {start:.2f} req/s instead of probing from zero."
        )

    # --- 2. robots.txt, an upper bound over everything above --------------
    if crawl_delay_seconds is not None and crawl_delay_seconds > 0:
        honoured = crawl_delay_seconds
        if honoured > MAX_HONOURED_CRAWL_DELAY_SECONDS:
            notes.append(
                f"robots.txt asks for {crawl_delay_seconds:g}s between requests, which would "
                f"take days for a normal site; honouring "
                f"{MAX_HONOURED_CRAWL_DELAY_SECONDS:g}s instead — the slowest we will go on a "
                "stated delay."
            )
            honoured = MAX_HONOURED_CRAWL_DELAY_SECONDS
        robots_rps = max(knobs.min_rps, 1.0 / honoured)
        if robots_rps < ceiling:
            ceiling = robots_rps
            ceiling_source = "robots_crawl_delay"
            notes.append(
                f"robots.txt asks for {crawl_delay_seconds:g}s between requests — capped at "
                f"{robots_rps:.3f} req/s."
            )
        start = min(start, robots_rps)
        if start_source == "floor" or start >= robots_rps:
            start_source = "robots_crawl_delay"

    # --- 1. the user's explicit maximum, a ceiling and never a start ------
    if user_max_rps is not None and user_max_rps > 0:
        if user_max_rps < ceiling:
            ceiling = user_max_rps
            ceiling_source = "user_max"
            notes.append(f"Your configured maximum of {user_max_rps:g} req/s applies.")
        elif user_max_rps > ceiling:
            user_max_reduced = True
            notes.append(
                f"Your configured maximum is {user_max_rps:g} req/s, but this host is held to "
                f"{ceiling:.2f} req/s by the rule above."
            )

    ceiling = knobs.bounded(ceiling)
    start = knobs.bounded(min(start, ceiling))
    if not notes:
        notes.append(
            f"Nothing is known about this host yet — opening at {start:.2f} req/s and climbing "
            "until it pushes back."
        )

    return HostPacingPlan(
        host=host,
        start_rps=start,
        ceiling_rps=ceiling,
        source=ceiling_source if ceiling_source != "floor" else start_source,
        platform=platform_name,
        platform_display=platform_display,
        fronted_by=fronted_by,
        crawl_delay_seconds=crawl_delay_seconds,
        notes=tuple(notes),
        user_max_reduced=user_max_reduced,
    )


@dataclass
class HostRamp:
    """The climb/back-off state machine for ONE host.

    Not thread-safe by design and not asyncio-locked: every mutation is a small
    arithmetic update on integers and floats made from the crawl's own workers,
    and a lost increment costs one deferred climb step, never correctness. The
    rate it produces is applied through the rate limiter, which IS locked.
    """

    plan: HostPacingPlan
    knobs: PacingKnobs = DEFAULT_KNOBS
    current_rps: float = 0.0
    consecutive_clean: int = 0
    limit_hits: int = 0
    climbs: int = 0
    #: The highest rate we held without the host complaining.
    highest_clean_rps: float = 0.0
    #: The rate at which the host last pushed back, if it ever has. This is the
    #: DISCOVERED ceiling — the number worth remembering across runs.
    discovered_limit_rps: float | None = None
    _latency_baseline_ms: float | None = field(default=None, repr=False)
    _latency_ewma_ms: float | None = field(default=None, repr=False)
    _last_change_at: float = field(default_factory=time.monotonic, repr=False)

    def __post_init__(self) -> None:
        if self.current_rps <= 0:
            self.current_rps = self.plan.start_rps
            self.highest_clean_rps = self.plan.start_rps

    # -- signals ---------------------------------------------------------

    def observe_success(self, *, latency_ms: float | None = None) -> float | None:
        """Record one clean response. Returns the new rate iff it changed.

        A "clean" response is one the host served without complaint. Latency is
        optional: a caller that cannot measure it simply forfeits the inflection
        check, it does not get a wrong one.
        """

        self.consecutive_clean += 1
        if self.current_rps > self.highest_clean_rps:
            self.highest_clean_rps = self.current_rps

        if latency_ms is not None and latency_ms > 0:
            self._latency_ewma_ms = (
                latency_ms
                if self._latency_ewma_ms is None
                else self._latency_ewma_ms * 0.8 + latency_ms * 0.2
            )
            if self._latency_baseline_ms is None and self.consecutive_clean >= 3:
                # The baseline is what this host costs at the OPENING rate, so it
                # is captured before any climb has had a chance to distort it.
                self._latency_baseline_ms = self._latency_ewma_ms

        if self.consecutive_clean < self.knobs.ramp_after_clean:
            return None
        if self.current_rps >= self.ceiling:
            # Already at the ceiling — hold. Resetting the counter keeps the
            # ramp from banking thousands of "credits" it would spend all at
            # once if the ceiling later rose.
            self.consecutive_clean = 0
            return None
        if self._latency_straining():
            self.consecutive_clean = 0
            self._record_limit(reason="latency")
            return self.current_rps
        return self._climb()

    def observe_limit(self, *, reason: str = "rate_limited") -> float:
        """The host pushed back (429/503). Back off and remember the rate."""

        self.consecutive_clean = 0
        self.limit_hits += 1
        self._record_limit(reason=reason)
        return self.current_rps

    # -- internals -------------------------------------------------------

    def _latency_straining(self) -> bool:
        baseline = self._latency_baseline_ms
        current = self._latency_ewma_ms
        if baseline is None or current is None:
            return False
        if current < self.knobs.latency_floor_ms:
            return False
        return current >= baseline * self.knobs.latency_inflection_factor

    def _climb(self) -> float:
        self.consecutive_clean = 0
        self.climbs += 1
        target = min(self.current_rps * self.knobs.ramp_factor, self.ceiling)
        self.current_rps = self.knobs.bounded(target)
        self._last_change_at = time.monotonic()
        return self.current_rps

    def _record_limit(self, *, reason: str) -> None:
        provoking_rate = self.current_rps
        held = self.knobs.bounded(provoking_rate * self.knobs.ceiling_hold)
        self.discovered_limit_rps = (
            held if self.discovered_limit_rps is None else min(self.discovered_limit_rps, held)
        )
        self.current_rps = self.knobs.bounded(provoking_rate * self.knobs.backoff_factor)
        self._last_change_at = time.monotonic()
        # The baseline was measured under conditions that no longer hold; a
        # stale one would report "straining" forever after one slow patch.
        self._latency_baseline_ms = None
        self._latency_ewma_ms = None
        logger.warning(
            "host %s pushed back (%s) at %.2f req/s — backed off to %.2f, ceiling now %.2f",
            self.plan.host,
            reason,
            provoking_rate,
            self.current_rps,
            self.ceiling,
        )

    @property
    def ceiling(self) -> float:
        """The live ceiling: the plan's, lowered by anything we have discovered."""
        if self.discovered_limit_rps is None:
            return self.plan.ceiling_rps
        return min(self.plan.ceiling_rps, self.discovered_limit_rps)

    # -- reporting -------------------------------------------------------

    def snapshot(self) -> dict[str, object]:
        """What the UI shows and what the host persists as the memory.

        ``discovered_ceiling_rps`` is only set once the host has ACTUALLY pushed
        back. A run that never found a limit reports ``None`` there and the
        highest clean rate beside it — claiming a ceiling we never hit would
        teach the next run a number we invented.
        """

        return {
            **self.plan.as_dict(),
            "current_rps": round(self.current_rps, 3),
            "effective_ceiling_rps": round(self.ceiling, 3),
            "discovered_ceiling_rps": (
                round(self.discovered_limit_rps, 3)
                if self.discovered_limit_rps is not None
                else None
            ),
            "highest_clean_rps": round(self.highest_clean_rps, 3),
            "limit_hits": self.limit_hits,
            "climbs": self.climbs,
        }

    def to_remembered(self) -> RememberedPacing | None:
        """The durable memory for the next run, or None if we learned nothing.

        A run that was never pushed back on still learned something worth
        keeping — the rate it sustained cleanly — but only when it actually
        climbed above where it opened. Opening at 0.5 and staying there because
        the crawl was six pages long teaches nothing.
        """

        if self.discovered_limit_rps is not None:
            return RememberedPacing(
                host=self.plan.host,
                ceiling_rps=self.discovered_limit_rps,
                source="remembered",
                platform=self.plan.platform,
                limit_hits=self.limit_hits,
            )
        if self.climbs > 0 and self.highest_clean_rps > self.plan.start_rps:
            return RememberedPacing(
                host=self.plan.host,
                ceiling_rps=self.highest_clean_rps,
                source="remembered",
                platform=self.plan.platform,
                limit_hits=0,
            )
        return None


def plan_from_first_response(
    host: str,
    *,
    headers: dict[str, str] | None,
    html: str | None,
    user_max_rps: float | None = None,
    crawl_delay_seconds: float | None = None,
    remembered: RememberedPacing | None = None,
    knobs: PacingKnobs = DEFAULT_KNOBS,
) -> HostPacingPlan:
    """Convenience: detect the platform from one response, then resolve."""

    return resolve_plan(
        host,
        user_max_rps=user_max_rps,
        platform=detect_platform(headers=headers, html=html),
        crawl_delay_seconds=crawl_delay_seconds,
        remembered=remembered,
        knobs=knobs,
    )


def plan_for_known_platform(
    host: str,
    platform_name: str,
    *,
    user_max_rps: float | None = None,
    crawl_delay_seconds: float | None = None,
    remembered: RememberedPacing | None = None,
    knobs: PacingKnobs = DEFAULT_KNOBS,
) -> HostPacingPlan:
    """Resolve for a platform someone already identified (a stored probe)."""

    profile = profile_for(platform_name)
    match = PlatformMatch(profile=profile, signals=("stored",)) if profile else None
    return resolve_plan(
        host,
        user_max_rps=user_max_rps,
        platform=match,
        crawl_delay_seconds=crawl_delay_seconds,
        remembered=remembered,
        knobs=knobs,
    )


__all__ += ["plan_from_first_response", "plan_for_known_platform"]
