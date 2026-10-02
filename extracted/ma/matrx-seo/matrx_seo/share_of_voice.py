"""AI share of voice from DataForSEO LLM-mentions cross-aggregated metrics — pure math.

Contract: ``common-docs/projects/outside-skill-packs/OPENSEO-TOOLS-SPEC.md`` §5.6
(census §3.3). Method learned from OpenSEO at ``every-app/open-seo@0ffff93``
(``src/server/features/ai-search/services/shareOfVoice.ts``) and made ours.

The one law this file exists for: **no data is not zero.** A brand the provider
returned nothing for is ``mentions=None`` ("we don't know"), never ``0``; it
stays on the leaderboard (the person asked to compare it), sorts last, and is
never counted in the denominator. A brand with a KNOWN ``0`` counts.

Rules, each unit-tested:

* competitor inputs are de-duplicated case-insensitively, and a competitor that
  collides with the target is dropped (it would buy a redundant paid group);
* every REQUESTED key is seeded to ``None`` before any provider row is read;
* provider rows for keys nobody asked for are ignored;
* per-brand mentions are the null-aware sum across successful platforms
  (``None + None = None``, ``None + n = n``);
* denominator = sum of the non-null mentions; ``share_pct`` is ``None`` when the
  brand's mentions are ``None`` or the denominator is ``<= 0``;
* ``None`` sorts after every number;
* the whole section is ``None`` (with a reason) when there are no competitors or
  every platform failed;
* a failed platform contributes nothing and is reported with ``mentions=None``.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Literal

TargetType = Literal["domain", "keyword"]

_WS = re.compile(r"\s")


@dataclass(frozen=True)
class DetectedTarget:
    """A free-text brand input resolved to a provider target entity."""

    type: TargetType
    value: str

    def provider_entity(self, *, include_subdomains: bool = True) -> dict[str, Any]:
        """The one ``target[]`` entity DataForSEO's LLM-mentions endpoints take."""
        if self.type == "domain":
            return {
                "domain": self.value,
                "include_subdomains": include_subdomains,
                "search_filter": "include",
                "search_scope": ["any"],
            }
        return {
            "keyword": self.value,
            "search_filter": "include",
            "search_scope": ["any"],
        }


def normalize_domain(raw: str) -> str:
    """``https://www.Example.com/path`` → ``example.com`` (empty when not a host)."""
    value = raw.strip().lower()
    value = re.sub(r"^[a-z][a-z0-9+.-]*://", "", value)
    value = value.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]
    value = value.split("@")[-1].split(":", 1)[0].strip(".")
    value = value.removeprefix("www.")
    if not value or "." not in value:
        return ""
    if not re.fullmatch(r"[a-z0-9.-]+", value):
        return ""
    return value


def detect_target(raw: str) -> DetectedTarget:
    """A domain when the input has no whitespace, contains a dot and normalizes
    to a host; otherwise a brand keyword (kept as typed, trimmed)."""
    trimmed = raw.strip()
    if trimmed and not _WS.search(trimmed) and "." in trimmed:
        host = normalize_domain(trimmed)
        if host:
            return DetectedTarget("domain", host)
    return DetectedTarget("keyword", trimmed)


@dataclass(frozen=True)
class CompetitorGroup:
    label: str
    detected: DetectedTarget


def resolve_competitor_groups(
    target_value: str, competitors: Iterable[str]
) -> list[CompetitorGroup]:
    """Detect each competitor's target type, drop blanks, dedupe by the resolved
    value case-insensitively, and drop any that collide with the target."""
    seen = {target_value.strip().lower()}
    groups: list[CompetitorGroup] = []
    for raw in competitors:
        if not isinstance(raw, str) or not raw.strip():
            continue
        detected = detect_target(raw)
        key = detected.value.lower()
        if key in seen:
            continue
        seen.add(key)
        groups.append(CompetitorGroup(label=detected.value, detected=detected))
    return groups


