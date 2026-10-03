"""Native models for trace projection contract v1; fixtures are checked against JS."""

from __future__ import annotations

import json
import re
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    field_validator,
    model_validator,
)
from pydantic.alias_generators import to_camel


def _integer(value: Any) -> Any:
    return int(value) if isinstance(value, float) and value.is_integer() else value


Integer = Annotated[StrictInt, BeforeValidator(_integer)]


def _true(value: Any) -> bool:
    if value is not True:
        raise ValueError("Expected true")
    return value


TrueLiteral = Annotated[Literal[True], BeforeValidator(_true)]


class TraceModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore",
        allow_inf_nan=False,
    )

    def wire(self) -> dict[str, Any]:
        return self.model_dump(mode="json", by_alias=True, exclude_unset=True)


class Annotation(TraceModel):
    type: Literal["url", "file", "event", "user", "signal"]
    text: StrictStr = None
    id: StrictStr = None
    url: StrictStr = None
    start_index: Integer = None
    end_index: Integer = None


class TextContent(TraceModel):
    type: Literal["text"]
    text: StrictStr
    annotations: list[Annotation] = None


class JsonContent(TraceModel):
    type: Literal["json"]
    value: Any = None
    raw: StrictStr | None


class MediaContent(TraceModel):
    type: Literal["image", "file"]
    mime_type: StrictStr = None
    url: StrictStr = None
    file_id: StrictStr = None
    name: StrictStr = None


class ReferenceContent(TraceModel):
    type: Literal["reference"]
    label: StrictStr
    ref_type: Literal["stored_tool_result", "external"]
    href: StrictStr = None
    metadata: dict[str, Any] = None


Content = Annotated[
    TextContent | JsonContent | MediaContent | ReferenceContent,
    Field(discriminator="type"),
]


class Payload(TraceModel):
    kind: Literal["empty", "text", "json", "reference"]
    raw: StrictStr | None
    truncated: StrictBool
    size_chars: Integer | None


class EntrySource(TraceModel):
    adapter: StrictStr
    confidence: Literal["high", "medium", "low"]
    span_ids: list[StrictStr]
    parent_span_ids: list[StrictStr]
    attribute_keys: list[StrictStr]


class Entry(TraceModel):
    id: StrictStr
    order: Integer
    start_ms: Integer | None
    end_ms: Integer | None
    source: EntrySource


class SystemEntry(Entry):
    type: Literal["system"]
    role: Literal["system", "developer"]
    content: TextContent
    collapsed: TrueLiteral
    token_estimate: Integer | None


class UserEntry(Entry):
    type: Literal["user_message"]
    role: Literal["user"]
    content: list[Content]


class AssistantEntry(Entry):
    type: Literal["assistant_text"]
    role: Literal["assistant"]
    content: list[Content]
    format: Literal["markdown", "text"]
    final: StrictBool


class ReasoningEntry(Entry):
    type: Literal["reasoning"]
    content: TextContent
    format: Literal["text"]
    visibility: Literal["collapsed", "expanded"]
    captured_as: Literal[
        "provider_reasoning", "reasoning_summary", "thinking", "unknown"
    ]


class ToolEntry(Entry):
    type: Literal["tool_call"]
    call_id: StrictStr | None
    name: StrictStr
    status: Literal["pending", "completed", "error", "unknown"]
    duration_ms: Integer | None
    input: Payload
    output: Payload | None
    error: Payload | None


class UnknownEntry(Entry):
    type: Literal["unknown_span"]
    span_type: StrictStr | None
    name: StrictStr
    hidden_by_default: TrueLiteral


class SubAgentEntry(Entry):
    type: Literal["sub_agent"]
    root_span_id: StrictStr
    name: StrictStr
    span_ids: list[StrictStr]
    tool_count: Integer
    llm_count: Integer
    duration_ms: Integer | None
    input_preview: StrictStr | None
    output_preview: StrictStr | None
    status: Literal["ok", "error", "unknown"]
    model: StrictStr | None
    total_input_tokens: Integer | None
    total_output_tokens: Integer | None


class DetachedEntry(Entry):
    type: Literal["detached_sub_agent"]
    root_span_id: StrictStr
    name: StrictStr
    duration_ms: Integer | None
    input_preview: StrictStr | None
    output_preview: StrictStr | None
    status: Literal["ok", "error", "unknown"]
    child_event_id: StrictStr


class HandoffEntry(Entry):
    type: Literal["agent_handoff"]
    from_agent: StrictStr
    to_agent: StrictStr
    reason: StrictStr | None


RichEntry = Annotated[
    SystemEntry
    | UserEntry
    | AssistantEntry
    | ReasoningEntry
    | ToolEntry
    | UnknownEntry
    | SubAgentEntry
    | DetachedEntry
    | HandoffEntry,
    Field(discriminator="type"),
]


class SpanSummary(TraceModel):
    span_id: StrictStr
    parent_span_id: StrictStr | None
    trace_id: StrictStr
    name: StrictStr
    span_type: StrictStr | None
    status: StrictStr | None
    start_ms: Integer | None
    end_ms: Integer | None
    duration_ms: Integer | None
    model: StrictStr | None
    provider: StrictStr | None
    rendered: StrictBool


