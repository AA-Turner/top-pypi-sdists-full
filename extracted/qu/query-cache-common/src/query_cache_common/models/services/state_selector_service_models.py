from __future__ import annotations

import typing as t
from query_cache_common.decorators import proto_dataclass, proto_enum
from query_cache_common.models import shared_models
from query_cache_common.models.base import BaseSerDeModel, BaseSerDeEnum

from query_cache_protobuf.query_cache.services import state_selector_service_pb2


@proto_dataclass(state_selector_service_pb2.StateSelectorRequest)
class StateSelectorRequest(BaseSerDeModel):
    target: str
    nodes: t.List[shared_models.DbtNodeState]
    selector_criteria: SelectorCriteria
    project_id: t.Optional[str] = None
    project_name: t.Optional[str] = None


@proto_enum(state_selector_service_pb2.SelectorCriteria)
class SelectorCriteria(BaseSerDeEnum):
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


@proto_dataclass(state_selector_service_pb2.StateSelectorResponse)
class StateSelectorResponse(BaseSerDeModel):
    modified_ids: t.List[str]
    new_ids: t.List[str]
    unmodified_ids: t.List[str]
    old_ids: t.List[str]
