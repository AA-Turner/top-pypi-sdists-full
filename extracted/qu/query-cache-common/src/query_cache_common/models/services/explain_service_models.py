from __future__ import annotations

import typing as t
from dataclasses import field

from query_cache_protobuf.query_cache.services import explain_service_pb2

from query_cache_common.decorators import proto_dataclass, proto_enum
from query_cache_common.models.base import BaseSerDeEnum, BaseSerDeModel
from query_cache_common.models.shared_models import SubmitSQLResultType


@proto_enum(explain_service_pb2.ExplainMarker)
class ExplainMarker(BaseSerDeEnum):
    _UNSUPPORTED = "_UNSUPPORTED"

    EM_UNSPECIFIED = "EM_UNSPECIFIED"
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    INFO = "INFO"


@proto_enum(explain_service_pb2.ExplainBadge)
class ExplainBadge(BaseSerDeEnum):
    _UNSUPPORTED = "_UNSUPPORTED"
    EB_UNSPECIFIED = "EB_UNSPECIFIED"
    FRESH = "FRESH"
    WITHIN_TOLERANCE = "WITHIN_TOLERANCE"
    OUTDATED = "OUTDATED"
    NODE_QUERY_CHANGED = "NODE_QUERY_CHANGED"
    NODE_QUERY_UNCHANGED = "NODE_QUERY_UNCHANGED"
    UPSTREAM_QUERY_CHANGED = "UPSTREAM_QUERY_CHANGED"
    UPSTREAM_QUERY_UNCHANGED = "UPSTREAM_QUERY_UNCHANGED"
    TARGET_TABLE_EXISTS = "TARGET_TABLE_EXISTS"


@proto_dataclass(explain_service_pb2.ExplainLine)
class ExplainLine(BaseSerDeModel):
    text: str
    marker: t.Optional[ExplainMarker] = None
    badge: t.Optional[ExplainBadge] = None
    children: t.List[ExplainLine] = field(default_factory=list)


@proto_dataclass(explain_service_pb2.ExplainMessageEntry)
class ExplainMessageEntry(BaseSerDeModel):
    execution_decision_id: str
    decision: SubmitSQLResultType
    decision_description: str
    explain_lines: t.List[ExplainLine] = field(default_factory=list)


@proto_dataclass(explain_service_pb2.GetExplainMessagesRequest)
class GetExplainMessagesRequest(BaseSerDeModel):
    execution_decision_ids: t.List[str]


@proto_dataclass(explain_service_pb2.GetExplainMessagesResponse)
class GetExplainMessagesResponse(BaseSerDeModel):
    messages: t.List[ExplainMessageEntry]

    @property
    def by_id(self) -> t.Dict[str, ExplainMessageEntry]:
        return {m.execution_decision_id: m for m in self.messages}
