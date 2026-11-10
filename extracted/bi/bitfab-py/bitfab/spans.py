from __future__ import annotations

from typing import Any, Literal, TypedDict, cast

from typing_extensions import NotRequired

from bitfab.http import HttpClient

LIST_PATH = "/api/sdk/spans/list"

SpanListType = Literal["llm", "agent", "function", "guardrail", "handoff", "custom"]

SpanListField = Literal["input", "output", "reasoning", "content", "errors", "contexts"]

MAX_PAGE_SIZE = 200
MAX_PAGE_SIZE_WITH_FIELDS = 50


class ListedSpan(TypedDict):
    id: str
    traceId: str
    parentSpanId: str | None
    name: str | None
    type: str | None
    startedAt: str | None
    endedAt: str | None
    metadata: dict[str, str]
    input: NotRequired[Any]
    output: NotRequired[Any]
    reasoning: NotRequired[Any]
    content: NotRequired[Any]
    errors: NotRequired[Any]
    contexts: NotRequired[Any]


class SpanListResult(TypedDict):
    spans: list[ListedSpan]
    nextCursor: str | None
    hasMore: bool


class SpansClient:
    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def list(
        self,
        trace_id: str,
        *,
        span_type: SpanListType | None = None,
        span_name: str | None = None,
        metadata: dict[str, str] | None = None,
        fields: list[SpanListField] | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SpanListResult:
        """One page of the spans of one trace, in the order they ran.

        Args:
            trace_id: The trace whose spans to list.
            span_type: Only spans of this type.
            span_name: Only spans with this name.
            metadata: Only spans whose metadata holds every one of these keys
                with these values, matched exactly and case-insensitively. Up
                to 10 keys. Span metadata is set with
                ``get_current_span().set_metadata(...)``.
            fields: Span content to include on each span.
            cursor: The ``nextCursor`` of the previous page.
            limit: Spans per page, 1 to 200, or at most 50 when ``fields`` is
                set, since each span's content is fetched. A larger value is
                refused with a ``requests.HTTPError`` naming the cap. The
                server defaults to 50. Use ``list_all`` to read every span
                without choosing a page size.
        """
        payload: dict[str, Any] = {"traceId": trace_id}
        if span_type is not None:
            payload["spanType"] = span_type
        if span_name is not None:
            payload["spanName"] = span_name
        if metadata is not None:
            payload["metadata"] = metadata
        if fields is not None:
            payload["fields"] = fields
        if cursor is not None:
            payload["cursor"] = cursor
        if limit is not None:
            payload["limit"] = limit
        return cast(SpanListResult, self._http_client.request(LIST_PATH, payload))

    def list_all(
        self,
        trace_id: str,
        *,
        span_type: SpanListType | None = None,
        span_name: str | None = None,
        metadata: dict[str, str] | None = None,
        fields: list[SpanListField] | None = None,
    ) -> list[ListedSpan]:
        """Every span of one trace in the order they ran.

        Fetched page by page until none are left, so no span is missed by
        forgetting to follow ``nextCursor``. Takes the same filters as
        ``list``. Pages hold 200 spans, or 50 when ``fields`` is set. Raises
        ``requests.HTTPError`` with a 404 when the trace is not in your
        organization.
        """
        limit = MAX_PAGE_SIZE_WITH_FIELDS if fields else MAX_PAGE_SIZE
        spans: list[ListedSpan] = []
        cursor: str | None = None
        while True:
            page = self.list(
                trace_id,
                span_type=span_type,
                span_name=span_name,
                metadata=metadata,
                fields=fields,
                cursor=cursor,
                limit=limit,
            )
            spans.extend(page["spans"])
            cursor = page["nextCursor"] if page["hasMore"] else None
            if cursor is None:
                return spans
