from __future__ import annotations

from io import BytesIO
from typing import (
    Any,
    ClassVar,
    Dict,
    Iterable,
    Sequence,
    Tuple,
    cast,
)

import pyarrow as pa
import pyarrow.feather as pf

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.json import (
    FeatureEncodingOptions,
    structs_as_objects_feature_json_converter,
    structure_json_to_primitive,
)
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.pyarrow import (
    coerce_map_pylist_to_dict,
    pyarrow_to_polars,
    pyarrow_to_primitive,
    rich_to_pyarrow,
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

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportMissingSuperCall=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false


def _dict_to_pa_map_list(d: Any, dtype: pa.DataType) -> Any:
    """Recursively convert a Python dict to PyArrow map-compatible list-of-dicts.

    PyArrow map arrays require ``[{"key": k, "value": v}, ...]`` format rather
    than plain Python dicts.  Handles nested maps, lists, and structs.

    Also accepts list-of-tuples (the format returned by ``pa.MapScalar.as_py()``),
    which is what ``PrimitiveFeatureConverter.primitive_default`` returns after a
    PyArrow round-trip.  This lets ``from_rich_to_pyarrow`` work correctly when the
    missing-value path returns a ``primitive_default`` in that format.
    """
    if d is None:
        return None
    if isinstance(dtype, pa.MapType):
        if isinstance(d, list):
            # list-of-(key, value) tuples — the .as_py() format for pa.MapScalar
            return [{"key": k, "value": _dict_to_pa_map_list(v, dtype.item_type)} for k, v in d]
        if not isinstance(d, dict):
            raise TypeError(f"Expected a `dict` but got: {type(d).__name__}")
        return [{"key": k, "value": _dict_to_pa_map_list(v, dtype.item_type)} for k, v in d.items()]
    if isinstance(dtype, (pa.ListType, pa.LargeListType, pa.FixedSizeListType)):
        return [_dict_to_pa_map_list(x, dtype.value_type) for x in d]
    if isinstance(dtype, pa.StructType):
        if not isinstance(d, dict):
            raise TypeError(f"Expected a `dict` but got: {type(d).__name__}")
        res: dict[str, Any] = {}
        for k, v in d.items():
            field_idx = dtype.get_field_index(k)
            if field_idx == -1:
                raise ValueError(f"Struct type does not have a field named '{k}'")
            res[k] = _dict_to_pa_map_list(v, dtype.field(field_idx).type)
        return res
    return d


class DictFeatureConverter(FeatureConverter["dict[str, Any]", "dict[str, Any]"]):
    """Feature converter for ``Dict[K, V]`` types stored as ``pa.map_``.

    Rich type:      ``Dict[K, V]``  (e.g. ``Dict[str, int]``, ``Dict[str, MyDC]``)
    Primitive type: ``Dict[K, V_prim]``  (values converted to primitive form)
    PyArrow type:   ``pa.map_(key_type, value_type)``

    Use :meth:`new` to obtain a (possibly cached) instance.
    """

    _cache: ClassVar[Dict[Tuple[Any, Any, bool, "pa.MapType | None"], "DictFeatureConverter"]] = {}

    @classmethod
    def new(
        cls,
        rich_type: type,
        default: "dict | None | ellipsis",
        is_nullable: bool,
        name: str = "",
        value_converter: "FeatureConverter | None" = None,
        pyarrow_dtype: "pa.MapType | None" = None,
    ) -> "DictFeatureConverter":
        """Factory with caching for simple defaults (``None`` / ``...``)."""
        if default is None or default is ...:
            key = (rich_type, default, is_nullable, pyarrow_dtype)
            cached = cls._cache.get(key)
            if cached is not None:
                return cached
            inst = cls.__new__(cls)
            inst._init(rich_type, default, is_nullable, name=name, value_converter=value_converter, pyarrow_dtype=pyarrow_dtype)
            cls._cache[key] = inst
            return inst
        inst = cls.__new__(cls)
        inst._init(rich_type, default, is_nullable, name=name, value_converter=value_converter, pyarrow_dtype=pyarrow_dtype)
        return inst

    def _init(
        self,
        rich_type: type,
        default: "dict | None | ellipsis",
        is_nullable: bool,
        name: str = "",
        value_converter: "FeatureConverter | None" = None,
        pyarrow_dtype: "pa.MapType | None" = None,
    ) -> None:
        super().__init__()
        self._rich_type = rich_type
        self._is_nullable = is_nullable

        # Prefer the explicitly-supplied dtype (which preserves caller-specified
        # field nullability) over the type derived from the Python annotation.
        self._pa_map_type: pa.MapType = pyarrow_dtype if pyarrow_dtype is not None else cast(pa.MapType, rich_to_pyarrow(rich_type, name or "f"))
        self._primitive_type = pyarrow_to_primitive(self._pa_map_type, name or "")

        # Build value-level element closures (mirrors ListFeatureConverter.__init__).
        if value_converter is None:
            from ._factory import make_feature_converter as _make_fc
            from typing_extensions import get_args as _get_args
            _vargs = _get_args(rich_type)
            _value_rich_type: Any = _vargs[1] if len(_vargs) == 2 else ...
            value_converter = _make_fc(
                name=None,
                is_nullable=True,
                rich_type=_value_rich_type,
                pyarrow_dtype=self._pa_map_type.item_type,
            )
        self._value_conv = value_converter
        if isinstance(value_converter, DataclassFeatureConverter):
            self._val_to_prim: Any = value_converter._rich_to_prim
            self._val_to_rich: Any = value_converter._prim_to_rich
        elif not value_converter.has_nontrivial_rich_type():
            # Fast path: for scalar converters, extract _coerce_fn directly and wrap
            # with a single None check.  This avoids the three guard branches in
            # from_rich_to_primitive (value is ..., value is None check, etc.) while
            # still coercing mismatched Python types (e.g. str "0" → int 0).
            # _scalar_coerce_fn is too narrow (datetime-like only); here we cover all
            # _ScalarConverterBase subclasses (str, int, float, bool, datetime, …).
            if isinstance(value_converter, _ScalarConverterBase):
                _val_coerce_fn = type(value_converter)._coerce_fn
                self._val_to_prim = lambda x, _c=_val_coerce_fn: None if x is None else _c(x)
            else:
                coerce = _scalar_coerce_fn(value_converter)
                self._val_to_prim = coerce if coerce is not None else value_converter.from_rich_to_primitive
            self._val_to_rich = _identity
        else:
            self._val_to_prim = value_converter.from_rich_to_primitive
            self._val_to_rich = value_converter.from_primitive_to_rich

        # Build key-level coercion closure so that _to_primitive normalises both keys
        # and values.  This mirrors what GenericFeatureConverter does via
        # structure_primitive_to_rich — e.g. int keys → str for map<large_string, V>.
        from ._factory import make_feature_converter as _make_fc
        from typing_extensions import get_args as _get_args
        _kargs = _get_args(rich_type)
        _key_rich_type: Any = _kargs[0] if len(_kargs) >= 1 else ...
        _key_elem_conv = _make_fc(
            name=None,
            is_nullable=False,
            rich_type=_key_rich_type,
            pyarrow_dtype=self._pa_map_type.key_type,
        )
        # Fast path for scalar key converters: use _coerce_fn directly (no None check
        # needed — map keys are always non-nullable).  Covers str, int, float, bool,
        # datetime, … without going through from_rich_to_primitive's guard branches.
        if isinstance(_key_elem_conv, _ScalarConverterBase):
            self._key_to_prim: Any = type(_key_elem_conv)._coerce_fn
        else:
            self._key_to_prim: Any = _key_elem_conv.from_rich_to_primitive

        # Derive protobuf ArrowTypes directly from the key/value converters, mirroring
        # ListFeatureConverter which uses item_converter.protobuf_dtype rather than
        # importing pa_scalar_to_proto.
        _key_conv = _make_fc(
            name=None,
            is_nullable=False,
            rich_type=...,
            pyarrow_dtype=self._pa_map_type.key_type,
        )
        _key_arrow_proto: pb.ArrowType = _key_conv.protobuf_dtype
        _item_arrow_proto: pb.ArrowType = value_converter.protobuf_dtype
        self._null_proto: pb.ArrowType = pb.ArrowType(
            map=pb.Map(
                key_field=pb.Field(
                    name=self._pa_map_type.key_field.name,
                    nullable=self._pa_map_type.key_field.nullable,
                    arrow_type=_key_arrow_proto,
                ),
                item_field=pb.Field(
                    name=self._pa_map_type.item_field.name,
                    nullable=self._pa_map_type.item_field.nullable,
                    arrow_type=_item_arrow_proto,
                ),
                keys_sorted=False,
            )
        )
        # Schema for feather serialisation inside protobuf round-trips.
        # The backing storage of a pa.MapArray is a StructArray of key/value pairs.
        # Build directly from the already-computed ArrowTypes — no scalar roundtrip needed.
        self._pb_schema: pb.Schema = pb.Schema(
            columns=[pb.Field(
                nullable=False,
                arrow_type=pb.ArrowType(struct=pb.Struct(sub_field_types=[
                    pb.Field(
                        name=self._pa_map_type.key_field.name,
                        nullable=self._pa_map_type.key_field.nullable,
                        arrow_type=_key_arrow_proto,
                    ),
                    pb.Field(
                        name=self._pa_map_type.item_field.name,
                        nullable=self._pa_map_type.item_field.nullable,
                        arrow_type=_item_arrow_proto,
                    ),
                ])),
            )]
        )

        if is_nullable and default is ...:
            default = None
        # Declare before branching so Pyright sees the attribute in every path.
        self._primitive_default: Any
        self._pyarrow_default: "ellipsis | pa.Array | pa.ChunkedArray"
        if default is not ...:
            self._has_default = True
            self._rich_default_val: "dict | None" = cast("dict | None", default)
            if default is None:
                self._primitive_default = None
                self._pyarrow_default = pa.array(
                    [None], type=self._pa_map_type
                )
            else:
                prim = self._to_primitive(default)
                self._primitive_default = prim
                self._pyarrow_default = pa.array(
                    [_dict_to_pa_map_list(prim, self._pa_map_type)], type=self._pa_map_type
                )
        else:
            self._has_default = False
            self._primitive_default = ...
            self._rich_default_val = None
            self._pyarrow_default = ...

    # ── helpers ───────────────────────────────────────────────────────────────

    def _to_primitive(self, value: "dict | list") -> "dict | list":
        """Convert a rich map value to its primitive form.

        Accepts both ``dict`` and list-of-``(key, value)`` tuples (the format
        returned by ``pa.MapArray.to_pylist()``).  Both key and value are
        coerced to the declared primitive types so that downstream PyArrow
        construction never sees unexpected Python types (e.g. ``int`` keys
        when the map type is ``map<large_string, V>``).
        """
        key_conv = self._key_to_prim
        val_conv = self._val_to_prim
        if isinstance(value, list):
            # list-of-(key, value) tuples from PyArrow .to_pylist()
            return [(key_conv(k), val_conv(v)) for k, v in value]
        return {key_conv(k): val_conv(v) for k, v in value.items()}

    def _to_rich(self, value: "dict | list") -> dict:
        """Apply value-level rich conversion to a non-None primitive dict.

        Accepts both ``dict`` and list-of-``(key, value)`` tuples — the format
        returned by ``pa.MapArray.to_pylist()`` and used by callers such as
        ``AnonymousStructConverter`` that call ``col.to_pylist()`` directly then
        feed the result to ``from_primitive_to_rich``.
        """
        conv = self._val_to_rich
        if isinstance(value, list):
            return {k: conv(v) for k, v in value}
        return {k: conv(v) for k, v in value.items()}

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

    # ── properties ────────────────────────────────────────────────────────────

    @property
    def rich_type(self) -> type:
        return self._rich_type

    @property
    def primitive_type(self) -> type:
        return self._primitive_type

    @property
    def pyarrow_dtype(self) -> pa.DataType:
        return self._pa_map_type

    @property
    def protobuf_dtype(self) -> pb.ArrowType:
        return self._null_proto

    @property
    def polars_dtype(self) -> Any:
        return pyarrow_to_polars(self._pa_map_type)

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
        if self._primitive_default is None:
            return None
        # GenericFeatureConverter (via PrimitiveFeatureConverter) stores the primitive default
        # as a PyArrow array and retrieves it via .as_py().  For map scalars, .as_py() returns
        # a list-of-tuples (e.g. [('x', 0)]) rather than a plain Python dict.  We match that
        # counterintuitive behavior here so callers see a consistent format regardless of which
        # converter produced the value.
        pa_default = self._pyarrow_default
        assert isinstance(pa_default, (pa.Array, pa.ChunkedArray)), f"Expected pa.Array or pa.ChunkedArray, got {type(pa_default)}"
        return cast("dict | None", cast(pa.Array, pa_default)[0].as_py())

    @property
    def rich_default(self) -> "dict | None":
        if not self._has_default:
            raise ValueError("No default value specified")
        return self._rich_default_val

    def has_nontrivial_rich_type(self) -> bool:
        # Mirrors GenericFeatureConverter: compare (optionally Optional-wrapped) primitive_type
        # against rich_type.  For Dict[str, int] non-nullable both are Dict[str, int] → False.
        # For nullable, the primitive is wrapped in Optional, which differs from the raw rich
        # type → True.  For Dict[str, Dataclass], primitive_type is Dict[str, ChalkStructType]
        # which differs from Dict[str, Dataclass] → True.
        import typing as _typing
        prim = self._primitive_type
        if self._is_nullable:
            prim = _typing.Optional[prim]
        return prim != self._rich_type

    def is_value_missing(self, value: Any) -> bool:
        if value is ...:
            return True
        if value is None:
            return not self._is_nullable
        return False

    def is_rich_valid(self, value: Any) -> bool:
        try:
            self.from_rich_to_primitive(value, "default_or_error")
            return True
        except (TypeError, ValueError):
            return False

    # ── rich ↔ primitive ──────────────────────────────────────────────────────

    def from_rich_to_primitive(
        self,
        value: "dict | None | ellipsis",
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> "dict | None":
        if value is ... or (value is None and not self._is_nullable):
            return cast("dict | None", self._handle_missing(value, missing_value_strategy))
        if value is None:
            return None
        return self._to_primitive(value)

    def from_primitive_to_rich(self, value: "dict | None") -> "dict | None":
        if value is None or value is ...:
            return cast("dict | None", value)
        return self._to_rich(value)

    # ── primitive ↔ pyarrow ───────────────────────────────────────────────────

    def from_pyarrow_to_primitive(self, values: "pa.Array | pa.ChunkedArray") -> "Sequence[dict | None]":
        return [
            None if v is None else coerce_map_pylist_to_dict(v, self._pa_map_type)
            for v in values.to_pylist()
        ]

    def from_primitive_to_pyarrow(self, values: "Iterable[dict | None]") -> "pa.Array | pa.ChunkedArray":
        converted = [
            None if v is None or v is ...
            else _dict_to_pa_map_list(v, self._pa_map_type)
            for v in values
        ]
        return pa.array(converted, type=self._pa_map_type)

    def from_pyarrow_to_rich(self, values: "pa.Array | pa.ChunkedArray", /) -> "Sequence[dict | None]":
        return [
            None if v is None else self._to_rich(v)
            for v in self.from_pyarrow_to_primitive(values)
        ]

    def from_rich_to_pyarrow(
        self,
        values: "Sequence[dict | None | ellipsis]",
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        feature_name: "str | None" = None,
    ) -> "pa.Array | pa.ChunkedArray":
        converted: list = []
        for v in values:
            if v is ... or (v is None and not self._is_nullable):
                result = self._handle_missing(v, missing_value_strategy)
                if result is ... or result is None:
                    converted.append(None)
                else:
                    converted.append(_dict_to_pa_map_list(cast(dict, result), self._pa_map_type))
            elif v is None:
                converted.append(None)
            else:
                # _to_primitive handles both dict and list-of-tuples inputs and
                # coerces both keys and values to the declared primitive types.
                prim = self._to_primitive(v)
                converted.append(_dict_to_pa_map_list(prim, self._pa_map_type))
        return pa.array(converted, type=self._pa_map_type)

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
        # Map types are always serialised as objects (not lists), regardless of options.
        return structs_as_objects_feature_json_converter.unstructure_primitive_to_json(value)

    def from_json_to_primitive(self, value: "TJSON | dict | None") -> "dict | None":
        if value is None:
            return None
        try:
            return cast(dict, structure_json_to_primitive(value, self._primitive_type))
        except (ValueError, TypeError) as e:
            raise TypeError(f"Could not convert '{value}' to `{self._primitive_type}`: {e}") from e

    def from_json_to_rich(self, value: TJSON) -> "dict | None":
        if value is None:
            return None
        prim = self.from_json_to_primitive(value)
        if prim is None:
            return None
        return self._to_rich(prim)

    def from_rich_to_json(
        self,
        value: "dict | None | ellipsis",
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        prim = self.from_rich_to_primitive(value, missing_value_strategy)
        return self.from_primitive_to_json(cast("dict | None", prim), options=options)

    # ── protobuf ↔ * ──────────────────────────────────────────────────────────

    def from_rich_to_protobuf(
        self,
        value: "dict | None | ellipsis",
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
        values = value.values  # backing StructArray of [{"key": k, "value": v}, ...]
        table = pa.Table.from_arrays([values], names=["values"])
        buf = BytesIO()
        pf.write_feather(table, dest=buf, compression=None)
        return pb.ScalarValue(
            map_value=pb.ScalarListValue(arrow_data=buf.getvalue(), schema=self._pb_schema)
        )

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=self._pa_map_type)[0]
        value = pb_value.map_value
        arr = pf.read_table(BytesIO(value.arrow_data)).column(0).combine_chunks()
        return pa.scalar(arr.to_pylist(), self._pa_map_type)
