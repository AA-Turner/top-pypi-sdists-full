from __future__ import annotations

from typing import Any, ClassVar, Iterable, Optional, Sequence

import pyarrow as pa

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.pyarrow import pyarrow_to_polars
from chalk.utils.json import TJSON

from ._base import _DEFAULT_FEATURE_ENCODING_OPTIONS, FeatureConverter

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportMissingSuperCall=false, reportReturnType=false, reportUnnecessaryCast=false


_NULL_ARROW_TYPE = pb.ArrowType(none=pb.EmptyMessage())
_NULL_SCALAR_VALUE = pb.ScalarValue(null_value=_NULL_ARROW_TYPE)


class NullFeatureConverter(FeatureConverter[None, None]):
    """Converter for pa.null() — all values are always None.

    Used for struct fields whose PyArrow type is pa.null() (e.g. columns
    inferred from an all-null dataset, as seen in GlueCatalog serde).
    Singleton: NullFeatureConverter.new() always returns the same instance.
    """

    _instance: ClassVar[Optional["NullFeatureConverter"]] = None

    @classmethod
    def new(cls) -> "NullFeatureConverter":
        if cls._instance is None:
            inst = cls.__new__(cls)
            super(NullFeatureConverter, inst).__init__()
            cls._instance = inst
        return cls._instance

    # ── properties ────────────────────────────────────────────────────────────

    @property
    def rich_type(self) -> type:
        return type(None)

    @property
    def primitive_type(self) -> type:
        return type(None)

    @property
    def pyarrow_dtype(self) -> pa.DataType:
        return pa.null()

    @property
    def protobuf_dtype(self) -> pb.ArrowType:
        return _NULL_ARROW_TYPE

    @property
    def polars_dtype(self) -> Any:
        return pyarrow_to_polars(pa.null())

    @property
    def encoder(self) -> None:
        return None

    @property
    def decoder(self) -> None:
        return None

    @property
    def is_nullable(self) -> bool:
        return True

    @property
    def has_default(self) -> bool:
        return True

    @property
    def pyarrow_default(self) -> pa.Array:
        return pa.array([None], type=pa.null())

    @property
    def primitive_default(self) -> None:
        return None

    @property
    def rich_default(self) -> None:
        return None

    def has_nontrivial_rich_type(self) -> bool:
        return False

    # ── missing-value helpers ─────────────────────────────────────────────────

    def is_value_missing(self, value: Any) -> bool:
        return value is ...

    def is_rich_valid(self, value: Any) -> bool:
        return True

    # ── rich ↔ primitive ──────────────────────────────────────────────────────

    def from_rich_to_primitive(
        self,
        value: Any,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> None:
        return None

    def from_primitive_to_rich(self, value: Any) -> None:
        return None

    # ── primitive ↔ pyarrow ───────────────────────────────────────────────────

    def from_pyarrow_to_primitive(self, values: "pa.Array | pa.ChunkedArray") -> Sequence[None]:
        return [None] * len(values)

    def from_primitive_to_pyarrow(self, values: "Iterable[Any]") -> pa.Array:
        return pa.array([None] * len(list(values)), type=pa.null())

    def from_pyarrow_to_rich(self, values: "pa.Array | pa.ChunkedArray", /) -> Sequence[None]:
        return [None] * len(values)

    def from_rich_to_pyarrow(
        self,
        values: "Sequence[Any]",
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        feature_name: "str | None" = None,
    ) -> pa.Array:
        return pa.array([None] * len(list(values)), type=pa.null())

    # ── json ↔ * ──────────────────────────────────────────────────────────────

    def from_primitive_to_json(
        self,
        value: None,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        return None

    def from_json_to_primitive(self, value: "TJSON | None") -> None:
        return None

    def from_json_to_rich(self, value: TJSON) -> None:
        return None

    def from_rich_to_json(
        self,
        value: Any,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        return None

    def from_pyarrow_to_json(
        self,
        values: "pa.Array | pa.ChunkedArray",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> "Sequence[TJSON]":
        return [None] * len(values)

    def from_json_to_pyarrow(self, values: "Sequence[TJSON]") -> pa.Array:
        return pa.array([None] * len(list(values)), type=pa.null())

    # ── protobuf ↔ * ─────────────────────────────────────────────────────────

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        return _NULL_SCALAR_VALUE

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        return pa.nulls(1, type=pa.null())[0]

    def from_rich_to_protobuf(
        self,
        value: Any,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        return _NULL_SCALAR_VALUE

    def from_primitive_to_protobuf(self, value: Any) -> pb.ScalarValue:
        return _NULL_SCALAR_VALUE
