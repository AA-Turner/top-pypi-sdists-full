from typing import Dict

import attrs

from tecton_core import schema
from tecton_core.data_types import DataType
from tecton_proto.args import pipeline__client_pb2 as pipeline_pb2


@attrs.frozen
class RequestContext:
    """
    Wrapper around the RequestContext proto object (that is part of the RequestDataSourceNode in the FV pipeline).
    """

    schema: Dict[str, DataType]

    @classmethod
    def from_proto(cls, proto: pipeline_pb2.RequestContext) -> "RequestContext":
        rc_schema = schema.Schema(proto.tecton_schema)
        return RequestContext(schema=rc_schema.to_dict())

    def merge(self, other):
        for field in other.schema:
            if field in self.schema:
                assert self.schema[field] == other.schema[field], f"Mismatched request context field types for {field}"
            else:
                self.schema[field] = other.schema[field]
