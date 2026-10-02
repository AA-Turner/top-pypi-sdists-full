"""Backlink change detection — what actually happened to a link we care about.

## Why this exists

`seo.backlink` is a CURRENT-STATE projection: the refresh upserts on
`(site_id, identity_key)` and overwrites `anchor_text`, `is_dofollow`, `state`
and `lost_at` with plain `Excluded(...)` values. So the moment a publisher
rewrites an anchor or flips a link to `rel="nofollow"`, the previous value is
gone and nothing anywhere records that it changed. The only surviving evidence
is `seo.backlink_observation` — append-only, one row per link per run — and
until now nothing compared consecutive rows.

This module is that comparison. It walks each link's observation chain, emits
one typed event per transition, and persists it to `seo.backlink_change_event`.

## The rule that matters most: ABSENCE IS NEVER LOSS

A link missing from a run's results says nothing about the web. It usually
means the run was truncated (the provider's detail limit is capped at 1,000
rows per call), or the provider paginated differently, or the call partially
failed. Inferring "lost" from absence would manufacture a wave of false
alarms — and "your link was removed" is exactly the alert a user acts on.

So loss is only ever read from a state the provider explicitly declared
(`state='lost'` / a `lost_date`), never from a link's silence.

## A change needs TWO RUNS — one run is a photograph, not a film

One `seo.backlink` row can have SEVERAL observation rows in a SINGLE run,
because its identity is `(site_id, source_url, target_url)` and a page is
perfectly entitled to link to the same target twice with different anchor text.
Measured on live data 2026-08-15: `dannegroni.com/resources/tag/millennials/page/2/`
links to one target as both "business coach" and "Titanium Success", in the same
snapshot.

Reading that as a chain — anchor A then anchor B — manufactures an
"anchor rewritten" event out of two links that coexist and never changed. So
observations are first COLLAPSED per run into one comparable point (the set of
anchors, the best follow state, whether any instance is live), and only those
per-run points are compared. A field difference inside one run is not a change;
it is what the page looks like.

## Why re-running is free

Every event's `dedupe_key` is derived from the pair that produced it
(`backlink_id` + kind + the observation being compared into). Re-running the
differ over an overlapping window produces the same keys and inserts nothing.
That is what lets the watcher use a generous lookback without bookkeeping.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from matrx_orm.operations.conflict_writes import bulk_insert_ignore
from pydantic import BaseModel, ConfigDict, Field

from matrx_seo.db import models_seo as m
from matrx_seo.identity import stable_hash

ChangeKind = Literal[
    "appeared",
    "lost",
    "restored",
    "anchor_changed",
    "dofollow_lost",
    "dofollow_gained",
    "target_changed",
    "source_page_dead",
    "source_page_redirected",
    "source_page_recovered",
]

#: Deterministic 0-100 severity per kind. This is the ONLY input to alerting,
#: so the numbers are a product decision, not a heuristic to tune later:
#: losing a dofollow link you earned is the worst thing that happens to a
#: backlink profile; gaining one needs no alarm.
#: A lost link's severity depends on what it was — a nofollow that disappears
#: is worth knowing, not worth interrupting anyone.
SEVERITY_LOST_DOFOLLOW = 90
SEVERITY_LOST_NOFOLLOW = 65
SEVERITY_DOFOLLOW_LOST = 80
SEVERITY_TARGET_CHANGED = 70
SEVERITY_ANCHOR_CHANGED = 40
SEVERITY_RESTORED = 35
SEVERITY_DOFOLLOW_GAINED = 25
SEVERITY_APPEARED_DOFOLLOW = 30
SEVERITY_APPEARED_NOFOLLOW = 20
SEVERITY_SOURCE_PAGE_DEAD = 85
SEVERITY_SOURCE_PAGE_REDIRECTED = 55
SEVERITY_SOURCE_PAGE_RECOVERED = 20

#: At or above this, the event becomes a platform.assists chip. Below it, the
#: event still exists and still shows in the feed — it just does not interrupt.
ALERT_SEVERITY_FLOOR = 60

#: Hard ceilings so one enormous site can never exhaust memory in a sweep that
#: is supposed to serve every site. Both are reported when they bite; a silent
#: truncation would read as "nothing changed".
MAX_OBSERVATIONS_PER_SITE = 40_000
BACKLINK_ID_CHUNK = 500

_OBSERVATION_FIELDS = (
    "id",
    "backlink_id",
    # snapshot_id IS the run identity. Without it every row looks like its own
    # run and two links coexisting on one page read as a change over time.
    "snapshot_id",
    "site_id",
    "source_url",
    "source_domain",
    "target_url",
    "anchor_text",
    "is_dofollow",
    "state",
    "first_seen_at",
    "last_seen_at",
    "lost_at",
    "created_at",
)


class ObservationPoint(BaseModel):
    """One link, as ONE RUN saw it — every observation row of that run, collapsed.

    A run may report the same link several times (a page linking twice to the
    same target with different anchors). Those rows are one photograph, not a
    sequence, so they are folded here: the anchors become a set, the follow
    state becomes the best instance, liveness becomes "any instance is live".
    """

    model_config = ConfigDict(extra="forbid")

    #: Representative observation row — what the event's FK points at.
    observation_id: str
    #: The run this point belongs to. Comparison only ever happens ACROSS runs.
    run_key: str
    backlink_id: str
    site_id: str
    source_url: str
    source_domain: str
    target_url: str | None = None
    anchor_texts: frozenset[str] = frozenset()
    is_dofollow: bool | None = None
    is_live: bool = True
    first_seen_at: datetime | None = None
    last_seen_at: datetime | None = None
    lost_at: datetime | None = None
    observed_at: datetime
    instance_count: int = 1

    @property
    def anchor_text(self) -> str | None:
        """The single anchor, when there is exactly one. For copy, not comparison."""
        return next(iter(self.anchor_texts)) if len(self.anchor_texts) == 1 else None

    def value_snapshot(self) -> dict[str, Any]:
        return {
            "anchor_text": self.anchor_text,
            "anchor_texts": sorted(self.anchor_texts),
            "is_dofollow": self.is_dofollow,
            "is_live": self.is_live,
            "target_url": self.target_url,
            "instance_count": self.instance_count,
            "first_seen_at": self.first_seen_at.isoformat() if self.first_seen_at else None,
            "last_seen_at": self.last_seen_at.isoformat() if self.last_seen_at else None,
            "lost_at": self.lost_at.isoformat() if self.lost_at else None,
            "observation_id": self.observation_id,
            "run_key": self.run_key,
        }


def collapse_run(rows: list[dict[str, Any]]) -> ObservationPoint | None:
    """Fold every observation row of ONE link in ONE run into one comparable point."""
    usable = [r for r in rows if r.get("backlink_id") is not None and r.get("source_url")]
    if not usable:
        return None
    ordered = sorted(usable, key=lambda r: r["created_at"])
    representative = ordered[-1]

    anchors = {a for a in (_normalized_anchor(r.get("anchor_text")) for r in ordered) if a}
    follow_flags = [r.get("is_dofollow") for r in ordered if r.get("is_dofollow") is not None]
    # A page that links to you once with dofollow and once without still gives
    # you a dofollow link; the best instance is the truth about the link.
    is_dofollow = any(follow_flags) if follow_flags else None
    # Likewise liveness: one live instance means the link is still there.
    is_live = any(str(r.get("state") or "active") != "lost" for r in ordered)

    first_seen = [r["first_seen_at"] for r in ordered if r.get("first_seen_at")]
    last_seen = [r["last_seen_at"] for r in ordered if r.get("last_seen_at")]
    lost = [r["lost_at"] for r in ordered if r.get("lost_at")]

    return ObservationPoint(
        observation_id=str(representative["id"]),
        run_key=str(representative.get("snapshot_id") or representative["created_at"]),
        backlink_id=str(representative["backlink_id"]),
        site_id=str(representative["site_id"]),
        source_url=str(representative["source_url"]),
        source_domain=str(representative["source_domain"] or ""),
        target_url=representative.get("target_url"),
        anchor_texts=frozenset(anchors),
        is_dofollow=is_dofollow,
        is_live=is_live,
        first_seen_at=min(first_seen) if first_seen else None,
        last_seen_at=max(last_seen) if last_seen else None,
        lost_at=max(lost) if lost else None,
        observed_at=representative["created_at"],
        instance_count=len(ordered),
    )


class BacklinkChange(BaseModel):
    """One detected transition, before it becomes a row."""

    model_config = ConfigDict(extra="forbid")

    backlink_id: str
    site_id: str
    change_kind: ChangeKind
    severity: int
    source_domain: str
    source_url: str
    target_url: str | None = None
    previous_value: dict[str, Any] = Field(default_factory=dict)
    current_value: dict[str, Any] = Field(default_factory=dict)
    previous_observation_id: str | None = None
    current_observation_id: str
    observed_at: datetime

    @property
    def dedupe_key(self) -> str:
        return stable_hash(
            {
                "backlink_id": self.backlink_id,
                "change_kind": self.change_kind,
                "current_observation_id": self.current_observation_id,
            }
        )

    @property
    def is_alertable(self) -> bool:
        return self.severity >= ALERT_SEVERITY_FLOOR


class SiteChangeDetection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    site_id: str
    observations_scanned: int = 0
    backlinks_compared: int = 0
    changes_detected: int = 0
    events_created: int = 0
    truncated: bool = False
    by_kind: dict[str, int] = Field(default_factory=dict)
    #: The rows that ACTUALLY landed this pass. The caller alerts on exactly
    #: these — never on a time-window re-read, which would race a concurrent
    #: pass and could alert on somebody else's rows or miss its own.
    created_event_ids: list[str] = Field(default_factory=list)


def _normalized_anchor(value: str | None) -> str | None:
    if value is None:
        return None
    collapsed = " ".join(value.split())
    return collapsed or None


def severity_for(kind: ChangeKind, *, is_dofollow: bool | None) -> int:
    if kind == "lost":
        return SEVERITY_LOST_DOFOLLOW if is_dofollow else SEVERITY_LOST_NOFOLLOW
    if kind == "appeared":
        return SEVERITY_APPEARED_DOFOLLOW if is_dofollow else SEVERITY_APPEARED_NOFOLLOW
    return {
        "dofollow_lost": SEVERITY_DOFOLLOW_LOST,
        "target_changed": SEVERITY_TARGET_CHANGED,
        "anchor_changed": SEVERITY_ANCHOR_CHANGED,
        "restored": SEVERITY_RESTORED,
        "dofollow_gained": SEVERITY_DOFOLLOW_GAINED,
        "source_page_dead": SEVERITY_SOURCE_PAGE_DEAD,
        "source_page_redirected": SEVERITY_SOURCE_PAGE_REDIRECTED,
        "source_page_recovered": SEVERITY_SOURCE_PAGE_RECOVERED,
    }[kind]


def _change(
    kind: ChangeKind,
    *,
    current: ObservationPoint,
    previous: ObservationPoint | None,
    is_dofollow: bool | None,
) -> BacklinkChange:
    return BacklinkChange(
        backlink_id=current.backlink_id,
        site_id=current.site_id,
        change_kind=kind,
        severity=severity_for(kind, is_dofollow=is_dofollow),
        source_domain=current.source_domain,
        source_url=current.source_url,
        target_url=current.target_url,
        previous_value=previous.value_snapshot() if previous is not None else {},
        current_value=current.value_snapshot(),
        previous_observation_id=previous.observation_id if previous is not None else None,
        current_observation_id=current.observation_id,
        observed_at=current.observed_at,
    )


def diff_pair(previous: ObservationPoint, current: ObservationPoint) -> list[BacklinkChange]:
    """Every transition between two consecutive observations of ONE link. Pure."""
    if previous.is_live and not current.is_live:
        # A lost link subsumes everything else about it. Reporting "the anchor
        # changed" alongside "the link is gone" is noise on top of bad news.
        return [
            _change("lost", current=current, previous=previous, is_dofollow=previous.is_dofollow)
        ]

    changes: list[BacklinkChange] = []
    if not previous.is_live and current.is_live:
        changes.append(
            _change("restored", current=current, previous=previous, is_dofollow=current.is_dofollow)
        )

    if previous.is_dofollow is not None and current.is_dofollow is not None:
        if previous.is_dofollow and not current.is_dofollow:
            changes.append(
                _change("dofollow_lost", current=current, previous=previous, is_dofollow=False)
            )
        elif not previous.is_dofollow and current.is_dofollow:
            changes.append(
                _change("dofollow_gained", current=current, previous=previous, is_dofollow=True)
            )

    # Set comparison, not string comparison: a page with two links to the same
    # target has two anchors at once, and their reporting ORDER varying between
    # runs is not the publisher rewriting anything.
    if previous.anchor_texts != current.anchor_texts:
        changes.append(
            _change(
                "anchor_changed",
                current=current,
                previous=previous,
                is_dofollow=current.is_dofollow,
            )
        )

    # NOTE: `target_changed` is deliberately never produced here. A backlink's
    # identity_key is (site_id, source_url, target_url), so a changed target is
    # a DIFFERENT seo.backlink row, not a mutation of this one. The kind stays
    # in the vocabulary for manual corrections and for the HTTP checker.
    return changes


def diff_chain(points: list[ObservationPoint], *, first_is_baseline: bool) -> list[BacklinkChange]:
    """Every transition across one link's ordered observation chain (oldest first).

    `first_is_baseline=True` means `points[0]` is the link's last observation
    from BEFORE the window: a comparison point only, never itself an event.
    `False` means the chain starts at the first observation we have ever had of
    this link, which is an `appeared` event — the only kind with no previous
    observation.
    """
    if not points:
        return []

    changes: list[BacklinkChange] = []
    first = points[0]
    if not first_is_baseline and first.is_live:
        changes.append(
            _change("appeared", current=first, previous=None, is_dofollow=first.is_dofollow)
        )
    for index in range(1, len(points)):
        changes.extend(diff_pair(points[index - 1], points[index]))
    return changes


def points_for_link(rows: list[dict[str, Any]]) -> list[ObservationPoint]:
    """One point per RUN for one link, oldest run first."""
    by_run: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        run_key = str(row.get("snapshot_id") or row["created_at"])
        by_run.setdefault(run_key, []).append(row)
    points = [p for p in (collapse_run(group) for group in by_run.values()) if p is not None]
    points.sort(key=lambda p: p.observed_at)
    return points


async def _load_window_observations(
    site_id: str, since: datetime
) -> tuple[list[dict[str, Any]], bool]:
    rows = await (
        m.BacklinkObservation.filter(site_id=site_id, created_at__gte=since)
        .order_by("backlink_id", "created_at")
        .limit(MAX_OBSERVATIONS_PER_SITE + 1)
        .values(*_OBSERVATION_FIELDS)
    )
    truncated = len(rows) > MAX_OBSERVATIONS_PER_SITE
    return rows[:MAX_OBSERVATIONS_PER_SITE], truncated


async def _load_baselines(
    site_id: str, backlink_ids: list[str], since: datetime
) -> dict[str, list[dict[str, Any]]]:
    """Every observation row of each link's newest run BEFORE the window.

    Two queries per chunk, not one: the newest prior row alone would carry only
    ONE of a multi-link page's anchors, and comparing a single anchor against
    the window's full anchor set would fabricate a rewrite at every window edge.
    """
    baselines: dict[str, list[dict[str, Any]]] = {}
    for start in range(0, len(backlink_ids), BACKLINK_ID_CHUNK):
        chunk = backlink_ids[start : start + BACKLINK_ID_CHUNK]
        newest = await (
            m.BacklinkObservation.filter(
                site_id=site_id, backlink_id__in=chunk, created_at__lt=since
            )
            .distinct("backlink_id")
            .order_by("backlink_id", "-created_at")
            .values("backlink_id", "snapshot_id")
        )
        wanted = {
            (str(row["backlink_id"]), str(row["snapshot_id"]))
            for row in newest
            if row.get("snapshot_id") is not None
        }
        snapshot_ids = sorted({snapshot for _, snapshot in wanted})
        if not snapshot_ids:
            # No snapshot linkage (legacy rows): fall back to the single newest
            # row per link, which is all the data there is.
            for row in await (
                m.BacklinkObservation.filter(
                    site_id=site_id, backlink_id__in=chunk, created_at__lt=since
                )
                .distinct("backlink_id")
                .order_by("backlink_id", "-created_at")
                .values(*_OBSERVATION_FIELDS)
            ):
                baselines[str(row["backlink_id"])] = [row]
            continue

        rows = await m.BacklinkObservation.filter(
            site_id=site_id,
            backlink_id__in=chunk,
            snapshot_id__in=snapshot_ids,
            created_at__lt=since,
        ).values(*_OBSERVATION_FIELDS)
        for row in rows:
            key = (str(row["backlink_id"]), str(row["snapshot_id"]))
            if key in wanted:
                baselines.setdefault(str(row["backlink_id"]), []).append(row)
    return baselines


def _event_row(
    change: BacklinkChange, *, organization_id: str, created_by: str, now: datetime
) -> dict[str, Any]:
    return {
        "id": str(uuid4()),
        "organization_id": organization_id,
        "created_by": created_by,
        "updated_by": created_by,
        "backlink_id": change.backlink_id,
        "site_id": change.site_id,
        "change_kind": change.change_kind,
        "severity": change.severity,
        "source_domain": change.source_domain,
        "source_url": change.source_url,
        "target_url": change.target_url,
        "previous_value": change.previous_value,
        "current_value": change.current_value,
        "previous_observation_id": change.previous_observation_id,
        "current_observation_id": change.current_observation_id,
        "observed_at": change.observed_at,
        "detected_at": now,
        "dedupe_key": change.dedupe_key,
    }


async def detect_site_changes(
    *,
    site_id: str,
    organization_id: str,
    created_by: str,
    since: datetime,
    now: datetime,
) -> SiteChangeDetection:
    """Compare every observation this site produced since `since` and persist the events.

    Idempotent: re-running over an overlapping window inserts nothing new.
    """
    rows, truncated = await _load_window_observations(site_id, since)
    result = SiteChangeDetection(
        site_id=site_id, observations_scanned=len(rows), truncated=truncated
    )
    if not rows:
        return result

    rows_by_backlink: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if row.get("backlink_id") is None or not row.get("source_url"):
            # A row with no link identity cannot be compared to anything. That
            # is a defect in the observation writer, not something to guess at.
            continue
        rows_by_backlink.setdefault(str(row["backlink_id"]), []).append(row)
    if not rows_by_backlink:
        return result

    baselines = await _load_baselines(site_id, sorted(rows_by_backlink), since)

    changes: list[BacklinkChange] = []
    for backlink_id, link_rows in rows_by_backlink.items():
        points = points_for_link(link_rows)
        if not points:
            continue
        baseline_rows = baselines.get(backlink_id) or []
        baseline_points = points_for_link(baseline_rows)
        if baseline_points:
            # The chain starts before the window, so the first windowed run is
            # a comparison, not a debut. Only the newest prior run is needed.
            changes.extend(diff_chain([baseline_points[-1], *points], first_is_baseline=True))
        else:
            changes.extend(diff_chain(points, first_is_baseline=False))
    result.backlinks_compared = len(rows_by_backlink)
    result.changes_detected = len(changes)
    for change in changes:
        result.by_kind[change.change_kind] = result.by_kind.get(change.change_kind, 0) + 1

    if not changes:
        return result

    created = await bulk_insert_ignore(
        m.BacklinkChangeEvent,
        [
            _event_row(change, organization_id=organization_id, created_by=created_by, now=now)
            for change in changes
        ],
        on_conflict=["dedupe_key"],
        returning=True,
    )
    created_rows = created or []
    result.created_event_ids = [
        str(row["id"] if isinstance(row, dict) else row.id) for row in created_rows
    ]
    result.events_created = len(result.created_event_ids)
    return result


__all__ = [
    "ALERT_SEVERITY_FLOOR",
    "BacklinkChange",
    "ChangeKind",
    "ObservationPoint",
    "SiteChangeDetection",
    "detect_site_changes",
    "diff_chain",
    "diff_pair",
    "severity_for",
]
