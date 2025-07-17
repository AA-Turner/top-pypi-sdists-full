from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
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

class ScalarFunction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SCALAR_FUNCTION_UNSPECIFIED: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ABS: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ACOS: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ASIN: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ATAN: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ASCII: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_CEIL: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_COS: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_DIGEST: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_EXP: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_FLOOR: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_LN: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_LOG: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_LOG10: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_LOG2: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ROUND: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_SIGNUM: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_SIN: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_SQRT: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_TAN: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_TRUNC: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_REGEXP_MATCH: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_BIT_LENGTH: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_BTRIM: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_CHARACTER_LENGTH: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_CHR: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_CONCAT: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_CONCAT_WITH_SEPARATOR: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_DATE_PART: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_DATE_TRUNC: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_INIT_CAP: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_LEFT: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_LPAD: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_LOWER: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_LTRIM: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_MD5: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_NULL_IF: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_OCTET_LENGTH: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_RANDOM: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_REGEXP_REPLACE: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_REPEAT: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_REPLACE: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_REVERSE: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_RIGHT: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_RPAD: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_RTRIM: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_SHA224: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_SHA256: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_SHA384: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_SHA512: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_SPLIT_PART: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_STARTS_WITH: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_STRPOS: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_SUBSTR: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_TO_HEX: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_TO_TIMESTAMP: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_TO_TIMESTAMP_MILLIS: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_TO_TIMESTAMP_MICROS: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_TO_TIMESTAMP_SECONDS: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_NOW: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_TRANSLATE: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_TRIM: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_UPPER: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_COALESCE: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_POWER: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_STRUCT_FUN: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_FROM_UNIXTIME: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ATAN2: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_DATE_BIN: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARROW_TYPEOF: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_CURRENT_DATE: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_CURRENT_TIME: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_UUID: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_CBRT: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ACOSH: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ASINH: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ATANH: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_SINH: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_COSH: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_TANH: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_PI: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_DEGREES: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_RADIANS: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_FACTORIAL: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_LCM: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_GCD: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_APPEND: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_CONCAT: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_DIMS: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_REPEAT: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_LENGTH: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_NDIMS: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_POSITION: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_POSITIONS: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_PREPEND: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_REMOVE: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_REPLACE: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_TO_STRING: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_CARDINALITY: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_ELEMENT: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_SLICE: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ENCODE: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_DECODE: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_COT: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_HAS: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_HAS_ANY: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_HAS_ALL: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_REMOVE_N: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_REPLACE_N: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_REMOVE_ALL: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_REPLACE_ALL: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_NANVL: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_FLATTEN: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ISNAN: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ISZERO: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_EMPTY: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_POP_BACK: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_STRING_TO_ARRAY: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_TO_TIMESTAMP_NANOS: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_INTERSECT: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_UNION: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_OVER_LAY: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_RANGE: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_EXCEPT: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_POP_FRONT: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_LEVENSHTEIN: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_SUBSTR_INDEX: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_FIND_IN_SET: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_SORT: _ClassVar[ScalarFunction]
    SCALAR_FUNCTION_ARRAY_DISTINCT: _ClassVar[ScalarFunction]

class AggregateFunction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AGGREGATE_FUNCTION_UNSPECIFIED: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_MIN: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_MAX: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_SUM: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_AVG: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_COUNT: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_APPROX_DISTINCT: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_ARRAY: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_VARIANCE: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_VARIANCE_POP: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_COVARIANCE: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_COVARIANCE_POP: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_STDDEV: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_STDDEV_POP: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_CORRELATION: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_APPROX_PERCENTILE_CONT: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_APPROX_MEDIAN: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_APPROX_PERCENTILE_CONT_WITH_WEIGHT: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_GROUPING: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_MEDIAN: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_BIT_AND: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_BIT_OR: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_BIT_XOR: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_BOOL_AND: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_BOOL_OR: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_FIRST_VALUE: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_LAST_VALUE: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_REGR_SLOPE: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_REGR_INTERCEPT: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_REGR_COUNT: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_REGR_R2: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_REGR_AVGX: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_REGR_AVGY: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_REGR_SXX: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_REGR_SYY: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_REGR_SXY: _ClassVar[AggregateFunction]
    AGGREGATE_FUNCTION_STRING: _ClassVar[AggregateFunction]

class BuiltInWindowFunction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUILT_IN_WINDOW_FUNCTION_UNSPECIFIED: _ClassVar[BuiltInWindowFunction]
    BUILT_IN_WINDOW_FUNCTION_ROW_NUMBER: _ClassVar[BuiltInWindowFunction]
    BUILT_IN_WINDOW_FUNCTION_RANK: _ClassVar[BuiltInWindowFunction]
    BUILT_IN_WINDOW_FUNCTION_DENSE_RANK: _ClassVar[BuiltInWindowFunction]
    BUILT_IN_WINDOW_FUNCTION_PERCENT_RANK: _ClassVar[BuiltInWindowFunction]
    BUILT_IN_WINDOW_FUNCTION_CUME_DIST: _ClassVar[BuiltInWindowFunction]
    BUILT_IN_WINDOW_FUNCTION_NTILE: _ClassVar[BuiltInWindowFunction]
    BUILT_IN_WINDOW_FUNCTION_LAG: _ClassVar[BuiltInWindowFunction]
    BUILT_IN_WINDOW_FUNCTION_LEAD: _ClassVar[BuiltInWindowFunction]
    BUILT_IN_WINDOW_FUNCTION_FIRST_VALUE: _ClassVar[BuiltInWindowFunction]
    BUILT_IN_WINDOW_FUNCTION_LAST_VALUE: _ClassVar[BuiltInWindowFunction]
    BUILT_IN_WINDOW_FUNCTION_NTH_VALUE: _ClassVar[BuiltInWindowFunction]

