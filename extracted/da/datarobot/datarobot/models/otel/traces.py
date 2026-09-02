#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, Iterable, List, Optional

import trafaret as t

from datarobot.models.api_object import APIObject, ServerDataType
from datarobot.models.otel.utils import to_datetime_param
from datarobot.utils.pagination import unpaginate

_trace_tool_trafaret = t.Dict({
    t.Key("name"): t.String(),
    t.Key("call_count"): t.Int(),
}).ignore_extra("*")

_event_trafaret = t.Dict({
    t.Key("name"): t.String(),
    t.Key("attributes"): t.Dict().allow_extra("*"),
}).ignore_extra("*")

_link_trafaret = t.Dict({
    t.Key("span_id"): t.String(),
    t.Key("trace_id"): t.String(),
    t.Key("attributes"): t.Dict().allow_extra("*"),
}).ignore_extra("*")

_resource_trafaret = t.Dict({
    t.Key("attributes"): t.Dict().allow_extra("*"),
}).ignore_extra("*")

_span_trafaret = t.Dict({
    t.Key("span_id"): t.String(),
    t.Key("trace_id"): t.String(),
    t.Key("name"): t.String(),
    t.Key("service_name"): t.String(),
    t.Key("kind"): t.String(),
    t.Key("duration"): t.Float(),
    t.Key("start_time"): t.Float(),
    t.Key("has_permission"): t.Bool(),
    t.Key("attributes"): t.Dict().allow_extra("*"),
    t.Key("events"): t.List(_event_trafaret),
    t.Key("links"): t.List(_link_trafaret),
    t.Key("resource"): _resource_trafaret,
    t.Key("scope"): t.Dict().allow_extra("*"),
    t.Key("parent_span_id", optional=True, default=None): t.Or(t.Null(), t.String()),
    t.Key("status_code", optional=True, default=None): t.Or(t.Null(), t.String()),
    t.Key("status_message", optional=True, default=None): t.Or(t.Null(), t.String()),
    t.Key("prompt", optional=True, default=None): t.Or(t.Null(), t.String()),
    t.Key("completion", optional=True, default=None): t.Or(t.Null(), t.String()),
    t.Key("entity_info", optional=True, default=None): t.Or(t.Null(), t.Dict().allow_extra("*")),
}).ignore_extra("*")


class TraceTool(APIObject):
    """A tool used within an OpenTelemetry trace.

    .. versionadded:: v3.19

    Attributes
    ----------
    name: str
        The name of the tool.
    call_count: int
        The number of times the tool was used in the trace.
    """

    _converter = _trace_tool_trafaret

    def __init__(self, name: str, call_count: int):
        self.name = name
        self.call_count = call_count

    def __repr__(self) -> str:
        return f"TraceTool({self.name}, call_count={self.call_count})"


class OtelTraceSpan(APIObject):
    """A span within an OpenTelemetry trace.

    .. versionadded:: v3.19

    Attributes
    ----------
    span_id: str
        The span ID.
    trace_id: str
        The OTel trace ID.
    name: str
        The span name.
    service_name: str
        The service name of the span.
    kind: str
        The kind of the span.
    duration: float
        The duration of the span.
    start_time: float
        The start time of the span.
    has_permission: bool
        Whether the user has permission to view the span.
    attributes: Dict[str, str]
        The attributes of the span.
    events: List[Dict[str, Any]]
        The list of events on the span.
    links: List[Dict[str, Any]]
        The list of links on the span.
    resource: Dict[str, Any]
        The resource of the span.
    scope: Dict[str, str]
        The scope of the span.
    parent_span_id: Optional[str]
        The parent span ID.
    status_code: Optional[str]
        The status code of the span.
    status_message: Optional[str]
        The status message of the span.
    prompt: Optional[str]
        The prompt of the span.
    completion: Optional[str]
        The completion of the span.
    entity_info: Optional[Dict[str, Any]]
        Entity metadata associated with the span.
    """

    _converter = _span_trafaret

    def __init__(
        self,
        span_id: str,
        trace_id: str,
        name: str,
        service_name: str,
        kind: str,
        duration: float,
        start_time: float,
        has_permission: bool,
        attributes: Dict[str, str],
        events: List[Dict[str, Any]],
        links: List[Dict[str, Any]],
        resource: Dict[str, Any],
        scope: Dict[str, str],
        parent_span_id: Optional[str] = None,
        status_code: Optional[str] = None,
        status_message: Optional[str] = None,
        prompt: Optional[str] = None,
        completion: Optional[str] = None,
        entity_info: Optional[Dict[str, Any]] = None,
    ):
        self.span_id = span_id
        self.trace_id = trace_id
        self.name = name
        self.service_name = service_name
        self.kind = kind
        self.duration = duration
        self.start_time = start_time
        self.has_permission = has_permission
        self.attributes = attributes
        self.events = events
        self.links = links
        self.resource = resource
        self.scope = scope
        self.parent_span_id = parent_span_id
        self.status_code = status_code
        self.status_message = status_message
        self.prompt = prompt
        self.completion = completion
        self.entity_info = entity_info

    def __repr__(self) -> str:
        return f"OtelTraceSpan({self.span_id}, {self.name}, duration={self.duration})"


