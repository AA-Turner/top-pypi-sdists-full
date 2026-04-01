from __future__ import annotations

import dataclasses as _dataclasses
import io
import json
import types
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from io import BytesIO
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    FrozenSet,
    Generic,
    Iterable,
    List,
    NoReturn,
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
from typing_extensions import get_args, get_origin

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
from chalk.features.feature_wrapper import UnresolvedFeature
from chalk.utils.collections import unwrap_annotated_if_needed, unwrap_optional_and_annotated_if_needed
from chalk.utils.df_utils import pa_array_to_pl_series
from chalk.utils.json import JSON, TJSON, is_pyarrow_json_type, pyarrow_json_type
from chalk.utils.log_with_context import get_logger

# pyright: reportIncompatibleMethodOverride=false, reportMissingSuperCall=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false, reportImplicitStringConcatenation=false


_logger = get_logger(__name__)

_TRich = TypeVar("_TRich")
_TRichCo = TypeVar("_TRichCo", covariant=True)
_TRichCon = TypeVar("_TRichCon", contravariant=True)

_TPrim = TypeVar("_TPrim", bound=TPrimitive)
_TPrimCo = TypeVar("_TPrimCo", bound=TPrimitive, covariant=True)
_TPrimCon = TypeVar("_TPrimCon", bound=TPrimitive, contravariant=True)
_TScalar = TypeVar("_TScalar", bound=TPrimitive)

_DEFAULT_FEATURE_ENCODING_OPTIONS = FeatureEncodingOptions()


