from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.flags.v1 import flags_pb2 as _flags_pb2
from chalk._gen.chalk.server.v1 import model_registry_pb2 as _model_registry_pb2
from chalk._gen.chalk.volume.v2 import volume_pb2 as _volume_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
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

class WeightStreamVersionKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WEIGHT_STREAM_VERSION_KIND_UNSPECIFIED: _ClassVar[WeightStreamVersionKind]
    WEIGHT_STREAM_VERSION_KIND_KEYFRAME: _ClassVar[WeightStreamVersionKind]
    WEIGHT_STREAM_VERSION_KIND_PATCH: _ClassVar[WeightStreamVersionKind]

WEIGHT_STREAM_VERSION_KIND_UNSPECIFIED: WeightStreamVersionKind
WEIGHT_STREAM_VERSION_KIND_KEYFRAME: WeightStreamVersionKind
WEIGHT_STREAM_VERSION_KIND_PATCH: WeightStreamVersionKind

class WeightStream(_message.Message):
    __slots__ = (
        "id",
        "name",
        "base_model",
        "architecture_hash",
        "current_version",
        "pinned_version",
        "created_at",
        "updated_at",
        "base_model_version",
        "volume",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    BASE_MODEL_FIELD_NUMBER: _ClassVar[int]
    ARCHITECTURE_HASH_FIELD_NUMBER: _ClassVar[int]
    CURRENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    PINNED_VERSION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    BASE_MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    base_model: str
    architecture_hash: str
    current_version: int
    pinned_version: int
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    base_model_version: _model_registry_pb2.ModelVersionKey
    volume: _volume_pb2.VolumeRef
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        base_model: _Optional[str] = ...,
        architecture_hash: _Optional[str] = ...,
        current_version: _Optional[int] = ...,
        pinned_version: _Optional[int] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        base_model_version: _Optional[
            _Union[_model_registry_pb2.ModelVersionKey, _Mapping]
        ] = ...,
        volume: _Optional[_Union[_volume_pb2.VolumeRef, _Mapping]] = ...,
    ) -> None: ...

class WeightStreamVersion(_message.Message):
    __slots__ = (
        "weight_stream_id",
        "version",
        "parent_version",
        "kind",
        "volume_version_id",
        "architecture_hash",
        "trainer_step",
        "training_run_id",
        "payload_bytes",
        "changed_element_fraction",
        "created_at",
        "manifest_sha256",
        "weight_schema_sha256",
    )
    WEIGHT_STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    PARENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    VOLUME_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    ARCHITECTURE_HASH_FIELD_NUMBER: _ClassVar[int]
    TRAINER_STEP_FIELD_NUMBER: _ClassVar[int]
    TRAINING_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_BYTES_FIELD_NUMBER: _ClassVar[int]
    CHANGED_ELEMENT_FRACTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_SHA256_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_SCHEMA_SHA256_FIELD_NUMBER: _ClassVar[int]
    weight_stream_id: str
    version: int
    parent_version: int
    kind: WeightStreamVersionKind
    volume_version_id: int
    architecture_hash: str
    trainer_step: int
    training_run_id: str
    payload_bytes: int
    changed_element_fraction: float
    created_at: _timestamp_pb2.Timestamp
    manifest_sha256: str
    weight_schema_sha256: str
    def __init__(
        self,
        weight_stream_id: _Optional[str] = ...,
        version: _Optional[int] = ...,
        parent_version: _Optional[int] = ...,
        kind: _Optional[_Union[WeightStreamVersionKind, str]] = ...,
        volume_version_id: _Optional[int] = ...,
        architecture_hash: _Optional[str] = ...,
        trainer_step: _Optional[int] = ...,
        training_run_id: _Optional[str] = ...,
        payload_bytes: _Optional[int] = ...,
        changed_element_fraction: _Optional[float] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        manifest_sha256: _Optional[str] = ...,
        weight_schema_sha256: _Optional[str] = ...,
    ) -> None: ...

