from __future__ import annotations

import typing as t
from dataclasses import field

from query_cache_protobuf.query_cache.services import sql_analysis_service_pb2

from query_cache_common.decorators import proto_dataclass
from query_cache_common.models.base import BaseSerDeModel


@proto_dataclass(sql_analysis_service_pb2.ExtractTableReferencesRequest)
class ExtractTableReferencesRequest(BaseSerDeModel):
    dialect: str
    sqls: t.List[str] = field(default_factory=list)


@proto_dataclass(sql_analysis_service_pb2.TableReference)
class TableReference(BaseSerDeModel):
    parts: t.List[str] = field(default_factory=list)
    fqn: str = ""


@proto_dataclass(sql_analysis_service_pb2.SqlTableReferences)
class SqlTableReferences(BaseSerDeModel):
    parsed: bool
    references: t.List[TableReference] = field(default_factory=list)


@proto_dataclass(sql_analysis_service_pb2.ExtractTableReferencesResponse)
class ExtractTableReferencesResponse(BaseSerDeModel):
    results: t.List[SqlTableReferences] = field(default_factory=list)
