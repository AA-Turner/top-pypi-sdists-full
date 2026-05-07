from __future__ import annotations

import enum as _enum_module
from typing import (
    Any,
    ClassVar,
    Iterable,
    Sequence,
    Type,
    Union,
    cast,
)

import pyarrow as pa
import pyarrow.compute as pc

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.primitive import TPrimitive
from chalk.features._encoding.pyarrow import pyarrow_to_polars
from chalk.utils.json import TJSON

from ._base import (
    _DEFAULT_FEATURE_ENCODING_OPTIONS,
    _FROM_NEW,
    FeatureConverter,
    MissingValueError,
    _raise_unsupported_missing_value_strategy,
    _unwrap_scalar_value,
)

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false, reportMissingSuperCall=false

def _make_coerce_to_enum(enum_class: type) -> "Any":
    """Return a closure that converts a value/key/member to an enum member.

    Resolution order (value-first, matching the generic converter):
      1. Already an instance of enum_class → return as-is.
      2. enum_class(val)  — lookup by value.
      3. enum_class(val_type(val)) — coerce to the enum's value type first
         (handles e.g. str "1" → int 1 → AccountTypeInt(1) for non-IntEnum
         enums with integer values whose primitives are stored as strings).
      4. enum_class[val]  — lookup by key name (only if val is a str).
    """
    ec = cast("type[_enum_module.Enum]", enum_class)
    _members = list(ec)
    _val_type: "type | None" = type(_members[0].value) if _members else None

    def _coerce(val: Any) -> Any:
        if isinstance(val, enum_class):
            return val
        try:
            return enum_class(val)
        except (ValueError, KeyError, TypeError):
            pass
        # If the value is not already the enum's value type, coerce it first.
        # This handles primitives that have been round-tripped through PyArrow —
        # e.g. AccountTypeInt stores primitives as str("1"), so when "1" arrives
        # as a rich input, enum_class(int("1")) recovers the correct member.
        if _val_type is not None and not isinstance(val, _val_type):
            try:
                return enum_class(_val_type(val))
            except (ValueError, KeyError, TypeError):
                pass
        if isinstance(val, str):
            try:
                return cast("type[_enum_module.Enum]", enum_class)[val]
            except KeyError:
                pass
        raise TypeError(
            f"Cannot convert {val!r} to {ec.__name__}. "
            + f"Valid values: {[m.value for m in ec]}, "
            + f"valid keys: {[m.name for m in ec]}"
        )
    return _coerce


