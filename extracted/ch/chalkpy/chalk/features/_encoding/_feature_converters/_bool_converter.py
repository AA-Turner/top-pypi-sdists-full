from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Sequence,
    Type,
    Union,
    cast,
)

import pyarrow as pa

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.primitive import TPrimitive
from chalk.features._encoding.rich import structure_primitive_to_rich
from chalk.utils.json import TJSON

from ._base import (
    _ScalarConverterBase,
    _unwrap_scalar_value,
    FeatureConverter,
)
from ._primitive_converter import _FeatureConverterArrowProtoHelpers

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false

try:
    import polars as pl
except ImportError:
    pl = None


def _coerce_bool(x: Any) -> bool:
    if type(x) is bool:
        return x
    return structure_primitive_to_rich(x, bool)


class BoolFeatureConverter(
    _ScalarConverterBase[bool, bool],
    _FeatureConverterArrowProtoHelpers,
    FeatureConverter[bool, bool],
):
    _rich_type_value: ClassVar[Type[bool]] = bool
    _primitive_type_value: ClassVar[Type[bool]] = bool
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.bool_()
    _polars_dtype_value: ClassVar[Any] = pl.Boolean() if pl is not None else None

    _coerce_fn = staticmethod(_coerce_bool)

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

    def from_primitive_to_protobuf(self, value: bool | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(bool=pb.EmptyMessage()))
        return pb.ScalarValue(bool_value=cast(bool, scalar_value))

    def from_rich_to_protobuf(
        self,
        value: bool | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(bool | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(bool=pb.EmptyMessage()))
        return pb.ScalarValue(bool_value=prim)

    def from_primitive_to_rich(self, value: bool) -> bool:
        return structure_primitive_to_rich(value, bool)

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
