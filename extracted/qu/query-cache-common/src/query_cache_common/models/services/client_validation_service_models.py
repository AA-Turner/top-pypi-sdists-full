from __future__ import annotations

from query_cache_protobuf.query_cache.services import client_validation_service_pb2

from query_cache_common.decorators import proto_dataclass
from query_cache_common.models.base import BaseSerDeModel


@proto_dataclass(client_validation_service_pb2.ValidateClientVersionRequest)
class ValidateClientVersionRequest(BaseSerDeModel):
    dbt_run_cache_version: str


@proto_dataclass(client_validation_service_pb2.ValidateClientVersionResponse)
class ValidateClientVersionResponse(BaseSerDeModel):
    is_supported: bool
