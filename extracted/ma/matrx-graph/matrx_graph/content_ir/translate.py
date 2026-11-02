"""Shared translation helpers — the code that unifies provider spellings.

Every function here exists to turn a provider-specific representation into the
common field downstream can count on (THE MERGE + TRANSLATION LAW).
Approximations are explicit: :func:`parse_published_at` derives an approximate
ISO date from "3 hours ago"-style strings, anchored to the capture moment.

**Only genuinely cross-family helpers live here.** A translator that reaches
into one family's models (``block_from_raw``, ``removals_from_raw``, …) stays
in that family's own ``translate.py``. These were promoted 2026-08-24 from
``search_kinds/translate.py`` and ``scraper_kinds/translate.py``, which held
two ``site_name_from_url`` implementations with two different signatures.

Nothing here imports ``aidream`` or any host module — matrx-graph is standalone.
"""

from __future__ import annotations

import html as html_lib
import re
from datetime import UTC, datetime, timedelta
from typing import Any
from urllib.parse import urlparse

_MONTHS = {
    m.lower(): i
    for i, m in enumerate(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        start=1,
    )
}

_RELATIVE_RE = re.compile(
    r"^\s*(\d+)\s+(minute|hour|day|week|month|year)s?\s+ago\s*$", re.IGNORECASE
)
_ABSOLUTE_RE = re.compile(r"^\s*([A-Za-z]{3,9})\.?\s+(\d{1,2}),\s*(\d{4})\s*$")
_ISO_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")

_RELATIVE_UNIT_DAYS = {
    "minute": 1 / 1440,
    "hour": 1 / 24,
    "day": 1,
    "week": 7,
    "month": 30,
    "year": 365,
}


def parse_published_at(value: str | None, *, now: datetime | None = None) -> str | None:
    """Best-effort ISO-8601 date from any provider date text.

    Handles ISO strings ("2025-12-16T08:00:00"), absolute US dates
    ("Mar 5, 2024"), and relative ages ("3 hours ago" — APPROXIMATE, anchored
    to `now`). Returns None when the text carries no honest date.
    """
    if not value or not isinstance(value, str):
        return None
    text = value.strip()
    if _ISO_PREFIX_RE.match(text):
        return text[:10] if len(text) == 10 else text
    m = _ABSOLUTE_RE.match(text)
    if m:
        month = _MONTHS.get(m.group(1)[:3].lower())
        if month:
            return f"{int(m.group(3)):04d}-{month:02d}-{int(m.group(2)):02d}"
    m = _RELATIVE_RE.match(text)
    if m:
        anchor = now or datetime.now(UTC)
        days = int(m.group(1)) * _RELATIVE_UNIT_DAYS[m.group(2).lower()]
        return (anchor - timedelta(days=days)).date().isoformat()
    return None


def is_relative_age(value: str | None) -> bool:
    return bool(value and _RELATIVE_RE.match(value.strip()))


_TAG_RE = re.compile(r"<[^>]+>")
_HREF_RE = re.compile(r"""href=['"]([^'"]+)['"]""")


def strip_html(value: str | None) -> tuple[str, list[str]]:
    """Convert an HTML fragment to (plain text, extracted link URLs)."""
    if not value:
        return "", []
    links = _HREF_RE.findall(value)
    text = _TAG_RE.sub("", value)
    text = html_lib.unescape(text)
    return re.sub(r"\s+", " ", text).strip(), links


def plain_text(value: str | None) -> str | None:
    """Provider text as a HUMAN reads it — tags gone, entities decoded.

    Every title/snippet/description a provider returns is HTML, not text:
    Brave wraps matched terms in ``<strong>`` and escapes apostrophes as
    ``&#x27;``. The kind carries TEXT, and every consumer renders it as text,
    so the decoding happens once here rather than in each of them (a reader on
    /search saw a literal ``I&#x27;m`` in a result, 2026-08-23).

    Returns None for a non-string or an empty result, so it drops straight into
    an optional field.
    """
    if not isinstance(value, str):
        return None
    text, _ = strip_html(value)
    return text or None


def parse_duration_seconds(value: str | None) -> int | None:
    """'12:38' -> 758; '1:02:03' -> 3723."""
    if not value or not isinstance(value, str):
        return None
    parts = value.strip().split(":")
    if not all(p.isdigit() for p in parts) or not 1 <= len(parts) <= 3:
        return None
    total = 0
    for p in parts:
        total = total * 60 + int(p)
    return total


def site_name_from_url(url: str | None) -> str | None:
    """Host of a URL, without ``www.``. Used only when the source gave none.

    Returns None when there is no host to report — a string that failed to
    parse is not a site name, and inventing one is the kind of quiet dishonesty
    the translation law exists to stop. A caller whose kind field is a required
    ``str`` supplies its own last-resort fallback at the call site, in the open.
    (``urlparse().hostname`` is already lowercased, so no case handling here.)
    """
    if not url:
        return None
    host = urlparse(url).hostname
    if not host:
        return None
    return host.removeprefix("www.")


def displayed_url_from(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or url).removeprefix("www.")
    segments = [s for s in (parsed.path or "").split("/") if s]
    return " › ".join([host, *segments])


def big_int_to_string(value: Any) -> str | None:
    """A 64-bit hash as a decimal STRING.

    ``simhash`` is routinely 19 digits (measured: ``7046352583261510909``),
    which is past ``Number.MAX_SAFE_INTEGER``. Sent as a JSON number, every
    JavaScript consumer silently rounds it and distinct pages start comparing
    equal.
    """
    if value is None or value == "":
        return None
    return str(value)
