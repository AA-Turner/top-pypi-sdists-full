from __future__ import annotations

import typing as t
from dataclasses import field

from query_cache_common.decorators import proto_dataclass
from query_cache_common.models import shared_models
from query_cache_common.models.services import sql_service_models
from query_cache_common.models.base import BaseSerDeModel
from query_cache_common.models.converters import dict_to_struct, struct_to_dict
from query_cache_protobuf.query_cache.services import execution_service_pb2


@proto_dataclass(execution_service_pb2.ConfirmExecutionRequest)
class ConfirmExecutionRequest(BaseSerDeModel):
    request_id: str
    last_modified_epoch: t.Optional[int]
    failed_to_clone: bool = False
    table_type: t.Optional[str] = None
    execution_results: t.Dict[str, t.Any] = field(
        default_factory=dict,
        metadata={
            "proto_converter": {
                "from_proto": struct_to_dict,
                "to_proto": dict_to_struct,
            }
        },
    )
    execution_runtime_ms: t.Optional[int] = None
    labels: t.Dict[str, str] = field(default_factory=dict)


@proto_dataclass(execution_service_pb2.ConfirmExecutionResponse)
class ConfirmExecutionResponse(BaseSerDeModel):
    request_id: str
    success: bool


@proto_dataclass(execution_service_pb2.SQLExecution)
class SQLExecution(BaseSerDeModel):
    target_table: t.Optional[str]
    dialect: str
    default_catalog: str
    execution_type: shared_models.ModelExecutionType
    sql: str
    tables: t.List[shared_models.TableModifiedInfo] = field(default_factory=list)
    query_dependencies: t.List[shared_models.QueryDependency] = field(default_factory=list)
    semantic_extras: t.Dict[str, str] = field(default_factory=dict)
    labels: t.Dict[str, str] = field(default_factory=dict)
    dbt_node_state: t.Optional[shared_models.DbtNodeState] = None

    @classmethod
    def from_submit_sql_request(
        cls, req: sql_service_models.SubmitEnrichedSQLRequest
    ) -> SQLExecution:
        return cls(
            target_table=req.target_table,
            dialect=req.dialect,
            default_catalog=req.default_catalog,
            execution_type=req.execution_type,
            sql=req.sql,
            tables=req.tables,
            query_dependencies=req.query_dependencies,
            semantic_extras=req.semantic_extras,
            labels=req.labels,
            dbt_node_state=req.dbt_node_state,
        )


@proto_dataclass(execution_service_pb2.ValuesExecution)
class ValuesExecution(BaseSerDeModel):
    target_table: str
    dialect: str
    default_catalog: str
    values_hash: str
    semantic_extras: t.Dict[str, str] = field(default_factory=dict)
    labels: t.Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_submit_values_request(
        cls, req: sql_service_models.SubmitValuesRequest
    ) -> ValuesExecution:
        return cls(
            target_table=req.target_table,
            dialect=req.dialect,
            default_catalog=req.default_catalog,
            values_hash=req.values_hash,
            semantic_extras=req.semantic_extras,
            labels=req.labels,
        )


@proto_dataclass(execution_service_pb2.ExecutionOutcome)
class ExecutionOutcome(BaseSerDeModel):
    last_modified_epoch: t.Optional[int]
    table_type: t.Optional[str]
    execution_results: t.Dict[str, t.Any] = field(
        default_factory=dict,
        metadata={
            "proto_converter": {
                "from_proto": struct_to_dict,
                "to_proto": dict_to_struct,
            }
        },
    )
    execution_runtime_ms: t.Optional[int] = None


@proto_dataclass(execution_service_pb2.ExecutionRecord)
class ExecutionRecord(BaseSerDeModel):
    outcome: ExecutionOutcome
    enriched_sql: t.Optional[SQLExecution] = None
    values: t.Optional[ValuesExecution] = None


@proto_dataclass(execution_service_pb2.RecordExecutionsRequest)
class RecordExecutionsRequest(BaseSerDeModel):
    records: t.List[ExecutionRecord] = field(default_factory=list)


@proto_dataclass(execution_service_pb2.RecordExecutionsResponse)
class RecordExecutionsResponse(BaseSerDeModel):
    records_stored: int = 0
