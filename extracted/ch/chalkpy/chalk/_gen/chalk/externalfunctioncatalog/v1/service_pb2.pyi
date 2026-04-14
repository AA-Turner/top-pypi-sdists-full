from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.runtime.v1 import remote_python_call_pb2 as _remote_python_call_pb2
from chalk._gen.chalk.scalinggroup.v1 import service_pb2 as _service_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class ExternalFunctionVersion(_message.Message):
    __slots__ = (
        "id",
        "function_name",
        "version",
        "input_arrow_schema",
        "output_arrow_schema",
        "scaling_group_name",
        "scaling_group_revision_id",
        "created_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    INPUT_ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    SCALING_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    SCALING_GROUP_REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    function_name: str
    version: int
    input_arrow_schema: _arrow_pb2.Schema
    output_arrow_schema: _arrow_pb2.Schema
    scaling_group_name: str
    scaling_group_revision_id: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        function_name: _Optional[str] = ...,
        version: _Optional[int] = ...,
        input_arrow_schema: _Optional[_Union[_arrow_pb2.Schema, _Mapping]] = ...,
        output_arrow_schema: _Optional[_Union[_arrow_pb2.Schema, _Mapping]] = ...,
        scaling_group_name: _Optional[str] = ...,
        scaling_group_revision_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class CreateExternalFunctionVersionRequest(_message.Message):
    __slots__ = ("function_name", "input_arrow_schema", "output_arrow_schema", "spec")
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    input_arrow_schema: _arrow_pb2.Schema
    output_arrow_schema: _arrow_pb2.Schema
    spec: _service_pb2.ScalingGroupSpec
    def __init__(
        self,
        function_name: _Optional[str] = ...,
        input_arrow_schema: _Optional[_Union[_arrow_pb2.Schema, _Mapping]] = ...,
        output_arrow_schema: _Optional[_Union[_arrow_pb2.Schema, _Mapping]] = ...,
        spec: _Optional[_Union[_service_pb2.ScalingGroupSpec, _Mapping]] = ...,
    ) -> None: ...

class CreateExternalFunctionVersionResponse(_message.Message):
    __slots__ = ("external_function_version", "scaling_group")
    EXTERNAL_FUNCTION_VERSION_FIELD_NUMBER: _ClassVar[int]
    SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    external_function_version: ExternalFunctionVersion
    scaling_group: _service_pb2.ScalingGroupResponse
    def __init__(
        self,
        external_function_version: _Optional[_Union[ExternalFunctionVersion, _Mapping]] = ...,
        scaling_group: _Optional[_Union[_service_pb2.ScalingGroupResponse, _Mapping]] = ...,
    ) -> None: ...

class ExternalFunctionVersionKey(_message.Message):
    __slots__ = ("function_name", "version")
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    version: int
    def __init__(self, function_name: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...

class GetExternalFunctionVersionRequest(_message.Message):
    __slots__ = ("id", "key", "include_scaling_group")
    ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    id: str
    key: ExternalFunctionVersionKey
    include_scaling_group: bool
    def __init__(
        self,
        id: _Optional[str] = ...,
        key: _Optional[_Union[ExternalFunctionVersionKey, _Mapping]] = ...,
        include_scaling_group: bool = ...,
    ) -> None: ...

class GetExternalFunctionVersionResponse(_message.Message):
    __slots__ = ("external_function_version", "scaling_group")
    EXTERNAL_FUNCTION_VERSION_FIELD_NUMBER: _ClassVar[int]
    SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    external_function_version: ExternalFunctionVersion
    scaling_group: _service_pb2.ScalingGroupResponse
    def __init__(
        self,
        external_function_version: _Optional[_Union[ExternalFunctionVersion, _Mapping]] = ...,
        scaling_group: _Optional[_Union[_service_pb2.ScalingGroupResponse, _Mapping]] = ...,
    ) -> None: ...

class ListExternalFunctionVersionsRequest(_message.Message):
    __slots__ = ("cursor", "limit", "include_scaling_group", "function_name")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    include_scaling_group: bool
    function_name: str
    def __init__(
        self,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        include_scaling_group: bool = ...,
        function_name: _Optional[str] = ...,
    ) -> None: ...

class ListExternalFunctionVersionsEntry(_message.Message):
    __slots__ = ("external_function_version", "scaling_group")
    EXTERNAL_FUNCTION_VERSION_FIELD_NUMBER: _ClassVar[int]
    SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    external_function_version: ExternalFunctionVersion
    scaling_group: _service_pb2.ScalingGroupResponse
    def __init__(
        self,
        external_function_version: _Optional[_Union[ExternalFunctionVersion, _Mapping]] = ...,
        scaling_group: _Optional[_Union[_service_pb2.ScalingGroupResponse, _Mapping]] = ...,
    ) -> None: ...

class ListExternalFunctionVersionsResponse(_message.Message):
    __slots__ = ("entries", "next_cursor")
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[ListExternalFunctionVersionsEntry]
    next_cursor: str
    def __init__(
        self,
        entries: _Optional[_Iterable[_Union[ListExternalFunctionVersionsEntry, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class DeleteExternalFunctionVersionRequest(_message.Message):
    __slots__ = ("id", "key")
    ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    id: str
    key: ExternalFunctionVersionKey
    def __init__(
        self, id: _Optional[str] = ..., key: _Optional[_Union[ExternalFunctionVersionKey, _Mapping]] = ...
    ) -> None: ...

class DeleteExternalFunctionVersionResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ExternalFunctionSummary(_message.Message):
    __slots__ = ("name", "latest_version", "latest_scaling_group_name", "latest_updated_at")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LATEST_VERSION_FIELD_NUMBER: _ClassVar[int]
    LATEST_SCALING_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    LATEST_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    name: str
    latest_version: int
    latest_scaling_group_name: str
    latest_updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        name: _Optional[str] = ...,
        latest_version: _Optional[int] = ...,
        latest_scaling_group_name: _Optional[str] = ...,
        latest_updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListExternalFunctionsRequest(_message.Message):
    __slots__ = ("cursor", "limit")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    def __init__(self, cursor: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class ListExternalFunctionsResponse(_message.Message):
    __slots__ = ("functions", "next_cursor")
    FUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    functions: _containers.RepeatedCompositeFieldContainer[ExternalFunctionSummary]
    next_cursor: str
    def __init__(
        self,
        functions: _Optional[_Iterable[_Union[ExternalFunctionSummary, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class CallExternalFunctionRequest(_message.Message):
    __slots__ = ("function", "remote_call_request")
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    REMOTE_CALL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    function: ExternalFunctionVersionKey
    remote_call_request: _remote_python_call_pb2.CallFunctionRequest
    def __init__(
        self,
        function: _Optional[_Union[ExternalFunctionVersionKey, _Mapping]] = ...,
        remote_call_request: _Optional[_Union[_remote_python_call_pb2.CallFunctionRequest, _Mapping]] = ...,
    ) -> None: ...

class CallExternalFunctionResponse(_message.Message):
    __slots__ = ("remote_call_response",)
    REMOTE_CALL_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    remote_call_response: _remote_python_call_pb2.CallFunctionResponse
    def __init__(
        self, remote_call_response: _Optional[_Union[_remote_python_call_pb2.CallFunctionResponse, _Mapping]] = ...
    ) -> None: ...
