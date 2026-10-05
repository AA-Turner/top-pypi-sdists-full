from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.container.v1 import service_pb2 as _service_pb2
from chalk._gen.chalk.externalfunctioncatalog.v1 import service_pb2 as _service_pb2_1
from chalk._gen.chalk.models.v1 import model_version_pb2 as _model_version_pb2
from chalk._gen.chalk.runtime.v1 import remote_python_call_pb2 as _remote_python_call_pb2
from chalk._gen.chalk.scalinggroup.v1 import service_pb2 as _service_pb2_1_1
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
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

class ModelScalingGroupSortColumn(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODEL_SCALING_GROUP_SORT_COLUMN_UNSPECIFIED: _ClassVar[ModelScalingGroupSortColumn]
    MODEL_SCALING_GROUP_SORT_COLUMN_CREATED_AT: _ClassVar[ModelScalingGroupSortColumn]
    MODEL_SCALING_GROUP_SORT_COLUMN_UPDATED_AT: _ClassVar[ModelScalingGroupSortColumn]

class ModelScalingGroupSortOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MODEL_SCALING_GROUP_SORT_ORDER_UNSPECIFIED: _ClassVar[ModelScalingGroupSortOrder]
    MODEL_SCALING_GROUP_SORT_ORDER_DESC: _ClassVar[ModelScalingGroupSortOrder]
    MODEL_SCALING_GROUP_SORT_ORDER_ASC: _ClassVar[ModelScalingGroupSortOrder]

MODEL_SCALING_GROUP_SORT_COLUMN_UNSPECIFIED: ModelScalingGroupSortColumn
MODEL_SCALING_GROUP_SORT_COLUMN_CREATED_AT: ModelScalingGroupSortColumn
MODEL_SCALING_GROUP_SORT_COLUMN_UPDATED_AT: ModelScalingGroupSortColumn
MODEL_SCALING_GROUP_SORT_ORDER_UNSPECIFIED: ModelScalingGroupSortOrder
MODEL_SCALING_GROUP_SORT_ORDER_DESC: ModelScalingGroupSortOrder
MODEL_SCALING_GROUP_SORT_ORDER_ASC: ModelScalingGroupSortOrder

class ModelContainerSpec(_message.Message):
    __slots__ = (
        "tags",
        "resources",
        "env_vars",
        "volumes",
        "routing",
        "authentication",
        "secret_refs",
        "readiness_probe",
        "startup_probe",
        "chalk_workload_identity",
    )
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class EnvVarsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    TAGS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    ENV_VARS_FIELD_NUMBER: _ClassVar[int]
    VOLUMES_FIELD_NUMBER: _ClassVar[int]
    ROUTING_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_FIELD_NUMBER: _ClassVar[int]
    SECRET_REFS_FIELD_NUMBER: _ClassVar[int]
    READINESS_PROBE_FIELD_NUMBER: _ClassVar[int]
    STARTUP_PROBE_FIELD_NUMBER: _ClassVar[int]
    CHALK_WORKLOAD_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.ScalarMap[str, str]
    resources: _service_pb2.ResourceLimits
    env_vars: _containers.ScalarMap[str, str]
    volumes: _containers.RepeatedCompositeFieldContainer[_service_pb2.VolumeMount]
    routing: str
    authentication: str
    secret_refs: _containers.RepeatedCompositeFieldContainer[_service_pb2.SecretRef]
    readiness_probe: _service_pb2.ReadinessProbe
    startup_probe: _service_pb2.StartupProbe
    chalk_workload_identity: _service_pb2.ChalkWorkloadIdentity
    def __init__(
        self,
        tags: _Optional[_Mapping[str, str]] = ...,
        resources: _Optional[_Union[_service_pb2.ResourceLimits, _Mapping]] = ...,
        env_vars: _Optional[_Mapping[str, str]] = ...,
        volumes: _Optional[_Iterable[_Union[_service_pb2.VolumeMount, _Mapping]]] = ...,
        routing: _Optional[str] = ...,
        authentication: _Optional[str] = ...,
        secret_refs: _Optional[_Iterable[_Union[_service_pb2.SecretRef, _Mapping]]] = ...,
        readiness_probe: _Optional[_Union[_service_pb2.ReadinessProbe, _Mapping]] = ...,
        startup_probe: _Optional[_Union[_service_pb2.StartupProbe, _Mapping]] = ...,
        chalk_workload_identity: _Optional[_Union[_service_pb2.ChalkWorkloadIdentity, _Mapping]] = ...,
    ) -> None: ...

class CreateModelScalingGroupRequest(_message.Message):
    __slots__ = ("name", "spec", "model_name", "identifier", "container_spec", "scaling_spec", "handler", "image")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_SPEC_FIELD_NUMBER: _ClassVar[int]
    SCALING_SPEC_FIELD_NUMBER: _ClassVar[int]
    HANDLER_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    name: str
    spec: ModelScalingGroupSpec
    model_name: str
    identifier: _model_version_pb2.ModelVersionIdentifier
    container_spec: ModelContainerSpec
    scaling_spec: _service_pb2_1_1.ScalingSpec
    handler: str
    image: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        spec: _Optional[_Union[ModelScalingGroupSpec, _Mapping]] = ...,
        model_name: _Optional[str] = ...,
        identifier: _Optional[_Union[_model_version_pb2.ModelVersionIdentifier, _Mapping]] = ...,
        container_spec: _Optional[_Union[ModelContainerSpec, _Mapping]] = ...,
        scaling_spec: _Optional[_Union[_service_pb2_1_1.ScalingSpec, _Mapping]] = ...,
        handler: _Optional[str] = ...,
        image: _Optional[str] = ...,
    ) -> None: ...

