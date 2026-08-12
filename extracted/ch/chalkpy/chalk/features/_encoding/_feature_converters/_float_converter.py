from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Iterable,
    Type,
    Union,
    cast,
)

import pyarrow as pa

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.missing_value import MissingValueStrategy

from ._base import (
    _ScalarConverterBase,
    _raise_unsupported_missing_value_strategy,
    _unwrap_scalar_value,
    FeatureConverter,
    MissingValueError,
)

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false

try:
    import numpy as np
except ImportError:
    np = None  # type: ignore[assignment]

# Sentinel NaN used by Float16FeatureConverter to represent missing values,
# matching GenericFeatureConverter's convention of using NaN (not null) for float16.
_F16_NAN: Any = np.float16("nan") if np is not None else float("nan")  # type: ignore[union-attr]


class Float16FeatureConverter(
    _ScalarConverterBase[float, float],
    FeatureConverter[float, float],
):
    """Converter for pa.float16().

    Float16 has two important quirks vs other float widths:

    1. PyArrow requires np.float16 objects for bulk array construction —
       passing Python floats raises ArrowTypeError.

    2. GenericFeatureConverter uses NaN (not proper null) to represent missing
       values in float16 arrays, because numpy float16 uses NaN as its null
       sentinel in masked arrays.  We match that convention so the two
       converters are drop-in compatible.
    """

    _rich_type_value: ClassVar[Type[float]] = float
    _primitive_type_value: ClassVar[Type[float]] = float
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.float16()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(float16=pb.EmptyMessage())
    _polars_dtype_value: ClassVar[Any] = None

    _coerce_fn = staticmethod(float)
    # pa.array([Python float], type=pa.float16()) raises ArrowTypeError.
    _arrow_coerce_fn: ClassVar = np.float16 if np is not None else float  # type: ignore[union-attr]
    _json_coerce_fn: ClassVar = np.float16 if np is not None else float  # type: ignore[union-attr]

    @property
    def polars_dtype(self) -> Any:
        """Return Float16 when supported, otherwise preserve the Float32 fallback."""
        val = type(self)._polars_dtype_value
        if val is None:
            try:
                import polars as pl

                val = getattr(pl, "Float16", pl.Float32)()
                type(self)._polars_dtype_value = val
            except ImportError:
                pass
        return val

    @classmethod
    def new(cls, default: Any, is_nullable: bool) -> "Float16FeatureConverter":
        # Match GenericFeatureConverter: use NaN (not None) as the null sentinel for float16
        # when no explicit default is given for a nullable feature.
        if is_nullable and default is ...:
            default = _F16_NAN
        return super().new(default=default, is_nullable=is_nullable)  # type: ignore[return-value]

    def __init__(self, default: Any, is_nullable: bool, *, pa_type: "pa.DataType | None" = None, _from_new: object = None) -> None:
        # Track what rich_default should expose (None when the user provided None or no default).
        # GenericFeatureConverter stores None as rich_default but NaN as primitive_default for float16.
        if default is _F16_NAN or default is None:
            self._f16_rich_default: Any = None
        else:
            self._f16_rich_default = ...  # sentinel: delegate to primitive_default

        # Coerce None → _F16_NAN so that primitive_default = nan (not None) matching GenericFeatureConverter.
        if default is None:
            default = _F16_NAN

        super().__init__(default, is_nullable, pa_type=pa_type, _from_new=_from_new)

    @property
    def rich_default(self) -> float:  # type: ignore[override]
        if self._f16_rich_default is not ...:
            return self._f16_rich_default  # type: ignore[return-value]
        return self.primitive_default  # type: ignore[return-value]

    def from_primitive_to_rich(self, value: float | None) -> float:
        if value is None or value is ...:
            return cast(float, value)
        return float(cast(Any, value))

    def is_rich_valid(self, value: Any) -> bool:
        # Override to coerce via np.float16 directly, avoiding pa.scalar(plain_float, pa.float16())
        # which raises ArrowTypeError on some PyArrow versions.
        if self.is_value_missing(value):
            return self._is_nullable
        try:
            np.float16(value)  # type: ignore[union-attr]
            return True
        except (TypeError, ValueError, OverflowError):
            return False

    def from_primitive_to_protobuf(self, value: float | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        # Float16 convention: None and ... both map to NaN (not null_value), matching GenericFeatureConverter.
        f16 = np.float16(scalar_value) if (scalar_value is not None and scalar_value is not ...) else _F16_NAN  # type: ignore[union-attr]
        return self.from_pyarrow_to_protobuf(pa.scalar(f16, type=pa.float16()))

    def from_rich_to_protobuf(
        self,
        value: "float | ellipsis | None",
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(float | None, self.from_rich_to_primitive(value, missing_value_strategy))
        # Float16 convention: None and ... both map to NaN, matching GenericFeatureConverter.
        f16 = np.float16(prim) if (prim is not None and prim is not ...) else _F16_NAN  # type: ignore[union-attr]
        return self.from_pyarrow_to_protobuf(pa.scalar(f16, type=pa.float16()))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=pb.ArrowType(float16=pb.EmptyMessage()))
        return pb.ScalarValue(float16_value=value.as_py())

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.float16())[0]
        return pa.scalar(np.float16(pb_value.float16_value), pa.float16())  # type: ignore[union-attr]

    def from_primitive_to_pyarrow(self, value: Iterable[Any]) -> "Union[pa.Array, pa.ChunkedArray]":
        # Converts None → _F16_NAN to match GenericFeatureConverter's NaN convention.
        return pa.array(
            [_F16_NAN if v is None else np.float16(v) for v in value],  # type: ignore[union-attr]
            type=pa.float16(),
        )

    def from_rich_to_pyarrow(
        self,
        values: Iterable[Any],
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        feature_name: "str | None" = None,
    ) -> "Union[pa.Array, pa.ChunkedArray]":
        # Re-implement to use _F16_NAN instead of None for all missing values.
        _coerce = self._arrow_coerce  # np.float16
        has_default = self._has_default
        is_nullable = self._is_nullable
        prim_default = self._primitive_default  # np.float16 value or _F16_NAN

        def _def_f16() -> Any:
            return np.float16(prim_default) if prim_default is not None else _F16_NAN  # type: ignore[union-attr]

        if missing_value_strategy == "allow":
            return pa.array(
                [_F16_NAN if x is ... else (_F16_NAN if x is None else _coerce(x)) for x in values],
                type=pa.float16(),
            )
        if missing_value_strategy == "default_or_allow":
            if not has_default:
                return pa.array(
                    [_F16_NAN if x is ... else (_F16_NAN if x is None else _coerce(x)) for x in values],
                    type=pa.float16(),
                )
            _def = _def_f16()
            if is_nullable:
                return pa.array(
                    [_def if x is ... else (_F16_NAN if x is None else _coerce(x)) for x in values],
                    type=pa.float16(),
                )
            return pa.array(
                [_def if x is ... else (_def if x is None else _coerce(x)) for x in values],
                type=pa.float16(),
            )
        if missing_value_strategy == "default_or_error":
            if has_default:
                _def = _def_f16()
                if is_nullable:
                    return pa.array(
                        [_def if x is ... else (_F16_NAN if x is None else _coerce(x)) for x in values],
                        type=pa.float16(),
                    )
                return pa.array(
                    [_def if x is ... else (_def if x is None else _coerce(x)) for x in values],
                    type=pa.float16(),
                )
            pa_values: list[Any] = []
            for x in values:
                if x is ... or (x is None and not is_nullable):
                    raise MissingValueError("The value is missing, and this feature has no default value.")
                pa_values.append(_F16_NAN if x is None else _coerce(x))
            return pa.array(pa_values, type=pa.float16())
        if missing_value_strategy == "error":
            pa_values = []
            for x in values:
                if x is ... or (x is None and not is_nullable):
                    raise MissingValueError(
                        "The value is missing, but `replace_missing_with_defaults` was set to `False`."
                    )
                pa_values.append(_F16_NAN if x is None else _coerce(x))
            return pa.array(pa_values, type=pa.float16())
        _raise_unsupported_missing_value_strategy(missing_value_strategy)


