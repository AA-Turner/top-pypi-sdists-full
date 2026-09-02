"""Durable memory of what a crawl learned about a host's crawl rate.

**Arman, 2026-08-20:** *"keep pushing up higher and higher and higher until we
figure out what the limit is and then back off from it."* Finding a host's limit
costs real requests — including, by definition, at least one the host refused.
Paying that cost again on every crawl of the same site would be its own kind of
rudeness, so what a run discovers is remembered and the next run opens near it
instead of probing from zero.

**Where it lives, and why not a new table.** ``web.site.metadata["host_pacing"]``
— the same row and the same mechanism ``site_probe.py`` already uses for site-
level evidence, for the same reasons it gave: one row per site, latest write
wins, and a stale entry is visible as a stale ``observed_at`` rather than as a
missing one. Deliberately NOT ``crawl_session.stats``, which every progress event
REPLACES wholesale; and deliberately not a new table, because a per-host learned
number is a fact about the site we already have a row for.

**What is remembered, and what is not.** Only a ceiling the host actually taught
us: a rate it refused (backed off to
:attr:`~matrx_scraper.host_pacing.PacingKnobs.ceiling_hold` of itself), or a rate
the ramp CLIMBED to and held cleanly. A crawl that opened at the floor and never
climbed learned nothing and writes nothing — recording "0.5 req/s" there would
teach the next run a number that came from the crawl being six pages long.
"""

from __future__ import annotations

import logging
from typing import Any

from matrx_utils import capture_error, utcnow

from matrx_scraper.db.models_web import Site as WebSite
from matrx_scraper.host_pacing import RememberedPacing

logger = logging.getLogger(__name__)

#: Where the memory lives on the site row, and the shape version. An entry
#: written by an older format is IGNORED rather than misread — the crawl then
#: probes as if it were the first, which is correct and merely slower.
PACING_METADATA_KEY = "host_pacing"
PACING_FORMAT_VERSION = 1

__all__ = [
    "PACING_METADATA_KEY",
    "PACING_FORMAT_VERSION",
    "load_remembered_pacing",
    "save_learned_pacing",
]


def _entry_to_remembered(host: str, entry: dict[str, Any]) -> RememberedPacing | None:
    ceiling = entry.get("ceiling_rps")
    try:
        ceiling_value = float(ceiling)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    if ceiling_value <= 0:
        return None
    return RememberedPacing(
        host=host,
        ceiling_rps=ceiling_value,
        source="remembered",
        platform=entry.get("platform"),
        observed_at=entry.get("observed_at"),
        limit_hits=int(entry.get("limit_hits") or 0),
    )


async def load_remembered_pacing(site_id: str, host: str) -> RememberedPacing | None:
    """What the last crawl learned about ``host``, or None if nothing yet.

    Fails OPEN and silent-to-the-crawl: a read error here means the crawl probes
    from scratch, which is the pre-memory behaviour and never a failure. It is
    logged, because a persistently failing read is a real defect that would
    otherwise show up only as crawls that never get faster.
    """

    if not site_id or not host:
        return None
    try:
        site = await WebSite.load_by_id_or_none(site_id)
    except Exception as exc:
        logger.exception("host-pacing memory read failed for site %s", site_id)
        await capture_error(
            exc,
            kind="crawl_pacing_memory_read_failed",
            context={"site_id": site_id},
        )
        return None
    if site is None:
        return None
    stored = (site.metadata or {}).get(PACING_METADATA_KEY) or {}
    if stored.get("version") != PACING_FORMAT_VERSION:
        return None
    entry = (stored.get("hosts") or {}).get(host)
    if not isinstance(entry, dict):
        return None
    return _entry_to_remembered(host, entry)


async def save_learned_pacing(site_id: str, learned: dict[str, RememberedPacing]) -> None:
    """Merge what this run discovered into the site's pacing memory.

    A MERGE, not a replace: a crawl that only visited the apex host must not
    erase what an earlier crawl learned about a subdomain. Within one host the
    newest observation wins outright — a host's capacity genuinely changes, and
    keeping the older, lower number would pin a site that has since been moved
    to better hosting at its old rate forever.
    """

    if not site_id or not learned:
        return
    try:
        site = await WebSite.load_by_id_or_none(site_id)
        if site is None:
            return
        metadata = dict(site.metadata or {})
        stored = metadata.get(PACING_METADATA_KEY)
        hosts: dict[str, Any] = {}
        if isinstance(stored, dict) and stored.get("version") == PACING_FORMAT_VERSION:
            hosts = dict(stored.get("hosts") or {})
        stamp = utcnow().isoformat()
        for host, memory in learned.items():
            hosts[host] = {
                "ceiling_rps": round(memory.ceiling_rps, 3),
                "platform": memory.platform,
                "limit_hits": memory.limit_hits,
                "observed_at": stamp,
            }
        metadata[PACING_METADATA_KEY] = {
            "version": PACING_FORMAT_VERSION,
            "updated_at": stamp,
            "hosts": hosts,
        }
        await WebSite.update_item(site_id, metadata=metadata)
    except Exception as exc:
        # Losing the memory costs the NEXT crawl a re-probe. It must never cost
        # THIS crawl its result, which is already fully persisted by now.
        logger.exception("host-pacing memory write failed for site %s", site_id)
        await capture_error(
            exc,
            kind="crawl_pacing_memory_write_failed",
            context={"site_id": site_id},
        )