class CreateModelScalingGroupResponse(_message.Message):
    __slots__ = ("scaling_group", "model_scaling_group", "current_revision")
    SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    MODEL_SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    CURRENT_REVISION_FIELD_NUMBER: _ClassVar[int]
    scaling_group: _service_pb2_1_1.ScalingGroupResponse
    model_scaling_group: ModelScalingGroup
    current_revision: ModelScalingGroupRevision
    def __init__(
        self,
        scaling_group: _Optional[_Union[_service_pb2_1_1.ScalingGroupResponse, _Mapping]] = ...,
        model_scaling_group: _Optional[_Union[ModelScalingGroup, _Mapping]] = ...,
        current_revision: _Optional[_Union[ModelScalingGroupRevision, _Mapping]] = ...,
    ) -> None: ...

class ModelVersionSelector(_message.Message):
    __slots__ = ("model_name", "identifier")
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    identifier: _model_version_pb2.ModelVersionIdentifier
    def __init__(
        self,
        model_name: _Optional[str] = ...,
        identifier: _Optional[_Union[_model_version_pb2.ModelVersionIdentifier, _Mapping]] = ...,
    ) -> None: ...

class ModelScalingGroupSpec(_message.Message):
    __slots__ = ("model_version", "container_spec", "scaling_spec", "handler", "image", "retry_policy", "queue_policy")
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_SPEC_FIELD_NUMBER: _ClassVar[int]
    SCALING_SPEC_FIELD_NUMBER: _ClassVar[int]
    HANDLER_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    RETRY_POLICY_FIELD_NUMBER: _ClassVar[int]
    QUEUE_POLICY_FIELD_NUMBER: _ClassVar[int]
    model_version: ModelVersionSelector
    container_spec: ModelContainerSpec
    scaling_spec: _service_pb2_1_1.ScalingSpec
    handler: str
    image: str
    retry_policy: _service_pb2_1.RetryPolicy
    queue_policy: _service_pb2_1.QueuePolicy
    def __init__(
        self,
        model_version: _Optional[_Union[ModelVersionSelector, _Mapping]] = ...,
        container_spec: _Optional[_Union[ModelContainerSpec, _Mapping]] = ...,
        scaling_spec: _Optional[_Union[_service_pb2_1_1.ScalingSpec, _Mapping]] = ...,
        handler: _Optional[str] = ...,
        image: _Optional[str] = ...,
        retry_policy: _Optional[_Union[_service_pb2_1.RetryPolicy, _Mapping]] = ...,
        queue_policy: _Optional[_Union[_service_pb2_1.QueuePolicy, _Mapping]] = ...,
    ) -> None: ...

