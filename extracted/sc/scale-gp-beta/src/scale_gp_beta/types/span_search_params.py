# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo
from .span_type import SpanType
from .span_status import SpanStatus
from .chat.sort_order import SortOrder

__all__ = ["SpanSearchParams", "ExcludedSpan", "Span"]


class SpanSearchParams(TypedDict, total=False):
    allow_partial_results: bool
    """
    Return however many spans fit the server byte budget instead of a 400
    SEARCH_RESULT_TOO_LARGE, reporting the rest through has_more plus next_cursor
    going forward or prev_cursor going back. A search that spends its time budget
    before the page fills also returns what it found, with search_status partial,
    searched_through and a next_cursor that resumes from there. Send it only if the
    client reads has_more, because under it a page shorter than limit no longer
    means the end of the list. Honored by the tracing service on either of its
    storage engines. Accounts still served by the legacy trace store ignore it and
    page by item count, where a short page still means the end of the list.
    """

    ending_before: str

    from_ts: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """The starting (oldest) timestamp in ISO format."""

    limit: int

    sort_by: str

    sort_order: SortOrder

    starting_after: str

    to_ts: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """The ending (most recent) timestamp in ISO format."""

    acp_types: SequenceNotStr[str]
    """Filter by ACP types"""

    agentex_agent_ids: SequenceNotStr[str]
    """Filter by Agentex agent IDs"""

    agentex_agent_names: SequenceNotStr[str]
    """Filter by Agentex agent names"""

    application_variant_ids: SequenceNotStr[str]
    """Filter by application variant IDs"""

    assessment_types: SequenceNotStr[str]
    """Filter to spans that have at least one assessment of these types"""

    excluded_span_ids: SequenceNotStr[str]
    """List of span IDs to exclude from results"""

    excluded_spans: Iterable[ExcludedSpan]
    """List of (trace_id, span_id) identities to exclude from results.

    Unlike excluded_span_ids, a pair never excludes a same-id span from another
    trace. Takes precedence over excluded_span_ids when both are set.
    """

    excluded_trace_ids: SequenceNotStr[str]
    """List of trace IDs to exclude from results"""

    extra_metadata: Dict[str, object]
    """
    Filter on custom metadata: each key must equal its value, or any value of an
    array, and keys are ANDed. On the ClickHouse read path `$or` and `$and` also
    compose nested groups of predicates. On Postgres a `$`-prefixed key is an
    ordinary metadata key matched literally. Array values match element-wise; a
    negative zero inside an array equals zero on Postgres-served accounts and not on
    ClickHouse-served ones.
    """

    group_id: str
    """Filter by group ID"""

    max_duration_ms: int
    """Maximum span duration in milliseconds (inclusive).

    Matched on completed duration, so a span with no end time is never returned:
    fetch it by its own id or in its trace's span list.
    """

    min_duration_ms: int
    """Minimum span duration in milliseconds (inclusive).

    Matched on completed duration, so a span with no end time is not reliably
    returned: fetch it by its own id or in its trace's span list.
    """

    names: SequenceNotStr[str]
    """Filter by trace/span name"""

    obs_span_ids: SequenceNotStr[str]
    """Filter to the business spans that executed in any of these observability spans.

    Each id must be 16 lowercase hex characters. A W3C span id is unique per trace
    only, so combine with obs_trace_ids for exact identity, the same looseness
    span_ids carries versus the spans pair filter. ANDs with obs_trace_ids when both
    are set. Served only by the sgp-traces service, so a request using this filter
    against an account still on the legacy store returns 422 rather than silently
    ignoring it.
    """

    obs_trace_ids: SequenceNotStr[str]
    """
    Filter to the business spans that executed in any of these observability traces
    (the obs-to-business reverse lookup). Each id must be 32 lowercase hex
    characters. Served only by the sgp-traces service, so a request using this
    filter against an account still on the legacy store returns 422 rather than
    silently ignoring it.
    """

    parent_ids: SequenceNotStr[str]
    """Filter to the direct children of any of these parent span IDs"""

    parents_only: bool
    """Only fetch spans that are the top-level (ie. have no parent_id)"""

    search_texts: SequenceNotStr[str]
    """Case-insensitive text search across span name, input, output, and metadata.

    A single-word term of ASCII letters and digits matches as a whole word in input,
    output, and metadata, and as a substring of the name. A term of up to 8 such
    words matches as a contiguous phrase whose words each appear as whole words. All
    other terms (punctuated, non-ASCII, longer) match as substrings, where mid-word
    fragments match and an inflected form such as a plural matches only where it
    appears literally. Wrapping a term in double quotes makes it a phrase: the
    quotes mark the phrase and are never matched, a backslash escapes a quote or a
    backslash inside them, the phrase must appear contiguously inside one searched
    value (the input, the output, or the metadata), a phrase of up to 8 ASCII
    letter-and-digit words additionally requires each of those words to appear there
    as a whole word, and a UUID-shaped phrase stays a text search. A term whose
    quote is unterminated or left unescaped mid-term is matched literally, quotes
    included. Multiple terms are ANDed, and UUID-shaped terms match trace IDs
    instead. A span must match every non-UUID term, and each term may match any of
    the searched fields. UUID matches are ORed onto the text match. Each term must
    be at least 2 characters, measured between the quotes and ignoring outer
    whitespace for a phrase, and at most 10 terms are supported. For exact trace ID
    lookup, use the `trace_ids` filter. The tracing service runs on either
    ClickHouse or Postgres, and the two engines match differently. On Postgres
    deployments the whole-word match uses the simple text-search parser, which keeps
    hosts, e-mail addresses, file paths, version strings, hyphenated compounds, URLs
    and query strings as single words (https://x.com/path?q=1 yields x.com/path?q=1,
    x.com and /path?q=1, never path, q or 1; user@example.com and v1.2.3 are one
    word each; gpt-4o yields the compound and its parts), whereas ClickHouse
    deployments split on every non-alphanumeric ASCII byte. A single word inside
    such a value is a whole-word hit on ClickHouse and a miss on Postgres; the
    substring forms behave identically on both. On Postgres deployments a value over
    80000 bytes has only its first 20000 characters indexed for whole-word matching;
    text past that is reachable only by the substring forms. Words longer than 2047
    bytes are matched as substrings, never as whole words. Case folding of non-ASCII
    text follows the database's LC_CTYPE on Postgres deployments, for the whole-word
    index, the quoted-phrase and substring forms and the word-boundary check alike;
    under a C-locale database non-ASCII letters are not folded. ASCII folds
    everywhere. Input and output behave identically on both engines. A
    substring-form term, or a text-filtered metrics request, reads every row of the
    time window that survives the other filters. A term that matches too many rows
    in the window is refused by the tracing service as QUERY_TOO_BROAD, at an
    engine-specific threshold; whether this API relays that refusal as a 400 or
    answers the page from the legacy trace store follows its read-routing rules, and
    an export's refusal is reported as the failed export's reason on the export
    status, not on the POST. On Postgres deployments each term is counted on its
    own, in every class (whole word, phrase and substring alike) and on every read
    that carries text, and is refused when it alone matches more than 50000 rows of
    the window that survive the other filters, with or without assessment_types. On
    ClickHouse deployments the refusal is the candidate-set cap, a
    deployment-configured limit counted over the matches of all terms together: a
    search page bounds its candidates to the page, so there the cap is a backstop
    rather than a limit a common term meets; metrics and by-span resolve every match
    and can trip it; and an export runs under its own 2000000-row set cap on every
    request, assessment_types included. Accounts still served by the legacy trace
    store match differently until migrated: every term matches as stemmed whole
    words (so inflected forms match and multi-word terms match word-adjacent), only
    input and output are searched, the 2-character minimum is not enforced, quoting
    a term changes nothing (the quotes are stripped and a multi-word term is already
    matched word-adjacent), and characters like `:`, `|`, or `!` inside a term may
    be interpreted as query operators or cause an error.
    """

    span_ids: SequenceNotStr[str]
    """Filter by span IDs"""

    spans: Iterable[Span]
    """Filter by exact (trace_id, span_id) identity.

    Unlike span_ids, a pair never matches a same-id span from another trace. ANDs
    with span_ids when both are set.
    """

    statuses: List[SpanStatus]
    """Filter on span status"""

    trace_ids: SequenceNotStr[str]
    """Filter by trace IDs.

    The combined count of trace_ids, span_ids, excluded_span_ids,
    excluded_trace_ids, parent_ids, and (trace_id, span_id) pairs (each pair
    counting 2) may not exceed 10000. A request over that returns 422.
    """

    types: List[SpanType]

    x_project_id: Annotated[str, PropertyInfo(alias="x-project-id")]


class ExcludedSpan(TypedDict, total=False):
    """
    One span addressed by its full identity, since span ids are only unique within a trace.
    """

    span_id: Required[str]
    """Span ID of the referenced span"""

    trace_id: Required[str]
    """Trace ID of the referenced span"""


class Span(TypedDict, total=False):
    """
    One span addressed by its full identity, since span ids are only unique within a trace.
    """

    span_id: Required[str]
    """Span ID of the referenced span"""

    trace_id: Required[str]
    """Trace ID of the referenced span"""
