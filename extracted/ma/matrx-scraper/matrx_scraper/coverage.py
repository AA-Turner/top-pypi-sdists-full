"""The coverage map — for any URL, which readers beyond our own scraper could get it.

ONE platform primitive (owner-approved design, 2026-10-16, "default Off everywhere"): every page
read, the retry door, the agent hint and the UI's "Try advanced reader" button ask the same
``coverage_for(url)``. Our scraper ALWAYS reads first; coverage only says what else exists.

Three services, fastest first:

* ``social``     — the social reader (profile / post data) for social profile and post links.
* ``unlocker``   — the advanced reader: any http(s) page, fetched through a page unlocker.
* ``structured`` — structured data: the site's records from a catalog dataset (``scraper.data_source``
  url_pattern rows, via ``vendors.site_catalog``). Slow (20 s to many minutes), so never "fast".

Each ``Coverage`` carries a speed class (``fast`` | ``research`` | ``batch``), typical seconds, the
price in points per page/record and what it returns. Prices and measured speeds come from the HOST
(injected resolvers below): this package never holds a price, and words a person or agent reads never
name a vendor.

Host hooks (``configure_ext``), all optional — absent = that piece is unknown, said honestly:

* ``coverage_price``           ``async (service, source_key, organization_id) -> (usd, points) | None``
* ``coverage_speed``           ``async (service, source_key) -> float | None`` — measured median seconds
* ``social_platform_detector`` ``(url) -> str | None`` — the platform of a social link (host: matrx-social)
* ``advanced_fallback_mode``   ``async () -> "off" | "fast" | "all"`` — the org knob (host: feature knob)
* ``advanced_reader``          ``async (urls, allow) -> list[dict]`` — the retry door (host service)
* ``advanced_fallback_run_slot`` ``async () -> bool`` — takes one of this run's automatic-retry slots
  (host: ``knowledge.scraper.advanced_fallback_max_pages_per_run``); ``False`` = the run's ceiling is spent
"""

from __future__ import annotations

import statistics
from dataclasses import asdict, dataclass
from typing import Any, Literal
from urllib.parse import urlparse

from matrx_scraper._ext import get_ext, has_ext

Service = Literal["social", "unlocker", "structured"]
Speed = Literal["fast", "research", "batch"]
Mode = Literal["off", "fast", "all"]

SOCIAL: Service = "social"
UNLOCKER: Service = "unlocker"
STRUCTURED: Service = "structured"

EXT_PRICE = "coverage_price"
EXT_SPEED = "coverage_speed"
EXT_SOCIAL_DETECT = "social_platform_detector"
EXT_MODE = "advanced_fallback_mode"
EXT_READER = "advanced_reader"
EXT_RUN_SLOT = "advanced_fallback_run_slot"
#: The unlocker lives on the injected data client (``vendors.brightdata.BrightDataClient.unlock``).
EXT_CLIENT = "brightdata_client"

#: What a person or agent reads for each service — never a vendor.
LABELS: dict[str, str] = {SOCIAL: "social reader", UNLOCKER: "advanced reader", STRUCTURED: "structured data"}
RETURNS: dict[str, str] = {
    SOCIAL: "the profile or post: name, bio, audience numbers, recent posts and captions",
    UNLOCKER: "the full page text, read through a page unlocker",
    STRUCTURED: "the site's records as structured fields",
}
UNITS: dict[str, str] = {SOCIAL: "lookup", UNLOCKER: "page", STRUCTURED: "record"}

#: Platforms the social reader serves (matrx-social ``Platform`` values).
SOCIAL_PLATFORMS = frozenset({"instagram", "tiktok", "x", "threads", "youtube", "facebook", "linkedin",
                              "pinterest", "reddit"})

