from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
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

class RawColumnKey(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class FeatureColumnKey(_message.Message):
    __slots__ = ("root_fqn",)
    ROOT_FQN_FIELD_NUMBER: _ClassVar[int]
    root_fqn: str
    def __init__(self, root_fqn: _Optional[str] = ...) -> None: ...

class HasManyFeatureKey(_message.Message):
    __slots__ = ("root_fqn", "df")
    ROOT_FQN_FIELD_NUMBER: _ClassVar[int]
    DF_FIELD_NUMBER: _ClassVar[int]
    root_fqn: str
    df: DataFrame
    def __init__(self, root_fqn: _Optional[str] = ..., df: _Optional[_Union[DataFrame, _Mapping]] = ...) -> None: ...

class DataFrameFeatureKey(_message.Message):
    __slots__ = ("root_namespace", "df")
    ROOT_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    DF_FIELD_NUMBER: _ClassVar[int]
    root_namespace: str
    df: DataFrame
    def __init__(
        self, root_namespace: _Optional[str] = ..., df: _Optional[_Union[DataFrame, _Mapping]] = ...
    ) -> None: ...

class DataFrame(_message.Message):
    __slots__ = ("optional_columns", "required_columns", "limit")
    OPTIONAL_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    optional_columns: _containers.RepeatedCompositeFieldContainer[FeatureColumnKey]
    required_columns: _containers.RepeatedCompositeFieldContainer[FeatureColumnKey]
    limit: int
    def __init__(
        self,
        optional_columns: _Optional[_Iterable[_Union[FeatureColumnKey, _Mapping]]] = ...,
        required_columns: _Optional[_Iterable[_Union[FeatureColumnKey, _Mapping]]] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class ColumnKey(_message.Message):
    __slots__ = ("feature", "raw")
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    RAW_FIELD_NUMBER: _ClassVar[int]
    feature: FeatureColumnKey
    raw: RawColumnKey
    def __init__(
        self,
        feature: _Optional[_Union[FeatureColumnKey, _Mapping]] = ...,
        raw: _Optional[_Union[RawColumnKey, _Mapping]] = ...,
    ) -> None: ...

class TableKey(_message.Message):
    __slots__ = ("has_many", "data_frame")
    HAS_MANY_FIELD_NUMBER: _ClassVar[int]
    DATA_FRAME_FIELD_NUMBER: _ClassVar[int]
    has_many: HasManyFeatureKey
    data_frame: DataFrameFeatureKey
    def __init__(
        self,
        has_many: _Optional[_Union[HasManyFeatureKey, _Mapping]] = ...,
        data_frame: _Optional[_Union[DataFrameFeatureKey, _Mapping]] = ...,
    ) -> None: ...

class Key(_message.Message):
    __slots__ = ("raw_column", "scalar", "has_many", "dataframe")
    RAW_COLUMN_FIELD_NUMBER: _ClassVar[int]
    SCALAR_FIELD_NUMBER: _ClassVar[int]
    HAS_MANY_FIELD_NUMBER: _ClassVar[int]
    DATAFRAME_FIELD_NUMBER: _ClassVar[int]
    raw_column: RawColumnKey
    scalar: FeatureColumnKey
    has_many: HasManyFeatureKey
    dataframe: DataFrameFeatureKey
    def __init__(
        self,
        raw_column: _Optional[_Union[RawColumnKey, _Mapping]] = ...,
        scalar: _Optional[_Union[FeatureColumnKey, _Mapping]] = ...,
        has_many: _Optional[_Union[HasManyFeatureKey, _Mapping]] = ...,
        dataframe: _Optional[_Union[DataFrameFeatureKey, _Mapping]] = ...,
    ) -> None: ...

class PyArrowSchema(_message.Message):
    __slots__ = ("scalars", "groups")
    class TableSchema(_message.Message):
        __slots__ = ("key", "schema")
        class SchemaEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: _arrow_pb2.ArrowType
            def __init__(
                self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...
            ) -> None: ...

        KEY_FIELD_NUMBER: _ClassVar[int]
        SCHEMA_FIELD_NUMBER: _ClassVar[int]
        key: TableKey
        schema: _containers.MessageMap[str, _arrow_pb2.ArrowType]
        def __init__(
            self,
            key: _Optional[_Union[TableKey, _Mapping]] = ...,
            schema: _Optional[_Mapping[str, _arrow_pb2.ArrowType]] = ...,
        ) -> None: ...

    class ColumnSchema(_message.Message):
        __slots__ = ("key", "schema")
        KEY_FIELD_NUMBER: _ClassVar[int]
        SCHEMA_FIELD_NUMBER: _ClassVar[int]
        key: ColumnKey
        schema: _arrow_pb2.ArrowType
        def __init__(
            self,
            key: _Optional[_Union[ColumnKey, _Mapping]] = ...,
            schema: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
        ) -> None: ...

    SCALARS_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    scalars: _containers.RepeatedCompositeFieldContainer[PyArrowSchema.ColumnSchema]
    groups: _containers.RepeatedCompositeFieldContainer[PyArrowSchema.TableSchema]
    def __init__(
        self,
        scalars: _Optional[_Iterable[_Union[PyArrowSchema.ColumnSchema, _Mapping]]] = ...,
        groups: _Optional[_Iterable[_Union[PyArrowSchema.TableSchema, _Mapping]]] = ...,
    ) -> None: ...

class Plan(_message.Message):
    __slots__ = ("nodes", "root_node_idx", "pyarrow_schema")
    NODES_FIELD_NUMBER: _ClassVar[int]
    ROOT_NODE_IDX_FIELD_NUMBER: _ClassVar[int]
    PYARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[Node]
    root_node_idx: int
    pyarrow_schema: PyArrowSchema
    def __init__(
        self,
        nodes: _Optional[_Iterable[_Union[Node, _Mapping]]] = ...,
        root_node_idx: _Optional[int] = ...,
        pyarrow_schema: _Optional[_Union[PyArrowSchema, _Mapping]] = ...,
    ) -> None: ...

class Node(_message.Message):
    __slots__ = ("children_indices", "impl")
    CHILDREN_INDICES_FIELD_NUMBER: _ClassVar[int]
    IMPL_FIELD_NUMBER: _ClassVar[int]
    children_indices: _containers.RepeatedScalarFieldContainer[int]
    impl: NodeImpl
    def __init__(
        self, children_indices: _Optional[_Iterable[int]] = ..., impl: _Optional[_Union[NodeImpl, _Mapping]] = ...
    ) -> None: ...

class NodeImpl(_message.Message):
    __slots__ = ("unknown", "givens_scan", "project", "chalk_project", "default_injector")
    UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    GIVENS_SCAN_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    CHALK_PROJECT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_INJECTOR_FIELD_NUMBER: _ClassVar[int]
    unknown: UnknownNode
    givens_scan: GivensScan
    project: Project
    chalk_project: ChalkProject
    default_injector: DefaultInjector
    def __init__(
        self,
        unknown: _Optional[_Union[UnknownNode, _Mapping]] = ...,
        givens_scan: _Optional[_Union[GivensScan, _Mapping]] = ...,
        project: _Optional[_Union[Project, _Mapping]] = ...,
        chalk_project: _Optional[_Union[ChalkProject, _Mapping]] = ...,
        default_injector: _Optional[_Union[DefaultInjector, _Mapping]] = ...,
    ) -> None: ...

class UnknownNode(_message.Message):
    __slots__ = ("type_name",)
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    type_name: str
    def __init__(self, type_name: _Optional[str] = ...) -> None: ...

class GivensScan(_message.Message):
    __slots__ = ("fields",)
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[Key]
    def __init__(self, fields: _Optional[_Iterable[_Union[Key, _Mapping]]] = ...) -> None: ...

class ChalkProject(_message.Message):
    __slots__ = ("fields", "promote_ts_to_feature_time")
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    PROMOTE_TS_TO_FEATURE_TIME_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[Key]
    promote_ts_to_feature_time: bool
    def __init__(
        self, fields: _Optional[_Iterable[_Union[Key, _Mapping]]] = ..., promote_ts_to_feature_time: bool = ...
    ) -> None: ...

class Project(_message.Message):
    __slots__ = ("fields",)
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[Key]
    def __init__(self, fields: _Optional[_Iterable[_Union[Key, _Mapping]]] = ...) -> None: ...

class DefaultInjector(_message.Message):
    __slots__ = ("defaulting_features",)
    DEFAULTING_FEATURES_FIELD_NUMBER: _ClassVar[int]
    defaulting_features: _containers.RepeatedCompositeFieldContainer[Key]
    def __init__(self, defaulting_features: _Optional[_Iterable[_Union[Key, _Mapping]]] = ...) -> None: ...
