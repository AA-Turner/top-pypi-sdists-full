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
from query_cache_protobuf.query_cache.services import clone_service_pb2


@proto_dataclass(clone_service_pb2.TableProperties)
class TableProperties(BaseSerDeModel):
    hours_to_expiration: t.Optional[int] = None
    partition_expiration_days: t.Optional[int] = None


@proto_dataclass(clone_service_pb2.CloneRequest)
class CloneRequest(BaseSerDeModel):
    target_table: str
    dialect: str
    default_catalog: str
    execution_type: shared_models.ModelExecutionType
    clone_source_table: str
    clone_source_last_modified_epoch: t.Optional[int] = None
    labels: t.Dict[str, str] = field(default_factory=dict)
    clone_source_table_type: t.Optional[str] = None
    table_properties: t.Optional[TableProperties] = None
    clone_chain_depth_limit: t.Optional[int] = None


@proto_dataclass(clone_service_pb2.ReadyToCloneResponse)
class ReadyToCloneResponse(BaseSerDeModel):
    request_id: str
    explained_decision: shared_models.ExplainedDecision
    transformed_nodes_by_query: TransformedNodesByQuery = transformed_nodes_by_query_field()
    clone_sqls: t.List[str] = field(default_factory=list)
    clone_source: str = ""
    clone_target: str = ""
    last_modified_query: str = ""  # Deprecated
    clone_required_last_modified_epoch: t.Optional[int] = None
    clone_execution_results: t.Dict[str, t.Any] = field(
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


@proto_dataclass(clone_service_pb2.UnableToCloneResponse)
class UnableToCloneResponse(BaseSerDeModel):
    explained_decision: shared_models.ExplainedDecision
    clone_source: str = ""
    clone_target: str = ""


@proto_dataclass(clone_service_pb2.UntrackableCloneResponse)
class UntrackableCloneResponse(BaseSerDeModel):
    explained_decision: shared_models.ExplainedDecision
    transformed_nodes_by_query: TransformedNodesByQuery = transformed_nodes_by_query_field()
    clone_sqls: t.List[str] = field(default_factory=list)
    clone_source: str = ""
    clone_target: str = ""