class WindowFrameUnits(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WINDOW_FRAME_UNITS_UNSPECIFIED: _ClassVar[WindowFrameUnits]
    WINDOW_FRAME_UNITS_ROWS: _ClassVar[WindowFrameUnits]
    WINDOW_FRAME_UNITS_RANGE: _ClassVar[WindowFrameUnits]
    WINDOW_FRAME_UNITS_GROUPS: _ClassVar[WindowFrameUnits]

class WindowFrameBoundType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WINDOW_FRAME_BOUND_TYPE_UNSPECIFIED: _ClassVar[WindowFrameBoundType]
    WINDOW_FRAME_BOUND_TYPE_CURRENT_ROW: _ClassVar[WindowFrameBoundType]
    WINDOW_FRAME_BOUND_TYPE_PRECEDING: _ClassVar[WindowFrameBoundType]
    WINDOW_FRAME_BOUND_TYPE_FOLLOWING: _ClassVar[WindowFrameBoundType]

SCALAR_FUNCTION_UNSPECIFIED: ScalarFunction
SCALAR_FUNCTION_ABS: ScalarFunction
SCALAR_FUNCTION_ACOS: ScalarFunction
SCALAR_FUNCTION_ASIN: ScalarFunction
SCALAR_FUNCTION_ATAN: ScalarFunction
SCALAR_FUNCTION_ASCII: ScalarFunction
SCALAR_FUNCTION_CEIL: ScalarFunction
SCALAR_FUNCTION_COS: ScalarFunction
SCALAR_FUNCTION_DIGEST: ScalarFunction
SCALAR_FUNCTION_EXP: ScalarFunction
SCALAR_FUNCTION_FLOOR: ScalarFunction
SCALAR_FUNCTION_LN: ScalarFunction
SCALAR_FUNCTION_LOG: ScalarFunction
SCALAR_FUNCTION_LOG10: ScalarFunction
SCALAR_FUNCTION_LOG2: ScalarFunction
SCALAR_FUNCTION_ROUND: ScalarFunction
SCALAR_FUNCTION_SIGNUM: ScalarFunction
SCALAR_FUNCTION_SIN: ScalarFunction
SCALAR_FUNCTION_SQRT: ScalarFunction
SCALAR_FUNCTION_TAN: ScalarFunction
SCALAR_FUNCTION_TRUNC: ScalarFunction
SCALAR_FUNCTION_ARRAY: ScalarFunction
SCALAR_FUNCTION_REGEXP_MATCH: ScalarFunction
SCALAR_FUNCTION_BIT_LENGTH: ScalarFunction
SCALAR_FUNCTION_BTRIM: ScalarFunction
SCALAR_FUNCTION_CHARACTER_LENGTH: ScalarFunction
SCALAR_FUNCTION_CHR: ScalarFunction
SCALAR_FUNCTION_CONCAT: ScalarFunction
SCALAR_FUNCTION_CONCAT_WITH_SEPARATOR: ScalarFunction
SCALAR_FUNCTION_DATE_PART: ScalarFunction
SCALAR_FUNCTION_DATE_TRUNC: ScalarFunction
SCALAR_FUNCTION_INIT_CAP: ScalarFunction
SCALAR_FUNCTION_LEFT: ScalarFunction
SCALAR_FUNCTION_LPAD: ScalarFunction
SCALAR_FUNCTION_LOWER: ScalarFunction
SCALAR_FUNCTION_LTRIM: ScalarFunction
SCALAR_FUNCTION_MD5: ScalarFunction
SCALAR_FUNCTION_NULL_IF: ScalarFunction
SCALAR_FUNCTION_OCTET_LENGTH: ScalarFunction
SCALAR_FUNCTION_RANDOM: ScalarFunction
SCALAR_FUNCTION_REGEXP_REPLACE: ScalarFunction
SCALAR_FUNCTION_REPEAT: ScalarFunction
SCALAR_FUNCTION_REPLACE: ScalarFunction
SCALAR_FUNCTION_REVERSE: ScalarFunction
SCALAR_FUNCTION_RIGHT: ScalarFunction
SCALAR_FUNCTION_RPAD: ScalarFunction
SCALAR_FUNCTION_RTRIM: ScalarFunction
SCALAR_FUNCTION_SHA224: ScalarFunction
SCALAR_FUNCTION_SHA256: ScalarFunction
SCALAR_FUNCTION_SHA384: ScalarFunction
SCALAR_FUNCTION_SHA512: ScalarFunction
SCALAR_FUNCTION_SPLIT_PART: ScalarFunction
SCALAR_FUNCTION_STARTS_WITH: ScalarFunction
SCALAR_FUNCTION_STRPOS: ScalarFunction
SCALAR_FUNCTION_SUBSTR: ScalarFunction
SCALAR_FUNCTION_TO_HEX: ScalarFunction
SCALAR_FUNCTION_TO_TIMESTAMP: ScalarFunction
SCALAR_FUNCTION_TO_TIMESTAMP_MILLIS: ScalarFunction
SCALAR_FUNCTION_TO_TIMESTAMP_MICROS: ScalarFunction
SCALAR_FUNCTION_TO_TIMESTAMP_SECONDS: ScalarFunction
SCALAR_FUNCTION_NOW: ScalarFunction
SCALAR_FUNCTION_TRANSLATE: ScalarFunction
SCALAR_FUNCTION_TRIM: ScalarFunction
SCALAR_FUNCTION_UPPER: ScalarFunction
SCALAR_FUNCTION_COALESCE: ScalarFunction
SCALAR_FUNCTION_POWER: ScalarFunction
SCALAR_FUNCTION_STRUCT_FUN: ScalarFunction
SCALAR_FUNCTION_FROM_UNIXTIME: ScalarFunction
SCALAR_FUNCTION_ATAN2: ScalarFunction
SCALAR_FUNCTION_DATE_BIN: ScalarFunction
SCALAR_FUNCTION_ARROW_TYPEOF: ScalarFunction
SCALAR_FUNCTION_CURRENT_DATE: ScalarFunction
SCALAR_FUNCTION_CURRENT_TIME: ScalarFunction
SCALAR_FUNCTION_UUID: ScalarFunction
SCALAR_FUNCTION_CBRT: ScalarFunction
SCALAR_FUNCTION_ACOSH: ScalarFunction
SCALAR_FUNCTION_ASINH: ScalarFunction
SCALAR_FUNCTION_ATANH: ScalarFunction
SCALAR_FUNCTION_SINH: ScalarFunction
SCALAR_FUNCTION_COSH: ScalarFunction
SCALAR_FUNCTION_TANH: ScalarFunction
SCALAR_FUNCTION_PI: ScalarFunction
SCALAR_FUNCTION_DEGREES: ScalarFunction
SCALAR_FUNCTION_RADIANS: ScalarFunction
SCALAR_FUNCTION_FACTORIAL: ScalarFunction
SCALAR_FUNCTION_LCM: ScalarFunction
SCALAR_FUNCTION_GCD: ScalarFunction
SCALAR_FUNCTION_ARRAY_APPEND: ScalarFunction
SCALAR_FUNCTION_ARRAY_CONCAT: ScalarFunction
SCALAR_FUNCTION_ARRAY_DIMS: ScalarFunction
SCALAR_FUNCTION_ARRAY_REPEAT: ScalarFunction
SCALAR_FUNCTION_ARRAY_LENGTH: ScalarFunction
SCALAR_FUNCTION_ARRAY_NDIMS: ScalarFunction
SCALAR_FUNCTION_ARRAY_POSITION: ScalarFunction
SCALAR_FUNCTION_ARRAY_POSITIONS: ScalarFunction
SCALAR_FUNCTION_ARRAY_PREPEND: ScalarFunction
SCALAR_FUNCTION_ARRAY_REMOVE: ScalarFunction
SCALAR_FUNCTION_ARRAY_REPLACE: ScalarFunction
SCALAR_FUNCTION_ARRAY_TO_STRING: ScalarFunction
SCALAR_FUNCTION_CARDINALITY: ScalarFunction
SCALAR_FUNCTION_ARRAY_ELEMENT: ScalarFunction
SCALAR_FUNCTION_ARRAY_SLICE: ScalarFunction
SCALAR_FUNCTION_ENCODE: ScalarFunction
SCALAR_FUNCTION_DECODE: ScalarFunction
SCALAR_FUNCTION_COT: ScalarFunction
SCALAR_FUNCTION_ARRAY_HAS: ScalarFunction
SCALAR_FUNCTION_ARRAY_HAS_ANY: ScalarFunction
SCALAR_FUNCTION_ARRAY_HAS_ALL: ScalarFunction
SCALAR_FUNCTION_ARRAY_REMOVE_N: ScalarFunction
SCALAR_FUNCTION_ARRAY_REPLACE_N: ScalarFunction
SCALAR_FUNCTION_ARRAY_REMOVE_ALL: ScalarFunction
SCALAR_FUNCTION_ARRAY_REPLACE_ALL: ScalarFunction
SCALAR_FUNCTION_NANVL: ScalarFunction
SCALAR_FUNCTION_FLATTEN: ScalarFunction
SCALAR_FUNCTION_ISNAN: ScalarFunction
SCALAR_FUNCTION_ISZERO: ScalarFunction
SCALAR_FUNCTION_ARRAY_EMPTY: ScalarFunction
SCALAR_FUNCTION_ARRAY_POP_BACK: ScalarFunction
SCALAR_FUNCTION_STRING_TO_ARRAY: ScalarFunction
SCALAR_FUNCTION_TO_TIMESTAMP_NANOS: ScalarFunction
SCALAR_FUNCTION_ARRAY_INTERSECT: ScalarFunction
SCALAR_FUNCTION_ARRAY_UNION: ScalarFunction
SCALAR_FUNCTION_OVER_LAY: ScalarFunction
SCALAR_FUNCTION_RANGE: ScalarFunction
SCALAR_FUNCTION_ARRAY_EXCEPT: ScalarFunction
SCALAR_FUNCTION_ARRAY_POP_FRONT: ScalarFunction
SCALAR_FUNCTION_LEVENSHTEIN: ScalarFunction
SCALAR_FUNCTION_SUBSTR_INDEX: ScalarFunction
SCALAR_FUNCTION_FIND_IN_SET: ScalarFunction
SCALAR_FUNCTION_ARRAY_SORT: ScalarFunction
SCALAR_FUNCTION_ARRAY_DISTINCT: ScalarFunction
AGGREGATE_FUNCTION_UNSPECIFIED: AggregateFunction
AGGREGATE_FUNCTION_MIN: AggregateFunction
AGGREGATE_FUNCTION_MAX: AggregateFunction
AGGREGATE_FUNCTION_SUM: AggregateFunction
AGGREGATE_FUNCTION_AVG: AggregateFunction
AGGREGATE_FUNCTION_COUNT: AggregateFunction
AGGREGATE_FUNCTION_APPROX_DISTINCT: AggregateFunction
AGGREGATE_FUNCTION_ARRAY: AggregateFunction
AGGREGATE_FUNCTION_VARIANCE: AggregateFunction
AGGREGATE_FUNCTION_VARIANCE_POP: AggregateFunction
AGGREGATE_FUNCTION_COVARIANCE: AggregateFunction
AGGREGATE_FUNCTION_COVARIANCE_POP: AggregateFunction
AGGREGATE_FUNCTION_STDDEV: AggregateFunction
AGGREGATE_FUNCTION_STDDEV_POP: AggregateFunction
AGGREGATE_FUNCTION_CORRELATION: AggregateFunction
AGGREGATE_FUNCTION_APPROX_PERCENTILE_CONT: AggregateFunction
AGGREGATE_FUNCTION_APPROX_MEDIAN: AggregateFunction
AGGREGATE_FUNCTION_APPROX_PERCENTILE_CONT_WITH_WEIGHT: AggregateFunction
AGGREGATE_FUNCTION_GROUPING: AggregateFunction
AGGREGATE_FUNCTION_MEDIAN: AggregateFunction
AGGREGATE_FUNCTION_BIT_AND: AggregateFunction
AGGREGATE_FUNCTION_BIT_OR: AggregateFunction
AGGREGATE_FUNCTION_BIT_XOR: AggregateFunction
AGGREGATE_FUNCTION_BOOL_AND: AggregateFunction
AGGREGATE_FUNCTION_BOOL_OR: AggregateFunction
AGGREGATE_FUNCTION_FIRST_VALUE: AggregateFunction
AGGREGATE_FUNCTION_LAST_VALUE: AggregateFunction
AGGREGATE_FUNCTION_REGR_SLOPE: AggregateFunction
AGGREGATE_FUNCTION_REGR_INTERCEPT: AggregateFunction
AGGREGATE_FUNCTION_REGR_COUNT: AggregateFunction
AGGREGATE_FUNCTION_REGR_R2: AggregateFunction
AGGREGATE_FUNCTION_REGR_AVGX: AggregateFunction
AGGREGATE_FUNCTION_REGR_AVGY: AggregateFunction
AGGREGATE_FUNCTION_REGR_SXX: AggregateFunction
AGGREGATE_FUNCTION_REGR_SYY: AggregateFunction
AGGREGATE_FUNCTION_REGR_SXY: AggregateFunction
AGGREGATE_FUNCTION_STRING: AggregateFunction
BUILT_IN_WINDOW_FUNCTION_UNSPECIFIED: BuiltInWindowFunction
BUILT_IN_WINDOW_FUNCTION_ROW_NUMBER: BuiltInWindowFunction
BUILT_IN_WINDOW_FUNCTION_RANK: BuiltInWindowFunction
BUILT_IN_WINDOW_FUNCTION_DENSE_RANK: BuiltInWindowFunction
BUILT_IN_WINDOW_FUNCTION_PERCENT_RANK: BuiltInWindowFunction
BUILT_IN_WINDOW_FUNCTION_CUME_DIST: BuiltInWindowFunction
BUILT_IN_WINDOW_FUNCTION_NTILE: BuiltInWindowFunction
BUILT_IN_WINDOW_FUNCTION_LAG: BuiltInWindowFunction
BUILT_IN_WINDOW_FUNCTION_LEAD: BuiltInWindowFunction
BUILT_IN_WINDOW_FUNCTION_FIRST_VALUE: BuiltInWindowFunction
BUILT_IN_WINDOW_FUNCTION_LAST_VALUE: BuiltInWindowFunction
BUILT_IN_WINDOW_FUNCTION_NTH_VALUE: BuiltInWindowFunction
WINDOW_FRAME_UNITS_UNSPECIFIED: WindowFrameUnits
WINDOW_FRAME_UNITS_ROWS: WindowFrameUnits
WINDOW_FRAME_UNITS_RANGE: WindowFrameUnits
WINDOW_FRAME_UNITS_GROUPS: WindowFrameUnits
WINDOW_FRAME_BOUND_TYPE_UNSPECIFIED: WindowFrameBoundType
WINDOW_FRAME_BOUND_TYPE_CURRENT_ROW: WindowFrameBoundType
WINDOW_FRAME_BOUND_TYPE_PRECEDING: WindowFrameBoundType
WINDOW_FRAME_BOUND_TYPE_FOLLOWING: WindowFrameBoundType

class Identifier(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class TypedIdentifier(_message.Message):
    __slots__ = ("name", "type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: _arrow_pb2.ArrowType
    def __init__(
        self, name: _Optional[str] = ..., type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...
    ) -> None: ...

class ExprGetAttribute(_message.Message):
    __slots__ = ("parent", "attribute")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    parent: LogicalExprNode
    attribute: Identifier
    def __init__(
        self,
        parent: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        attribute: _Optional[_Union[Identifier, _Mapping]] = ...,
    ) -> None: ...

class ExprGetSubscript(_message.Message):
    __slots__ = ("parent", "subscript")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPT_FIELD_NUMBER: _ClassVar[int]
    parent: LogicalExprNode
    subscript: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    def __init__(
        self,
        parent: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        subscript: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ...,
    ) -> None: ...

class ExprCall(_message.Message):
    __slots__ = ("func", "args", "kwargs", "repr_override")
    class KwargsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: LogicalExprNode
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[LogicalExprNode, _Mapping]] = ...
        ) -> None: ...

    FUNC_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    KWARGS_FIELD_NUMBER: _ClassVar[int]
    REPR_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    func: LogicalExprNode
    args: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    kwargs: _containers.MessageMap[str, LogicalExprNode]
    repr_override: str
    def __init__(
        self,
        func: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        args: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ...,
        kwargs: _Optional[_Mapping[str, LogicalExprNode]] = ...,
        repr_override: _Optional[str] = ...,
    ) -> None: ...

class ExprLiteral(_message.Message):
    __slots__ = ("value", "is_arrow_scalar_object")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    IS_ARROW_SCALAR_OBJECT_FIELD_NUMBER: _ClassVar[int]
    value: _arrow_pb2.ScalarValue
    is_arrow_scalar_object: bool
    def __init__(
        self, value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ..., is_arrow_scalar_object: bool = ...
    ) -> None: ...

class LogicalExprNode(_message.Message):
    __slots__ = (
        "identifier",
        "get_attribute",
        "get_subscript",
        "call",
        "literal_value",
        "typed_identifier",
        "expr_id",
        "column",
        "alias",
        "literal",
        "binary_expr",
        "aggregate_expr",
        "is_null_expr",
        "is_not_null_expr",
        "not_expr",
        "between",
        "case",
        "cast",
        "sort",
        "negative",
        "in_list",
        "wildcard",
        "scalar_function",
        "try_cast",
        "window_expr",
        "aggregate_udf_expr",
        "scalar_udf_expr",
        "get_indexed_field",
        "grouping_set",
        "cube",
        "rollup",
        "is_true",
        "is_false",
        "is_unknown",
        "is_not_true",
        "is_not_false",
        "is_not_unknown",
        "like",
        "ilike",
        "similar_to",
        "placeholder",
    )
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    GET_ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    GET_SUBSCRIPT_FIELD_NUMBER: _ClassVar[int]
    CALL_FIELD_NUMBER: _ClassVar[int]
    LITERAL_VALUE_FIELD_NUMBER: _ClassVar[int]
    TYPED_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    EXPR_ID_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    ALIAS_FIELD_NUMBER: _ClassVar[int]
    LITERAL_FIELD_NUMBER: _ClassVar[int]
    BINARY_EXPR_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_EXPR_FIELD_NUMBER: _ClassVar[int]
    IS_NULL_EXPR_FIELD_NUMBER: _ClassVar[int]
    IS_NOT_NULL_EXPR_FIELD_NUMBER: _ClassVar[int]
    NOT_EXPR_FIELD_NUMBER: _ClassVar[int]
    BETWEEN_FIELD_NUMBER: _ClassVar[int]
    CASE_FIELD_NUMBER: _ClassVar[int]
    CAST_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    IN_LIST_FIELD_NUMBER: _ClassVar[int]
    WILDCARD_FIELD_NUMBER: _ClassVar[int]
    SCALAR_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    TRY_CAST_FIELD_NUMBER: _ClassVar[int]
    WINDOW_EXPR_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_UDF_EXPR_FIELD_NUMBER: _ClassVar[int]
    SCALAR_UDF_EXPR_FIELD_NUMBER: _ClassVar[int]
    GET_INDEXED_FIELD_FIELD_NUMBER: _ClassVar[int]
    GROUPING_SET_FIELD_NUMBER: _ClassVar[int]
    CUBE_FIELD_NUMBER: _ClassVar[int]
    ROLLUP_FIELD_NUMBER: _ClassVar[int]
    IS_TRUE_FIELD_NUMBER: _ClassVar[int]
    IS_FALSE_FIELD_NUMBER: _ClassVar[int]
    IS_UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    IS_NOT_TRUE_FIELD_NUMBER: _ClassVar[int]
    IS_NOT_FALSE_FIELD_NUMBER: _ClassVar[int]
    IS_NOT_UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    LIKE_FIELD_NUMBER: _ClassVar[int]
    ILIKE_FIELD_NUMBER: _ClassVar[int]
    SIMILAR_TO_FIELD_NUMBER: _ClassVar[int]
    PLACEHOLDER_FIELD_NUMBER: _ClassVar[int]
    identifier: Identifier
    get_attribute: ExprGetAttribute
    get_subscript: ExprGetSubscript
    call: ExprCall
    literal_value: ExprLiteral
    typed_identifier: TypedIdentifier
    expr_id: str
    column: Column
    alias: AliasNode
    literal: _arrow_pb2.ScalarValue
    binary_expr: BinaryExprNode
    aggregate_expr: AggregateExprNode
    is_null_expr: IsNull
    is_not_null_expr: IsNotNull
    not_expr: Not
    between: BetweenNode
    case: CaseNode
    cast: CastNode
    sort: SortExprNode
    negative: NegativeNode
    in_list: InListNode
    wildcard: Wildcard
    scalar_function: ScalarFunctionNode
    try_cast: TryCastNode
    window_expr: WindowExprNode
    aggregate_udf_expr: AggregateUDFExprNode
    scalar_udf_expr: ScalarUDFExprNode
    get_indexed_field: GetIndexedField
    grouping_set: GroupingSetNode
    cube: CubeNode
    rollup: RollupNode
    is_true: IsTrue
    is_false: IsFalse
    is_unknown: IsUnknown
    is_not_true: IsNotTrue
    is_not_false: IsNotFalse
    is_not_unknown: IsNotUnknown
    like: LikeNode
    ilike: ILikeNode
    similar_to: SimilarToNode
    placeholder: PlaceholderNode
    def __init__(
        self,
        identifier: _Optional[_Union[Identifier, _Mapping]] = ...,
        get_attribute: _Optional[_Union[ExprGetAttribute, _Mapping]] = ...,
        get_subscript: _Optional[_Union[ExprGetSubscript, _Mapping]] = ...,
        call: _Optional[_Union[ExprCall, _Mapping]] = ...,
        literal_value: _Optional[_Union[ExprLiteral, _Mapping]] = ...,
        typed_identifier: _Optional[_Union[TypedIdentifier, _Mapping]] = ...,
        expr_id: _Optional[str] = ...,
        column: _Optional[_Union[Column, _Mapping]] = ...,
        alias: _Optional[_Union[AliasNode, _Mapping]] = ...,
        literal: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...,
        binary_expr: _Optional[_Union[BinaryExprNode, _Mapping]] = ...,
        aggregate_expr: _Optional[_Union[AggregateExprNode, _Mapping]] = ...,
        is_null_expr: _Optional[_Union[IsNull, _Mapping]] = ...,
        is_not_null_expr: _Optional[_Union[IsNotNull, _Mapping]] = ...,
        not_expr: _Optional[_Union[Not, _Mapping]] = ...,
        between: _Optional[_Union[BetweenNode, _Mapping]] = ...,
        case: _Optional[_Union[CaseNode, _Mapping]] = ...,
        cast: _Optional[_Union[CastNode, _Mapping]] = ...,
        sort: _Optional[_Union[SortExprNode, _Mapping]] = ...,
        negative: _Optional[_Union[NegativeNode, _Mapping]] = ...,
        in_list: _Optional[_Union[InListNode, _Mapping]] = ...,
        wildcard: _Optional[_Union[Wildcard, _Mapping]] = ...,
        scalar_function: _Optional[_Union[ScalarFunctionNode, _Mapping]] = ...,
        try_cast: _Optional[_Union[TryCastNode, _Mapping]] = ...,
        window_expr: _Optional[_Union[WindowExprNode, _Mapping]] = ...,
        aggregate_udf_expr: _Optional[_Union[AggregateUDFExprNode, _Mapping]] = ...,
        scalar_udf_expr: _Optional[_Union[ScalarUDFExprNode, _Mapping]] = ...,
        get_indexed_field: _Optional[_Union[GetIndexedField, _Mapping]] = ...,
        grouping_set: _Optional[_Union[GroupingSetNode, _Mapping]] = ...,
        cube: _Optional[_Union[CubeNode, _Mapping]] = ...,
        rollup: _Optional[_Union[RollupNode, _Mapping]] = ...,
        is_true: _Optional[_Union[IsTrue, _Mapping]] = ...,
        is_false: _Optional[_Union[IsFalse, _Mapping]] = ...,
        is_unknown: _Optional[_Union[IsUnknown, _Mapping]] = ...,
        is_not_true: _Optional[_Union[IsNotTrue, _Mapping]] = ...,
        is_not_false: _Optional[_Union[IsNotFalse, _Mapping]] = ...,
        is_not_unknown: _Optional[_Union[IsNotUnknown, _Mapping]] = ...,
        like: _Optional[_Union[LikeNode, _Mapping]] = ...,
        ilike: _Optional[_Union[ILikeNode, _Mapping]] = ...,
        similar_to: _Optional[_Union[SimilarToNode, _Mapping]] = ...,
        placeholder: _Optional[_Union[PlaceholderNode, _Mapping]] = ...,
    ) -> None: ...

class ColumnRelation(_message.Message):
    __slots__ = ("relation",)
    RELATION_FIELD_NUMBER: _ClassVar[int]
    relation: str
    def __init__(self, relation: _Optional[str] = ...) -> None: ...

class Column(_message.Message):
    __slots__ = ("name", "relation")
    NAME_FIELD_NUMBER: _ClassVar[int]
    RELATION_FIELD_NUMBER: _ClassVar[int]
    name: str
    relation: ColumnRelation
    def __init__(
        self, name: _Optional[str] = ..., relation: _Optional[_Union[ColumnRelation, _Mapping]] = ...
    ) -> None: ...

class Wildcard(_message.Message):
    __slots__ = ("qualifier",)
    QUALIFIER_FIELD_NUMBER: _ClassVar[int]
    qualifier: str
    def __init__(self, qualifier: _Optional[str] = ...) -> None: ...

class PlaceholderNode(_message.Message):
    __slots__ = ("id", "data_type")
    ID_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    data_type: _arrow_pb2.ArrowType
    def __init__(
        self, id: _Optional[str] = ..., data_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...
    ) -> None: ...

class LogicalExprList(_message.Message):
    __slots__ = ("expr",)
    EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    def __init__(self, expr: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ...) -> None: ...

class GroupingSetNode(_message.Message):
    __slots__ = ("expr",)
    EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: _containers.RepeatedCompositeFieldContainer[LogicalExprList]
    def __init__(self, expr: _Optional[_Iterable[_Union[LogicalExprList, _Mapping]]] = ...) -> None: ...

class CubeNode(_message.Message):
    __slots__ = ("expr",)
    EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    def __init__(self, expr: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ...) -> None: ...

class RollupNode(_message.Message):
    __slots__ = ("expr",)
    EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    def __init__(self, expr: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ...) -> None: ...

class NamedStructField(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: _arrow_pb2.ScalarValue
    def __init__(self, name: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...) -> None: ...

class ListIndex(_message.Message):
    __slots__ = ("key",)
    KEY_FIELD_NUMBER: _ClassVar[int]
    key: LogicalExprNode
    def __init__(self, key: _Optional[_Union[LogicalExprNode, _Mapping]] = ...) -> None: ...

class ListRange(_message.Message):
    __slots__ = ("start", "stop")
    START_FIELD_NUMBER: _ClassVar[int]
    STOP_FIELD_NUMBER: _ClassVar[int]
    start: LogicalExprNode
    stop: LogicalExprNode
    def __init__(
        self,
        start: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        stop: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
    ) -> None: ...

class GetIndexedField(_message.Message):
    __slots__ = ("expr", "named_struct_field", "list_index", "list_range")
    EXPR_FIELD_NUMBER: _ClassVar[int]
    NAMED_STRUCT_FIELD_FIELD_NUMBER: _ClassVar[int]
    LIST_INDEX_FIELD_NUMBER: _ClassVar[int]
    LIST_RANGE_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    named_struct_field: NamedStructField
    list_index: ListIndex
    list_range: ListRange
    def __init__(
        self,
        expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        named_struct_field: _Optional[_Union[NamedStructField, _Mapping]] = ...,
        list_index: _Optional[_Union[ListIndex, _Mapping]] = ...,
        list_range: _Optional[_Union[ListRange, _Mapping]] = ...,
    ) -> None: ...

class IsNull(_message.Message):
    __slots__ = ("expr",)
    EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    def __init__(self, expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...) -> None: ...

class IsNotNull(_message.Message):
    __slots__ = ("expr",)
    EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    def __init__(self, expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...) -> None: ...

class IsTrue(_message.Message):
    __slots__ = ("expr",)
    EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    def __init__(self, expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...) -> None: ...

class IsFalse(_message.Message):
    __slots__ = ("expr",)
    EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    def __init__(self, expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...) -> None: ...

class IsUnknown(_message.Message):
    __slots__ = ("expr",)
    EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    def __init__(self, expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...) -> None: ...

class IsNotTrue(_message.Message):
    __slots__ = ("expr",)
    EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    def __init__(self, expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...) -> None: ...

class IsNotFalse(_message.Message):
    __slots__ = ("expr",)
    EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    def __init__(self, expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...) -> None: ...

class IsNotUnknown(_message.Message):
    __slots__ = ("expr",)
    EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    def __init__(self, expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...) -> None: ...

class Not(_message.Message):
    __slots__ = ("expr",)
    EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    def __init__(self, expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...) -> None: ...

class AliasNode(_message.Message):
    __slots__ = ("expr", "alias", "relation")
    EXPR_FIELD_NUMBER: _ClassVar[int]
    ALIAS_FIELD_NUMBER: _ClassVar[int]
    RELATION_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    alias: str
    relation: _containers.RepeatedCompositeFieldContainer[OwnedTableReference]
    def __init__(
        self,
        expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        alias: _Optional[str] = ...,
        relation: _Optional[_Iterable[_Union[OwnedTableReference, _Mapping]]] = ...,
    ) -> None: ...

class BareTableReference(_message.Message):
    __slots__ = ("table",)
    TABLE_FIELD_NUMBER: _ClassVar[int]
    table: str
    def __init__(self, table: _Optional[str] = ...) -> None: ...

class PartialTableReference(_message.Message):
    __slots__ = ("schema", "table")
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    schema: str
    table: str
    def __init__(self, schema: _Optional[str] = ..., table: _Optional[str] = ...) -> None: ...

class FullTableReference(_message.Message):
    __slots__ = ("catalog", "schema", "table")
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    catalog: str
    schema: str
    table: str
    def __init__(
        self, catalog: _Optional[str] = ..., schema: _Optional[str] = ..., table: _Optional[str] = ...
    ) -> None: ...

class OwnedTableReference(_message.Message):
    __slots__ = ("bare", "partial", "full")
    BARE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_FIELD_NUMBER: _ClassVar[int]
    FULL_FIELD_NUMBER: _ClassVar[int]
    bare: BareTableReference
    partial: PartialTableReference
    full: FullTableReference
    def __init__(
        self,
        bare: _Optional[_Union[BareTableReference, _Mapping]] = ...,
        partial: _Optional[_Union[PartialTableReference, _Mapping]] = ...,
        full: _Optional[_Union[FullTableReference, _Mapping]] = ...,
    ) -> None: ...

class BinaryExprNode(_message.Message):
    __slots__ = ("operands", "op")
    OPERANDS_FIELD_NUMBER: _ClassVar[int]
    OP_FIELD_NUMBER: _ClassVar[int]
    operands: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    op: str
    def __init__(
        self, operands: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ..., op: _Optional[str] = ...
    ) -> None: ...

class NegativeNode(_message.Message):
    __slots__ = ("expr",)
    EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    def __init__(self, expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...) -> None: ...

class InListNode(_message.Message):
    __slots__ = ("expr", "list", "negated")
    EXPR_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    NEGATED_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    list: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    negated: bool
    def __init__(
        self,
        expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        list: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ...,
        negated: bool = ...,
    ) -> None: ...

class ScalarFunctionNode(_message.Message):
    __slots__ = ("fun", "args")
    FUN_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    fun: ScalarFunction
    args: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    def __init__(
        self,
        fun: _Optional[_Union[ScalarFunction, str]] = ...,
        args: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ...,
    ) -> None: ...

class AggregateExprNode(_message.Message):
    __slots__ = ("aggr_function", "expr", "distinct", "filter", "order_by")
    AGGR_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    EXPR_FIELD_NUMBER: _ClassVar[int]
    DISTINCT_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    aggr_function: AggregateFunction
    expr: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    distinct: bool
    filter: LogicalExprNode
    order_by: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    def __init__(
        self,
        aggr_function: _Optional[_Union[AggregateFunction, str]] = ...,
        expr: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ...,
        distinct: bool = ...,
        filter: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        order_by: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ...,
    ) -> None: ...

class AggregateUDFExprNode(_message.Message):
    __slots__ = ("fun_name", "args", "filter", "order_by", "kwargs")
    class KwargsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: LogicalExprNode
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[LogicalExprNode, _Mapping]] = ...
        ) -> None: ...

    FUN_NAME_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    KWARGS_FIELD_NUMBER: _ClassVar[int]
    fun_name: str
    args: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    filter: LogicalExprNode
    order_by: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    kwargs: _containers.MessageMap[str, LogicalExprNode]
    def __init__(
        self,
        fun_name: _Optional[str] = ...,
        args: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ...,
        filter: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        order_by: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ...,
        kwargs: _Optional[_Mapping[str, LogicalExprNode]] = ...,
    ) -> None: ...

