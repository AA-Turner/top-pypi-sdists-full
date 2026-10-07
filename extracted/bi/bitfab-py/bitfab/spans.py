from __future__ import annotations

from typing import Any, Literal, TypedDict, cast

from typing_extensions import NotRequired

from bitfab.http import HttpClient

LIST_PATH = "/api/sdk/spans/list"

SpanListType = Literal["llm", "agent", "function", "guardrail", "handoff", "custom"]

SpanListField = Literal["input", "output", "reasoning", "content", "errors", "contexts"]


class ListedSpan(TypedDict):
    id: str
    traceId: str
    parentSpanId: str | None
    name: str | None
    type: str | None
    startedAt: str | None
    endedAt: str | None
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
        fields: list[SpanListField] | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> SpanListResult:
        payload: dict[str, Any] = {"traceId": trace_id}
        if span_type is not None:
            payload["spanType"] = span_type
        if span_name is not None:
            payload["spanName"] = span_name
        if fields is not None:
            payload["fields"] = fields
        if cursor is not None:
            payload["cursor"] = cursor
        if limit is not None:
            payload["limit"] = limit
        return cast(SpanListResult, self._http_client.request(LIST_PATH, payload))
