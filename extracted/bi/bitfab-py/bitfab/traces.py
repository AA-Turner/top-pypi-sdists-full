from __future__ import annotations

import asyncio
import time
from typing import Any, Literal, TypedDict, cast
from urllib.parse import quote

from typing_extensions import NotRequired, TypeGuard

from bitfab.approval import ApprovalFields, Assignee, Justification
from bitfab.assertion_categories import AssertionCategorySummary
from bitfab.http import HttpClient

TraceTargetOccurrence = Literal["first", "last"] | int

TraceAssertionSource = Literal["human", "agent"]
AssertionEvidenceParameterType = Literal[
    "string", "number", "boolean", "object", "array", "null", "unknown"
]
AssertionEvidenceSpanType = Literal[
    "llm", "agent", "function", "guardrail", "handoff", "custom"
]

ASSERTIONS_PATH = "/api/sdk/traces/assertions"
SEARCH_PATH = "/api/sdk/traces/search"


class TraceSearchEntry(TypedDict):
    id: str
    traceFunctionKey: str | None
    name: str | None
    status: Literal["pending", "completed", "failed", "dropped"]
    createdAt: str
    callerMetadata: dict[str, str]


class TraceSearchResult(TypedDict):
    traces: list[TraceSearchEntry]
    nextCursor: str | None
    hasMore: bool


class OutputTarget(TypedDict):
    kind: Literal["output"]


class SpanTarget(TypedDict):
    kind: Literal["span"]
    name: str
    occurrence: NotRequired[TraceTargetOccurrence]


TraceTarget = OutputTarget | SpanTarget


class TraceAssertion(ApprovalFields):
    id: str
    traceId: str
    assertion: str
    humanNote: str | None
    category_assertion_id: str | None
    category: AssertionCategorySummary | None
    passCriteria: str | None
    failCriteria: str | None
    targetOnEvaluatedTrace: TraceTarget | None
    source: TraceAssertionSource
    justification: Justification | None
    categoryJustification: Justification | None
    assignee: Assignee | None
    createdAt: str
    updatedAt: str


class AssertionEvidenceParameter(TypedDict):
    name: str
    type: AssertionEvidenceParameterType


class AssertionLabelEvidence(TypedDict):
    spanId: str
    text: str
    sourceField: str
    spanName: str | None
    parameters: list[AssertionEvidenceParameter]
    spanType: AssertionEvidenceSpanType
    isMocked: bool


class AssertionEvidenceError(RuntimeError):
    pass


def parse_assertion_evidence_response(
    response: dict[str, Any], trace_id: str, assertion_id: str
) -> list[AssertionLabelEvidence]:
    target = f"assertion {assertion_id} on trace {trace_id}"
    if "evidence" not in response:
        raise AssertionEvidenceError(f"The response for {target} carries no evidence")
    evidence = response["evidence"]
    if not isinstance(evidence, list):
        raise AssertionEvidenceError(
            f"Evidence for {target} came back as "
            f"{type(evidence).__name__} instead of a list"
        )
    return [
        _parse_assertion_evidence_item(item, position, target)
        for position, item in enumerate(evidence)
    ]


def _parse_assertion_evidence_item(
    item: object, position: int, target: str
) -> AssertionLabelEvidence:
    if not isinstance(item, dict):
        raise AssertionEvidenceError(
            f"Evidence item {position} for {target} came back as "
            f"{type(item).__name__} instead of an object"
        )
    missing = sorted(AssertionLabelEvidence.__required_keys__ - item.keys())
    if missing:
        raise AssertionEvidenceError(
            f"Evidence item {position} for {target} is missing {', '.join(missing)}"
        )
    span_id = item["spanId"]
    if not isinstance(span_id, str) or not span_id:
        raise AssertionEvidenceError(
            f"Evidence item {position} for {target} has "
            f"{span_id!r} where a spanId belongs"
        )
    return cast(AssertionLabelEvidence, item)


