from __future__ import annotations

import uuid as _uuid_module
from ipaddress import IPv4Address, IPv6Address
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

# ── Coerce functions ───────────────────────────────────────────────────────────

def _coerce_uuid(x: Any) -> str:
    """Convert x to the canonical lowercase-hyphenated UUID string.

    - uuid.UUID inputs are stringified directly.
    - str inputs are normalised through uuid.UUID() (handles uppercase, compact
      form without hyphens, etc.).
    """
    if isinstance(x, _uuid_module.UUID):
        return str(x)
    return str(_uuid_module.UUID(x))


def _coerce_ipv4(x: Any) -> int:
    """Convert x to the packed uint32 integer form of an IPv4 address.

    Accepts IPv4Address, dotted-string, or integer inputs.
    """
    return int(IPv4Address(x))


def _coerce_ipv6(x: Any) -> str:
    """Convert x to the normalised short-form IPv6 string.

    - IPv6Address inputs are stringified directly.
    - str and int inputs are normalised through IPv6Address().
    """
    if isinstance(x, IPv6Address):
        return str(x)
    return str(IPv6Address(x))


# ══════════════════════════════════════════════════════════════════════════════
# UUID
# ══════════════════════════════════════════════════════════════════════════════

class UUIDFeatureConverter(
    _ScalarConverterBase[str, _uuid_module.UUID],
    FeatureConverter[str, _uuid_module.UUID],
):
    """Specialized converter for uuid.UUID features.

    Stored as pa.large_utf8(). Primitive type is str; rich type is uuid.UUID.
    """

    _rich_type_value: ClassVar[Type[_uuid_module.UUID]] = _uuid_module.UUID
    _primitive_type_value: ClassVar[Type[str]] = str
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.large_utf8()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(large_utf8=pb.EmptyMessage())
    _polars_dtype_value: ClassVar[Any] = None

    _coerce_fn = staticmethod(_coerce_uuid)

    @property
    def rich_default(self) -> _uuid_module.UUID:
        prim = self._primitive_default
        if prim is ...:
            raise ValueError("No default value specified")
        if prim is None:
            return cast(_uuid_module.UUID, None)
        return _uuid_module.UUID(cast(str, prim))

    def has_nontrivial_rich_type(self) -> bool:
        return True

    def from_primitive_to_rich(self, value: str | None) -> _uuid_module.UUID:
        if value is None or value is ...:
            return cast(_uuid_module.UUID, value)
        return _uuid_module.UUID(str(value))

    def from_pyarrow_to_rich(self, values: Union[pa.Array, pa.ChunkedArray], /) -> Sequence[_uuid_module.UUID]:
        return [None if s is None else _uuid_module.UUID(s) for s in values.to_pylist()]  # type: ignore[misc]

    def from_json_to_rich(self, value: Any) -> _uuid_module.UUID:
        return self.from_primitive_to_rich(self.from_json_to_primitive(value))

    def from_primitive_to_protobuf(self, value: str | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(large_utf8=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(str, scalar_value), type=pa.large_utf8()))

    def from_rich_to_protobuf(
        self,
        value: _uuid_module.UUID | ellipsis | None,
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


# ══════════════════════════════════════════════════════════════════════════════
# IPv4
# ══════════════════════════════════════════════════════════════════════════════

_IPV4_PROTO_ARROW_TYPE = pb.ArrowType(uint32=pb.EmptyMessage())


class IPv4FeatureConverter(
    _ScalarConverterBase[int, IPv4Address],
    FeatureConverter[int, IPv4Address],
):
    """Specialized converter for ipaddress.IPv4Address features.

    Stored as pa.uint32() (packed integer). Primitive type is int; rich type
    is IPv4Address.
    """

    _rich_type_value: ClassVar[Type[IPv4Address]] = IPv4Address
    _primitive_type_value: ClassVar[Type[int]] = int
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.uint32()
    _proto_arrow_type: ClassVar[pb.ArrowType] = _IPV4_PROTO_ARROW_TYPE
    _polars_dtype_value: ClassVar[Any] = None

    _coerce_fn = staticmethod(_coerce_ipv4)

    @property
    def rich_default(self) -> IPv4Address:
        prim = self._primitive_default
        if prim is ...:
            raise ValueError("No default value specified")
        if prim is None:
            return cast(IPv4Address, None)
        return IPv4Address(cast(int, prim))

    def has_nontrivial_rich_type(self) -> bool:
        return True

    def from_primitive_to_rich(self, value: int | None) -> IPv4Address:
        if value is None or value is ...:
            return cast(IPv4Address, value)
        return IPv4Address(int(cast(Any, value)))

    def from_pyarrow_to_rich(self, values: Union[pa.Array, pa.ChunkedArray], /) -> Sequence[IPv4Address]:
        return [None if v is None else IPv4Address(v) for v in values.to_pylist()]  # type: ignore[misc]

    def from_json_to_rich(self, value: Any) -> IPv4Address:
        return self.from_primitive_to_rich(self.from_json_to_primitive(value))

    def from_primitive_to_protobuf(self, value: int | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=_IPV4_PROTO_ARROW_TYPE)
        return self.from_pyarrow_to_protobuf(pa.scalar(int(scalar_value), type=pa.uint32()))

    def from_rich_to_protobuf(
        self,
        value: IPv4Address | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast("int | None", self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return pb.ScalarValue(null_value=_IPV4_PROTO_ARROW_TYPE)
        return self.from_pyarrow_to_protobuf(pa.scalar(prim, type=pa.uint32()))

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        if value.as_py() is None:
            return pb.ScalarValue(null_value=_IPV4_PROTO_ARROW_TYPE)
        return pb.ScalarValue(uint32_value=value.as_py())

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=pa.uint32())[0]
        return pa.scalar(pb_value.uint32_value, pa.uint32())


# ══════════════════════════════════════════════════════════════════════════════
# IPv6
# ══════════════════════════════════════════════════════════════════════════════

class IPv6FeatureConverter(
    _ScalarConverterBase[str, IPv6Address],
    FeatureConverter[str, IPv6Address],
):
    """Specialized converter for ipaddress.IPv6Address features.

    Stored as pa.large_utf8(). Primitive type is str; rich type is IPv6Address.
    """

    _rich_type_value: ClassVar[Type[IPv6Address]] = IPv6Address
    _primitive_type_value: ClassVar[Type[str]] = str
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pa.large_utf8()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(large_utf8=pb.EmptyMessage())
    _polars_dtype_value: ClassVar[Any] = None

    _coerce_fn = staticmethod(_coerce_ipv6)

    @property
    def rich_default(self) -> IPv6Address:
        prim = self._primitive_default
        if prim is ...:
            raise ValueError("No default value specified")
        if prim is None:
            return cast(IPv6Address, None)
        return IPv6Address(cast(str, prim))

    def has_nontrivial_rich_type(self) -> bool:
        return True

    def from_primitive_to_rich(self, value: str | None) -> IPv6Address:
        if value is None or value is ...:
            return cast(IPv6Address, value)
        return IPv6Address(str(value))

    def from_pyarrow_to_rich(self, values: Union[pa.Array, pa.ChunkedArray], /) -> Sequence[IPv6Address]:
        return [None if s is None else IPv6Address(s) for s in values.to_pylist()]  # type: ignore[misc]

    def from_json_to_rich(self, value: Any) -> IPv6Address:
        return self.from_primitive_to_rich(self.from_json_to_primitive(value))

    def from_primitive_to_protobuf(self, value: str | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return pb.ScalarValue(null_value=pb.ArrowType(large_utf8=pb.EmptyMessage()))
        return self.from_pyarrow_to_protobuf(pa.scalar(cast(str, scalar_value), type=pa.large_utf8()))

    def from_rich_to_protobuf(
        self,
        value: IPv6Address | ellipsis | None,
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