class ScalarUDFExprNode(_message.Message):
    __slots__ = ("fun_name", "args")
    FUN_NAME_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    fun_name: str
    args: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    def __init__(
        self, fun_name: _Optional[str] = ..., args: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ...
    ) -> None: ...

class WindowExprNode(_message.Message):
    __slots__ = (
        "aggr_function",
        "built_in_function",
        "udaf",
        "udwf",
        "expr",
        "partition_by",
        "order_by",
        "window_frame",
    )
    AGGR_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    BUILT_IN_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    UDAF_FIELD_NUMBER: _ClassVar[int]
    UDWF_FIELD_NUMBER: _ClassVar[int]
    EXPR_FIELD_NUMBER: _ClassVar[int]
    PARTITION_BY_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    WINDOW_FRAME_FIELD_NUMBER: _ClassVar[int]
    aggr_function: AggregateFunction
    built_in_function: BuiltInWindowFunction
    udaf: str
    udwf: str
    expr: LogicalExprNode
    partition_by: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    order_by: _containers.RepeatedCompositeFieldContainer[LogicalExprNode]
    window_frame: WindowFrame
    def __init__(
        self,
        aggr_function: _Optional[_Union[AggregateFunction, str]] = ...,
        built_in_function: _Optional[_Union[BuiltInWindowFunction, str]] = ...,
        udaf: _Optional[str] = ...,
        udwf: _Optional[str] = ...,
        expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        partition_by: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ...,
        order_by: _Optional[_Iterable[_Union[LogicalExprNode, _Mapping]]] = ...,
        window_frame: _Optional[_Union[WindowFrame, _Mapping]] = ...,
    ) -> None: ...

