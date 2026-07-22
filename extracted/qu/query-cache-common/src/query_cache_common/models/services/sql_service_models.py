from __future__ import annotations

import typing as t
from dataclasses import field

from query_cache_common.decorators import proto_dataclass
from query_cache_common.models import shared_models
from query_cache_common.models._typing import TransformedNodesByQuery
from query_cache_common.models.base import BaseSerDeModel
from query_cache_common.models.converters import dict_to_struct, struct_to_dict
from query_cache_common.models.fields import (
    transformed_nodes_by_query_field,
)
from query_cache_common.models.services.clone_service_models import TableProperties
from query_cache_protobuf.query_cache.services import sql_service_pb2


@proto_dataclass(sql_service_pb2.SubmitValuesRequest)
class SubmitValuesRequest(BaseSerDeModel):
    target_table: str
    dialect: str
    default_catalog: str
    values_hash: str
    semantic_extras: t.Dict[str, str]
    last_modified_epoch: t.Optional[int]
    labels: t.Dict[str, str] = field(default_factory=dict)
    clone_time_travel_limit: t.Optional[int] = None
    clone_table_properties: t.Optional[TableProperties] = None
    clone_chain_depth_limit: t.Optional[int] = None


@proto_dataclass(sql_service_pb2.SubmitEnrichedSQLRequest)
class SubmitEnrichedSQLRequest(BaseSerDeModel):
    target_table: t.Optional[str]
    dialect: str
    default_catalog: str
    execution_type: shared_models.ModelExecutionType
    sql: str
    tables: t.List[shared_models.TableModifiedInfo] = field(default_factory=list)
    query_dependencies: t.List[shared_models.QueryDependency] = field(default_factory=list)
    semantic_extras: t.Dict[str, str] = field(default_factory=dict)
    freshness_tolerance_seconds: int = 0
    lenient_dependencies: t.Set[str] = field(default_factory=set)
    tolerate_nondeterminism: bool = False
    labels: t.Dict[str, str] = field(default_factory=dict)
    clone_time_travel_limit: t.Optional[int] = None
    clone_table_properties: t.Optional[TableProperties] = None
    stale_upstream_policy: shared_models.StaleUpstreamPolicy = shared_models.StaleUpstreamPolicy.ANY
    clone_chain_depth_limit: t.Optional[int] = None
    dbt_node_state: t.Optional[shared_models.DbtNodeState] = None
    default_schema: t.Optional[str] = None
    compare_unrendered_code: bool = False


@proto_dataclass(sql_service_pb2.QueryHashMatchMetadataInfo)
class QueryHashMatchMetadataInfo(BaseSerDeModel):
    semantic_hash_match: bool
    data_hash_match: bool


@proto_dataclass(sql_service_pb2.ReadyToExecuteResponse)
class ReadyToExecuteResponse(BaseSerDeModel):
    request_id: str
    explained_decision: shared_models.ExplainedDecision
    transformed_nodes_by_query: TransformedNodesByQuery = transformed_nodes_by_query_field()
    query_hash_metadata_info: t.Optional[QueryHashMatchMetadataInfo] = None
    last_modified_query: str = ""  # Deprecated
    execution_decision_id: t.Optional[str] = ""


@proto_dataclass(sql_service_pb2.ReadyToExecuteUntrackedResponse)
class ReadyToExecuteUntrackedResponse(BaseSerDeModel):
    pass


@proto_dataclass(sql_service_pb2.UndecidedResponse)
class UndecidedResponse(BaseSerDeModel):
    pass


@proto_dataclass(sql_service_pb2.SkipExecutionResponse)
class SkipExecutionResponse(BaseSerDeModel):
    explained_decision: shared_models.ExplainedDecision
    transformed_nodes_by_query: TransformedNodesByQuery = transformed_nodes_by_query_field()
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
    execution_decision_id: t.Optional[str] = ""
