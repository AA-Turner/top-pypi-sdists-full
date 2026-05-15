from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Dict,
    Iterable,
    List,
    Sequence,
    Tuple,
    cast,
)

import pyarrow as pa

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.json import (
    FeatureEncodingOptions,
    unstructure_primitive_to_json,
)
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.pyarrow import pyarrow_to_polars, pyarrow_to_primitive
from chalk.utils.json import TJSON

from ._base import (
    _DEFAULT_FEATURE_ENCODING_OPTIONS,
    _FROM_NEW,
    FeatureConverter,
    MissingValueError,
    _raise_unsupported_missing_value_strategy,
)

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportMissingSuperCall=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false, reportImplicitStringConcatenation=false


class AnonymousStructFeatureConverter(
    FeatureConverter["dict[str, Any]", "dict[str, Any]"],
):
    """FeatureConverter for a struct type with no associated Python class.

    Rich type:      dict[str, Any]  (plain dict, keyed by field name)
    Primitive type: dict[str, Any]
    PyArrow type:   pa.StructType

    Used when the factory receives rich_type=... with a pa.StructType —
    the schema-only path that arises during operator deserialization, where
    only the Arrow schema survives the round-trip and no Python class is
    available.

    None handling matches GenericFeatureConverter: None is expanded to an
    all-null-field dict ({"x": None, "y": None, ...}), producing a *valid*
    struct row with null field values rather than a null struct row.  This
    preserves the existing GenericFC contract that callers depend on.

    JSON encoding uses the same positional-list format as GenericFC:
    {"x": 1, "y": "a"} → [1, "a"].
    """

    _cache: ClassVar[Dict[Tuple[pa.DataType, Any, bool], "AnonymousStructFeatureConverter"]] = {}

    @classmethod
    def new(
        cls,
        pa_struct_type: pa.StructType,
        default: "Any | ellipsis",
        is_nullable: bool,
        *,
        field_converters: "Dict[str, FeatureConverter]",
    ) -> "AnonymousStructFeatureConverter":
        """Factory with caching for simple defaults (None / ...)."""
        if default is None or default is ...:
            key = (pa_struct_type, default, is_nullable)
            cached = cls._cache.get(key)
            if cached is not None:
                return cached
            inst = cls(pa_struct_type, default, is_nullable, field_converters=field_converters, _from_new=_FROM_NEW)
            cls._cache[key] = inst
            return inst
        return cls(pa_struct_type, default, is_nullable, field_converters=field_converters, _from_new=_FROM_NEW)

    def __init__(
        self,
        pa_struct_type: pa.StructType,
        default: "Any | ellipsis",
        is_nullable: bool,
        *,
        field_converters: "Dict[str, FeatureConverter]",
        _from_new: object = None,
    ) -> None:
        super().__init__()
        if _from_new is not _FROM_NEW:
            raise TypeError("Use AnonymousStructFeatureConverter.new() instead")

        self._pa_struct_type: pa.StructType = pa_struct_type
        self._is_nullable = is_nullable
        self._pa_struct_fields: List[pa.Field] = [pa_struct_type.field(i) for i in range(pa_struct_type.num_fields)]
        self._field_names: Tuple[str, ...] = tuple(f.name for f in self._pa_struct_fields)
        self._field_converters: Dict[str, FeatureConverter] = field_converters
        self._null_prim: dict = {name: None for name in self._field_names}
        self._primitive_type = pyarrow_to_primitive(pa_struct_type, "")

        # Track which fields need per-element coercion (nontrivial rich type)
        # and which nested anonymous structs get the columnar path.
        self._nontrivial_fields: Tuple[str, ...] = tuple(
            name for name in self._field_names
            if field_converters[name].has_nontrivial_rich_type()
        )
        self._sub_anon_converters: Dict[str, "AnonymousStructFeatureConverter"] = {
            k: v for k, v in field_converters.items()
            if isinstance(v, AnonymousStructFeatureConverter)
        }

        # Protobuf type descriptors — built from each field converter.
        self._proto_field_arrow_types: Dict[str, pb.ArrowType] = {
            fname: fconv.from_pyarrow_to_protobuf(pa.nulls(1, fconv.pyarrow_dtype)[0]).null_value
            for fname, fconv in field_converters.items()
        }
        self._null_proto: pb.ArrowType = pb.ArrowType(
            struct=pb.Struct(sub_field_types=[
                pb.Field(
                    name=pa_field.name,
                    nullable=pa_field.nullable,
                    arrow_type=self._proto_field_arrow_types[pa_field.name],
                )
                for pa_field in self._pa_struct_fields
            ])
        )

        # Default handling
        if is_nullable and default is ...:
            default = None
        if default is not ...:
            self._has_default = True
            self._rich_default_val: Any = default
            if default is None:
                self._primitive_default: "dict | None | ellipsis" = self._null_prim
                self._pyarrow_default: "ellipsis | pa.Array | pa.ChunkedArray" = pa.array(
                    [self._null_prim], type=self._pa_struct_type
                )
            else:
                prim = {name: field_converters[name].from_rich_to_primitive(default[name]) for name in self._field_names}
                self._primitive_default = prim
                self._pyarrow_default = pa.array([prim], type=self._pa_struct_type)
        else:
            self._has_default = False
            self._primitive_default = ...
            self._rich_default_val = None
            self._pyarrow_default = ...

    # ── columnar helpers ──────────────────────────────────────────────────────

    def _to_pyarrow_flat_from_dicts(self, dicts: list) -> "pa.StructArray":
        """Convert a flat list of dicts → pa.StructArray (columnar)."""
        if not dicts:
            return pa.array([], type=self._pa_struct_type)
        if not self._pa_struct_fields:
            return pa.array(dicts, type=self._pa_struct_type)
        arrays: list = []
        for pa_field in self._pa_struct_fields:
            fname = pa_field.name
            fc = self._field_converters[fname]
            col = [None if d is None else d.get(fname) for d in dicts]
            if fname in self._sub_anon_converters:
                arrays.append(self._sub_anon_converters[fname]._to_pyarrow_flat_from_dicts(col))
            elif fname in self._nontrivial_fields:
                arrays.append(pa.array(
                    [None if x is None else fc.from_rich_to_primitive(x) for x in col],
                    type=pa_field.type,
                ))
            else:
                arrays.append(pa.array(col, type=pa_field.type))
        if any(d is None for d in dicts):
            null_mask = pa.array([d is None for d in dicts])
            return pa.StructArray.from_arrays(arrays, fields=self._pa_struct_fields, mask=null_mask)
        return pa.StructArray.from_arrays(arrays, fields=self._pa_struct_fields)

    def _from_pyarrow_flat(self, struct_arr: "pa.StructArray") -> list:
        """Convert a pa.StructArray → list of plain dicts (columnar)."""
        n = len(struct_arr)
        if n == 0:
            return []
        valid = struct_arr.is_valid().to_pylist()
        has_nulls = not all(valid)
        field_data: list = []
        for pa_field in self._pa_struct_fields:
            fname = pa_field.name
            fc = self._field_converters[fname]
            col = struct_arr.field(fname)
            if fname in self._sub_anon_converters:
                field_data.append(self._sub_anon_converters[fname]._from_pyarrow_flat(col))
            elif fname in self._nontrivial_fields:
                field_data.append([None if x is None else fc.from_primitive_to_rich(x) for x in col.to_pylist()])
            else:
                field_data.append(col.to_pylist())
        field_names = self._field_names
        n_fields = len(field_data)
        if has_nulls:
            return [
                None if not valid[i]
                else {field_names[fi]: field_data[fi][i] for fi in range(n_fields)}
                for i in range(n)
            ]
        return [{field_names[fi]: field_data[fi][i] for fi in range(n_fields)} for i in range(n)]

    # ── helpers ───────────────────────────────────────────────────────────────

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

    def _apply_rich_to_prim(self, v: dict) -> dict:
        if not self._nontrivial_fields and not self._sub_anon_converters:
            return {name: v.get(name) for name in self._field_names}
        result: dict[str, Any] = {}
        for name in self._field_names:
            val = v.get(name)
            if name in self._sub_anon_converters or name in self._nontrivial_fields:
                result[name] = self._field_converters[name].from_rich_to_primitive(val)
            else:
                result[name] = val
        return result

    def _apply_prim_to_rich(self, v: dict) -> dict:
        if not self._nontrivial_fields and not self._sub_anon_converters:
            return {name: v.get(name) for name in self._field_names}
        result: dict[str, Any] = {}
        for name in self._field_names:
            val = v.get(name)
            if name in self._sub_anon_converters or name in self._nontrivial_fields:
                result[name] = self._field_converters[name].from_primitive_to_rich(val)
            else:
                result[name] = val
        return result

    # ── properties ────────────────────────────────────────────────────────────

    @property
    def rich_type(self) -> type:
        return dict

    @property
    def primitive_type(self) -> type:
        return dict

    @property
    def pyarrow_dtype(self) -> pa.DataType:
        return self._pa_struct_type

    @property
    def protobuf_dtype(self) -> pb.ArrowType:
        return self._null_proto

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
        return value is ...

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
            return self._null_prim
        return self._apply_rich_to_prim(value)

    def from_primitive_to_rich(self, value: "dict | None") -> Any:
        if value is ...:
            return ...
        if value is None:
            return self._null_prim
        return self._apply_prim_to_rich(value)

    # ── primitive ↔ pyarrow ───────────────────────────────────────────────────

    def from_pyarrow_to_primitive(self, values: "pa.Array | pa.ChunkedArray") -> "Sequence[dict | None]":
        if isinstance(values, pa.ChunkedArray):
            values = values.combine_chunks()
        return self._from_pyarrow_flat(values)

    def from_primitive_to_pyarrow(self, values: "Iterable[dict | None]") -> "pa.Array | pa.ChunkedArray":
        values_list = [None if v is ... else v for v in values]
        return self._to_pyarrow_flat_from_dicts(values_list)

    def from_pyarrow_to_rich(self, values: "pa.Array | pa.ChunkedArray", /) -> "Sequence[Any]":
        if isinstance(values, pa.ChunkedArray):
            values = values.combine_chunks()
        return self._from_pyarrow_flat(values)

    def from_rich_to_pyarrow(
        self,
        values: "Sequence[Any | ellipsis | None]",
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        feature_name: "str | None" = None,
    ) -> "pa.Array | pa.ChunkedArray":
        converted: list = []
        for v in values:
            if v is ...:
                result = self._handle_missing(v, missing_value_strategy)
                converted.append(None if result is ... else cast(Any, result))
            elif v is None:
                converted.append(self._null_prim)
            else:
                converted.append(self._apply_rich_to_prim(v))
        return self._to_pyarrow_flat_from_dicts(converted)

    # ── json ↔ * ──────────────────────────────────────────────────────────────

    def from_primitive_to_json(
        self,
        value: "dict | None",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        # Produces a positional list [v1, v2, ...] matching GenericFC format.
        return unstructure_primitive_to_json(value)

    def from_json_to_primitive(self, value: "TJSON | dict | None") -> "dict | None":
        # GenericFC serialises structs as positional lists; we must handle both
        # list and dict inputs. structure_json_to_primitive(list, dict) fails,
        # so we implement the decode manually.
        if value is None:
            return self._null_prim
        if isinstance(value, dict):
            return {
                name: self._field_converters[name].from_json_to_primitive(value.get(name))
                for name in self._field_names
            }
        if isinstance(value, (list, tuple)):
            return {
                self._field_names[i]: self._field_converters[self._field_names[i]].from_json_to_primitive(
                    value[i] if i < len(value) else None
                )
                for i in range(len(self._field_names))
            }
        raise TypeError(f"Cannot convert {type(value).__name__} to struct primitive")

    def from_json_to_rich(self, value: TJSON) -> Any:
        prim = self.from_json_to_primitive(value)
        if prim is None:
            return None
        return self._apply_prim_to_rich(prim)

    def from_rich_to_json(
        self,
        value: "Any | ellipsis | None",
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        prim = self.from_rich_to_primitive(value, missing_value_strategy)
        return self.from_primitive_to_json(cast("dict | None", prim), options=options)

    def from_pyarrow_to_json(
        self,
        values: "pa.Array | pa.ChunkedArray",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> "Sequence[TJSON]":
        return [self.from_primitive_to_json(x, options=options) for x in self.from_pyarrow_to_primitive(values)]

    def from_json_to_pyarrow(self, values: "Sequence[TJSON]") -> "pa.Array | pa.ChunkedArray":
        return self.from_primitive_to_pyarrow([self.from_json_to_primitive(x) for x in values])

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
            return pb.ScalarValue(null_value=self._null_proto)
        fields: List[pb.Field] = []
        field_values: List[pb.ScalarValue] = []
        for name, pa_scalar in value.items():
            fields.append(pb.Field(name=name, nullable=True, arrow_type=self._proto_field_arrow_types[name]))
            field_values.append(self._field_converters[name].from_pyarrow_to_protobuf(pa_scalar))
        return pb.ScalarValue(struct_value=pb.StructValue(fields=fields, field_values=field_values))

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=self._pa_struct_type)[0]
        name_to_pa_scalar = {
            field.name: self._field_converters[field.name].from_protobuf_to_pyarrow(fv)
            for field, fv in zip(pb_value.struct_value.fields, pb_value.struct_value.field_values)
        }
        name_to_py_not_none = {k: o for k, v in name_to_pa_scalar.items() if (o := v.as_py()) is not None}
        pa_fields = [pa.field(k, v.type) for k, v in name_to_pa_scalar.items()]
        return pa.scalar(name_to_py_not_none, pa.struct(pa_fields))
