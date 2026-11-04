"""Runtime deprecation notices, read off the response.

A port of the TypeScript golden reference (``src/compat/deprecation.ts``), with
the same three fields and the same confinement rules:

* ``Deprecation`` (RFC 9745) — an Item Structured Field whose value is a Date
  (RFC 9651 §3.3.7): ``@`` followed by integer seconds since the Unix epoch,
  e.g. ``Deprecation: @1688169599``.
* ``Sunset`` (RFC 8594) — an HTTP-date, e.g.
  ``Sunset: Sat, 31 Dec 2018 23:59:59 GMT``.
* ``Link`` (RFC 8288) — ``rel="deprecation"`` points at human-readable notes,
  ``rel="successor-version"`` (RFC 5829) at the replacement resource.

Where the TypeScript client writes through its ``logger`` at ``warn``, this one
raises :class:`ComposioDeprecationWarning`, because a warning is how Python
says this. Deduplication is the *client's*, not the :mod:`warnings` module's:
each client instance warns at most once per distinct notice per operation,
regardless of the process-wide warning filters in force.

A deprecation notice is advisory: an oversized field, a control character, an
unparseable date or a cross-origin successor is dropped rather than surfaced,
and nothing here raises of its own accord.

The one exception is deliberate and belongs to the caller, not to this module.
Under ``-W error`` (or pytest's ``filterwarnings = ["error"]``) the
:func:`warnings.warn` call below *does* raise, because that is precisely what
the caller asked warnings to do. The kernel honors that intent only for a
response that succeeded -- see ``_note_deprecation`` in :mod:`._base_client`,
which never lets an advisory notice displace a real API error.
"""

from __future__ import annotations

import functools
import re
import warnings
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, NamedTuple
from urllib.parse import urlsplit

import httpx

from ._deprecated_inputs import DEPRECATED_INPUTS, DeprecatedInput
from ._operations import OPERATIONS, Operation

__all__ = ["ComposioDeprecationWarning"]


class ComposioDeprecationWarning(UserWarning):
    """A deprecated API operation was called.

    Raised once per distinct notice per operation per client instance when the
    server announces the deprecation with an RFC 9745 ``Deprecation`` response
    header. It is a :class:`UserWarning` rather than a
    :class:`DeprecationWarning` on purpose:
    ``DeprecationWarning`` is hidden by default outside ``__main__``, and this
    one is aimed at the application developer whose call is about to stop
    working. Silence it with the usual filters::

        warnings.filterwarnings("ignore", category=ComposioDeprecationWarning)
    """


#: Field-size ceiling; an oversized field is dropped rather than parsed.
MAX_FIELD_LENGTH = 2048

#: How many distinct (operation, notice) pairs one client instance will ever
#: warn about. The operation table is fixed and small and a server revises a notice
#: rarely, so the bound is unreachable in practice; it exists because both
#: halves of the key are server- or caller-controlled -- an escape-hatch caller
#: keys on a substituted path, and a server rotating ``Sunset`` or ``Link`` on
#: every response mints a fresh pair each time.
MAX_TRACKED_NOTICES = 1024

_CONTROL_CHARACTERS = re.compile(r"[\x00-\x1f\x7f]")
_STRUCTURED_DATE = re.compile(r"^@(-?\d{1,15})$")


def _read_field(headers: httpx.Headers, name: str) -> str | None:
    value: str | None = headers.get(name)
    if value is None:
        return None
    if len(value) > MAX_FIELD_LENGTH or _CONTROL_CHARACTERS.search(value):
        return None
    return value


def parse_structured_date(value: str) -> datetime | None:
    """RFC 9651 §3.3.7 sf-date: ``@`` then integer seconds since the epoch.

    Anything else — including the pre-RFC ``true`` and bare HTTP-date spellings
    the draft years produced — yields no date. The notice still fires: the
    server sending the field at all is the signal.
    """
    match = _STRUCTURED_DATE.match(value.strip())
    if match is None:
        return None
    try:
        return datetime.fromtimestamp(int(match.group(1)), tz=timezone.utc)
    except (OverflowError, OSError, ValueError):
        return None


_MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
_DAY = "(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)"
_DAY_LONG = "(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"
_MONTH = f"({'|'.join(_MONTHS)})"
_TIME = r"(\d{2}):(\d{2}):(\d{2})"

#: ``day-name "," SP 2DIGIT SP month SP 4DIGIT SP time-of-day SP GMT``
_IMF_FIXDATE = re.compile(rf"^{_DAY}, (\d{{2}}) {_MONTH} (\d{{4}}) {_TIME} GMT$")
#: ``day-name-l "," SP 2DIGIT "-" month "-" 2DIGIT SP time-of-day SP GMT``
_RFC850_DATE = re.compile(rf"^{_DAY_LONG}, (\d{{2}})-{_MONTH}-(\d{{2}}) {_TIME} GMT$")
#: ``day-name SP month SP ( 2DIGIT / ( SP 1DIGIT ) ) SP time-of-day SP 4DIGIT``
_ASCTIME_DATE = re.compile(rf"^{_DAY} {_MONTH} (\d{{2}}| \d) {_TIME} (\d{{4}})$")


def parse_http_date(value: str) -> datetime | None:
    """RFC 8594 ``Sunset``: an HTTP-date.

    RFC 7231 §7.1.1.1 defines exactly three forms -- IMF-fixdate (the only one
    a sender may generate), and the obsolete rfc850-date and asctime-date a
    recipient must still accept. All three denote UTC.

    Written out by hand rather than delegated to
    :func:`email.utils.parsedate_to_datetime`, which parses RFC 5322 -- a
    neighbouring grammar, not this one. It accepted a numeric offset
    (``-0500``) and a zone-less timestamp, neither of which is an HTTP-date,
    and its two-digit-year and obsolete-zone rules are its own. The TypeScript
    client is held to identical parses on every input;
    ``test/fixtures/http-date-vectors.json`` is the table both suites read.

    Rejection is not a silencer: an unparseable ``Sunset`` leaves the removal
    date out of the warning, and the notice still fires on the field's
    presence -- the same stance :func:`parse_structured_date` takes on
    ``Deprecation``.
    """
    trimmed = value.strip()

    # Each branch normalizes its capture order into the same six fields, so the
    # validation below is written once and the three grammars differ only in
    # how they are spelled.
    match = _IMF_FIXDATE.match(trimmed)
    if match is not None:
        year, month, day = int(match.group(3)), match.group(2), match.group(1)
        clock = match.group(4, 5, 6)
    elif (match := _RFC850_DATE.match(trimmed)) is not None:
        # A two-digit year keeps the fixed CPython mapping this function has
        # always applied through ``email.utils`` (``< 70`` is the 21st
        # century) rather than RFC 7231's sliding 50-year window, which would
        # make a parsed sunset date change century as the clock advanced.
        short = int(match.group(3))
        year, month, day = (2000 + short if short < 70 else 1900 + short), match.group(2), match.group(1)
        clock = match.group(4, 5, 6)
    elif (match := _ASCTIME_DATE.match(trimmed)) is not None:
        year, month, day = int(match.group(6)), match.group(1), match.group(2).strip()
        clock = match.group(3, 4, 5)
    else:
        return None

    hour, minute, second = (int(part) for part in clock)
    if hour > 23 or minute > 59 or second > 59:
        return None
    try:
        # ``datetime`` is the calendar check: an impossible day (`31 Feb`) or a
        # year below ``MINYEAR`` raises rather than rolling forward.
        return datetime(year, _MONTHS.index(month) + 1, int(day), hour, minute, second, tzinfo=timezone.utc)
    except ValueError:
        return None


class Link(NamedTuple):
    target: str
    rels: tuple[str, ...]
    #: True when the link carried an ``anchor`` parameter. RFC 8288 §3.2 makes
    #: ``anchor`` re-point the link's *context* at some other resource, so such
    #: a link says nothing about the response it arrived on.
    anchored: bool