class FeatureConverter(Protocol[_TPrim, _TRich]):
    @property
    def rich_type(self) -> Type[_TRich]: ...

    @property
    def primitive_type(self) -> Type[TPrimitive]: ...

    @property
    def pyarrow_dtype(self) -> pa.DataType: ...

    @property
    def polars_dtype(self) -> Any: ...

    @property
    def is_nullable(self) -> bool: ...

    @property
    def has_default(self) -> bool: ...

    @property
    def pyarrow_default(self) -> ellipsis | pa.Array | pa.ChunkedArray: ...

    @property
    def primitive_default(self) -> _TPrim: ...

    @property
    def rich_default(self) -> _TRich: ...

    def has_nontrivial_rich_type(self) -> bool: ...

    @property
    def encoder(self) -> TEncoder[_TPrim, _TRich] | None: ...

    @property
    def decoder(self) -> TDecoder[_TPrim, _TRich] | None: ...

    def from_pyarrow_to_json(
        self,
        values: pa.Array | pa.ChunkedArray,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> Sequence[TJSON]: ...

    def from_pyarrow_to_primitive(self, values: Union[pa.Array, pa.ChunkedArray]) -> Sequence[_TPrim]: ...

    def from_primitive_to_pyarrow(self, value: Iterable[_TPrim]) -> Union[pa.Array, pa.ChunkedArray]: ...

    def from_primitive_to_json(
        self,
        value: TPrimitive,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON: ...

    def from_json_to_pyarrow(self, values: Sequence[TJSON]) -> Union[pa.Array, pa.ChunkedArray]: ...

    def from_json_to_primitive(self, value: TJSON | TPrimitive) -> _TPrim: ...

    def is_value_missing(self, value: Any) -> bool: ...

    def from_primitive_to_protobuf(self, value: _TPrim) -> pb.ScalarValue: ...

    def is_rich_valid(self, value: _TRich) -> bool: ...

    def from_rich_to_pyarrow(
        self,
        values: Sequence[_TRich | ellipsis | None],
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> Union[pa.Array, pa.ChunkedArray]: ...

    def from_rich_to_protobuf(
        self,
        value: _TRich | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue: ...

    def from_rich_to_primitive(
        self,
        value: _TRich | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> _TPrim: ...

    def from_rich_to_json(
        self,
        value: _TRich | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON: ...

    def from_pyarrow_to_rich(self, values: pa.Array | pa.ChunkedArray, /) -> Sequence[_TRich]: ...

    def from_primitive_to_rich(self, value: _TPrim | _TRich) -> _TRich: ...

    def from_json_to_rich(self, value: TJSON) -> _TRich: ...

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar: ...

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue: ...


try:
    import polars as pl
except ImportError:
    pl = None

_FROM_NEW = object()


def _identity(v: Any) -> Any:
    return v


_UNSUPPORTED_MISSING_VALUE_STRATEGY_MESSAGE = (
    "It must be one of 'allow', 'default_or_allow', 'default_or_error', or 'error'."
)


def _raise_unsupported_missing_value_strategy(missing_value_strategy: MissingValueStrategy) -> NoReturn:
    raise ValueError(
        f"Unsupported missing value strategy: {missing_value_strategy}. {_UNSUPPORTED_MISSING_VALUE_STRATEGY_MESSAGE}"
    )


def _unwrap_scalar_value(value: Any) -> Any:
    if isinstance(value, pa.Scalar):
        return value.as_py()
    return value


class _FeatureConverterArrowProtoHelpers:
    def convert_pa_dtype_to_proto_dtype(self, dtype: pa.DataType) -> pb.ArrowType:
        return PrimitiveFeatureConverter.convert_pa_dtype_to_proto_dtype(dtype)

    def convert_proto_dtype_to_pa_dtype(self, dtype: pb.ArrowType) -> pa.DataType:
        return PrimitiveFeatureConverter.convert_proto_dtype_to_pa_dtype(dtype)

    def convert_pa_field_to_proto_field(self, field: pa.Field) -> pb.Field:
        return PrimitiveFeatureConverter.convert_pa_field_to_proto_field(field)

    def convert_proto_field_to_pa_field(self, proto_field: pb.Field) -> pa.Field:
        return PrimitiveFeatureConverter.convert_proto_field_to_pa_field(proto_field)

    def convert_pa_schema_to_proto_schema(self, schema: pa.Schema) -> pb.Schema:
        return PrimitiveFeatureConverter.convert_pa_schema_to_proto_schema(schema)

    def convert_proto_schema_to_pa_schema(self, proto_schema: pb.Schema) -> pa.Schema:
        return PrimitiveFeatureConverter.convert_proto_schema_to_pa_schema(proto_schema)


class _SpecializedFeatureConverterProperties(Generic[_TPrim, _TRich]):
    _rich_type_value: ClassVar[Type[Any]]
    _primitive_type_value: ClassVar[Type[Any]]
    _pyarrow_dtype_value: ClassVar[pa.DataType]
    _polars_dtype_value: ClassVar[Any]

    @property
    def rich_type(self) -> Type[_TRich]:
        t = cast(Type[_TRich], type(self)._rich_type_value)
        if self._is_nullable:  # type: ignore[attr-defined]
            from typing import Optional as _Optional

            return _Optional[t]  # type: ignore[return-value]
        return t

    @property
    def primitive_type(self) -> Type[TPrimitive]:
        return cast(Type[TPrimitive], type(self)._primitive_type_value)

    @property
    def pyarrow_dtype(self) -> pa.DataType:
        return type(self)._pyarrow_dtype_value

    @property
    def polars_dtype(self) -> Any:
        return type(self)._polars_dtype_value

    @property
    def encoder(self) -> TEncoder[_TPrim, _TRich] | None:
        return None

    @property
    def decoder(self) -> TDecoder[_TPrim, _TRich] | None:
        return None


class BoolFeatureConverter(
    _FeatureConverterArrowProtoHelpers,
    _SpecializedFeatureConverterProperties[bool, bool],
    FeatureConverter[bool, bool],
):
    _rich_type_value: ClassVar[Type[bool]] = bool
    _primitive_type_value: ClassVar[Type[bool]] = bool
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.bool_()
    _polars_dtype_value: ClassVar[Any] = pl.Boolean() if pl is not None else None

    _cache: ClassVar[Dict[Tuple[bool | None | ellipsis, bool], "BoolFeatureConverter"]] = {}

    @classmethod
    def new(cls, default: bool | None | ellipsis, is_nullable: bool) -> "BoolFeatureConverter":
        key = (default, is_nullable)
        cached = cls._cache.get(key)
        if cached is not None:
            return cached
        inst = cls(default, is_nullable, _from_new=_FROM_NEW)
        cls._cache[key] = inst
        return inst

    def __init__(self, default: bool | None | ellipsis, is_nullable: bool, *, _from_new: object = None):
        super().__init__()
        if _from_new is not _FROM_NEW:
            raise TypeError("Use BoolFeatureConverter.new() instead of calling the constructor directly")
        self._is_nullable = is_nullable
        if is_nullable and default is ...:
            default = None
        if default is not ...:
            self._primitive_default: bool | None | ellipsis
            self._primitive_default = default
            self._has_default = True
            self._pyarrow_default: ellipsis | pa.Array | pa.ChunkedArray = pa.array([default], type=pa.bool_())
        else:
            self._has_default = False
            self._primitive_default = ...
            self._pyarrow_default = ...

    @property
    def is_nullable(self) -> bool:
        return self._is_nullable

    @property
    def has_default(self) -> bool:
        return self._has_default

    @property
    def pyarrow_default(self) -> ellipsis | pa.Array | pa.ChunkedArray:
        return self._pyarrow_default

    @property
    def primitive_default(self) -> bool:
        if self._primitive_default is ...:
            raise ValueError("No default value specified")
        return cast(bool, self._primitive_default)

    @property
    def rich_default(self) -> bool:
        return self.primitive_default

    def has_nontrivial_rich_type(self) -> bool:
        return False

    def from_pyarrow_to_json(
        self,
        values: pa.Array | pa.ChunkedArray,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> Sequence[TJSON]:
        return values.to_pylist()

    def from_pyarrow_to_primitive(self, values: Union[pa.Array, pa.ChunkedArray]) -> Sequence[bool]:
        return values.to_pylist()

    def from_primitive_to_pyarrow(self, value: Iterable[bool]) -> Union[pa.Array, pa.ChunkedArray]:
        return pa.array([None if x is ... else x for x in value], type=pa.bool_())

    def from_primitive_to_json(
        self,
        value: TPrimitive,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        return value

    def from_json_to_pyarrow(self, values: Sequence[TJSON]) -> Union[pa.Array, pa.ChunkedArray]:
        converted: list[bool | None] = []
        for value in values:
            if value is None or value is ...:
                converted.append(None)
            elif value in (True, 1, 1.0):
                converted.append(True)
            elif value in (False, 0, 0.0):
                converted.append(False)
            else:
                raise TypeError(
                    f"Could not convert '{value}' to `<class 'bool'>`: Cannot convert '{value}' to a Boolean. Valid values are 1, True, 0, or False."
                )
        return pa.array(converted, type=pa.bool_())

    def from_json_to_primitive(self, value: TJSON | TPrimitive) -> bool:
        if value is None:
            return cast(bool, None)
        if value in (True, 1, 1.0):
            return True
        if value in (False, 0, 0.0):
            return False
        raise TypeError(
            f"Could not convert '{value}' to `<class 'bool'>`: Cannot convert '{value}' to a Boolean. Valid values are 1, True, 0, or False."
        )

    def is_value_missing(self, value: Any) -> bool:
        if value is ...:
            return True
        if value is None:
            return not self._is_nullable
        return False

    def from_primitive_to_protobuf(self, value: bool | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(bool=pb.EmptyMessage()))
        return pb.ScalarValue(bool_value=cast(bool, scalar_value))

    def is_rich_valid(self, value: bool) -> bool:
        try:
            pa.scalar(self.from_rich_to_primitive(value, "default_or_error"), type=pa.bool_())
            return True
        except (TypeError, ValueError):
            return False

    def from_rich_to_pyarrow(
        self,
        values: Sequence[bool | ellipsis | None],
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> Union[pa.Array, pa.ChunkedArray]:
        pa_values = [
            None if x is ... else (None if x is None else structure_primitive_to_rich(x, bool)) for x in values
        ]
        if missing_value_strategy == "allow":
            return pa.array(pa_values, type=pa.bool_())
        if missing_value_strategy == "default_or_allow":
            if not self._has_default:
                return pa.array(pa_values, type=pa.bool_())
            if self._is_nullable:
                return pa.array(
                    [
                        (
                            self.primitive_default
                            if x is ...
                            else (None if x is None else structure_primitive_to_rich(x, bool))
                        )
                        for x in values
                    ],
                    type=pa.bool_(),
                )
            return cast(
                Union[pa.Array, pa.ChunkedArray],
                pc.fill_null(pa.array(pa_values, type=pa.bool_()), pa.scalar(self.primitive_default, type=pa.bool_())),
            )
        if missing_value_strategy == "default_or_error":
            if self._has_default:
                if self._is_nullable:
                    return pa.array(
                        [
                            (
                                self.primitive_default
                                if x is ...
                                else (None if x is None else structure_primitive_to_rich(x, bool))
                            )
                            for x in values
                        ],
                        type=pa.bool_(),
                    )
                return cast(
                    Union[pa.Array, pa.ChunkedArray],
                    pc.fill_null(
                        pa.array(pa_values, type=pa.bool_()),
                        pa.scalar(self.primitive_default, type=pa.bool_()),
                    ),
                )
            for x in values:
                if x is ... or (x is None and not self._is_nullable):
                    raise TypeError("The value is missing, and this feature has no default value.")
            return pa.array(pa_values, type=pa.bool_())
        if missing_value_strategy == "error":
            for x in values:
                if x is ... or (x is None and not self._is_nullable):
                    raise MissingValueError(
                        "The value is missing, but `replace_missing_with_defaults` was set to `False`."
                    )
            return pa.array(pa_values, type=pa.bool_())
        _raise_unsupported_missing_value_strategy(missing_value_strategy)

    def from_rich_to_protobuf(
        self,
        value: bool | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(bool | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(bool=pb.EmptyMessage()))
        return pb.ScalarValue(bool_value=prim)

    def from_rich_to_primitive(
        self,
        value: bool | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> bool:
        if value is ... or (value is None and not self._is_nullable):
            if missing_value_strategy == "allow":
                return cast(bool, value)
            elif missing_value_strategy == "default_or_error":
                if self._has_default:
                    return self.primitive_default
                raise TypeError("The value is missing, and this feature has no default value.")
            elif missing_value_strategy == "default_or_allow":
                if self._has_default:
                    return self.primitive_default
                return cast(bool, value)
            elif missing_value_strategy == "error":
                raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
            else:
                _raise_unsupported_missing_value_strategy(missing_value_strategy)
        return structure_primitive_to_rich(value, bool)

    def from_rich_to_json(
        self,
        value: bool | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        if value is ... or (value is None and not self._is_nullable):
            if missing_value_strategy == "allow":
                return cast(TJSON, value)
            if missing_value_strategy == "default_or_error":
                if self._has_default:
                    return cast(TJSON, self.primitive_default)
                raise TypeError("The value is missing, and this feature has no default value.")
            if missing_value_strategy == "default_or_allow":
                if self._has_default:
                    return cast(TJSON, self.primitive_default)
                return cast(TJSON, value)
            if missing_value_strategy == "error":
                raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
            _raise_unsupported_missing_value_strategy(missing_value_strategy)
        return structure_primitive_to_rich(value, bool)

    def from_pyarrow_to_rich(self, values: pa.Array | pa.ChunkedArray, /) -> Sequence[bool]:
        return values.to_pylist()

    def from_primitive_to_rich(self, value: bool) -> bool:
        return structure_primitive_to_rich(value, bool)

    def from_json_to_rich(self, value: TJSON) -> bool:
        return self.from_json_to_primitive(value)

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.bool_())[0]
        if pb_value.HasField("bool_value"):
            return pa.scalar(pb_value.bool_value, pa.bool_())
        raise ValueError(f"Unsupported protobuf value for BoolFeatureConverter: {pb_value}")

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        scalar_value = value.as_py()
        if scalar_value is None:
            return pb.ScalarValue(null_value=pb.ArrowType(bool=pb.EmptyMessage()))
        return pb.ScalarValue(bool_value=cast(bool, scalar_value))


class Int64FeatureConverter(
    _FeatureConverterArrowProtoHelpers,
    _SpecializedFeatureConverterProperties[int, int],
    FeatureConverter[int, int],
):
    _rich_type_value: ClassVar[Type[int]] = int
    _primitive_type_value: ClassVar[Type[int]] = int
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.int64()
    _polars_dtype_value: ClassVar[Any] = pl.Int64() if pl is not None else None

    _cache: ClassVar[Dict[Tuple[int | None | ellipsis, bool], "Int64FeatureConverter"]] = {}

    @classmethod
    def new(cls, default: int | None | ellipsis, is_nullable: bool) -> "Int64FeatureConverter":
        key = (default, is_nullable)
        cached = cls._cache.get(key)
        if cached is not None:
            return cached
        inst = cls(default, is_nullable, _from_new=_FROM_NEW)
        cls._cache[key] = inst
        return inst

    def __init__(self, default: int | None | ellipsis, is_nullable: bool, *, _from_new: object = None):
        super().__init__()
        if _from_new is not _FROM_NEW:
            raise TypeError("Use Int64FeatureConverter.new() instead of calling the constructor directly")
        self._is_nullable = is_nullable
        if is_nullable and default is ...:
            default = None
        if default is not ...:
            self._primitive_default: int | None | ellipsis
            self._primitive_default = default
            self._has_default = True
            self._pyarrow_default: ellipsis | pa.Array | pa.ChunkedArray = pa.array([default], type=pa.int64())
        else:
            self._has_default = False
            self._primitive_default = ...
            self._pyarrow_default = ...

    @property
    def is_nullable(self) -> bool:
        return self._is_nullable

    @property
    def has_default(self) -> bool:
        return self._has_default

    @property
    def pyarrow_default(self) -> ellipsis | pa.Array | pa.ChunkedArray:
        return self._pyarrow_default

    @property
    def primitive_default(self) -> int:
        if self._primitive_default is ...:
            raise ValueError("No default value specified")
        return cast(int, self._primitive_default)

    @property
    def rich_default(self) -> int:
        if self._primitive_default is ...:
            raise ValueError("No default value specified")
        return cast(int, self._primitive_default)

    def has_nontrivial_rich_type(self) -> bool:
        return False

    def from_pyarrow_to_json(
        self,
        values: pa.Array | pa.ChunkedArray,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> Sequence[TJSON]:
        return values.to_pylist()

    def from_pyarrow_to_primitive(self, values: Union[pa.Array, pa.ChunkedArray]) -> Sequence[int]:
        return values.to_pylist()

    def from_primitive_to_pyarrow(self, value: Iterable[int]) -> Union[pa.Array, pa.ChunkedArray]:
        return pa.array([None if x is ... else x for x in value], type=pa.int64())

    def from_primitive_to_json(
        self,
        value: TPrimitive,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        return value

    def from_json_to_pyarrow(self, values: Sequence[TJSON]) -> Union[pa.Array, pa.ChunkedArray]:
        return pa.array(
            [None if x is None or x is ... else int(cast(Any, x)) for x in values],
            type=pa.int64(),
        )

    def from_json_to_primitive(self, value: TJSON | TPrimitive) -> int:
        if value is None or value is ...:
            return cast(int, None)
        return int(cast(Any, value))

    def is_value_missing(self, value: Any) -> bool:
        if value is ...:
            return True
        if value is None:
            return not self._is_nullable
        return False

    def from_primitive_to_protobuf(self, value: int | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(int64=pb.EmptyMessage()))
        return pb.ScalarValue(int64_value=cast(int, scalar_value))

    def is_rich_valid(self, value: int) -> bool:
        try:
            pa.scalar(self.from_rich_to_primitive(value, "default_or_error"), type=pa.int64())
            return True
        except (TypeError, ValueError):
            return False

    def from_rich_to_pyarrow(
        self,
        values: Sequence[int | ellipsis | None],
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> Union[pa.Array, pa.ChunkedArray]:
        pa_values = [None if x is ... else (None if x is None else int(x)) for x in values]
        if missing_value_strategy == "allow":
            return pa.array(pa_values, type=pa.int64())
        if missing_value_strategy == "default_or_allow":
            if not self._has_default:
                return pa.array(pa_values, type=pa.int64())
            if self._is_nullable:
                return pa.array(
                    [self.primitive_default if x is ... else (None if x is None else int(x)) for x in values],
                    type=pa.int64(),
                )
            return cast(
                Union[pa.Array, pa.ChunkedArray],
                pc.fill_null(pa.array(pa_values, type=pa.int64()), pa.scalar(self.primitive_default, type=pa.int64())),
            )
        if missing_value_strategy == "default_or_error":
            if self._has_default:
                if self._is_nullable:
                    return pa.array(
                        [self.primitive_default if x is ... else (None if x is None else int(x)) for x in values],
                        type=pa.int64(),
                    )
                return cast(
                    Union[pa.Array, pa.ChunkedArray],
                    pc.fill_null(
                        pa.array(pa_values, type=pa.int64()),
                        pa.scalar(self.primitive_default, type=pa.int64()),
                    ),
                )
            for x in values:
                if x is ... or (x is None and not self._is_nullable):
                    raise TypeError("The value is missing, and this feature has no default value.")
            return pa.array(pa_values, type=pa.int64())
        if missing_value_strategy == "error":
            for x in values:
                if x is ... or (x is None and not self._is_nullable):
                    raise MissingValueError(
                        "The value is missing, but `replace_missing_with_defaults` was set to `False`."
                    )
            return pa.array(pa_values, type=pa.int64())
        _raise_unsupported_missing_value_strategy(missing_value_strategy)

    def from_rich_to_protobuf(
        self,
        value: int | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(int | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None:
            return pb.ScalarValue(null_value=pb.ArrowType(int64=pb.EmptyMessage()))
        if prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(int64=pb.EmptyMessage()))
        return pb.ScalarValue(int64_value=prim)

    def from_rich_to_primitive(
        self,
        value: int | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> int:
        if value is ... or (value is None and not self._is_nullable):
            if missing_value_strategy == "allow":
                return cast(int, value)
            elif missing_value_strategy == "default_or_error":
                if self._has_default:
                    return self.primitive_default
                raise TypeError("The value is missing, and this feature has no default value.")
            elif missing_value_strategy == "default_or_allow":
                if self._has_default:
                    return self.primitive_default
                return cast(int, value)
            elif missing_value_strategy == "error":
                raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
            else:
                _raise_unsupported_missing_value_strategy(missing_value_strategy)
        if value is None:
            return cast(int, None)
        return int(cast(Any, value))

    def from_rich_to_json(
        self,
        value: int | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        if value is ... or (value is None and not self._is_nullable):
            if missing_value_strategy == "allow":
                return cast(TJSON, value)
            if missing_value_strategy == "default_or_error":
                if self._has_default:
                    return cast(TJSON, self.primitive_default)
                raise TypeError("The value is missing, and this feature has no default value.")
            if missing_value_strategy == "default_or_allow":
                if self._has_default:
                    return cast(TJSON, self.primitive_default)
                return cast(TJSON, value)
            if missing_value_strategy == "error":
                raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
            _raise_unsupported_missing_value_strategy(missing_value_strategy)
        if value is None:
            return None
        return int(cast(Any, value))

    def from_pyarrow_to_rich(self, values: pa.Array | pa.ChunkedArray, /) -> Sequence[int]:
        return values.to_pylist()

    def from_primitive_to_rich(self, value: int | None) -> int:
        if value is None:
            return cast(int, None)
        if value is ...:
            return cast(int, ...)
        return int(cast(Any, value))

    def from_json_to_rich(self, value: TJSON) -> int:
        if value is None:
            return cast(int, None)
        return int(cast(Any, value))

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.int64())[0]
        if pb_value.HasField("int64_value"):
            return pa.scalar(pb_value.int64_value, pa.int64())
        raise ValueError(f"Unsupported protobuf value for Int64FeatureConverter: {pb_value}")

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        scalar_value = value.as_py()
        if scalar_value is None:
            return pb.ScalarValue(null_value=pb.ArrowType(int64=pb.EmptyMessage()))
        return pb.ScalarValue(int64_value=cast(int, scalar_value))


class Int32FeatureConverter(
    _FeatureConverterArrowProtoHelpers,
    _SpecializedFeatureConverterProperties[int, int],
    FeatureConverter[int, int],
):
    _rich_type_value: ClassVar[Type[int]] = int
    _primitive_type_value: ClassVar[Type[int]] = int
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.int32()
    _polars_dtype_value: ClassVar[Any] = pl.Int32() if pl is not None else None

    _cache: ClassVar[Dict[Tuple[int | None | ellipsis, bool], "Int32FeatureConverter"]] = {}

    @classmethod
    def new(cls, default: int | None | ellipsis, is_nullable: bool) -> "Int32FeatureConverter":
        key = (default, is_nullable)
        cached = cls._cache.get(key)
        if cached is not None:
            return cached
        inst = cls(default, is_nullable, _from_new=_FROM_NEW)
        cls._cache[key] = inst
        return inst

    def __init__(self, default: int | None | ellipsis, is_nullable: bool, *, _from_new: object = None):
        super().__init__()
        if _from_new is not _FROM_NEW:
            raise TypeError("Use Int32FeatureConverter.new() instead of calling the constructor directly")
        self._is_nullable = is_nullable
        if is_nullable and default is ...:
            default = None
        if default is not ...:
            self._primitive_default: int | None | ellipsis
            self._primitive_default = default
            self._has_default = True
            self._pyarrow_default: ellipsis | pa.Array | pa.ChunkedArray = pa.array([default], type=pa.int32())
        else:
            self._has_default = False
            self._primitive_default = ...
            self._pyarrow_default = ...

    @property
    def is_nullable(self) -> bool:
        return self._is_nullable

    @property
    def has_default(self) -> bool:
        return self._has_default

    @property
    def pyarrow_default(self) -> ellipsis | pa.Array | pa.ChunkedArray:
        return self._pyarrow_default

    @property
    def primitive_default(self) -> int:
        if self._primitive_default is ...:
            raise ValueError("No default value specified")
        return cast(int, self._primitive_default)

    @property
    def rich_default(self) -> int:
        return self.primitive_default

    def has_nontrivial_rich_type(self) -> bool:
        return False

    def from_pyarrow_to_json(
        self,
        values: pa.Array | pa.ChunkedArray,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> Sequence[TJSON]:
        return values.to_pylist()

    def from_pyarrow_to_primitive(self, values: Union[pa.Array, pa.ChunkedArray]) -> Sequence[int]:
        return values.to_pylist()

    def from_primitive_to_pyarrow(self, value: Iterable[int]) -> Union[pa.Array, pa.ChunkedArray]:
        return pa.array([None if x is ... else x for x in value], type=pa.int32())

    def from_primitive_to_json(
        self,
        value: TPrimitive,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        return value

    def from_json_to_pyarrow(self, values: Sequence[TJSON]) -> Union[pa.Array, pa.ChunkedArray]:
        return pa.array(
            [None if x is None or x is ... else int(cast(Any, x)) for x in values],
            type=pa.int32(),
        )

    def from_json_to_primitive(self, value: TJSON | TPrimitive) -> int:
        if value is None:
            return cast(int, None)
        return int(cast(Any, value))

    def is_value_missing(self, value: Any) -> bool:
        if value is ...:
            return True
        if value is None:
            return not self._is_nullable
        return False

    def from_primitive_to_protobuf(self, value: int | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(int32=pb.EmptyMessage()))
        return pb.ScalarValue(int32_value=cast(int, scalar_value))

    def is_rich_valid(self, value: int) -> bool:
        try:
            pa.scalar(self.from_rich_to_primitive(value, "default_or_error"), type=pa.int32())
            return True
        except (TypeError, ValueError):
            return False

    def from_rich_to_pyarrow(
        self,
        values: Sequence[int | ellipsis | None],
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> Union[pa.Array, pa.ChunkedArray]:
        pa_values = [None if x is ... else (None if x is None else int(x)) for x in values]
        if missing_value_strategy == "allow":
            return pa.array(pa_values, type=pa.int32())
        if missing_value_strategy == "default_or_allow":
            if not self._has_default:
                return pa.array(pa_values, type=pa.int32())
            if self._is_nullable:
                return pa.array(
                    [self.primitive_default if x is ... else (None if x is None else int(x)) for x in values],
                    type=pa.int32(),
                )
            return cast(
                Union[pa.Array, pa.ChunkedArray],
                pc.fill_null(pa.array(pa_values, type=pa.int32()), pa.scalar(self.primitive_default, type=pa.int32())),
            )
        if missing_value_strategy == "default_or_error":
            if self._has_default:
                if self._is_nullable:
                    return pa.array(
                        [self.primitive_default if x is ... else (None if x is None else int(x)) for x in values],
                        type=pa.int32(),
                    )
                return cast(
                    Union[pa.Array, pa.ChunkedArray],
                    pc.fill_null(
                        pa.array(pa_values, type=pa.int32()),
                        pa.scalar(self.primitive_default, type=pa.int32()),
                    ),
                )
            for x in values:
                if x is ... or (x is None and not self._is_nullable):
                    raise TypeError("The value is missing, and this feature has no default value.")
            return pa.array(pa_values, type=pa.int32())
        if missing_value_strategy == "error":
            for x in values:
                if x is ... or (x is None and not self._is_nullable):
                    raise MissingValueError(
                        "The value is missing, but `replace_missing_with_defaults` was set to `False`."
                    )
            return pa.array(pa_values, type=pa.int32())
        _raise_unsupported_missing_value_strategy(missing_value_strategy)

    def from_rich_to_protobuf(
        self,
        value: int | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(int | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(int32=pb.EmptyMessage()))
        return pb.ScalarValue(int32_value=prim)

    def from_rich_to_primitive(
        self,
        value: int | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> int:
        if value is ... or (value is None and not self._is_nullable):
            if missing_value_strategy == "allow":
                return cast(int, value)
            elif missing_value_strategy == "default_or_error":
                if self._has_default:
                    return self.primitive_default
                raise TypeError("The value is missing, and this feature has no default value.")
            elif missing_value_strategy == "default_or_allow":
                if self._has_default:
                    return self.primitive_default
                return cast(int, value)
            elif missing_value_strategy == "error":
                raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
            else:
                _raise_unsupported_missing_value_strategy(missing_value_strategy)
        if value is None:
            return cast(int, None)
        return int(cast(Any, value))

    def from_rich_to_json(
        self,
        value: int | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        if value is ... or (value is None and not self._is_nullable):
            if missing_value_strategy == "allow":
                return cast(TJSON, value)
            if missing_value_strategy == "default_or_error":
                if self._has_default:
                    return cast(TJSON, self.primitive_default)
                raise TypeError("The value is missing, and this feature has no default value.")
            if missing_value_strategy == "default_or_allow":
                if self._has_default:
                    return cast(TJSON, self.primitive_default)
                return cast(TJSON, value)
            if missing_value_strategy == "error":
                raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
            _raise_unsupported_missing_value_strategy(missing_value_strategy)
        if value is None:
            return None
        return int(cast(Any, value))

    def from_pyarrow_to_rich(self, values: pa.Array | pa.ChunkedArray, /) -> Sequence[int]:
        return values.to_pylist()

    def from_primitive_to_rich(self, value: int | None) -> int:
        if value is None or value is ...:
            return cast(int, value)
        return int(cast(Any, value))

    def from_json_to_rich(self, value: TJSON) -> int:
        if value is None:
            return cast(int, None)
        return int(cast(Any, value))

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.int32())[0]
        if pb_value.HasField("int32_value"):
            return pa.scalar(pb_value.int32_value, pa.int32())
        raise ValueError(f"Unsupported protobuf value for Int32FeatureConverter: {pb_value}")

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        scalar_value = value.as_py()
        if scalar_value is None:
            return pb.ScalarValue(null_value=pb.ArrowType(int32=pb.EmptyMessage()))
        return pb.ScalarValue(int32_value=cast(int, scalar_value))


class StringFeatureConverter(
    _FeatureConverterArrowProtoHelpers,
    _SpecializedFeatureConverterProperties[str, str],
    FeatureConverter[str, str],
):
    _rich_type_value: ClassVar[Type[str]] = str
    _primitive_type_value: ClassVar[Type[str]] = str
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.utf8()
    _polars_dtype_value: ClassVar[Any] = pl.Utf8() if pl is not None else None

    _cache: ClassVar[Dict[Tuple[str | None | ellipsis, bool], "StringFeatureConverter"]] = {}

    @classmethod
    def new(cls, default: str | None | ellipsis, is_nullable: bool) -> "StringFeatureConverter":
        key = (default, is_nullable)
        cached = cls._cache.get(key)
        if cached is not None:
            return cached
        inst = cls(default, is_nullable, _from_new=_FROM_NEW)
        cls._cache[key] = inst
        return inst

    def __init__(self, default: str | None | ellipsis, is_nullable: bool, *, _from_new: object = None):
        super().__init__()
        if _from_new is not _FROM_NEW:
            raise TypeError("Use StringFeatureConverter.new() instead of calling the constructor directly")
        self._is_nullable = is_nullable
        if is_nullable and default is ...:
            default = None
        if default is not ...:
            self._primitive_default: str | None | ellipsis
            self._primitive_default = default
            self._has_default = True
            self._pyarrow_default: ellipsis | pa.Array | pa.ChunkedArray = pa.array([default], type=pa.utf8())
        else:
            self._has_default = False
            self._primitive_default = ...
            self._pyarrow_default = ...

    @property
    def is_nullable(self) -> bool:
        return self._is_nullable

    @property
    def has_default(self) -> bool:
        return self._has_default

    @property
    def pyarrow_default(self) -> ellipsis | pa.Array | pa.ChunkedArray:
        return self._pyarrow_default

    @property
    def primitive_default(self) -> str:
        if self._primitive_default is ...:
            raise ValueError("No default value specified")
        return cast(str, self._primitive_default)

    @property
    def rich_default(self) -> str:
        return self.primitive_default

    def has_nontrivial_rich_type(self) -> bool:
        return False

    def from_pyarrow_to_json(
        self,
        values: pa.Array | pa.ChunkedArray,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> Sequence[TJSON]:
        return values.to_pylist()

    def from_pyarrow_to_primitive(self, values: Union[pa.Array, pa.ChunkedArray]) -> Sequence[str]:
        return values.to_pylist()

    def from_primitive_to_pyarrow(self, value: Iterable[str]) -> Union[pa.Array, pa.ChunkedArray]:
        return pa.array([None if x is ... else x for x in value], type=pa.utf8())

    def from_primitive_to_json(
        self,
        value: TPrimitive,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        return value

    def from_json_to_pyarrow(self, values: Sequence[TJSON]) -> Union[pa.Array, pa.ChunkedArray]:
        return pa.array(
            [None if x is None or x is ... else x for x in values],
            type=pa.utf8(),
        )

    def from_json_to_primitive(self, value: TJSON | TPrimitive) -> str:
        if value is None:
            return cast(str, None)
        return cast(str, value)

    def is_value_missing(self, value: Any) -> bool:
        if value is ...:
            return True
        if value is None:
            return not self._is_nullable
        return False

    def from_primitive_to_protobuf(self, value: str | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(utf8=pb.EmptyMessage()))
        return pb.ScalarValue(utf8_value=cast(str, scalar_value))

    def is_rich_valid(self, value: str) -> bool:
        try:
            pa.scalar(self.from_rich_to_primitive(value, "default_or_error"), type=pa.utf8())
            return True
        except (TypeError, ValueError):
            return False

    def from_rich_to_pyarrow(
        self,
        values: Sequence[str | ellipsis | None],
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> Union[pa.Array, pa.ChunkedArray]:
        pa_values = [None if x is ... else (None if x is None else str(x)) for x in values]
        if missing_value_strategy == "allow":
            return pa.array(pa_values, type=pa.utf8())
        if missing_value_strategy == "default_or_allow":
            if not self._has_default:
                return pa.array(pa_values, type=pa.utf8())
            if self._is_nullable:
                return pa.array(
                    [self.primitive_default if x is ... else (None if x is None else str(x)) for x in values],
                    type=pa.utf8(),
                )
            return cast(
                Union[pa.Array, pa.ChunkedArray],
                pc.fill_null(pa.array(pa_values, type=pa.utf8()), pa.scalar(self.primitive_default, type=pa.utf8())),
            )
        if missing_value_strategy == "default_or_error":
            if self._has_default:
                if self._is_nullable:
                    return pa.array(
                        [self.primitive_default if x is ... else (None if x is None else str(x)) for x in values],
                        type=pa.utf8(),
                    )
                return cast(
                    Union[pa.Array, pa.ChunkedArray],
                    pc.fill_null(
                        pa.array(pa_values, type=pa.utf8()),
                        pa.scalar(self.primitive_default, type=pa.utf8()),
                    ),
                )
            for x in values:
                if x is ... or (x is None and not self._is_nullable):
                    raise TypeError("The value is missing, and this feature has no default value.")
            return pa.array(pa_values, type=pa.utf8())
        if missing_value_strategy == "error":
            for x in values:
                if x is ... or (x is None and not self._is_nullable):
                    raise MissingValueError(
                        "The value is missing, but `replace_missing_with_defaults` was set to `False`."
                    )
            return pa.array(pa_values, type=pa.utf8())
        _raise_unsupported_missing_value_strategy(missing_value_strategy)

    def from_rich_to_protobuf(
        self,
        value: str | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(str | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None:
            return pb.ScalarValue(null_value=pb.ArrowType(utf8=pb.EmptyMessage()))
        return pb.ScalarValue(utf8_value=prim)

    def from_rich_to_primitive(
        self,
        value: str | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> str:
        if value is ... or (value is None and not self._is_nullable):
            if missing_value_strategy == "allow":
                return cast(str, value)
            elif missing_value_strategy == "default_or_error":
                if self._has_default:
                    return self.primitive_default
                raise TypeError("The value is missing, and this feature has no default value.")
            elif missing_value_strategy == "default_or_allow":
                if self._has_default:
                    return self.primitive_default
                return cast(str, value)
            elif missing_value_strategy == "error":
                raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
            else:
                _raise_unsupported_missing_value_strategy(missing_value_strategy)
        if value is None:
            return cast(str, None)
        return str(value)

    def from_rich_to_json(
        self,
        value: str | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        if value is ... or (value is None and not self._is_nullable):
            if missing_value_strategy == "allow":
                return cast(TJSON, value)
            if missing_value_strategy == "default_or_error":
                if self._has_default:
                    return cast(TJSON, self.primitive_default)
                raise TypeError("The value is missing, and this feature has no default value.")
            if missing_value_strategy == "default_or_allow":
                if self._has_default:
                    return cast(TJSON, self.primitive_default)
                return cast(TJSON, value)
            if missing_value_strategy == "error":
                raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
            _raise_unsupported_missing_value_strategy(missing_value_strategy)
        if value is None:
            return None
        return str(value)

    def from_pyarrow_to_rich(self, values: pa.Array | pa.ChunkedArray, /) -> Sequence[str]:
        return values.to_pylist()

    def from_primitive_to_rich(self, value: str | None) -> str:
        if value is None:
            return cast(str, None)
        return str(value)

    def from_json_to_rich(self, value: TJSON) -> str:
        if value is None:
            return cast(str, None)
        return str(value)

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.utf8())[0]
        if pb_value.HasField("utf8_value"):
            return pa.scalar(pb_value.utf8_value, pa.utf8())
        raise ValueError(f"Unsupported protobuf value for StringFeatureConverter: {pb_value}")

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        scalar_value = value.as_py()
        if scalar_value is None:
            return pb.ScalarValue(null_value=pb.ArrowType(utf8=pb.EmptyMessage()))
        return pb.ScalarValue(utf8_value=cast(str, scalar_value))


def _build_to_primitive_converter(typ: type) -> "Callable[[Any], Any] | None":
    """Return a closure that converts a value of *typ* to its primitive form, or ``None`` if
    the type is already primitive (no conversion needed).

    Handles arbitrary nesting: dataclasses, ``list[T]``, and combinations thereof.
    ``Optional[T]`` / ``Annotated[T, ...]`` wrappers are stripped before dispatch.
    """
    inner = unwrap_optional_and_annotated_if_needed(typ)

    if _dataclasses.is_dataclass(inner) and isinstance(inner, type):
        return _build_dc_to_dict(inner)

    origin = get_origin(inner)
    if origin in (list, List):
        args = get_args(inner)
        if args:
            item_conv = _build_to_primitive_converter(args[0])
            if item_conv is not None:
                return lambda lst, _c=item_conv: None if lst is None else [_c(x) for x in lst]

    return None


def _build_to_rich_converter(typ: type) -> "Callable[[Any], Any] | None":
    """Return a closure that converts a primitive value back to *typ*, or ``None`` if
    the type is already primitive (no conversion needed).

    Mirrors :func:`_build_to_primitive_converter` in the reverse direction.
    """
    inner = unwrap_optional_and_annotated_if_needed(typ)

    if _dataclasses.is_dataclass(inner) and isinstance(inner, type):
        return _build_dict_to_dc(inner)

    origin = get_origin(inner)
    if origin in (list, List):
        args = get_args(inner)
        if args:
            item_conv = _build_to_rich_converter(args[0])
            if item_conv is not None:
                return lambda lst, _c=item_conv: None if lst is None else [_c(x) for x in lst]

    return None


def _build_dc_to_dict(dc_class: type) -> "Callable[[Any], Any]":
    """Build a converter from a dataclass instance to a plain dict.

    Uses :func:`_build_to_primitive_converter` for each field, so nested
    dataclasses, ``list[dataclass]``, and any combination are handled recursively.
    Primitive fields are read directly from ``v.__dict__`` with no extra calls.
    """
    import typing as _typing_mod

    field_names: tuple[str, ...] = tuple(f.name for f in _dataclasses.fields(dc_class))
    hints = _typing_mod.get_type_hints(dc_class)

    sub: dict[str, Callable] = {
        name: conv for name in field_names if (conv := _build_to_primitive_converter(hints[name])) is not None
    }

    null_prim: dict = {f: None for f in field_names}

    if not sub:

        def _convert_flat(v: Any) -> Any:
            if v is None:
                return null_prim
            if v is ...:
                return v
            # Assume v is a dataclass or dict
            d = getattr(v, "__dict__", v)
            return {f: d[f] for f in field_names}

        return _convert_flat
    else:

        def _convert_nested(v: Any) -> Any:
            if v is None:
                return {f: sub[f](None) if f in sub else None for f in field_names}
            # Assume v is a dataclass or dict
            d = getattr(v, "__dict__", v)
            return {f: sub[f](d[f]) if f in sub else d[f] for f in field_names}

        return _convert_nested


def _build_dict_to_dc(dc_class: type) -> "Callable[[Any], Any]":
    """Build a converter from a plain dict back to a dataclass instance.

    Uses :func:`_build_to_rich_converter` for each field, mirroring
    :func:`_build_dc_to_dict` in the reverse direction.
    """
    import typing as _typing_mod

    field_names: tuple[str, ...] = tuple(f.name for f in _dataclasses.fields(dc_class))
    hints = _typing_mod.get_type_hints(dc_class)

    sub: dict[str, Callable] = {
        name: conv for name in field_names if (conv := _build_to_rich_converter(hints[name])) is not None
    }

    if not sub:

        def _reconstruct_flat(d: Any) -> Any:
            if d is None:
                return dc_class(*[None] * len(field_names))
            if isinstance(d, dc_class):
                return d
            return dc_class(**d)

        return _reconstruct_flat
    else:

        def _reconstruct_nested(d: Any) -> Any:
            if d is None:
                return dc_class(**{f: sub[f](None) if f in sub else None for f in field_names})
            if isinstance(d, dc_class):
                return d
            return dc_class(**{f: sub[f](d[f]) if f in sub else d[f] for f in field_names})

        return _reconstruct_nested


class DataclassFeatureConverter(
    _FeatureConverterArrowProtoHelpers,
    FeatureConverter["dict[str, Any]", Any],
):
    """Full :class:`FeatureConverter` for a single dataclass (struct) element.

    Rich type:      T (a dataclass)
    Primitive type: dict[str, Any]
    PyArrow type:   pa.struct([...])

    Also serves as the ``item_converter`` for :class:`ListConverter`.  Use
    :meth:`for_class` to get a cached instance suitable for that purpose.
    """

    _cache: ClassVar[Dict[Tuple[type, Any, bool], "DataclassFeatureConverter"]] = {}

    @classmethod
    def for_class(cls, dc_class: type) -> "DataclassFeatureConverter":
        """Return a cached ``DataclassConverter`` (``is_nullable=True``, no default).

        Suitable for use as the ``item_converter`` in :class:`ListConverter`.
        """
        return cls.new(dc_class, ..., is_nullable=True)

    @classmethod
    def new(
        cls,
        dc_class: type,
        default: "Any | ellipsis",
        is_nullable: bool,
    ) -> "DataclassFeatureConverter":
        """Factory with caching for simple defaults (``None`` / ``...``)."""
        if default is None or default is ...:
            key = (dc_class, default, is_nullable)
            cached = cls._cache.get(key)
            if cached is not None:
                return cached
            inst = cls(dc_class, default, is_nullable, _from_new=_FROM_NEW)
            cls._cache[key] = inst
            return inst
        return cls(dc_class, default, is_nullable, _from_new=_FROM_NEW)

    def __init__(
        self,
        dc_class: type,
        default: "Any | ellipsis",
        is_nullable: bool,
        *,
        _from_new: object = None,
    ) -> None:
        super().__init__()
        if _from_new is not _FROM_NEW:
            raise TypeError("Use DataclassConverter.new() or DataclassConverter.for_class() instead")
        self._dc_class = dc_class
        self._is_nullable = is_nullable

        import typing as _typing_mod

        field_names: tuple[str, ...] = tuple(f.name for f in _dataclasses.fields(dc_class))
        hints = _typing_mod.get_type_hints(dc_class)
        struct_fields = [pa.field(name, rich_to_pyarrow(hints[name], name)) for name in field_names]
        self._pa_struct_type: pa.DataType = pa.struct(struct_fields)
        self._primitive_type = pyarrow_to_primitive(self._pa_struct_type, "")
        self._rich_to_prim: Callable[[Any], Any] = _build_dc_to_dict(dc_class)
        self._prim_to_rich: Callable[[Any], Any] = _build_dict_to_dc(dc_class)
        # Null primitive: a dict with every field set to None — used when a None rich value
        # is received.  GenericFeatureConverter converts None to this form for struct types
        # (None is never "missing" for structs), and we must match that behaviour.
        self._null_prim: dict = {name: None for name in field_names}

        # Columnar PyArrow path: per-field sub-converters used by _to_pyarrow_flat /
        # _from_pyarrow_flat to avoid building intermediate Python dicts per element.
        self._field_names = field_names
        self._struct_fields_list = struct_fields  # list[pa.Field] in field order
        self._sub_dc_converters: Dict[str, "DataclassFeatureConverter"] = {}
        self._field_prim_convs: Dict[str, Callable[[Any], Any]] = {}
        self._field_rich_convs: Dict[str, Callable[[Any], Any]] = {}
        for _fname in field_names:
            _inner_t = unwrap_optional_and_annotated_if_needed(hints[_fname])
            if _dataclasses.is_dataclass(_inner_t) and isinstance(_inner_t, type):
                self._sub_dc_converters[_fname] = DataclassFeatureConverter.for_class(_inner_t)
            else:
                _to_prim = _build_to_primitive_converter(hints[_fname])
                _to_rich = _build_to_rich_converter(hints[_fname])
                if _to_prim is not None:
                    self._field_prim_convs[_fname] = _to_prim
                if _to_rich is not None:
                    self._field_rich_convs[_fname] = _to_rich

        if is_nullable and default is ...:
            default = None
        if default is not ...:
            self._has_default = True
            self._rich_default_val: Any = default
            if default is None:
                self._primitive_default: "dict | None | ellipsis" = None
                self._pyarrow_default: "ellipsis | pa.Array | pa.ChunkedArray" = pa.array(
                    [None], type=self._pa_struct_type
                )
            else:
                prim = self._rich_to_prim(default)
                self._primitive_default = prim
                self._pyarrow_default = pa.array([prim], type=self._pa_struct_type)
        else:
            self._has_default = False
            self._primitive_default = ...
            self._rich_default_val = None
            self._pyarrow_default = ...

    # ── columnar PyArrow helpers ──────────────────────────────────────────────

    def _to_pyarrow_flat(self, instances: list) -> "pa.StructArray":
        """Convert a flat list of dataclass instances → pa.StructArray (columnar).

        *instances* may contain ``None`` entries (e.g. ``None`` list elements or
        ``Optional[SubDC]`` fields set to ``None``).  Following
        :class:`GenericFeatureConverter`, ``None`` is treated as a valid struct
        whose fields are all ``null`` — NOT as a null struct.  This means the
        rich→pyarrow→rich round-trip is intentionally lossy for ``None`` instances:
        ``None`` decodes back as ``DC(None, None, …)``.
        """
        if not instances:
            return pa.array([], type=self._pa_struct_type)
        arrays: list = []
        for pa_field in self._struct_fields_list:
            fname = pa_field.name
            col = [None if inst is None else getattr(inst, "__dict__", inst)[fname] for inst in instances]
            if fname in self._sub_dc_converters:
                arrays.append(self._sub_dc_converters[fname]._to_pyarrow_flat(col))
            elif fname in self._field_prim_convs:
                prim_conv = self._field_prim_convs[fname]
                arrays.append(pa.array([None if x is None else prim_conv(x) for x in col], type=pa_field.type))
            else:
                arrays.append(pa.array(col, type=pa_field.type))
        return pa.StructArray.from_arrays(arrays, fields=self._struct_fields_list)

    def _from_pyarrow_flat(self, struct_arr: "pa.StructArray") -> list:
        """Convert a pa.StructArray → list of dataclass instances (columnar).

        Null struct rows (validity bit False) are returned as ``None``, preserving
        the distinction between a null struct and a struct whose fields are all null.
        """
        n = len(struct_arr)
        if n == 0:
            return []
        valid = struct_arr.is_valid().to_pylist()
        has_nulls = not all(valid)
        field_data: list[list] = []
        for pa_field in self._struct_fields_list:
            fname = pa_field.name
            col = struct_arr.field(fname)
            if fname in self._sub_dc_converters:
                field_data.append(self._sub_dc_converters[fname]._from_pyarrow_flat(col))
            elif fname in self._field_rich_convs:
                rich_conv = self._field_rich_convs[fname]
                field_data.append([rich_conv(x) for x in col.to_pylist()])
            else:
                field_data.append(col.to_pylist())
        dc = self._dc_class
        n_fields = len(field_data)
        if has_nulls:
            return [None if not valid[i] else dc(*[field_data[fi][i] for fi in range(n_fields)]) for i in range(n)]
        return [dc(*row) for row in zip(*field_data)]

    # ── helpers ──────────────────────────────────────────────────────────────

    def _handle_missing(self, value: Any, missing_value_strategy: MissingValueStrategy) -> Any:
        if missing_value_strategy == "allow":
            return value
        if missing_value_strategy in ("default_or_allow", "default_or_error"):
            if self._has_default:
                return self.primitive_default
            if missing_value_strategy == "default_or_error":
                raise TypeError("The value is missing, and this feature has no default value.")
            return value
        if missing_value_strategy == "error":
            raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
        _raise_unsupported_missing_value_strategy(missing_value_strategy)

    # ── properties ───────────────────────────────────────────────────────────

    @property
    def rich_type(self) -> type:
        return self._dc_class

    @property
    def primitive_type(self) -> type:
        return dict

    @property
    def pyarrow_dtype(self) -> pa.DataType:
        return self._pa_struct_type

    @property
    def polars_dtype(self) -> Any:
        return pyarrow_to_polars(self._pa_struct_type)

    @property
    def encoder(self) -> None:
        return None

    @property
    def decoder(self) -> None:
        return None

    @property
    def is_nullable(self) -> bool:
        return self._is_nullable

    @property
    def has_default(self) -> bool:
        return self._has_default

    @property
    def pyarrow_default(self) -> "ellipsis | pa.Array | pa.ChunkedArray":
        return self._pyarrow_default

    @property
    def primitive_default(self) -> "dict | None":
        if self._primitive_default is ...:
            raise ValueError("No default value specified")
        return cast("dict | None", self._primitive_default)

    @property
    def rich_default(self) -> Any:
        if not self._has_default:
            raise ValueError("No default value specified")
        return self._rich_default_val

    def has_nontrivial_rich_type(self) -> bool:
        return True

    # ── missing-value helpers ─────────────────────────────────────────────────

    def is_value_missing(self, value: Any) -> bool:
        if value is ...:
            return True
        # None is never "missing" for struct types — it converts to an all-null struct.
        # This matches GenericFeatureConverter.is_value_missing behaviour.
        return False

    def is_rich_valid(self, value: Any) -> bool:
        try:
            self.from_rich_to_primitive(value, "default_or_error")
            return True
        except (TypeError, ValueError):
            return False

    # ── rich ↔ primitive ─────────────────────────────────────────────────────

    def from_rich_to_primitive(
        self,
        value: "Any | ellipsis | None",
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> "dict | None":
        if value is ...:
            return cast("dict | None", self._handle_missing(value, missing_value_strategy))
        if value is None:
            # None → all-null struct dict, matching GenericFeatureConverter semantics.
            return self._null_prim
        if not isinstance(value, self._dc_class):
            # Coerce non-dataclass inputs (e.g. tuples, dicts) to the rich type first,
            # matching GenericFeatureConverter which calls from_primitive_to_rich before encoding.
            value = structure_primitive_to_rich(value, self._dc_class)
        return self._rich_to_prim(value)

    def from_primitive_to_rich(self, value: "dict | None") -> Any:
        if value is None or value is ...:
            return cast(Any, value)
        return self._prim_to_rich(value)

    # ── primitive ↔ pyarrow ───────────────────────────────────────────────────

    def from_pyarrow_to_primitive(self, values: "pa.Array | pa.ChunkedArray") -> "Sequence[dict | None]":
        return values.to_pylist()

    def from_primitive_to_pyarrow(self, values: "Iterable[dict | None]") -> "pa.Array | pa.ChunkedArray":
        return pa.array(
            [None if v is ... else v for v in values],
            type=self._pa_struct_type,
        )

    def from_pyarrow_to_rich(self, values: "pa.Array | pa.ChunkedArray", /) -> "Sequence[Any]":
        return [self._prim_to_rich(v) for v in values.to_pylist()]

    def from_rich_to_pyarrow(
        self,
        values: "Sequence[Any | ellipsis | None]",
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> "pa.Array | pa.ChunkedArray":
        converted: list = []
        for v in values:
            if v is ...:
                result = self._handle_missing(v, missing_value_strategy)
                converted.append(None if result is ... else cast(Any, result))
            elif v is None:
                # None → all-null struct dict, matching GenericFeatureConverter semantics.
                converted.append(self._null_prim)
            else:
                if not isinstance(v, self._dc_class):
                    v = structure_primitive_to_rich(v, self._dc_class)
                converted.append(self._rich_to_prim(v))
        return pa.array(converted, type=self._pa_struct_type)

    # ── json ↔ * ──────────────────────────────────────────────────────────────

    def from_pyarrow_to_json(
        self,
        values: "pa.Array | pa.ChunkedArray",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> "Sequence[TJSON]":
        return [self.from_primitive_to_json(x, options=options) for x in self.from_pyarrow_to_primitive(values)]

    def from_json_to_pyarrow(self, values: "Sequence[TJSON]") -> "pa.Array | pa.ChunkedArray":
        return self.from_primitive_to_pyarrow([self.from_json_to_primitive(x) for x in values])

    def from_primitive_to_json(
        self,
        value: "dict | None",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        if options.encode_structs_as_objects or is_map_in_dtype_tree(self._pa_struct_type):
            return structs_as_objects_feature_json_converter.unstructure_primitive_to_json(value)
        return unstructure_primitive_to_json(value)

    def from_json_to_primitive(self, value: "TJSON | dict | None") -> "dict | None":
        if value is None:
            return None
        try:
            return cast(dict, structure_json_to_primitive(value, self._primitive_type))
        except (ValueError, TypeError) as e:
            raise TypeError(f"Could not convert '{value}' to `{self._primitive_type}`: {e}") from e

    def from_json_to_rich(self, value: TJSON) -> Any:
        if value is None:
            return None
        prim = self.from_json_to_primitive(value)
        if prim is None:
            return None
        return self._prim_to_rich(prim)

    def from_rich_to_json(
        self,
        value: "Any | ellipsis | None",
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        prim = self.from_rich_to_primitive(value, missing_value_strategy)
        return self.from_primitive_to_json(cast("dict | None", prim), options=options)

    # ── protobuf ↔ * ─────────────────────────────────────────────────────────

    def from_rich_to_protobuf(
        self,
        value: "Any | ellipsis | None",
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = self.from_rich_to_primitive(value, missing_value_strategy)
        return self.from_primitive_to_protobuf(prim)

    def from_primitive_to_protobuf(self, value: "dict | None | pa.Scalar") -> pb.ScalarValue:
        if isinstance(value, pa.Scalar):
            return self.from_pyarrow_to_protobuf(value)
        as_arr = self.from_primitive_to_pyarrow([value])
        return self.from_pyarrow_to_protobuf(as_arr[0])

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=PrimitiveFeatureConverter.convert_pa_dtype_to_proto_dtype(value.type))
        # PrimitiveFeatureConverter handles all scalar types (including nested structs) recursively
        return PrimitiveFeatureConverter("", True, self._pa_struct_type).from_pyarrow_to_protobuf(value)

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=self._pa_struct_type)[0]
        return PrimitiveFeatureConverter("", True, self._pa_struct_type).from_protobuf_to_pyarrow(pb_value)


class ListFeatureConverter(
    _FeatureConverterArrowProtoHelpers,
    FeatureConverter[list, list],
):
    """List-level feature converter parameterized by an item :class:`FeatureConverter`.

    Rich type:      list[T]
    Primitive type: list[primitive(T)]
    PyArrow type:   pa.large_list(item_converter.pyarrow_dtype)

    Use :meth:`new` to obtain a (possibly cached) instance.  For list[dataclass]
    features, pair with :class:`DataclassConverter` as the ``item_converter``.
    """

    _cache: ClassVar[Dict[Tuple[Any, Any, bool], "ListFeatureConverter"]] = {}

    @classmethod
    def new(
        cls,
        item_converter: FeatureConverter,
        default: "list | None | ellipsis",
        is_nullable: bool,
    ) -> "ListFeatureConverter":
        # Cache only for simple defaults since lists are not hashable.
        # item_converter instances are cached themselves (e.g. DataclassConverter.for_class),
        # so using object identity as the key is stable.
        if default is None or default is ...:
            key = (item_converter, default, is_nullable)
            cached = cls._cache.get(key)
            if cached is not None:
                return cached
            inst = cls(item_converter, default, is_nullable)
            cls._cache[key] = inst
            return inst
        return cls(item_converter, default, is_nullable)

    def __init__(
        self,
        item_converter: FeatureConverter,
        default: "list | None | ellipsis",
        is_nullable: bool,
    ) -> None:
        super().__init__()
        self._item = item_converter
        self._is_nullable = is_nullable
        self._pa_list_type: pa.DataType = pa.large_list(item_converter.pyarrow_dtype)
        # Store the element-level closures directly to avoid method-dispatch overhead
        # in _to_primitive / _to_rich.  ListConverter guarantees it only calls these
        # with non-None, non-... values (missing values are handled at the list level).
        if isinstance(item_converter, DataclassFeatureConverter):
            self._elem_to_prim: Callable[[Any], Any] = (
                item_converter._rich_to_prim  # pyright: ignore[reportPrivateUsage]
            )
            self._elem_to_rich: Callable[[Any], Any] = (
                item_converter._prim_to_rich  # pyright: ignore[reportPrivateUsage]
            )
        elif not item_converter.has_nontrivial_rich_type():
            # Primitive types (bool, int, str, …): rich IS primitive — no conversion needed.
            self._elem_to_prim = _identity
            self._elem_to_rich = _identity
        else:
            self._elem_to_prim = item_converter.from_rich_to_primitive
            self._elem_to_rich = item_converter.from_primitive_to_rich
        self._primitive_type = pyarrow_to_primitive(self._pa_list_type, "")

        if is_nullable and default is ...:
            default = None
        if default is not ...:
            self._has_default = True
            self._rich_default_val: "list | None" = cast("list | None", default)
            if default is None:
                self._primitive_default: "list | None | ellipsis" = None
                self._pyarrow_default: "ellipsis | pa.Array | pa.ChunkedArray" = pa.array(
                    [None], type=self._pa_list_type
                )
            else:
                prim = self._to_primitive(default)
                self._primitive_default = prim
                self._pyarrow_default = pa.array([prim], type=self._pa_list_type)
        else:
            self._has_default = False
            self._primitive_default = ...
            self._rich_default_val = None
            self._pyarrow_default = ...

    # ── helpers ──────────────────────────────────────────────────────────────

    def _to_primitive(self, value: list) -> "list[Any]":
        """Convert list[T] → list[primitive] via the element closure."""
        conv = self._elem_to_prim
        return [conv(v) for v in value]

    def _to_rich(self, value: "list[Any]") -> list:
        """Convert list[primitive] → list[T] via the element closure."""
        conv = self._elem_to_rich
        return [conv(d) for d in value]

    def _handle_missing(self, value: Any, missing_value_strategy: MissingValueStrategy) -> Any:
        if missing_value_strategy == "allow":
            return value
        if missing_value_strategy in ("default_or_allow", "default_or_error"):
            if self._has_default:
                return self.primitive_default
            if missing_value_strategy == "default_or_error":
                raise TypeError("The value is missing, and this feature has no default value.")
            return value
        if missing_value_strategy == "error":
            raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
        _raise_unsupported_missing_value_strategy(missing_value_strategy)

    # ── properties ───────────────────────────────────────────────────────────

    @property
    def rich_type(self) -> Type[list]:
        return list

    @property
    def primitive_type(self) -> Type[list]:
        return list

    @property
    def pyarrow_dtype(self) -> pa.DataType:
        return self._pa_list_type

    @property
    def polars_dtype(self) -> Any:
        return pyarrow_to_polars(self._pa_list_type)

    @property
    def encoder(self) -> None:
        return None

    @property
    def decoder(self) -> None:
        return None

    @property
    def is_nullable(self) -> bool:
        return self._is_nullable

    @property
    def has_default(self) -> bool:
        return self._has_default

    @property
    def pyarrow_default(self) -> ellipsis | pa.Array | pa.ChunkedArray:
        return self._pyarrow_default

    @property
    def primitive_default(self) -> list | None:
        if self._primitive_default is ...:
            raise ValueError("No default value specified")
        return cast(list | None, self._primitive_default)

    @property
    def rich_default(self) -> list | None:
        if not self._has_default:
            raise ValueError("No default value specified")
        return self._rich_default_val

    def has_nontrivial_rich_type(self) -> bool:
        # The list type is trivial iff its element type is trivial (e.g. list[int], list[str]).
        return self._item.has_nontrivial_rich_type()

    # ── missing-value helpers ─────────────────────────────────────────────────

    def is_value_missing(self, value: Any) -> bool:
        if value is ...:
            return True
        if value is None:
            return not self._is_nullable
        return False

    def is_rich_valid(self, value: list) -> bool:
        try:
            self.from_rich_to_primitive(value, "default_or_error")
            return True
        except (TypeError, ValueError):
            return False

    # ── rich ↔ primitive ─────────────────────────────────────────────────────

    def from_rich_to_primitive(
        self,
        value: list | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> list | None:
        if value is ... or (value is None and not self._is_nullable):
            return cast(list | None, self._handle_missing(value, missing_value_strategy))
        if value is None:
            return None
        return self._to_primitive(value)

    def from_primitive_to_rich(self, value: list | None) -> list | None:
        if value is None or value is ...:
            return cast(list | None, value)
        return self._to_rich(value)

    # ── primitive ↔ pyarrow ───────────────────────────────────────────────────

    def from_pyarrow_to_primitive(self, values: pa.Array | pa.ChunkedArray) -> Sequence[list | None]:
        return values.to_pylist()

    def from_primitive_to_pyarrow(self, values: Iterable[list | None]) -> pa.Array | pa.ChunkedArray:
        return pa.array(
            [None if v is None or v is ... else v for v in values],
            type=self._pa_list_type,
        )

    def from_pyarrow_to_rich(self, values: pa.Array | pa.ChunkedArray, /) -> Sequence[list | None]:
        if not isinstance(self._item, DataclassFeatureConverter):
            return [None if v is None else self._to_rich(v) for v in values.to_pylist()]
        # Columnar path: avoid materialising N intermediate Python dicts via to_pylist()
        if isinstance(values, pa.ChunkedArray):
            values = values.combine_chunks()
        flat_struct = values.values  # pa.StructArray backing all list elements
        flat_rich = self._item._from_pyarrow_flat(flat_struct)  # pyright: ignore[reportPrivateUsage]
        offsets = values.offsets.to_pylist()
        valid = values.is_valid().to_pylist()
        result: list = []
        for i in range(len(offsets) - 1):
            result.append(flat_rich[offsets[i] : offsets[i + 1]] if valid[i] else None)
        return result

    def from_rich_to_pyarrow(
        self,
        values: Sequence[list | ellipsis | None],
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pa.Array | pa.ChunkedArray:
        if not isinstance(self._item, DataclassFeatureConverter):
            converted: list[list | None] = []
            for v in values:
                if v is ... or (v is None and not self._is_nullable):
                    result = self._handle_missing(v, missing_value_strategy)
                    converted.append(None if result is ... else cast(Any, result))
                elif v is None:
                    converted.append(None)
                else:
                    converted.append(self._to_primitive(v))
            return pa.array(converted, type=self._pa_list_type)

        # Columnar path: build a flat StructArray + offsets instead of N intermediate dicts
        flat_elems: list = []
        offsets: list[int] = [0]
        null_flags: list[bool] = []
        has_nulls = False
        for v in values:
            if v is ... or (v is None and not self._is_nullable):
                res = self._handle_missing(v, missing_value_strategy)
                if res is ... or res is None:
                    null_flags.append(True)
                    offsets.append(offsets[-1])
                    has_nulls = True
                else:
                    # res is a primitive list from a non-None default; convert to rich
                    rich_res = self._to_rich(cast(list, res))
                    null_flags.append(False)
                    flat_elems.extend(rich_res)
                    offsets.append(offsets[-1] + len(rich_res))
            elif v is None:
                null_flags.append(True)
                offsets.append(offsets[-1])
                has_nulls = True
            else:
                null_flags.append(False)
                flat_elems.extend(v)
                offsets.append(offsets[-1] + len(v))
        flat_struct = self._item._to_pyarrow_flat(flat_elems)  # pyright: ignore[reportPrivateUsage]
        offsets_arr = pa.array(offsets, type=pa.int64())
        if has_nulls:
            return pa.LargeListArray.from_arrays(offsets_arr, flat_struct, mask=pa.array(null_flags))
        return pa.LargeListArray.from_arrays(offsets_arr, flat_struct)

    # ── json ↔ * ──────────────────────────────────────────────────────────────

    def from_pyarrow_to_json(
        self,
        values: pa.Array | pa.ChunkedArray,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> Sequence[TJSON]:
        return [self.from_primitive_to_json(x, options=options) for x in self.from_pyarrow_to_primitive(values)]

    def from_json_to_pyarrow(self, values: Sequence[TJSON]) -> pa.Array | pa.ChunkedArray:
        return self.from_primitive_to_pyarrow([self.from_json_to_primitive(x) for x in values])

    def from_primitive_to_json(
        self,
        value: list | None,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        if options.encode_structs_as_objects or is_map_in_dtype_tree(self._pa_list_type):
            return structs_as_objects_feature_json_converter.unstructure_primitive_to_json(value)
        return unstructure_primitive_to_json(value)

    def from_json_to_primitive(self, value: TJSON | list | None) -> list | None:
        if value is None:
            return None
        try:
            return cast(list, structure_json_to_primitive(value, self._primitive_type))
        except (ValueError, TypeError) as e:
            raise TypeError(f"Could not convert '{value}' to `{self._primitive_type}`: {e}") from e

    def from_json_to_rich(self, value: TJSON) -> list | None:
        if value is None:
            return None
        prim = self.from_json_to_primitive(value)
        if prim is None:
            return None
        return self._to_rich(prim)

    def from_rich_to_json(
        self,
        value: list | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        prim = self.from_rich_to_primitive(value, missing_value_strategy)
        return self.from_primitive_to_json(cast(list | None, prim), options=options)

    # ── protobuf ↔ * ─────────────────────────────────────────────────────────

    def from_rich_to_protobuf(
        self,
        value: list | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = self.from_rich_to_primitive(value, missing_value_strategy)
        return self.from_primitive_to_protobuf(prim)

    def from_primitive_to_protobuf(self, value: list | None | pa.Scalar) -> pb.ScalarValue:
        if isinstance(value, pa.Scalar):
            return self.from_pyarrow_to_protobuf(value)
        as_arr = self.from_primitive_to_pyarrow([value])
        return self.from_pyarrow_to_protobuf(as_arr[0])

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=PrimitiveFeatureConverter.convert_pa_dtype_to_proto_dtype(value.type))
        return PrimitiveFeatureConverter._serialize_pa_list_to_pb(value)  # pyright: ignore[reportPrivateUsage]

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=self._pa_list_type)[0]
        return PrimitiveFeatureConverter._deserialize_pb_list_to_pa(pb_value)  # pyright: ignore[reportPrivateUsage]


def make_primitive_converter(
    name: str,
    is_nullable: bool,
    pyarrow_dtype: pa.DataType,
    primitive_default: Any = ...,
) -> FeatureConverter[Any, Any]:
    """Create a primitive-shaped feature converter, using a specialized implementation when possible."""
    return make_feature_converter(
        name=name,
        is_nullable=is_nullable,
        rich_type=...,
        primitive_default=primitive_default,
        pyarrow_dtype=pyarrow_dtype,
    )


def make_feature_converter(
    name: str | None,
    is_nullable: bool,
    rich_type: Type[Any] | ellipsis = ...,
    primitive_default: Any = ...,
    rich_default: Any = ...,
    pyarrow_dtype: pa.DataType | None = None,
    encoder: TEncoder[Any, Any] | None = None,
    decoder: TDecoder[Any, Any] | None = None,
) -> FeatureConverter[Any, Any]:
    """Create a feature converter, using a specialized implementation when possible."""
    rich_type = unwrap_annotated_if_needed(rich_type)

    if pyarrow_dtype is None:
        if rich_type is ...:
            raise ValueError("Either the `rich_type` or `pyarrow_dtype` must be provided")
        pyarrow_dtype = rich_to_pyarrow(rich_type, "" if name is None else name)

    specialized_default = primitive_default
    if rich_type is ...:
        if rich_default != ...:
            raise ValueError(
                "The `rich_default` cannot be used without the `rich_type`. Perhaps specify the `primitive_default` instead?"
            )
        if is_nullable and primitive_default is ...:
            specialized_default = None
    else:
        if primitive_default != ...:
            raise ValueError(
                "The `primitive_default` cannot be used when specifying the `rich_type`. Instead, specify the `rich_default`."
            )
        if is_nullable and rich_default is ...:
            rich_default = None
        if isinstance(rich_default, UnresolvedFeature):
            rich_default = ...
        specialized_default = rich_default

    rich_primitive_type = ... if rich_type is ... else unwrap_optional_and_annotated_if_needed(rich_type)
    if encoder is None and decoder is None:
        # if pa.types.is_boolean(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is bool):
        #     return BoolFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        # if pa.types.is_int64(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is int):
        #     return Int64FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        # if pa.types.is_int32(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is int):
        #     return Int32FeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        # if pa.types.is_string(pyarrow_dtype) and (rich_type is ... or rich_primitive_type is str):
        #     return StringFeatureConverter.new(default=specialized_default, is_nullable=is_nullable)
        if (
            pa.types.is_struct(pyarrow_dtype)
            and isinstance(rich_primitive_type, type)
            and _dataclasses.is_dataclass(rich_primitive_type)
        ):
            return DataclassFeatureConverter.new(rich_primitive_type, specialized_default, is_nullable)
        if (
            (pyarrow_dtype is not None and (pa.types.is_list(pyarrow_dtype) or pa.types.is_large_list(pyarrow_dtype)))
            and rich_primitive_type is not ...
            and get_origin(rich_primitive_type) in (list, List)
        ):
            inner_args = get_args(rich_primitive_type)
            if inner_args:
                inner_type = unwrap_optional_and_annotated_if_needed(inner_args[0])
                # Temporary: only use ListFeatureConverter for list[dataclass]. This will be
                # generalized to other inner types (e.g. list[str], list[int]) in the near future.
                if isinstance(inner_type, type) and _dataclasses.is_dataclass(inner_type):
                    item_conv = make_feature_converter(
                        name=None,
                        is_nullable=True,
                        rich_type=inner_args[0],
                        pyarrow_dtype=pyarrow_dtype.value_type,
                    )
                    return ListFeatureConverter.new(
                        item_converter=item_conv,
                        default=specialized_default,
                        is_nullable=is_nullable,
                    )

    return GenericFeatureConverter(
        name="" if name is None else name,
        is_nullable=is_nullable,
        rich_type=rich_type,
        primitive_default=primitive_default,
        rich_default=rich_default,
        pyarrow_dtype=pyarrow_dtype,
        encoder=encoder,
        decoder=decoder,
    )


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


class PrimitiveFeatureConverter(FeatureConverter[_TPrim, _TRich], Generic[_TPrim, _TRich]):
    """Feature converter that can only deal with primitive types. This means it can be constructed from a serialized graph,
    but it cannot convert to/from rich types"""

    @overload
    def __init__(
        self,
        name: str,
        is_nullable: bool,
        pyarrow_dtype: pa.DataType,
        primitive_default: ellipsis = ...,
    ) -> None: ...

    @overload
    def __init__(
        self,
        name: str,
        is_nullable: bool,
        pyarrow_dtype: pa.DataType,
        primitive_default: _TPrim,
    ) -> None: ...

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
            self._polars_dtype = pyarrow_to_polars(self.pyarrow_dtype, self._name)

    __slots__ = ("_name", "_pyarrow_dtype", "_is_nullable", "_primitive_type", "_polars_dtype", "_pyarrow_default")

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
            self._polars_dtype = pyarrow_to_polars(self.pyarrow_dtype, self._name)

    @property
    def polars_dtype(self) -> Any:
        return self._polars_dtype

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

    @property
    def rich_type(self) -> Type[_TRich]:
        t = cast(Type[_TRich], self._primitive_type)
        if self._is_nullable:
            from typing import Optional as _Optional

            return _Optional[t]  # type: ignore[return-value]
        return t

    @property
    def rich_default(self) -> _TRich:
        return cast(_TRich, self.primitive_default)

    @property
    def encoder(self) -> Optional[TEncoder[_TPrim, _TRich]]:
        return None

    @property
    def decoder(self) -> Optional[TDecoder[_TPrim, _TRich]]:
        return None

    def is_value_missing(self, value: Any) -> bool:
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

    def is_rich_valid(self, value: _TRich) -> bool:
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
                    f"The value for feature '{self._name}' is missing, but `replace_missing_with_defaults` was set to `False`."
                )
            else:
                raise ValueError(
                    (
                        f"Unsupported missing value strategy: {missing_value_strategy}. "
                        "It must be one of 'allow', 'default_or_allow', 'default_or_error', or 'error'."
                    )
                )
        return cast(_TPrim, value)

    def from_rich_to_json(
        self,
        value: Union[_TRich, ellipsis, None],
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        prim_val = self.from_rich_to_primitive(value, missing_value_strategy)
        return self.from_primitive_to_json(prim_val, options=options)

    def from_pyarrow_to_rich(self, values: Union[pa.Array, pa.ChunkedArray], /) -> Sequence[_TRich]:
        return cast(Sequence[_TRich], self.from_pyarrow_to_primitive(values))

    def from_primitive_to_rich(self, value: Union[_TPrim, _TRich]) -> _TRich:
        return cast(_TRich, value)

    def from_json_to_rich(self, value: TJSON) -> _TRich:
        return cast(_TRich, self.from_json_to_primitive(value))

    def has_nontrivial_rich_type(self) -> bool:
        return False

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("extension_value"):
            storage_val = self.from_protobuf_to_pyarrow(pb_value.extension_value.storage_value)
            logical_type = type(self).convert_proto_dtype_to_pa_dtype(
                pb.ArrowType(extension=pb_value.extension_value.extension_type)
            )
            return pa.ExtensionScalar.from_storage(logical_type, storage_val)
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=type(self).convert_proto_dtype_to_pa_dtype(pb_value.null_value))[0]
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
                field.name: self.from_protobuf_to_pyarrow(field_value)
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
            return type(self)._deserialize_pb_list_to_pa(pb_value)
        if pb_value.HasField("duration_second_value"):
            return pa.scalar(timedelta(seconds=pb_value.duration_second_value), pa.duration("s"))
        if pb_value.HasField("duration_millisecond_value"):
            return pa.scalar(timedelta(milliseconds=pb_value.duration_millisecond_value), pa.duration("ms"))
        if pb_value.HasField("duration_microsecond_value"):
            return pa.scalar(timedelta(microseconds=pb_value.duration_microsecond_value), pa.duration("us"))
        if pb_value.HasField("duration_nanosecond_value"):
            return pa.scalar(timedelta(microseconds=pb_value.duration_nanosecond_value / 1000), pa.duration("ns"))
        if pb_value.HasField("decimal128_value"):
            return type(self)._deserialize_pb_to_pa_decimal(pb_value)
        if pb_value.HasField("decimal256_value"):
            return type(self)._deserialize_pb_to_pa_decimal(pb_value)
        raise ValueError(f"Unsupported Protobuf type: {pb_value}")

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=type(self).convert_pa_dtype_to_proto_dtype(value.type))
        if pa.types.is_null(value.type):
            return pb.ScalarValue(null_value=type(self).convert_pa_dtype_to_proto_dtype(value.type))
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
                pb_scalar = self.from_pyarrow_to_protobuf(pa_scalar)
                fields.append(
                    pb.Field(
                        name=name,
                        arrow_type=type(self).convert_pa_dtype_to_proto_dtype(pa_scalar.type),
                        nullable=True,
                    )
                )
                field_values.append(pb_scalar)
            return pb.ScalarValue(struct_value=pb.StructValue(fields=fields, field_values=field_values))
        if isinstance(value, pa.MapScalar):
            return type(self)._serialize_pa_list_to_pb(value)
        if isinstance(value, pa.ListScalar):
            return type(self)._serialize_pa_list_to_pb(value)
        if isinstance(value, pa.Decimal128Scalar):
            return type(self)._serialize_pa_decimal_to_pb(value)
        if isinstance(value, pa.Decimal256Scalar):
            return type(self)._serialize_pa_decimal_to_pb(value)

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

    @classmethod
    def convert_pa_field_to_proto_field(cls, field: pa.Field) -> pb.Field:
        """Convert a PyArrow Field to proto Field."""
        field_proto = pb.Field(
            name=field.name, arrow_type=cls.convert_pa_dtype_to_proto_dtype(field.type), nullable=field.nullable
        )

        if field.metadata:
            # field.metadata is of types dict[bytes, bytes]
            for k, v in field.metadata.items():
                field_proto.metadata[k.decode("utf-8")] = v.decode("utf-8")

        return field_proto

    @classmethod
    def convert_proto_field_to_pa_field(cls, proto_field: pb.Field) -> pa.Field:
        """Convert a proto Field to PyArrow Field."""
        arrow_type = cls.convert_proto_dtype_to_pa_dtype(proto_field.arrow_type)

        # don't have to convert back to dict[bytes, bytes] as can initialize with dict[str, str]
        metadata = dict(proto_field.metadata) if proto_field.metadata else None

        return pa.field(
            name=proto_field.name,
            type=arrow_type,
            nullable=proto_field.nullable,
            metadata=metadata,
        )

    @classmethod
    def convert_pa_schema_to_proto_schema(cls, schema: pa.Schema) -> pb.Schema:
        schema_proto = pb.Schema(
            columns=[cls.convert_pa_field_to_proto_field(field) for field in schema],
        )

        if schema.metadata:
            # schema.metadata is of types dict[bytes, bytes]
            for k, v in schema.metadata.items():
                schema_proto.metadata[k.decode("utf-8")] = v.decode("utf-8")

        return schema_proto

    @classmethod
    def convert_proto_schema_to_pa_schema(cls, proto_schema: pb.Schema) -> pa.Schema:
        fields = [cls.convert_proto_field_to_pa_field(proto_field) for proto_field in proto_schema.columns]

        # don't have to convert back to dict[bytes, bytes] as can initialize with dict[str, str]
        metadata = dict(proto_schema.metadata) if proto_schema.metadata else None

        return pa.schema(fields, metadata=metadata)

    @staticmethod
    def convert_arrow_table_to_proto(table: pa.Table | pa.RecordBatch) -> pb.TableParquetBytes:
        if isinstance(table, pa.RecordBatch):
            table = pa.Table.from_batches([table])
        elif isinstance(table, pa.Table):
            pass
        else:
            raise TypeError(f"expected pa.Table or pa.RecordBatch, got {type(table)!r}")

        sink = io.BytesIO()
        import pyarrow.parquet

        pyarrow.parquet.write_table(table, sink)
        return pb.TableParquetBytes(encoded_parquet_bytes=sink.getvalue())

    @staticmethod
    def convert_arrow_table_from_proto(proto: pb.TableParquetBytes) -> pa.Table:
        import pyarrow.parquet as pq

        return pq.read_table(io.BytesIO(proto.encoded_parquet_bytes))

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
    def __call__(self, value: _TRichCon, /) -> _TPrimCo: ...


class TDecoder(Protocol[_TPrimCon, _TRichCo]):
    def __call__(self, value: _TPrimCon, /) -> _TRichCo: ...


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


class GenericFeatureConverter(PrimitiveFeatureConverter[_TPrim, _TRich], Generic[_TPrim, _TRich]):
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
            # In notebook environments, UnresolvedFeature may be used as a placeholder
            # for features that can't be resolved due to a stale registry.
            # Treat these as missing defaults since they're not concrete values.
            if isinstance(rich_default, UnresolvedFeature):
                rich_default = ...
            else:
                # The missing value strategy doesn't really matter because rich_default is not missing
                primitive_default = self.from_rich_to_primitive(rich_default, missing_value_strategy="allow")
        super().__init__(
            name, is_nullable=is_nullable, pyarrow_dtype=pyarrow_dtype, primitive_default=primitive_default
        )

    @property
    def rich_type(self) -> Type[_TRich]:
        if self._rich_type is ...:
            raise ValueError(
                "Rich types cannot be used as the GenericFeatureConverter was created without providing a `rich_type`"
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
                    f"The value for feature '{self._name}' is missing, but `replace_missing_with_defaults` was set to `False`."
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
                "Rich types cannot be used as the GenericFeatureConverter was created without providing a `rich_type`"
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
            prim_canonical = Optional[prim_canonical]
        return prim_canonical != rich_canonical
