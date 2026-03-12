from buf.validate import validate_pb2 as _validate_pb2
from nominal.streaming_connection_service.v1 import opc_ua_pb2 as _opc_ua_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StreamingConnectionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STREAMING_CONNECTION_STATUS_UNSPECIFIED: _ClassVar[StreamingConnectionStatus]
    CONNECTED: _ClassVar[StreamingConnectionStatus]
    DISCONNECTED: _ClassVar[StreamingConnectionStatus]
STREAMING_CONNECTION_STATUS_UNSPECIFIED: StreamingConnectionStatus
CONNECTED: StreamingConnectionStatus
DISCONNECTED: StreamingConnectionStatus

class StreamingConnectionDetails(_message.Message):
    __slots__ = ("opc_ua",)
    OPC_UA_FIELD_NUMBER: _ClassVar[int]
    opc_ua: _opc_ua_pb2.OpcUaConnectionDetails
    def __init__(self, opc_ua: _Optional[_Union[_opc_ua_pb2.OpcUaConnectionDetails, _Mapping]] = ...) -> None: ...

class StreamingConnectionDetailsSecret(_message.Message):
    __slots__ = ("opc_ua",)
    OPC_UA_FIELD_NUMBER: _ClassVar[int]
    opc_ua: _opc_ua_pb2.OpcUaConnectionDetailsSecret
    def __init__(self, opc_ua: _Optional[_Union[_opc_ua_pb2.OpcUaConnectionDetailsSecret, _Mapping]] = ...) -> None: ...

class StreamingScrapingConfig(_message.Message):
    __slots__ = ("opc_ua",)
    OPC_UA_FIELD_NUMBER: _ClassVar[int]
    opc_ua: _opc_ua_pb2.OpcUaScrapingConfig
    def __init__(self, opc_ua: _Optional[_Union[_opc_ua_pb2.OpcUaScrapingConfig, _Mapping]] = ...) -> None: ...
