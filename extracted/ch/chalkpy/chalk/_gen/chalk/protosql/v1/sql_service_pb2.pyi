from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
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

class ExecuteSqlQueryRequest(_message.Message):
    __slots__ = ("query",)
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: str
    def __init__(self, query: _Optional[str] = ...) -> None: ...

class ExecuteSqlQueryResponse(_message.Message):
    __slots__ = ("query_id", "parquet", "errors")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    PARQUET_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    parquet: bytes
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        query_id: _Optional[str] = ...,
        parquet: _Optional[bytes] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class PlanSqlQueryRequest(_message.Message):
    __slots__ = ("query",)
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: str
    def __init__(self, query: _Optional[str] = ...) -> None: ...

class PlanSqlQueryResponse(_message.Message):
    __slots__ = ("logical_plan", "errors")
    LOGICAL_PLAN_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    logical_plan: str
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        logical_plan: _Optional[str] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class GetDbCatalogsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDbCatalogsResponse(_message.Message):
    __slots__ = ("catalog_names", "errors")
    CATALOG_NAMES_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    catalog_names: _containers.RepeatedScalarFieldContainer[str]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        catalog_names: _Optional[_Iterable[str]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class GetDbSchemasRequest(_message.Message):
    __slots__ = ("catalog", "db_schema_filter_pattern", "errors")
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    DB_SCHEMA_FILTER_PATTERN_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    catalog: str
    db_schema_filter_pattern: str
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        catalog: _Optional[str] = ...,
        db_schema_filter_pattern: _Optional[str] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class DbSchemaInfo(_message.Message):
    __slots__ = ("catalog_name", "db_schema_name")
    CATALOG_NAME_FIELD_NUMBER: _ClassVar[int]
    DB_SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    catalog_name: str
    db_schema_name: str
    def __init__(self, catalog_name: _Optional[str] = ..., db_schema_name: _Optional[str] = ...) -> None: ...

class GetDbSchemasResponse(_message.Message):
    __slots__ = ("schemas", "errors")
    SCHEMAS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    schemas: _containers.RepeatedCompositeFieldContainer[DbSchemaInfo]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        schemas: _Optional[_Iterable[_Union[DbSchemaInfo, _Mapping]]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class GetTablesRequest(_message.Message):
    __slots__ = ("catalog", "db_schema_filter_pattern", "table_name_filter_pattern")
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    DB_SCHEMA_FILTER_PATTERN_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FILTER_PATTERN_FIELD_NUMBER: _ClassVar[int]
    catalog: str
    db_schema_filter_pattern: str
    table_name_filter_pattern: str
    def __init__(
        self,
        catalog: _Optional[str] = ...,
        db_schema_filter_pattern: _Optional[str] = ...,
        table_name_filter_pattern: _Optional[str] = ...,
    ) -> None: ...

class TableInfo(_message.Message):
    __slots__ = ("catalog_name", "db_schema_name", "table_name")
    CATALOG_NAME_FIELD_NUMBER: _ClassVar[int]
    DB_SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    catalog_name: str
    db_schema_name: str
    table_name: str
    def __init__(
        self, catalog_name: _Optional[str] = ..., db_schema_name: _Optional[str] = ..., table_name: _Optional[str] = ...
    ) -> None: ...

class GetTablesResponse(_message.Message):
    __slots__ = ("tables", "errors")
    TABLES_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    tables: _containers.RepeatedCompositeFieldContainer[TableInfo]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        tables: _Optional[_Iterable[_Union[TableInfo, _Mapping]]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...
