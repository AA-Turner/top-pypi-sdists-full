from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.auth import principal__client_pb2 as _principal__client_pb2
from tecton_proto.common import container_image__client_pb2 as _container_image__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
JOB_ENVIRONMENT_REALTIME: JobEnvironment
JOB_ENVIRONMENT_RIFT_BATCH: JobEnvironment
JOB_ENVIRONMENT_RIFT_STREAM: JobEnvironment
JOB_ENVIRONMENT_UNSPECIFIED: JobEnvironment
REMOTE_COMPUTE_TYPE_CORE: RemoteComputeType
REMOTE_COMPUTE_TYPE_CUSTOM: RemoteComputeType
REMOTE_COMPUTE_TYPE_EXTENDED: RemoteComputeType
REMOTE_COMPUTE_TYPE_SNOWPARK_DEPRECATED_DO_NOT_USE: RemoteComputeType
REMOTE_ENVIRONMENT_STATUS_DELETING: RemoteEnvironmentStatus
REMOTE_ENVIRONMENT_STATUS_DELETION_FAILED: RemoteEnvironmentStatus
REMOTE_ENVIRONMENT_STATUS_ERROR: RemoteEnvironmentStatus
REMOTE_ENVIRONMENT_STATUS_PENDING: RemoteEnvironmentStatus
REMOTE_ENVIRONMENT_STATUS_READY: RemoteEnvironmentStatus

class DependentFeatureService(_message.Message):
    __slots__ = ["feature_service_name", "workspace_name"]
    FEATURE_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    feature_service_name: str
    workspace_name: str
    def __init__(self, workspace_name: _Optional[str] = ..., feature_service_name: _Optional[str] = ...) -> None: ...

class DependentFeatureView(_message.Message):
    __slots__ = ["feature_view_name", "workspace_name"]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    feature_view_name: str
    workspace_name: str
    def __init__(self, workspace_name: _Optional[str] = ..., feature_view_name: _Optional[str] = ...) -> None: ...

class ObjectStoreUploadPart(_message.Message):
    __slots__ = ["s3_upload_part"]
    S3_UPLOAD_PART_FIELD_NUMBER: _ClassVar[int]
    s3_upload_part: S3UploadPart
    def __init__(self, s3_upload_part: _Optional[_Union[S3UploadPart, _Mapping]] = ...) -> None: ...

class RealtimeEnvironment(_message.Message):
    __slots__ = ["feature_services", "image_info", "online_provisioned", "provisioned_image_info", "remote_function_uri", "tecton_transform_runtime_version"]
    FEATURE_SERVICES_FIELD_NUMBER: _ClassVar[int]
    IMAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    ONLINE_PROVISIONED_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_IMAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    REMOTE_FUNCTION_URI_FIELD_NUMBER: _ClassVar[int]
    TECTON_TRANSFORM_RUNTIME_VERSION_FIELD_NUMBER: _ClassVar[int]
    feature_services: _containers.RepeatedCompositeFieldContainer[DependentFeatureService]
    image_info: _container_image__client_pb2.ContainerImage
    online_provisioned: bool
    provisioned_image_info: _container_image__client_pb2.ContainerImage
    remote_function_uri: str
    tecton_transform_runtime_version: str
    def __init__(self, tecton_transform_runtime_version: _Optional[str] = ..., image_info: _Optional[_Union[_container_image__client_pb2.ContainerImage, _Mapping]] = ..., provisioned_image_info: _Optional[_Union[_container_image__client_pb2.ContainerImage, _Mapping]] = ..., remote_function_uri: _Optional[str] = ..., feature_services: _Optional[_Iterable[_Union[DependentFeatureService, _Mapping]]] = ..., online_provisioned: bool = ...) -> None: ...

