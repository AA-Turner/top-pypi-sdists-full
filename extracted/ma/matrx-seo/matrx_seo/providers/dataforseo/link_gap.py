"""DataForSEO backlink intersection → the competitor link gap.

*"When we're doing things to try to get backlinks, it's not so much who's
linking to us — it's about analyzing who's linking to our competitors."*
— Arman, 2026-08-14

``/v3/backlinks/domain_intersection/live`` answers exactly that, and its
``exclude_targets`` field is documented by the provider as enabling link gap
analysis: put the competitors in ``targets`` and our own domain in
``exclude_targets``, and what comes back is domains that link to them and not
to us. The gap is computed provider-side; we do not diff anything.

**The payload shape is counter-intuitive and was verified against a real live
call (2026-08-14, $0.024) rather than the docs.** Read this before editing:

* ``result.targets`` echoes the SUBMITTED numbered map — ``{"1": "shredit.com",
  "2": "shrednations.com"}``. The numbered KEY identifies the COMPETITOR.
* Each item's ``domain_intersection`` uses those same numbered keys, and the
  ``target`` field INSIDE each one is the **referring** domain — the thing doing
  the linking. It repeats identically under every key. Reading ``target`` as the
  competitor (the natural assumption, and what the field name suggests) silently
  inverts the entire feature: every gap domain would be recorded as a link to
  itself.
* ``item.summary.intersections_count`` is how many competitors it links to.

This module is a pure normalizer: dict in, contracts out. No DB, no network.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from ...contracts import LinkGapDomainItem, LinkGapMatchItem, LinkGapObservation

DOMAIN_INTERSECTION = "/v3/backlinks/domain_intersection/live"
PAGE_INTERSECTION = "/v3/backlinks/page_intersection/live"

SUPPORTED_INTERSECTION_ENDPOINTS = frozenset({DOMAIN_INTERSECTION, PAGE_INTERSECTION})

#: Fields lifted onto the typed match columns; everything else is kept in
#: ``extras`` so the provider's platform/country/TLD breakdowns are not lost.
_MATCH_MODELLED = frozenset(
    {
        "type",
        "target",
        "rank",
        "backlinks",
        "backlinks_spam_score",
        "first_seen",
        "lost_date",
        "referring_pages",
        "domain_from",
        "url_from",
        "url_to",
        "domain_from_rank",
        "backlink_spam_score",
        "dofollow",
        "links_count",
        "last_seen",
    }
)


def supports_intersection_endpoint(endpoint: str | None) -> bool:
    return endpoint is not None and endpoint.rstrip("/") in SUPPORTED_INTERSECTION_ENDPOINTS


def normalize_link_gap_payload(
    *,
    endpoint: str,
    raw: dict[str, Any],
    site_id: str,
    excluded_targets: list[str] | None = None,
    fetched_at: datetime,
) -> list[LinkGapObservation]:
    """Turn one intersection response into link-gap observations.

    One observation per provider ``result`` (normally one). Raises on a payload
    that does not have the documented envelope — a silently-empty gap list would
    read as "you have no opportunities", which is a far worse outcome than a
    loud parse failure.
    """
    normalized_endpoint = endpoint.rstrip("/")
    if normalized_endpoint not in SUPPORTED_INTERSECTION_ENDPOINTS:
        raise ValueError(f"unsupported DataForSEO intersection endpoint: {endpoint}")
    if not site_id.strip():
        raise ValueError("site_id must be nonblank")

    tasks = raw.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("DataForSEO intersection payload tasks must be a non-empty list")

    observations: list[LinkGapObservation] = []
    envelope_extras = {key: value for key, value in raw.items() if key != "tasks"}

    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("DataForSEO intersection tasks must contain objects")
        results = task.get("result")
        if not isinstance(results, list):
            raise ValueError("DataForSEO intersection task.result must be a list")
        for result in results:
            if not isinstance(result, dict):
                raise ValueError("DataForSEO intersection task.result must contain objects")
            observations.append(
                _observation(
                    result=result,
                    site_id=site_id,
                    excluded_targets=excluded_targets or [],
                    fetched_at=fetched_at,
                    extras={
                        "provider_envelope": envelope_extras,
                        "provider_task": {
                            key: value for key, value in task.items() if key != "result"
                        },
                        "endpoint": normalized_endpoint,
                    },
                )
            )
    return observations


def _observation(
    *,
    result: dict[str, Any],
    site_id: str,
    excluded_targets: list[str],
    fetched_at: datetime,
    extras: dict[str, Any],
) -> LinkGapObservation:
    # The submitted numbered map — the ONLY thing that says which competitor a
    # numbered key refers to.
    targets = result.get("targets")
    competitor_targets: dict[str, str] = {}
    if isinstance(targets, dict):
        competitor_targets = {
            str(key): str(value).strip()
            for key, value in targets.items()
            if isinstance(value, str) and value.strip()
        }

    items = result.get("items")
    if items is None and not result.get("items_count") and not result.get("total_count"):
        items = []
    if not isinstance(items, list):
        raise ValueError("DataForSEO intersection result.items must be a list")

    domains = [_domain_item(item, competitor_targets) for item in items if isinstance(item, dict)]
    if len(domains) != len(items):
        raise ValueError("DataForSEO intersection result.items must contain objects")

    return LinkGapObservation(
        site_id=site_id,
        competitor_targets=competitor_targets,
        excluded_targets=[t for t in excluded_targets if t and t.strip()],
        total_available=_optional_int(result.get("total_count")),
        observed_at=_as_utc(fetched_at),
        domains=domains,
        extras=extras,
    )


def _domain_item(item: dict[str, Any], competitor_targets: dict[str, str]) -> LinkGapDomainItem:
    intersection = item.get("domain_intersection") or item.get("page_intersection")
    if not isinstance(intersection, dict) or not intersection:
        raise ValueError("intersection item must carry a non-empty intersection object")

    matches: list[LinkGapMatchItem] = []
    referring: str | None = None
    best_rank: Decimal | None = None
    total_backlinks = 0
    saw_backlinks = False
    first_seen: datetime | None = None
    last_seen: datetime | None = None
    worst_spam: Decimal | None = None

    page_level = "page_intersection" in item
    for key, raw_entry in sorted(intersection.items()):
        entries = raw_entry if page_level else [raw_entry]
        if not isinstance(entries, list) or not entries:
            raise ValueError(
                "page intersection entries must be non-empty arrays"
                if page_level
                else "intersection entries must be objects"
            )
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError(
                    "page intersection entry arrays must contain objects"
                    if page_level
                    else "intersection entries must be objects"
                )
            match = _match_item(
                key=str(key),
                entry=entry,
                competitor_targets=competitor_targets,
                page_level=page_level,
            )
            entry_referrer = (
                _optional_string(entry.get("domain_from"))
                if page_level
                else _optional_string(entry.get("target"))
            )
            if entry_referrer and referring is None:
                referring = entry_referrer
            rank = match.domain_rank
            spam = match.spam_score
            backlinks = match.backlinks
            seen_at = match.first_seen_at
            latest_at = match.last_seen_at or seen_at
            if rank is not None and (best_rank is None or rank > best_rank):
                best_rank = rank
            if spam is not None and (worst_spam is None or spam > worst_spam):
                worst_spam = spam
            if backlinks is not None:
                total_backlinks += backlinks
                saw_backlinks = True
            if seen_at is not None and (first_seen is None or seen_at < first_seen):
                first_seen = seen_at
            if latest_at is not None and (last_seen is None or latest_at > last_seen):
                last_seen = latest_at
            matches.append(match)

    if not referring:
        raise ValueError("intersection item carries no referring domain")

    summary = item.get("summary")
    match_count = None
    if isinstance(summary, dict):
        match_count = _optional_int(summary.get("intersections_count"))
    if match_count is None:
        match_count = len({match.competitor_domain for match in matches})

    normalized = _normalize_domain(referring)
    return LinkGapDomainItem(
        normalized_domain=normalized,
        display_domain=referring,
        match_count=match_count,
        domain_rank=best_rank,
        spam_score=worst_spam,
        total_backlinks=total_backlinks if saw_backlinks else None,
        first_seen_at=first_seen,
        last_seen_at=last_seen,
        matches=matches,
        extras={
            key: value
            for key, value in item.items()
            if key not in {"domain_intersection", "page_intersection", "summary"}
        },
    )


def _match_item(
    *,
    key: str,
    entry: dict[str, Any],
    competitor_targets: dict[str, str],
    page_level: bool,
) -> LinkGapMatchItem:
    # Domain intersection's `target` is the referrer; page intersection's
    # numbered value is an array of complete backlinks. In both cases the
    # submitted numbered map is the only competitor identity.
    competitor = competitor_targets.get(key)
    if not competitor:
        # A numbered key with no submitted target means the request map and the
        # response disagree. Recording against an unknown competitor is a lie.
        raise ValueError(
            f"intersection key {key!r} has no matching submitted target "
            f"(submitted: {sorted(competitor_targets)})"
        )
    return LinkGapMatchItem(
        competitor_domain=_normalize_domain(competitor),
        source_url=_optional_string(entry.get("url_from")) if page_level else None,
        target_url=_optional_string(entry.get("url_to")) if page_level else None,
        backlinks=_optional_int(entry.get("links_count") if page_level else entry.get("backlinks")),
        referring_pages=(None if page_level else _optional_int(entry.get("referring_pages"))),
        domain_rank=_optional_decimal(
            entry.get("domain_from_rank") if page_level else entry.get("rank")
        ),
        spam_score=_optional_decimal(
            entry.get("backlink_spam_score") if page_level else entry.get("backlinks_spam_score")
        ),
        is_dofollow=entry.get("dofollow") if page_level else None,
        first_seen_at=_optional_datetime(entry.get("first_seen")),
        last_seen_at=(_optional_datetime(entry.get("last_seen")) if page_level else None),
        lost_at=_optional_datetime(entry.get("lost_date")),
        extras={key_: value for key_, value in entry.items() if key_ not in _MATCH_MODELLED},
    )


def _normalize_domain(value: str) -> str:
    normalized = value.strip().lower()
    if "://" in normalized:
        normalized = normalized.split("://", 1)[1]
    normalized = normalized.split("/", 1)[0]
    if normalized.startswith("www."):
        normalized = normalized[4:]
    normalized = normalized.rstrip(".")
    if not normalized:
        raise ValueError(f"link gap domain {value!r} normalizes to nothing")
    return normalized


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"expected string, received {type(value).__name__}")
    return value.strip() or None


def _optional_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("boolean is not a valid intersection integer")
    return int(value)


def _optional_decimal(value: Any) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("boolean is not a valid intersection decimal")
    return Decimal(str(value))


def _optional_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return _as_utc(value)
    if not isinstance(value, str):
        raise ValueError("intersection datetime must be a string")
    text = value.strip()
    if not text:
        return None
    # DataForSEO emits "2025-09-09 01:21:09 +00:00".
    candidate = text.replace("Z", "+00:00")
    if " " in candidate and "T" not in candidate:
        head, _, tail = candidate.partition(" ")
        rest = tail.strip()
        if rest and (rest[0].isdigit()):
            time_part, _, offset = rest.partition(" ")
            candidate = f"{head}T{time_part}{offset.replace(' ', '')}"
        else:
            candidate = f"{head}T{rest}"
    try:
        return _as_utc(datetime.fromisoformat(candidate))
    except ValueError as exc:
        raise ValueError(f"intersection datetime {value!r} is not parseable") from exc


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
