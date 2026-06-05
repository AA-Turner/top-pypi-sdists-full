from chalk._gen.chalk.models.v1 import model_version_pb2 as _model_version_pb2
from chalk._gen.chalk.server.v1 import deployment_pb2 as _deployment_pb2
from chalk._gen.chalk.server.v1 import environment_pb2 as _environment_pb2
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

class DeploymentRevisionTrigger(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEPLOYMENT_REVISION_TRIGGER_UNSPECIFIED: _ClassVar[DeploymentRevisionTrigger]
    DEPLOYMENT_REVISION_TRIGGER_APPLY: _ClassVar[DeploymentRevisionTrigger]
    DEPLOYMENT_REVISION_TRIGGER_REDEPLOY: _ClassVar[DeploymentRevisionTrigger]
    DEPLOYMENT_REVISION_TRIGGER_REBUILD: _ClassVar[DeploymentRevisionTrigger]
    DEPLOYMENT_REVISION_TRIGGER_PATCH: _ClassVar[DeploymentRevisionTrigger]
    DEPLOYMENT_REVISION_TRIGGER_SET_TAG_WEIGHTS: _ClassVar[DeploymentRevisionTrigger]
    DEPLOYMENT_REVISION_TRIGGER_SUSPEND: _ClassVar[DeploymentRevisionTrigger]
    DEPLOYMENT_REVISION_TRIGGER_RESUME: _ClassVar[DeploymentRevisionTrigger]

DEPLOYMENT_REVISION_TRIGGER_UNSPECIFIED: DeploymentRevisionTrigger
DEPLOYMENT_REVISION_TRIGGER_APPLY: DeploymentRevisionTrigger
DEPLOYMENT_REVISION_TRIGGER_REDEPLOY: DeploymentRevisionTrigger
DEPLOYMENT_REVISION_TRIGGER_REBUILD: DeploymentRevisionTrigger
DEPLOYMENT_REVISION_TRIGGER_PATCH: DeploymentRevisionTrigger
DEPLOYMENT_REVISION_TRIGGER_SET_TAG_WEIGHTS: DeploymentRevisionTrigger
DEPLOYMENT_REVISION_TRIGGER_SUSPEND: DeploymentRevisionTrigger
DEPLOYMENT_REVISION_TRIGGER_RESUME: DeploymentRevisionTrigger

class DeploymentRevisionIntegration(_message.Message):
    __slots__ = ("id", "kind", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    kind: str
    name: str
    def __init__(self, id: _Optional[str] = ..., kind: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class DeploymentRevisionIntegrationSecret(_message.Message):
    __slots__ = ("id", "integration_id", "environment_secret_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    integration_id: str
    environment_secret_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        integration_id: _Optional[str] = ...,
        environment_secret_id: _Optional[str] = ...,
    ) -> None: ...

class DeploymentRevisionEnvironmentSecret(_message.Message):
    __slots__ = ("id", "secret_store_id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_STORE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    secret_store_id: str
    name: str
    def __init__(
        self, id: _Optional[str] = ..., secret_store_id: _Optional[str] = ..., name: _Optional[str] = ...
    ) -> None: ...

class DeploymentRevisionSpec(_message.Message):
    __slots__ = (
        "environment",
        "deployment",
        "integrations",
        "integration_secrets",
        "environment_secrets",
        "mounted_model_specs",
        "model_endpoint_config_json",
        "feature_flags",
        "api_server_commit_sha",
    )
    class FeatureFlagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bool
        def __init__(self, key: _Optional[str] = ..., value: bool = ...) -> None: ...

    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_SECRETS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_SECRETS_FIELD_NUMBER: _ClassVar[int]
    MOUNTED_MODEL_SPECS_FIELD_NUMBER: _ClassVar[int]
    MODEL_ENDPOINT_CONFIG_JSON_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    API_SERVER_COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    environment: _environment_pb2.Environment
    deployment: _deployment_pb2.Deployment
    integrations: _containers.RepeatedCompositeFieldContainer[DeploymentRevisionIntegration]
    integration_secrets: _containers.RepeatedCompositeFieldContainer[DeploymentRevisionIntegrationSecret]
    environment_secrets: _containers.RepeatedCompositeFieldContainer[DeploymentRevisionEnvironmentSecret]
    mounted_model_specs: _model_version_pb2.MountedModelsSpecs
    model_endpoint_config_json: str
    feature_flags: _containers.ScalarMap[str, bool]
    api_server_commit_sha: str
    def __init__(
        self,
        environment: _Optional[_Union[_environment_pb2.Environment, _Mapping]] = ...,
        deployment: _Optional[_Union[_deployment_pb2.Deployment, _Mapping]] = ...,
        integrations: _Optional[_Iterable[_Union[DeploymentRevisionIntegration, _Mapping]]] = ...,
        integration_secrets: _Optional[_Iterable[_Union[DeploymentRevisionIntegrationSecret, _Mapping]]] = ...,
        environment_secrets: _Optional[_Iterable[_Union[DeploymentRevisionEnvironmentSecret, _Mapping]]] = ...,
        mounted_model_specs: _Optional[_Union[_model_version_pb2.MountedModelsSpecs, _Mapping]] = ...,
        model_endpoint_config_json: _Optional[str] = ...,
        feature_flags: _Optional[_Mapping[str, bool]] = ...,
        api_server_commit_sha: _Optional[str] = ...,
    ) -> None: ...

class DeploymentRevision(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "deployment_id",
        "build_trigger",
        "status",
        "spec",
        "started_at",
        "finished_at",
        "triggered_by",
        "created_at",
        "updated_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    BUILD_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    TRIGGERED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    deployment_id: str
    build_trigger: DeploymentRevisionTrigger
    status: _deployment_pb2.DeploymentStatus
    spec: DeploymentRevisionSpec
    started_at: _timestamp_pb2.Timestamp
    finished_at: _timestamp_pb2.Timestamp
    triggered_by: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        build_trigger: _Optional[_Union[DeploymentRevisionTrigger, str]] = ...,
        status: _Optional[_Union[_deployment_pb2.DeploymentStatus, str]] = ...,
        spec: _Optional[_Union[DeploymentRevisionSpec, _Mapping]] = ...,
        started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        finished_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        triggered_by: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListDeploymentRevisionsRequest(_message.Message):
    __slots__ = ("deployment_id", "cursor", "limit")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    cursor: str
    limit: int
    def __init__(
        self, deployment_id: _Optional[str] = ..., cursor: _Optional[str] = ..., limit: _Optional[int] = ...
    ) -> None: ...

class ListDeploymentRevisionsResponse(_message.Message):
    __slots__ = ("revisions", "next_cursor")
    REVISIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    revisions: _containers.RepeatedCompositeFieldContainer[DeploymentRevision]
    next_cursor: str
    def __init__(
        self,
        revisions: _Optional[_Iterable[_Union[DeploymentRevision, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...
