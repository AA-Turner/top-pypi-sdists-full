"""SerpAPI location resolution — the ONE place a free-text place name becomes
the canonical SerpAPI location string.

SerpAPI's ``location`` parameter is not fuzzy: it accepts only names from its
own catalogue, in the exact canonical form (comma separated, **no space after
the commas**) — ``Newport Beach,California,United States``. Anything else is a
hard HTTP 400 on EVERY search, forever, so an unvalidated free-text location
stored on a rank target is a permanently dead target that silently records zero
observations.

This module resolves the name ONCE, at target-creation time, against the free
``locations.json`` catalogue endpoint (no API key, no search credit), and
caches the answer. It must never be called from a scheduled check's hot path.

Resolution is deliberately generous — over-tightening is a defect. A name that
identifies exactly one place is CORRECTED to its canonical form rather than
refused (``Newport Beach, CA`` -> ``Newport Beach,California,United States``);
only a genuinely ambiguous or genuinely unknown name is refused, and the
refusal carries the candidate canonical names so the caller can pick one.
"""

from __future__ import annotations

import asyncio
from collections.abc import Iterable, Mapping, Sequence
from time import monotonic
from typing import Any, Protocol

import httpx
from pydantic import BaseModel, ConfigDict

LOCATIONS_ENDPOINT = "https://serpapi.com/locations.json"

# CAPS — catalogue lookup behaviour. Not env vars: these are product choices.
CANDIDATE_LIMIT = 25
SUGGESTION_LIMIT = 5
POSITIVE_CACHE_TTL_SECONDS = 24 * 60 * 60
NEGATIVE_CACHE_TTL_SECONDS = 15 * 60

# Abbreviations a human types instead of the catalogue's spelled-out segment.
# Matching is "any expansion matches any canonical segment", so an ambiguous
# abbreviation (CA = California OR Canada) simply widens the accepted set and
# is then disambiguated by the rest of the name.
_SEGMENT_ALIASES: dict[str, tuple[str, ...]] = {
    "us": ("united states",),
    "usa": ("united states",),
    "u.s.": ("united states",),
    "u.s.a.": ("united states",),
    "america": ("united states",),
    "uk": ("united kingdom",),
    "u.k.": ("united kingdom",),
    "gb": ("united kingdom",),
    "great britain": ("united kingdom",),
    "uae": ("united arab emirates",),
    "al": ("alabama",),
    "ak": ("alaska",),
    "az": ("arizona",),
    "ar": ("arkansas",),
    "ca": ("california", "canada"),
    "co": ("colorado",),
    "ct": ("connecticut",),
    "de": ("delaware", "germany"),
    "dc": ("district of columbia",),
    "fl": ("florida",),
    "ga": ("georgia",),
    "hi": ("hawaii",),
    "id": ("idaho",),
    "il": ("illinois",),
    "in": ("indiana",),
    "ia": ("iowa",),
    "ks": ("kansas",),
    "ky": ("kentucky",),
    "la": ("louisiana",),
    "me": ("maine",),
    "md": ("maryland",),
    "ma": ("massachusetts",),
    "mi": ("michigan",),
    "mn": ("minnesota",),
    "ms": ("mississippi",),
    "mo": ("missouri",),
    "mt": ("montana",),
    "ne": ("nebraska",),
    "nv": ("nevada",),
    "nh": ("new hampshire",),
    "nj": ("new jersey",),
    "nm": ("new mexico",),
    "ny": ("new york",),
    "nc": ("north carolina",),
    "nd": ("north dakota",),
    "oh": ("ohio",),
    "ok": ("oklahoma",),
    "or": ("oregon",),
    "pa": ("pennsylvania",),
    "ri": ("rhode island",),
    "sc": ("south carolina",),
    "sd": ("south dakota",),
    "tn": ("tennessee",),
    "tx": ("texas",),
    "ut": ("utah",),
    "vt": ("vermont",),
    "va": ("virginia",),
    "wa": ("washington",),
    "wv": ("west virginia",),
    "wi": ("wisconsin",),
    "wy": ("wyoming",),
    "ab": ("alberta",),
    "bc": ("british columbia",),
    "mb": ("manitoba",),
    "nb": ("new brunswick",),
    "nl": ("newfoundland and labrador", "netherlands"),
    "ns": ("nova scotia",),
    "on": ("ontario",),
    "pe": ("prince edward island", "peru"),
    "qc": ("quebec",),
    "sk": ("saskatchewan",),
}