class Float32FeatureConverter(
    _ScalarConverterBase[float, float],
    FeatureConverter[float, float],
):
    _rich_type_value: ClassVar[Type[float]] = float
    _primitive_type_value: ClassVar[Type[float]] = float
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.float32()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(float32=pb.EmptyMessage())
    _polars_dtype_value: ClassVar[Any] = None

    _coerce_fn = staticmethod(float)

    def from_primitive_to_rich(self, value: float | None) -> float:
        if value is None or value is ...:
            return cast(float, value)
        return float(cast(Any, value))

    def from_primitive_to_protobuf(self, value: float | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(float32=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(float, scalar_value), type=pa.float32()))

    def from_rich_to_protobuf(
        self,
        value: float | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(float | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(float32=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.float32()))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=pb.ArrowType(float32=pb.EmptyMessage()))
        return pb.ScalarValue(float32_value=value.as_py())

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.float32())[0]
        return pa.scalar(pb_value.float32_value, pa.float32())


class Float64FeatureConverter(
    _ScalarConverterBase[float, float],
    FeatureConverter[float, float],
):
    _rich_type_value: ClassVar[Type[float]] = float
    _primitive_type_value: ClassVar[Type[float]] = float
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.float64()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(float64=pb.EmptyMessage())
    _polars_dtype_value: ClassVar[Any] = None

    _coerce_fn = staticmethod(float)

    def from_primitive_to_rich(self, value: float | None) -> float:
        if value is None or value is ...:
            return cast(float, value)
        return float(cast(Any, value))

    def from_primitive_to_protobuf(self, value: float | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(float64=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(float, scalar_value), type=pa.float64()))

    def from_rich_to_protobuf(
        self,
        value: float | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(float | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(float64=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.float64()))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=pb.ArrowType(float64=pb.EmptyMessage()))
        return pb.ScalarValue(float64_value=value.as_py())

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.float64())[0]
        return pa.scalar(pb_value.float64_value, pa.float64())
