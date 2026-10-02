from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Literal

from ...contracts import (
    BacklinkDimensionItem,
    BacklinkItem,
    BacklinkSnapshotObservation,
)

_SUMMARY = "/v3/backlinks/summary/live"
_BACKLINKS = "/v3/backlinks/backlinks/live"
_REFERRING_DOMAINS = "/v3/backlinks/referring_domains/live"
_ANCHORS = "/v3/backlinks/anchors/live"
_HISTORY = "/v3/backlinks/history/live"
_DOMAIN_PAGES = "/v3/backlinks/domain_pages/live"
_DOMAIN_PAGES_SUMMARY = "/v3/backlinks/domain_pages_summary/live"
_TIMESERIES_SUMMARY = "/v3/backlinks/timeseries_summary/live"
_TIMESERIES_NEW_LOST = "/v3/backlinks/timeseries_new_lost_summary/live"
_COMPETITORS = "/v3/backlinks/competitors/live"

SUPPORTED_BACKLINK_ENDPOINTS = frozenset(
    {
        _SUMMARY,
        _BACKLINKS,
        _REFERRING_DOMAINS,
        _ANCHORS,
        _HISTORY,
        _DOMAIN_PAGES,
        _DOMAIN_PAGES_SUMMARY,
        _TIMESERIES_SUMMARY,
        _TIMESERIES_NEW_LOST,
        _COMPETITORS,
    }
)


def supports_backlink_endpoint(endpoint: str | None) -> bool:
    return endpoint is not None and endpoint.rstrip("/") in SUPPORTED_BACKLINK_ENDPOINTS


_SNAPSHOT_METRIC_KEYS = {
    "backlinks",
    "backlinks_dofollow",
    "backlinks_nofollow",
    "backlinks_spam_score",
    "broken_backlinks",
    "date",
    "lost_backlinks",
    "new_backlinks",
    "rank",
    "referring_domains",
    "referring_ips",
    "referring_subnets",
    "target",
}


def normalize_backlink_payload(
    *,
    endpoint: str,
    raw: dict[str, Any],
    site_id: str,
    page_id: str | None,
    target: str,
    fetched_at: datetime,
) -> list[BacklinkSnapshotObservation]:
    normalized_endpoint = endpoint.rstrip("/")
    if normalized_endpoint not in SUPPORTED_BACKLINK_ENDPOINTS:
        raise ValueError(f"unsupported DataForSEO backlinks endpoint: {endpoint}")
    if not site_id.strip():
        raise ValueError("site_id must be nonblank")
    if not target.strip():
        raise ValueError("target must be nonblank")

    observations: list[BacklinkSnapshotObservation] = []
    for result, context_extras in _results(raw):
        result_target = _optional_string(result.get("target")) or target.strip()
        result_extras = _without(result, {"items", *_SNAPSHOT_METRIC_KEYS})
        base_extras = {**context_extras, "provider_result": result_extras}

        if normalized_endpoint == _SUMMARY:
            observations.append(
                _snapshot(
                    dataset="summary",
                    metrics=result,
                    site_id=site_id,
                    page_id=page_id,
                    target=result_target,
                    observed_at=fetched_at,
                    extras=base_extras,
                )
            )
            continue

        items = result.get("items")
        if items is None and result.get("items_count") == 0 and result.get("total_count") == 0:
            items = []
        if not isinstance(items, list):
            raise ValueError(f"{normalized_endpoint} result.items must be a list")
        if any(not isinstance(item, dict) for item in items):
            raise ValueError(f"{normalized_endpoint} result.items must contain objects")

        if normalized_endpoint in {_HISTORY, _TIMESERIES_SUMMARY, _TIMESERIES_NEW_LOST}:
            for item in items:
                observations.append(
                    _snapshot(
                        dataset=normalized_endpoint.rsplit("/", 2)[-2],
                        metrics=item,
                        site_id=site_id,
                        page_id=page_id,
                        target=result_target,
                        observed_at=_required_datetime(item.get("date"), "item.date"),
                        extras={
                            **base_extras,
                            "provider_item": _without(item, _SNAPSHOT_METRIC_KEYS),
                        },
                    )
                )
            continue

        observations.append(
            _collection_snapshot(
                endpoint=normalized_endpoint,
                result=result,
                items=items,
                site_id=site_id,
                page_id=page_id,
                target=result_target,
                fetched_at=fetched_at,
                extras=base_extras,
            )
        )
    return observations