def parse_link_field(value: str) -> tuple[Link, ...]:
    """RFC 8288 ``Link``, enough of it.

    A comma-separated list of ``<target>`` each followed by ``;``-separated
    parameters, where a parameter value may be quoted (and may therefore
    contain commas and semicolons). Only ``rel`` is retained. Malformed input
    truncates the list instead of failing — whatever parsed before the damage is
    still usable.
    """
    links: list[Link] = []
    index = 0
    length = len(value)

    def at(position: int) -> str:
        return value[position] if position < length else ""

    while index < length:
        while index < length and at(index) in ", \t":
            index += 1
        if at(index) != "<":
            break
        close = value.find(">", index)
        if close < 0:
            break
        target = value[index + 1 : close].strip()
        index = close + 1

        rels: list[str] = []
        seen_rel = False
        anchored = False
        while index < length:
            while index < length and at(index) in " \t":
                index += 1
            if at(index) == ",":
                index += 1
                break
            if at(index) != ";":
                index += 1
                continue
            index += 1
            name_start = index
            while index < length and at(index) not in "=;,":
                index += 1
            name = value[name_start:index].strip().lower()

            parameter = ""
            if at(index) == "=":
                index += 1
                while index < length and at(index) in " \t":
                    index += 1
                if at(index) == '"':
                    index += 1
                    parts: list[str] = []
                    while index < length and at(index) != '"':
                        if at(index) == "\\" and index + 1 < length:
                            parts.append(at(index + 1))
                            index += 2
                            continue
                        parts.append(at(index))
                        index += 1
                    index += 1
                    parameter = "".join(parts)
                else:
                    start = index
                    while index < length and at(index) not in ";,":
                        index += 1
                    parameter = value[start:index].strip()

            # Only the first ``rel`` on a link counts (RFC 8288 §3.3);
            # accumulating later ones would let ``rel=alternate; rel=deprecation``
            # smuggle an arbitrary target into the relation this client acts on.
            if name == "rel" and not seen_rel:
                seen_rel = True
                rels.extend(rel.lower() for rel in parameter.split() if rel)
            if name == "anchor":
                anchored = True

        links.append(Link(target, tuple(rels), anchored))

    return tuple(links)


def _resolve(target: str, base_url: str) -> httpx.URL | None:
    """``target`` resolved against ``base_url``, restricted to http(s)."""
    try:
        url = httpx.URL(base_url).join(target)
    except (httpx.InvalidURL, UnicodeError, ValueError):
        return None
    return url if url.scheme in ("http", "https") else None


def _same_origin(target: str, context_url: str, base_url: str) -> httpx.URL | None:
    """A successor is only followed as far as *naming* it, and only when it
    lands on the API this client is configured against.

    Two URLs are in play and conflating them is a real exposure. The *context*
    is the URL the response actually came from, which is what RFC 8288 §3.1
    resolves a relative target against -- and after a redirect that is not the
    URL we asked for. The *origin allowlist* stays the configured ``base_url``
    precisely so a redirected response cannot nominate itself by emitting a
    relative link that lands back on our origin.
    """
    url = _resolve(target, context_url)
    if url is None:
        return None
    try:
        base = httpx.URL(base_url)
    except (httpx.InvalidURL, UnicodeError, ValueError):
        return None
    return url if (url.scheme, url.host, url.port) == (base.scheme, base.host, base.port) else None


class Notice(NamedTuple):
    """What the three response fields said, after parsing and validation."""

    deprecated_at: datetime | None
    sunset_at: datetime | None
    documentation: str | None
    successor: httpx.URL | None