class OtelTraceDetail(APIObject):
    """A retrieved OpenTelemetry trace with its spans.

    .. versionadded:: v3.19

    Attributes
    ----------
    trace_id: str
        The OTel trace ID.
    duration: Optional[float]
        The duration of the trace.
    root_service_name: Optional[str]
        The root service name.
    root_span_name: Optional[str]
        The root span name.
    span_count: int
        The number of spans in the trace.
    spans: List[OtelTraceSpan]
        The spans that make up the trace.
    metrics: Optional[Dict[str, Any]]
        Metric values produced by DataRobot moderations.
    total_count: Optional[int]
        The total number of spans across all pages.
    """

    _converter = t.Dict({
        t.Key("trace_id"): t.String(),
        t.Key("duration", optional=True): t.Or(t.Null(), t.Float()),
        t.Key("root_service_name", optional=True): t.Or(t.Null(), t.String()),
        t.Key("root_span_name", optional=True): t.Or(t.Null(), t.String()),
        t.Key("span_count"): t.Int(),
        t.Key("spans"): t.List(_span_trafaret),
        t.Key("metrics", optional=True, default=None): t.Or(t.Null(), t.Dict().allow_extra("*")),
        t.Key("total_count", optional=True, default=None): t.Or(t.Null(), t.Int()),
    }).ignore_extra("*")

    def __init__(
        self,
        trace_id: str,
        span_count: int,
        spans: List[OtelTraceSpan],
        duration: Optional[float] = None,
        root_service_name: Optional[str] = None,
        root_span_name: Optional[str] = None,
        metrics: Optional[Dict[str, Any]] = None,
        total_count: Optional[int] = None,
    ):
        self.trace_id = trace_id
        self.duration = duration
        self.root_service_name = root_service_name
        self.root_span_name = root_span_name
        self.span_count = span_count
        self.spans = spans
        self.metrics = metrics
        self.total_count = total_count

    def __repr__(self) -> str:
        return f"OtelTraceDetail({self.trace_id}, {self.root_span_name}, spans={len(self.spans)}/{self.span_count})"

    @classmethod
    def from_server_data(cls, data: ServerDataType, keep_attrs: Optional[Iterable[str]] = None) -> OtelTraceDetail:
        detail = super().from_server_data(data, keep_attrs=keep_attrs)
        if isinstance(data, dict):
            span_data = data.get("spans")
            if isinstance(span_data, list):
                detail.spans = [OtelTraceSpan.from_server_data(item) for item in span_data]
        return detail


