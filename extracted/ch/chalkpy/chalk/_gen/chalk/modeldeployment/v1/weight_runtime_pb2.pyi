from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.modeldeployment.v1 import service_pb2 as _service_pb2
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

class GetModelWeightRuntimeTargetRequest(_message.Message):
    __slots__ = ("expected_revision_id", "manifest_versions")
    EXPECTED_REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    expected_revision_id: str
    manifest_versions: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self, expected_revision_id: _Optional[str] = ..., manifest_versions: _Optional[_Iterable[int]] = ...
    ) -> None: ...

class GetModelWeightRuntimeTargetResponse(_message.Message):
    __slots__ = ("target", "lease_expires_at", "manifest_identities")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    LEASE_EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_IDENTITIES_FIELD_NUMBER: _ClassVar[int]
    target: _service_pb2.ModelScalingGroupWeightTarget
    lease_expires_at: _timestamp_pb2.Timestamp
    manifest_identities: _containers.RepeatedCompositeFieldContainer[ModelWeightRuntimeManifestIdentity]
    def __init__(
        self,
        target: _Optional[_Union[_service_pb2.ModelScalingGroupWeightTarget, _Mapping]] = ...,
        lease_expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        manifest_identities: _Optional[_Iterable[_Union[ModelWeightRuntimeManifestIdentity, _Mapping]]] = ...,
    ) -> None: ...

class ModelWeightRuntimeManifestIdentity(_message.Message):
    __slots__ = ("version", "manifest_sha256")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_SHA256_FIELD_NUMBER: _ClassVar[int]
    version: int
    manifest_sha256: str
    def __init__(self, version: _Optional[int] = ..., manifest_sha256: _Optional[str] = ...) -> None: ...
