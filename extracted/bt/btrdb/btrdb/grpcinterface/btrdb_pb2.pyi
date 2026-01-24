from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MergePolicy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NEVER: _ClassVar[MergePolicy]
    EQUAL: _ClassVar[MergePolicy]
    RETAIN: _ClassVar[MergePolicy]
    REPLACE: _ClassVar[MergePolicy]

class SubscriptionUpdateOp(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ADD_UUIDS: _ClassVar[SubscriptionUpdateOp]
    REMOVE_UUIDS: _ClassVar[SubscriptionUpdateOp]
NEVER: MergePolicy
EQUAL: MergePolicy
RETAIN: MergePolicy
REPLACE: MergePolicy
ADD_UUIDS: SubscriptionUpdateOp
REMOVE_UUIDS: SubscriptionUpdateOp

class RawValuesParams(_message.Message):
    __slots__ = ("uuid", "start", "end", "versionMajor")
    UUID_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    start: int
    end: int
    versionMajor: int
    def __init__(self, uuid: _Optional[bytes] = ..., start: _Optional[int] = ..., end: _Optional[int] = ..., versionMajor: _Optional[int] = ...) -> None: ...

class RawValuesResponse(_message.Message):
    __slots__ = ("stat", "versionMajor", "versionMinor", "values")
    STAT_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    VERSIONMINOR_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    versionMajor: int
    versionMinor: int
    values: _containers.RepeatedCompositeFieldContainer[RawPoint]
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., versionMajor: _Optional[int] = ..., versionMinor: _Optional[int] = ..., values: _Optional[_Iterable[_Union[RawPoint, _Mapping]]] = ...) -> None: ...

class ArrowRawValuesParams(_message.Message):
    __slots__ = ("uuid", "start", "end", "versionMajor", "templateBytes")
    UUID_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    TEMPLATEBYTES_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    start: int
    end: int
    versionMajor: int
    templateBytes: bytes
    def __init__(self, uuid: _Optional[bytes] = ..., start: _Optional[int] = ..., end: _Optional[int] = ..., versionMajor: _Optional[int] = ..., templateBytes: _Optional[bytes] = ...) -> None: ...

class ArrowRawValuesResponse(_message.Message):
    __slots__ = ("stat", "versionMajor", "versionMinor", "arrowBytes")
    STAT_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    VERSIONMINOR_FIELD_NUMBER: _ClassVar[int]
    ARROWBYTES_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    versionMajor: int
    versionMinor: int
    arrowBytes: bytes
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., versionMajor: _Optional[int] = ..., versionMinor: _Optional[int] = ..., arrowBytes: _Optional[bytes] = ...) -> None: ...

class ArrowMultiValuesParams(_message.Message):
    __slots__ = ("uuid", "versionMajor", "start", "end", "snapPeriodNs", "templateBytes")
    UUID_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    SNAPPERIODNS_FIELD_NUMBER: _ClassVar[int]
    TEMPLATEBYTES_FIELD_NUMBER: _ClassVar[int]
    uuid: _containers.RepeatedScalarFieldContainer[bytes]
    versionMajor: _containers.RepeatedScalarFieldContainer[int]
    start: int
    end: int
    snapPeriodNs: int
    templateBytes: bytes
    def __init__(self, uuid: _Optional[_Iterable[bytes]] = ..., versionMajor: _Optional[_Iterable[int]] = ..., start: _Optional[int] = ..., end: _Optional[int] = ..., snapPeriodNs: _Optional[int] = ..., templateBytes: _Optional[bytes] = ...) -> None: ...

class ArrowMultiValuesResponse(_message.Message):
    __slots__ = ("stat", "arrowBytes")
    STAT_FIELD_NUMBER: _ClassVar[int]
    ARROWBYTES_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    arrowBytes: bytes
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., arrowBytes: _Optional[bytes] = ...) -> None: ...

class RawPointVec(_message.Message):
    __slots__ = ("time", "value")
    TIME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    time: int
    value: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, time: _Optional[int] = ..., value: _Optional[_Iterable[float]] = ...) -> None: ...