class Warning(TraceModel):
    code: Literal[
        "no_spans",
        "missing_llm_input",
        "missing_llm_output",
        "duplicate_output_suppressed",
        "tool_call_unmatched",
        "payload_truncated",
        "unknown_span_shape",
    ]
    message: StrictStr
    span_ids: list[StrictStr] = None


class Diagnostics(TraceModel):
    extraction_version: Literal["rich-interaction/1"]
    warnings: list[Warning]
    unrendered_span_count: Integer


class InteractionStats(TraceModel):
    agent_count: Integer
    llm_call_count: Integer
    tool_call_count: Integer
    error_count: Integer
    agent_names: list[StrictStr]


class RichInteraction(TraceModel):
    schema_version: Literal["2026-05-20"]
    event_id: StrictStr
    trace_ids: list[StrictStr]
    root_span_ids: list[StrictStr]
    status: Literal["complete", "partial", "missing_spans"]
    started_at: StrictStr | None
    ended_at: StrictStr | None
    duration_ms: Integer | None
    stats: InteractionStats
    entries: list[RichEntry]
    spans: list[SpanSummary]
    diagnostics: Diagnostics


def _string(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, dict):
        return "[object Object]"
    if isinstance(value, list):
        return ",".join("" if item is None else _string(item) for item in value)
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def _number(value: Any) -> float:
    # The shared event schema deliberately coerces category metadata like JS Number.
    if value is None:
        return 0
    if isinstance(value, list):
        value = _string(value)
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return 0
        if value.lower().startswith(("0x", "0b", "0o")):
            return int(value, 0)
    return float(value)


CoercedNumber = Annotated[float, BeforeValidator(_number)]


class LensInfo(TraceModel):
    lens_id: CoercedNumber
    source_id: StrictStr
    source: StrictStr = None
    category_id: CoercedNumber


class CategoryLog(TraceModel):
    lens_id: CoercedNumber
    category_id: Annotated[str, BeforeValidator(_string)]
    action: Literal["add_category", "remove_category", "skip_category"]


class Attachment(TraceModel):
    model_config = ConfigDict(alias_generator=None)
    attachment_id: StrictStr
    attachment_type: Literal["text", "image", "iframe"] = "text"
    value: StrictStr
    name: StrictStr = ""


def _invalid_json_constant(value: str) -> Any:
    raise ValueError(f"Invalid JSON constant: {value}")


class Signal(TraceModel):
    id: StrictStr = None
    name: StrictStr
    timestamp: StrictStr
    attachment_id: StrictStr = None
    properties: Any
    signal_type: StrictStr = None
    score: StrictFloat = None

    @field_validator("properties", mode="before")
    @classmethod
    def properties_json(cls, value: Any) -> Any:
        if isinstance(value, str):
            return json.loads(value, parse_constant=_invalid_json_constant)
        if not isinstance(value, dict):
            raise ValueError("Signal properties must be an object or JSON string")
        return value


class ErrorSpan(TraceModel):
    model_config = ConfigDict(alias_generator=None)
    span_id: StrictStr = None
    started_at: StrictStr = None
    status: StrictStr = None
    duration_ms: CoercedNumber = None
    span_type: StrictStr = None
    span_name: StrictStr = None
    output_payload: Any = None


class AIData(TraceModel):
    input: StrictStr | None = None
    output: StrictStr | None = None
    model: StrictStr | None = None
    convo_id: StrictStr | None = None


class TraceEvent(TraceModel):
    id: StrictStr
    database_id: StrictStr = Field(alias="_raindropDatabaseId")
    project_id: StrictStr = None
    name: StrictStr
    timestamp: StrictStr
    received_at: StrictStr
    user_id: StrictStr
    ai_data: AIData
    properties: dict[str, Any] | None
    custom_event_id: StrictStr | None = None
    occurrences_in_window: StrictFloat = None
    lens_info: list[LensInfo] = None
    topics: list[StrictStr] = None
    categories: list[tuple[StrictStr, StrictStr | None, CoercedNumber | None]] = None
    category_log: list[CategoryLog] = None
    input_attachments: list[Attachment]
    output_attachments: list[Attachment]
    signals: list[Signal] = None
    error_spans: list[ErrorSpan] = None
    regex_signals: list[StrictStr] = None
    tool_calls: list[Any] = None
    tool_call_names: list[StrictStr] = None
    rich_interaction: RichInteraction | None = None
    ai_output_words: StrictFloat = Field(default=None, alias="_ai_output_words")
    ai_input_words: StrictFloat = Field(default=None, alias="_ai_input_words")
    user_traits: dict[str, Any] | None = None
    feature_flags: dict[str, StrictStr] | None = None
    user_created_at: StrictStr | None = None
    user_plan: StrictStr | None = None
    user_last_plan: StrictStr | None = None
    user_plan_change_ts: StrictStr | None = None
    is_pending: StrictBool = None

    @model_validator(mode="before")
    @classmethod
    def attachments(cls, raw: Any) -> Any:
        if not isinstance(raw, dict):
            return raw
        value = dict(raw)
        for key in ("inputAttachments", "outputAttachments"):
            items = value.get(key, [])
            if not isinstance(items, list):
                raise ValueError("Attachments must be an array")
            parsed = []
            for item in items:
                if isinstance(item, str):
                    try:
                        item = Attachment.model_validate(json.loads(item)).model_dump()
                    except ValueError:
                        continue
                else:
                    item = Attachment.model_validate(item).model_dump()
                parsed.append(item)
            value[key] = parsed
        return value


