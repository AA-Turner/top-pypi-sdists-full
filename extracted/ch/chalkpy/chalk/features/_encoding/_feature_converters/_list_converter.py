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

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.json import (
    FeatureEncodingOptions,
    structs_as_objects_feature_json_converter,
    structure_json_to_primitive,
    unstructure_primitive_to_json,
)
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.pyarrow import (
    is_map_in_dtype_tree,
    pyarrow_to_polars,
    pyarrow_to_primitive,
)
from chalk.utils.json import TJSON

from ._base import (
    _DEFAULT_FEATURE_ENCODING_OPTIONS,
    _identity,
    _scalar_coerce_fn,
    _ScalarConverterBase,
    FeatureConverter,
    MissingValueError,
    _raise_unsupported_missing_value_strategy,
)
from ._dataclass_converter import DataclassFeatureConverter
from ._primitive_converter import _FeatureConverterArrowProtoHelpers, PrimitiveFeatureConverter

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportMissingSuperCall=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false, reportImplicitStringConcatenation=false


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

    _cache: ClassVar[Dict[Tuple[Any, Any, bool, Any], "ListFeatureConverter"]] = {}

    @classmethod
    def new(
        cls,
        item_converter: FeatureConverter,
        default: "list | None | ellipsis",
        is_nullable: bool,
        list_rich_type: "Type | None" = None,
    ) -> "ListFeatureConverter":
        # Cache only for simple defaults since lists are not hashable.
        # item_converter instances are cached themselves (e.g. DataclassConverter.for_class),
        # so using object identity as the key is stable.
        if default is None or default is ...:
            key = (item_converter, default, is_nullable, list_rich_type)
            cached = cls._cache.get(key)
            if cached is not None:
                return cached
            inst = cls(item_converter, default, is_nullable, list_rich_type)
            cls._cache[key] = inst
            return inst
        return cls(item_converter, default, is_nullable, list_rich_type)

    def __init__(
        self,
        item_converter: FeatureConverter,
        default: "list | None | ellipsis",
        is_nullable: bool,
        list_rich_type: "Type | None" = None,
    ) -> None:
        super().__init__()
        self._item = item_converter
        self._is_nullable = is_nullable
        self._list_rich_type = list_rich_type
        self._pa_list_type: pa.DataType = pa.large_list(item_converter.pyarrow_dtype)
        # Store the element-level closures directly to avoid method-dispatch overhead
        # in _to_primitive / _to_rich.  ListConverter guarantees it only calls these
        # with non-None, non-... values (missing values are handled at the list level).
        if isinstance(item_converter, DataclassFeatureConverter):
            self._elem_to_prim: Any = (
                item_converter._rich_to_prim  # pyright: ignore[reportPrivateUsage]
            )
            self._elem_to_rich: Any = (
                item_converter._prim_to_rich  # pyright: ignore[reportPrivateUsage]
            )
        elif not item_converter.has_nontrivial_rich_type():
            # For most primitive types (bool, int, str, …) rich IS primitive.
            # For coercible scalar types (datetime, date, time, timedelta) the
            # converter accepts a wider input set (e.g. date → datetime), so use
            # its coerce function to normalise elements on the rich→primitive path.
            coerce = _scalar_coerce_fn(item_converter)
            self._elem_to_prim = coerce if coerce is not None else _identity
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

    @property
    def _item_type_display(self) -> str:
        """Return the non-nullable item type name for use in error messages (e.g. 'bool', 'int')."""
        if isinstance(self._item, _ScalarConverterBase):
            return type(self._item)._rich_type_value.__name__  # type: ignore[attr-defined]
        return str(self._item.rich_type)

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
        # Fast path: pa.array() handles the whole structure in C++ when no per-field
        # coercion is needed (non-dataclass items, or dataclass items whose primitive
        # form maps directly to their PyArrow types without any Python-level coercion).
        if not (
            isinstance(self._item, DataclassFeatureConverter)
            and (self._item._field_prim_convs or self._item._sub_dc_converters)  # pyright: ignore[reportPrivateUsage]
        ):
            return pa.array(
                [None if v is None or v is ... else v for v in values],
                type=self._pa_list_type,
            )
        # Columnar path: build a flat StructArray via _to_pyarrow_flat_from_dicts so
        # that per-field coercions (e.g. str/date → datetime) are applied correctly.
        flat_dicts: list = []
        offsets: list[int] = [0]
        null_flags: list[bool] = []
        has_nulls = False
        for v in values:
            if v is None or v is ...:
                null_flags.append(True)
                offsets.append(offsets[-1])
                has_nulls = True
            else:
                null_flags.append(False)
                flat_dicts.extend(v)
                offsets.append(offsets[-1] + len(v))
        flat_struct = self._item._to_pyarrow_flat_from_dicts(flat_dicts)  # pyright: ignore[reportPrivateUsage]
        offsets_arr = pa.array(offsets, type=pa.int64())
        if has_nulls:
            return pa.LargeListArray.from_arrays(offsets_arr, flat_struct, mask=pa.array(null_flags))
        return pa.LargeListArray.from_arrays(offsets_arr, flat_struct)

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
        feature_name: str | None = None,
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
                    try:
                        converted.append(self._to_primitive(cast(list, v)))
                    except (TypeError, ValueError) as e:
                        feature_part = f" for feature '{feature_name}'" if feature_name is not None else ""
                        raise TypeError(
                            f"Could not convert '{v}' to `list[{self._item_type_display}]`{feature_part}: {e}"
                        ) from e
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