class AlignedWindowsParams(_message.Message):
    __slots__ = ("uuid", "start", "end", "versionMajor", "pointWidth")
    UUID_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    POINTWIDTH_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    start: int
    end: int
    versionMajor: int
    pointWidth: int
    def __init__(self, uuid: _Optional[bytes] = ..., start: _Optional[int] = ..., end: _Optional[int] = ..., versionMajor: _Optional[int] = ..., pointWidth: _Optional[int] = ...) -> None: ...

class AlignedWindowsResponse(_message.Message):
    __slots__ = ("stat", "versionMajor", "versionMinor", "values")
    STAT_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    VERSIONMINOR_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    versionMajor: int
    versionMinor: int
    values: _containers.RepeatedCompositeFieldContainer[StatPoint]
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., versionMajor: _Optional[int] = ..., versionMinor: _Optional[int] = ..., values: _Optional[_Iterable[_Union[StatPoint, _Mapping]]] = ...) -> None: ...

class ArrowAlignedWindowsResponse(_message.Message):
    __slots__ = ("stat", "versionMajor", "versionMinor", "arrowBytes")
    STAT_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    VERSIONMINOR_FIELD_NUMBER: _ClassVar[int]
    ARROWBYTES_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    versionMajor: int
    versionMinor: int
    arrowBytes: bytes
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., versionMajor: _Optional[int] = ..., versionMinor: _Optional[int] = ..., arrowBytes: _Optional[bytes] = ...) -> None: ...

class WindowsParams(_message.Message):
    __slots__ = ("uuid", "start", "end", "versionMajor", "width", "depth")
    UUID_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    start: int
    end: int
    versionMajor: int
    width: int
    depth: int
    def __init__(self, uuid: _Optional[bytes] = ..., start: _Optional[int] = ..., end: _Optional[int] = ..., versionMajor: _Optional[int] = ..., width: _Optional[int] = ..., depth: _Optional[int] = ...) -> None: ...

class WindowsResponse(_message.Message):
    __slots__ = ("stat", "versionMajor", "versionMinor", "values")
    STAT_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    VERSIONMINOR_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    versionMajor: int
    versionMinor: int
    values: _containers.RepeatedCompositeFieldContainer[StatPoint]
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., versionMajor: _Optional[int] = ..., versionMinor: _Optional[int] = ..., values: _Optional[_Iterable[_Union[StatPoint, _Mapping]]] = ...) -> None: ...

class ArrowWindowsResponse(_message.Message):
    __slots__ = ("stat", "versionMajor", "versionMinor", "arrowBytes")
    STAT_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    VERSIONMINOR_FIELD_NUMBER: _ClassVar[int]
    ARROWBYTES_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    versionMajor: int
    versionMinor: int
    arrowBytes: bytes
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., versionMajor: _Optional[int] = ..., versionMinor: _Optional[int] = ..., arrowBytes: _Optional[bytes] = ...) -> None: ...

class StreamInfoParams(_message.Message):
    __slots__ = ("uuid", "omitVersion", "omitDescriptor", "role")
    UUID_FIELD_NUMBER: _ClassVar[int]
    OMITVERSION_FIELD_NUMBER: _ClassVar[int]
    OMITDESCRIPTOR_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    omitVersion: bool
    omitDescriptor: bool
    role: Role
    def __init__(self, uuid: _Optional[bytes] = ..., omitVersion: bool = ..., omitDescriptor: bool = ..., role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class StreamInfoResponse(_message.Message):
    __slots__ = ("stat", "versionMajor", "versionMinor", "descriptor")
    STAT_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    VERSIONMINOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    versionMajor: int
    versionMinor: int
    descriptor: StreamDescriptor
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., versionMajor: _Optional[int] = ..., versionMinor: _Optional[int] = ..., descriptor: _Optional[_Union[StreamDescriptor, _Mapping]] = ...) -> None: ...

class StreamDescriptor(_message.Message):
    __slots__ = ("uuid", "collection", "tags", "annotations", "propertyVersion")
    UUID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    PROPERTYVERSION_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    collection: str
    tags: _containers.RepeatedCompositeFieldContainer[KeyOptValue]
    annotations: _containers.RepeatedCompositeFieldContainer[KeyOptValue]
    propertyVersion: int
    def __init__(self, uuid: _Optional[bytes] = ..., collection: _Optional[str] = ..., tags: _Optional[_Iterable[_Union[KeyOptValue, _Mapping]]] = ..., annotations: _Optional[_Iterable[_Union[KeyOptValue, _Mapping]]] = ..., propertyVersion: _Optional[int] = ...) -> None: ...