class RemoteComputeEnvironment(_message.Message):
    __slots__ = ["created_at", "created_by", "created_by_principal", "description", "feature_services", "id", "image_info", "name", "provisioned_image_info", "python_version", "realtime_job_environment", "requirements", "resolved_requirements", "rift_batch_job_environment", "s3_wheels_location", "sdk_version", "status", "status_details", "supported_job_environments", "type", "updated_at"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IMAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_IMAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    PYTHON_VERSION_FIELD_NUMBER: _ClassVar[int]
    REALTIME_JOB_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    RESOLVED_REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    RIFT_BATCH_JOB_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    S3_WHEELS_LOCATION_FIELD_NUMBER: _ClassVar[int]
    SDK_VERSION_FIELD_NUMBER: _ClassVar[int]
    STATUS_DETAILS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_JOB_ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    created_by: _principal__client_pb2.Principal
    created_by_principal: _principal__client_pb2.PrincipalBasic
    description: str
    feature_services: _containers.RepeatedCompositeFieldContainer[DependentFeatureService]
    id: str
    image_info: _container_image__client_pb2.ContainerImage
    name: str
    provisioned_image_info: _container_image__client_pb2.ContainerImage
    python_version: str
    realtime_job_environment: RealtimeEnvironment
    requirements: str
    resolved_requirements: str
    rift_batch_job_environment: RiftBatchEnvironment
    s3_wheels_location: str
    sdk_version: str
    status: RemoteEnvironmentStatus
    status_details: str
    supported_job_environments: _containers.RepeatedScalarFieldContainer[JobEnvironment]
    type: RemoteComputeType
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[_Union[RemoteComputeType, str]] = ..., status: _Optional[_Union[RemoteEnvironmentStatus, str]] = ..., image_info: _Optional[_Union[_container_image__client_pb2.ContainerImage, _Mapping]] = ..., provisioned_image_info: _Optional[_Union[_container_image__client_pb2.ContainerImage, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., created_by: _Optional[_Union[_principal__client_pb2.Principal, _Mapping]] = ..., created_by_principal: _Optional[_Union[_principal__client_pb2.PrincipalBasic, _Mapping]] = ..., description: _Optional[str] = ..., python_version: _Optional[str] = ..., requirements: _Optional[str] = ..., resolved_requirements: _Optional[str] = ..., s3_wheels_location: _Optional[str] = ..., feature_services: _Optional[_Iterable[_Union[DependentFeatureService, _Mapping]]] = ..., realtime_job_environment: _Optional[_Union[RealtimeEnvironment, _Mapping]] = ..., rift_batch_job_environment: _Optional[_Union[RiftBatchEnvironment, _Mapping]] = ..., supported_job_environments: _Optional[_Iterable[_Union[JobEnvironment, str]]] = ..., sdk_version: _Optional[str] = ..., status_details: _Optional[str] = ...) -> None: ...

class RemoteEnvironmentUploadInfo(_message.Message):
    __slots__ = ["environment_id", "s3_upload_info"]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    S3_UPLOAD_INFO_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    s3_upload_info: S3UploadInfo
    def __init__(self, environment_id: _Optional[str] = ..., s3_upload_info: _Optional[_Union[S3UploadInfo, _Mapping]] = ...) -> None: ...

class RiftBatchEnvironment(_message.Message):
    __slots__ = ["cluster_environment_build_id", "image_info", "tecton_materialization_runtime_version"]
    CLUSTER_ENVIRONMENT_BUILD_ID_FIELD_NUMBER: _ClassVar[int]
    IMAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    TECTON_MATERIALIZATION_RUNTIME_VERSION_FIELD_NUMBER: _ClassVar[int]
    cluster_environment_build_id: str
    image_info: _container_image__client_pb2.ContainerImage
    tecton_materialization_runtime_version: str
    def __init__(self, tecton_materialization_runtime_version: _Optional[str] = ..., image_info: _Optional[_Union[_container_image__client_pb2.ContainerImage, _Mapping]] = ..., cluster_environment_build_id: _Optional[str] = ...) -> None: ...

class S3UploadInfo(_message.Message):
    __slots__ = ["upload_id", "upload_parts"]
    UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_PARTS_FIELD_NUMBER: _ClassVar[int]
    upload_id: str
    upload_parts: _containers.RepeatedCompositeFieldContainer[S3UploadPart]
    def __init__(self, upload_id: _Optional[str] = ..., upload_parts: _Optional[_Iterable[_Union[S3UploadPart, _Mapping]]] = ...) -> None: ...

class S3UploadPart(_message.Message):
    __slots__ = ["e_tag", "parent_upload_id", "part_number", "upload_url"]
    E_TAG_FIELD_NUMBER: _ClassVar[int]
    PARENT_UPLOAD_ID_FIELD_NUMBER: _ClassVar[int]
    PART_NUMBER_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    e_tag: str
    parent_upload_id: str
    part_number: int
    upload_url: str
    def __init__(self, parent_upload_id: _Optional[str] = ..., part_number: _Optional[int] = ..., e_tag: _Optional[str] = ..., upload_url: _Optional[str] = ...) -> None: ...

class JobEnvironment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class RemoteEnvironmentStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class RemoteComputeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
