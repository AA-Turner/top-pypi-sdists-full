from __future__ import annotations

import dataclasses as _dataclasses
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
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
    FeatureConverter,
    MissingValueError,
    _raise_unsupported_missing_value_strategy,
)

from ._struct_coerce import _build_to_primitive_converter, _build_to_rich_converter

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportMissingSuperCall=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false, reportImplicitStringConcatenation=false


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
            if isinstance(v, dict):
                return {f: v.get(f) for f in field_names}
            if isinstance(v, (list, tuple)):
                return dict(zip(field_names, v))
            return {f: getattr(v, f, None) for f in field_names}

        return _convert_flat
    else:

        def _convert_nested(v: Any) -> Any:
            if v is None:
                return {f: sub[f](None) if f in sub else None for f in field_names}
            if isinstance(v, dict):
                return {f: sub[f](v.get(f)) if f in sub else v.get(f) for f in field_names}
            if isinstance(v, (list, tuple)):
                raw = dict(zip(field_names, v))
                return {f: sub[f](raw.get(f)) if f in sub else raw.get(f) for f in field_names}
            return {f: sub[f](getattr(v, f, None)) if f in sub else getattr(v, f, None) for f in field_names}

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
    FeatureConverter["dict[str, Any]", Any],
):
    """Full :class:`FeatureConverter` for a single dataclass (struct) element.

    Rich type:      T (a dataclass)
    Primitive type: dict[str, Any]
    PyArrow type:   pa.struct([...])

    Also serves as the ``item_converter`` for :class:`ListConverter`.  Use
    :meth:`for_class` to get a cached instance suitable for that purpose.
    """

    _cache: ClassVar[Dict[Tuple[type, Any, bool, pa.DataType | None], "DataclassFeatureConverter"]] = {}

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
        field_converters: "Dict[str, FeatureConverter] | None" = None,
        pa_struct_type: "pa.DataType | None" = None,
    ) -> "DataclassFeatureConverter":
        """Factory with caching for simple defaults (``None`` / ``...``).

        Parameters
        ----------
        pa_struct_type:
            When provided, used as the PyArrow struct type directly instead of
            recomputing it from type hints. Required for generic dataclasses
            (e.g. ``HttpResponse[bytes]``) where type hints contain unresolved
            TypeVars.
        """
        if default is None or default is ...:
            key = (dc_class, default, is_nullable, pa_struct_type)
            cached = cls._cache.get(key)
            if cached is not None:
                return cached
            if field_converters is None:
                from ._factory import make_field_converters_for_dataclass as _make_field_converters
                field_converters = _make_field_converters(dc_class)
            inst = cls(dc_class, default, is_nullable, field_converters=field_converters, pa_struct_type=pa_struct_type, _from_new=_FROM_NEW)
            cls._cache[key] = inst
            return inst
        if field_converters is None:
            from ._factory import make_field_converters_for_dataclass as _make_field_converters
            field_converters = _make_field_converters(dc_class)
        return cls(dc_class, default, is_nullable, field_converters=field_converters, pa_struct_type=pa_struct_type, _from_new=_FROM_NEW)

    def __init__(
        self,
        dc_class: type,
        default: "Any | ellipsis",
        is_nullable: bool,
        *,
        field_converters: "Dict[str, FeatureConverter]",
        pa_struct_type: "pa.DataType | None" = None,
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
        if pa_struct_type is not None:
            # Caller provided the struct type directly (e.g. for generic aliases like
            # HttpResponse[bytes] where type hints contain unresolved TypeVars).
            assert isinstance(pa_struct_type, pa.StructType), f"Expected pa.StructType, got {type(pa_struct_type)}"
            struct_fields = [pa_struct_type.field(i) for i in range(pa_struct_type.num_fields)]
            self._pa_struct_type: pa.DataType = pa_struct_type
        else:
            struct_fields = [pa.field(name, rich_to_pyarrow(hints[name], name, in_struct=True)) for name in field_names]
            self._pa_struct_type: pa.DataType = pa.struct(struct_fields)
        self._primitive_type = pyarrow_to_primitive(self._pa_struct_type, "")
        self._rich_to_prim: Callable[[Any], Any] = _build_dc_to_dict(dc_class)
        self._prim_to_rich: Callable[[Any], Any] = _build_dict_to_dc(dc_class)
        # Null primitive: a dict with every field set to None — used when a None rich value
        # is received.  GenericFeatureConverter converts None to this form for struct types
        # (None is never "missing" for structs), and we must match that behaviour.
        self._null_prim: dict = self._rich_to_prim(None)

        # Columnar PyArrow path: per-field sub-converters used by _to_pyarrow_flat /
        # _from_pyarrow_flat to avoid building intermediate Python dicts per element.
        self._field_names = field_names
        self._struct_fields_list = struct_fields  # list[pa.Field] in field order
        self._field_converters: Dict[str, FeatureConverter] = field_converters
        self._sub_dc_converters: Dict[str, "DataclassFeatureConverter"] = {
            k: v for k, v in field_converters.items() if isinstance(v, DataclassFeatureConverter)
        }
        self._field_prim_convs: Dict[str, Callable[[Any], Any]] = {}
        self._field_rich_convs: Dict[str, Callable[[Any], Any]] = {}
        for _fname in field_names:
            _inner_t = unwrap_optional_and_annotated_if_needed(hints[_fname])
            if not (_dataclasses.is_dataclass(_inner_t) and isinstance(_inner_t, type)):
                _to_prim = _build_to_primitive_converter(hints[_fname])
                _to_rich = _build_to_rich_converter(hints[_fname])
                if _to_prim is not None:
                    self._field_prim_convs[_fname] = _to_prim
                if _to_rich is not None:
                    self._field_rich_convs[_fname] = _to_rich
        self._has_map_fields: bool = any(is_map_in_dtype_tree(f.type) for f in struct_fields)

        # Precompute proto arrow types for each field by serializing a null scalar.
        # Used by from_pyarrow_to_protobuf to build pb.Field descriptors without
        # importing _primitive_converter.py.
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

    def _to_pyarrow_flat_from_dicts(self, dicts: list) -> "pa.StructArray":
        """Convert a flat list of primitive dicts → pa.StructArray (columnar).

        Used by :meth:`from_primitive_to_pyarrow` when there are fields that
        need per-value coercion (e.g. ISO strings or ``date`` objects stored in a
        ``datetime`` field).  Fields with no coercion entry still take the fast
        ``pa.array(col, type=…)`` path so only affected columns pay extra cost.

        ``None`` entries produce null struct rows (validity bit False), matching
        the behaviour of ``pa.array([None], type=struct_type)``.
        """
        if not dicts:
            return pa.array([], type=self._pa_struct_type)
        if not self._struct_fields_list:
            return pa.array(dicts, type=self._pa_struct_type)
        arrays: list = []
        for pa_field in self._struct_fields_list:
            fname = pa_field.name
            col = [None if d is None else (d.get(fname) if isinstance(d, dict) else d[fname]) for d in dicts]
            if fname in self._sub_dc_converters:
                arrays.append(self._sub_dc_converters[fname]._to_pyarrow_flat_from_dicts(col))
            elif fname in self._field_prim_convs and not pa.types.is_struct(pa_field.type):
                # For struct-typed fields the col is already in primitive (dict/None) form;
                # applying prim_conv would expand None to an all-null dict and lose the
                # null validity bit.  Use the fast pa.array path for structs.
                prim_conv = self._field_prim_convs[fname]
                arrays.append(pa.array([None if x is None else prim_conv(x) for x in col], type=pa_field.type))
            else:
                arrays.append(pa.array(col, type=pa_field.type))
        # None dicts → null struct rows (validity bit False); non-None dicts with null
        # field values → valid struct rows whose fields happen to be null.
        if any(d is None for d in dicts):
            null_mask = pa.array([d is None for d in dicts])
            return pa.StructArray.from_arrays(arrays, fields=self._struct_fields_list, mask=null_mask)
        return pa.StructArray.from_arrays(arrays, fields=self._struct_fields_list)

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
            elif is_map_in_dtype_tree(pa_field.type):
                field_data.append([coerce_map_pylist_to_dict(x, pa_field.type) for x in col.to_pylist()])
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
        if self._is_nullable:
            return Optional[self._dc_class]  # type: ignore[return-value]
        return self._dc_class

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
        return self._rich_to_prim(value)

    def from_primitive_to_rich(self, value: "dict | None") -> Any:
        if value is None or value is ...:
            return cast(Any, value)
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
        # Use the columnar path only when there are fields that need coercion;
        # otherwise fall through to the fast single-call pa.array() C++ path.
        if self._field_prim_convs or self._sub_dc_converters:
            return self._to_pyarrow_flat_from_dicts(values_list)
        return pa.array(values_list, type=self._pa_struct_type)

    def from_pyarrow_to_rich(self, values: "pa.Array | pa.ChunkedArray", /) -> "Sequence[Any]":
        if isinstance(values, pa.ChunkedArray):
            values = values.combine_chunks()
        # Use the full columnar path when field conversions are needed.
        if self._has_map_fields or self._field_rich_convs or self._sub_dc_converters:
            return self._from_pyarrow_flat(values)
        # Fast columnar path: extract per-field lists directly, avoiding the per-row
        # Python dict that struct to_pylist() would materialise for each row.
        n = len(values)
        if n == 0:
            return []
        dc = self._dc_class
        field_names = [f.name for f in self._struct_fields_list]
        cols = [values.field(name).to_pylist() for name in field_names]
        if values.null_count > 0:
            # Null struct rows → dc(None, None, ...) to match existing row-based semantics.
            valid = values.is_valid().to_pylist()
            _null_dc = dc(*([None] * len(field_names)))
            return [_null_dc if not valid[i] else dc(*[col[i] for col in cols]) for i in range(n)]
        return [dc(*row) for row in zip(*cols)]

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
                converted.append(self._null_prim if result is ... else cast(Any, result))
            elif v is None:
                # None → all-null struct dict, matching GenericFeatureConverter semantics.
                converted.append(self._null_prim)
            else:
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