class SetStreamAnnotationsParams(_message.Message):
    __slots__ = ("uuid", "expectedPropertyVersion", "changes", "removals")
    UUID_FIELD_NUMBER: _ClassVar[int]
    EXPECTEDPROPERTYVERSION_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    REMOVALS_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    expectedPropertyVersion: int
    changes: _containers.RepeatedCompositeFieldContainer[KeyOptValue]
    removals: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, uuid: _Optional[bytes] = ..., expectedPropertyVersion: _Optional[int] = ..., changes: _Optional[_Iterable[_Union[KeyOptValue, _Mapping]]] = ..., removals: _Optional[_Iterable[str]] = ...) -> None: ...

class SetStreamAnnotationsResponse(_message.Message):
    __slots__ = ("stat",)
    STAT_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ...) -> None: ...

class SetStreamTagsParams(_message.Message):
    __slots__ = ("uuid", "expectedPropertyVersion", "tags", "collection", "remove")
    UUID_FIELD_NUMBER: _ClassVar[int]
    EXPECTEDPROPERTYVERSION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    REMOVE_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    expectedPropertyVersion: int
    tags: _containers.RepeatedCompositeFieldContainer[KeyOptValue]
    collection: str
    remove: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, uuid: _Optional[bytes] = ..., expectedPropertyVersion: _Optional[int] = ..., tags: _Optional[_Iterable[_Union[KeyOptValue, _Mapping]]] = ..., collection: _Optional[str] = ..., remove: _Optional[_Iterable[str]] = ...) -> None: ...

class SetStreamTagsResponse(_message.Message):
    __slots__ = ("stat",)
    STAT_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ...) -> None: ...

class CreateParams(_message.Message):
    __slots__ = ("uuid", "collection", "tags", "annotations")
    UUID_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    collection: str
    tags: _containers.RepeatedCompositeFieldContainer[KeyOptValue]
    annotations: _containers.RepeatedCompositeFieldContainer[KeyOptValue]
    def __init__(self, uuid: _Optional[bytes] = ..., collection: _Optional[str] = ..., tags: _Optional[_Iterable[_Union[KeyOptValue, _Mapping]]] = ..., annotations: _Optional[_Iterable[_Union[KeyOptValue, _Mapping]]] = ...) -> None: ...

class CreateResponse(_message.Message):
    __slots__ = ("stat",)
    STAT_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ...) -> None: ...

class MetadataUsageParams(_message.Message):
    __slots__ = ("prefix", "role")
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    prefix: str
    role: Role
    def __init__(self, prefix: _Optional[str] = ..., role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class MetadataUsageResponse(_message.Message):
    __slots__ = ("stat", "tags", "annotations")
    STAT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    tags: _containers.RepeatedCompositeFieldContainer[KeyCount]
    annotations: _containers.RepeatedCompositeFieldContainer[KeyCount]
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., tags: _Optional[_Iterable[_Union[KeyCount, _Mapping]]] = ..., annotations: _Optional[_Iterable[_Union[KeyCount, _Mapping]]] = ...) -> None: ...

