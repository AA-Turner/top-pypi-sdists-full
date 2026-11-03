"""Collect and persist per-job metadata (crawl kwargs, settings snapshot, stats)."""

from __future__ import annotations

from typing import Any

from ..utils.serialization import json_safe

_SETTINGS_PREFIXES = ("INGEST_", "JOB_", "DB_", "SEARCH_", "ITEMS_", "REQUESTS_", "LOGS_", "JOBS_", "SPIDERS_")
_SPIDER_ATTR_KEYS = ("url", "start_url", "urls")
_SKIP = frozenset({"name", "crawler", "settings", "logger", "start_urls", "allowed_domains", "custom_settings"})
_EMPTY_ARGS = frozenset({"", "[]", "{}", "null"})


def _json_val(value: object) -> Any:
    try:
        return json_safe(value)
    except (TypeError, ValueError):
        return str(value)


def _real(value: object) -> bool:
    return value is not None and getattr(type(value), "__module__", "") != "unittest.mock"


def spider_args_empty(raw) -> bool:
    return raw is None or (isinstance(raw, str) and raw.strip() in _EMPTY_ARGS)


def _crawl_kwargs(spider) -> dict[str, Any]:
    crawler = getattr(spider, "crawler", None)
    raw = getattr(crawler, "_ingest_spider_kwargs", None) if crawler else None
    if not isinstance(raw, dict):
        return {}
    return {
        str(k): _json_val(v)
        for k, v in raw.items()
        if k != "name" and not str(k).startswith("_")
    }


def collect_spider_args(spider) -> dict[str, Any]:
    """``process.crawl(Spider, **kwargs)`` as JSON-serializable ``{key: value}``."""
    kw = _crawl_kwargs(spider)
    if kw:
        return kw

    out: dict[str, Any] = {}
    for key in _SPIDER_ATTR_KEYS:
        val = getattr(spider, key, None)
        if _real(val):
            out[key] = _json_val(val)

    start = getattr(spider, "start_urls", None) or []
    if isinstance(start, str):
        start = [start]
    urls = [str(_json_val(u)) for u in start if u]
    if urls:
        out["start_urls"] = urls
    if out:
        return out

    for key, val in getattr(spider, "__dict__", {}).items():
        if key.startswith("_") or key in _SKIP or not _real(val):
            continue
        if key.endswith("_url") or key == "url" or (
            isinstance(val, str) and val.strip().startswith(("http://", "https://"))
        ):
            out[key] = _json_val(val)
    return out


def collect_crawl_settings(spider) -> dict | None:
    crawler = getattr(spider, "crawler", None)
    if not crawler:
        return None
    snap = {
        str(k): _json_val(crawler.settings.get(k))
        for k in sorted(crawler.settings.keys())
        if str(k).startswith(_SETTINGS_PREFIXES)
    }
    return snap or None
