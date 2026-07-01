from __future__ import annotations

from dataclasses import field


import typing as t
from datetime import timedelta

from query_cache_common.decorators import proto_dataclass, proto_enum
from query_cache_common.models.base import BaseSerDeModel, BaseSerDeEnum
from query_cache_common.models.converters import (
    struct_to_dict,
    dict_to_struct,
    duration_to_timedelta,
    timedelta_to_duration,
)
from query_cache_protobuf.query_cache.services import client_telemetry_service_pb2


@proto_dataclass(client_telemetry_service_pb2.SessionStartRequest)
class SessionStartRequest(BaseSerDeModel):
    dbt_run_cache_version: str
    dbt_version: str
    sqlglot_version: str
    config: t.Dict[str, t.Any] = field(
        metadata={
            "proto_converter": {
                "from_proto": struct_to_dict,
                "to_proto": dict_to_struct,
            }
        }
    )


@proto_dataclass(client_telemetry_service_pb2.SessionStartResponse)
class SessionStartResponse(BaseSerDeModel):
    success: bool
    session_id: str


@proto_dataclass(client_telemetry_service_pb2.ClientPrepareEnrichedSQLRequest)
class ClientPrepareEnrichedSQLRequest(BaseSerDeModel):
    request_id: str
    duration: float
    target_table_fqn: t.Optional[str]
    num_dependencies: t.Optional[int] = None
    num_view_dependencies: t.Optional[int] = None
    error_type: t.Optional[str] = None
    view_traversal_duration_ms: t.Optional[int] = None
    last_modified_duration_ms: t.Optional[int] = None
    labels: t.Dict[str, str] = field(default_factory=dict)


@proto_enum(client_telemetry_service_pb2.SessionEndRequest.ClientResult)
class ClientResult(BaseSerDeEnum):
    _UNSUPPORTED = "_UNSUPPORTED"

    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    CANCELLED = "CANCELLED"


@proto_dataclass(client_telemetry_service_pb2.SessionEndRequest)
class SessionEndRequest(BaseSerDeModel):
    result: ClientResult
    result_description: str
    session_duration: timedelta = field(
        metadata={
            "proto_converter": {
                "from_proto": duration_to_timedelta,
                "to_proto": timedelta_to_duration,
            }
        }
    )
    metrics: t.Dict[str, t.Any] = field(
        metadata={
            "proto_converter": {
                "from_proto": struct_to_dict,
                "to_proto": dict_to_struct,
            }
        }
    )


@proto_dataclass(client_telemetry_service_pb2.ClientTelemetryEvent)
class ClientTelemetryEvent(BaseSerDeModel):
    event_order: t.Optional[int] = None

    enriched_sql_prepared: t.Optional[ClientPrepareEnrichedSQLRequest] = None
    session_start: t.Optional[SessionStartRequest] = None
    session_end: t.Optional[SessionEndRequest] = None


@proto_dataclass(client_telemetry_service_pb2.SubmitTelemetryBatchRequest)
class SubmitTelemetryBatchRequest(BaseSerDeModel):
    events: t.List[ClientTelemetryEvent]


@proto_dataclass(client_telemetry_service_pb2.SubmitTelemetryBatchResponse)
class SubmitTelemetryBatchResponse(BaseSerDeModel):
    success: bool
