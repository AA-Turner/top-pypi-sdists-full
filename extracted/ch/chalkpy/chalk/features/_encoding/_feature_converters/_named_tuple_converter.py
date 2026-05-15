from __future__ import annotations

import typing
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
    pyarrow_to_polars,
    pyarrow_to_primitive,
    rich_to_pyarrow,
)
from chalk.utils.collections import is_namedtuple, unwrap_optional_and_annotated_if_needed
from chalk.utils.json import TJSON

from ._base import (
    _DEFAULT_FEATURE_ENCODING_OPTIONS,
    _FROM_NEW,
    FeatureConverter,
    MissingValueError,
    _raise_unsupported_missing_value_strategy,
)
from ._dataclass_converter import (
    DataclassFeatureConverter,
    _build_to_primitive_converter,
    _build_to_rich_converter,
    _build_dc_to_dict,
    _build_dict_to_dc,
)

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportMissingSuperCall=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false

import dataclasses as _dataclasses


def _build_nt_to_dict(nt_class: type) -> Callable[[Any], Any]:
    """Build a converter from a NamedTuple instance to a plain dict.

    Handles nested NamedTuples, nested dataclasses, and list/scalar fields
    the same way _build_dc_to_dict does for dataclasses.
    """
    field_names: tuple[str, ...] = nt_class._fields
    hints = typing.get_type_hints(nt_class)

    sub: dict[str, Callable] = {}
    for name in field_names:
        inner = unwrap_optional_and_annotated_if_needed(hints[name])
        if is_namedtuple(inner):
            sub[name] = _build_nt_to_dict(inner)
        elif _dataclasses.is_dataclass(inner) and isinstance(inner, type):
            sub[name] = _build_dc_to_dict(inner)
        else:
            conv = _build_to_primitive_converter(hints[name])
            if conv is not None:
                sub[name] = conv

    null_prim: dict = {f: None for f in field_names}

    def _convert(v: Any) -> Any:
        if v is None:
            return null_prim
        if v is ...:
            return v
        if isinstance(v, dict):
            return {f: sub[f](v.get(f)) if f in sub else v.get(f) for f in field_names}
        # NamedTuple or any object with attribute access
        return {f: sub[f](getattr(v, f)) if f in sub else getattr(v, f) for f in field_names}

    return _convert


def _build_dict_to_nt(nt_class: type) -> Callable[[Any], Any]:
    """Build a converter from a plain dict (or list/tuple) back to a NamedTuple instance.

    Also handles list/array input (the JSON array form of NamedTuples).
    """
    field_names: tuple[str, ...] = nt_class._fields
    hints = typing.get_type_hints(nt_class)

    sub: dict[str, Callable] = {}
    for name in field_names:
        inner = unwrap_optional_and_annotated_if_needed(hints[name])
        if is_namedtuple(inner):
            sub[name] = _build_dict_to_nt(inner)
        elif _dataclasses.is_dataclass(inner) and isinstance(inner, type):
            sub[name] = _build_dict_to_dc(inner)
        else:
            conv = _build_to_rich_converter(hints[name])
            if conv is not None:
                sub[name] = conv

    def _reconstruct(d: Any) -> Any:
        if d is None:
            return nt_class(*[None] * len(field_names))
        if isinstance(d, nt_class):
            return d
        if isinstance(d, dict):
            return nt_class(**{f: sub[f](d.get(f)) if f in sub else d.get(f) for f in field_names})
        # list/tuple (JSON array form)
        return nt_class(**{f: sub[f](v) if f in sub else v for f, v in zip(field_names, d)})

    return _reconstruct


