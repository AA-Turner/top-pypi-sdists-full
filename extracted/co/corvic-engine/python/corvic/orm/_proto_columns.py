import copy
from typing import TypeVar

import google.protobuf.message
import sqlalchemy as sa

_ProtoMessage = TypeVar("_ProtoMessage", bound=google.protobuf.message.Message)


class ProtoMessageDecorator(sa.types.TypeDecorator[_ProtoMessage]):
    impl = sa.LargeBinary

    cache_ok = True

    def __init__(self, message: _ProtoMessage):
        super().__init__()
        self._message = message

    def process_bind_param(
        self, value: _ProtoMessage | None, dialect: sa.Dialect
    ) -> bytes | None:
        if value is None:
            return None
        return value.SerializeToString()

    def process_result_value(
        self, value: bytes | None, dialect: sa.Dialect
    ) -> _ProtoMessage | None:
        if value is None:
            return None
        result = copy.deepcopy(self._message)
        result.ParseFromString(value)
        return result
