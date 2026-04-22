from __future__ import annotations

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
from chalk.utils.pydanticutil.pydantic_compat import construct_pydantic_model as _pydantic_construct
from chalk.utils.json import TJSON
from chalk.utils.missing_dependency import missing_dependency_exception

from ._base import (
    _DEFAULT_FEATURE_ENCODING_OPTIONS,
    _FROM_NEW,
    FeatureConverter,
    MissingValueError,
    _raise_unsupported_missing_value_strategy,
)

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportMissingSuperCall=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false, reportImplicitStringConcatenation=false

try:
    from pydantic import BaseModel
except ImportError:
    BaseModel = None  # type: ignore[assignment, misc]

try:
    from pydantic.v1 import BaseModel as V1BaseModel
except ImportError:
    V1BaseModel = None  # type: ignore[assignment, misc]


def _is_pydantic_model(typ: Any) -> bool:
    if not isinstance(typ, type):
        return False
    try:
        if BaseModel is not None and issubclass(typ, BaseModel):
            return True
        if V1BaseModel is not None and issubclass(typ, V1BaseModel):
            return True
    except TypeError:
        # On Python 3.10, generic aliases like list[X] satisfy isinstance(x, type)
        # but raise TypeError in issubclass() via pydantic's __subclasscheck__.
        pass
    return False


def _get_field_names(model_class: type) -> tuple[str, ...]:
    # model_fields is Pydantic v2; __fields__ is Pydantic v1.
    fields = getattr(model_class, "model_fields", None) or getattr(model_class, "__fields__", {})
    return tuple(fields.keys())


from ._struct_coerce import _build_to_primitive_converter, _build_to_rich_converter


def _build_model_to_dict(model_class: type) -> "Callable[[Any], Any]":
    field_names: tuple[str, ...] = _get_field_names(model_class)
    hints = _typing_mod.get_type_hints(model_class)

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
            return {f: getattr(v, f, None) for f in field_names}

        return _convert_flat
    else:

        def _convert_nested(v: Any) -> Any:
            if v is None:
                return {f: sub[f](None) if f in sub else None for f in field_names}
            if isinstance(v, dict):
                return {f: sub[f](v.get(f)) if f in sub else v.get(f) for f in field_names}
            return {f: sub[f](getattr(v, f, None)) if f in sub else getattr(v, f, None) for f in field_names}

        return _convert_nested


def _build_dict_to_model(model_class: type) -> "Callable[[Any], Any]":
    field_names: tuple[str, ...] = _get_field_names(model_class)
    hints = _typing_mod.get_type_hints(model_class)

    sub: dict[str, Callable] = {
        name: conv for name in field_names if (conv := _build_to_rich_converter(hints[name])) is not None
    }

    null_kwargs = {f: None for f in field_names}

    if not sub:

        def _reconstruct_flat(d: Any) -> Any:
            if isinstance(d, model_class):
                return d
            return _pydantic_construct(model_class, **(null_kwargs if d is None else d))

        return _reconstruct_flat
    else:

        def _reconstruct_nested(d: Any) -> Any:
            if isinstance(d, model_class):
                return d
            if d is None:
                return _pydantic_construct(model_class, **{f: sub[f](None) if f in sub else None for f in field_names})
            converted = {f: sub[f](d[f]) if f in sub else d[f] for f in field_names}
            return _pydantic_construct(model_class, **converted)

        return _reconstruct_nested


