from __future__ import annotations

import json
import types
import typing
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from io import BytesIO
from typing import (
    Any,
    Dict,
    FrozenSet,
    Generic,
    Iterable,
    List,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    final,
    overload,
)

import dateutil.tz
import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.feather as pf
from typing_extensions import Final, get_args, get_origin

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.json import (
    FeatureEncodingOptions,
    structs_as_objects_feature_json_converter,
    structure_json_to_primitive,
    unstructure_primitive_to_json,
)
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.primitive import TPrimitive
from chalk.features._encoding.protobuf import PROTOBUF_TO_UNIT, UNIT_TO_PROTOBUF
from chalk.features._encoding.pyarrow import (
    is_map_in_dtype_tree,
    pyarrow_to_polars,
    pyarrow_to_primitive,
    rich_to_pyarrow,
)
from chalk.features._encoding.rich import structure_primitive_to_rich, unstructure_rich_to_primitive
from chalk.utils.collections import unwrap_annotated_if_needed, unwrap_optional_and_annotated_if_needed
from chalk.utils.df_utils import pa_array_to_pl_series
from chalk.utils.json import JSON, TJSON, is_pyarrow_json_type, pyarrow_json_type
from chalk.utils.log_with_context import get_logger

_logger = get_logger(__name__)

_TRich = TypeVar("_TRich")
_TRichCo = TypeVar("_TRichCo", covariant=True)
_TRichCon = TypeVar("_TRichCon", contravariant=True)

_TPrim = TypeVar("_TPrim", bound=TPrimitive)
_TPrimCo = TypeVar("_TPrimCo", bound=TPrimitive, covariant=True)
_TPrimCon = TypeVar("_TPrimCon", bound=TPrimitive, contravariant=True)

_DEFAULT_FEATURE_ENCODING_OPTIONS = FeatureEncodingOptions()


def _recursively_unwrap(x: Any, dtype: pa.DataType) -> Any:
    if x is None:
        return None
    if isinstance(dtype, pa.MapType):
        if not isinstance(x, list):
            raise ValueError(f"Expected a list, but got {type(x).__name__}")
        if not x:
            return {}
        if not isinstance(x[0], tuple):
            raise TypeError(f"Expected a list of tuples, but got a list of {type(x[0]).__name__}")
        return {k: _recursively_unwrap(v, dtype.item_type) for k, v in x}
    if isinstance(dtype, (pa.ListType, pa.LargeListType, pa.FixedSizeListType)):
        if not isinstance(x, list):
            raise TypeError(f"Expected a list, but got {type(x).__name__}")
        return [_recursively_unwrap(y, dtype.value_type) for y in x]
    if isinstance(dtype, pa.StructType):
        if not isinstance(x, dict):
            raise TypeError(f"Expected a dict, but got {type(x).__name__}")
        return {k: _recursively_unwrap(v, dtype.field(dtype.get_field_index(k)).type) for (k, v) in x.items()}
    if isinstance(x, np.number):
        return x.item()
    return x


class MissingValueError(TypeError):
    """Raised when a missing value is encountered and the missing value strategy is set to ``error``."""

    pass


