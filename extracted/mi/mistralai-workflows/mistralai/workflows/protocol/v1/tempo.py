from enum import StrEnum
from typing import List, Union

from pydantic import BaseModel, Field


class TempoTraceAttributeStringValue(BaseModel):
    stringValue: str = Field(description="The string value of the attribute")


class TempoTraceAttributeIntValue(BaseModel):
    intValue: str = Field(description="The integer value of the attribute")


class TempoTraceAttributeBoolValue(BaseModel):
    boolValue: bool = Field(description="The boolean value of the attribute")


class TempoTraceAttributeArrayValue(BaseModel):
    arrayValue: "TempoTraceAttributeArrayContainer" = Field(description="The array value of the attribute")


class TempoTraceAttributeArrayContainer(BaseModel):
    values: List["TempoTraceAttributeArrayElement"] = Field(default_factory=list, description="The values of the array")


class TempoTraceAttributeArrayElement(BaseModel):
    stringValue: str | None = Field(default=None, description="A string element in the array")
    intValue: str | None = Field(default=None, description="An integer element in the array")
    boolValue: bool | None = Field(default=None, description="A boolean element in the array")


TempoTraceAttributeValue = Union[
    TempoTraceAttributeStringValue,
    TempoTraceAttributeIntValue,
    TempoTraceAttributeBoolValue,
    TempoTraceAttributeArrayValue,
]


class TempoTraceAttribute(BaseModel):
    key: str = Field(description="The key of the attribute")
    value: TempoTraceAttributeValue = Field(description="The value of the attribute")


class TempoTraceResource(BaseModel):
    attributes: List[TempoTraceAttribute] = Field(default_factory=list, description="The attributes of the resource")


class TempoTraceScope(BaseModel):
    name: str = Field(description="The name of the span")


class TempoTraceScopeKind(StrEnum):
    SPAN_KIND_INTERNAL = "SPAN_KIND_INTERNAL"
    SPAN_KIND_SERVER = "SPAN_KIND_SERVER"
    SPAN_KIND_CLIENT = "SPAN_KIND_CLIENT"


class TempoTraceEvent(BaseModel):
    name: str = Field(description="The name of the event")
    timeUnixNano: str = Field(description="The time of the event in Unix nano")
    attributes: List[TempoTraceAttribute] = Field(default_factory=list, description="The attributes of the event")


class TempoTraceSpan(BaseModel):
    traceId: str = Field(description="The trace ID of the scope")
    spanId: str = Field(description="The span ID of the scope")
    parentSpanId: str | None = Field(default=None, description="The parent span ID of the scope")
    name: str = Field(description="The name of the scope")
    kind: TempoTraceScopeKind = Field(description="The kind of the scope")
    startTimeUnixNano: str = Field(description="The start time of the scope in Unix nano")
    endTimeUnixNano: str = Field(description="The end time of the scope in Unix nano")
    attributes: List[TempoTraceAttribute] = Field(default_factory=list, description="The attributes of the scope")
    events: List[TempoTraceEvent] = Field(default_factory=list, description="The events of the scope")


class TempoTraceScopeSpan(BaseModel):
    scope: TempoTraceScope = Field(description="The scope of the span")
    spans: List[TempoTraceSpan] = Field(default_factory=list, description="The spans of the scope")


class TempoTraceBatch(BaseModel):
    resource: TempoTraceResource = Field(description="The resource of the batch")
    scopeSpans: List[TempoTraceScopeSpan] = Field(default_factory=list, description="The spans of the scope")


class TempoGetTraceResponse(BaseModel):
    """Trace response in OpenTelemetry format.

    This is the unified trace format used across all trace providers (Tempo, ClickHouse, etc.).
    Regardless of the underlying backend, all trace data is normalized to this Tempo-compatible
    OpenTelemetry format to ensure consistency in the API response structure.
    """

    batches: List[TempoTraceBatch] = Field(default_factory=list, description="The batches of the trace")