class KeyCount(_message.Message):
    __slots__ = ("key", "count")
    KEY_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    key: str
    count: int
    def __init__(self, key: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class ListCollectionsParams(_message.Message):
    __slots__ = ("prefix", "role")
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    prefix: str
    role: Role
    def __init__(self, prefix: _Optional[str] = ..., role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class ListCollectionsResponse(_message.Message):
    __slots__ = ("stat", "collections")
    STAT_FIELD_NUMBER: _ClassVar[int]
    COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    collections: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., collections: _Optional[_Iterable[str]] = ...) -> None: ...

class LookupStreamsParams(_message.Message):
    __slots__ = ("collection", "isCollectionPrefix", "tags", "annotations", "role")
    COLLECTION_FIELD_NUMBER: _ClassVar[int]
    ISCOLLECTIONPREFIX_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    collection: str
    isCollectionPrefix: bool
    tags: _containers.RepeatedCompositeFieldContainer[KeyOptValue]
    annotations: _containers.RepeatedCompositeFieldContainer[KeyOptValue]
    role: Role
    def __init__(self, collection: _Optional[str] = ..., isCollectionPrefix: bool = ..., tags: _Optional[_Iterable[_Union[KeyOptValue, _Mapping]]] = ..., annotations: _Optional[_Iterable[_Union[KeyOptValue, _Mapping]]] = ..., role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class LookupStreamsResponse(_message.Message):
    __slots__ = ("stat", "results")
    STAT_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    results: _containers.RepeatedCompositeFieldContainer[StreamDescriptor]
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., results: _Optional[_Iterable[_Union[StreamDescriptor, _Mapping]]] = ...) -> None: ...

class NearestParams(_message.Message):
    __slots__ = ("uuid", "time", "versionMajor", "backward")
    UUID_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    BACKWARD_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    time: int
    versionMajor: int
    backward: bool
    def __init__(self, uuid: _Optional[bytes] = ..., time: _Optional[int] = ..., versionMajor: _Optional[int] = ..., backward: bool = ...) -> None: ...

class NearestResponse(_message.Message):
    __slots__ = ("stat", "versionMajor", "versionMinor", "value")
    STAT_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    VERSIONMINOR_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    versionMajor: int
    versionMinor: int
    value: RawPoint
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., versionMajor: _Optional[int] = ..., versionMinor: _Optional[int] = ..., value: _Optional[_Union[RawPoint, _Mapping]] = ...) -> None: ...

class ChangesParams(_message.Message):
    __slots__ = ("uuid", "fromMajor", "toMajor", "resolution")
    UUID_FIELD_NUMBER: _ClassVar[int]
    FROMMAJOR_FIELD_NUMBER: _ClassVar[int]
    TOMAJOR_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    fromMajor: int
    toMajor: int
    resolution: int
    def __init__(self, uuid: _Optional[bytes] = ..., fromMajor: _Optional[int] = ..., toMajor: _Optional[int] = ..., resolution: _Optional[int] = ...) -> None: ...

class ChangesResponse(_message.Message):
    __slots__ = ("stat", "versionMajor", "versionMinor", "ranges")
    STAT_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    VERSIONMINOR_FIELD_NUMBER: _ClassVar[int]
    RANGES_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    versionMajor: int
    versionMinor: int
    ranges: _containers.RepeatedCompositeFieldContainer[ChangedRange]
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., versionMajor: _Optional[int] = ..., versionMinor: _Optional[int] = ..., ranges: _Optional[_Iterable[_Union[ChangedRange, _Mapping]]] = ...) -> None: ...

class RoundSpec(_message.Message):
    __slots__ = ("bits",)
    BITS_FIELD_NUMBER: _ClassVar[int]
    bits: int
    def __init__(self, bits: _Optional[int] = ...) -> None: ...

class InsertParams(_message.Message):
    __slots__ = ("uuid", "sync", "merge_policy", "rounding", "values")
    UUID_FIELD_NUMBER: _ClassVar[int]
    SYNC_FIELD_NUMBER: _ClassVar[int]
    MERGE_POLICY_FIELD_NUMBER: _ClassVar[int]
    ROUNDING_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    sync: bool
    merge_policy: MergePolicy
    rounding: RoundSpec
    values: _containers.RepeatedCompositeFieldContainer[RawPoint]
    def __init__(self, uuid: _Optional[bytes] = ..., sync: bool = ..., merge_policy: _Optional[_Union[MergePolicy, str]] = ..., rounding: _Optional[_Union[RoundSpec, _Mapping]] = ..., values: _Optional[_Iterable[_Union[RawPoint, _Mapping]]] = ...) -> None: ...

class ArrowInsertParams(_message.Message):
    __slots__ = ("uuid", "sync", "merge_policy", "rounding", "arrowBytes")
    UUID_FIELD_NUMBER: _ClassVar[int]
    SYNC_FIELD_NUMBER: _ClassVar[int]
    MERGE_POLICY_FIELD_NUMBER: _ClassVar[int]
    ROUNDING_FIELD_NUMBER: _ClassVar[int]
    ARROWBYTES_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    sync: bool
    merge_policy: MergePolicy
    rounding: RoundSpec
    arrowBytes: bytes
    def __init__(self, uuid: _Optional[bytes] = ..., sync: bool = ..., merge_policy: _Optional[_Union[MergePolicy, str]] = ..., rounding: _Optional[_Union[RoundSpec, _Mapping]] = ..., arrowBytes: _Optional[bytes] = ...) -> None: ...