class PrimitiveFeatureConverter(Generic[_TPrim]):
    """Feature converter that can only deal with primitive types. This means it can be constructed from a serialized graph,
    but it cannot convert to/from rich types"""

    @overload
    def __init__(
        self,
        name: str,
        is_nullable: bool,
        pyarrow_dtype: pa.DataType,
        primitive_default: ellipsis = ...,
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        name: str,
        is_nullable: bool,
        pyarrow_dtype: pa.DataType,
        primitive_default: _TPrim,
    ) -> None:
        ...

    def __init__(
        self,
        name: str,
        is_nullable: bool,
        pyarrow_dtype: pa.DataType,
        primitive_default: Any = ...,
    ) -> None:
        super().__init__()
        self._name = name

        if is_nullable and primitive_default is ...:
            primitive_default = None

        self._pyarrow_dtype = pyarrow_dtype
        if pa.types.is_struct(pyarrow_dtype) and is_nullable:
            is_nullable = False
        self._is_nullable = is_nullable
        self._primitive_type = pyarrow_to_primitive(self._pyarrow_dtype, name)
        try:
            # Storing as an array so we can reuse the same conversion logic
            self._pyarrow_default: ellipsis | pa.Array | pa.ChunkedArray = (
                ... if primitive_default is ... else self.from_primitive_to_pyarrow([primitive_default])
            )
        except Exception as e:
            raise ValueError(
                f"Unable to convert default {primitive_default} of type {type(primitive_default)} to a pyarrow scalar of type {self._pyarrow_dtype}"
            ) from e
        try:
            import polars as pl
        except ModuleNotFoundError:
            pass
        else:
            del pl
            self.polars_dtype: Final = pyarrow_to_polars(self.pyarrow_dtype, self._name)

    __slots__ = ("_name", "_pyarrow_dtype", "_is_nullable", "_primitive_type", "polars_dtype", "_pyarrow_default")

    def __eq__(self, other: object):
        if not isinstance(other, PrimitiveFeatureConverter):
            return NotImplemented
        if not (
            self._name == other._name
            and self._pyarrow_dtype == other._pyarrow_dtype
            and self._is_nullable == other.is_nullable
        ):
            return False
        if self._pyarrow_default == other._pyarrow_default:
            # Fast path -- defaults are definitively equal if 1x1 pyarrow arrays of the default value are equal
            return True
        else:
            if self._pyarrow_default is ... or other._pyarrow_default is ...:
                # Already handled the case where they are both ellipsis above, since ... == ...
                # If here, then one side has a default, when the other side doesn't
                return False
            # Could have false negatives due to nan/null equality
            # To deal, we'll convert both to polars, and compare. This should (recursively) handle nans/nulls
            self_pl = pa_array_to_pl_series(self._pyarrow_default)
            other_pl = pa_array_to_pl_series(other._pyarrow_default)
            import polars.testing

            try:
                # Must use the testing API because otherwise nan != nan
                polars.testing.assert_series_equal(self_pl, other_pl, check_exact=True)
                return True
            except AssertionError:
                return False

    def __hash__(self) -> int:
        return hash((self._name, self._pyarrow_dtype, self._is_nullable, self._pyarrow_default))

    def __getstate__(self):
        # We do NOT include the polars dtype or primitive type on the state; we will reconstruct these from the pyarrow dtype
        # Primitive types might differ if we dynamically construct a class (in the case of structs)
        return (self._name, self._pyarrow_dtype, self._is_nullable, self._pyarrow_default)

    def __setstate__(self, state: tuple[Any, ...]):
        self._name, self._pyarrow_dtype, self._is_nullable, self._pyarrow_default = state
        self._primitive_type = pyarrow_to_primitive(self._pyarrow_dtype, self._name)

        try:
            import polars as pl
        except ModuleNotFoundError:
            pass
        else:
            del pl  # unused
            self.polars_dtype = pyarrow_to_polars(  # pyright: ignore[reportAttributeAccessIssue] -- ok to modify final variables in getstate / setstate
                self.pyarrow_dtype, self._name
            )

    def from_pyarrow_to_json(
        self,
        values: Union[pa.Array, pa.ChunkedArray],
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> Sequence[TJSON]:
        return [self.from_primitive_to_json(x, options=options) for x in self.from_pyarrow_to_primitive(values)]

    def from_pyarrow_to_primitive(self, values: Union[pa.Array, pa.ChunkedArray]) -> Sequence[_TPrim]:
        return [_recursively_unwrap(x, self._pyarrow_dtype) for x in values.to_pylist()]

    def from_primitive_to_pyarrow(self, value: Iterable[_TPrim]) -> Union[pa.Array, pa.ChunkedArray]:
        # FIXME: Convert recursively
        if pa.types.is_float16(self._pyarrow_dtype):
            return pa.array(np.array([None if x is ... else x for x in value], np.dtype("float16")))
        if pa.types.is_fixed_size_list(self._pyarrow_dtype):
            assert isinstance(self._pyarrow_dtype, pa.FixedSizeListType)
            list_size: int = self._pyarrow_dtype.list_size
            value_type: pa.DataType = self._pyarrow_dtype.value_type
            if pa.types.is_float16(value_type):
                value = tuple(value)
                empty = [None] * list_size
                # NOTE: Numpy converts both nan and null to nan for individual array elements.
                # Because pc.if_else doesn't work for float16 arrays, it is difficult to flip the null bits from the python api
                # Since the main use case of FixedSizeList(float16) is for vectors, will leave the nans as-is, because it is more likely
                # for an individual element of a vector to be nan (i.e. overflow from underlying embedding model) than null
                ans = pa.FixedSizeListArray.from_arrays(
                    np.array([empty if x is ... or x is None else x for x in value], np.dtype("float16")).reshape(-1),
                    list_size,
                )
                mask = [x is not ... and x is not None for x in value]
                ans = pc.if_else(pa.array(mask, pa.bool_()), ans, pa.scalar(None, self._pyarrow_dtype))  # type: ignore
                return ans
        if is_map_in_dtype_tree(self._pyarrow_dtype):
            return pa.array(
                [None if x is ... else self._recursive_dict_to_list_of_dicts(x, self._pyarrow_dtype) for x in value],
                type=self._pyarrow_dtype,
            )
        return pa.array([None if x is ... else x for x in value], type=self._pyarrow_dtype)

    def from_primitive_to_json(
        self, value: TPrimitive, options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS
    ) -> TJSON:
        if options.encode_structs_as_objects or is_map_in_dtype_tree(self._pyarrow_dtype):
            return structs_as_objects_feature_json_converter.unstructure_primitive_to_json(value)
        else:
            return unstructure_primitive_to_json(value)

    def from_json_to_pyarrow(self, values: Sequence[TJSON]) -> Union[pa.Array, pa.ChunkedArray]:
        primitive_vals = [self.from_json_to_primitive(x) for x in values]
        return self.from_primitive_to_pyarrow(primitive_vals)

    def from_json_to_primitive(self, value: Union[TJSON, TPrimitive]) -> _TPrim:
        try:
            if self._primitive_type == JSON:  # pyright: ignore[reportUnnecessaryComparison]
                # The JSON is the primitive!
                return cast(_TPrim, value)
            return cast(_TPrim, structure_json_to_primitive(value, self._primitive_type))
        except (ValueError, TypeError) as e:
            raise TypeError(f"Could not convert '{value}' to `{self._primitive_type}`: {e}") from e

    @property
    def pyarrow_dtype(self) -> pa.DataType:
        return self._pyarrow_dtype

    @property
    def pyarrow_default(self) -> ellipsis | pa.Array | pa.ChunkedArray:
        return self._pyarrow_default

    @property
    def is_nullable(self) -> bool:
        return self._is_nullable

    @property
    def primitive_type(self) -> Type[TPrimitive]:
        return self._primitive_type

    @property
    def has_default(self) -> bool:
        # primitive default is set <==> rich default is also set or no rich type was provided
        return self._pyarrow_default != ...

    @property
    def primitive_default(self) -> _TPrim:
        if self._pyarrow_default is ...:
            raise ValueError(f"Feature '{self._name}' has no default value")
        return cast(_TPrim, self._pyarrow_default.to_pylist()[0])

    def is_value_missing(self, value: Any):
        """Returns whether the ``value`` should be treated as a "missing" value"""
        if value is ...:
            # Ellipsis is always missing
            return True
        if value is None:
            # All nullable args have a default (``None`` if not otherwise specified)
            if pa.types.is_struct(self.pyarrow_dtype):
                # Nones are not missing for structs
                return False
            return not self._is_nullable
        return False

    @classmethod
    def from_protobuf_to_pyarrow(cls, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("extension_value"):
            storage_val = cls.from_protobuf_to_pyarrow(pb_value.extension_value.storage_value)
            logical_type = cls.convert_proto_dtype_to_pa_dtype(
                pb.ArrowType(extension=pb_value.extension_value.extension_type)
            )
            return pa.ExtensionScalar.from_storage(logical_type, storage_val)
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=cls.convert_proto_dtype_to_pa_dtype(pb_value.null_value))[0]
        if pb_value.HasField("bool_value"):
            return pa.scalar(pb_value.bool_value, pa.bool_())
        if pb_value.HasField("int8_value"):
            return pa.scalar(pb_value.int8_value, pa.int8())
        if pb_value.HasField("int16_value"):
            return pa.scalar(pb_value.int16_value, pa.int16())
        if pb_value.HasField("int32_value"):
            return pa.scalar(pb_value.int32_value, pa.int32())
        if pb_value.HasField("int64_value"):
            return pa.scalar(pb_value.int64_value, pa.int64())
        if pb_value.HasField("uint8_value"):
            return pa.scalar(pb_value.uint8_value, pa.uint8())
        if pb_value.HasField("uint16_value"):
            return pa.scalar(pb_value.uint16_value, pa.uint16())
        if pb_value.HasField("uint32_value"):
            return pa.scalar(pb_value.uint32_value, pa.uint32())
        if pb_value.HasField("uint64_value"):
            return pa.scalar(pb_value.uint64_value, pa.uint64())
        if pb_value.HasField("float16_value"):
            return pa.scalar(np.float16(pb_value.float16_value), pa.float16())
        if pb_value.HasField("float32_value"):
            return pa.scalar(pb_value.float32_value, pa.float32())
        if pb_value.HasField("float64_value"):
            return pa.scalar(pb_value.float64_value, pa.float64())
        if pb_value.HasField("utf8_value"):
            return pa.scalar(pb_value.utf8_value, pa.utf8())
        if pb_value.HasField("large_utf8_value"):
            return pa.scalar(pb_value.large_utf8_value, pa.large_utf8())
        if pb_value.HasField("binary_value"):
            return pa.scalar(pb_value.binary_value, pa.binary())
        if pb_value.HasField("large_binary_value"):
            return pa.scalar(pb_value.large_binary_value, pa.large_binary())
        if pb_value.HasField("fixed_size_binary_value"):
            return pa.scalar(
                pb_value.fixed_size_binary_value.values, pa.binary(pb_value.fixed_size_binary_value.length)
            )
        if pb_value.HasField("date_32_value"):
            return pa.scalar(date(1970, 1, 1) + timedelta(days=pb_value.date_32_value), pa.date32())
        if pb_value.HasField("date_64_value"):
            return pa.scalar(date(1970, 1, 1) + timedelta(days=pb_value.date_64_value), pa.date64())
        if pb_value.HasField("time32_value"):
            if pb_value.time32_value.HasField("time32_second_value"):
                seconds = pb_value.time32_value.time32_second_value
                return pa.scalar(
                    time(
                        hour=seconds // 3600,
                        minute=(seconds % 3600) // 60,
                        second=seconds % 60,
                    ),
                    pa.time32("s"),
                )
            if pb_value.time32_value.HasField("time32_millisecond_value"):
                milliseconds = pb_value.time32_value.time32_millisecond_value
                return pa.scalar(
                    time(
                        hour=milliseconds // 3600000,
                        minute=(milliseconds % 3600000) // 60000,
                        second=(milliseconds % 60000) // 1000,
                        microsecond=(milliseconds % 1000) * 1000,
                    ),
                    pa.time32("ms"),
                )
            raise ValueError(
                "Unsupported time32 value - missing fields `time32_second_value` and `time32_millisecond_value`"
            )
        if pb_value.HasField("time64_value"):
            if pb_value.time64_value.HasField("time64_microsecond_value"):
                microseconds = pb_value.time64_value.time64_microsecond_value
                return pa.scalar(
                    time(
                        hour=microseconds // 3600000000,
                        minute=(microseconds % 3600000000) // 60000000,
                        second=(microseconds % 60000000) // 1000000,
                        microsecond=microseconds % 1000000,
                    ),
                    pa.time64("us"),
                )
            if pb_value.time64_value.HasField("time64_nanosecond_value"):
                nanoseconds = pb_value.time64_value.time64_nanosecond_value
                # Python's datetime.time does not support nanoseconds, so we round to the nearest microsecond
                microseconds = nanoseconds // 1000
                return pa.scalar(
                    time(
                        hour=microseconds // 3600000000,
                        minute=(microseconds % 3600000000) // 60000000,
                        second=(microseconds % 60000000) // 1000000,
                        microsecond=microseconds % 1000000,
                    ),
                    pa.time64("ns"),
                )
            raise ValueError(
                "Unsupported time64 value - missing fields `time64_microsecond_value` and `time64_nanosecond_value`"
            )
        if pb_value.HasField("timestamp_value"):
            tz_str = pb_value.timestamp_value.timezone
            tz = dateutil.tz.gettz(tz_str) if tz_str else None
            if pb_value.timestamp_value.HasField("time_second_value"):
                seconds = pb_value.timestamp_value.time_second_value
                return pa.scalar(datetime.fromtimestamp(seconds, tz=tz), pa.timestamp("s", tz=tz_str))
            if pb_value.timestamp_value.HasField("time_millisecond_value"):
                milliseconds = pb_value.timestamp_value.time_millisecond_value
                return pa.scalar(datetime.fromtimestamp(milliseconds / 1000, tz=tz), pa.timestamp("ms", tz=tz_str))
            if pb_value.timestamp_value.HasField("time_microsecond_value"):
                microseconds = pb_value.timestamp_value.time_microsecond_value
                return pa.scalar(datetime.fromtimestamp(microseconds / 1_000_000, tz=tz), pa.timestamp("us", tz=tz_str))
            if pb_value.timestamp_value.HasField("time_nanosecond_value"):
                nanoseconds = pb_value.timestamp_value.time_nanosecond_value
                return pa.scalar(
                    datetime.fromtimestamp(nanoseconds / 1_000_000_000, tz=tz), pa.timestamp("ns", tz=tz_str)
                )
            raise ValueError(
                (
                    "Unsupported protobuf timestamp value - missing fields `time_second_value`, "
                    "`time_millisecond_value`, `time_microsecond_value`, and `time_nanosecond_value`"
                )
            )
        if pb_value.HasField("struct_value"):
            name_to_pa_scalar = {
                field.name: cls.from_protobuf_to_pyarrow(field_value)
                for field, field_value in zip(pb_value.struct_value.fields, pb_value.struct_value.field_values)
            }
            # TODO: Add test using `v.as_py()` values that evaluate to 0 for testing `if (o := v.as_py()) is not None`
            name_to_py_values_not_none = {k: o for k, v in name_to_pa_scalar.items() if (o := v.as_py()) is not None}
            fields = [pa.field(k, v.type) for k, v in name_to_pa_scalar.items()]
            return pa.scalar(name_to_py_values_not_none, pa.struct(fields))
        if (
            pb_value.HasField("list_value")
            or pb_value.HasField("large_list_value")
            or pb_value.HasField("fixed_size_list_value")
            or pb_value.HasField("map_value")
        ):
            return cls._deserialize_pb_list_to_pa(pb_value)
        if pb_value.HasField("duration_second_value"):
            return pa.scalar(timedelta(seconds=pb_value.duration_second_value), pa.duration("s"))
        if pb_value.HasField("duration_millisecond_value"):
            return pa.scalar(timedelta(milliseconds=pb_value.duration_millisecond_value), pa.duration("ms"))
        if pb_value.HasField("duration_microsecond_value"):
            return pa.scalar(timedelta(microseconds=pb_value.duration_microsecond_value), pa.duration("us"))
        if pb_value.HasField("duration_nanosecond_value"):
            return pa.scalar(timedelta(microseconds=pb_value.duration_nanosecond_value / 1000), pa.duration("ns"))
        if pb_value.HasField("decimal128_value"):
            return cls._deserialize_pb_to_pa_decimal(pb_value)
        if pb_value.HasField("decimal256_value"):
            return cls._deserialize_pb_to_pa_decimal(pb_value)
        raise ValueError(f"Unsupported Protobuf type: {pb_value}")

    @classmethod
    def from_pyarrow_to_protobuf(cls, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=cls.convert_pa_dtype_to_proto_dtype(value.type))
        if pa.types.is_null(value.type):
            return pb.ScalarValue(null_value=cls.convert_pa_dtype_to_proto_dtype(value.type))
        if pa.types.is_boolean(value.type):
            return pb.ScalarValue(bool_value=value.as_py())
        if pa.types.is_int8(value.type):
            return pb.ScalarValue(int8_value=value.as_py())
        if pa.types.is_int16(value.type):
            return pb.ScalarValue(int16_value=value.as_py())
        if pa.types.is_int32(value.type):
            return pb.ScalarValue(int32_value=value.as_py())
        if pa.types.is_int64(value.type):
            return pb.ScalarValue(int64_value=value.as_py())
        if pa.types.is_uint8(value.type):
            return pb.ScalarValue(uint8_value=value.as_py())
        if pa.types.is_uint16(value.type):
            return pb.ScalarValue(uint16_value=value.as_py())
        if pa.types.is_uint32(value.type):
            return pb.ScalarValue(uint32_value=value.as_py())
        if pa.types.is_uint64(value.type):
            return pb.ScalarValue(uint64_value=value.as_py())
        if pa.types.is_float16(value.type):
            return pb.ScalarValue(float16_value=value.as_py())
        if pa.types.is_float32(value.type):
            return pb.ScalarValue(float32_value=value.as_py())
        if pa.types.is_float64(value.type):
            return pb.ScalarValue(float64_value=value.as_py())
        if pa.types.is_string(value.type):
            return pb.ScalarValue(utf8_value=value.as_py())
        if pa.types.is_large_string(value.type):
            return pb.ScalarValue(large_utf8_value=value.as_py())
        if pa.types.is_binary(value.type):
            return pb.ScalarValue(binary_value=value.as_py())
        if pa.types.is_large_binary(value.type):
            return pb.ScalarValue(large_binary_value=value.as_py())
        if pa.types.is_date32(value.type):
            date_value = value.as_py()
            if not isinstance(date_value, date):
                raise TypeError(f"Expected Python `date` but got `{type(date_value).__name__}`")
            epoch_days = date_value - date(1970, 1, 1)
            return pb.ScalarValue(date_32_value=epoch_days.days)
        if pa.types.is_date64(value.type):
            date_value = value.as_py()
            if not isinstance(date_value, date):
                raise TypeError(f"Expected Python `date` but got `{type(date_value).__name__}`")
            epoch_days = date_value - date(1970, 1, 1)
            return pb.ScalarValue(date_64_value=epoch_days.days)
        if pa.types.is_time32(value.type):
            time_val = value.as_py()
            if not isinstance(time_val, time):
                raise TypeError(f"Expected Python `time`, but got `{type(time_val).__name__}`")
            ms_since_midnight = (
                time_val.hour * 3_600_000
                + time_val.minute * 60_000
                + time_val.second * 1000
                + time_val.microsecond // 1000
            )

            # Failing assertion, because dtype is a `DataType` instead of a `Time32Type`
            # assert isinstance(dtype, pa.Time32Type)
            if value.type == pa.time32("s"):
                return pb.ScalarValue(time32_value=pb.ScalarTime32Value(time32_second_value=ms_since_midnight // 1000))
            assert value.type == pa.time32("ms")
            return pb.ScalarValue(time32_value=pb.ScalarTime32Value(time32_millisecond_value=ms_since_midnight))
        if pa.types.is_time64(value.type):
            time_val = value.as_py()
            if not isinstance(time_val, time):
                raise TypeError(f"Expected Python `time`, but got `{type(time_val).__name__}`")
            ns_since_midnight = (
                time_val.hour * 3_600_000_000_000
                + time_val.minute * 60_000_000_000
                + time_val.second * 1_000_000_000
                + time_val.microsecond * 1000
            )

            # Failing assertion, because dtype is a `DataType` instead of a `Time64Type`
            # assert isinstance(dtype, pa.Time64Type)
            if value.type == pa.time64("us"):
                return pb.ScalarValue(
                    time64_value=pb.ScalarTime64Value(time64_microsecond_value=ns_since_midnight // 1000)
                )
            assert value.type == pa.time64("ns")
            return pb.ScalarValue(time64_value=pb.ScalarTime64Value(time64_nanosecond_value=ns_since_midnight))
        if isinstance(value.type, pa.TimestampType):
            dt_val = value.as_py()
            float_s = dt_val.timestamp()
            if not isinstance(dt_val, datetime):
                raise TypeError(f"Expected Python `datetime`, but got `{type(dt_val).__name__}`")
            timezone = None if dt_val.tzinfo is None else dt_val.tzinfo.tzname(dt_val)

            if value.type.unit == "ms":
                return pb.ScalarValue(
                    timestamp_value=pb.ScalarTimestampValue(
                        time_millisecond_value=int(float_s * 1000),
                        timezone=timezone,
                    )
                )
            elif value.type.unit == "us":
                return pb.ScalarValue(
                    timestamp_value=pb.ScalarTimestampValue(
                        time_microsecond_value=int(float_s * 1_000_000),
                        timezone=timezone,
                    )
                )
            elif value.type.unit == "ns":
                return pb.ScalarValue(
                    timestamp_value=pb.ScalarTimestampValue(
                        time_nanosecond_value=int(float_s * 1_000_000_000),
                        timezone=timezone,
                    )
                )
            return pb.ScalarValue(
                timestamp_value=pb.ScalarTimestampValue(
                    time_second_value=int(float_s),
                    timezone=timezone,
                )
            )
        if pa.types.is_duration(value.type):
            duration_val = value.as_py()
            if not isinstance(duration_val, timedelta):
                raise TypeError(
                    f"Expected a `timedelta` as the Python equivalent of a PyArrow Duration, but got: {type(duration_val).__name__}"
                )
            dtype = value.type
            if not isinstance(dtype, pa.DurationType):
                raise TypeError(
                    f"Expected a `pa.DurationType` as the PyArrow type of a PyArrow Duration, but got: {type(dtype).__name__}"
                )
            if dtype.unit == "s":
                return pb.ScalarValue(duration_second_value=int(duration_val.total_seconds()))
            if dtype.unit == "ms":
                return pb.ScalarValue(duration_millisecond_value=int(duration_val.total_seconds() * 1000))
            if dtype.unit == "us":
                return pb.ScalarValue(duration_microsecond_value=int(duration_val.total_seconds() * 1_000_000))
            if dtype.unit == "ns":
                return pb.ScalarValue(duration_nanosecond_value=int(duration_val.total_seconds() * 1_000_000_000))
            raise ValueError(f"Unsupported duration unit: {dtype.unit}")
        if pa.types.is_fixed_size_binary(value.type):
            bytes_obj = value.as_py()
            if not isinstance(bytes_obj, bytes):
                raise TypeError(f"Expected Python `bytes` but got `{type(bytes_obj).__name__}`")
            return pb.ScalarValue(
                fixed_size_binary_value=pb.ScalarFixedSizeBinary(values=bytes_obj, length=len(bytes_obj))
            )
        if isinstance(value, pa.StructScalar):
            fields = []
            field_values = []
            for name, pa_scalar in value.items():
                pb_scalar = cls.from_pyarrow_to_protobuf(pa_scalar)
                fields.append(
                    pb.Field(
                        name=name,
                        arrow_type=cls.convert_pa_dtype_to_proto_dtype(pa_scalar.type),
                        nullable=True,
                    )
                )
                field_values.append(pb_scalar)
            return pb.ScalarValue(struct_value=pb.StructValue(fields=fields, field_values=field_values))
        if isinstance(value, pa.MapScalar):
            return cls._serialize_pa_list_to_pb(value)
        if isinstance(value, pa.ListScalar):
            return cls._serialize_pa_list_to_pb(value)
        if isinstance(value, pa.Decimal128Scalar):
            return cls._serialize_pa_decimal_to_pb(value)
        if isinstance(value, pa.Decimal256Scalar):
            return cls._serialize_pa_decimal_to_pb(value)

        raise ValueError(f"Unsupported type: {value.type}")

    @classmethod
    def convert_proto_dtype_to_pa_dtype(cls, dtype: pb.ArrowType) -> pa.DataType:
        if dtype.HasField("none"):
            return pa.null()
        elif dtype.HasField("bool"):
            return pa.bool_()
        elif dtype.HasField("int8"):
            return pa.int8()
        elif dtype.HasField("int16"):
            return pa.int16()
        elif dtype.HasField("int32"):
            return pa.int32()
        elif dtype.HasField("int64"):
            return pa.int64()
        elif dtype.HasField("uint8"):
            return pa.uint8()
        elif dtype.HasField("uint16"):
            return pa.uint16()
        elif dtype.HasField("uint32"):
            return pa.uint32()
        elif dtype.HasField("uint64"):
            return pa.uint64()
        elif dtype.HasField("float16"):
            return pa.float16()
        elif dtype.HasField("float32"):
            return pa.float32()
        elif dtype.HasField("float64"):
            return pa.float64()
        elif dtype.HasField("utf8"):
            return pa.utf8()
        elif dtype.HasField("large_utf8"):
            return pa.large_utf8()
        elif dtype.HasField("binary"):
            return pa.binary()
        elif dtype.HasField("large_binary"):
            return pa.large_binary()
        elif dtype.HasField("date32"):
            return pa.date32()
        elif dtype.HasField("date64"):
            return pa.date64()
        elif dtype.HasField("time32"):
            unit = PROTOBUF_TO_UNIT[dtype.time32]
            assert unit == "s" or unit == "ms"
            return pa.time32(unit)
        elif dtype.HasField("time64"):
            unit = PROTOBUF_TO_UNIT[dtype.time64]
            assert unit == "us" or unit == "ns"
            return pa.time64(unit)
        elif dtype.HasField("timestamp"):
            unit = PROTOBUF_TO_UNIT[dtype.timestamp.time_unit]
            assert unit in ("s", "ms", "us", "ns")
            return pa.timestamp(unit, tz=dtype.timestamp.timezone)
        elif dtype.HasField("duration"):
            unit = PROTOBUF_TO_UNIT[dtype.duration]
            assert unit in ("s", "ms", "us", "ns")
            return pa.duration(unit)
        elif dtype.HasField("decimal_128"):
            return pa.decimal128(dtype.decimal_128.precision, dtype.decimal_128.scale)
        elif dtype.HasField("decimal_256"):
            return pa.decimal256(dtype.decimal_256.precision, dtype.decimal_256.scale)
        elif dtype.HasField("struct"):
            fields = [
                pa.field(
                    field.name,
                    cls.convert_proto_dtype_to_pa_dtype(field.arrow_type),
                    nullable=field.nullable,
                )
                for field in dtype.struct.sub_field_types
            ]
            return pa.struct(fields)
        elif dtype.HasField("list"):
            return pa.list_(
                pa.field(
                    name=dtype.list.field_type.name,
                    type=cls.convert_proto_dtype_to_pa_dtype(dtype.list.field_type.arrow_type),
                    nullable=dtype.list.field_type.nullable,
                )
            )
        elif dtype.HasField("large_list"):
            return pa.large_list(
                pa.field(
                    name=dtype.large_list.field_type.name,
                    type=cls.convert_proto_dtype_to_pa_dtype(dtype.large_list.field_type.arrow_type),
                    nullable=dtype.large_list.field_type.nullable,
                )
            )
        elif dtype.HasField("fixed_size_list"):
            return pa.list_(
                pa.field(
                    name=dtype.fixed_size_list.field_type.name,
                    type=cls.convert_proto_dtype_to_pa_dtype(dtype.fixed_size_list.field_type.arrow_type),
                    nullable=dtype.fixed_size_list.field_type.nullable,
                ),
                list_size=dtype.fixed_size_list.list_size,
            )
        elif dtype.HasField("map"):
            key_field = pa.field(
                name=dtype.map.key_field.name,
                type=cls.convert_proto_dtype_to_pa_dtype(dtype.map.key_field.arrow_type),
                nullable=dtype.map.key_field.nullable,
            )
            item_field = pa.field(
                name=dtype.map.item_field.name,
                type=cls.convert_proto_dtype_to_pa_dtype(dtype.map.item_field.arrow_type),
                nullable=dtype.map.item_field.nullable,
            )
            return pa.map_(
                key_type=key_field,
                item_type=item_field,
                keys_sorted=dtype.map.keys_sorted,
            )
        if dtype.HasField("extension"):
            if dtype.extension.name == "arrow.json":
                return pyarrow_json_type()
            raise ValueError(f"Unsupported extension type: '{dtype.extension.name}'")

        raise ValueError(f"Could not convert the protobuf type `{dtype}` to a pyarrow dtype")

    @classmethod
    def convert_pa_dtype_to_proto_dtype(cls, dtype: pa.DataType) -> pb.ArrowType:
        if dtype == pa.null():
            return pb.ArrowType(none=pb.EmptyMessage())
        elif pa.types.is_boolean(dtype):
            return pb.ArrowType(bool=pb.EmptyMessage())
        elif pa.types.is_int8(dtype):
            return pb.ArrowType(int8=pb.EmptyMessage())
        elif pa.types.is_int16(dtype):
            return pb.ArrowType(int16=pb.EmptyMessage())
        elif pa.types.is_int32(dtype):
            return pb.ArrowType(int32=pb.EmptyMessage())
        elif pa.types.is_int64(dtype):
            return pb.ArrowType(int64=pb.EmptyMessage())
        elif pa.types.is_uint8(dtype):
            return pb.ArrowType(uint8=pb.EmptyMessage())
        elif pa.types.is_uint16(dtype):
            return pb.ArrowType(uint16=pb.EmptyMessage())
        elif pa.types.is_uint32(dtype):
            return pb.ArrowType(uint32=pb.EmptyMessage())
        elif pa.types.is_uint64(dtype):
            return pb.ArrowType(uint64=pb.EmptyMessage())
        elif pa.types.is_float16(dtype):
            return pb.ArrowType(float16=pb.EmptyMessage())
        elif pa.types.is_float32(dtype):
            return pb.ArrowType(float32=pb.EmptyMessage())
        elif pa.types.is_float64(dtype):
            return pb.ArrowType(float64=pb.EmptyMessage())
        elif pa.types.is_string(dtype):
            return pb.ArrowType(utf8=pb.EmptyMessage())
        elif pa.types.is_large_string(dtype):
            return pb.ArrowType(large_utf8=pb.EmptyMessage())
        elif pa.types.is_binary(dtype):
            return pb.ArrowType(binary=pb.EmptyMessage())
        elif pa.types.is_large_binary(dtype):
            return pb.ArrowType(large_binary=pb.EmptyMessage())
        elif pa.types.is_date32(dtype):
            return pb.ArrowType(date32=pb.EmptyMessage())
        elif pa.types.is_date64(dtype):
            return pb.ArrowType(date64=pb.EmptyMessage())
        elif dtype == pa.time32("s"):
            return pb.ArrowType(time32=pb.TIME_UNIT_SECOND)
        elif dtype == pa.time32("ms"):
            return pb.ArrowType(time32=pb.TIME_UNIT_MILLISECOND)
        elif dtype == pa.time64("us"):
            return pb.ArrowType(time64=pb.TIME_UNIT_MICROSECOND)
        elif dtype == pa.time64("ns"):
            return pb.ArrowType(time64=pb.TIME_UNIT_NANOSECOND)
        elif isinstance(dtype, pa.TimestampType):
            return pb.ArrowType(timestamp=pb.Timestamp(time_unit=UNIT_TO_PROTOBUF[dtype.unit], timezone=dtype.tz))
        elif isinstance(dtype, pa.DurationType):
            return pb.ArrowType(duration=UNIT_TO_PROTOBUF[dtype.unit])
        elif isinstance(dtype, pa.Decimal128Type):
            return pb.ArrowType(decimal_128=pb.Decimal(precision=dtype.precision, scale=dtype.scale))
        elif isinstance(dtype, pa.Decimal256Type):
            return pb.ArrowType(decimal_256=pb.Decimal(precision=dtype.precision, scale=dtype.scale))
        elif isinstance(dtype, pa.StructType):
            pb_fields = []
            for pa_field in dtype:
                pb_fields.append(
                    pb.Field(
                        name=pa_field.name,
                        nullable=pa_field.nullable,
                        arrow_type=cls.convert_pa_dtype_to_proto_dtype(pa_field.type),
                    )
                )
            return pb.ArrowType(struct=pb.Struct(sub_field_types=pb_fields))
        elif isinstance(dtype, pa.ListType):
            pb_field = pb.Field(
                name=dtype.value_field.name,
                nullable=dtype.value_field.nullable,
                arrow_type=cls.convert_pa_dtype_to_proto_dtype(dtype.value_field.type),
            )
            return pb.ArrowType(list=pb.List(field_type=pb_field))
        elif isinstance(dtype, pa.LargeListType):
            pb_field = pb.Field(
                name=dtype.value_field.name,
                nullable=dtype.value_field.nullable,
                arrow_type=cls.convert_pa_dtype_to_proto_dtype(dtype.value_field.type),
            )
            return pb.ArrowType(large_list=pb.List(field_type=pb_field))
        elif isinstance(dtype, pa.FixedSizeListType):
            pb_field = pb.Field(
                name=dtype.value_field.name,
                nullable=dtype.value_field.nullable,
                arrow_type=cls.convert_pa_dtype_to_proto_dtype(dtype.value_field.type),
            )
            return pb.ArrowType(fixed_size_list=pb.FixedSizeList(field_type=pb_field, list_size=dtype.list_size))
        elif isinstance(dtype, pa.MapType):
            return pb.ArrowType(
                map=pb.Map(
                    key_field=pb.Field(
                        name=dtype.key_field.name,
                        nullable=dtype.key_field.nullable,
                        arrow_type=cls.convert_pa_dtype_to_proto_dtype(dtype.key_field.type),
                    ),
                    item_field=pb.Field(
                        name=dtype.item_field.name,
                        nullable=dtype.item_field.nullable,
                        arrow_type=cls.convert_pa_dtype_to_proto_dtype(dtype.item_field.type),
                    ),
                ),
            )
        elif isinstance(dtype, pa.ExtensionType):
            return pb.ArrowType(
                extension=pb.Extension(
                    name=dtype.extension_name,
                    storage_type=cls.convert_pa_dtype_to_proto_dtype(dtype.storage_type),
                )
            )
        else:
            raise TypeError(f"Could not convert the pyarrow dtype {dtype} to a protobuf message")

    @staticmethod
    def _serialize_pa_decimal_to_pb(value: Union[pa.Decimal128Scalar, pa.Decimal256Scalar]) -> pb.ScalarValue:
        dec_val = value.as_py()
        if not isinstance(dec_val, Decimal):
            raise ValueError(
                f"Expected a `Decimal` as the Python equivalent of a PyArrow decimal, but got a '{type(dec_val).__name__}'"
            )

        dtype = value.type
        if not isinstance(dtype, (pa.Decimal128Type, pa.Decimal256Type)):
            raise TypeError(
                f"Expected a `pa.Decimal128Type` or `pa.Decimal256Type` as the PyArrow type of a PyArrow decimal, but got: {type(dtype).__name__}"
            )

        _, digits, exponent = dec_val.as_tuple()
        scale = int(exponent * -1)
        if scale != dtype.scale:
            raise ValueError(
                f"Expected Python Decimal {dec_val} to have a scale of {dtype.scale}, but got scale {scale}"
            )
        int_val = int(dec_val.scaleb(Decimal(scale)))
        bytes_val = int_val.to_bytes((int_val.bit_length() + 7) // 8, byteorder="big", signed=True)
        precision = max(len(digits), scale)
        if precision != dtype.precision:
            raise ValueError(
                f"Expected Python Decimal {dec_val} to have a precision of {dtype.precision}, but got precision {precision}"
            )

        if isinstance(value, pa.Decimal256Scalar):
            return pb.ScalarValue(decimal256_value=pb.DecimalValue(value=bytes_val, precision=precision, scale=scale))

        return pb.ScalarValue(decimal128_value=pb.DecimalValue(value=bytes_val, precision=precision, scale=scale))

    @staticmethod
    def _deserialize_pb_to_pa_decimal(scalar_value: pb.ScalarValue) -> pa.Scalar:
        if scalar_value.HasField("decimal128_value"):
            value = scalar_value.decimal128_value
        elif scalar_value.HasField("decimal256_value"):
            value = scalar_value.decimal256_value
        else:
            raise ValueError("Protobuf ScalarValue does not contain a Decimal128 or a Decimal256 value")
        bytes_val = value.value
        expected_precision = value.precision
        scale = value.scale

        # Convert bytes back to integer
        int_val = int.from_bytes(bytes_val, byteorder="big", signed=True)

        # Construct Decimal from integer
        decimal_scale = Decimal(10) ** -scale
        dec_val = Decimal(int_val) * decimal_scale

        # Validate precision
        _, digits, exponent = dec_val.as_tuple()
        assert isinstance(exponent, int)
        actual_precision = max(len(digits), exponent * -1)
        if actual_precision != expected_precision:
            raise ValueError(f"Reconstructed Decimal has precision {expected_precision}; expected {actual_precision}")

        if scalar_value.HasField("decimal256_value"):
            dtype = pa.decimal256(actual_precision, scale)
        else:
            dtype = pa.decimal128(actual_precision, scale)
        return pa.scalar(dec_val, type=dtype)

    @classmethod
    def _serialize_pa_list_to_pb(cls, value: pa.ListScalar) -> pb.ScalarValue:
        values = value.values
        if values is None:
            return pb.ScalarValue(null_value=cls.convert_pa_dtype_to_proto_dtype(value.type))
        table = pa.Table.from_arrays([values], names=["values"])

        arrow_buffer = BytesIO()
        pf.write_feather(table, dest=arrow_buffer, compression=None)
        arrow_bytes = arrow_buffer.getvalue()

        pb_schema = pb.Schema(
            columns=[
                pb.Field(
                    nullable=False,
                    arrow_type=cls.convert_pa_dtype_to_proto_dtype(values.type),
                ),
            ]
        )

        pb_value = pb.ScalarListValue(
            arrow_data=arrow_bytes,
            schema=pb_schema,
        )
        if isinstance(value, pa.LargeListScalar):
            return pb.ScalarValue(large_list_value=pb_value)
        elif isinstance(value, pa.FixedSizeListScalar):
            return pb.ScalarValue(fixed_size_list_value=pb_value)
        elif isinstance(value, pa.MapScalar):
            return pb.ScalarValue(map_value=pb_value)
        elif isinstance(value, pa.ListScalar):
            return pb.ScalarValue(list_value=pb_value)
        else:
            raise TypeError(f"Unsupported list type: {type(value).__name__}")

    @classmethod
    def _deserialize_pb_list_to_pa(cls, scalar_value: pb.ScalarValue) -> pa.Scalar:
        if scalar_value.HasField("list_value"):
            value = scalar_value.list_value
        elif scalar_value.HasField("large_list_value"):
            value = scalar_value.large_list_value
        elif scalar_value.HasField("fixed_size_list_value"):
            value = scalar_value.fixed_size_list_value
        elif scalar_value.HasField("map_value"):
            value = scalar_value.map_value
        else:
            raise ValueError(
                "Protobuf ScalarValue does not contain the attributes "
                + "`list_value`, `large_list_value`, `map_value`, or `fixed_size_list_value`"
            )

        if not isinstance(value, pb.ScalarListValue):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"Unsupported list value type: {type(value).__name__}")

        if value.arrow_data:
            arrow_buffer = BytesIO(value.arrow_data)
            table = pf.read_table(arrow_buffer)
        else:
            raise ValueError("Missing `arrow_data` attribute in `ScalarListValue`")

        arr = table.column(0).combine_chunks()

        if scalar_value.HasField("list_value"):
            return pa.scalar(arr.to_pylist(), pa.list_(arr.type))
        elif scalar_value.HasField("large_list_value"):
            return pa.scalar(arr.to_pylist(), pa.large_list(arr.type))
        elif scalar_value.HasField("map_value"):
            if not isinstance(arr.type, pa.StructType):
                raise TypeError(f"Expected a `Struct` but got: {type(arr).__name__}")
            return pa.scalar(
                arr.to_pylist(),
                pa.map_(key_type=arr.type.field("key"), item_type=arr.type.field("value")),
            )
        else:
            return pa.scalar(arr.to_pylist(), pa.list_(arr.type, len(arr)))

    @classmethod
    def _recursive_dict_to_list_of_dicts(cls, d: Any, dtype: pa.DataType) -> Any:
        if d is None:
            return None
        if isinstance(dtype, pa.MapType):
            if isinstance(d, pa.MapScalar):
                # If the value is already wrapped as an Arrow scalar, unwrap it.
                d = {k: v for k, v in d.as_py()}

            if not isinstance(d, dict):
                raise TypeError(f"Expected a `dict` but got: {type(d).__name__}")
            return [{"key": k, "value": cls._recursive_dict_to_list_of_dicts(v, dtype.item_type)} for k, v in d.items()]
        elif isinstance(dtype, (pa.ListType, pa.LargeListType, pa.FixedSizeListType)):
            return [cls._recursive_dict_to_list_of_dicts(x, dtype.value_type) for x in d]
        elif isinstance(dtype, pa.StructType):
            if not isinstance(d, dict):
                raise TypeError(f"Expected a `dict` but got: {type(d).__name__}")
            res = {}
            for k, v in d.items():
                field_idx = dtype.get_field_index(k)
                if field_idx == -1:
                    raise ValueError(f"Struct type does not have a field named '{k}'")
                res[k] = cls._recursive_dict_to_list_of_dicts(v, dtype.field(field_idx).type)
            return res
        return d

    def from_primitive_to_protobuf(
        self,
        value: _TPrim,
    ) -> pb.ScalarValue:
        if isinstance(value, pa.Scalar):
            # This value is alreay a scalar.
            as_scalar = value
        else:
            as_arr = self.from_primitive_to_pyarrow([value])
            as_scalar = as_arr[0]
        return self.from_pyarrow_to_protobuf(as_scalar)


class TEncoder(Protocol[_TPrimCo, _TRichCon]):
    def __call__(self, value: _TRichCon, /) -> _TPrimCo:
        ...


class TDecoder(Protocol[_TPrimCon, _TRichCo]):
    def __call__(self, value: _TPrimCon, /) -> _TRichCo:
        ...


def _encode_json(t: JSON) -> str:
    return json.dumps(t)


def _decode_json(s: str) -> JSON:
    return cast(JSON, json.loads(s))


def _to_old_style_type(origin: object):
    if origin is list:
        return List
    elif origin is tuple:
        return Tuple
    elif origin is set:
        return Set
    elif origin is frozenset:
        return FrozenSet
    elif origin is dict:
        return Dict
    elif hasattr(types, "UnionType"):
        # Only available in python >=3.10
        if origin is getattr(types, "UnionType"):
            return Union
    return origin


def canonicalize_typ(x: object):
    """Canonicalize a type annotation for equality checking.
    New-style types are replaced with old-style types, and
    annotated markers are ignored. Specifically:

    - typing.Annotated -> unwrapped
    - list             -> typing.List
    - tuple            -> typing.Tuple
    - set              -> typing.Set
    - frozenset        -> typing.Frozenset
    - dict             -> typing.Dict
    - union            -> typing.Union
    """

    if x is None:
        x = type(None)
    x = unwrap_annotated_if_needed(x)
    origin, args = get_origin(x), get_args(x)
    if origin is None:
        return _to_old_style_type(x)
    origin = _to_old_style_type(origin)
    args = tuple(canonicalize_typ(x) for x in args)
    return origin[args]  # type: ignore -- pyright doesn't understand metaprogramming


@final
class JSONCodec:
    encode: TEncoder[str, JSON] = _encode_json
    decode: TDecoder[str, JSON] = _decode_json


class FeatureConverter(PrimitiveFeatureConverter[_TPrim], Generic[_TPrim, _TRich]):
    """Feature converter that deals with rich types. It supports everything that the primitive feature converter supports.

    However, since it deals with Rich types, it can only be constructed from the source code, since rich type information
    is not stored in serialized graphs."""

    def __init__(
        self,
        name: str,
        is_nullable: bool,
        rich_type: Union[Type[_TRich], ellipsis] = ...,
        primitive_default: Union[_TPrim, ellipsis] = ...,
        rich_default: Union[_TRich, ellipsis] = ...,
        pyarrow_dtype: Optional[pa.DataType] = None,
        encoder: Optional[TEncoder[_TPrim, _TRich]] = None,
        decoder: Optional[TDecoder[_TPrim, _TRich]] = None,
    ) -> None:
        self._rich_type = unwrap_annotated_if_needed(rich_type)

        if pyarrow_dtype is None:
            if rich_type is ...:
                raise ValueError("Either the `rich_type` or `pyarrow_dtype` must be provided")
            pyarrow_dtype = rich_to_pyarrow(rich_type, name)

        if rich_type is ...:
            if rich_default != ...:
                raise ValueError(
                    "The `rich_default` cannot be used without the `rich_type`. Perhaps specify the `primitive_default` instead?"
                )
            if is_nullable and primitive_default is ...:
                primitive_default = cast(_TPrim, None)

        else:
            if primitive_default != ...:
                raise ValueError(
                    "The `primitive_default` cannot be used when specifying the `rich_type`. Instead, specify the `rich_default`."
                )
            if is_nullable and rich_default is ...:
                rich_default = cast(_TRich, None)

        # In the future, we will require the rich type to be not-none and remove the primitive default flag,
        # and then we can simplify the code as follows:
        # if pyarrow_dtype is None:
        #     if rich_type is ...:
        #         raise ValueError("Either the `rich_type` or `pyarrow_dtype` must be provided")
        #     pyarrow_dtype = rich_to_pyarrow(rich_type, name)

        # elif is_nullable and rich_default is ...:
        #     rich_default = cast(_TRich, None)

        if rich_type is ...:
            if encoder is not None:
                raise ValueError("An encoder cannot be specified without also specifying the `rich_type`")
            if decoder is not None:
                raise ValueError("An encoder cannot be specified without also specifying the `rich_type`")
        self._encoder = encoder
        self._decoder = decoder
        self._rich_default = rich_default
        self._primitive_type = pyarrow_to_primitive(pyarrow_dtype, name)
        self._pyarrow_dtype = pyarrow_dtype
        self._is_nullable = is_nullable

        # This field is also set in the super() call, but must be initialized here
        # because it is also used for error handling inside of `from_rich_to_primitive`.
        self._name = name
        if rich_default != ...:
            # The missing value strategy doesn't really matter because rich_default is not missing
            primitive_default = self.from_rich_to_primitive(rich_default, missing_value_strategy="allow")
        super().__init__(
            name, is_nullable=is_nullable, pyarrow_dtype=pyarrow_dtype, primitive_default=primitive_default
        )

    @property
    def rich_type(self) -> Type[_TRich]:
        if self._rich_type is ...:
            raise ValueError(
                "Rich types cannot be used as the FeatureConverter was created without providing a `rich_type`"
            )
        return cast(Type[_TRich], self._rich_type)

    @property
    def rich_default(self) -> _TRich:
        if self._rich_default is ...:
            raise ValueError(f"Feature '{self._name}' has no default value")
        return self._rich_default

    def is_rich_valid(self, value: _TRich) -> bool:
        """Returns true if value has a valid rich type"""
        try:
            prim = self.from_rich_to_primitive(value, "default_or_error")
            pa.scalar(prim, type=self.pyarrow_dtype)
            return True
        except (TypeError, ValueError):
            return False

    def from_rich_to_pyarrow(
        self,
        values: Sequence[Union[_TRich, ellipsis, None]],
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> Union[pa.Array, pa.ChunkedArray]:
        prim_values = [self.from_rich_to_primitive(x, missing_value_strategy) for x in values]
        return self.from_primitive_to_pyarrow(prim_values)

    def from_rich_to_protobuf(
        self,
        value: Union[_TRich, ellipsis, None],
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        return self.from_primitive_to_protobuf(self.from_rich_to_primitive(value, missing_value_strategy))

    def from_rich_to_primitive(
        self,
        value: Union[_TRich, ellipsis, None],
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> _TPrim:
        # Ensure that the rich value is indeed the rich type
        # For example, if a string is passed in for a datetime value, convert it into a datetime
        if self.is_value_missing(value):
            if missing_value_strategy == "allow":
                return cast(_TPrim, value)
            elif missing_value_strategy in ("default_or_error", "default_or_allow"):
                if self.has_default:
                    return self.primitive_default
                elif missing_value_strategy == "default_or_error":
                    raise TypeError(
                        f"The value for feature '{self._name}' is missing, and this feature has no default value."
                    )
                else:
                    return cast(_TPrim, value)
            elif missing_value_strategy == "error":
                raise MissingValueError(
                    f"The value for feature '{self._name}' is missing, but `replace_missing_with_defaults` was set to False."
                )
            else:
                raise ValueError(
                    (
                        f"Unsupported missing value strategy: {missing_value_strategy}. "
                        "It must be one of 'allow', 'default_or_allow', 'default_or_error', or 'error'."
                    )
                )
        value = self.from_primitive_to_rich(cast(_TPrim, value))
        return self._to_primitive(value)

    def from_rich_to_json(
        self,
        value: Union[_TRich, ellipsis, None],
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        prim_val = self.from_rich_to_primitive(value, missing_value_strategy)
        return self.from_primitive_to_json(prim_val, options=options)

    def from_pyarrow_to_rich(self, values: Union[pa.Array, pa.ChunkedArray], /) -> Sequence[_TRich]:
        return [self.from_primitive_to_rich(x) for x in self.from_pyarrow_to_primitive(values)]

    @property
    def encoder(self) -> Optional[TEncoder[_TPrim, _TRich]]:
        return self._encoder

    @property
    def decoder(self) -> Optional[TDecoder[_TPrim, _TRich]]:
        return self._decoder

    def _to_primitive(self, val: _TRich) -> _TPrim:
        if val is None or self._encoder is None:
            # Structuring null values to the primitive type to ensure that a singular null for an entire struct
            # is propagated to individual struct fields -- e.g.
            # class LatLong:
            #     lat: Optional[float]
            #     long: Optional[float]
            # then self._from_prim(None) == LatLong(None, None)
            # Using self.primitive_type, rather than self._rich_type, as the primitive type
            # might not be registered on the converter for custom classes
            try:
                x = unstructure_rich_to_primitive(val)
            except (TypeError, ValueError) as e:
                raise TypeError(
                    f"Could not convert '{val}' to `{self.primitive_type}` for feature '{self._name}': {e}"
                ) from e
            if x is None and not self._is_nullable:
                raise ValueError(f"Feature '{self._name}' is null, but it cannot be nullable")
            try:
                return cast(_TPrim, structure_primitive_to_rich(x, self.primitive_type))
            except (TypeError, ValueError) as e:
                raise TypeError(
                    f"Could not convert '{val}' to `{self.primitive_type}` for feature '{self._name}': {e}"
                ) from e
        return self._encoder(val)

    def _from_prim(self, val: Union[_TPrim, _TRich]) -> _TRich:
        if self._rich_type is ...:
            raise ValueError(
                "Rich types cannot be used as the FeatureConverter was created without providing a `rich_type`"
            )
        if val is None:
            # Structuring null values to the primitive type to ensure that a singular null for an entire struct
            # is propagated to individual struct fields -- e.g.
            # class LatLong:
            #     lat: Optional[float]
            #     long: Optional[float]
            # then self._from_prim(None) == LatLong(None, None)
            # Using self.primitive_type, rather than self._rich_type, as the primitive type
            # might not be registered on the converter for custom classes
            try:
                val = structure_primitive_to_rich(cast(_TPrim, val), cast(Type[_TRich], self.primitive_type))
            except (TypeError, ValueError) as e:
                raise TypeError(
                    f"Could not convert '{val}' to `{self.primitive_type}` for feature '{self._name}': {e}"
                ) from e
        if self._decoder is None:
            try:
                return structure_primitive_to_rich(cast(_TPrim, val), self._rich_type)
            except (TypeError, ValueError) as e:
                raise TypeError(
                    f"Could not convert '{val}' to `{self._rich_type}` for feature '{self._name}': {e}"
                ) from e
        # is_pyarrow_json_type is only needed to handle python 3.8
        if is_pyarrow_json_type(self.pyarrow_dtype) or isinstance(
            val, unwrap_optional_and_annotated_if_needed(self._rich_type)
        ):
            return cast(_TRich, val)
        if val is None:
            # If the value is None, then we won't call the custom converter, since those likely cannot handle null values
            # and None is perfectly valid as a "rich" type
            return cast(_TRich, None)
        return self._decoder(cast(_TPrim, val))

    def from_primitive_to_rich(self, value: Union[_TPrim, _TRich]) -> _TRich:
        return self._from_prim(value)

    def from_json_to_rich(self, value: TJSON) -> _TRich:
        prim_val = self.from_json_to_primitive(value)
        return self.from_primitive_to_rich(prim_val)

    def has_nontrivial_rich_type(self) -> bool:
        if self._encoder is not None or self._decoder is not None:
            return True

        prim_canonical = canonicalize_typ(self.primitive_type)
        rich_canonical = canonicalize_typ(self.rich_type)
        if self.is_nullable:
            # Primitive type is based off of the pyarrow dtype, which doesn't know about nullability
            # So Optional[str] will become just 'str' and needs to be re-wrapped in an Optional[] to compare w/ the rich type
            # This is mainly a hack for re-creating python Feature objects from serialize proto features (e.g. for running notebook-defined resolvers)
            # We can remove this once we support encoding more information about the rich type itself in the feature proto.
            prim_canonical = typing.Optional[prim_canonical]
        return prim_canonical != rich_canonical