#: MEASURED, not settings (live runs 2026-10-16; the host's ``coverage_speed`` replaces them with its own
#: history): unlocker 2-16 s, median 7; social reader 6-15 s; structured datasets 20 s to 25 min.
MEASURED_TYPICAL_S: dict[str, float] = {UNLOCKER: 7.0, SOCIAL: 9.0, STRUCTURED: 180.0}
#: Speed class boundaries over typical seconds: a chat turn can wait for "fast", a research run for
#: "research"; anything slower is a "batch" job. The design's own words, not a tunable.
_FAST_MAX_S = 20.0
_RESEARCH_MAX_S = 120.0
_SPEED_RANK = {"fast": 0, "research": 1, "batch": 2}
_SERVICE_RANK = {SOCIAL: 0, UNLOCKER: 1, STRUCTURED: 2}


@dataclass(frozen=True)
class Coverage:
    """One service that could read a URL our scraper could not."""

    service: str
    label: str
    speed: str
    typical_seconds: float | None
    unit: str
    points_per_unit: int | None
    returns: str
    #: ``structured`` only: the catalog source key and its label.
    source_key: str | None = None
    source_label: str | None = None
    #: ``social`` only: the platform.
    platform: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def speed_class(seconds: float | None, service: str) -> str:
    if service == STRUCTURED and seconds is None:
        return "batch"
    if seconds is None:
        return "fast"
    if seconds <= _FAST_MAX_S and service != STRUCTURED:
        return "fast"
    if seconds <= _RESEARCH_MAX_S:
        return "research"
    return "batch"


def _is_web(url: str) -> bool:
    try:
        p = urlparse(url or "")
    except ValueError:
        return False
    return p.scheme in ("http", "https") and bool(p.hostname)


def social_platform(url: str) -> str | None:
    if not has_ext(EXT_SOCIAL_DETECT) or get_ext(EXT_SOCIAL_DETECT) is None:
        return None
    try:
        plat = get_ext(EXT_SOCIAL_DETECT)(url)
    except Exception:  # noqa: BLE001 - an unparseable link is simply not social
        return None
    value = getattr(plat, "value", plat)
    return value if value in SOCIAL_PLATFORMS else None


def unlocker_available() -> bool:
    client = get_ext(EXT_CLIENT) if has_ext(EXT_CLIENT) else None
    return client is not None and hasattr(client, "unlock")


async def _price(service: str, source_key: str | None, organization_id: str | None) -> int | None:
    if not has_ext(EXT_PRICE) or get_ext(EXT_PRICE) is None:
        return None
    try:
        got = await get_ext(EXT_PRICE)(service, source_key, organization_id)
    except Exception:  # noqa: BLE001 - a quote is display; unknown stays unknown (None), never a guessed 0
        return None
    return None if got is None else int(got[1])


async def _speed(service: str, source_key: str | None) -> float | None:
    if has_ext(EXT_SPEED) and get_ext(EXT_SPEED) is not None:
        try:
            got = await get_ext(EXT_SPEED)(service, source_key)
            if got is not None:
                return float(got)
        except Exception:  # noqa: BLE001 - measured history unreadable: the measured default holds
            pass
    return MEASURED_TYPICAL_S.get(service)


async def _make(service: str, organization_id: str | None, *, source_key: str | None = None,
                source_label: str | None = None, platform: str | None = None) -> Coverage:
    seconds = await _speed(service, source_key)
    returns = RETURNS[service]
    if service == STRUCTURED and source_label:
        returns = f"{source_label}: {returns}"
    return Coverage(service=service, label=LABELS[service], speed=speed_class(seconds, service),
                    typical_seconds=round(seconds, 1) if seconds is not None else None, unit=UNITS[service],
                    points_per_unit=await _price(service, source_key, organization_id), returns=returns,
                    source_key=source_key, source_label=source_label, platform=platform)