class BetweenNode(_message.Message):
    __slots__ = ("expr", "negated", "low", "high")
    EXPR_FIELD_NUMBER: _ClassVar[int]
    NEGATED_FIELD_NUMBER: _ClassVar[int]
    LOW_FIELD_NUMBER: _ClassVar[int]
    HIGH_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    negated: bool
    low: LogicalExprNode
    high: LogicalExprNode
    def __init__(
        self,
        expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        negated: bool = ...,
        low: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        high: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
    ) -> None: ...

class LikeNode(_message.Message):
    __slots__ = ("negated", "expr", "pattern", "escape_char")
    NEGATED_FIELD_NUMBER: _ClassVar[int]
    EXPR_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    ESCAPE_CHAR_FIELD_NUMBER: _ClassVar[int]
    negated: bool
    expr: LogicalExprNode
    pattern: LogicalExprNode
    escape_char: str
    def __init__(
        self,
        negated: bool = ...,
        expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        pattern: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        escape_char: _Optional[str] = ...,
    ) -> None: ...

class ILikeNode(_message.Message):
    __slots__ = ("negated", "expr", "pattern", "escape_char")
    NEGATED_FIELD_NUMBER: _ClassVar[int]
    EXPR_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    ESCAPE_CHAR_FIELD_NUMBER: _ClassVar[int]
    negated: bool
    expr: LogicalExprNode
    pattern: LogicalExprNode
    escape_char: str
    def __init__(
        self,
        negated: bool = ...,
        expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        pattern: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        escape_char: _Optional[str] = ...,
    ) -> None: ...