def sum_nullable(values: Iterable[float | int | None]) -> float | int | None:
    """Sum of the known values; ``None`` when none is known."""
    total: float | int = 0
    known = False
    for value in values:
        if value is None:
            continue
        total += value
        known = True
    return total if known else None


def round_or_none(value: Any) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return None


@dataclass(frozen=True)
class PlatformOutcome:
    """One platform's cross-aggregated call: ``ok`` with its provider items, or
    ``failed`` with the reason (a failed platform contributes nothing)."""

    platform: str
    status: Literal["ok", "failed"]
    items: Sequence[Mapping[str, Any]] = ()
    error: str | None = None


@dataclass
class ShareOfVoiceEntry:
    name: str
    is_target: bool
    mentions: int | None
    share_pct: float | None

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "is_target": self.is_target,
            "mentions": self.mentions,
            "share_pct": self.share_pct,
        }


@dataclass
class ShareOfVoice:
    entries: list[ShareOfVoiceEntry]
    platforms: list[dict[str, Any]]
    notices: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "entries": [e.as_dict() for e in self.entries],
            "platforms": self.platforms,
        }


def _platform_mentions(item: Mapping[str, Any], platform: str) -> int | None:
    rows = item.get("platform")
    if not isinstance(rows, list):
        return None
    values = [
        round_or_none(row.get("mentions"))
        for row in rows
        if isinstance(row, Mapping) and (row.get("key") in (None, platform))
    ]
    return sum_nullable(values)  # type: ignore[return-value]


def compute_share_of_voice(
    outcomes: Sequence[PlatformOutcome],
    target_key: str,
    competitor_keys: Sequence[str],
) -> tuple[ShareOfVoice | None, str | None]:
    """The leaderboard, or ``(None, reason)`` when there is nothing to compare.

    ``target_key`` and ``competitor_keys`` are the aggregation keys that were
    SENT (already de-duplicated by :func:`resolve_competitor_groups`)."""
    platform_rows = [
        {"platform": o.platform, "status": o.status, **({"error": o.error} if o.error else {})}
        for o in outcomes
    ]
    if not competitor_keys:
        return (
            None,
            "There are no competitors to compare against, so share of voice is not computed.",
        )
    successful = [o for o in outcomes if o.status == "ok"]
    if not successful:
        return None, "Every platform call failed, so share of voice is unknown (not zero)."

    requested = [target_key, *competitor_keys]
    label_by_key = {key.lower(): key for key in reversed(requested)}
    mentions_by_key: dict[str, int | None] = {key.lower(): None for key in requested}

    for outcome in successful:
        for item in outcome.items:
            if not isinstance(item, Mapping):
                continue
            raw_key = item.get("key")
            if not isinstance(raw_key, str):
                continue
            key = raw_key.lower()
            if key not in mentions_by_key:
                continue  # never let an unrequested row move requested shares
            platform_mentions = _platform_mentions(item, outcome.platform)
            mentions_by_key[key] = sum_nullable([mentions_by_key[key], platform_mentions])  # type: ignore[assignment]

    denominator = sum_nullable(mentions_by_key.values()) or 0
    target_lower = target_key.lower()
    entries = [
        ShareOfVoiceEntry(
            name=label_by_key[key],
            is_target=key == target_lower,
            mentions=mentions,
            share_pct=(
                None
                if mentions is None or denominator <= 0
                else round(mentions / denominator * 100, 2)
            ),
        )
        for key, mentions in mentions_by_key.items()
    ]
    # Known numbers first, largest first; unknown last (stable within ties).
    entries.sort(key=lambda e: (e.mentions is None, -(e.mentions or 0)))
    return ShareOfVoice(entries=entries, platforms=platform_rows), None


__all__ = [
    "CompetitorGroup",
    "DetectedTarget",
    "PlatformOutcome",
    "ShareOfVoice",
    "ShareOfVoiceEntry",
    "compute_share_of_voice",
    "detect_target",
    "normalize_domain",
    "resolve_competitor_groups",
    "round_or_none",
    "sum_nullable",
]
