from chalk._gen.chalk.artifacts.v1 import export_pb2 as _export_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
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

class FeatureSQL(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "deployment_id",
        "fqn",
        "name",
        "namespace",
        "max_staleness",
        "etl_offline_to_online",
        "description",
        "owner",
        "tags",
        "kind_enum",
        "kind",
        "was_reset",
        "internal_version",
        "is_singleton",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    FQN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    MAX_STALENESS_FIELD_NUMBER: _ClassVar[int]
    ETL_OFFLINE_TO_ONLINE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    KIND_ENUM_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    WAS_RESET_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_VERSION_FIELD_NUMBER: _ClassVar[int]
    IS_SINGLETON_FIELD_NUMBER: _ClassVar[int]
    id: int
    environment_id: str
    deployment_id: str
    fqn: str
    name: str
    namespace: str
    max_staleness: str
    etl_offline_to_online: bool
    description: str
    owner: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    kind_enum: str
    kind: str
    was_reset: bool
    internal_version: int
    is_singleton: bool
    def __init__(
        self,
        id: _Optional[int] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        fqn: _Optional[str] = ...,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        max_staleness: _Optional[str] = ...,
        etl_offline_to_online: bool = ...,
        description: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        kind_enum: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        was_reset: bool = ...,
        internal_version: _Optional[int] = ...,
        is_singleton: bool = ...,
    ) -> None: ...

class GetFeatureSQLResponse(_message.Message):
    __slots__ = ("features",)
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedCompositeFieldContainer[FeatureSQL]
    def __init__(self, features: _Optional[_Iterable[_Union[FeatureSQL, _Mapping]]] = ...) -> None: ...

class GetFeatureSQLRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class FeatureMetadata(_message.Message):
    __slots__ = ("fqn", "name", "namespace", "description", "owner", "tags", "max_staleness", "etl_offline_to_online")
    FQN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    MAX_STALENESS_FIELD_NUMBER: _ClassVar[int]
    ETL_OFFLINE_TO_ONLINE_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    name: str
    namespace: str
    description: str
    owner: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    max_staleness: str
    etl_offline_to_online: bool
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        description: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        max_staleness: _Optional[str] = ...,
        etl_offline_to_online: bool = ...,
    ) -> None: ...

class GetFeaturesMetadataResponse(_message.Message):
    __slots__ = ("features", "environment_id", "deployment_id")
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedCompositeFieldContainer[FeatureMetadata]
    environment_id: str
    deployment_id: str
    def __init__(
        self,
        features: _Optional[_Iterable[_Union[FeatureMetadata, _Mapping]]] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
    ) -> None: ...

class GetFeaturesMetadataRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateGraphRequest(_message.Message):
    __slots__ = ("deployment_id", "graph", "chalkpy_version", "tag", "export")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    CHALKPY_VERSION_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    graph: _graph_pb2.Graph
    chalkpy_version: str
    tag: str
    export: _export_pb2.Export
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        graph: _Optional[_Union[_graph_pb2.Graph, _Mapping]] = ...,
        chalkpy_version: _Optional[str] = ...,
        tag: _Optional[str] = ...,
        export: _Optional[_Union[_export_pb2.Export, _Mapping]] = ...,
    ) -> None: ...

class UpdateGraphResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetGraphRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class GetGraphResponse(_message.Message):
    __slots__ = ("graph", "chalkpy_version", "tag", "export")
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    CHALKPY_VERSION_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    graph: _graph_pb2.Graph
    chalkpy_version: str
    tag: str
    export: _export_pb2.Export
    def __init__(
        self,
        graph: _Optional[_Union[_graph_pb2.Graph, _Mapping]] = ...,
        chalkpy_version: _Optional[str] = ...,
        tag: _Optional[str] = ...,
        export: _Optional[_Union[_export_pb2.Export, _Mapping]] = ...,
    ) -> None: ...

class PythonVersion(_message.Message):
    __slots__ = ("major", "minor", "patch")
    MAJOR_FIELD_NUMBER: _ClassVar[int]
    MINOR_FIELD_NUMBER: _ClassVar[int]
    PATCH_FIELD_NUMBER: _ClassVar[int]
    major: int
    minor: int
    patch: int
    def __init__(
        self, major: _Optional[int] = ..., minor: _Optional[int] = ..., patch: _Optional[int] = ...
    ) -> None: ...

class GetCodegenFeaturesFromGraphRequest(_message.Message):
    __slots__ = ("deployment_id", "branch", "python_version")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    PYTHON_VERSION_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    branch: str
    python_version: PythonVersion
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        branch: _Optional[str] = ...,
        python_version: _Optional[_Union[PythonVersion, _Mapping]] = ...,
    ) -> None: ...

class GetCodegenFeaturesFromGraphResponse(_message.Message):
    __slots__ = ("codegen", "errors")
    CODEGEN_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    codegen: str
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        codegen: _Optional[str] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...
