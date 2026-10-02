"""Collection outcome seam — every collection run reports what it ACTUALLY
persisted, and a run that persisted nothing screams.

WHY THIS EXISTS (2026-08-04). GSC ingestion was 100% dead for five days and
no layer noticed:

* `fail_run` wrote `status='failed'` + a structured error — silently. No log,
  no alarm.
* A run that persists ZERO rows was indistinguishable from a healthy one:
  `complete_run` returns `created=0`, the nightly dispatcher counts the SITE
  as synced, and `AgentRunResult.success` stays True.
* Worst of all, an empty window still counts as *covered* by design
  (`gsc_run_covered_window`), so the watermark advances past days that never
  landed — a silent zero becomes PERMANENT.

So this seam fires on every terminal outcome of `_execute_claimed` — the one
body both `collect()` and `resume()` converge on. The package always screams
to console (it must work standalone); a host registers a durable sink
(aidream writes an ops-triage record) via `register_collection_outcome_sink`.

Never raises into the caller: an observability failure must not kill a
collection.
"""

from __future__ import annotations

import json
import logging
import re
from collections.abc import Callable
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# `logging`, never `print`: a host's root handler is what carries this to a
# durable log store (aidream ships every record to `public.app_log`). A bare
# print is invisible to every one of them, which would make the always-on
# scream the quietest layer here.
log = logging.getLogger(__name__)

CollectionOutcomeStatus = Literal["completed", "failed"]

# The problems this seam names. Ordered worst-first; `classify_outcome`
# returns the FIRST that applies so an alarm names the root cause.
CollectionProblem = Literal[
    "needs_reconnect",
    "failed",
    "zero_rows",
]

# A failed run whose cause is the ORGANIZATION'S provider access — a revoked or
# expired grant, a disconnected account, a property the connection no longer
# discovers — is not a platform defect. It is the customer's state: the site's
# ingestion banner already tells that organization to reconnect (matrx-frontend
# `features/marketing/google/gsc-property.ts` ACCESS_FAILURE_PATTERNS, which this
# list mirrors), and filing it as a high-severity platform alarm made
# `seo_collection_failed:gsc:search_performance` read as a ~7% platform failure
# rate when 16 of its 19 failures (30 days to 2026-09-25) were access states:
# two orgs' shared Google connection plus one QA fixture property.
# `invalid_client` is deliberately ABSENT: that is OUR OAuth client
# configuration, a platform defect.
_RECONNECT_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.I)
    for pattern in (
        r"ResourceBindingError",
        r"no live discovered",
        r"needs? re-?authentication",
        r"no vault credential",
        r"invalid_grant",
        r"insufficient.*(scope|permission)",
        r"unauthorized_client",
        r"access.*(revoked|denied)",
        r"token.*(expired|revoked)",
        r"connection.*(revoked|missing|no longer active)",
        r"was disconnected",
    )
)


def requires_reconnect(error: dict[str, Any] | None) -> bool:
    """True when a failed run's error is the organization's provider access,
    which only that organization can repair (reconnect / rebind)."""
    if not isinstance(error, dict):
        return False
    try:
        text = json.dumps(error, default=str)
    except (TypeError, ValueError):
        text = str(error)
    return any(pattern.search(text) for pattern in _RECONNECT_PATTERNS)

# NOT a problem here: "the window covered fewer distinct dates than it asked
# for". That looks like the perfect coverage guard and is in fact a wolf-crier
# — GSC returns NO ROW for a day with zero traffic, and the freshest day
# inside the 2-day finalization lag routinely hasn't landed yet. It would
# have fired on healthy runs nightly, on every site, which is exactly how an
# alarm becomes background noise and the next real outage goes unread.
# Coverage gaps are measured where they can be measured honestly: over the
# whole persisted history, by `seo.gsc_ingestion_health` (matrx-frontend), as
# a warning, not a per-run alarm.


