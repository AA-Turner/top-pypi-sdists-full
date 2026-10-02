"""Search opportunities — Search Console pages near the top, scored by what they are worth.

Pure: no I/O. The host reads both sources LIVE (Search Console by page, GA4
organic landing pages) and hands the rows here; this module joins them, picks
the candidates, and scores them.

Method (OpenSEO ``SearchOpportunityService``, commit ``0ffff93``; spec
OPENSEO-TOOLS-SPEC §5.5 item 6):

* **Join key** — lowercase host, default port dropped, scheme / query /
  fragment ignored, trailing slash stripped except at the root, path case and
  subdomains kept (``www`` is not the apex). ``(not set)`` or an unparseable
  URL is unmatched and counted, never guessed.
* **Candidates** — Search Console pages whose position is inside the
  ``position_range`` knob (OpenSEO: 4–20).
* **Score** over JOINED candidates only: percentile rank
  (``count(values < v) / (n − 1)``, ties share a rank, ``n = 1`` → 1) of
  demand = ``log1p(impressions)``, value = ``sessionKeyEventRate`` (or
  ``engagementRate`` when every joined row has zero key events — flagged
  ``engagement_fallback``), reach = ``20 − position``;
  ``score = round(100·(w_demand·d + w_value·v + w_reach·r))``.
* **Unmatched Search Console pages stay visible, unscored, last.** Unknown is
  ``None``, never ``0``.

Where we go past OpenSEO: several GA4 rows (or Search Console rows) that land on
one join key are MERGED (sums, session-weighted rates, impression-weighted
position) instead of the last one silently winning; and business value can come
from what the business says an offering is worth (``value_source =
"offering_worth"``), ranked within the pages that have a worth, with every page
that has none falling back to the GA4 metric and saying so on its row.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any, Literal
from urllib.parse import urlsplit

ValueSource = Literal["ga4", "offering_worth"]

SCORE_DISCLAIMER = "The score ranks these pages; it is not a forecast."


@dataclass(frozen=True, slots=True)
class GscPageRow:
    """One Search Console row with dimension ``page`` for the whole window."""

    page: str
    clicks: int
    impressions: int
    position: float


@dataclass(frozen=True, slots=True)
class Ga4LandingRow:
    """One GA4 organic landing-page row (``hostName`` + ``landingPage``)."""

    host: str
    landing_page: str
    sessions: float | None
    engaged_sessions: float | None
    engagement_rate: float | None
    key_events: float | None
    session_key_event_rate: float | None


@dataclass(frozen=True, slots=True)
class Weights:
    demand: float
    value: float
    reach: float

    @classmethod
    def from_knob(cls, raw: Mapping[str, Any]) -> Weights:
        try:
            weights = cls(
                demand=float(raw["demand"]), value=float(raw["value"]), reach=float(raw["reach"])
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(
                "opportunity.weights must be an object with numeric demand, value and reach"
            ) from exc
        if min(weights.demand, weights.value, weights.reach) < 0:
            raise ValueError("opportunity.weights cannot be negative")
        return weights


def normalize_page_key(value: str | None) -> str | None:
    """The join key, or ``None`` when the value cannot be joined honestly."""

    if value is None:
        return None
    trimmed = value.strip()
    if not trimmed or trimmed.lower() == "(not set)":
        return None
    candidate = trimmed if "://" in trimmed else f"https://{trimmed}"
    try:
        parts = urlsplit(candidate)
        host = (parts.hostname or "").lower()
        port = parts.port
    except ValueError:
        return None
    if not host:
        return None
    scheme = parts.scheme.lower()
    if port is not None and not (
        (scheme == "http" and port == 80) or (scheme == "https" and port == 443)
    ):
        host = f"{host}:{port}"
    path = parts.path or "/"
    if len(path) > 1:
        path = path.rstrip("/") or "/"
    return f"{host}{path}"


def percentile_ranks(values: list[float]) -> list[float]:
    """``count(values < v) / (n − 1)``; ties share a rank; ``n = 1`` → ``[1.0]``."""

    n = len(values)
    if n == 0:
        return []
    if n == 1:
        return [1.0]
    ordered = sorted(values)
    out: list[float] = []
    for value in values:
        lower = _count_below(ordered, value)
        out.append(lower / (n - 1))
    return out


def _count_below(ordered: list[float], value: float) -> int:
    lo, hi = 0, len(ordered)
    while lo < hi:
        mid = (lo + hi) // 2
        if ordered[mid] < value:
            lo = mid + 1
        else:
            hi = mid
    return lo


@dataclass(slots=True)
class _Ga4Merged:
    sessions: float | None = None
    engaged_sessions: float | None = None
    key_events: float | None = None
    # session-weighted sums for the two rates
    _ekr_weighted: float = 0.0
    _ekr_weight: float = 0.0
    _er_weighted: float = 0.0
    _er_weight: float = 0.0
    rows: int = 0

    def add(self, row: Ga4LandingRow) -> None:
        self.rows += 1
        self.sessions = _plus(self.sessions, row.sessions)
        self.engaged_sessions = _plus(self.engaged_sessions, row.engaged_sessions)
        self.key_events = _plus(self.key_events, row.key_events)
        weight = row.sessions or 0.0
        if row.session_key_event_rate is not None:
            self._ekr_weighted += row.session_key_event_rate * max(weight, 1e-12)
            self._ekr_weight += max(weight, 1e-12)
        if row.engagement_rate is not None:
            self._er_weighted += row.engagement_rate * max(weight, 1e-12)
            self._er_weight += max(weight, 1e-12)

    @property
    def session_key_event_rate(self) -> float | None:
        return self._ekr_weighted / self._ekr_weight if self._ekr_weight else None

    @property
    def engagement_rate(self) -> float | None:
        return self._er_weighted / self._er_weight if self._er_weight else None


def _plus(a: float | None, b: float | None) -> float | None:
    if a is None:
        return b
    if b is None:
        return a
    return a + b


@dataclass(slots=True)
class _GscMerged:
    page: str
    clicks: int = 0
    impressions: int = 0
    _pos_weighted: float = 0.0
    _pos_weight: float = 0.0

    def add(self, row: GscPageRow) -> None:
        self.clicks += int(row.clicks)
        self.impressions += int(row.impressions)
        weight = float(max(row.impressions, 0)) or 1e-12
        self._pos_weighted += float(row.position) * weight
        self._pos_weight += weight

    @property
    def position(self) -> float:
        return self._pos_weighted / self._pos_weight if self._pos_weight else 0.0


@dataclass(slots=True)
class OpportunityResult:
    rows: list[dict[str, Any]]
    formula: str
    #: ``None`` when GA4 was never read: there is no value metric to name.
    value_metric: str | None
    #: ``None`` when GA4 was never read (unknown, not "no fallback happened").
    engagement_fallback: bool | None
    coverage: dict[str, int | None]
    truncated: dict[str, bool | None]
    notices: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "rows": self.rows,
            "formula": self.formula,
            "value_metric": self.value_metric,
            "engagement_fallback": self.engagement_fallback,
            "coverage": self.coverage,
            "truncated": self.truncated,
            "disclaimer": SCORE_DISCLAIMER,
        }


def score_search_opportunities(
    gsc_rows: Iterable[GscPageRow],
    ga4_rows: Iterable[Ga4LandingRow],
    *,
    weights: Weights,
    position_min: float,
    position_max: float,
    limit: int,
    value_source: ValueSource = "ga4",
    offering_worth: Mapping[str, float] | None = None,
    gsc_truncated: bool = False,
    ga4_truncated: bool = False,
    ga4_read: bool = True,
) -> OpportunityResult:
    """Join, pick candidates, score, sort. ``offering_worth`` maps a JOIN KEY to
    the page's business worth (only read when ``value_source='offering_worth'``).

    ``ga4_read=False`` means GA4 was never read (the host's read failed): every
    candidate is ``gsc_only`` and unscored, and every GA4-derived figure —
    rows considered, matches, the value metric, the engagement fallback, GA4
    truncation — is ``None`` (unknown), never ``0`` or ``False``."""

    if not ga4_read:
        ga4_rows = ()

    gsc_list = list(gsc_rows)
    ga4_list = list(ga4_rows)

    ga4_by_key: dict[str, _Ga4Merged] = {}
    unparseable_ga4 = 0
    for row in ga4_list:
        key = normalize_page_key(f"{row.host}{row.landing_page}")
        if key is None or row.landing_page.strip().lower() == "(not set)":
            unparseable_ga4 += 1
            continue
        ga4_by_key.setdefault(key, _Ga4Merged()).add(row)

    gsc_by_key: dict[str, _GscMerged] = {}
    unparseable_gsc: list[GscPageRow] = []
    for row in gsc_list:
        key = normalize_page_key(row.page)
        if key is None:
            unparseable_gsc.append(row)
            continue
        gsc_by_key.setdefault(key, _GscMerged(page=row.page)).add(row)

    candidates: list[dict[str, Any]] = []
    for key, merged in gsc_by_key.items():
        position = merged.position
        if not (position_min <= position <= position_max):
            continue
        analytics = ga4_by_key.get(key)
        candidates.append(
            {
                "_key": key,
                "_ga4": analytics,
                "page": merged.page,
                "position": round(position, 2),
                "impressions": merged.impressions,
                "clicks": merged.clicks,
                "sessions": _num(analytics.sessions) if analytics else None,
                "key_event_rate": _rate(analytics.session_key_event_rate) if analytics else None,
                "engagement_rate": _rate(analytics.engagement_rate) if analytics else None,
                "score": None,
                "components": None,
                "join_status": "joined" if analytics else "gsc_only",
            }
        )
    for row in unparseable_gsc:
        if position_min <= row.position <= position_max:
            candidates.append(
                {
                    "_key": None,
                    "_ga4": None,
                    "page": row.page,
                    "position": round(float(row.position), 2),
                    "impressions": int(row.impressions),
                    "clicks": int(row.clicks),
                    "sessions": None,
                    "key_event_rate": None,
                    "engagement_rate": None,
                    "score": None,
                    "components": None,
                    "join_status": "gsc_only",
                    "note": "This page address could not be parsed, so it was not joined.",
                }
            )

    joined = [c for c in candidates if c["_ga4"] is not None]
    engagement_fallback = bool(joined) and all(
        (c["_ga4"].key_events or 0) == 0 for c in joined
    )
    ga4_metric_name = "engagementRate" if engagement_fallback else "sessionKeyEventRate"

    def ga4_value(c: dict[str, Any]) -> float | None:
        ga4 = c["_ga4"]
        return ga4.engagement_rate if engagement_fallback else ga4.session_key_event_rate

    demand = percentile_ranks([math.log1p(c["impressions"]) for c in joined])
    reach = percentile_ranks([20.0 - c["position"] for c in joined])

    # Business value: one percentile rank per value basis, each within its own group.
    # A page whose value metric is unknown (None) joins NO group: it stays
    # visible, unscored, and says why — never ranked as if it were 0.
    value_component: list[float | None] = [None] * len(joined)
    worth = offering_worth or {}
    use_worth = value_source == "offering_worth"
    worth_group: list[tuple[int, float]] = []
    ga4_group: list[tuple[int, float]] = []
    for i, c in enumerate(joined):
        worth_value = worth.get(c["_key"]) if use_worth else None
        if worth_value is not None:
            worth_group.append((i, float(worth_value)))
            continue
        metric = ga4_value(c)
        if metric is not None:
            ga4_group.append((i, float(metric)))
    for group in (worth_group, ga4_group):
        ranks = percentile_ranks([value for _, value in group])
        for (i, _), rank in zip(group, ranks, strict=True):
            value_component[i] = rank
    worth_idx = [i for i, _ in worth_group]
    worth_set = set(worth_idx)

    for i, c in enumerate(joined):
        v = value_component[i]
        if use_worth:
            c["value_basis"] = "offering_worth" if i in worth_set else ga4_metric_name
            if i not in worth_set:
                c["note"] = (
                    "No offering is mapped to this page's keywords, so its business value "
                    f"uses GA4 {ga4_metric_name} instead."
                )
        if v is None:
            c["note"] = "GA4 returned no value metric for this page, so it is not scored."
            continue
        components = {
            "demand": round(demand[i], 4),
            "value": round(v, 4),
            "reach": round(reach[i], 4),
        }
        c["components"] = components
        c["score"] = round(
            100
            * (
                weights.demand * components["demand"]
                + weights.value * components["value"]
                + weights.reach * components["reach"]
            )
        )

    candidates.sort(
        key=lambda c: (
            c["score"] is None,
            -(c["score"] or 0),
            -c["impressions"],
        )
    )
    returned = candidates[:limit]
    rows = [{k: v for k, v in c.items() if not k.startswith("_")} for c in returned]

    matched = len(joined)
    joined_keys = {c["_key"] for c in joined}
    value_metric = (
        f"offering worth_points (pages without a mapped offering: {ga4_metric_name})"
        if use_worth
        else ga4_metric_name
    )
    formula = (
        f"round(100 * ({weights.demand} * demand + {weights.value} * value + "
        f"{weights.reach} * reach)); each part is a percentile rank among joined pages: "
        f"demand = log1p(impressions), value = {value_metric}, reach = 20 - position"
    )
    notices: list[str] = []
    if engagement_fallback:
        notices.append(
            "No joined page recorded a GA4 key event in this window, so business value "
            "uses engagementRate instead of sessionKeyEventRate (engagement_fallback)."
        )
    if use_worth and not worth_idx:
        notices.append(
            "Business value was asked to use offering worth, but no candidate page's keywords "
            "map to a valued offering yet; every row fell back to the GA4 metric."
        )
    if not ga4_read:
        return OpportunityResult(
            rows=rows,
            formula=(
                f"round(100 * ({weights.demand} * demand + {weights.value} * value + "
                f"{weights.reach} * reach)); not computed: GA4 was not read, so no page "
                "has a value and none is scored"
            ),
            value_metric=None,
            engagement_fallback=None,
            coverage={
                "gsc_rows_considered": len(gsc_list),
                "ga4_rows_considered": None,
                "candidates": len(candidates),
                "matched": None,
                "unmatched_gsc": None,
                "unmatched_ga4": None,
                "unparseable_gsc": len(unparseable_gsc),
                "unparseable_ga4": None,
                "value_from_offering_worth": None,
            },
            truncated={
                "gsc": gsc_truncated,
                "ga4": None,
                "candidates": len(returned) < len(candidates),
            },
            notices=[
                "GA4 was not read, so every GA4 figure here is unknown (null), not zero, "
                "and no page is scored."
            ],
        )
    return OpportunityResult(
        rows=rows,
        formula=formula,
        value_metric=value_metric,
        engagement_fallback=engagement_fallback,
        coverage={
            "gsc_rows_considered": len(gsc_list),
            "ga4_rows_considered": len(ga4_list),
            "candidates": len(candidates),
            "matched": matched,
            "unmatched_gsc": len(candidates) - matched,
            "unmatched_ga4": max(len(ga4_by_key) - len(joined_keys), 0) + unparseable_ga4,
            "unparseable_gsc": len(unparseable_gsc),
            "unparseable_ga4": unparseable_ga4,
            "value_from_offering_worth": len(worth_idx),
        },
        truncated={
            "gsc": gsc_truncated,
            "ga4": ga4_truncated,
            "candidates": len(returned) < len(candidates),
        },
        notices=notices,
    )


def _num(value: float | None) -> float | None:
    if value is None:
        return None
    return int(value) if float(value).is_integer() else round(float(value), 4)


def _rate(value: float | None) -> float | None:
    return None if value is None else round(float(value), 4)


__all__ = [
    "SCORE_DISCLAIMER",
    "Ga4LandingRow",
    "GscPageRow",
    "OpportunityResult",
    "ValueSource",
    "Weights",
    "normalize_page_key",
    "percentile_ranks",
    "score_search_opportunities",
]
