from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EnvironmentMetadata(_message.Message):
    __slots__ = ("deployment_id", "environment_id", "environment_name")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    environment_id: str
    environment_name: str
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        environment_name: _Optional[str] = ...,
    ) -> None: ...

class ExecutionMetadata(_message.Message):
    __slots__ = ("query_id", "query_hash", "query_timestamp", "execution_duration", "metadata", "additional_metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class AdditionalMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_HASH_FIELD_NUMBER: _ClassVar[int]
    QUERY_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_DURATION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_METADATA_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    query_hash: str
    query_timestamp: _timestamp_pb2.Timestamp
    execution_duration: _duration_pb2.Duration
    metadata: _containers.ScalarMap[str, str]
    additional_metadata: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(
        self,
        query_id: _Optional[str] = ...,
        query_hash: _Optional[str] = ...,
        query_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        execution_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
        additional_metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
    ) -> None: ...