class SerpApiLocation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str = ""
    canonical_name: str = ""
    target_type: str | None = None
    reach: int | None = None


class SerpApiLocationUnresolved(ValueError):
    """The catalogue answered and the name is not usable as-is.

    A ``ValueError`` on purpose: every caller already surfaces those as a 422
    with the message, and the message carries the canonical suggestions.
    """

    def __init__(self, query: str, suggestions: Sequence[str], *, ambiguous: bool) -> None:
        self.query = query
        self.suggestions = list(suggestions)
        self.ambiguous = ambiguous
        if suggestions:
            listed = " | ".join(f'"{item}"' for item in suggestions)
            reason = "matches more than one place" if ambiguous else "is not a SerpAPI location"
            message = (
                f'location "{query}" {reason}. Use the exact canonical name '
                f"(commas, no spaces): {listed}"
            )
        else:
            message = (
                f'location "{query}" is not a SerpAPI location and the catalogue '
                "offered no close match — search https://serpapi.com/locations-api "
                "for the canonical name"
            )
        super().__init__(message)


class SerpApiLocationCatalogUnavailable(RuntimeError):
    """The catalogue could not be reached. NEVER a refusal on its own — a
    creation must not fail because a validation endpoint is down."""


class SerpApiLocationTransport(Protocol):
    async def search(self, query: str, limit: int) -> list[dict[str, Any]]: ...


class HttpxSerpApiLocationTransport:
    def __init__(self, timeout: httpx.Timeout | None = None) -> None:
        self.timeout = timeout or httpx.Timeout(connect=5, read=15, write=5, pool=5)

    async def search(self, query: str, limit: int) -> list[dict[str, Any]]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(LOCATIONS_ENDPOINT, params={"q": query, "limit": limit})
        except httpx.HTTPError as exc:
            raise SerpApiLocationCatalogUnavailable(
                f"SerpAPI location catalogue unreachable: {type(exc).__name__}"
            ) from exc
        if response.status_code >= 400:
            raise SerpApiLocationCatalogUnavailable(
                f"SerpAPI location catalogue returned HTTP {response.status_code}"
            )
        try:
            payload = response.json()
        except ValueError as exc:
            raise SerpApiLocationCatalogUnavailable(
                "SerpAPI location catalogue returned non-JSON"
            ) from exc
        if not isinstance(payload, list):
            raise SerpApiLocationCatalogUnavailable(
                "SerpAPI location catalogue must return a JSON array"
            )
        return [item for item in payload if isinstance(item, dict)]


def normalize_location_query(value: str) -> str:
    """Canonical WIRE form: comma separated, no spaces around the commas."""
    segments = location_segments(value)
    if not segments:
        raise ValueError("location cannot be blank")
    return ",".join(segments)


def location_segments(value: str) -> list[str]:
    return [segment.strip() for segment in value.split(",") if segment.strip()]


def _expansions(segment: str) -> tuple[str, ...]:
    folded = segment.casefold()
    return (folded, *_SEGMENT_ALIASES.get(folded, ()))


def _matches_tail(candidate: SerpApiLocation, tail: Sequence[str]) -> bool:
    canonical_segments = {
        segment.casefold() for segment in location_segments(candidate.canonical_name)
    }
    return all(
        any(expansion in canonical_segments for expansion in _expansions(segment))
        for segment in tail
    )


def _by_reach(candidates: Iterable[SerpApiLocation]) -> list[SerpApiLocation]:
    return sorted(candidates, key=lambda item: (item.reach or 0), reverse=True)


