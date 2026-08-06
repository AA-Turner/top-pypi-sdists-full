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
    """Filter on custom metadata key-value pairs"""

    group_id: str
    """Filter by group ID"""

    max_duration_ms: int
    """Maximum span duration in milliseconds (inclusive).

    An in-flight span with no end time has no known duration and is treated as
    unbounded, so it never falls within a maximum and is excluded.
    """

    min_duration_ms: int
    """Minimum span duration in milliseconds (inclusive).

    An in-flight span with no end time has no known duration and is treated as
    unbounded, so it matches every minimum.
    """

    names: SequenceNotStr[str]
    """Filter by trace/span name"""

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
    appears literally. Multiple terms are ANDed, and UUID-shaped terms match trace
    IDs instead. A span must match every non-UUID term, and each term may match any
    of the searched fields. UUID matches are ORed onto the text match. Each term
    must be at least 2 characters, and at most 10 terms are supported. For exact
    trace ID lookup, use the `trace_ids` filter. Accounts still served by the legacy
    trace store match differently until migrated: every term matches as stemmed
    whole words (so inflected forms match and multi-word terms match word-adjacent),
    only input and output are searched, the 2-character minimum is not enforced, and
    characters like `:`, `|`, or `!` inside a term may be interpreted as query
    operators or cause an error.
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