class CollectionOutcomeEvent(BaseModel):
    """One terminal collection outcome, with expected-vs-actual attached."""

    model_config = ConfigDict(extra="forbid")

    provider: str
    capability: str
    operation: str
    run_id: str
    site_id: str | None = None
    organization_id: str | None = None
    trigger: str | None = None
    status: CollectionOutcomeStatus

    # What the request ASKED for.
    window_start: str | None = None
    window_end: str | None = None
    expected_days: int | None = None
    profiles: tuple[str, ...] = ()

    # What actually LANDED.
    observation_count: int = 0
    created: int = 0
    existing: int = 0
    distinct_dates: int = 0

    # Set when the run came from cache / an already-completed run, where
    # zero NEW rows is correct and must never alarm.
    reused: bool = False

    # A historical backfill window may legitimately predate the site itself,
    # and `gsc_run_covered_window` counts an empty window as covered BY
    # DESIGN so the frontier can't stall. Alarming on those would fire on
    # every backfill window, forever.
    is_backfill: bool = False

    # Has this site EVER landed a row for this capability? A parked or
    # brand-new property with genuinely zero traffic returns nothing every
    # night and is not broken. None = not determined (never alarms).
    site_has_prior_data: bool | None = None

    error: dict[str, Any] | None = None
    problem: CollectionProblem | None = None
    detail: dict[str, Any] = Field(default_factory=dict)

    @property
    def is_alarming(self) -> bool:
        """A PLATFORM problem — something we must fix."""
        return self.problem in ("failed", "zero_rows")

    @property
    def needs_customer_action(self) -> bool:
        """The organization's own provider access broke; only it can repair it."""
        return self.problem == "needs_reconnect"


def classify_outcome(event: CollectionOutcomeEvent) -> CollectionProblem | None:
    """The ONE predicate for 'this run is not okay'. Kept pure + importable so
    the host sink, the tests, and any future dashboard agree exactly."""
    if event.status == "failed":
        return "needs_reconnect" if requires_reconnect(event.error) else "failed"
    if event.reused:
        # A cache hit / re-run of a completed run legitimately creates nothing.
        return None
    if event.capability == "raw_provider":
        # Raw-provider operations persist the provider response as evidence but
        # deliberately create no normalized observation rows.  Applying the
        # ingestion zero-row predicate to metadata commands such as
        # bing_webmaster.sites.list makes every successful call an alarm.
        return None
    if event.created == 0 and event.existing == 0:
        # Zero rows is only a DEFECT for a site that has history and is being
        # kept current. The two exclusions below are not softening — an alarm
        # that fires on normal operation trains everyone to ignore it, which
        # is the failure this whole seam exists to prevent.
        if event.is_backfill:
            return None
        if event.site_has_prior_data is False:
            return None
        return "zero_rows"
    return None


CollectionOutcomeSink = Callable[[CollectionOutcomeEvent], None]

_SINKS: list[CollectionOutcomeSink] = []


def register_collection_outcome_sink(sink: CollectionOutcomeSink) -> None:
    """Host injection point (aidream wires the ops-triage writer)."""
    if sink not in _SINKS:
        _SINKS.append(sink)


def reset_collection_outcome_sinks() -> None:
    """Test helper — never call from product code."""
    _SINKS.clear()


def emit_collection_outcome(event: CollectionOutcomeEvent) -> None:
    """Fire every registered sink, then the always-on console fallback.

    Best-effort by construction: a sink that raises is reported and skipped,
    never propagated — observability must not break ingestion.
    """
    event.problem = classify_outcome(event)
    for sink in list(_SINKS):
        try:
            sink(event)
        except Exception as exc:  # noqa: BLE001 - a sink must never break a run
            log.warning("[collection-outcome] sink %r raised: %s", sink, exc)
    if event.is_alarming:
        _console_alarm(event)
    elif event.needs_customer_action:
        log.warning(
            "[collection-outcome] %s/%s run %s needs the organization to reconnect "
            "its provider access (site %s): %s",
            event.provider,
            event.capability,
            event.run_id,
            event.site_id,
            event.error,
        )


def _console_alarm(event: CollectionOutcomeEvent) -> None:
    """The standalone-safe scream. A host sink adds durability on top; this
    guarantees the package alone is never silent."""
    window = (
        f"{event.window_start}..{event.window_end}"
        if event.window_start or event.window_end
        else "n/a"
    )
    log.error(
        "\n#################### SEO COLLECTION ALARM ####################\n"
        f"  problem   : {event.problem}\n"
        f"  provider  : {event.provider} / {event.capability}\n"
        f"  run       : {event.run_id}  (trigger={event.trigger})\n"
        f"  site      : {event.site_id}\n"
        f"  window    : {window}  expected_days={event.expected_days}\n"
        f"  persisted : created={event.created} existing={event.existing} "
        f"observations={event.observation_count} distinct_dates={event.distinct_dates}\n"
        f"  error     : {event.error}\n"
        "##############################################################\n"
    )