AssertionGenerationStatus = Literal["running", "completed", "failed"]


class AssertionGeneration(TypedDict):
    status: AssertionGenerationStatus
    error: str | None
    assertionIds: list[str]
    startedAt: str
    finishedAt: str | None


class TraceAssertionsResult(TypedDict):
    assertions: list[TraceAssertion]
    inheritedFrom: str | None
    generation: AssertionGeneration | None


class SaveAssertion(TypedDict):
    category_assertion_id: NotRequired[str | None]
    id: NotRequired[str]
    assertion: str
    humanNote: NotRequired[str | None]
    passCriteria: NotRequired[str | None]
    failCriteria: NotRequired[str | None]
    targetOnEvaluatedTrace: NotRequired[TraceTarget | None]
    justification: NotRequired[Justification | None]
    categoryJustification: NotRequired[Justification | None]
    assigneeEmail: NotRequired[str | None]


class TraceAssertionsUpdate(TypedDict):
    traceId: str
    assertions: list[SaveAssertion]


DEFAULT_GENERATION_TIMEOUT_SECONDS = 600.0
GENERATION_POLL_INTERVAL_SECONDS = 2.0


class _GenerateAssertionsResponse(TypedDict):
    generation: AssertionGeneration
    assertions: list[TraceAssertion]


class AssertionGenerationError(RuntimeError):
    def __init__(self, message: str, trace_id: str) -> None:
        super().__init__(message)
        self.trace_id = trace_id


class AssertionGenerationTimeoutError(AssertionGenerationError, TimeoutError):
    pass


def _generation_payload(
    guidance: str | None, category_ids: list[str] | None, regenerate: bool | None
) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if guidance is not None:
        payload["guidance"] = guidance
    if category_ids is not None:
        payload["categoryIds"] = category_ids
    if regenerate is not None:
        payload["regenerate"] = regenerate
    return payload


def _is_generation_finished(
    generation: AssertionGeneration | None, trace_id: str
) -> TypeGuard[AssertionGeneration]:
    if generation is None or generation["status"] == "running":
        return False
    if generation["status"] == "failed":
        raise AssertionGenerationError(
            f"Assertion generation for trace {trace_id} failed: "
            f"{generation['error'] or 'no reason recorded'}. "
            "Pass regenerate=True to try again.",
            trace_id,
        )
    return True


def _drafts_in_generation_order(
    result: TraceAssertionsResult, generation: AssertionGeneration
) -> list[TraceAssertion]:
    by_id = {assertion["id"]: assertion for assertion in result["assertions"]}
    return [by_id[id_] for id_ in generation["assertionIds"] if id_ in by_id]


def _generation_timed_out(
    trace_id: str, timeout: float
) -> AssertionGenerationTimeoutError:
    return AssertionGenerationTimeoutError(
        f"Assertion generation for trace {trace_id} did not finish within "
        f"{timeout:g} seconds. Generation keeps running on Bitfab. Call "
        "get_assertions and read its generation field to check its status.",
        trace_id,
    )


def _trace_assertions_path(trace_id: str, suffix: str = "") -> str:
    return f"/api/sdk/traces/{quote(trace_id, safe='')}/assertions{suffix}"