def _results(raw: dict[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    tasks = raw.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("DataForSEO backlink payload tasks must be a non-empty list")
    envelope_extras = _without(raw, {"tasks"})
    results: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("DataForSEO backlink payload tasks must contain objects")
        task_results = task.get("result")
        if not isinstance(task_results, list):
            raise ValueError("DataForSEO backlink task.result must be a list")
        if any(not isinstance(result, dict) for result in task_results):
            raise ValueError("DataForSEO backlink task.result must contain objects")
        context = {
            "provider_envelope": envelope_extras,
            "provider_task": _without(task, {"result"}),
        }
        results.extend((result, context) for result in task_results)
    return results


def _collection_snapshot(
    *,
    endpoint: str,
    result: dict[str, Any],
    items: list[dict[str, Any]],
    site_id: str,
    page_id: str | None,
    target: str,
    fetched_at: datetime,
    extras: dict[str, Any],
) -> BacklinkSnapshotObservation:
    backlinks: list[BacklinkItem] = []
    dimensions: list[BacklinkDimensionItem] = []
    metrics: dict[str, Any] = {}
    dataset = endpoint.rsplit("/", 2)[-2]

    if endpoint == _BACKLINKS:
        backlinks = [_backlink_item(item) for item in items]
        metrics["backlinks"] = result.get("total_count")
    elif endpoint == _REFERRING_DOMAINS:
        dimensions = [_dimension(item, "referring_domain", "domain") for item in items]
    elif endpoint == _ANCHORS:
        dimensions = [_dimension(item, "anchor", "anchor") for item in items]
    elif endpoint == _DOMAIN_PAGES:
        dimensions = [_target_page_dimension(item, nested_summary=True) for item in items]
    elif endpoint == _DOMAIN_PAGES_SUMMARY:
        dimensions = [_target_page_dimension(item, nested_summary=False) for item in items]
    elif endpoint == _COMPETITORS:
        dimensions = [_dimension(item, "competitor_domain", "target") for item in items]
    else:
        raise ValueError(f"unsupported DataForSEO backlinks collection endpoint: {endpoint}")

    return _snapshot(
        dataset=dataset,
        metrics=metrics,
        site_id=site_id,
        page_id=page_id,
        target=target,
        observed_at=fetched_at,
        backlinks=backlinks,
        dimensions=dimensions,
        extras=extras,
    )


def _snapshot(
    *,
    dataset: str,
    metrics: dict[str, Any],
    site_id: str,
    page_id: str | None,
    target: str,
    observed_at: datetime,
    backlinks: list[BacklinkItem] | None = None,
    dimensions: list[BacklinkDimensionItem] | None = None,
    extras: dict[str, Any],
) -> BacklinkSnapshotObservation:
    total = _optional_int(metrics.get("backlinks"))
    nofollow = _nofollow_backlink_count(metrics)
    dofollow = _optional_int(metrics.get("backlinks_dofollow"))
    if dofollow is None and total is not None and nofollow is not None:
        dofollow = max(total - nofollow, 0)
    return BacklinkSnapshotObservation(
        site_id=site_id,
        page_id=page_id,
        dataset=dataset,
        target=target,
        target_type="url" if "://" in target else "domain",
        total_backlinks=total,
        referring_domains=_optional_int(metrics.get("referring_domains")),
        referring_ips=_optional_int(metrics.get("referring_ips")),
        referring_subnets=_optional_int(metrics.get("referring_subnets")),
        dofollow_backlinks=dofollow,
        nofollow_backlinks=nofollow,
        new_backlinks=_optional_int(metrics.get("new_backlinks")),
        lost_backlinks=_optional_int(metrics.get("lost_backlinks")),
        broken_backlinks=_optional_int(metrics.get("broken_backlinks")),
        rank_score=_optional_decimal(metrics.get("rank")),
        spam_score=_optional_decimal(metrics.get("backlinks_spam_score")),
        observed_at=_as_utc(observed_at),
        backlinks=backlinks or [],
        dimensions=dimensions or [],
        extras=extras,
    )


def _backlink_item(item: dict[str, Any]) -> BacklinkItem:
    source_url = _required_string(item.get("url_from"), "item.url_from")
    target_url = _required_string(item.get("url_to"), "item.url_to")
    modeled = {
        "anchor",
        "backlink_spam_score",
        "dofollow",
        "domain_from",
        "domain_from_rank",
        "first_seen",
        "is_lost",
        "is_new",
        "item_type",
        "last_seen",
        "lost_date",
        "page_from_rank",
        "url_from",
        "url_to",
    }
    state: Literal["active", "new", "lost"] = "active"
    if item.get("is_lost") is True or item.get("lost_date") is not None:
        state = "lost"
    elif item.get("is_new") is True:
        state = "new"
    return BacklinkItem(
        source_url=source_url,
        source_domain=_optional_string(item.get("domain_from")),
        target_url=target_url,
        anchor_text=_optional_string(item.get("anchor")),
        link_type=_optional_string(item.get("item_type")),
        is_dofollow=_optional_bool(item.get("dofollow")),
        first_seen_at=_optional_datetime(item.get("first_seen"), "item.first_seen"),
        last_seen_at=_optional_datetime(item.get("last_seen"), "item.last_seen"),
        lost_at=_optional_datetime(item.get("lost_date"), "item.lost_date"),
        state=state,
        source_rank=_optional_decimal(item.get("page_from_rank")),
        domain_rank=_optional_decimal(item.get("domain_from_rank")),
        spam_score=_optional_decimal(item.get("backlink_spam_score")),
        extras=_without(item, modeled),
    )


def _dimension(
    item: dict[str, Any],
    kind: Literal["referring_domain", "anchor", "competitor_domain"],
    key_field: str,
) -> BacklinkDimensionItem:
    raw_key = item.get(key_field)
    if kind == "anchor" and raw_key in {None, ""}:
        key = "<empty-anchor>"
    else:
        key = _required_string(raw_key, f"item.{key_field}")
    modeled = {
        "backlinks",
        "backlinks_spam_score",
        "first_seen",
        "last_seen",
        "rank",
        "referring_domains",
        key_field,
    }
    return BacklinkDimensionItem(
        dimension_kind=kind,
        dimension_key=key,
        label=_optional_string(raw_key),
        backlinks=_optional_int(item.get("backlinks")),
        referring_domains=_optional_int(item.get("referring_domains")),
        rank_score=_optional_decimal(item.get("rank")),
        spam_score=_optional_decimal(item.get("backlinks_spam_score")),
        first_seen_at=_optional_datetime(item.get("first_seen"), "item.first_seen"),
        last_seen_at=_optional_datetime(item.get("last_seen"), "item.last_seen"),
        extras=_without(item, modeled),
    )


def _target_page_dimension(item: dict[str, Any], *, nested_summary: bool) -> BacklinkDimensionItem:
    key_field = "page" if nested_summary else "url"
    url = _required_string(item.get(key_field), f"item.{key_field}")
    summary = item.get("page_summary") if nested_summary else item
    if not isinstance(summary, dict):
        raise ValueError("domain_pages item.page_summary must be an object")
    title = None
    if nested_summary:
        meta = item.get("meta")
        if isinstance(meta, dict):
            title = _optional_string(meta.get("title"))
    modeled_summary = {
        "backlinks",
        "backlinks_spam_score",
        "first_seen",
        "last_seen",
        "rank",
        "referring_domains",
    }
    modeled_item = {key_field, "page_summary"} if nested_summary else modeled_summary | {key_field}
    extras = _without(item, modeled_item)
    if nested_summary:
        extras["page_summary"] = _without(summary, modeled_summary)
    return BacklinkDimensionItem(
        dimension_kind="target_page",
        dimension_key=url,
        label=title or url,
        url=url,
        backlinks=_optional_int(summary.get("backlinks")),
        referring_domains=_optional_int(summary.get("referring_domains")),
        rank_score=_optional_decimal(summary.get("rank")),
        spam_score=_optional_decimal(summary.get("backlinks_spam_score")),
        first_seen_at=_optional_datetime(summary.get("first_seen"), "item.first_seen"),
        last_seen_at=_optional_datetime(summary.get("last_seen"), "item.last_seen"),
        extras=extras,
    )


def _nofollow_backlink_count(metrics: dict[str, Any]) -> int | None:
    direct = _optional_int(metrics.get("backlinks_nofollow"))
    if direct is not None:
        return direct
    attrs = metrics.get("referring_links_attributes")
    if isinstance(attrs, dict):
        from_attrs = _optional_int(attrs.get("nofollow"))
        if from_attrs is not None:
            return from_attrs
    return _optional_int(metrics.get("referring_pages_nofollow"))


def _without(value: dict[str, Any], keys: set[str]) -> dict[str, Any]:
    return {key: item for key, item in value.items() if key not in keys}


def _required_string(value: Any, field: str) -> str:
    normalized = _optional_string(value)
    if normalized is None:
        raise ValueError(f"DataForSEO backlink {field} must be a nonblank string")
    return normalized


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"expected string, received {type(value).__name__}")
    normalized = value.strip()
    return normalized or None


def _optional_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("boolean is not a valid backlink integer")
    return int(value)


def _optional_decimal(value: Any) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("boolean is not a valid backlink decimal")
    return Decimal(str(value))


def _optional_bool(value: Any) -> bool | None:
    if value is None or isinstance(value, bool):
        return value
    raise ValueError(f"expected boolean, received {type(value).__name__}")


def _required_datetime(value: Any, field: str) -> datetime:
    parsed = _optional_datetime(value, field)
    if parsed is None:
        raise ValueError(f"DataForSEO backlink {field} is required")
    return parsed


def _optional_datetime(value: Any, field: str) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return _as_utc(value)
    if not isinstance(value, str):
        raise ValueError(f"DataForSEO backlink {field} must be a datetime string")
    try:
        return _as_utc(datetime.fromisoformat(value.replace("Z", "+00:00")))
    except ValueError as exc:
        raise ValueError(f"DataForSEO backlink {field} is not a valid datetime") from exc


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)