class InsertResponse(_message.Message):
    __slots__ = ("stat", "versionMajor", "versionMinor")
    STAT_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    VERSIONMINOR_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    versionMajor: int
    versionMinor: int
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., versionMajor: _Optional[int] = ..., versionMinor: _Optional[int] = ...) -> None: ...

class DeleteParams(_message.Message):
    __slots__ = ("uuid", "start", "end")
    UUID_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    start: int
    end: int
    def __init__(self, uuid: _Optional[bytes] = ..., start: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ("stat", "versionMajor", "versionMinor")
    STAT_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    VERSIONMINOR_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    versionMajor: int
    versionMinor: int
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., versionMajor: _Optional[int] = ..., versionMinor: _Optional[int] = ...) -> None: ...

class InfoParams(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class InfoResponse(_message.Message):
    __slots__ = ("stat", "mash", "majorVersion", "minorVersion", "build", "proxy")
    STAT_FIELD_NUMBER: _ClassVar[int]
    MASH_FIELD_NUMBER: _ClassVar[int]
    MAJORVERSION_FIELD_NUMBER: _ClassVar[int]
    MINORVERSION_FIELD_NUMBER: _ClassVar[int]
    BUILD_FIELD_NUMBER: _ClassVar[int]
    PROXY_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    mash: Mash
    majorVersion: int
    minorVersion: int
    build: str
    proxy: ProxyInfo
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., mash: _Optional[_Union[Mash, _Mapping]] = ..., majorVersion: _Optional[int] = ..., minorVersion: _Optional[int] = ..., build: _Optional[str] = ..., proxy: _Optional[_Union[ProxyInfo, _Mapping]] = ...) -> None: ...

class ProxyInfo(_message.Message):
    __slots__ = ("proxyEndpoints",)
    PROXYENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    proxyEndpoints: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, proxyEndpoints: _Optional[_Iterable[str]] = ...) -> None: ...

class FaultInjectParams(_message.Message):
    __slots__ = ("type", "params")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    type: int
    params: bytes
    def __init__(self, type: _Optional[int] = ..., params: _Optional[bytes] = ...) -> None: ...

class FaultInjectResponse(_message.Message):
    __slots__ = ("stat", "rv")
    STAT_FIELD_NUMBER: _ClassVar[int]
    RV_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    rv: bytes
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., rv: _Optional[bytes] = ...) -> None: ...

class FlushParams(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    def __init__(self, uuid: _Optional[bytes] = ...) -> None: ...

class FlushResponse(_message.Message):
    __slots__ = ("stat", "versionMajor", "versionMinor")
    STAT_FIELD_NUMBER: _ClassVar[int]
    VERSIONMAJOR_FIELD_NUMBER: _ClassVar[int]
    VERSIONMINOR_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    versionMajor: int
    versionMinor: int
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., versionMajor: _Optional[int] = ..., versionMinor: _Optional[int] = ...) -> None: ...

class ObliterateParams(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    def __init__(self, uuid: _Optional[bytes] = ...) -> None: ...

class ObliterateResponse(_message.Message):
    __slots__ = ("stat",)
    STAT_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ...) -> None: ...