class TracesClient:
    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def search(
        self,
        *,
        caller_metadata: dict[str, str] | None = None,
        name: str | None = None,
        name_contains: str | None = None,
        trace_function_key: str | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> TraceSearchResult:
        """Search traces by caller metadata or by name.

        ``caller_metadata`` matches up to 10 key/value pairs exactly and every
        pair must match. ``name`` matches the trace name's words in order, so
        "Order ABC" also matches "Order ABC 123", and it matches whole words
        rather than inside a word. ``name_contains`` matches any part of the
        name, including inside a word, and needs at least 3 characters. All
        three are case-insensitive, and supplying more than one narrows the
        search. At least one is required. Pass ``nextCursor`` from the result as
        ``cursor`` to fetch another page.
        """
        payload: dict[str, Any] = {}
        if caller_metadata is not None:
            payload["callerMetadata"] = caller_metadata
        if name is not None:
            payload["name"] = name
        if name_contains is not None:
            payload["nameContains"] = name_contains
        if trace_function_key is not None:
            payload["traceFunctionKey"] = trace_function_key
        if cursor is not None:
            payload["cursor"] = cursor
        if limit is not None:
            payload["limit"] = limit
        result = self._http_client.request(SEARCH_PATH, payload)
        return result  # type: ignore[return-value]

    def get_assertions(self, trace_id: str) -> TraceAssertionsResult:
        result = self._http_client.get(_trace_assertions_path(trace_id))
        return result  # type: ignore[return-value]

    def save_assertions(
        self,
        trace_id: str,
        assertions: list[SaveAssertion],
        source: TraceAssertionSource = "agent",
    ) -> list[TraceAssertion]:
        return self.save_assertions_all(
            [{"traceId": trace_id, "assertions": assertions}], source=source
        )

    def save_assertions_all(
        self,
        updates: list[TraceAssertionsUpdate],
        source: TraceAssertionSource = "agent",
    ) -> list[TraceAssertion]:
        if not updates:
            return []
        payload: dict[str, Any] = {
            "updates": updates,
            "source": source,
        }
        result = self._http_client.request(ASSERTIONS_PATH, payload)
        return result["assertions"]

    def generate_assertions(
        self,
        trace_id: str,
        *,
        guidance: str | None = None,
        category_ids: list[str] | None = None,
        regenerate: bool | None = None,
        timeout: float = DEFAULT_GENERATION_TIMEOUT_SECONDS,
    ) -> list[TraceAssertion]:
        started: _GenerateAssertionsResponse = self._http_client.request(  # type: ignore[assignment]
            _trace_assertions_path(trace_id, "/generate"),
            _generation_payload(guidance, category_ids, regenerate),
        )
        if _is_generation_finished(started["generation"], trace_id):
            return started["assertions"]
        deadline = time.monotonic() + timeout
        while True:
            if time.monotonic() >= deadline:
                raise _generation_timed_out(trace_id, timeout)
            time.sleep(GENERATION_POLL_INTERVAL_SECONDS)
            read = self.get_assertions(trace_id)
            generation = read.get("generation")
            if _is_generation_finished(generation, trace_id):
                return _drafts_in_generation_order(read, generation)

    async def generate_assertions_async(
        self,
        trace_id: str,
        *,
        guidance: str | None = None,
        category_ids: list[str] | None = None,
        regenerate: bool | None = None,
        timeout: float = DEFAULT_GENERATION_TIMEOUT_SECONDS,
    ) -> list[TraceAssertion]:
        started = cast(
            _GenerateAssertionsResponse,
            await asyncio.to_thread(
                self._http_client.request,
                _trace_assertions_path(trace_id, "/generate"),
                _generation_payload(guidance, category_ids, regenerate),
            ),
        )
        if _is_generation_finished(started["generation"], trace_id):
            return started["assertions"]
        deadline = time.monotonic() + timeout
        while True:
            if time.monotonic() >= deadline:
                raise _generation_timed_out(trace_id, timeout)
            await asyncio.sleep(GENERATION_POLL_INTERVAL_SECONDS)
            read = await asyncio.to_thread(self.get_assertions, trace_id)
            generation = read.get("generation")
            if _is_generation_finished(generation, trace_id):
                return _drafts_in_generation_order(read, generation)

    def archive_assertions(self, trace_id: str, assertion_ids: list[str]) -> list[str]:
        result = self._http_client.request(
            _trace_assertions_path(trace_id, "/archive"),
            {"assertionIds": assertion_ids},
        )
        return result["archived"]