async def coverage_for(url: str, *, organization_id: str | None = None) -> list[Coverage]:
    """Every service beyond our scraper that could read ``url``, fastest first."""
    if not _is_web(url):
        return []
    out: list[Coverage] = []
    platform = social_platform(url)
    if platform:
        out.append(await _make(SOCIAL, organization_id, platform=platform))
    if unlocker_available():
        out.append(await _make(UNLOCKER, organization_id))
        from matrx_scraper.vendors.site_catalog import ensure_catalog, entries_for_url

        try:
            await ensure_catalog()
        except Exception:  # noqa: BLE001 - the host catalog is unreadable: the bundled seed answers
            pass
        for entry in entries_for_url(url):
            out.append(await _make(STRUCTURED, organization_id, source_key=entry.key, source_label=entry.label))
    out.sort(key=lambda c: (_SPEED_RANK.get(c.speed, 9), _SERVICE_RANK.get(c.service, 9),
                            c.typical_seconds if c.typical_seconds is not None else 1e9))
    return out


def allowed(cov: Coverage, allow: str) -> bool:
    """``fast`` = the fast services only; ``all`` = every service."""
    if allow == "all":
        return True
    return allow == "fast" and cov.speed == "fast"


async def fallback_mode() -> Mode:
    """The organization's ``knowledge.scraper.advanced_fallback`` (host-injected). No host = ``off``
    (nothing paid ever runs on a host that did not decide)."""
    if not has_ext(EXT_MODE) or get_ext(EXT_MODE) is None:
        return "off"
    try:
        mode = str(await get_ext(EXT_MODE)()).strip().lower()
    except Exception:  # noqa: BLE001 - unreadable knob: the safe answer is the default, off
        return "off"
    return mode if mode in ("off", "fast", "all") else "off"  # type: ignore[return-value]


async def take_run_slot() -> bool:
    """Take one automatic-retry slot for the current run. No host hook = unlimited (the knob is the host's);
    a hook that fails is a defect that must not buy pages, so it answers ``False``."""
    if not has_ext(EXT_RUN_SLOT) or get_ext(EXT_RUN_SLOT) is None:
        return True
    try:
        return bool(await get_ext(EXT_RUN_SLOT)())
    except Exception:  # noqa: BLE001 - unreadable ceiling: spend nothing, the failed read stands
        return False


def hint_line(failed: list[tuple[str, list[Coverage] | list[dict[str, Any]]]], *, tool: str = "advanced_read") -> str | None:
    """ONE short line for an agent when some pages failed and are covered, else ``None``.

    ``failed`` = ``[(url, coverage)]`` for the pages that failed in this read."""
    covered = [(u, [c if isinstance(c, dict) else c.to_dict() for c in cov]) for u, cov in failed if cov]
    if not covered:
        return None
    # An agent is only ever pointed at a quick reader. Pages only a slow structured reader covers
    # stay silent here: that is a person's click on the page, never the agent's choice.
    fast = [cov[0] for _, cov in covered if cov[0].get("speed") == "fast"]
    if not fast:
        return None
    n = len(fast)
    seconds = [c["typical_seconds"] for c in fast if c.get("typical_seconds")]
    points = [c["points_per_unit"] for c in fast if c.get("points_per_unit") is not None]
    secs = f"~{round(statistics.median(seconds))} s" if seconds else "a few seconds"
    pts = f", ~{round(statistics.median(points))} points" if points else ""
    social = sum(1 for c in fast if c.get("service") == SOCIAL)
    tail = f"; {social} via the social reader" if social else ""
    noun = "page" if n == 1 else "pages"
    return (f"{n} {noun} failed that a paid advanced reader can probably open ({secs} each{pts}{tail}). "
            f"Call {tool} with those URLs only if you have no better source.")


__all__ = [
    "Coverage",
    "EXT_MODE",
    "EXT_PRICE",
    "EXT_READER",
    "EXT_RUN_SLOT",
    "EXT_SOCIAL_DETECT",
    "EXT_SPEED",
    "LABELS",
    "SOCIAL",
    "STRUCTURED",
    "UNLOCKER",
    "allowed",
    "coverage_for",
    "fallback_mode",
    "take_run_slot",
    "hint_line",
    "social_platform",
    "speed_class",
    "unlocker_available",
]
