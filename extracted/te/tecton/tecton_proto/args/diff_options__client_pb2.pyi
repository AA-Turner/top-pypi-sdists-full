from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

CUSTOM_COMPARATOR_AGGREGATION_NAME: CustomComparator
CUSTOM_COMPARATOR_BATCH_SCHEDULE: CustomComparator
CUSTOM_COMPARATOR_DIFF_OVERRIDE_JOIN_KEYS_AS_MAP: CustomComparator
CUSTOM_COMPARATOR_DISPLAY_NOTSET: CustomComparator
CUSTOM_COMPARATOR_ENTITY_JOIN_KEYS: CustomComparator
CUSTOM_COMPARATOR_FEATURE_PARAM_UPGRADE: CustomComparator
CUSTOM_COMPARATOR_FILTERED_SOURCE: CustomComparator
CUSTOM_COMPARATOR_OFFLINE_STORE: CustomComparator
CUSTOM_COMPARATOR_OFFLINE_STORE_LEGACY: CustomComparator
CUSTOM_COMPARATOR_ONLINE_OFFLINE_ENABLED: CustomComparator
CUSTOM_COMPARATOR_OPTION_VALUE_WITH_REDACTION: CustomComparator
CUSTOM_COMPARATOR_PUBLISH_FEATURES: CustomComparator
CUSTOM_COMPARATOR_REQUEST_SOURCE: CustomComparator
CUSTOM_COMPARATOR_STREAM_PROCESSING_MODE: CustomComparator
CUSTOM_COMPARATOR_TIMESTAMP_FIELD: CustomComparator
CUSTOM_COMPARATOR_TIME_WINDOW: CustomComparator
CUSTOM_COMPARATOR_TIME_WINDOW_LEGACY: CustomComparator
CUSTOM_COMPARATOR_UNITY_CATALOG_ACCESS_MODE: CustomComparator
CUSTOM_COMPARATOR_UNSET: CustomComparator
DESCRIPTOR: _descriptor.FileDescriptor
DIFF_OPTIONS_FIELD_NUMBER: _ClassVar[int]
FCO_PROPERTY_RENDERING_TYPE_HIDDEN: FcoPropertyRenderingType
FCO_PROPERTY_RENDERING_TYPE_ONLY_DECLARED: FcoPropertyRenderingType
FCO_PROPERTY_RENDERING_TYPE_PLAIN_TEXT: FcoPropertyRenderingType
FCO_PROPERTY_RENDERING_TYPE_PYTHON: FcoPropertyRenderingType
FCO_PROPERTY_RENDERING_TYPE_REDACTED: FcoPropertyRenderingType
FCO_PROPERTY_RENDERING_TYPE_SQL: FcoPropertyRenderingType
FCO_PROPERTY_RENDERING_TYPE_UNSPECIFIED: FcoPropertyRenderingType
INPLACE: UpdateStrategy
INPLACE_ON_ADD: UpdateStrategy
INPLACE_ON_REMOVE: UpdateStrategy
ONE_WAY_INPLACE_ON_ADD: UpdateStrategy
PASSIVE: UpdateStrategy
RECREATE: UpdateStrategy
RECREATE_UNLESS_SUPPRESSED: UpdateStrategy
RECREATE_UNLESS_SUPPRESSED_INVALIDATE_CHECKPOINTS: UpdateStrategy
RECREATE_UNLESS_SUPPRESSED_RESTART_STREAM: UpdateStrategy
diff_options: _descriptor.FieldDescriptor

class DiffOptions(_message.Message):
    __slots__ = ["custom_comparator", "hide_path", "rename", "rendering_type", "update"]
    CUSTOM_COMPARATOR_FIELD_NUMBER: _ClassVar[int]
    HIDE_PATH_FIELD_NUMBER: _ClassVar[int]
    RENAME_FIELD_NUMBER: _ClassVar[int]
    RENDERING_TYPE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    custom_comparator: CustomComparator
    hide_path: bool
    rename: FieldRenameConfig
    rendering_type: FcoPropertyRenderingType
    update: UpdateStrategy
    def __init__(self, update: _Optional[_Union[UpdateStrategy, str]] = ..., hide_path: bool = ..., rendering_type: _Optional[_Union[FcoPropertyRenderingType, str]] = ..., custom_comparator: _Optional[_Union[CustomComparator, str]] = ..., rename: _Optional[_Union[FieldRenameConfig, _Mapping]] = ...) -> None: ...

class FieldRenameConfig(_message.Message):
    __slots__ = ["cutover_version", "former_name"]
    CUTOVER_VERSION_FIELD_NUMBER: _ClassVar[int]
    FORMER_NAME_FIELD_NUMBER: _ClassVar[int]
    cutover_version: str
    former_name: str
    def __init__(self, former_name: _Optional[str] = ..., cutover_version: _Optional[str] = ...) -> None: ...

class UpdateStrategy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class FcoPropertyRenderingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class CustomComparator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