class ModelScalingGroup(_message.Message):
    __slots__ = (
        "id",
        "name",
        "queue_name",
        "model_id",
        "created_by",
        "created_at",
        "status",
        "status_message",
        "status_details",
        "ready_replicas",
        "available_replicas",
        "revision_id",
        "updated_at",
        "deleted_at",
        "web_url",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUEUE_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_DETAILS_FIELD_NUMBER: _ClassVar[int]
    READY_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    WEB_URL_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    queue_name: str
    model_id: str
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    status: str
    status_message: str
    status_details: str
    ready_replicas: int
    available_replicas: int
    revision_id: str
    updated_at: _timestamp_pb2.Timestamp
    deleted_at: _timestamp_pb2.Timestamp
    web_url: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        queue_name: _Optional[str] = ...,
        model_id: _Optional[str] = ...,
        created_by: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        status: _Optional[str] = ...,
        status_message: _Optional[str] = ...,
        status_details: _Optional[str] = ...,
        ready_replicas: _Optional[int] = ...,
        available_replicas: _Optional[int] = ...,
        revision_id: _Optional[str] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        deleted_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        web_url: _Optional[str] = ...,
    ) -> None: ...

class ModelScalingGroupRevision(_message.Message):
    __slots__ = ("id", "model_scaling_group_id", "model_version", "spec", "created_by", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_SCALING_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    model_scaling_group_id: str
    model_version: int
    spec: ModelScalingGroupSpec
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        model_scaling_group_id: _Optional[str] = ...,
        model_version: _Optional[int] = ...,
        spec: _Optional[_Union[ModelScalingGroupSpec, _Mapping]] = ...,
        created_by: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ModelScalingGroupTraffic(_message.Message):
    __slots__ = ("targets",)
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    targets: _containers.RepeatedCompositeFieldContainer[ModelScalingGroupTrafficTarget]
    def __init__(
        self, targets: _Optional[_Iterable[_Union[ModelScalingGroupTrafficTarget, _Mapping]]] = ...
    ) -> None: ...

class ModelScalingGroupTrafficTarget(_message.Message):
    __slots__ = ("model_scaling_group_revision_id", "latest_revision", "percent")
    MODEL_SCALING_GROUP_REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    LATEST_REVISION_FIELD_NUMBER: _ClassVar[int]
    PERCENT_FIELD_NUMBER: _ClassVar[int]
    model_scaling_group_revision_id: str
    latest_revision: _empty_pb2.Empty
    percent: int
    def __init__(
        self,
        model_scaling_group_revision_id: _Optional[str] = ...,
        latest_revision: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...,
        percent: _Optional[int] = ...,
    ) -> None: ...

class UpdateModelScalingGroupRequest(_message.Message):
    __slots__ = ("model_scaling_group_id", "model_scaling_group_name", "spec", "traffic", "update_mask")
    MODEL_SCALING_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_SCALING_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    model_scaling_group_id: str
    model_scaling_group_name: str
    spec: ModelScalingGroupSpec
    traffic: ModelScalingGroupTraffic
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        model_scaling_group_id: _Optional[str] = ...,
        model_scaling_group_name: _Optional[str] = ...,
        spec: _Optional[_Union[ModelScalingGroupSpec, _Mapping]] = ...,
        traffic: _Optional[_Union[ModelScalingGroupTraffic, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateModelScalingGroupResponse(_message.Message):
    __slots__ = ("scaling_group", "model_scaling_group", "current_revision")
    SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    MODEL_SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    CURRENT_REVISION_FIELD_NUMBER: _ClassVar[int]
    scaling_group: _service_pb2_1_1.ScalingGroupResponse
    model_scaling_group: ModelScalingGroup
    current_revision: ModelScalingGroupRevision
    def __init__(
        self,
        scaling_group: _Optional[_Union[_service_pb2_1_1.ScalingGroupResponse, _Mapping]] = ...,
        model_scaling_group: _Optional[_Union[ModelScalingGroup, _Mapping]] = ...,
        current_revision: _Optional[_Union[ModelScalingGroupRevision, _Mapping]] = ...,
    ) -> None: ...

class GetModelScalingGroupRequest(_message.Message):
    __slots__ = ("model_scaling_group_id", "model_scaling_group_name", "include_deleted")
    MODEL_SCALING_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_SCALING_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DELETED_FIELD_NUMBER: _ClassVar[int]
    model_scaling_group_id: str
    model_scaling_group_name: str
    include_deleted: bool
    def __init__(
        self,
        model_scaling_group_id: _Optional[str] = ...,
        model_scaling_group_name: _Optional[str] = ...,
        include_deleted: bool = ...,
    ) -> None: ...

class GetModelScalingGroupResponse(_message.Message):
    __slots__ = ("scaling_group", "model_scaling_group", "current_revision")
    SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    MODEL_SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    CURRENT_REVISION_FIELD_NUMBER: _ClassVar[int]
    scaling_group: _service_pb2_1_1.ScalingGroupResponse
    model_scaling_group: ModelScalingGroup
    current_revision: ModelScalingGroupRevision
    def __init__(
        self,
        scaling_group: _Optional[_Union[_service_pb2_1_1.ScalingGroupResponse, _Mapping]] = ...,
        model_scaling_group: _Optional[_Union[ModelScalingGroup, _Mapping]] = ...,
        current_revision: _Optional[_Union[ModelScalingGroupRevision, _Mapping]] = ...,
    ) -> None: ...

class ListModelScalingGroupsRequest(_message.Message):
    __slots__ = (
        "model_version",
        "cursor",
        "limit",
        "include_deleted",
        "filters",
        "search",
        "sort_column",
        "sort_order",
    )
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DELETED_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    SORT_COLUMN_FIELD_NUMBER: _ClassVar[int]
    SORT_ORDER_FIELD_NUMBER: _ClassVar[int]
    model_version: ModelVersionSelector
    cursor: str
    limit: int
    include_deleted: bool
    filters: ListModelScalingGroupsFilters
    search: str
    sort_column: ModelScalingGroupSortColumn
    sort_order: ModelScalingGroupSortOrder
    def __init__(
        self,
        model_version: _Optional[_Union[ModelVersionSelector, _Mapping]] = ...,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        include_deleted: bool = ...,
        filters: _Optional[_Union[ListModelScalingGroupsFilters, _Mapping]] = ...,
        search: _Optional[str] = ...,
        sort_column: _Optional[_Union[ModelScalingGroupSortColumn, str]] = ...,
        sort_order: _Optional[_Union[ModelScalingGroupSortOrder, str]] = ...,
    ) -> None: ...

class ListModelScalingGroupsFilters(_message.Message):
    __slots__ = ("statuses", "images", "model_name")
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    statuses: _containers.RepeatedScalarFieldContainer[str]
    images: _containers.RepeatedScalarFieldContainer[str]
    model_name: str
    def __init__(
        self,
        statuses: _Optional[_Iterable[str]] = ...,
        images: _Optional[_Iterable[str]] = ...,
        model_name: _Optional[str] = ...,
    ) -> None: ...

class ListModelScalingGroupsResponse(_message.Message):
    __slots__ = ("scaling_groups", "next_cursor", "model_scaling_groups", "current_revisions")
    SCALING_GROUPS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    MODEL_SCALING_GROUPS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_REVISIONS_FIELD_NUMBER: _ClassVar[int]
    scaling_groups: _containers.RepeatedCompositeFieldContainer[_service_pb2_1_1.ScalingGroupResponse]
    next_cursor: str
    model_scaling_groups: _containers.RepeatedCompositeFieldContainer[ModelScalingGroup]
    current_revisions: _containers.RepeatedCompositeFieldContainer[ModelScalingGroupRevision]
    def __init__(
        self,
        scaling_groups: _Optional[_Iterable[_Union[_service_pb2_1_1.ScalingGroupResponse, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
        model_scaling_groups: _Optional[_Iterable[_Union[ModelScalingGroup, _Mapping]]] = ...,
        current_revisions: _Optional[_Iterable[_Union[ModelScalingGroupRevision, _Mapping]]] = ...,
    ) -> None: ...

class DeleteModelScalingGroupRequest(_message.Message):
    __slots__ = ("model_scaling_group_id", "model_scaling_group_name")
    MODEL_SCALING_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_SCALING_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    model_scaling_group_id: str
    model_scaling_group_name: str
    def __init__(
        self, model_scaling_group_id: _Optional[str] = ..., model_scaling_group_name: _Optional[str] = ...
    ) -> None: ...

class DeleteModelScalingGroupResponse(_message.Message):
    __slots__ = ("scaling_group", "model_scaling_group")
    SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    MODEL_SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    scaling_group: _service_pb2_1_1.ScalingGroupResponse
    model_scaling_group: ModelScalingGroup
    def __init__(
        self,
        scaling_group: _Optional[_Union[_service_pb2_1_1.ScalingGroupResponse, _Mapping]] = ...,
        model_scaling_group: _Optional[_Union[ModelScalingGroup, _Mapping]] = ...,
    ) -> None: ...

class GetModelScalingGroupRevisionRequest(_message.Message):
    __slots__ = ("model_scaling_group_id", "model_scaling_group_name", "revision_id", "include_deleted")
    MODEL_SCALING_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_SCALING_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DELETED_FIELD_NUMBER: _ClassVar[int]
    model_scaling_group_id: str
    model_scaling_group_name: str
    revision_id: str
    include_deleted: bool
    def __init__(
        self,
        model_scaling_group_id: _Optional[str] = ...,
        model_scaling_group_name: _Optional[str] = ...,
        revision_id: _Optional[str] = ...,
        include_deleted: bool = ...,
    ) -> None: ...

class GetModelScalingGroupRevisionResponse(_message.Message):
    __slots__ = ("revision", "model_revision")
    REVISION_FIELD_NUMBER: _ClassVar[int]
    MODEL_REVISION_FIELD_NUMBER: _ClassVar[int]
    revision: _service_pb2_1_1.ScalingGroupRevisionResponse
    model_revision: ModelScalingGroupRevision
    def __init__(
        self,
        revision: _Optional[_Union[_service_pb2_1_1.ScalingGroupRevisionResponse, _Mapping]] = ...,
        model_revision: _Optional[_Union[ModelScalingGroupRevision, _Mapping]] = ...,
    ) -> None: ...

class ListModelScalingGroupRevisionsRequest(_message.Message):
    __slots__ = ("model_scaling_group_id", "model_scaling_group_name", "cursor", "limit", "include_deleted")
    MODEL_SCALING_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_SCALING_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DELETED_FIELD_NUMBER: _ClassVar[int]
    model_scaling_group_id: str
    model_scaling_group_name: str
    cursor: str
    limit: int
    include_deleted: bool
    def __init__(
        self,
        model_scaling_group_id: _Optional[str] = ...,
        model_scaling_group_name: _Optional[str] = ...,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        include_deleted: bool = ...,
    ) -> None: ...

class ListModelScalingGroupRevisionsResponse(_message.Message):
    __slots__ = ("revisions", "next_cursor", "model_revisions")
    REVISIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    MODEL_REVISIONS_FIELD_NUMBER: _ClassVar[int]
    revisions: _containers.RepeatedCompositeFieldContainer[_service_pb2_1_1.ScalingGroupRevisionResponse]
    next_cursor: str
    model_revisions: _containers.RepeatedCompositeFieldContainer[ModelScalingGroupRevision]
    def __init__(
        self,
        revisions: _Optional[_Iterable[_Union[_service_pb2_1_1.ScalingGroupRevisionResponse, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
        model_revisions: _Optional[_Iterable[_Union[ModelScalingGroupRevision, _Mapping]]] = ...,
    ) -> None: ...

class CallModelRequest(_message.Message):
    __slots__ = (
        "model_version",
        "model_scaling_group_id",
        "model_scaling_group_name",
        "remote_call_request",
        "enqueue_remote_call_request",
    )
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    MODEL_SCALING_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_SCALING_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    REMOTE_CALL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    ENQUEUE_REMOTE_CALL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    model_version: ModelVersionSelector
    model_scaling_group_id: str
    model_scaling_group_name: str
    remote_call_request: _remote_python_call_pb2.CallFunctionRequest
    enqueue_remote_call_request: _remote_python_call_pb2.EnqueueRemoteCallRequest
    def __init__(
        self,
        model_version: _Optional[_Union[ModelVersionSelector, _Mapping]] = ...,
        model_scaling_group_id: _Optional[str] = ...,
        model_scaling_group_name: _Optional[str] = ...,
        remote_call_request: _Optional[_Union[_remote_python_call_pb2.CallFunctionRequest, _Mapping]] = ...,
        enqueue_remote_call_request: _Optional[
            _Union[_remote_python_call_pb2.EnqueueRemoteCallRequest, _Mapping]
        ] = ...,
    ) -> None: ...

class CallModelResponse(_message.Message):
    __slots__ = ("remote_call_response", "enqueue_remote_call_response")
    REMOTE_CALL_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ENQUEUE_REMOTE_CALL_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    remote_call_response: _remote_python_call_pb2.CallFunctionResponse
    enqueue_remote_call_response: _remote_python_call_pb2.EnqueueRemoteCallResponse
    def __init__(
        self,
        remote_call_response: _Optional[_Union[_remote_python_call_pb2.CallFunctionResponse, _Mapping]] = ...,
        enqueue_remote_call_response: _Optional[
            _Union[_remote_python_call_pb2.EnqueueRemoteCallResponse, _Mapping]
        ] = ...,
    ) -> None: ...
