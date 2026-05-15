from __future__ import annotations

import dataclasses as _dataclasses
import typing as _typing_mod
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterable,
    List,
    Sequence,
    Tuple,
    cast,
    get_args,
    get_origin,
    is_typeddict,
)

import pyarrow as pa

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.json import (
    FeatureEncodingOptions,
    structure_json_to_primitive,
    unstructure_primitive_to_json,
)
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.pyarrow import (
    coerce_map_pylist_to_dict,
    is_map_in_dtype_tree,
    pyarrow_to_polars,
    pyarrow_to_primitive,
    rich_to_pyarrow,
)
from chalk.utils.collections import unwrap_optional_and_annotated_if_needed
from chalk.utils.json import TJSON

from ._base import (
    _DEFAULT_FEATURE_ENCODING_OPTIONS,
    _FROM_NEW,
    _SCALAR_COERCIBLE_TYPES,
    FeatureConverter,
    MissingValueError,
    _raise_unsupported_missing_value_strategy,
    _scalar_coerce_fn,
)

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportMissingSuperCall=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false, reportImplicitStringConcatenation=false


def _build_to_primitive_converter(typ: type) -> "Callable[[Any], Any] | None":
    """Return a closure that converts a value of *typ* to its primitive form, or ``None``
    if no conversion is needed.

    Handles TypedDicts, dataclasses, ``list[T]``, and scalar coercible types (date/datetime/etc.).
    ``Optional[T]`` / ``Annotated[T, …]`` wrappers are stripped before dispatch.
    """
    inner = unwrap_optional_and_annotated_if_needed(typ)

    if isinstance(inner, type) and is_typeddict(inner):
        return _build_td_to_dict(inner)

    if _dataclasses.is_dataclass(inner) and isinstance(inner, type):
        from ._dataclass_converter import _build_dc_to_dict
        return _build_dc_to_dict(inner)

    origin = get_origin(inner)
    if origin in (list, List):
        args = get_args(inner)
        if args:
            item_conv = _build_to_primitive_converter(args[0])
            if item_conv is not None:
                return lambda lst, _c=item_conv: None if lst is None else [_c(x) for x in lst]

    if inner in _SCALAR_COERCIBLE_TYPES:
        from ._factory import make_feature_converter as _make_fc
        fc = _make_fc(name="", is_nullable=True, rich_type=typ)
        closure = _scalar_coerce_fn(fc)
        if closure is not None:
            return closure

    return None


def _build_to_rich_converter(typ: type) -> "Callable[[Any], Any] | None":
    """Return a closure that converts a primitive value back to *typ*, or ``None``
    if no conversion is needed.

    Mirrors :func:`_build_to_primitive_converter` in the reverse direction.
    """
    inner = unwrap_optional_and_annotated_if_needed(typ)

    if isinstance(inner, type) and is_typeddict(inner):
        return _build_dict_to_td(inner)

    if _dataclasses.is_dataclass(inner) and isinstance(inner, type):
        from ._dataclass_converter import _build_dict_to_dc
        return _build_dict_to_dc(inner)

    origin = get_origin(inner)
    if origin in (list, List):
        args = get_args(inner)
        if args:
            item_conv = _build_to_rich_converter(args[0])
            if item_conv is not None:
                return lambda lst, _c=item_conv: None if lst is None else [_c(x) for x in lst]

    return None


def _build_td_to_dict(td_class: type) -> "Callable[[Any], Any]":
    """Build a converter from a TypedDict instance (plain dict) to a primitive dict.

    TypedDict is always a plain ``dict`` at runtime, so there is no ``getattr`` branch.
    Per-field sub-coercions are built with :func:`_build_to_primitive_converter` so that
    nested TypedDicts, dataclasses, date fields, etc. are all handled recursively.
    """
    hints = _typing_mod.get_type_hints(td_class)
    field_names: tuple[str, ...] = tuple(hints.keys())

    sub: dict[str, Callable] = {
        name: conv
        for name in field_names
        if (conv := _build_to_primitive_converter(hints[name])) is not None
    }

    null_prim: dict = {f: None for f in field_names}

    if not sub:
        def _convert_flat(v: Any) -> Any:
            if v is None:
                return null_prim
            if v is ...:
                return v
            return {f: v.get(f) for f in field_names}
        return _convert_flat
    else:
        def _convert_nested(v: Any) -> Any:
            if v is None:
                return {f: sub[f](None) if f in sub else None for f in field_names}
            return {f: sub[f](v.get(f)) if f in sub else v.get(f) for f in field_names}
        return _convert_nested


