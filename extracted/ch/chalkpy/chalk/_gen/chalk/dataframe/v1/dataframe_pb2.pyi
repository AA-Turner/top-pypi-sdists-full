from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
from chalk._gen.chalk.expression.v1 import expression_pb2 as _expression_pb2
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

class DataFrameOperand(_message.Message):
    __slots__ = (
        "value_string",
        "value_int",
        "value_bool",
        "value_none",
        "value_list",
        "value_dict",
        "value_dataframe_index",
        "arrow_schema",
        "arrow_table",
        "underscore_expr",
        "libchalk_expr",
    )
    VALUE_STRING_FIELD_NUMBER: _ClassVar[int]
    VALUE_INT_FIELD_NUMBER: _ClassVar[int]
    VALUE_BOOL_FIELD_NUMBER: _ClassVar[int]
    VALUE_NONE_FIELD_NUMBER: _ClassVar[int]
    VALUE_LIST_FIELD_NUMBER: _ClassVar[int]
    VALUE_DICT_FIELD_NUMBER: _ClassVar[int]
    VALUE_DATAFRAME_INDEX_FIELD_NUMBER: _ClassVar[int]
    ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    ARROW_TABLE_FIELD_NUMBER: _ClassVar[int]
    UNDERSCORE_EXPR_FIELD_NUMBER: _ClassVar[int]
    LIBCHALK_EXPR_FIELD_NUMBER: _ClassVar[int]
    value_string: str
    value_int: int
    value_bool: bool
    value_none: PyNone
    value_list: PyList
    value_dict: PyDict
    value_dataframe_index: DataFrameIndex
    arrow_schema: _arrow_pb2.Schema
    arrow_table: _arrow_pb2.TableParquetBytes
    underscore_expr: _expression_pb2.LogicalExprNode
    libchalk_expr: _expression_pb2.LogicalExprNode
    def __init__(
        self,
        value_string: _Optional[str] = ...,
        value_int: _Optional[int] = ...,
        value_bool: bool = ...,
        value_none: _Optional[_Union[PyNone, _Mapping]] = ...,
        value_list: _Optional[_Union[PyList, _Mapping]] = ...,
        value_dict: _Optional[_Union[PyDict, _Mapping]] = ...,
        value_dataframe_index: _Optional[_Union[DataFrameIndex, _Mapping]] = ...,
        arrow_schema: _Optional[_Union[_arrow_pb2.Schema, _Mapping]] = ...,
        arrow_table: _Optional[_Union[_arrow_pb2.TableParquetBytes, _Mapping]] = ...,
        underscore_expr: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
        libchalk_expr: _Optional[_Union[_expression_pb2.LogicalExprNode, _Mapping]] = ...,
    ) -> None: ...

class DataFrameIndex(_message.Message):
    __slots__ = ("dataframe_op_index",)
    DATAFRAME_OP_INDEX_FIELD_NUMBER: _ClassVar[int]
    dataframe_op_index: int
    def __init__(self, dataframe_op_index: _Optional[int] = ...) -> None: ...

class PyNone(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PyList(_message.Message):
    __slots__ = ("list_items",)
    LIST_ITEMS_FIELD_NUMBER: _ClassVar[int]
    list_items: _containers.RepeatedCompositeFieldContainer[DataFrameOperand]
    def __init__(self, list_items: _Optional[_Iterable[_Union[DataFrameOperand, _Mapping]]] = ...) -> None: ...

class PyDictEntry(_message.Message):
    __slots__ = ("entry_key", "entry_value")
    ENTRY_KEY_FIELD_NUMBER: _ClassVar[int]
    ENTRY_VALUE_FIELD_NUMBER: _ClassVar[int]
    entry_key: DataFrameOperand
    entry_value: DataFrameOperand
    def __init__(
        self,
        entry_key: _Optional[_Union[DataFrameOperand, _Mapping]] = ...,
        entry_value: _Optional[_Union[DataFrameOperand, _Mapping]] = ...,
    ) -> None: ...

class PyDict(_message.Message):
    __slots__ = ("dict_entries",)
    DICT_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    dict_entries: _containers.RepeatedCompositeFieldContainer[PyDictEntry]
    def __init__(self, dict_entries: _Optional[_Iterable[_Union[PyDictEntry, _Mapping]]] = ...) -> None: ...

class DataFrameConstructor(_message.Message):
    __slots__ = ("self_operand", "function_name", "args", "kwargs")
    SELF_OPERAND_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    KWARGS_FIELD_NUMBER: _ClassVar[int]
    self_operand: DataFrameIndex
    function_name: str
    args: PyList
    kwargs: PyDict
    def __init__(
        self,
        self_operand: _Optional[_Union[DataFrameIndex, _Mapping]] = ...,
        function_name: _Optional[str] = ...,
        args: _Optional[_Union[PyList, _Mapping]] = ...,
        kwargs: _Optional[_Union[PyDict, _Mapping]] = ...,
    ) -> None: ...

class DataFramePlan(_message.Message):
    __slots__ = ("constructors",)
    CONSTRUCTORS_FIELD_NUMBER: _ClassVar[int]
    constructors: _containers.RepeatedCompositeFieldContainer[DataFrameConstructor]
    def __init__(self, constructors: _Optional[_Iterable[_Union[DataFrameConstructor, _Mapping]]] = ...) -> None: ...