class SimilarToNode(_message.Message):
    __slots__ = ("negated", "expr", "pattern", "escape_char")
    NEGATED_FIELD_NUMBER: _ClassVar[int]
    EXPR_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    ESCAPE_CHAR_FIELD_NUMBER: _ClassVar[int]
    negated: bool
    expr: LogicalExprNode
    pattern: LogicalExprNode
    escape_char: str
    def __init__(
        self,
        negated: bool = ...,
        expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        pattern: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        escape_char: _Optional[str] = ...,
    ) -> None: ...

class CaseNode(_message.Message):
    __slots__ = ("expr", "when_then_expr", "else_expr")
    EXPR_FIELD_NUMBER: _ClassVar[int]
    WHEN_THEN_EXPR_FIELD_NUMBER: _ClassVar[int]
    ELSE_EXPR_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    when_then_expr: _containers.RepeatedCompositeFieldContainer[WhenThen]
    else_expr: LogicalExprNode
    def __init__(
        self,
        expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        when_then_expr: _Optional[_Iterable[_Union[WhenThen, _Mapping]]] = ...,
        else_expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
    ) -> None: ...

class WhenThen(_message.Message):
    __slots__ = ("when_expr", "then_expr")
    WHEN_EXPR_FIELD_NUMBER: _ClassVar[int]
    THEN_EXPR_FIELD_NUMBER: _ClassVar[int]
    when_expr: LogicalExprNode
    then_expr: LogicalExprNode
    def __init__(
        self,
        when_expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        then_expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
    ) -> None: ...

