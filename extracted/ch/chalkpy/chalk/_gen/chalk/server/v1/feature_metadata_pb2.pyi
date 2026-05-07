from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
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

class DropFeatureVersionsRequest(_message.Message):
    __slots__ = ("namespace", "features")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    features: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, namespace: _Optional[str] = ..., features: _Optional[_Iterable[str]] = ...) -> None: ...

class DropFeatureVersionsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FeatureMigrateTypeRequest(_message.Message):
    __slots__ = ("namespace", "features", "retain_online", "retain_offline")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    RETAIN_ONLINE_FIELD_NUMBER: _ClassVar[int]
    RETAIN_OFFLINE_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    features: _containers.RepeatedScalarFieldContainer[str]
    retain_online: bool
    retain_offline: bool
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        features: _Optional[_Iterable[str]] = ...,
        retain_online: bool = ...,
        retain_offline: bool = ...,
    ) -> None: ...

class FeatureMigrateTypeResponse(_message.Message):
    __slots__ = ("errors",)
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(self, errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...) -> None: ...

class DeleteFeatureObservationsRequest(_message.Message):
    __slots__ = ("namespace", "features", "tags", "primary_keys", "retain_online", "retain_offline")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_KEYS_FIELD_NUMBER: _ClassVar[int]
    RETAIN_ONLINE_FIELD_NUMBER: _ClassVar[int]
    RETAIN_OFFLINE_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    features: _containers.RepeatedScalarFieldContainer[str]
    tags: _containers.RepeatedScalarFieldContainer[str]
    primary_keys: _containers.RepeatedScalarFieldContainer[str]
    retain_online: bool
    retain_offline: bool
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        features: _Optional[_Iterable[str]] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        primary_keys: _Optional[_Iterable[str]] = ...,
        retain_online: bool = ...,
        retain_offline: bool = ...,
    ) -> None: ...

class DeleteFeatureObservationsResponse(_message.Message):
    __slots__ = ("errors",)
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(self, errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...) -> None: ...

class GetIncrementalProgressRequest(_message.Message):
    __slots__ = ("resolver_fqn", "query_name")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    query_name: str
    def __init__(self, resolver_fqn: _Optional[str] = ..., query_name: _Optional[str] = ...) -> None: ...

class GetIncrementalProgressResponse(_message.Message):
    __slots__ = ("environment_id", "resolver_fqn", "query_name", "max_ingested_timestamp", "last_execution_timestamp")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    MAX_INGESTED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LAST_EXECUTION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    resolver_fqn: str
    query_name: str
    max_ingested_timestamp: _timestamp_pb2.Timestamp
    last_execution_timestamp: _timestamp_pb2.Timestamp
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        resolver_fqn: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
        max_ingested_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_execution_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class SetIncrementalProgressRequest(_message.Message):
    __slots__ = ("resolver_fqn", "query_name", "max_ingested_timestamp", "last_execution_timestamp")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    MAX_INGESTED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LAST_EXECUTION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    query_name: str
    max_ingested_timestamp: _timestamp_pb2.Timestamp
    last_execution_timestamp: _timestamp_pb2.Timestamp
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
        max_ingested_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_execution_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class SetIncrementalProgressResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteIncrementalProgressRequest(_message.Message):
    __slots__ = ("resolver_fqn", "query_name")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    query_name: str
    def __init__(self, resolver_fqn: _Optional[str] = ..., query_name: _Optional[str] = ...) -> None: ...

class DeleteIncrementalProgressResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