class RawPoint(_message.Message):
    __slots__ = ("time", "value")
    TIME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    time: int
    value: float
    def __init__(self, time: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...

class StatPoint(_message.Message):
    __slots__ = ("time", "min", "mean", "max", "count", "stddev")
    TIME_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MEAN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    STDDEV_FIELD_NUMBER: _ClassVar[int]
    time: int
    min: float
    mean: float
    max: float
    count: int
    stddev: float
    def __init__(self, time: _Optional[int] = ..., min: _Optional[float] = ..., mean: _Optional[float] = ..., max: _Optional[float] = ..., count: _Optional[int] = ..., stddev: _Optional[float] = ...) -> None: ...

class ChangedRange(_message.Message):
    __slots__ = ("start", "end")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    start: int
    end: int
    def __init__(self, start: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ("code", "msg", "mash")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    MASH_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    mash: Mash
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ..., mash: _Optional[_Union[Mash, _Mapping]] = ...) -> None: ...

class Mash(_message.Message):
    __slots__ = ("revision", "leader", "leaderRevision", "totalWeight", "healthy", "unmapped", "members")
    REVISION_FIELD_NUMBER: _ClassVar[int]
    LEADER_FIELD_NUMBER: _ClassVar[int]
    LEADERREVISION_FIELD_NUMBER: _ClassVar[int]
    TOTALWEIGHT_FIELD_NUMBER: _ClassVar[int]
    HEALTHY_FIELD_NUMBER: _ClassVar[int]
    UNMAPPED_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    revision: int
    leader: str
    leaderRevision: int
    totalWeight: int
    healthy: bool
    unmapped: float
    members: _containers.RepeatedCompositeFieldContainer[Member]
    def __init__(self, revision: _Optional[int] = ..., leader: _Optional[str] = ..., leaderRevision: _Optional[int] = ..., totalWeight: _Optional[int] = ..., healthy: bool = ..., unmapped: _Optional[float] = ..., members: _Optional[_Iterable[_Union[Member, _Mapping]]] = ...) -> None: ...

class Member(_message.Message):
    __slots__ = ("hash", "nodename", "up", "enabled", "start", "end", "weight", "readPreference", "httpEndpoints", "grpcEndpoints")
    HASH_FIELD_NUMBER: _ClassVar[int]
    NODENAME_FIELD_NUMBER: _ClassVar[int]
    UP_FIELD_NUMBER: _ClassVar[int]
    IN_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    READPREFERENCE_FIELD_NUMBER: _ClassVar[int]
    HTTPENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    GRPCENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    hash: int
    nodename: str
    up: bool
    enabled: bool
    start: int
    end: int
    weight: int
    readPreference: float
    httpEndpoints: str
    grpcEndpoints: str
    def __init__(self, hash: _Optional[int] = ..., nodename: _Optional[str] = ..., up: bool = ..., enabled: bool = ..., start: _Optional[int] = ..., end: _Optional[int] = ..., weight: _Optional[int] = ..., readPreference: _Optional[float] = ..., httpEndpoints: _Optional[str] = ..., grpcEndpoints: _Optional[str] = ..., **kwargs) -> None: ...

class KeyOptValue(_message.Message):
    __slots__ = ("key", "val")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VAL_FIELD_NUMBER: _ClassVar[int]
    key: str
    val: OptValue
    def __init__(self, key: _Optional[str] = ..., val: _Optional[_Union[OptValue, _Mapping]] = ...) -> None: ...

class OptValue(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class KeyValue(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class StreamCSVConfig(_message.Message):
    __slots__ = ("version", "label", "uuid")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    version: int
    label: str
    uuid: bytes
    def __init__(self, version: _Optional[int] = ..., label: _Optional[str] = ..., uuid: _Optional[bytes] = ...) -> None: ...

class GenerateCSVParams(_message.Message):
    __slots__ = ("queryType", "startTime", "endTime", "windowSize", "depth", "includeVersions", "streams")
    class QueryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ALIGNED_WINDOWS_QUERY: _ClassVar[GenerateCSVParams.QueryType]
        WINDOWS_QUERY: _ClassVar[GenerateCSVParams.QueryType]
        RAW_QUERY: _ClassVar[GenerateCSVParams.QueryType]
    ALIGNED_WINDOWS_QUERY: GenerateCSVParams.QueryType
    WINDOWS_QUERY: GenerateCSVParams.QueryType
    RAW_QUERY: GenerateCSVParams.QueryType
    QUERYTYPE_FIELD_NUMBER: _ClassVar[int]
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    WINDOWSIZE_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    INCLUDEVERSIONS_FIELD_NUMBER: _ClassVar[int]
    STREAMS_FIELD_NUMBER: _ClassVar[int]
    queryType: GenerateCSVParams.QueryType
    startTime: int
    endTime: int
    windowSize: int
    depth: int
    includeVersions: bool
    streams: _containers.RepeatedCompositeFieldContainer[StreamCSVConfig]
    def __init__(self, queryType: _Optional[_Union[GenerateCSVParams.QueryType, str]] = ..., startTime: _Optional[int] = ..., endTime: _Optional[int] = ..., windowSize: _Optional[int] = ..., depth: _Optional[int] = ..., includeVersions: bool = ..., streams: _Optional[_Iterable[_Union[StreamCSVConfig, _Mapping]]] = ...) -> None: ...

class GenerateCSVResponse(_message.Message):
    __slots__ = ("stat", "isHeader", "row")
    STAT_FIELD_NUMBER: _ClassVar[int]
    ISHEADER_FIELD_NUMBER: _ClassVar[int]
    ROW_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    isHeader: bool
    row: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., isHeader: bool = ..., row: _Optional[_Iterable[str]] = ...) -> None: ...

class SQLQueryParams(_message.Message):
    __slots__ = ("query", "params", "role")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    query: str
    params: _containers.RepeatedScalarFieldContainer[str]
    role: Role
    def __init__(self, query: _Optional[str] = ..., params: _Optional[_Iterable[str]] = ..., role: _Optional[_Union[Role, _Mapping]] = ...) -> None: ...

class SQLQueryResponse(_message.Message):
    __slots__ = ("stat", "SQLQueryRow")
    STAT_FIELD_NUMBER: _ClassVar[int]
    SQLQUERYROW_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    SQLQueryRow: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., SQLQueryRow: _Optional[_Iterable[bytes]] = ...) -> None: ...

class Role(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class SetCompactionConfigParams(_message.Message):
    __slots__ = ("uuid", "CompactedVersion", "reducedResolutionRanges", "unused0")
    UUID_FIELD_NUMBER: _ClassVar[int]
    COMPACTEDVERSION_FIELD_NUMBER: _ClassVar[int]
    REDUCEDRESOLUTIONRANGES_FIELD_NUMBER: _ClassVar[int]
    UNUSED0_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    CompactedVersion: int
    reducedResolutionRanges: _containers.RepeatedCompositeFieldContainer[ReducedResolutionRange]
    unused0: int
    def __init__(self, uuid: _Optional[bytes] = ..., CompactedVersion: _Optional[int] = ..., reducedResolutionRanges: _Optional[_Iterable[_Union[ReducedResolutionRange, _Mapping]]] = ..., unused0: _Optional[int] = ...) -> None: ...

class SetCompactionConfigResponse(_message.Message):
    __slots__ = ("stat",)
    STAT_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ...) -> None: ...

class GetCompactionConfigParams(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: bytes
    def __init__(self, uuid: _Optional[bytes] = ...) -> None: ...

class GetCompactionConfigResponse(_message.Message):
    __slots__ = ("stat", "LatestMajorVersion", "CompactedVersion", "reducedResolutionRanges", "unused0")
    STAT_FIELD_NUMBER: _ClassVar[int]
    LATESTMAJORVERSION_FIELD_NUMBER: _ClassVar[int]
    COMPACTEDVERSION_FIELD_NUMBER: _ClassVar[int]
    REDUCEDRESOLUTIONRANGES_FIELD_NUMBER: _ClassVar[int]
    UNUSED0_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    LatestMajorVersion: int
    CompactedVersion: int
    reducedResolutionRanges: _containers.RepeatedCompositeFieldContainer[ReducedResolutionRange]
    unused0: int
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., LatestMajorVersion: _Optional[int] = ..., CompactedVersion: _Optional[int] = ..., reducedResolutionRanges: _Optional[_Iterable[_Union[ReducedResolutionRange, _Mapping]]] = ..., unused0: _Optional[int] = ...) -> None: ...

class ReducedResolutionRange(_message.Message):
    __slots__ = ("Start", "End", "Resolution")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    Start: int
    End: int
    Resolution: int
    def __init__(self, Start: _Optional[int] = ..., End: _Optional[int] = ..., Resolution: _Optional[int] = ...) -> None: ...

class SubscriptionUpdate(_message.Message):
    __slots__ = ("op", "uuid")
    OP_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    op: SubscriptionUpdateOp
    uuid: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, op: _Optional[_Union[SubscriptionUpdateOp, str]] = ..., uuid: _Optional[_Iterable[bytes]] = ...) -> None: ...

class SubscriptionResp(_message.Message):
    __slots__ = ("stat", "uuid", "arrowBytes")
    STAT_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    ARROWBYTES_FIELD_NUMBER: _ClassVar[int]
    stat: Status
    uuid: bytes
    arrowBytes: bytes
    def __init__(self, stat: _Optional[_Union[Status, _Mapping]] = ..., uuid: _Optional[bytes] = ..., arrowBytes: _Optional[bytes] = ...) -> None: ...