def parse_deprecation(headers: httpx.Headers, context_url: str, base_url: str) -> Notice | None:
    """The notice a response carries, or ``None`` when it carries none.

    The ``Deprecation`` field's *presence* is what marks the operation
    deprecated; ``Sunset`` and ``Link`` only enrich the message.

    ``context_url`` is the response's own URL (post-redirect), the context RFC
    8288 resolves relative link targets against; ``base_url`` is the configured
    API origin a successor must land on.
    """
    deprecation = _read_field(headers, "deprecation")
    if deprecation is None:
        return None

    sunset = _read_field(headers, "sunset")
    link = _read_field(headers, "link")
    links = parse_link_field(link) if link is not None else ()

    def target_for(rel: str) -> str | None:
        # An anchored link describes some other resource (RFC 8288 §3.2), so it
        # says nothing about the response it rode in on.
        return next(
            (c.target for c in links if not c.anchored and rel in c.rels),
            None,
        )

    documentation = target_for("deprecation")
    successor = target_for("successor-version")
    # The documentation link points at developer notes, which live off the API
    # origin by design; it is only ever printed, so http(s) is the whole bar.
    documentation_url = None if documentation is None else _resolve(documentation, context_url)

    return Notice(
        deprecated_at=parse_structured_date(deprecation),
        sunset_at=None if sunset is None else parse_http_date(sunset),
        documentation=None if documentation_url is None else str(documentation_url),
        successor=None if successor is None else _same_origin(successor, context_url, base_url),
    )


def _segments(path: str) -> list[str]:
    return [segment for segment in urlsplit(path).path.split("/") if segment]


@functools.lru_cache(maxsize=1024)
def _template_segments(operation: Operation) -> tuple[str, ...]:
    """A template's segments, cached: the operations table is module-level and
    immortal, so the match pays the split once per operation rather than once
    per request. Bounded because a test's stand-in table is not immortal."""
    return tuple(_segments(operation.path))


def _index_operations(
    operations: tuple[Operation, ...],
) -> dict[tuple[str, int], tuple[Operation, ...]]:
    grouped: dict[tuple[str, int], list[Operation]] = {}
    for operation in operations:
        key = (operation.method, len(_template_segments(operation)))
        grouped.setdefault(key, []).append(operation)
    return {key: tuple(group) for key, group in grouped.items()}


_OPERATIONS_BY_SHAPE = _index_operations(OPERATIONS)


def match_operation(method: str, path: str, operations: tuple[Operation, ...]) -> Operation | None:
    """The operation a dispatched request belongs to, recovered from its path.

    Path parameters are percent-encoded on the way out (``path_segment``), which
    encodes ``/`` and leaves the unreserved characters every literal template
    segment is made of — so a substituted path has the same segment count as its
    template and its literal segments compare byte for byte. Where a
    parameterized template and a literal one overlap the literal wins, the same
    most-specific-first rule the server routes by.
    """
    wanted = method.lower()
    segments = _segments(path)
    best: Operation | None = None
    best_literals = -1
    candidates = (
        _OPERATIONS_BY_SHAPE.get((wanted, len(segments)), ()) if operations is OPERATIONS else operations
    )

    for operation in candidates:
        if operation.method != wanted:
            continue
        template = _template_segments(operation)
        if len(template) != len(segments):
            continue

        literals = 0
        matched = True
        for part, segment in zip(template, segments, strict=True):
            if part.startswith("{") and part.endswith("}"):
                continue
            if part != segment:
                matched = False
                break
            literals += 1

        if matched and literals > best_literals:
            best = operation
            best_literals = literals

    return best


def match_successor_chain(
    method: str, successor: httpx.URL, operations: tuple[Operation, ...]
) -> tuple[str, ...] | None:
    """The client chain a successor URL names, under the *same* HTTP method.

    RFC 5829's ``successor-version`` points at a resource, and an earlier
    revision of this code fell back to any unambiguous match under a different
    method when the same one missed. That was wrong in a way that matters: it
    could answer a deprecated ``GET`` with "use ``client....create`` instead",
    telling the caller to replace a read with a write. A successor named under
    a different method is not a successor for *this* operation, so it is left
    unnamed and the raw URL is printed instead.
    """
    matched = match_operation(method, successor.path, operations)
    return None if matched is None else matched.chain


def _chain_label(chain: tuple[str, ...]) -> str:
    return f"`client.{'.'.join(chain)}`"