def _build_dict_to_td(td_class: type) -> "Callable[[Any], Any]":
    """Build a converter from a primitive dict back to a TypedDict (plain dict).

    Since TypedDict is just ``dict`` at runtime, no constructor call is needed —
    only per-field sub-coercions for nested types.
    """
    hints = _typing_mod.get_type_hints(td_class)
    field_names: tuple[str, ...] = tuple(hints.keys())

    sub: dict[str, Callable] = {
        name: conv
        for name in field_names
        if (conv := _build_to_rich_converter(hints[name])) is not None
    }

    null_prim: dict = {f: None for f in field_names}

    if not sub:
        def _reconstruct_flat(d: Any) -> Any:
            if d is None:
                return null_prim
            return {f: d.get(f) for f in field_names}
        return _reconstruct_flat
    else:
        def _reconstruct_nested(d: Any) -> Any:
            if d is None:
                return {f: sub[f](None) if f in sub else None for f in field_names}
            return {f: sub[f](d.get(f)) if f in sub else d.get(f) for f in field_names}
        return _reconstruct_nested


class TypedDictFeatureConverter(
    FeatureConverter["dict[str, Any]", "dict[str, Any]"],
):
    """Full :class:`FeatureConverter` for a single TypedDict (struct) element.

    Rich type:      dict[str, Any]  (TypedDict is plain dict at runtime)
    Primitive type: dict[str, Any]
    PyArrow type:   pa.struct([...])

    Structurally mirrors :class:`DataclassFeatureConverter`, with two key differences:

    1. Field names are read from ``typing.get_type_hints`` instead of ``dataclasses.fields``.
    2. ``from_primitive_to_rich(None)`` returns an all-null dict (``{"x": None, …}``) rather
       than ``None``, matching :class:`GenericFeatureConverter` semantics for TypedDict
       (``SimpleDict(x=None, y=None) == {"x": None, "y": None}``).
    """

    _cache: ClassVar[Dict[Tuple[type, Any, bool], "TypedDictFeatureConverter"]] = {}

    @classmethod
    def for_class(cls, td_class: type) -> "TypedDictFeatureConverter":
        """Return a cached converter (``is_nullable=True``, no default).

        Suitable for use as the ``item_converter`` in :class:`ListConverter`.
        """
        return cls.new(td_class, ..., is_nullable=True)

    @classmethod
    def new(
        cls,
        td_class: type,
        default: "Any | ellipsis",
        is_nullable: bool,
        field_converters: "Dict[str, FeatureConverter] | None" = None,
    ) -> "TypedDictFeatureConverter":
        """Factory with caching for simple defaults (``None`` / ``…``)."""
        if default is None or default is ...:
            key = (td_class, default, is_nullable)
            cached = cls._cache.get(key)
            if cached is not None:
                return cached
            if field_converters is None:
                from ._factory import make_field_converters_for_typed_dict as _make_fc
                field_converters = _make_fc(td_class)
            inst = cls(td_class, default, is_nullable, field_converters=field_converters, _from_new=_FROM_NEW)
            cls._cache[key] = inst
            return inst
        if field_converters is None:
            from ._factory import make_field_converters_for_typed_dict as _make_fc
            field_converters = _make_fc(td_class)
        return cls(td_class, default, is_nullable, field_converters=field_converters, _from_new=_FROM_NEW)

    def __init__(
        self,
        td_class: type,
        default: "Any | ellipsis",
        is_nullable: bool,
        *,
        field_converters: "Dict[str, FeatureConverter] | None" = None,
        _from_new: object = None,
    ) -> None:
        super().__init__()
        if _from_new is not _FROM_NEW:
            raise TypeError("Use TypedDictFeatureConverter.new() or TypedDictFeatureConverter.for_class() instead")
        assert field_converters is not None, "field_converters must be provided via TypedDictFeatureConverter.new()"
        self._td_class = td_class
        self._is_nullable = is_nullable

        hints = _typing_mod.get_type_hints(td_class)
        field_names: tuple[str, ...] = tuple(hints.keys())
        struct_fields = [pa.field(name, rich_to_pyarrow(hints[name], name, in_struct=True)) for name in field_names]
        self._pa_struct_type: pa.DataType = pa.struct(struct_fields)
        self._primitive_type = pyarrow_to_primitive(self._pa_struct_type, "")
        self._rich_to_prim: Callable[[Any], Any] = _build_td_to_dict(td_class)
        self._prim_to_rich: Callable[[Any], Any] = _build_dict_to_td(td_class)
        self._null_prim: dict = {name: None for name in field_names}

        self._field_names = field_names
        self._struct_fields_list = struct_fields
        self._field_converters: Dict[str, FeatureConverter] = field_converters
        self._sub_td_converters: Dict[str, "TypedDictFeatureConverter"] = {
            k: v for k, v in field_converters.items() if isinstance(v, TypedDictFeatureConverter)
        }
        self._field_prim_convs: Dict[str, Callable[[Any], Any]] = {}
        self._field_rich_convs: Dict[str, Callable[[Any], Any]] = {}
        for _fname in field_names:
            _inner_t = unwrap_optional_and_annotated_if_needed(hints[_fname])
            if not (isinstance(_inner_t, type) and is_typeddict(_inner_t)):
                _to_prim = _build_to_primitive_converter(hints[_fname])
                _to_rich = _build_to_rich_converter(hints[_fname])
                if _to_prim is not None:
                    self._field_prim_convs[_fname] = _to_prim
                if _to_rich is not None:
                    self._field_rich_convs[_fname] = _to_rich
        self._has_map_fields: bool = any(is_map_in_dtype_tree(f.type) for f in struct_fields)

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
                for pa_field in struct_fields
            ])
        )

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
                prim = self._rich_to_prim(default)
                self._primitive_default = prim
                self._pyarrow_default = pa.array([prim], type=self._pa_struct_type)
        else:
            self._has_default = False
            self._primitive_default = ...
            self._rich_default_val = None
            self._pyarrow_default = ...

    # ── columnar PyArrow helpers ──────────────────────────────────────────────

    def _to_pyarrow_flat_from_dicts(self, dicts: list) -> "pa.StructArray":
        """Convert a flat list of dicts → pa.StructArray (columnar).

        Used by both :meth:`from_primitive_to_pyarrow` and :meth:`from_rich_to_pyarrow`
        (TypedDict rich values are already dicts, so both paths share this helper).
        """
        if not dicts:
            return pa.array([], type=self._pa_struct_type)
        if not self._struct_fields_list:
            return pa.array(dicts, type=self._pa_struct_type)
        arrays: list = []
        for pa_field in self._struct_fields_list:
            fname = pa_field.name
            col = [None if d is None else d.get(fname) for d in dicts]
            if fname in self._sub_td_converters:
                arrays.append(self._sub_td_converters[fname]._to_pyarrow_flat_from_dicts(col))
            elif fname in self._field_prim_convs:
                prim_conv = self._field_prim_convs[fname]
                arrays.append(pa.array([None if x is None else prim_conv(x) for x in col], type=pa_field.type))
            else:
                arrays.append(pa.array(col, type=pa_field.type))
        if any(d is None for d in dicts):
            null_mask = pa.array([d is None for d in dicts])
            return pa.StructArray.from_arrays(arrays, fields=self._struct_fields_list, mask=null_mask)
        return pa.StructArray.from_arrays(arrays, fields=self._struct_fields_list)

    def _from_pyarrow_flat(self, struct_arr: "pa.StructArray") -> list:
        """Convert a pa.StructArray → list of plain dicts (columnar).

        Null struct rows (validity bit False) are returned as ``None``.
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
            if fname in self._sub_td_converters:
                field_data.append(self._sub_td_converters[fname]._from_pyarrow_flat(col))
            elif fname in self._field_rich_convs:
                rich_conv = self._field_rich_convs[fname]
                field_data.append([rich_conv(x) for x in col.to_pylist()])
            elif is_map_in_dtype_tree(pa_field.type):
                field_data.append([coerce_map_pylist_to_dict(x, pa_field.type) for x in col.to_pylist()])
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
        return self._td_class

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
        if value is ...:
            return True
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
            return self._null_prim
        return self._rich_to_prim(value)

    def from_primitive_to_rich(self, value: "dict | None") -> Any:
        if value is ...:
            return ...
        if value is None:
            # TypedDict is a plain dict at runtime: SimpleDict(x=None, y=None) == {"x": None, "y": None}.
            # GenericFeatureConverter expands None to the all-null dict rather than returning None,
            # so we match that behaviour here.
            return self._null_prim
        return self._prim_to_rich(value)

    # ── primitive ↔ pyarrow ───────────────────────────────────────────────────

    def from_pyarrow_to_primitive(self, values: "pa.Array | pa.ChunkedArray") -> "Sequence[dict | None]":
        if not self._has_map_fields:
            return values.to_pylist()
        if isinstance(values, pa.ChunkedArray):
            values = values.combine_chunks()
        result: list[dict | None] = []
        for row in values.to_pylist():
            if row is None:
                result.append(None)
            else:
                fixed: dict[str, Any] = {}
                for pa_field in self._struct_fields_list:
                    v = row[pa_field.name]
                    fixed[pa_field.name] = coerce_map_pylist_to_dict(v, pa_field.type) if is_map_in_dtype_tree(pa_field.type) else v
                result.append(fixed)
        return result

    def from_primitive_to_pyarrow(self, values: "Iterable[dict | None]") -> "pa.Array | pa.ChunkedArray":
        values_list = [None if v is ... else v for v in values]
        if self._field_prim_convs or self._sub_td_converters:
            return self._to_pyarrow_flat_from_dicts(values_list)
        return pa.array(values_list, type=self._pa_struct_type)

    def from_pyarrow_to_rich(self, values: "pa.Array | pa.ChunkedArray", /) -> "Sequence[Any]":
        if isinstance(values, pa.ChunkedArray):
            values = values.combine_chunks()
        # Fast path: no per-field conversions needed.  TypedDict is plain dict at runtime,
        # so to_pylist() already returns the correct type — no constructor call needed.
        if not self._field_rich_convs and not self._sub_td_converters and not self._has_map_fields:
            if values.null_count == 0:
                return values.to_pylist()
            _null = self._null_prim
            return [_null if v is None else v for v in values.to_pylist()]
        return self._from_pyarrow_flat(values)

    def from_rich_to_pyarrow(
        self,
        values: "Sequence[Any | ellipsis | None]",
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        feature_name: str | None = None,
    ) -> "pa.Array | pa.ChunkedArray":
        converted: list = []
        for v in values:
            if v is ...:
                result = self._handle_missing(v, missing_value_strategy)
                # When _handle_missing returns ... (allow / default_or_allow with no default),
                # the value is still missing — produce a null struct row (None), not a valid
                # struct with null fields. This matches GenericFeatureConverter semantics.
                converted.append(None if result is ... else cast(Any, result))
            elif v is None:
                converted.append(self._null_prim)
            else:
                converted.append(self._rich_to_prim(v))
        if self._field_prim_convs or self._sub_td_converters:
            return self._to_pyarrow_flat_from_dicts(converted)
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
            return unstructure_primitive_to_json(value, encode_structs_as_objects=True)
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
