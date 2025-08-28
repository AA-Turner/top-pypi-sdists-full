import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from nominal.streaming_connection_service.v1 import opc_ua_pb2 as _opc_ua_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StreamingConnectionErrorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STREAMING_CONNECTION_ERROR_TYPE_UNSPECIFIED: _ClassVar[StreamingConnectionErrorType]
    STREAMING_CONNECTION_ERROR_TYPE_CONNECTION_NOT_FOUND: _ClassVar[StreamingConnectionErrorType]
    STREAMING_CONNECTION_ERROR_TYPE_WORKFLOW_NOT_FOUND: _ClassVar[StreamingConnectionErrorType]
    STREAMING_CONNECTION_ERROR_TYPE_STREAMING_CONNECTION_ALREADY_RUNNING: _ClassVar[StreamingConnectionErrorType]

class StreamingConnectionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STREAMING_CONNECTION_STATUS_UNSPECIFIED: _ClassVar[StreamingConnectionStatus]
    CONNECTED: _ClassVar[StreamingConnectionStatus]
    DISCONNECTED: _ClassVar[StreamingConnectionStatus]
STREAMING_CONNECTION_ERROR_TYPE_UNSPECIFIED: StreamingConnectionErrorType
STREAMING_CONNECTION_ERROR_TYPE_CONNECTION_NOT_FOUND: StreamingConnectionErrorType
STREAMING_CONNECTION_ERROR_TYPE_WORKFLOW_NOT_FOUND: StreamingConnectionErrorType
STREAMING_CONNECTION_ERROR_TYPE_STREAMING_CONNECTION_ALREADY_RUNNING: StreamingConnectionErrorType
STREAMING_CONNECTION_STATUS_UNSPECIFIED: StreamingConnectionStatus
CONNECTED: StreamingConnectionStatus
DISCONNECTED: StreamingConnectionStatus

class CreateStreamingConnectionRequest(_message.Message):
    __slots__ = ("name", "description", "connection_details", "workspace_rid")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_DETAILS_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    connection_details: StreamingConnectionDetails
    workspace_rid: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., connection_details: _Optional[_Union[StreamingConnectionDetails, _Mapping]] = ..., workspace_rid: _Optional[str] = ...) -> None: ...

class CreateStreamingConnectionResponse(_message.Message):
    __slots__ = ("streaming_connection_rid",)
    STREAMING_CONNECTION_RID_FIELD_NUMBER: _ClassVar[int]
    streaming_connection_rid: str
    def __init__(self, streaming_connection_rid: _Optional[str] = ...) -> None: ...

class StopStreamResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class StartStreamResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class StreamingConnection(_message.Message):
    __slots__ = ("streaming_connection_rid", "name", "description", "connection_details", "status", "created_at")
    STREAMING_CONNECTION_RID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_DETAILS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    streaming_connection_rid: str
    name: str
    description: str
    connection_details: StreamingConnectionDetails
    status: StreamingConnectionStatus
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, streaming_connection_rid: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., connection_details: _Optional[_Union[StreamingConnectionDetails, _Mapping]] = ..., status: _Optional[_Union[StreamingConnectionStatus, str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class StreamingConnectionDetails(_message.Message):
    __slots__ = ("opc_ua",)
    OPC_UA_FIELD_NUMBER: _ClassVar[int]
    opc_ua: _opc_ua_pb2.OpcUaConnectionDetails
    def __init__(self, opc_ua: _Optional[_Union[_opc_ua_pb2.OpcUaConnectionDetails, _Mapping]] = ...) -> None: ...

class StreamingScrapingConfig(_message.Message):
    __slots__ = ("opc_ua",)
    OPC_UA_FIELD_NUMBER: _ClassVar[int]
    opc_ua: _opc_ua_pb2.OpcUaScrapingConfig
    def __init__(self, opc_ua: _Optional[_Union[_opc_ua_pb2.OpcUaScrapingConfig, _Mapping]] = ...) -> None: ...

class GetStreamingConnectionRequest(_message.Message):
    __slots__ = ("streaming_connection_rid",)
    STREAMING_CONNECTION_RID_FIELD_NUMBER: _ClassVar[int]
    streaming_connection_rid: str
    def __init__(self, streaming_connection_rid: _Optional[str] = ...) -> None: ...

class GetStreamingConnectionResponse(_message.Message):
    __slots__ = ("streaming_connection",)
    STREAMING_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    streaming_connection: StreamingConnection
    def __init__(self, streaming_connection: _Optional[_Union[StreamingConnection, _Mapping]] = ...) -> None: ...

class ListStreamingConnectionsRequest(_message.Message):
    __slots__ = ("workspace_rids",)
    WORKSPACE_RIDS_FIELD_NUMBER: _ClassVar[int]
    workspace_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, workspace_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class ListStreamingConnectionsResponse(_message.Message):
    __slots__ = ("streaming_connections",)
    STREAMING_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    streaming_connections: _containers.RepeatedCompositeFieldContainer[StreamingConnection]
    def __init__(self, streaming_connections: _Optional[_Iterable[_Union[StreamingConnection, _Mapping]]] = ...) -> None: ...

class UpdateStreamingConnectionStatusRequest(_message.Message):
    __slots__ = ("streaming_connection_rid", "status")
    STREAMING_CONNECTION_RID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    streaming_connection_rid: str
    status: StreamingConnectionStatus
    def __init__(self, streaming_connection_rid: _Optional[str] = ..., status: _Optional[_Union[StreamingConnectionStatus, str]] = ...) -> None: ...

class UpdateStreamingConnectionStatusResponse(_message.Message):
    __slots__ = ("streaming_connection",)
    STREAMING_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    streaming_connection: StreamingConnection
    def __init__(self, streaming_connection: _Optional[_Union[StreamingConnection, _Mapping]] = ...) -> None: ...

class StartStreamRequest(_message.Message):
    __slots__ = ("streaming_connection_rid", "scraping_config", "target_dataset_rid")
    STREAMING_CONNECTION_RID_FIELD_NUMBER: _ClassVar[int]
    SCRAPING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    TARGET_DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    streaming_connection_rid: str
    scraping_config: StreamingScrapingConfig
    target_dataset_rid: str
    def __init__(self, streaming_connection_rid: _Optional[str] = ..., scraping_config: _Optional[_Union[StreamingScrapingConfig, _Mapping]] = ..., target_dataset_rid: _Optional[str] = ...) -> None: ...

class StopStreamRequest(_message.Message):
    __slots__ = ("streaming_connection_rid",)
    STREAMING_CONNECTION_RID_FIELD_NUMBER: _ClassVar[int]
    streaming_connection_rid: str
    def __init__(self, streaming_connection_rid: _Optional[str] = ...) -> None: ...
