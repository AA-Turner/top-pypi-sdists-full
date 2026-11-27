from qm.grpc.qm.pb import inc_qua_pb2 as _inc_qua_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QuaVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    QUA_VERSION_UNSPECIFIED: _ClassVar[QuaVersion]
    QUA1: _ClassVar[QuaVersion]
    QUA2: _ClassVar[QuaVersion]
QUA_VERSION_UNSPECIFIED: QuaVersion
QUA1: QuaVersion
QUA2: QuaVersion

class GetTopologyRequest(_message.Message):
    __slots__ = ["profile_name", "device_name", "qua_version"]
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    QUA_VERSION_FIELD_NUMBER: _ClassVar[int]
    profile_name: str
    device_name: str
    qua_version: QuaVersion
    def __init__(self, profile_name: _Optional[str] = ..., device_name: _Optional[str] = ..., qua_version: _Optional[_Union[QuaVersion, str]] = ...) -> None: ...

class GetTopologyResponse(_message.Message):
    __slots__ = ["success", "error"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: GetTopologySuccess
    error: GetTopologyError
    def __init__(self, success: _Optional[_Union[GetTopologySuccess, _Mapping]] = ..., error: _Optional[_Union[GetTopologyError, _Mapping]] = ...) -> None: ...

class GetTopologySuccess(_message.Message):
    __slots__ = ["nodes", "subgraphs"]
    NODES_FIELD_NUMBER: _ClassVar[int]
    SUBGRAPHS_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[Node]
    subgraphs: _containers.RepeatedCompositeFieldContainer[SubGraph]
    def __init__(self, nodes: _Optional[_Iterable[_Union[Node, _Mapping]]] = ..., subgraphs: _Optional[_Iterable[_Union[SubGraph, _Mapping]]] = ...) -> None: ...

class GetTopologyError(_message.Message):
    __slots__ = ["details"]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    details: str
    def __init__(self, details: _Optional[str] = ...) -> None: ...

class UpdateTopologyRequest(_message.Message):
    __slots__ = ["profile_name", "nodes", "subgraphs", "device_name", "qua_version"]
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    SUBGRAPHS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    QUA_VERSION_FIELD_NUMBER: _ClassVar[int]
    profile_name: str
    nodes: _containers.RepeatedCompositeFieldContainer[Node]
    subgraphs: _containers.RepeatedCompositeFieldContainer[SubGraph]
    device_name: str
    qua_version: QuaVersion
    def __init__(self, profile_name: _Optional[str] = ..., nodes: _Optional[_Iterable[_Union[Node, _Mapping]]] = ..., subgraphs: _Optional[_Iterable[_Union[SubGraph, _Mapping]]] = ..., device_name: _Optional[str] = ..., qua_version: _Optional[_Union[QuaVersion, str]] = ...) -> None: ...

class UpdateTopologyResponse(_message.Message):
    __slots__ = ["success", "error"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: UpdateTopologySuccess
    error: UpdateTopologyError
    def __init__(self, success: _Optional[_Union[UpdateTopologySuccess, _Mapping]] = ..., error: _Optional[_Union[UpdateTopologyError, _Mapping]] = ...) -> None: ...

class UpdateTopologySuccess(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateTopologyError(_message.Message):
    __slots__ = ["details"]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    details: str
    def __init__(self, details: _Optional[str] = ...) -> None: ...

class Node(_message.Message):
    __slots__ = ["name", "metadata", "target_type", "ref_target_name", "ref_target_type_name", "kernels_and_fidelity", "metadata_json"]
    class Metadata(_message.Message):
        __slots__ = ["last_updated_at", "super_conducting"]
        class SuperConducting(_message.Message):
            __slots__ = ["t1_seconds", "t1_seconds_std_error", "t2_ramsey_seconds", "t2_ramsey_seconds_std_error", "t2_echo_seconds", "t2_echo_seconds_std_error", "frequency_hz", "frequency_hz_std_error", "readout_fidelity", "readout_fidelity_std_error", "average_gate_fidelity", "average_gate_fidelity_std_error"]
            T1_SECONDS_FIELD_NUMBER: _ClassVar[int]
            T1_SECONDS_STD_ERROR_FIELD_NUMBER: _ClassVar[int]
            T2_RAMSEY_SECONDS_FIELD_NUMBER: _ClassVar[int]
            T2_RAMSEY_SECONDS_STD_ERROR_FIELD_NUMBER: _ClassVar[int]
            T2_ECHO_SECONDS_FIELD_NUMBER: _ClassVar[int]
            T2_ECHO_SECONDS_STD_ERROR_FIELD_NUMBER: _ClassVar[int]
            FREQUENCY_HZ_FIELD_NUMBER: _ClassVar[int]
            FREQUENCY_HZ_STD_ERROR_FIELD_NUMBER: _ClassVar[int]
            READOUT_FIDELITY_FIELD_NUMBER: _ClassVar[int]
            READOUT_FIDELITY_STD_ERROR_FIELD_NUMBER: _ClassVar[int]
            AVERAGE_GATE_FIDELITY_FIELD_NUMBER: _ClassVar[int]
            AVERAGE_GATE_FIDELITY_STD_ERROR_FIELD_NUMBER: _ClassVar[int]
            t1_seconds: float
            t1_seconds_std_error: float
            t2_ramsey_seconds: float
            t2_ramsey_seconds_std_error: float
            t2_echo_seconds: float
            t2_echo_seconds_std_error: float
            frequency_hz: float
            frequency_hz_std_error: float
            readout_fidelity: float
            readout_fidelity_std_error: float
            average_gate_fidelity: float
            average_gate_fidelity_std_error: float
            def __init__(self, t1_seconds: _Optional[float] = ..., t1_seconds_std_error: _Optional[float] = ..., t2_ramsey_seconds: _Optional[float] = ..., t2_ramsey_seconds_std_error: _Optional[float] = ..., t2_echo_seconds: _Optional[float] = ..., t2_echo_seconds_std_error: _Optional[float] = ..., frequency_hz: _Optional[float] = ..., frequency_hz_std_error: _Optional[float] = ..., readout_fidelity: _Optional[float] = ..., readout_fidelity_std_error: _Optional[float] = ..., average_gate_fidelity: _Optional[float] = ..., average_gate_fidelity_std_error: _Optional[float] = ...) -> None: ...
        LAST_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
        SUPER_CONDUCTING_FIELD_NUMBER: _ClassVar[int]
        last_updated_at: _timestamp_pb2.Timestamp
        super_conducting: Node.Metadata.SuperConducting
        def __init__(self, last_updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., super_conducting: _Optional[_Union[Node.Metadata.SuperConducting, _Mapping]] = ...) -> None: ...
    class KernelsAndFidelityEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    TARGET_TYPE_FIELD_NUMBER: _ClassVar[int]
    REF_TARGET_NAME_FIELD_NUMBER: _ClassVar[int]
    REF_TARGET_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    KERNELS_AND_FIDELITY_FIELD_NUMBER: _ClassVar[int]
    METADATA_JSON_FIELD_NUMBER: _ClassVar[int]
    name: str
    metadata: Node.Metadata
    target_type: _inc_qua_pb2.QuaProgram.TargetType
    ref_target_name: str
    ref_target_type_name: str
    kernels_and_fidelity: _containers.ScalarMap[str, float]
    metadata_json: _struct_pb2.Struct
    def __init__(self, name: _Optional[str] = ..., metadata: _Optional[_Union[Node.Metadata, _Mapping]] = ..., target_type: _Optional[_Union[_inc_qua_pb2.QuaProgram.TargetType, _Mapping]] = ..., ref_target_name: _Optional[str] = ..., ref_target_type_name: _Optional[str] = ..., kernels_and_fidelity: _Optional[_Mapping[str, float]] = ..., metadata_json: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class SubGraph(_message.Message):
    __slots__ = ["name", "indices", "metadata", "target_type", "ref_target_name", "ref_target_type_name", "kernels_and_fidelity", "metadata_json"]
    class Metadata(_message.Message):
        __slots__ = ["last_updated_at", "super_conducting"]
        class SuperConducting(_message.Message):
            __slots__ = ["average_gate_fidelity", "average_gate_fidelity_std_error"]
            AVERAGE_GATE_FIDELITY_FIELD_NUMBER: _ClassVar[int]
            AVERAGE_GATE_FIDELITY_STD_ERROR_FIELD_NUMBER: _ClassVar[int]
            average_gate_fidelity: float
            average_gate_fidelity_std_error: float
            def __init__(self, average_gate_fidelity: _Optional[float] = ..., average_gate_fidelity_std_error: _Optional[float] = ...) -> None: ...
        LAST_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
        SUPER_CONDUCTING_FIELD_NUMBER: _ClassVar[int]
        last_updated_at: _timestamp_pb2.Timestamp
        super_conducting: SubGraph.Metadata.SuperConducting
        def __init__(self, last_updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., super_conducting: _Optional[_Union[SubGraph.Metadata.SuperConducting, _Mapping]] = ...) -> None: ...
    class KernelsAndFidelityEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    INDICES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    TARGET_TYPE_FIELD_NUMBER: _ClassVar[int]
    REF_TARGET_NAME_FIELD_NUMBER: _ClassVar[int]
    REF_TARGET_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    KERNELS_AND_FIDELITY_FIELD_NUMBER: _ClassVar[int]
    METADATA_JSON_FIELD_NUMBER: _ClassVar[int]
    name: str
    indices: _containers.RepeatedScalarFieldContainer[int]
    metadata: SubGraph.Metadata
    target_type: _inc_qua_pb2.QuaProgram.CompositeTargetType
    ref_target_name: str
    ref_target_type_name: str
    kernels_and_fidelity: _containers.ScalarMap[str, float]
    metadata_json: _struct_pb2.Struct
    def __init__(self, name: _Optional[str] = ..., indices: _Optional[_Iterable[int]] = ..., metadata: _Optional[_Union[SubGraph.Metadata, _Mapping]] = ..., target_type: _Optional[_Union[_inc_qua_pb2.QuaProgram.CompositeTargetType, _Mapping]] = ..., ref_target_name: _Optional[str] = ..., ref_target_type_name: _Optional[str] = ..., kernels_and_fidelity: _Optional[_Mapping[str, float]] = ..., metadata_json: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class EntityRef(_message.Message):
    __slots__ = ["name", "kind"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    name: str
    kind: str
    def __init__(self, name: _Optional[str] = ..., kind: _Optional[str] = ...) -> None: ...

class Device(_message.Message):
    __slots__ = ["device_name", "metadata", "default_profile_name"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    metadata: _struct_pb2.Struct
    default_profile_name: str
    def __init__(self, device_name: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., default_profile_name: _Optional[str] = ...) -> None: ...

class CreateDeviceRequest(_message.Message):
    __slots__ = ["device_name", "metadata"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    metadata: _struct_pb2.Struct
    def __init__(self, device_name: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class CreateDeviceResponse(_message.Message):
    __slots__ = ["device"]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    device: Device
    def __init__(self, device: _Optional[_Union[Device, _Mapping]] = ...) -> None: ...

class ListDevicesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListDevicesResponse(_message.Message):
    __slots__ = ["devices"]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    devices: _containers.RepeatedCompositeFieldContainer[Device]
    def __init__(self, devices: _Optional[_Iterable[_Union[Device, _Mapping]]] = ...) -> None: ...

class SetDefaultProfileRequest(_message.Message):
    __slots__ = ["device_name", "profile_name"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    profile_name: str
    def __init__(self, device_name: _Optional[str] = ..., profile_name: _Optional[str] = ...) -> None: ...

class SetDefaultProfileResponse(_message.Message):
    __slots__ = ["device"]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    device: Device
    def __init__(self, device: _Optional[_Union[Device, _Mapping]] = ...) -> None: ...

class RemoveDeviceRequest(_message.Message):
    __slots__ = ["device_name"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    def __init__(self, device_name: _Optional[str] = ...) -> None: ...

class RemoveDeviceResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class InterfaceItem(_message.Message):
    __slots__ = ["name", "artifact_digest", "dependencies"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_DIGEST_FIELD_NUMBER: _ClassVar[int]
    DEPENDENCIES_FIELD_NUMBER: _ClassVar[int]
    name: str
    artifact_digest: str
    dependencies: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., artifact_digest: _Optional[str] = ..., dependencies: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateProfileRequest(_message.Message):
    __slots__ = ["device_name", "profile_name", "target_types", "module_interfaces", "metadata", "qua_version"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_TYPES_FIELD_NUMBER: _ClassVar[int]
    MODULE_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    QUA_VERSION_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    profile_name: str
    target_types: _containers.RepeatedCompositeFieldContainer[InterfaceItem]
    module_interfaces: _containers.RepeatedCompositeFieldContainer[InterfaceItem]
    metadata: _struct_pb2.Struct
    qua_version: QuaVersion
    def __init__(self, device_name: _Optional[str] = ..., profile_name: _Optional[str] = ..., target_types: _Optional[_Iterable[_Union[InterfaceItem, _Mapping]]] = ..., module_interfaces: _Optional[_Iterable[_Union[InterfaceItem, _Mapping]]] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., qua_version: _Optional[_Union[QuaVersion, str]] = ...) -> None: ...

class CreateProfileResponse(_message.Message):
    __slots__ = ["profile_name"]
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    profile_name: str
    def __init__(self, profile_name: _Optional[str] = ...) -> None: ...

class ListProfilesRequest(_message.Message):
    __slots__ = ["device_name"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    def __init__(self, device_name: _Optional[str] = ...) -> None: ...

class ListProfilesResponse(_message.Message):
    __slots__ = ["profile_names"]
    PROFILE_NAMES_FIELD_NUMBER: _ClassVar[int]
    profile_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, profile_names: _Optional[_Iterable[str]] = ...) -> None: ...

class GetProfileRequest(_message.Message):
    __slots__ = ["device_name", "profile_name", "qua_version"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    QUA_VERSION_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    profile_name: str
    qua_version: QuaVersion
    def __init__(self, device_name: _Optional[str] = ..., profile_name: _Optional[str] = ..., qua_version: _Optional[_Union[QuaVersion, str]] = ...) -> None: ...

class GetProfileResponse(_message.Message):
    __slots__ = ["device_name", "profile_name", "target_types", "module_interfaces", "metadata", "qua_version"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_TYPES_FIELD_NUMBER: _ClassVar[int]
    MODULE_INTERFACES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    QUA_VERSION_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    profile_name: str
    target_types: _containers.RepeatedCompositeFieldContainer[InterfaceItem]
    module_interfaces: _containers.RepeatedCompositeFieldContainer[InterfaceItem]
    metadata: _struct_pb2.Struct
    qua_version: QuaVersion
    def __init__(self, device_name: _Optional[str] = ..., profile_name: _Optional[str] = ..., target_types: _Optional[_Iterable[_Union[InterfaceItem, _Mapping]]] = ..., module_interfaces: _Optional[_Iterable[_Union[InterfaceItem, _Mapping]]] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., qua_version: _Optional[_Union[QuaVersion, str]] = ...) -> None: ...

class RemoveProfileRequest(_message.Message):
    __slots__ = ["device_name", "profile_name"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    profile_name: str
    def __init__(self, device_name: _Optional[str] = ..., profile_name: _Optional[str] = ...) -> None: ...

class RemoveProfileResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListEntitiesRequest(_message.Message):
    __slots__ = ["device_name", "profile_name", "qua_version"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    QUA_VERSION_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    profile_name: str
    qua_version: QuaVersion
    def __init__(self, device_name: _Optional[str] = ..., profile_name: _Optional[str] = ..., qua_version: _Optional[_Union[QuaVersion, str]] = ...) -> None: ...

class ListEntitiesResponse(_message.Message):
    __slots__ = ["entities"]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    entities: _containers.RepeatedCompositeFieldContainer[EntityRef]
    def __init__(self, entities: _Optional[_Iterable[_Union[EntityRef, _Mapping]]] = ...) -> None: ...

class GetEntitiesRequest(_message.Message):
    __slots__ = ["device_name", "profile_name", "entities", "as_of", "qua_version"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    AS_OF_FIELD_NUMBER: _ClassVar[int]
    QUA_VERSION_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    profile_name: str
    entities: _containers.RepeatedCompositeFieldContainer[EntityRef]
    as_of: _timestamp_pb2.Timestamp
    qua_version: QuaVersion
    def __init__(self, device_name: _Optional[str] = ..., profile_name: _Optional[str] = ..., entities: _Optional[_Iterable[_Union[EntityRef, _Mapping]]] = ..., as_of: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., qua_version: _Optional[_Union[QuaVersion, str]] = ...) -> None: ...

class GetEntitiesResponse(_message.Message):
    __slots__ = ["artifact_digests"]
    ARTIFACT_DIGESTS_FIELD_NUMBER: _ClassVar[int]
    artifact_digests: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, artifact_digests: _Optional[_Iterable[str]] = ...) -> None: ...

class UploadArtifactRequest(_message.Message):
    __slots__ = ["digest", "kind", "data"]
    DIGEST_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    digest: str
    kind: str
    data: bytes
    def __init__(self, digest: _Optional[str] = ..., kind: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class UploadArtifactResponse(_message.Message):
    __slots__ = ["digest", "kind"]
    DIGEST_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    digest: str
    kind: str
    def __init__(self, digest: _Optional[str] = ..., kind: _Optional[str] = ...) -> None: ...

class GetArtifactRequest(_message.Message):
    __slots__ = ["digest"]
    DIGEST_FIELD_NUMBER: _ClassVar[int]
    digest: str
    def __init__(self, digest: _Optional[str] = ...) -> None: ...

class GetArtifactResponse(_message.Message):
    __slots__ = ["digest", "kind", "data"]
    DIGEST_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    digest: str
    kind: str
    data: bytes
    def __init__(self, digest: _Optional[str] = ..., kind: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class ArtifactExistsRequest(_message.Message):
    __slots__ = ["digest"]
    DIGEST_FIELD_NUMBER: _ClassVar[int]
    digest: str
    def __init__(self, digest: _Optional[str] = ...) -> None: ...

class ArtifactExistsResponse(_message.Message):
    __slots__ = ["digest", "exists"]
    DIGEST_FIELD_NUMBER: _ClassVar[int]
    EXISTS_FIELD_NUMBER: _ClassVar[int]
    digest: str
    exists: bool
    def __init__(self, digest: _Optional[str] = ..., exists: bool = ...) -> None: ...

class RemoveArtifactRequest(_message.Message):
    __slots__ = ["digest"]
    DIGEST_FIELD_NUMBER: _ClassVar[int]
    digest: str
    def __init__(self, digest: _Optional[str] = ...) -> None: ...

class RemoveArtifactResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PublishItem(_message.Message):
    __slots__ = ["name", "artifact_digest", "dependencies", "kind"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_DIGEST_FIELD_NUMBER: _ClassVar[int]
    DEPENDENCIES_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    name: str
    artifact_digest: str
    dependencies: _containers.RepeatedCompositeFieldContainer[EntityRef]
    kind: str
    def __init__(self, name: _Optional[str] = ..., artifact_digest: _Optional[str] = ..., dependencies: _Optional[_Iterable[_Union[EntityRef, _Mapping]]] = ..., kind: _Optional[str] = ...) -> None: ...

class PublishRequest(_message.Message):
    __slots__ = ["device_name", "profile_name", "targets", "modules", "performed_by", "notes", "metadata", "entities", "qua_version"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    MODULES_FIELD_NUMBER: _ClassVar[int]
    PERFORMED_BY_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    QUA_VERSION_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    profile_name: str
    targets: _containers.RepeatedCompositeFieldContainer[PublishItem]
    modules: _containers.RepeatedCompositeFieldContainer[PublishItem]
    performed_by: str
    notes: str
    metadata: _struct_pb2.Struct
    entities: _containers.RepeatedCompositeFieldContainer[PublishItem]
    qua_version: QuaVersion
    def __init__(self, device_name: _Optional[str] = ..., profile_name: _Optional[str] = ..., targets: _Optional[_Iterable[_Union[PublishItem, _Mapping]]] = ..., modules: _Optional[_Iterable[_Union[PublishItem, _Mapping]]] = ..., performed_by: _Optional[str] = ..., notes: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., entities: _Optional[_Iterable[_Union[PublishItem, _Mapping]]] = ..., qua_version: _Optional[_Union[QuaVersion, str]] = ...) -> None: ...

class PublishResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetPublishEventsRequest(_message.Message):
    __slots__ = ["device_name", "profile_name", "qua_version"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    QUA_VERSION_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    profile_name: str
    qua_version: QuaVersion
    def __init__(self, device_name: _Optional[str] = ..., profile_name: _Optional[str] = ..., qua_version: _Optional[_Union[QuaVersion, str]] = ...) -> None: ...

class PublishEvent(_message.Message):
    __slots__ = ["timestamp", "notes", "metadata", "performed_by", "updated_entities", "qua_version"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PERFORMED_BY_FIELD_NUMBER: _ClassVar[int]
    UPDATED_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    QUA_VERSION_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    notes: str
    metadata: _struct_pb2.Struct
    performed_by: str
    updated_entities: _containers.RepeatedCompositeFieldContainer[EntityRef]
    qua_version: QuaVersion
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., notes: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., performed_by: _Optional[str] = ..., updated_entities: _Optional[_Iterable[_Union[EntityRef, _Mapping]]] = ..., qua_version: _Optional[_Union[QuaVersion, str]] = ...) -> None: ...

class GetPublishEventsResponse(_message.Message):
    __slots__ = ["events"]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[PublishEvent]
    def __init__(self, events: _Optional[_Iterable[_Union[PublishEvent, _Mapping]]] = ...) -> None: ...

class AuthenticateRequest(_message.Message):
    __slots__ = ["device_name", "key"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    key: str
    def __init__(self, device_name: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class AuthenticateResponse(_message.Message):
    __slots__ = ["valid"]
    VALID_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    def __init__(self, valid: bool = ...) -> None: ...

class ReplaceKeysRequest(_message.Message):
    __slots__ = ["device_name", "keys"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, device_name: _Optional[str] = ..., keys: _Optional[_Iterable[str]] = ...) -> None: ...

class ReplaceKeysResponse(_message.Message):
    __slots__ = ["device_name", "count"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    count: int
    def __init__(self, device_name: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class AddKeyRequest(_message.Message):
    __slots__ = ["device_name", "key"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    key: str
    def __init__(self, device_name: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class AddKeyResponse(_message.Message):
    __slots__ = ["device_name", "added", "count"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ADDED_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    added: bool
    count: int
    def __init__(self, device_name: _Optional[str] = ..., added: bool = ..., count: _Optional[int] = ...) -> None: ...

class RemoveKeyRequest(_message.Message):
    __slots__ = ["device_name", "key"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    key: str
    def __init__(self, device_name: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class RemoveKeyResponse(_message.Message):
    __slots__ = ["device_name", "removed", "count"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    removed: bool
    count: int
    def __init__(self, device_name: _Optional[str] = ..., removed: bool = ..., count: _Optional[int] = ...) -> None: ...