class CaseExpectation(TraceModel):
    model_config = ConfigDict(extra="forbid")
    description: Annotated[StrictStr, Field(min_length=1, max_length=10000)]
    basis: Literal["human", "policy", "code", "inferred"] = None
    reference: Annotated[StrictStr, Field(min_length=1, max_length=2000)] = None

    @field_validator("description", "reference", mode="before")
    @classmethod
    def trim(cls, value: Any) -> Any:
        return value.strip() if isinstance(value, str) else value


class CaseContext(TraceModel):
    case_id: Annotated[StrictStr, Field(min_length=1, max_length=512)]
    expectation: CaseExpectation = None

    @field_validator("case_id")
    @classmethod
    def unpadded_id(cls, value: str) -> str:
        if value != value.strip():
            raise ValueError("Case id cannot have surrounding whitespace")
        return value


class Trace(TraceModel):
    origin: Literal["production", "dataset", "simulation", "replay"]
    event: TraceEvent
    entries: list[RichEntry]
    case_context: CaseContext = None


def _nanoseconds(value: Any) -> str:
    if (
        not isinstance(value, str)
        or re.fullmatch(r"[0-9]{1,20}", value) is None
        or int(value) > 2**64 - 1
    ):
        raise ValueError("Nanoseconds must be a UInt64 decimal string")
    return value


Nanoseconds = Annotated[str, BeforeValidator(_nanoseconds)]


class SnapshotSpan(TraceModel):
    model_config = ConfigDict(alias_generator=None, extra="forbid")
    org_public_id: StrictStr
    project_id: Annotated[StrictStr, Field(min_length=1)]
    user_id: StrictStr
    convo_id: StrictStr
    event_id: Annotated[StrictStr, Field(min_length=1)]
    custom_event_id: StrictStr
    trace_id: Annotated[StrictStr, Field(pattern=r"^[0-9a-f]{32}$")]
    span_id: Annotated[StrictStr, Field(pattern=r"^[0-9a-f]{16}$")]
    parent_span_id: Annotated[StrictStr, Field(pattern=r"^([0-9a-f]{16})?$")]
    span_type: Literal[
        "INTERNAL", "LLM_GENERATION", "LLM_GENERATION_STREAM", "TOOL_CALL"
    ]
    span_name: StrictStr
    status: Literal["UNSET", "OK", "ERROR"]
    input_payload: StrictStr
    output_payload: StrictStr
    start_unix_ns: Nanoseconds
    end_unix_ns: Nanoseconds
    duration_ns: Nanoseconds
    timestamp: Annotated[StrictStr, Field(min_length=1)]
    end_timestamp: Annotated[StrictStr, Field(min_length=1)]
    inserted_at: Annotated[StrictStr, Field(min_length=1)] = Field(alias="_inserted_at")
    input_tokens: StrictFloat
    output_tokens: StrictFloat
    model: StrictStr
    provider: StrictStr
    attributes_string: dict[str, StrictStr]
    attributes_num: dict[str, StrictFloat]

    @field_validator("org_public_id")
    @classmethod
    def uuid_string(cls, value: str) -> str:
        if not re.fullmatch(
            r"[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}", value
        ):
            raise ValueError("Expected a hyphenated UUID")
        return value


class Snapshot(TraceModel):
    model_config = ConfigDict(extra="forbid")
    event: TraceEvent
    spans: Annotated[list[SnapshotSpan], Field(min_length=1, max_length=500)]

    @model_validator(mode="after")
    def identities_and_times(self) -> Snapshot:
        ids = {span.span_id for span in self.spans}
        if (
            len(ids) != len(self.spans)
            or len({span.trace_id for span in self.spans}) != 1
        ):
            raise ValueError("Snapshot needs unique spans from one trace")
        parents = {span.span_id: span.parent_span_id for span in self.spans}
        for span in self.spans:
            if span.event_id != self.event.database_id:
                raise ValueError("Span event identity does not match captured event")
            if int(span.start_unix_ns) == 0 or int(span.end_unix_ns) < int(
                span.start_unix_ns
            ):
                raise ValueError("Captured span must end at or after its nonzero start")
            seen = set()
            current = span.span_id
            while current:
                if current in seen:
                    raise ValueError("Captured span parents cannot contain a cycle")
                seen.add(current)
                current = parents.get(current, "")
        return self