class NamedTupleFeatureConverter(FeatureConverter["dict[str, Any]", Any]):
    """Full :class:`FeatureConverter` for a single NamedTuple (struct) element.

    Rich type:      T (a NamedTuple)
    Primitive type: dict[str, Any]
    PyArrow type:   pa.struct([...])

    Use :meth:`new` to obtain a (possibly cached) instance.
    """

    _cache: ClassVar[Dict[Tuple[type, Any, bool], "NamedTupleFeatureConverter"]] = {}

    @classmethod
    def new(
        cls,
        nt_class: type,
        default: "Any | ellipsis",
        is_nullable: bool,
        name: str = "",
        field_converters: "Dict[str, FeatureConverter] | None" = None,
    ) -> "NamedTupleFeatureConverter":
        """Factory with caching for simple defaults (``None`` / ``...``)."""
        if default is None or default is ...:
            key = (nt_class, default, is_nullable)
            cached = cls._cache.get(key)
            if cached is not None:
                return cached
            if field_converters is None:
                from ._factory import make_field_converters_for_namedtuple as _make_fc
                field_converters = _make_fc(nt_class)
            inst = cls(nt_class, default, is_nullable, name=name, field_converters=field_converters, _from_new=_FROM_NEW)
            cls._cache[key] = inst
            return inst
        if field_converters is None:
            from ._factory import make_field_converters_for_namedtuple as _make_fc
            field_converters = _make_fc(nt_class)
        return cls(nt_class, default, is_nullable, name=name, field_converters=field_converters, _from_new=_FROM_NEW)

    def __init__(
        self,
        nt_class: type,
        default: "Any | ellipsis",
        is_nullable: bool,
        *,
        name: str = "",
        field_converters: "Dict[str, FeatureConverter]",
        _from_new: object = None,
    ) -> None:
        super().__init__()
        if _from_new is not _FROM_NEW:
            raise TypeError("Use NamedTupleFeatureConverter.new() instead of calling the constructor directly")

        self._nt_class = nt_class
        self._is_nullable = is_nullable

        field_names: tuple[str, ...] = nt_class._fields
        hints = typing.get_type_hints(nt_class)

        struct_fields = [pa.field(n, rich_to_pyarrow(hints[n], n, in_struct=True)) for n in field_names]
        self._pa_struct_type: pa.DataType = pa.struct(struct_fields)
        self._primitive_type = pyarrow_to_primitive(self._pa_struct_type, "")
        self._rich_to_prim: Callable[[Any], Any] = _build_nt_to_dict(nt_class)
        self._prim_to_rich: Callable[[Any], Any] = _build_dict_to_nt(nt_class)
        self._null_prim: dict = {n: None for n in field_names}

        self._field_names = field_names
        self._struct_fields_list = struct_fields
        self._field_converters: Dict[str, FeatureConverter] = field_converters

        # Sub-converters for nested struct types used in the columnar PyArrow path.
        self._sub_nt_converters: Dict[str, "NamedTupleFeatureConverter"] = {
            k: v for k, v in field_converters.items() if isinstance(v, NamedTupleFeatureConverter)
        }
        self._sub_dc_converters: Dict[str, "DataclassFeatureConverter"] = {
            k: v for k, v in field_converters.items() if isinstance(v, DataclassFeatureConverter)
        }

        # Precompute proto field arrow types.
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

    def _get_field(self, inst: Any, fname: str) -> Any:
        """Access a field from a NamedTuple, dict, or list."""
        if isinstance(inst, dict):
            return inst[fname]
        return getattr(inst, fname)

    # ── properties ───────────────────────────────────────────────────────────

    @property
    def rich_type(self) -> type:
        return self._nt_class

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
            return cast(Any, value)
        return self._prim_to_rich(value)

    # ── primitive ↔ pyarrow ───────────────────────────────────────────────────

    def from_pyarrow_to_primitive(self, values: "pa.Array | pa.ChunkedArray") -> "Sequence[dict | None]":
        return values.to_pylist()

    def from_primitive_to_pyarrow(self, values: "Iterable[dict | None]") -> "pa.Array | pa.ChunkedArray":
        values_list = [None if v is ... else v for v in values]
        return pa.array(values_list, type=self._pa_struct_type)

    def from_pyarrow_to_rich(self, values: "pa.Array | pa.ChunkedArray", /) -> "Sequence[Any]":
        return [self._prim_to_rich(v) for v in values.to_pylist()]

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
                converted.append(self._null_prim if result is ... else cast(Any, result))
            elif v is None:
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
        return unstructure_primitive_to_json(value)

    def from_json_to_primitive(self, value: "TJSON | dict | None") -> "dict | None":
        if value is None:
            return self._null_prim
        try:
            return cast(dict, structure_json_to_primitive(value, self._primitive_type))
        except (ValueError, TypeError) as e:
            raise TypeError(f"Could not convert '{value}' to `{self._primitive_type}`: {e}") from e

    def from_json_to_rich(self, value: TJSON) -> Any:
        prim = self.from_json_to_primitive(value)
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