class CreateWeightStreamRequest(_message.Message):
    __slots__ = (
        "name",
        "base_model",
        "architecture_hash",
        "base_model_version",
        "volume",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    BASE_MODEL_FIELD_NUMBER: _ClassVar[int]
    ARCHITECTURE_HASH_FIELD_NUMBER: _ClassVar[int]
    BASE_MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    name: str
    base_model: str
    architecture_hash: str
    base_model_version: _model_registry_pb2.ModelVersionKey
    volume: _volume_pb2.VolumeRef
    def __init__(
        self,
        name: _Optional[str] = ...,
        base_model: _Optional[str] = ...,
        architecture_hash: _Optional[str] = ...,
        base_model_version: _Optional[
            _Union[_model_registry_pb2.ModelVersionKey, _Mapping]
        ] = ...,
        volume: _Optional[_Union[_volume_pb2.VolumeRef, _Mapping]] = ...,
    ) -> None: ...

class CreateWeightStreamResponse(_message.Message):
    __slots__ = ("weight_stream",)
    WEIGHT_STREAM_FIELD_NUMBER: _ClassVar[int]
    weight_stream: WeightStream
    def __init__(
        self, weight_stream: _Optional[_Union[WeightStream, _Mapping]] = ...
    ) -> None: ...

class GetWeightStreamRequest(_message.Message):
    __slots__ = ("weight_stream_id", "weight_stream_name")
    WEIGHT_STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
    weight_stream_id: str
    weight_stream_name: str
    def __init__(
        self,
        weight_stream_id: _Optional[str] = ...,
        weight_stream_name: _Optional[str] = ...,
    ) -> None: ...

class GetWeightStreamResponse(_message.Message):
    __slots__ = ("weight_stream",)
    WEIGHT_STREAM_FIELD_NUMBER: _ClassVar[int]
    weight_stream: WeightStream
    def __init__(
        self, weight_stream: _Optional[_Union[WeightStream, _Mapping]] = ...
    ) -> None: ...

class ListWeightStreamsFilters(_message.Message):
    __slots__ = ("names", "base_models")
    NAMES_FIELD_NUMBER: _ClassVar[int]
    BASE_MODELS_FIELD_NUMBER: _ClassVar[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    base_models: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        names: _Optional[_Iterable[str]] = ...,
        base_models: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class ListWeightStreamsRequest(_message.Message):
    __slots__ = ("filters", "cursor", "limit")
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    filters: ListWeightStreamsFilters
    cursor: str
    limit: int
    def __init__(
        self,
        filters: _Optional[_Union[ListWeightStreamsFilters, _Mapping]] = ...,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class ListWeightStreamsResponse(_message.Message):
    __slots__ = ("weight_streams", "next_cursor")
    WEIGHT_STREAMS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    weight_streams: _containers.RepeatedCompositeFieldContainer[WeightStream]
    next_cursor: str
    def __init__(
        self,
        weight_streams: _Optional[_Iterable[_Union[WeightStream, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class RecordWeightStreamVersionRequest(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: WeightStreamVersion
    def __init__(
        self, version: _Optional[_Union[WeightStreamVersion, _Mapping]] = ...
    ) -> None: ...

class RecordWeightStreamVersionResponse(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: WeightStreamVersion
    def __init__(
        self, version: _Optional[_Union[WeightStreamVersion, _Mapping]] = ...
    ) -> None: ...

class ListWeightStreamVersionsFilters(_message.Message):
    __slots__ = ("kinds", "min_version", "max_version")
    KINDS_FIELD_NUMBER: _ClassVar[int]
    MIN_VERSION_FIELD_NUMBER: _ClassVar[int]
    MAX_VERSION_FIELD_NUMBER: _ClassVar[int]
    kinds: _containers.RepeatedScalarFieldContainer[WeightStreamVersionKind]
    min_version: int
    max_version: int
    def __init__(
        self,
        kinds: _Optional[_Iterable[_Union[WeightStreamVersionKind, str]]] = ...,
        min_version: _Optional[int] = ...,
        max_version: _Optional[int] = ...,
    ) -> None: ...

class ListWeightStreamVersionsRequest(_message.Message):
    __slots__ = ("weight_stream_id", "filters", "cursor", "limit")
    WEIGHT_STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    weight_stream_id: str
    filters: ListWeightStreamVersionsFilters
    cursor: str
    limit: int
    def __init__(
        self,
        weight_stream_id: _Optional[str] = ...,
        filters: _Optional[_Union[ListWeightStreamVersionsFilters, _Mapping]] = ...,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class ListWeightStreamVersionsResponse(_message.Message):
    __slots__ = ("versions", "next_cursor")
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    versions: _containers.RepeatedCompositeFieldContainer[WeightStreamVersion]
    next_cursor: str
    def __init__(
        self,
        versions: _Optional[_Iterable[_Union[WeightStreamVersion, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class SetWeightStreamPinRequest(_message.Message):
    __slots__ = ("weight_stream_id", "version")
    WEIGHT_STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    weight_stream_id: str
    version: int
    def __init__(
        self, weight_stream_id: _Optional[str] = ..., version: _Optional[int] = ...
    ) -> None: ...

class SetWeightStreamPinResponse(_message.Message):
    __slots__ = ("weight_stream",)
    WEIGHT_STREAM_FIELD_NUMBER: _ClassVar[int]
    weight_stream: WeightStream
    def __init__(
        self, weight_stream: _Optional[_Union[WeightStream, _Mapping]] = ...
    ) -> None: ...

class ClearWeightStreamPinRequest(_message.Message):
    __slots__ = ("weight_stream_id",)
    WEIGHT_STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    weight_stream_id: str
    def __init__(self, weight_stream_id: _Optional[str] = ...) -> None: ...

class ClearWeightStreamPinResponse(_message.Message):
    __slots__ = ("weight_stream",)
    WEIGHT_STREAM_FIELD_NUMBER: _ClassVar[int]
    weight_stream: WeightStream
    def __init__(
        self, weight_stream: _Optional[_Union[WeightStream, _Mapping]] = ...
    ) -> None: ...

class PromoteWeightStreamVersionRequest(_message.Message):
    __slots__ = ("weight_stream_id", "version", "model_name", "aliases")
    WEIGHT_STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    ALIASES_FIELD_NUMBER: _ClassVar[int]
    weight_stream_id: str
    version: int
    model_name: str
    aliases: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        weight_stream_id: _Optional[str] = ...,
        version: _Optional[int] = ...,
        model_name: _Optional[str] = ...,
        aliases: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class PromoteWeightStreamVersionResponse(_message.Message):
    __slots__ = ("model_version_id", "model_volume_version_id", "model_version_key")
    MODEL_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_VOLUME_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_KEY_FIELD_NUMBER: _ClassVar[int]
    model_version_id: str
    model_volume_version_id: int
    model_version_key: _model_registry_pb2.ModelVersionKey
    def __init__(
        self,
        model_version_id: _Optional[str] = ...,
        model_volume_version_id: _Optional[int] = ...,
        model_version_key: _Optional[
            _Union[_model_registry_pb2.ModelVersionKey, _Mapping]
        ] = ...,
    ) -> None: ...
