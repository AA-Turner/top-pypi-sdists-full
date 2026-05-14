from chalk._gen.chalk.common.v1 import online_query_pb2 as _online_query_pb2
from chalk._gen.chalk.engine.v1 import plan_pb2 as _plan_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPlanRequest(_message.Message):
    __slots__ = ("online_query_request",)
    ONLINE_QUERY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    online_query_request: _online_query_pb2.OnlineQueryRequest
    def __init__(
        self, online_query_request: _Optional[_Union[_online_query_pb2.OnlineQueryRequest, _Mapping]] = ...
    ) -> None: ...

class GetPlanResponse(_message.Message):
    __slots__ = ("plan",)
    PLAN_FIELD_NUMBER: _ClassVar[int]
    plan: _plan_pb2.Plan
    def __init__(self, plan: _Optional[_Union[_plan_pb2.Plan, _Mapping]] = ...) -> None: ...

class ExecuteQueryRequest(_message.Message):
    __slots__ = ("online_query_request",)
    ONLINE_QUERY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    online_query_request: _online_query_pb2.OnlineQueryRequest
    def __init__(
        self, online_query_request: _Optional[_Union[_online_query_pb2.OnlineQueryRequest, _Mapping]] = ...
    ) -> None: ...

class ExecuteQueryResponse(_message.Message):
    __slots__ = ("online_query_response",)
    ONLINE_QUERY_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    online_query_response: _online_query_pb2.OnlineQueryResponse
    def __init__(
        self, online_query_response: _Optional[_Union[_online_query_pb2.OnlineQueryResponse, _Mapping]] = ...
    ) -> None: ...
