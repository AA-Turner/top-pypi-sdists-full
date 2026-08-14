from __future__ import annotations

import typing as t

from query_cache_protobuf.query_cache.services import selector_service_pb2

from query_cache_common.decorators import proto_dataclass, proto_enum
from query_cache_common.models.base import BaseSerDeEnum, BaseSerDeModel


@proto_enum(selector_service_pb2.SelectorCriteria)
class SelectorCriteria(BaseSerDeEnum):
    SC_UNSPECIFIED = "SC_UNSPECIFIED"
    MODIFIED = "MODIFIED"
    NEW = "NEW"
    UNMODIFIED = "UNMODIFIED"
    OLD = "OLD"
    BODY = "BODY"
    CONFIGS = "CONFIGS"
    RELATION = "RELATION"
    PERSISTED_DESCRIPTIONS = "PERSISTED_DESCRIPTIONS"
    MACROS = "MACROS"
    CONTRACT = "CONTRACT"


@proto_dataclass(selector_service_pb2.DbtNodeData)
class DbtNodeData(BaseSerDeModel):
    node_unique_id: str
    node_hash: str
    node_body_hash: t.Optional[str] = None
    node_configs_hash: t.Optional[str] = None
    node_persisted_descriptions_hash: t.Optional[str] = None
    node_macros_hash: t.Optional[str] = None
    node_contract_hash: t.Optional[str] = None
    node_database_representation: t.Optional[str] = None


@proto_dataclass(selector_service_pb2.SelectorRequest)
class SelectorRequest(BaseSerDeModel):
    target: str
    project_id: str
    nodes: t.List[DbtNodeData]
    selector_criteria: SelectorCriteria


@proto_dataclass(selector_service_pb2.SelectorResponse)
class SelectorResponse(BaseSerDeModel):
    node_unique_ids: t.List[str]