class SerpApiLocationResolver:
    """Process-wide resolver with a TTL cache. Creation-time only."""

    def __init__(self, transport: SerpApiLocationTransport | None = None) -> None:
        self.transport = transport or HttpxSerpApiLocationTransport()
        self._cache: dict[str, tuple[float, str | None, list[str], bool]] = {}
        self._lock = asyncio.Lock()

    def clear_cache(self) -> None:
        self._cache.clear()

    async def resolve(self, location: str) -> str:
        """Return the canonical SerpAPI location name for ``location``.

        Raises ``SerpApiLocationUnresolved`` when the catalogue answered and
        the name is unknown or ambiguous, and
        ``SerpApiLocationCatalogUnavailable`` when the catalogue itself could
        not be consulted.
        """
        query = normalize_location_query(location)
        key = query.casefold()
        cached = self._cache.get(key)
        if cached is not None and cached[0] > monotonic():
            _, canonical, suggestions, ambiguous = cached
            if canonical is not None:
                return canonical
            raise SerpApiLocationUnresolved(query, suggestions, ambiguous=ambiguous)

        segments = location_segments(query)
        head = segments[0]
        tail = segments[1:]

        candidates = await self._search(query)
        exact = next(
            (item for item in candidates if item.canonical_name.casefold() == key),
            None,
        )
        if exact is not None:
            return self._remember(key, exact.canonical_name)

        if head.casefold() != key:
            candidates = _dedupe(candidates + await self._search(head))

        survivors = [
            item
            for item in candidates
            if item.name.casefold() == head.casefold() and _matches_tail(item, tail)
        ]
        if len(survivors) > 1:
            cities = [item for item in survivors if (item.target_type or "").casefold() == "city"]
            if len(cities) == 1:
                survivors = cities
        if len(survivors) == 1:
            return self._remember(key, survivors[0].canonical_name)

        pool = survivors or candidates
        suggestions = [item.canonical_name for item in _by_reach(pool)[:SUGGESTION_LIMIT]]
        ambiguous = len(survivors) > 1
        self._cache[key] = (
            monotonic() + NEGATIVE_CACHE_TTL_SECONDS,
            None,
            suggestions,
            ambiguous,
        )
        raise SerpApiLocationUnresolved(query, suggestions, ambiguous=ambiguous)

    def _remember(self, key: str, canonical: str) -> str:
        self._cache[key] = (monotonic() + POSITIVE_CACHE_TTL_SECONDS, canonical, [], False)
        return canonical

    async def _search(self, query: str) -> list[SerpApiLocation]:
        async with self._lock:
            rows = await self.transport.search(query, CANDIDATE_LIMIT)
        return [SerpApiLocation.model_validate(row) for row in rows if _has_canonical(row)]


def _has_canonical(row: Mapping[str, Any]) -> bool:
    return bool(str(row.get("canonical_name") or "").strip())


def _dedupe(items: Sequence[SerpApiLocation]) -> list[SerpApiLocation]:
    seen: set[str] = set()
    unique: list[SerpApiLocation] = []
    for item in items:
        key = item.canonical_name.casefold()
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


_DEFAULT_RESOLVER = SerpApiLocationResolver()


async def resolve_serpapi_location(location: str) -> str:
    """Module-level convenience over the shared, cached resolver."""
    return await _DEFAULT_RESOLVER.resolve(location)


def default_location_resolver() -> SerpApiLocationResolver:
    return _DEFAULT_RESOLVER


__all__ = [
    "CANDIDATE_LIMIT",
    "HttpxSerpApiLocationTransport",
    "LOCATIONS_ENDPOINT",
    "SerpApiLocation",
    "SerpApiLocationCatalogUnavailable",
    "SerpApiLocationResolver",
    "SerpApiLocationTransport",
    "SerpApiLocationUnresolved",
    "default_location_resolver",
    "location_segments",
    "normalize_location_query",
    "resolve_serpapi_location",
]
