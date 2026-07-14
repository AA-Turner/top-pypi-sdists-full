from __future__ import annotations

import typing
from typing import (
    Any,
    ClassVar,
    Dict,
    Iterable,
    Sequence,
    Tuple,
    Type,
    cast,
)

import pyarrow as pa
import pyarrow.compute as pc

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.json import (
    FeatureEncodingOptions,
    structure_json_to_primitive,
    unstructure_primitive_to_json,
)
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.pyarrow import (
    pyarrow_to_polars,
    pyarrow_to_primitive,
)
from chalk.utils.df_utils import table_from_arrow_ipc, table_to_arrow_ipc
from chalk.utils.json import TJSON

from ._base import (
    _DEFAULT_FEATURE_ENCODING_OPTIONS,
    _identity,
    _scalar_coerce_fn,
    FeatureConverter,
    MissingValueError,
    _raise_unsupported_missing_value_strategy,
)

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportMissingSuperCall=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false

try:
    import numpy as np
except ImportError:
    np = None  # type: ignore[assignment]


class FixedSizeListFeatureConverter(FeatureConverter[list, list]):
    """Feature converter for fixed-size list features (pa.list_(T, N)).

    Rich type:      list[T]
    Primitive type: list[primitive(T)]
    PyArrow type:   pa.list_(item_converter.pyarrow_dtype, list_size)

    Use :meth:`new` to obtain a (possibly cached) instance.

    Float16 element note: PyArrow cannot construct fixed-size-list arrays from
    Python floats for float16 items.  The array is built via numpy (matching
    PrimitiveFeatureConverter's convention), and null elements within the list
    become NaN rather than proper null entries.
    """

    _cache: ClassVar[Dict[Tuple[Any, Any, bool, int, Any], "FixedSizeListFeatureConverter"]] = {}

    @classmethod
    def new(
        cls,
        item_converter: FeatureConverter,
        default: "list | None | ellipsis",
        is_nullable: bool,
        list_size: int,
        list_rich_type: "Type | None" = None,
    ) -> "FixedSizeListFeatureConverter":
        if default is None or default is ...:
            key = (item_converter, default, is_nullable, list_size, list_rich_type)
            cached = cls._cache.get(key)
            if cached is not None:
                return cached
            inst = cls(item_converter, default, is_nullable, list_size, list_rich_type)
            cls._cache[key] = inst
            return inst
        return cls(item_converter, default, is_nullable, list_size, list_rich_type)

    def __init__(
        self,
        item_converter: FeatureConverter,
        default: "list | None | ellipsis",
        is_nullable: bool,
        list_size: int,
        list_rich_type: "Type | None" = None,
    ) -> None:
        super().__init__()
        self._item = item_converter
        self._is_nullable = is_nullable
        self._list_size = list_size
        self._list_rich_type = list_rich_type
        self._pa_list_type: pa.DataType = pa.list_(item_converter.pyarrow_dtype, list_size)
        self._is_float16_items: bool = pa.types.is_float16(item_converter.pyarrow_dtype)

        # Element coercion closures — same logic as ListFeatureConverter.
        coerce = _scalar_coerce_fn(item_converter)
        if not item_converter.has_nontrivial_rich_type():
            self._elem_to_prim: Any = coerce if coerce is not None else _identity
            self._elem_to_rich: Any = _identity
        else:
            self._elem_to_prim = item_converter.from_rich_to_primitive
            self._elem_to_rich = item_converter.from_primitive_to_rich

        self._primitive_type = pyarrow_to_primitive(self._pa_list_type, "")

        # Precompute protobuf schema from item converter.
        _item_null_pb = item_converter.from_pyarrow_to_protobuf(pa.nulls(1, item_converter.pyarrow_dtype)[0])
        self._item_arrow_proto_type: pb.ArrowType = _item_null_pb.null_value
        self._null_proto: pb.ArrowType = pb.ArrowType(
            fixed_size_list=pb.FixedSizeList(
                field_type=pb.Field(
                    name=self._pa_list_type.value_field.name,
                    nullable=self._pa_list_type.value_field.nullable,
                    arrow_type=self._item_arrow_proto_type,
                ),
                list_size=list_size,
            )
        )
        self._pb_schema: pb.Schema = pb.Schema(
            columns=[pb.Field(nullable=False, arrow_type=self._item_arrow_proto_type)]
        )

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
                self._pyarrow_default = self.from_primitive_to_pyarrow([prim])
        else:
            self._has_default = False
            self._primitive_default = ...
            self._rich_default_val = None
            self._pyarrow_default = ...

    # ── helpers ──────────────────────────────────────────────────────────────

    def _to_primitive(self, value: list) -> list:
        conv = self._elem_to_prim
        return [conv(v) for v in value]

    def _to_rich(self, value: list) -> list:
        conv = self._elem_to_rich
        return [conv(v) for v in value]

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
        if self._list_rich_type is not None:
            return self._list_rich_type  # type: ignore[return-value]
        if self.is_nullable:
            return typing.Optional[list[self._item.rich_type]]  # type: ignore[return-value]
        return list[self._item.rich_type]  # type: ignore[return-value]

    @property
    def primitive_type(self) -> Type[list]:
        return typing.List[self._item.primitive_type]

    @property
    def pyarrow_dtype(self) -> pa.DataType:
        return self._pa_list_type

    @property
    def protobuf_dtype(self) -> pb.ArrowType:
        return self._null_proto

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
        return self._item.has_nontrivial_rich_type()

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
        if self._is_float16_items:
            values = tuple(values)
            empty = [None] * self._list_size
            flat = np.array(  # type: ignore[union-attr]
                [empty if v is None or v is ... else v for v in values],
                dtype=np.float16,  # type: ignore[union-attr]
            ).reshape(-1)
            ans = pa.FixedSizeListArray.from_arrays(flat, self._list_size)
            mask = pa.array([v is not None and v is not ... for v in values], type=pa.bool_())
            return pc.if_else(mask, ans, pa.scalar(None, self._pa_list_type))  # type: ignore[attr-defined]
        return pa.array(
            [None if v is None or v is ... else v for v in values],
            type=self._pa_list_type,
        )

    def from_pyarrow_to_rich(self, values: pa.Array | pa.ChunkedArray, /) -> Sequence[list | None]:
        return [None if v is None else self._to_rich(v) for v in values.to_pylist()]

    def from_rich_to_pyarrow(
        self,
        values: Sequence[list | ellipsis | None],
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        feature_name: str | None = None,
    ) -> pa.Array | pa.ChunkedArray:
        converted: list[list | None] = []
        for v in values:
            if v is ... or (v is None and not self._is_nullable):
                result = self._handle_missing(v, missing_value_strategy)
                converted.append(None if result is ... else cast(Any, result))
            elif v is None:
                converted.append(None)
            else:
                converted.append(self._to_primitive(cast(list, v)))
        return self.from_primitive_to_pyarrow(converted)

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
            return pb.ScalarValue(null_value=self._null_proto)
        values = value.values
        table = pa.Table.from_arrays([values], names=["values"])
        return pb.ScalarValue(
            fixed_size_list_value=pb.ScalarListValue(
                arrow_data=table_to_arrow_ipc(table, compression="lz4"), schema=self._pb_schema
            )
        )

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=self._pa_list_type)[0]
        arr = table_from_arrow_ipc(pb_value.fixed_size_list_value.arrow_data).column(0).combine_chunks()
        return pa.scalar(arr.to_pylist(), pa.list_(arr.type, len(arr)))