class CastNode(_message.Message):
    __slots__ = ("expr", "arrow_type")
    EXPR_FIELD_NUMBER: _ClassVar[int]
    ARROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    arrow_type: _arrow_pb2.ArrowType
    def __init__(
        self,
        expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        arrow_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
    ) -> None: ...

class TryCastNode(_message.Message):
    __slots__ = ("expr", "arrow_type")
    EXPR_FIELD_NUMBER: _ClassVar[int]
    ARROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    arrow_type: _arrow_pb2.ArrowType
    def __init__(
        self,
        expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ...,
        arrow_type: _Optional[_Union[_arrow_pb2.ArrowType, _Mapping]] = ...,
    ) -> None: ...

class SortExprNode(_message.Message):
    __slots__ = ("expr", "asc", "nulls_first")
    EXPR_FIELD_NUMBER: _ClassVar[int]
    ASC_FIELD_NUMBER: _ClassVar[int]
    NULLS_FIRST_FIELD_NUMBER: _ClassVar[int]
    expr: LogicalExprNode
    asc: bool
    nulls_first: bool
    def __init__(
        self, expr: _Optional[_Union[LogicalExprNode, _Mapping]] = ..., asc: bool = ..., nulls_first: bool = ...
    ) -> None: ...

class WindowFrame(_message.Message):
    __slots__ = ("window_frame_units", "start_bound", "bound")
    WINDOW_FRAME_UNITS_FIELD_NUMBER: _ClassVar[int]
    START_BOUND_FIELD_NUMBER: _ClassVar[int]
    BOUND_FIELD_NUMBER: _ClassVar[int]
    window_frame_units: WindowFrameUnits
    start_bound: WindowFrameBound
    bound: WindowFrameBound
    def __init__(
        self,
        window_frame_units: _Optional[_Union[WindowFrameUnits, str]] = ...,
        start_bound: _Optional[_Union[WindowFrameBound, _Mapping]] = ...,
        bound: _Optional[_Union[WindowFrameBound, _Mapping]] = ...,
    ) -> None: ...

class WindowFrameBound(_message.Message):
    __slots__ = ("window_frame_bound_type", "bound_value")
    WINDOW_FRAME_BOUND_TYPE_FIELD_NUMBER: _ClassVar[int]
    BOUND_VALUE_FIELD_NUMBER: _ClassVar[int]
    window_frame_bound_type: WindowFrameBoundType
    bound_value: _arrow_pb2.ScalarValue
    def __init__(
        self,
        window_frame_bound_type: _Optional[_Union[WindowFrameBoundType, str]] = ...,
        bound_value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...,
    ) -> None: ...