class PydanticFeatureConverter(
    FeatureConverter["dict[str, Any]", Any],
):
    """Full :class:`FeatureConverter` for a single Pydantic BaseModel (struct) element.

    Rich type:      T (a Pydantic BaseModel subclass)
    Primitive type: dict[str, Any]
    PyArrow type:   pa.struct([...])

    Also serves as the ``item_converter`` for :class:`ListConverter`.  Use
    :meth:`for_class` to get a cached instance suitable for that purpose.
    """

    _cache: ClassVar[Dict[Tuple[type, Any, bool], "PydanticFeatureConverter"]] = {}

    @classmethod
    def for_class(cls, model_class: type) -> "PydanticFeatureConverter":
        return cls.new(model_class, ..., is_nullable=True)

    @classmethod
    def new(
        cls,
        model_class: type,
        default: "Any | ellipsis",
        is_nullable: bool,
        field_converters: "Dict[str, FeatureConverter] | None" = None,
        name: str = "",
    ) -> "PydanticFeatureConverter":
        if BaseModel is None:
            raise missing_dependency_exception("pydantic")
        if default is None or default is ...:
            key = (model_class, default, is_nullable)
            cached = cls._cache.get(key)
            if cached is not None:
                return cached
            if field_converters is None:
                from ._factory import make_field_converters_for_pydantic as _make_field_converters
                field_converters = _make_field_converters(model_class)
            inst = cls(model_class, default, is_nullable, field_converters=field_converters, name=name, _from_new=_FROM_NEW)
            cls._cache[key] = inst
            return inst
        if field_converters is None:
            from ._factory import make_field_converters_for_pydantic as _make_field_converters
            field_converters = _make_field_converters(model_class)
        return cls(model_class, default, is_nullable, field_converters=field_converters, name=name, _from_new=_FROM_NEW)

    def __init__(
        self,
        model_class: type,
        default: "Any | ellipsis",
        is_nullable: bool,
        *,
        field_converters: "Dict[str, FeatureConverter] | None" = None,
        name: str = "",
        _from_new: object = None,
    ) -> None:
        super().__init__()
        if _from_new is not _FROM_NEW:
            raise TypeError("Use PydanticFeatureConverter.new() or PydanticFeatureConverter.for_class() instead")
        assert field_converters is not None, "field_converters must be provided via PydanticFeatureConverter.new()"
        self._model_class = model_class
        self._is_nullable = is_nullable

        field_names: tuple[str, ...] = _get_field_names(model_class)
        hints = _typing_mod.get_type_hints(model_class)
        struct_fields = [pa.field(name, rich_to_pyarrow(hints[name], name, in_struct=True)) for name in field_names]
        self._pa_struct_type: pa.DataType = pa.struct(struct_fields)
        self._primitive_type = pyarrow_to_primitive(self._pa_struct_type, name)
        self._rich_to_prim: Callable[[Any], Any] = _build_model_to_dict(model_class)
        self._prim_to_rich: Callable[[Any], Any] = _build_dict_to_model(model_class)
        self._null_prim: dict = self._rich_to_prim(None)

        self._field_names = field_names
        self._struct_fields_list = struct_fields
        self._field_converters: Dict[str, FeatureConverter] = field_converters
        self._sub_model_converters: Dict[str, "PydanticFeatureConverter"] = {
            k: v for k, v in field_converters.items() if isinstance(v, PydanticFeatureConverter)
        }
        self._field_prim_convs: Dict[str, Callable[[Any], Any]] = {}
        self._field_rich_convs: Dict[str, Callable[[Any], Any]] = {}
        for _fname in field_names:
            _inner_t = unwrap_optional_and_annotated_if_needed(hints[_fname])
            if not _is_pydantic_model(_inner_t):
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
        if not dicts:
            return pa.array([], type=self._pa_struct_type)
        if not self._struct_fields_list:
            return pa.array(dicts, type=self._pa_struct_type)
        arrays: list = []
        for pa_field in self._struct_fields_list:
            fname = pa_field.name
            col = [None if d is None else (d.get(fname) if isinstance(d, dict) else d[fname]) for d in dicts]
            if fname in self._sub_model_converters:
                arrays.append(self._sub_model_converters[fname]._to_pyarrow_flat_from_dicts(col))
            elif fname in self._field_prim_convs and not pa.types.is_struct(pa_field.type):
                # For struct-typed fields the col is already in primitive (dict/None) form;
                # applying prim_conv would expand None to an all-null dict and lose the
                # null validity bit.  Use the fast pa.array path for structs.
                prim_conv = self._field_prim_convs[fname]
                arrays.append(pa.array([None if x is None else prim_conv(x) for x in col], type=pa_field.type))
            else:
                arrays.append(pa.array(col, type=pa_field.type))
        if any(d is None for d in dicts):
            null_mask = pa.array([d is None for d in dicts])
            return pa.StructArray.from_arrays(arrays, fields=self._struct_fields_list, mask=null_mask)
        return pa.StructArray.from_arrays(arrays, fields=self._struct_fields_list)

    def _to_pyarrow_flat(self, instances: list) -> "pa.StructArray":
        if not instances:
            return pa.array([], type=self._pa_struct_type)
        arrays: list = []
        for pa_field in self._struct_fields_list:
            fname = pa_field.name
            col = [None if inst is None else getattr(inst, fname) for inst in instances]
            if fname in self._sub_model_converters:
                arrays.append(self._sub_model_converters[fname]._to_pyarrow_flat(col))
            elif fname in self._field_prim_convs:
                prim_conv = self._field_prim_convs[fname]
                arrays.append(pa.array([None if x is None else prim_conv(x) for x in col], type=pa_field.type))
            else:
                arrays.append(pa.array(col, type=pa_field.type))
        return pa.StructArray.from_arrays(arrays, fields=self._struct_fields_list)

    def _from_pyarrow_flat(self, struct_arr: "pa.StructArray") -> list:
        n = len(struct_arr)
        if n == 0:
            return []
        valid = struct_arr.is_valid().to_pylist()
        has_nulls = not all(valid)
        field_data: list[list] = []
        for pa_field in self._struct_fields_list:
            fname = pa_field.name
            col = struct_arr.field(fname)
            if fname in self._sub_model_converters:
                field_data.append(self._sub_model_converters[fname]._from_pyarrow_flat(col))
            elif fname in self._field_rich_convs:
                rich_conv = self._field_rich_convs[fname]
                field_data.append([rich_conv(x) for x in col.to_pylist()])
            elif is_map_in_dtype_tree(pa_field.type):
                field_data.append([coerce_map_pylist_to_dict(x, pa_field.type) for x in col.to_pylist()])
            else:
                field_data.append(col.to_pylist())
        mc = self._model_class
        n_fields = len(field_data)
        field_names = self._field_names
        if has_nulls:
            return [
                None if not valid[i]
                else _pydantic_construct(mc, **{field_names[fi]: field_data[fi][i] for fi in range(n_fields)})
                for i in range(n)
            ]
        return [_pydantic_construct(mc, **{field_names[fi]: field_data[fi][i] for fi in range(n_fields)}) for i in range(n)]

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
        return self._model_class

    @property
    def primitive_type(self) -> type:
        return self._primitive_type

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
        if self._field_prim_convs or self._sub_model_converters:
            return self._to_pyarrow_flat_from_dicts(values_list)
        return pa.array(values_list, type=self._pa_struct_type)

    def from_pyarrow_to_rich(self, values: "pa.Array | pa.ChunkedArray", /) -> "Sequence[Any]":
        if isinstance(values, pa.ChunkedArray):
            values = values.combine_chunks()
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
                converted.append(None if result is ... else cast(Any, result))
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