class OtelTrace(APIObject):
    """An OpenTelemetry trace.

    .. versionadded:: v3.19

    Attributes
    ----------
    trace_id: str
        The OTel trace ID.
    timestamp: float
        The timestamp of the trace.
    duration: float
        The duration of the trace.
    cost: float
        The cost of the trace.
    root_service_name: str
        The root service name.
    root_span_name: str
        The root span name.
    spans_count: int
        The number of spans in the trace.
    error_spans_count: int
        The number of error spans in the trace.
    prompt: Optional[str]
        The prompt of the trace.
    completion: Optional[str]
        The completion of the trace.
    tools: Optional[List[TraceTool]]
        A list of tool names used in the trace.
    gen_ai_usage_input_tokens: Optional[int]
        The number of input tokens used by GenAI operations in the trace.
    gen_ai_usage_output_tokens: Optional[int]
        The number of output tokens used by GenAI operations in the trace.
    root_user_id: Optional[str]
        The user ID associated with the root span of the trace.
    """

    _path = "otel/{}/{}/traces/"
    _detail_path = "otel/{}/{}/traces/{}/"
    _converter = t.Dict({
        t.Key("trace_id"): t.String(),
        t.Key("timestamp"): t.Float(),
        t.Key("duration"): t.Float(),
        t.Key("cost"): t.Float(),
        t.Key("root_service_name"): t.String(),
        t.Key("root_span_name"): t.String(),
        t.Key("spans_count"): t.Int(),
        t.Key("error_spans_count"): t.Int(),
        t.Key("prompt", optional=True): t.Or(t.Null(), t.String()),
        t.Key("completion", optional=True): t.Or(t.Null(), t.String()),
        t.Key("tools", optional=True, default=None): t.Or(
            t.Null(),
            t.List(_trace_tool_trafaret),
        ),
        t.Key("gen_ai_usage_input_tokens", optional=True, default=None): t.Or(t.Null(), t.Int()),
        t.Key("gen_ai_usage_output_tokens", optional=True, default=None): t.Or(t.Null(), t.Int()),
        t.Key("root_user_id", optional=True, default=None): t.Or(t.Null(), t.String()),
    }).ignore_extra("*")

    def __init__(
        self,
        trace_id: str,
        timestamp: float,
        duration: float,
        cost: float,
        root_service_name: str,
        root_span_name: str,
        spans_count: int,
        error_spans_count: int,
        prompt: Optional[str] = None,
        completion: Optional[str] = None,
        tools: Optional[List[TraceTool]] = None,
        gen_ai_usage_input_tokens: Optional[int] = None,
        gen_ai_usage_output_tokens: Optional[int] = None,
        root_user_id: Optional[str] = None,
    ):
        self.trace_id = trace_id
        self.timestamp = timestamp
        self.duration = duration
        self.cost = cost
        self.root_service_name = root_service_name
        self.root_span_name = root_span_name
        self.spans_count = spans_count
        self.error_spans_count = error_spans_count
        self.prompt = prompt
        self.completion = completion
        self.tools = tools
        self.gen_ai_usage_input_tokens = gen_ai_usage_input_tokens
        self.gen_ai_usage_output_tokens = gen_ai_usage_output_tokens
        self.root_user_id = root_user_id

    def __repr__(self) -> str:
        return f"Trace({self.trace_id}, {self.root_span_name}, spans={self.spans_count}, duration={self.duration})"

    @classmethod
    def from_server_data(cls, data: ServerDataType, keep_attrs: Optional[Iterable[str]] = None) -> OtelTrace:
        trace = super().from_server_data(data, keep_attrs=keep_attrs)
        if isinstance(data, dict):
            tool_data = data.get('tools')
            if isinstance(tool_data, list):
                trace.tools = [TraceTool.from_server_data(item) for item in tool_data]
        return trace

    @classmethod
    def list(
        cls,
        entity_type: str,
        entity_id: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        start_time: Optional[datetime | date | str] = None,
        end_time: Optional[datetime | date | str] = None,
        search_keys: Optional[str | List[str]] = None,
        search_values: Optional[str | List[str]] = None,
        min_span_duration: Optional[int] = None,
        max_span_duration: Optional[int] = None,
        min_trace_duration: Optional[int] = None,
        min_trace_cost: Optional[int] = None,
        max_trace_cost: Optional[int] = None,
        root_span_name: Optional[str | List[str]] = None,
        status: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None,
        trace_type: Optional[str] = None,
        tools: Optional[str | List[str]] = None,
    ) -> List[OtelTrace]:
        """List OpenTelemetry traces for the specified entity.

        .. versionadded:: v3.19

        Parameters
        ----------
        entity_type: str
            The entity type of the traces (e.g., deployment or use_case).
        entity_id: str
            The entity ID of the traces (e.g., `123456`).
        offset: Optional[int]
            Offset for pagination.
        limit: Optional[int]
            Limit for pagination.
        start_time: Optional[datetime | date | str]
            The start time to filter traces by.
        end_time: Optional[datetime | date | str]
            The end time to filter traces by.
        search_keys: Optional[str | List[str]]
            The list of search keys.
        search_values: Optional[str | List[str]]
            The list of search values.
        min_span_duration: Optional[int]
            The minimum duration of the span in nanoseconds.
        max_span_duration: Optional[int]
            The maximum duration of the span in nanoseconds.
        min_trace_duration: Optional[int]
            The minimum duration of the trace in nanoseconds.
        min_trace_cost: Optional[int]
            The minimum cost of the trace.
        max_trace_cost: Optional[int]
            The maximum cost of the trace.
        root_span_name: Optional[str | List[str]]
            Filter by root span name.
        status: Optional[str]
            Filter traces by status. One of ``error`` or ``ok``.
        sort_by: Optional[str]
            Field to sort traces by. One of ``timestamp``, ``duration``, or ``cost``.
        sort_direction: Optional[str]
            Sort direction. One of ``asc`` or ``desc``.
        trace_type: Optional[str]
            Filter traces by trace type. Currently supports only ``gen_ai``.
        tools: Optional[str | List[str]]
            Filter by gen_ai.tool.name.

        Returns
        -------
        traces: List[OtelTrace]
        """
        path = cls._path.format(entity_type, entity_id)
        params = cls._build_query_params(
            start_time=start_time,
            end_time=end_time,
            search_keys=search_keys,
            search_values=search_values,
            min_span_duration=min_span_duration,
            max_span_duration=max_span_duration,
            min_trace_duration=min_trace_duration,
            min_trace_cost=min_trace_cost,
            max_trace_cost=max_trace_cost,
            root_span_name=root_span_name,
            status=status,
            sort_by=sort_by,
            sort_direction=sort_direction,
            trace_type=trace_type,
            tools=tools,
            offset=offset,
            limit=limit,
        )

        if offset is None:
            data = unpaginate(path, params, cls._client)
        else:
            data = cls._client.get(path, params=params or None).json()["data"]
        return [cls.from_server_data(d) for d in data]

    @classmethod
    def get(
        cls,
        entity_type: str,
        entity_id: str,
        trace_id: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> OtelTraceDetail:
        """Retrieve a single OpenTelemetry trace with all of its spans.

        .. versionadded:: v3.19

        Parameters
        ----------
        entity_type: str
            The entity type of the trace (e.g., deployment or use_case).
        entity_id: str
            The entity ID of the trace (e.g., `123456`).
        trace_id: str
            The OTel trace ID.
        offset: Optional[int]
            Offset for span pagination.
        limit: Optional[int]
            Limit for span pagination.

        Returns
        -------
        trace: OtelTraceDetail
        """
        path = cls._detail_path.format(entity_type, entity_id, trace_id)
        params: Dict[str, Any] = {}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit

        response = cls._client.get(path, params=params or None).json()
        if offset is None:
            spans = list(response["spans"])
            while response.get("next"):
                response = cls._client.get(response["next"]).json()
                spans.extend(response["spans"])
            response["spans"] = spans
        return OtelTraceDetail.from_server_data(response)

    @classmethod
    def delete(
        cls,
        entity_type: str,
        entity_id: str,
        start_time: Optional[datetime | date | str] = None,
        end_time: Optional[datetime | date | str] = None,
        search_keys: Optional[str | List[str]] = None,
        search_values: Optional[str | List[str]] = None,
    ) -> None:
        """Delete OpenTelemetry traces for the specified entity.

        .. versionadded:: v3.19

        Parameters
        ----------
        entity_type: str
            The entity type of the traces (e.g., deployment or use_case).
        entity_id: str
            The entity ID of the traces (e.g., `123456`).
        start_time: Optional[datetime | date | str]
            The start time to filter traces by.
        end_time: Optional[datetime | date | str]
            The end time to filter traces by.
        search_keys: Optional[str | List[str]]
            The list of search keys.
        search_values: Optional[str | List[str]]
            The list of search values.

        Returns
        -------
        None
        """
        path = cls._path.format(entity_type, entity_id)
        params = cls._build_query_params(
            start_time=start_time,
            end_time=end_time,
            search_keys=search_keys,
            search_values=search_values,
        )
        cls._client.delete(path, params=params or None)

    @staticmethod
    def _build_query_params(
        start_time: Optional[datetime | date | str] = None,
        end_time: Optional[datetime | date | str] = None,
        search_keys: Optional[str | List[str]] = None,
        search_values: Optional[str | List[str]] = None,
        min_span_duration: Optional[int] = None,
        max_span_duration: Optional[int] = None,
        min_trace_duration: Optional[int] = None,
        min_trace_cost: Optional[int] = None,
        max_trace_cost: Optional[int] = None,
        root_span_name: Optional[str | List[str]] = None,
        status: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None,
        trace_type: Optional[str] = None,
        tools: Optional[str | List[str]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if start_time:
            params["startTime"] = to_datetime_param(start_time)
        if end_time:
            params["endTime"] = to_datetime_param(end_time)
        if search_keys:
            params["searchKeys"] = search_keys
        if search_values:
            params["searchValues"] = search_values
        if min_span_duration is not None:
            params["minSpanDuration"] = min_span_duration
        if max_span_duration is not None:
            params["maxSpanDuration"] = max_span_duration
        if min_trace_duration is not None:
            params["minTraceDuration"] = min_trace_duration
        if min_trace_cost is not None:
            params["minTraceCost"] = min_trace_cost
        if max_trace_cost is not None:
            params["maxTraceCost"] = max_trace_cost
        if root_span_name:
            params["rootSpanName"] = root_span_name
        if status:
            params["status"] = status
        if sort_by:
            params["sortBy"] = sort_by
        if sort_direction:
            params["sortDirection"] = sort_direction
        if trace_type:
            params["traceType"] = trace_type
        if tools:
            params["tools"] = tools
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        return params