class EnumFeatureConverter(FeatureConverter):
    """Specialized converter for Python :class:`enum.Enum` subclasses.

    Supports:
    - ``enum.Enum`` with string values  → ``pa.large_utf8()`` primitive
    - ``enum.IntEnum`` / int-mixin enums → ``pa.int64()`` primitive

    Rich inputs accept enum members, value literals, or key name strings.
    """

    _cache: ClassVar[dict] = {}

    # ── Construction ──────────────────────────────────────────────────────────

    @classmethod
    def new(
        cls,
        enum_class: type,
        default: Any = ...,
        is_nullable: bool = False,
    ) -> "EnumFeatureConverter":
        if is_nullable and default is ...:
            default = None
        key = (enum_class, default, is_nullable)
        cached = cls._cache.get(key)
        if cached is not None:
            return cached
        inst = cls(enum_class, default, is_nullable, _from_new=_FROM_NEW)
        cls._cache[key] = inst
        return inst

    def __init__(
        self,
        enum_class: type,
        default: Any = ...,
        is_nullable: bool = False,
        *,
        _from_new: object = None,
    ) -> None:
        if _from_new is not _FROM_NEW:
            raise TypeError(f"Use {type(self).__name__}.new() instead of calling the constructor directly")

        self._enum_class = enum_class
        self._is_nullable = is_nullable

        # ── Determine primitive type ──────────────────────────────────────────
        # Use the actual value type of the enum members rather than just checking
        # isinstance(int). This means plain enum.Enum with integer values (e.g.
        # AccountTypeInt) uses pa.int64() just like IntEnum, avoiding unnecessary
        # string coercions and round-trip impedance mismatches.
        from chalk.utils.enum import get_enum_value_type as _get_enum_value_type
        from chalk.features._encoding.pyarrow import rich_to_pyarrow as _rich_to_pyarrow
        try:
            _val_type = _get_enum_value_type(cast("type[_enum_module.Enum]", enum_class))
        except ValueError:
            _val_type = str  # empty enum — fall back to string
        self._pa_type: pa.DataType = _rich_to_pyarrow(_val_type, "")
        self._prim_type: type = _val_type

        if issubclass(_val_type, int):
            from ._int_converter import Int64FeatureConverter
            self._scalar_conv = Int64FeatureConverter.new(default=..., is_nullable=is_nullable)
        elif issubclass(_val_type, float):
            from ._float_converter import Float64FeatureConverter
            self._scalar_conv = Float64FeatureConverter.new(default=..., is_nullable=is_nullable)
        else:
            from ._string_converter import LargeStringFeatureConverter
            self._scalar_conv = LargeStringFeatureConverter.new(default=..., is_nullable=is_nullable)

        # ── Lookup table: primitive value → enum member ───────────────────────
        ec2 = cast("type[_enum_module.Enum]", enum_class)
        self._prim_to_enum: dict = {m.value: m for m in ec2}

        # ── Coerce closures ───────────────────────────────────────────────────
        self._coerce_to_enum = _make_coerce_to_enum(enum_class)
        _coerce_to_enum = self._coerce_to_enum

        _prim_type = self._prim_type

        def _coerce_to_prim(val: Any) -> Any:
            return _prim_type(_coerce_to_enum(val).value)

        self._coerce_to_prim = _coerce_to_prim

        # ── Default handling ──────────────────────────────────────────────────
        if default is ...:
            self._has_default = False
            self._primitive_default: Any = ...
            self._rich_default_val: Any = ...
            self._pyarrow_default: "ellipsis | pa.Array" = ...
        else:
            self._has_default = True
            if default is None:
                self._primitive_default = None
                self._rich_default_val = None
                self._pyarrow_default = pa.array([None], type=self._pa_type)
            else:
                rich_default = _coerce_to_enum(default)
                prim_default = rich_default.value
                self._primitive_default = prim_default
                self._rich_default_val = rich_default
                self._pyarrow_default = pa.array([prim_default], type=self._pa_type)

    # ── Properties ────────────────────────────────────────────────────────────

    @property
    def rich_type(self) -> type:
        if self._is_nullable:
            from typing import Optional as _Optional
            return _Optional[self._enum_class]  # type: ignore[return-value]
        return self._enum_class

    @property
    def primitive_type(self) -> Type[TPrimitive]:
        return cast(Type[TPrimitive], self._prim_type)

    @property
    def pyarrow_dtype(self) -> pa.DataType:
        return self._pa_type

    @property
    def protobuf_dtype(self) -> pb.ArrowType:
        return self._scalar_conv.protobuf_dtype

    @property
    def polars_dtype(self) -> Any:
        return pyarrow_to_polars(self._pa_type)

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
    def primitive_default(self) -> Any:
        if self._primitive_default is ...:
            raise ValueError("No default value specified")
        return self._primitive_default

    @property
    def rich_default(self) -> Any:
        if self._rich_default_val is ...:
            raise ValueError("No default value specified")
        return self._rich_default_val

    @property
    def encoder(self) -> Any:
        return None

    @property
    def decoder(self) -> Any:
        return None

    def has_nontrivial_rich_type(self) -> bool:
        return True

    # ── Validity / missing ────────────────────────────────────────────────────

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
        value: Any,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> Any:
        if value is ... or (value is None and not self._is_nullable):
            if missing_value_strategy == "allow":
                return value
            if missing_value_strategy == "default_or_allow":
                return self.primitive_default if self._has_default else value
            if missing_value_strategy == "default_or_error":
                if self._has_default:
                    return self.primitive_default
                raise TypeError("The value is missing, and this feature has no default value.")
            if missing_value_strategy == "error":
                raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
            _raise_unsupported_missing_value_strategy(missing_value_strategy)
        if value is None:
            return None
        return self._coerce_to_prim(value)

    def from_primitive_to_rich(self, value: Any) -> Any:
        if value is None:
            return cast(Any, None)
        # Fast path: O(1) dict lookup for the common case where value is already
        # the correct primitive type (e.g. int for IntEnum, str for str-valued Enum).
        member = self._prim_to_enum.get(value)
        if member is not None:
            return member
        # Slow path: coerce value to the enum's value type first
        # (e.g. stored "1" → int("1") → AccountTypeInt(1)).
        ec = cast("type[_enum_module.Enum]", self._enum_class)
        try:
            return ec(self._prim_type(value))
        except (ValueError, KeyError, TypeError):
            return ec(value)

    # ── rich ↔ JSON ───────────────────────────────────────────────────────────

    def from_rich_to_json(
        self,
        value: Any,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        if value is ... or (value is None and not self._is_nullable):
            if missing_value_strategy == "allow":
                return cast(TJSON, value)
            if missing_value_strategy == "default_or_allow":
                return cast(TJSON, self.primitive_default if self._has_default else value)
            if missing_value_strategy == "default_or_error":
                if self._has_default:
                    return cast(TJSON, self.primitive_default)
                raise TypeError("The value is missing, and this feature has no default value.")
            if missing_value_strategy == "error":
                raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
            _raise_unsupported_missing_value_strategy(missing_value_strategy)
        if value is None:
            return None
        return cast(TJSON, self._coerce_to_prim(value))

    def from_json_to_primitive(self, value: Any) -> Any:
        if value is None or value is ...:
            return None
        # JSON value is already the primitive (string or int)
        return self._prim_type(value)

    def from_json_to_rich(self, value: Any) -> Any:
        if value is None or value is ...:
            return cast(Any, None)
        return self.from_primitive_to_rich(self._prim_type(value))

    def from_primitive_to_json(
        self,
        value: Any,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        return cast(TJSON, value)

    # ── rich ↔ pyarrow ────────────────────────────────────────────────────────

    def from_rich_to_pyarrow(
        self,
        values: "Sequence[Any]",
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        feature_name: "str | None" = None,
    ) -> "Union[pa.Array, pa.ChunkedArray]":
        pa_type = self._pa_type
        _prim_default = self._primitive_default
        _coerce = self._coerce_to_prim
        has_default = self._has_default
        is_nullable = self._is_nullable

        try:
            if missing_value_strategy == "allow":
                return pa.array(
                    [None if x is ... else (None if x is None else _coerce(x)) for x in values],
                    type=pa_type,
                )
            if missing_value_strategy == "default_or_allow":
                if not has_default:
                    return pa.array(
                        [None if x is ... else (None if x is None else _coerce(x)) for x in values],
                        type=pa_type,
                    )
                if is_nullable:
                    return pa.array(
                        [_prim_default if x is ... else (None if x is None else _coerce(x)) for x in values],
                        type=pa_type,
                    )
                return cast(
                    "Union[pa.Array, pa.ChunkedArray]",
                    pc.fill_null(
                        pa.array([None if x is ... else (None if x is None else _coerce(x)) for x in values], type=pa_type),
                        pa.scalar(_prim_default, type=pa_type),
                    ),
                )
            if missing_value_strategy == "default_or_error":
                if has_default:
                    if is_nullable:
                        return pa.array(
                            [_prim_default if x is ... else (None if x is None else _coerce(x)) for x in values],
                            type=pa_type,
                        )
                    return cast(
                        "Union[pa.Array, pa.ChunkedArray]",
                        pc.fill_null(
                            pa.array([None if x is ... else (None if x is None else _coerce(x)) for x in values], type=pa_type),
                            pa.scalar(_prim_default, type=pa_type),
                        ),
                    )
                pa_values: list[Any] = []
                for x in values:
                    if x is ... or (x is None and not is_nullable):
                        raise MissingValueError("The value is missing, and this feature has no default value.")
                    pa_values.append(None if x is None else _coerce(x))
                return pa.array(pa_values, type=pa_type)
            if missing_value_strategy == "error":
                pa_values = []
                for x in values:
                    if x is ... or (x is None and not is_nullable):
                        raise MissingValueError(
                            "The value is missing, but `replace_missing_with_defaults` was set to `False`."
                        )
                    pa_values.append(None if x is None else _coerce(x))
                return pa.array(pa_values, type=pa_type)
            _raise_unsupported_missing_value_strategy(missing_value_strategy)
        except (TypeError, ValueError) as e:
            for val in values:
                if val is None or val is ...:
                    continue
                try:
                    _coerce(val)
                except (TypeError, ValueError) as scan_e:
                    feature_part = f" for feature '{feature_name}'" if feature_name is not None else ""
                    raise TypeError(
                        f"Could not convert '{val}' to `{self.rich_type}`{feature_part}: {scan_e}"
                    ) from scan_e
            if not isinstance(e, MissingValueError):
                feature_part = f" for feature '{feature_name}'" if feature_name is not None else ""
                raise TypeError(f"Could not convert a value to `{self.rich_type}`{feature_part}: {e}") from e
            raise

    def from_pyarrow_to_rich(self, values: "pa.Array | pa.ChunkedArray", /) -> list:
        # Use the precomputed dict for O(1) lookup per element — avoids per-call
        # overhead of from_primitive_to_rich's slow-path fallback logic.
        _lookup = self._prim_to_enum
        return [None if x is None else _lookup[x] for x in values.to_pylist()]

    # ── primitive ↔ pyarrow ───────────────────────────────────────────────────

    def from_pyarrow_to_primitive(self, values: "Union[pa.Array, pa.ChunkedArray]") -> list:
        return values.to_pylist()

    def from_primitive_to_pyarrow(self, values: "Iterable[Any]") -> "Union[pa.Array, pa.ChunkedArray]":
        _pa_type = self._pa_type
        _coerce = self._coerce_to_prim
        if isinstance(values, (list, tuple)):
            try:
                return pa.array(values, type=_pa_type)
            except (TypeError, pa.ArrowTypeError):
                pass
        else:
            values = list(values)
        return pa.array(
            [None if v is None or v is ... else _coerce(v) for v in values],
            type=_pa_type,
        )

    # ── pyarrow ↔ JSON ────────────────────────────────────────────────────────

    def from_pyarrow_to_json(
        self,
        values: "pa.Array | pa.ChunkedArray",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> "Sequence[TJSON]":
        return values.to_pylist()

    def from_json_to_pyarrow(self, values: "Sequence[TJSON]") -> "Union[pa.Array, pa.ChunkedArray]":
        _prim_type = self._prim_type
        return pa.array(
            [None if x is None or x is ... else _prim_type(x) for x in values],
            type=self._pa_type,
        )

    # ── Protobuf (delegated to underlying scalar converter) ───────────────────

    def from_primitive_to_protobuf(self, value: Any) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        return self._scalar_conv.from_primitive_to_protobuf(scalar_value)

    def from_rich_to_protobuf(
        self,
        value: Any,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = self.from_rich_to_primitive(value, missing_value_strategy)
        return self._scalar_conv.from_primitive_to_protobuf(prim)

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        return self._scalar_conv.from_pyarrow_to_protobuf(value)

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        return self._scalar_conv.from_protobuf_to_pyarrow(pb_value)