def format_warning(subject: str, notice: Notice, successor_chain: tuple[str, ...] | None) -> str:
    # The TypeScript client prefixes this first clause with "Composio: ";
    # here the `warnings` module already renders the category name
    # ("ComposioDeprecationWarning: ..."), so repeating the brand would stutter.
    # Every clause after the first is identical across the two clients.
    parts = [f"{subject} is deprecated."]
    if notice.deprecated_at is not None:
        parts.append(f"Announced {_isoformat(notice.deprecated_at)}.")
    if notice.sunset_at is not None:
        parts.append(f"Scheduled for removal on {_isoformat(notice.sunset_at)}.")
    if successor_chain is not None:
        parts.append(f"Use {_chain_label(successor_chain)} instead.")
    elif notice.successor is not None:
        parts.append(f"Successor: {notice.successor}.")
    if notice.documentation is not None:
        parts.append(f"See {notice.documentation}")
    return " ".join(parts)


def _isoformat(value: datetime) -> str:
    """The TypeScript client's ``Date.prototype.toISOString`` spelling, so the
    two clients report the same instant the same way.

    Formatted field by field rather than through ``strftime``, whose ``%Y`` is
    delegated to the platform's C library and does **not** zero-pad a year
    below 1000 uniformly: glibc renders year 50 as ``50`` where macOS renders
    ``0050``. Reachable, because :func:`parse_http_date` accepts any year from
    1, and host-dependent warning text is the same defect this module's
    ``Sunset`` parser was rewritten to remove.
    """
    utc = value.astimezone(timezone.utc)
    return (
        f"{utc.year:04d}-{utc.month:02d}-{utc.day:02d}T"
        f"{utc.hour:02d}:{utc.minute:02d}:{utc.second:02d}.{utc.microsecond // 1000:03d}Z"
    )


#: Joins the halves of a warn-once key. Neither a client chain nor a URL can
#: carry a NUL, so no pair of distinct components can collide by concatenation.
_KEY_SEPARATOR = "\0"


def _instant(value: datetime | None) -> str:
    """An instant as integer milliseconds since the epoch.

    The spelling TypeScript's ``Date.prototype.getTime`` produces, so both
    clients draw the same equivalence between two notices -- and, unlike an ISO
    rendering, two ``datetime`` objects naming the same instant in different
    zones compare equal.
    """
    return "" if value is None else str(round(value.timestamp() * 1000))


def _notice_key(notice: Notice) -> str:
    """What makes one notice *distinct* from another, for the warn-once record.

    Derived from the parsed fields rather than the raw header bytes on purpose:
    a requoted ``Link`` or a stray space around ``Deprecation`` reads as the
    same notice and must not warn a second time. The three fields here are the
    ones a caller acts on -- when the deprecation was announced, when the
    operation stops being served, and what replaces it. ``documentation`` is
    deliberately excluded: it points at prose *about* this notice, so the
    platform moving its developer notes to another URL is not news worth
    repeating a warning for.
    """
    successor = "" if notice.successor is None else str(notice.successor)
    return _KEY_SEPARATOR.join((_instant(notice.deprecated_at), _instant(notice.sunset_at), successor))


def _context_url(response: httpx.Response, base_url: str) -> str:
    """The URL the response came from -- the context RFC 8288 resolves relative
    link targets against, which after a redirect is not the URL we asked for.

    ``httpx.Response.url`` reads through to the originating request and raises
    when a response was constructed without one (hand-built responses in tests,
    and any transport that does not attach it). Falling back to the configured
    origin keeps a relative target resolvable instead of losing the notice.
    """
    try:
        return str(response.url) or base_url
    except RuntimeError:
        return base_url


