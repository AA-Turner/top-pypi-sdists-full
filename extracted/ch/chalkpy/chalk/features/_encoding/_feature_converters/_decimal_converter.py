from __future__ import annotations

from decimal import Decimal
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

from ._base import (
    _ScalarConverterBase,
    _unwrap_scalar_value,
    FeatureConverter,
)

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false


def _coerce_decimal(x: Any) -> str:
    """Convert x to the normalized string form of its Decimal value.

    Uses Decimal.normalize() to match the cattrs unstructure hook registered
    in rich.py: ``lambda x: str(x.normalize())``.  This strips trailing zeros
    (e.g. Decimal("1.000") → "1") and keeps sign, scientific notation, NaN,
    and Infinity unchanged.
    """
    if isinstance(x, Decimal):
        return str(x.normalize())
    return str(Decimal(x).normalize())


class DecimalFeatureConverter(
    _ScalarConverterBase[str, Decimal],
    FeatureConverter[str, Decimal],
):
    """Specialized converter for decimal.Decimal features.

    Chalk stores Decimal as pa.large_utf8() (a string).  The primitive type
    is therefore ``str``; rich values are ``decimal.Decimal`` instances.

    There is a single converter regardless of precision/scale — the
    pa.decimal128/decimal256 PyArrow types are a distinct, unrelated path.
    """

    _rich_type_value: ClassVar[Type[Decimal]] = Decimal
    _primitive_type_value: ClassVar[Type[str]] = str
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.large_utf8()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(large_utf8=pb.EmptyMessage())
    _polars_dtype_value: ClassVar[Any] = None

    _coerce_fn = staticmethod(_coerce_decimal)
    _use_fast_path: ClassVar[bool] = False  # fast path skips _coerce_fn; Decimal needs normalization

    # ── rich_default must return Decimal, not the str primitive ───────────────

    @property
    def rich_default(self) -> Decimal:
        prim = self._primitive_default
        if prim is ...:
            raise ValueError("No default value specified")
        if prim is None:
            return cast(Decimal, None)
        return Decimal(cast(str, prim))

    # ── rich ↔ primitive ──────────────────────────────────────────────────────

    def has_nontrivial_rich_type(self) -> bool:
        return True

    def from_primitive_to_rich(self, value: str | None) -> Decimal:
        if value is None or value is ...:
            return cast(Decimal, value)
        return Decimal(str(value))

    def from_pyarrow_to_rich(self, values: Union[pa.Array, pa.ChunkedArray], /) -> Sequence[Decimal]:
        return [None if s is None else Decimal(s) for s in values.to_pylist()]  # type: ignore[misc]

    def from_json_to_rich(self, value: Any) -> Decimal:
        prim = self.from_json_to_primitive(value)
        return self.from_primitive_to_rich(prim)

    # ── protobuf ──────────────────────────────────────────────────────────────

    def from_primitive_to_protobuf(self, value: str | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(large_utf8=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(str, scalar_value), type=pa.large_utf8()))

    def from_rich_to_protobuf(
        self,
        value: Decimal | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast("str | None", self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(large_utf8=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.large_utf8()))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=pb.ArrowType(large_utf8=pb.EmptyMessage()))
        return pb.ScalarValue(large_utf8_value=value.as_py())

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.large_utf8())[0]
        return pa.scalar(pb_value.large_utf8_value, pa.large_utf8())
