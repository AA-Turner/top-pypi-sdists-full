"""One window grammar, one timestamp coercion (PF-398).

Both of these had grown several byte-identical copies, in modules that do not
import each other and so could drift apart silently:

* the relative-window grammar (`3d`, `12h`, `2w`) existed as
  `_WINDOW_RE`/`_WINDOW_UNITS` in `services/summary_service.py` and as
  `_RELATIVE_SINCE`/`_RELATIVE_UNITS` in `cli/commands/sync.py` -- the same
  duplication class as the `_parse_since` collision fixed earlier in this
  branch. Two spellings of one grammar is not a cosmetic problem: the spec
  string is the summary cache key, so a divergence between what the CLI
  accepts and what the engine accepts is a permanent cache miss that looks
  like the cache working.
* "an ISO string (or a datetime) read as aware UTC" existed three times, in
  `board_sync_service._parse_since`, `code_activity._parse_github_time` and
  the absolute branch of `cli/commands/sync.parse_since`. Each returned the
  same thing for the same input; each had made its own decision about naive
  input, and a naive value compared against an aware one raises TypeError.

A third divergence, fixed later: the *vocabulary*. The CLI's `--window` accepted
`day | week | 3d | release` while the engine accepted only the grammar above, so
`--window day` was legal at one surface and a 422 at another, and `2w` -- fine to
the engine -- was rejected by the CLI. The grammar is canonical and the words are
aliases onto it (`WINDOW_ALIASES`), resolved here so every surface agrees.

Callers still keep their own error types and their own logging -- what is shared
is the parsing and the vocabulary, not what to do when either fails.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta, timezone
from typing import Optional, Union

#: `3d`, `12 h`, `2W`. Whitespace-tolerant, deliberately nothing else: the spec
#: is a cache key, so accepting two spellings of one window ('3d', '72h') that
#: produce different keys would silently halve the hit rate.
WINDOW_RE = re.compile(r"^\s*(\d+)\s*([hdw])\s*$", re.IGNORECASE)
WINDOW_UNITS = {"h": "hours", "d": "days", "w": "weeks"}

#: Words the CLI has always accepted for `--window`, mapped onto the grammar.
#: They are resolved *here*, not in the CLI, so that a word arriving by any
#: other route -- the MCP tool, a hand-written API call -- means the same thing
#: instead of being rejected. `release` is deliberately absent, but no longer for
#: the reason this comment used to give ("it has no fixed answer and is resolved
#: against the project's last release at call time"). Since #563 `release` is not
#: a duration at all: it is a *scope*, carried as the `release:<version>` spec and
#: resolved by `summary_service.resolve_scope`. It is absent here because it does
#: not belong to this grammar, not because it resolves late.
WINDOW_ALIASES = {"day": "1d", "week": "1w"}

#: The one phrasing of "what a window looks like". Every surface that rejects a
#: window quotes this, so the CLI, the engine and the MCP tool cannot describe
#: the same grammar three different ways -- which is exactly how `--window day`
#: came to be legal in one and a 422 in another.
WINDOW_GRAMMAR_HINT = "a duration like '3d', '12h' or '2w', or one of: " + ", ".join(
    sorted(WINDOW_ALIASES)
)


def normalize_window(spec: str) -> Optional[str]:
    """``'day'``/``' 3D '`` → ``'3d'``; ``None`` when `spec` is not a window.

    Canonical form is lowercase, unpadded and un-zero-padded because the spec
    *is* the summary cache key. `WINDOW_RE` is deliberately case-insensitive
    and whitespace-tolerant, so `'3D'` and `'3d'` already parse to the same
    timedelta -- but stored verbatim they are two cache entries for one window,
    the same halved-hit-rate failure the grammar comment above warns about, one
    level up. Normalising on the way in is what makes that comment true.

    Raises `ValueError` for a window that parses but covers less than one unit,
    by delegating to `parse_window` rather than re-deciding it here.
    """
    candidate = str(spec or "").strip().lower()
    canonical = WINDOW_ALIASES.get(candidate, candidate)
    if parse_window(canonical) is None:
        return None
    match = WINDOW_RE.match(canonical)
    assert match is not None  # parse_window just matched the same pattern
    return f"{int(match.group(1))}{match.group(2).lower()}"


def parse_window(spec: str) -> Optional[timedelta]:
    """``'3d'`` → 3 days; ``None`` when `spec` is not a window at all.

    Returns None rather than raising because the two callers want different
    exceptions for it -- `InvalidWindowSpec` in the engine, `ValueError` with
    a `--since`-flavoured message in the CLI. A window that parses but covers
    less than one unit *does* raise `ValueError`: that is a malformed window,
    not "this string is a date instead".
    """
    match = WINDOW_RE.match(spec or "")
    if not match:
        return None
    amount = int(match.group(1))
    if amount < 1:
        raise ValueError("a window must cover at least one unit")
    return timedelta(**{WINDOW_UNITS[match.group(2).lower()]: amount})


def as_utc(value: Optional[datetime]) -> Optional[datetime]:
    """A datetime read as UTC when it carries no timezone.

    Naive timestamps come straight out of the database -- `Summary.created_at`
    and `BoardSyncHistory.completed_at` are naive columns written from
    `datetime.utcnow()`. Comparing one against an aware `now` raises TypeError,
    which inside a cache gate reads as "miss" and quietly disables caching.
    """
    if value is None:
        return None
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def parse_iso_utc(value: Union[str, datetime, None]) -> Optional[datetime]:
    """An ISO-8601 string (or a datetime) as an aware UTC datetime, else None.

    Trailing `Z` is accepted, which `datetime.fromisoformat` did not handle
    before 3.11 and which every hand-rolled copy of this had to special case.

    **It has not replaced them all**, and saying so here previously was simply
    untrue: measured 2026-08-10, four files import this and roughly two dozen
    `fromisoformat(...replace("Z", "+00:00"))` sites remain. The blocker was
    that this returns an *aware* value while most columns in this schema are
    naive (99 naive to 7 aware) -- `parse_iso_naive` now covers that case, so
    the remaining copies can be retired as their files are touched rather than
    in one sweep. The ones with no error handling, and the one that stripped an
    offset instead of converting it, have been done.

    Note that "UTC" here means *an aware datetime describing the right
    instant*, not necessarily one whose tzinfo is UTC: an input carrying
    `+02:00` is returned at `+02:00`. Aware comparisons handle that correctly.
    If you need the tzinfo normalised, `astimezone(timezone.utc)` it -- or use
    `parse_iso_naive`, which does. Unparseable is None, never an exception: each caller decides whether
    that is an error, a skipped record, or "no watermark".
    """
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return as_utc(value)
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return as_utc(parsed)


def parse_iso_naive(value: Union[str, datetime, None]) -> Optional[datetime]:
    """`parse_iso_utc`, but returning **naive UTC** for this schema's columns.

    The reason 31 hand-rolled copies of this parse outlived `parse_iso_utc`,
    whose docstring claimed it replaced "every one of the copies": it returns an
    *aware* datetime, and most columns here are naive (measured: 99 naive to 7
    aware). Every would-be caller with a naive column had to parse and then
    `.replace(tzinfo=None)` itself, so it kept its own copy instead -- and the
    copies drifted, several of them into `fromisoformat` calls with no error
    handling at all.

    An offset is **converted, not discarded**: `+02:00` moves the instant two
    hours, and dropping it silently records the wrong time. Same
    never-raises contract as `parse_iso_utc` -- unparseable is None, because
    every caller here is reading a third-party API payload where "this field is
    junk today" must not take down a sync.
    """
    parsed = parse_iso_utc(value)
    if parsed is None:
        return None
    # `astimezone` first, then strip. `as_utc` (which `parse_iso_utc` uses)
    # only *attaches* UTC to a naive value -- by design, that is its whole job --
    # and leaves an aware one at its original offset. Stripping tzinfo straight
    # off a `+02:00` value therefore records an instant two hours wrong, which
    # is precisely the bug the hand-rolled copies carry.
    return parsed.astimezone(timezone.utc).replace(tzinfo=None)


#: Month abbreviations, spelled out rather than taken from `strftime`, so the
#: rendering does not depend on the process locale. `%b` is locale-sensitive:
#: a container with a non-English locale would render a summary note's date in
#: another language beside English prose.
_MONTH_ABBR = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)


def format_note_date(
    moment: Optional[datetime], *, today: Optional[datetime] = None
) -> str:
    """``9 Aug``, or ``9 Aug 2025`` once it is not from the current year.

    One implementation for the CLI and the dashboard. They render the same
    field beside the same prose, and they had drifted immediately -- `Aug 9`
    against `9 Aug` -- which reads as two different pieces of data rather than
    one formatted two ways.

    **Built by hand, not by `strftime`.** `%-d` (no zero padding) is a glibc
    extension: musl and Windows reject it, so a template using it does not
    render differently there, it raises and takes the page with it. `%b` is
    locale-sensitive for the same class of reason.

    **The year appears only when it is not the current one**, because a summary
    note is inherited indefinitely -- a note from last August is both the most
    likely to be acted on wrongly and the one a bare `9 Aug` disguises best.
    Suppressing it for this year keeps the common case short.
    """
    if moment is None:
        return ""
    stamped = as_utc(moment)
    now = as_utc(today) if today is not None else datetime.now(timezone.utc)
    day = f"{stamped.day} {_MONTH_ABBR[stamped.month - 1]}"
    return day if stamped.year == now.year else f"{day} {stamped.year}"


def format_target_date(day: Optional[date], *, today: Optional[date] = None) -> str:
    """``14 Nov``, or ``14 Nov 2027`` once it is not the current year.

    The same shape as `format_note_date` and sharing its month table, because the
    two appear on the same page and a `14 Nov` beside a `Nov 14` reads as two
    different kinds of data rather than one style applied twice.

    Takes a `date`, not a `datetime`: `Release.target_date` is a calendar day
    (see the column's own note), and accepting a datetime here would invite a
    caller to pass an aware one and get a day-boundary shift for their trouble.

    Empty string for `None`, which is the common case -- a release has no target
    until somebody sets one, and the callers render their own "not set" wording
    around it.
    """
    if day is None:
        return ""
    current = today.year if today is not None else datetime.now(timezone.utc).year
    stamp = f"{day.day} {_MONTH_ABBR[day.month - 1]}"
    return stamp if day.year == current else f"{stamp} {day.year}"