def inspect_deprecation(
    response: httpx.Response,
    *,
    method: str,
    path: str,
    base_url: str,
    seen: set[str],
    operations: tuple[Operation, ...] = OPERATIONS,
    operation: Operation | None = None,
    stacklevel: int = 2,
) -> None:
    """Warn at most once per distinct notice per operation per client instance.

    Called at the single response exit in the kernel, after the retry decision
    has settled, so a response about to be discarded and retried never warns.
    """
    # The hot path: no field, no work.
    notice = parse_deprecation(response.headers, _context_url(response, base_url), base_url)
    if notice is None:
        return

    # The record is keyed on (operation, notice), never on the operation alone.
    # A notice is revised over an operation's life -- `Deprecation` is announced
    # first and a committed `Sunset` lands later -- and keying on the operation
    # would swallow the removal date the caller most needs to hear. The
    # operation half falls back to the substituted path when nothing matched (an
    # escape-hatch call), the same identity the warning text names in that
    # branch.
    operation = operation if operation is not None else match_operation(method, path, operations)
    operation_key = (
        f"{method.lower()} {'/'.join(_segments(path))}" if operation is None else ".".join(operation.chain)
    )
    key = f"{operation_key}{_KEY_SEPARATOR}{_notice_key(notice)}"
    if key in seen or len(seen) >= MAX_TRACKED_NOTICES:
        return
    seen.add(key)

    successor_chain = (
        None if notice.successor is None else match_successor_chain(method, notice.successor, operations)
    )
    subject = f"{method.upper()} {path}" if operation is None else _chain_label(operation.chain)
    warnings.warn(
        format_warning(subject, notice, successor_chain),
        ComposioDeprecationWarning,
        stacklevel=stacklevel,
    )


def inspect_deprecated_inputs(
    *,
    operation: Operation | None,
    query: Mapping[str, Any],
    body: Mapping[str, Any] | None,
    headers: Mapping[str, str] | None = None,
    seen: set[str],
    table: Mapping[tuple[str, ...], tuple[DeprecatedInput, ...]] = DEPRECATED_INPUTS,
    stacklevel: int = 2,
) -> None:
    """The static parameter-level warning: fires when the client sends an
    input the committed spec marks ``deprecated: true``, decided entirely
    from the request the caller is about to send.

    Unlike :func:`inspect_deprecation`, this needs no response -- it runs
    before dispatch, so a connection failure never swallows it. ``operation``
    is ``None`` for an escape-hatch call to a path matching no known
    operation, which cannot be warned about: there is no chain to key
    ``table`` by. ``headers`` is the caller-set headers only (client defaults
    then the per-call override), never the kernel's own accept/user-agent/
    credential headers -- those were never something the caller "sent" in the
    sense this warning reports on.

    One notice per (operation, sorted set of deprecated wire names present)
    per client instance, but every input in that set gets its own
    :func:`warnings.warn` call -- the once-only key only suppresses an
    exact-repeat call, it does not collapse several inputs on one call into a
    single message.
    """
    if operation is None:
        return
    declared = table.get(operation.chain)
    if not declared:
        return

    # `None` reads as "not present" only for query: `_encode_query` drops a
    # `None` query value outright, while an explicit `None` body field is
    # still sent as JSON `null` (`compact` preserves it) -- so filtering body
    # the same way would create the false negative the query filter exists to
    # avoid the false positive of.
    query_keys = frozenset(key for key, value in query.items() if value is not None)
    body_keys = frozenset(body) if body else frozenset()
    header_keys = frozenset() if headers is None else frozenset(name.lower() for name in headers)

    def is_present(item: DeprecatedInput) -> bool:
        if item.location == "query":
            return item.wire in query_keys
        if item.location == "body":
            return item.wire in body_keys
        return item.wire.lower() in header_keys

    present = [item for item in declared if is_present(item)]
    if not present:
        return

    wire_set = ",".join(sorted({item.wire for item in present}))
    key = f"param{_KEY_SEPARATOR}{'.'.join(operation.chain)}{_KEY_SEPARATOR}{wire_set}"
    if key in seen or len(seen) >= MAX_TRACKED_NOTICES:
        return

    subject = _chain_label(operation.chain)
    for item in present:
        # Named by the caller's own keyword, not the wire name: two flat
        # params can disambiguate to `query_show_disabled_1` /
        # `query_show_disabled_2`, and the wire name alone does not say which
        # one the caller passed.
        clause = "" if item.replacement_param is None else f" Use `{item.replacement_param}` instead."
        warnings.warn(
            f"the `{item.param}` parameter of {subject} is deprecated.{clause}",
            ComposioDeprecationWarning,
            stacklevel=stacklevel,
        )
    seen.add(key)
