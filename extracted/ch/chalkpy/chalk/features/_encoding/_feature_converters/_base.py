from __future__ import annotations

from datetime import datetime, date, time, timedelta
from typing import (
    Any,
    Callable,
    ClassVar,
    Generic,
    Iterable,
    NoReturn,
    Protocol,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from typing_extensions import Self

import pyarrow as pa
import pyarrow.compute as pc

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.json import (
    FeatureEncodingOptions,
)
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.primitive import TPrimitive
from chalk.utils.json import TJSON
from chalk.utils.log_with_context import get_logger

# pyright: reportPrivateUsage=false, reportUnusedFunction=false, reportUnusedClass=false, reportIncompatibleMethodOverride=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false


_logger = get_logger(__name__)

_pl_module: Any = None


def _lazy_polars() -> Any:
    """Import and cache Polars only when a converter needs its dtype."""
    global _pl_module
    if _pl_module is None:
        try:
            import polars as pl

            _pl_module = pl
        except ImportError:
            pass
    return _pl_module


_TRich = TypeVar("_TRich")
_TRichCo = TypeVar("_TRichCo", covariant=True)
_TRichCon = TypeVar("_TRichCon", contravariant=True)

_TPrim = TypeVar("_TPrim", bound=TPrimitive)
_TPrimCo = TypeVar("_TPrimCo", bound=TPrimitive, covariant=True)
_TPrimCon = TypeVar("_TPrimCon", bound=TPrimitive, contravariant=True)
_TScalar = TypeVar("_TScalar", bound=TPrimitive)

_DEFAULT_FEATURE_ENCODING_OPTIONS = FeatureEncodingOptions()


_FROM_NEW = object()

_UNSUPPORTED_MISSING_VALUE_STRATEGY_MESSAGE = (
    "It must be one of 'allow', 'default_or_allow', 'default_or_error', or 'error'."
)


def _identity(v: Any) -> Any:
    return v


def _raise_unsupported_missing_value_strategy(missing_value_strategy: MissingValueStrategy) -> NoReturn:
    raise ValueError(
        f"Unsupported missing value strategy: {missing_value_strategy}. {_UNSUPPORTED_MISSING_VALUE_STRATEGY_MESSAGE}"
    )


def _unwrap_scalar_value(value: Any) -> Any:
    if isinstance(value, pa.Scalar):
        return value.as_py()
    return value


class MissingValueError(TypeError):
    """Raised when a missing value is encountered and the missing value strategy is set to ``error``."""

    pass


# Forward-declared Protocol — TEncoder/TDecoder are defined in generic_converter.py.
# We import them lazily where needed to avoid circular imports.


class FeatureConverter(Protocol[_TPrim, _TRich]):
    @property
    def rich_type(self) -> Type[_TRich]: ...

    @property
    def primitive_type(self) -> Type[TPrimitive]: ...

    @property
    def pyarrow_dtype(self) -> pa.DataType: ...

    @property
    def protobuf_dtype(self) -> pb.ArrowType: ...

    @property
    def polars_dtype(self) -> Any: ...

    @property
    def is_nullable(self) -> bool: ...

    @property
    def has_default(self) -> bool: ...

    @property
    def pyarrow_default(self) -> ellipsis | pa.Array | pa.ChunkedArray: ...

    @property
    def primitive_default(self) -> _TPrim: ...

    @property
    def rich_default(self) -> _TRich: ...

    def has_nontrivial_rich_type(self) -> bool: ...

    @property
    def encoder(self) -> Any: ...

    @property
    def decoder(self) -> Any: ...

    def from_pyarrow_to_json(
        self,
        values: pa.Array | pa.ChunkedArray,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> Sequence[TJSON]: ...

    def from_pyarrow_to_primitive(self, values: Union[pa.Array, pa.ChunkedArray]) -> Sequence[_TPrim]: ...

    def from_primitive_to_pyarrow(self, value: Iterable[_TPrim]) -> Union[pa.Array, pa.ChunkedArray]: ...

    def from_primitive_to_json(
        self,
        value: TPrimitive,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON: ...

    def from_json_to_pyarrow(self, values: Sequence[TJSON]) -> Union[pa.Array, pa.ChunkedArray]: ...

    def from_json_to_primitive(self, value: TJSON | TPrimitive) -> _TPrim: ...

    def is_value_missing(self, value: Any) -> bool: ...

    def from_primitive_to_protobuf(self, value: _TPrim) -> pb.ScalarValue: ...

    def is_rich_valid(self, value: _TRich) -> bool: ...

    def from_rich_to_pyarrow(
        self,
        values: Sequence[_TRich | ellipsis | None],
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        feature_name: str | None = None,
    ) -> Union[pa.Array, pa.ChunkedArray]: ...

    def from_rich_to_protobuf(
        self,
        value: _TRich | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue: ...

    def from_rich_to_primitive(
        self,
        value: _TRich | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> _TPrim: ...

    def from_rich_to_json(
        self,
        value: _TRich | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON: ...

    def from_pyarrow_to_rich(self, values: pa.Array | pa.ChunkedArray, /) -> Sequence[_TRich]: ...

    def from_primitive_to_rich(self, value: _TPrim | _TRich) -> _TRich: ...

    def from_json_to_rich(self, value: TJSON) -> _TRich: ...

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar: ...

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue: ...


class _ScalarConverterBase(Generic[_TPrim, _TRich]):
    """Base class for all scalar (non-composite) feature converters.

    Provides caching and construction via ``new()``/``__init__``, typed properties, and
    default implementations of every ``from_*_to_*`` conversion method, driven by three
    ClassVar callables that subclasses configure:

    **Required**:

    - ``_coerce_fn`` — converts a rich value to its primitive form (use ``staticmethod``).
      Raises ``TypeError`` for unsupported input types.

    **Optional overrides**:

    - ``_arrow_coerce_fn`` — used instead of ``_coerce_fn`` in ``from_rich_to_pyarrow``.
      Override only when the Arrow path can accept a cheaper representation (e.g.
      ``BytesFeatureConverter`` returns a ``memoryview`` rather than ``bytes`` to avoid a
      copy).
    - ``_json_coerce_fn`` — used instead of ``_coerce_fn`` in ``from_json_to_*``. Override
      when JSON inputs should be coerced differently from rich inputs (e.g.
      ``DateFeatureConverter`` uses ``_coerce_date_from_json``, which silently truncates a
      ``datetime``'s time component, whereas ``_coerce_date`` raises on non-zero time).

    All three are class-level (not bound methods) so hot loops can hoist them into locals
    with zero per-element method-dispatch overhead.

    **Overriding conversion methods**: subclasses that need custom logic for a specific
    path (e.g. ``BoolFeatureConverter.from_json_to_pyarrow``) simply override that method;
    all other paths continue to use the defaults here.

    **Composite converters** (``ListFeatureConverter``, ``DataclassFeatureConverter``) do
    *not* inherit from this class — they have fundamentally different construction, caching,
    and type semantics.
    """

    _rich_type_value: ClassVar[Type[Any]]
    _primitive_type_value: ClassVar[Type[Any]]
    _pyarrow_dtype_value: ClassVar[pa.DataType]
    _proto_arrow_type: ClassVar[pb.ArrowType]
    _polars_dtype_value: ClassVar[Any]
    _cache: ClassVar[dict]  # populated per-subclass by __init_subclass__

    _coerce_fn: ClassVar[Callable[[Any], Any]]
    _arrow_coerce_fn: ClassVar[Callable[[Any], Any]] = None  # type: ignore[assignment]
    _json_coerce_fn: ClassVar[Callable[[Any], Any]] = None  # type: ignore[assignment]
    _use_fast_path: ClassVar[bool] = True

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls._cache = {}
        if hasattr(cls, "_coerce_fn"):
            if cls._arrow_coerce_fn is None:
                cls._arrow_coerce_fn = cls._coerce_fn
            if cls._json_coerce_fn is None:
                cls._json_coerce_fn = cls._coerce_fn

    @classmethod
    def new(cls, default: Any, is_nullable: bool) -> Self:
        pa_type = cls._pyarrow_dtype_value
        key = (default, is_nullable, pa_type)
        cached = cls._cache.get(key)
        if cached is not None:
            return cached
        inst = cls(default, is_nullable, pa_type=pa_type, _from_new=_FROM_NEW)  # type: ignore[call-arg]
        cls._cache[key] = inst
        return inst

    def __init__(self, default: Any, is_nullable: bool, *, pa_type: "pa.DataType | None" = None, _from_new: object = None) -> None:
        super().__init__()
        cls = type(self)
        self._coerce: Callable[[Any], Any] = cls._coerce_fn
        self._arrow_coerce: Callable[[Any], Any] = cls._arrow_coerce_fn
        self._json_coerce: Callable[[Any], Any] = cls._json_coerce_fn
        if _from_new is not _FROM_NEW:
            raise TypeError(f"Use {type(self).__name__}.new() instead of calling the constructor directly")
        if pa_type is None:
            pa_type = type(self)._pyarrow_dtype_value
        self._is_nullable = is_nullable
        if is_nullable and default is ...:
            default = None
        if default is not ...:
            self._has_default = True
            _pa_default = pa.array(
                [None if default is None else self._arrow_coerce(default)],
                type=pa_type,
            )
            self._pyarrow_default: "ellipsis | pa.Array | pa.ChunkedArray" = _pa_default
            self._primitive_default: Any = _pa_default.to_pylist()[0]
        else:
            self._has_default = False
            self._primitive_default = ...
            self._pyarrow_default = ...

    @property
    def rich_type(self) -> Type[_TRich]:
        t = cast(Type[_TRich], type(self)._rich_type_value)
        if self._is_nullable:
            from typing import Optional as _Optional

            return _Optional[t]  # type: ignore[return-value]
        return t

    @property
    def primitive_type(self) -> Type[TPrimitive]:
        return cast(Type[TPrimitive], type(self)._primitive_type_value)

    @property
    def pyarrow_dtype(self) -> pa.DataType:
        return type(self)._pyarrow_dtype_value

    @property
    def protobuf_dtype(self) -> "pb.ArrowType":
        return type(self)._proto_arrow_type

    @property
    def polars_dtype(self) -> Any:
        val = type(self)._polars_dtype_value
        if val is None:
            pl = _lazy_polars()
            if pl is not None:
                from chalk.features._encoding.pyarrow import pyarrow_to_polars

                val = pyarrow_to_polars(type(self)._pyarrow_dtype_value, "")
                type(self)._polars_dtype_value = val
        return val

    @property
    def encoder(self) -> Any:
        return None

    @property
    def decoder(self) -> Any:
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
    def primitive_default(self) -> _TPrim:
        if self._primitive_default is ...:
            raise ValueError("No default value specified")
        return cast(_TPrim, self._primitive_default)

    @property
    def rich_default(self) -> _TRich:
        return cast(_TRich, self.primitive_default)

    def _serialize_to_json(self, x: Any) -> TJSON:
        return cast(TJSON, x)

    def has_nontrivial_rich_type(self) -> bool:
        return False

    def is_value_missing(self, value: Any) -> bool:
        if value is ...:
            return True
        if value is None:
            return not self._is_nullable
        return False

    def is_rich_valid(self, value: Any) -> bool:
        try:
            pa.scalar(self.from_rich_to_primitive(value, "default_or_error"), type=self.pyarrow_dtype)
            return True
        except (TypeError, ValueError):
            return False

    def from_rich_to_pyarrow(
        self,
        values: Iterable[Any],
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        feature_name: str | None = None,
    ) -> Union[pa.Array, pa.ChunkedArray]:
        pa_type = self.pyarrow_dtype
        _prim_default = self._primitive_default

        # ── Fast path ────────────────────────────────────────────────────────
        # Most callers supply values that are already the correct Python type
        # with no Ellipsis sentinels.  Skip the Python-level coercion loop and
        # let PyArrow build the array in C.  Temporal converters opt out via
        # _use_fast_path=False because PyArrow silently accepts ints for those
        # types (e.g. 42 → timedelta(microseconds=42)), diverging from _coerce_fn.
        if type(self)._use_fast_path and isinstance(values, (list, tuple)):
            try:
                arr = pa.array(values, type=pa_type)
            except (TypeError, ValueError, pa.ArrowException):
                pass  # values need Python-level coercion — fall through
            else:
                if missing_value_strategy == "allow":
                    return arr
                if missing_value_strategy == "default_or_allow":
                    if not self._has_default or self._is_nullable or arr.null_count == 0:
                        return arr
                    # non-nullable + has default + nulls from explicit None → fill
                    return cast(
                        Union[pa.Array, pa.ChunkedArray],
                        pc.fill_null(arr, pa.scalar(_prim_default, type=pa_type)),
                    )
                if missing_value_strategy == "default_or_error":
                    if arr.null_count == 0:
                        return arr
                    if self._has_default:
                        if self._is_nullable:
                            return arr
                        return cast(
                            Union[pa.Array, pa.ChunkedArray],
                            pc.fill_null(arr, pa.scalar(_prim_default, type=pa_type)),
                        )
                    raise TypeError("The value is missing, and this feature has no default value.")
                if missing_value_strategy == "error":
                    if arr.null_count and not self._is_nullable:
                        raise MissingValueError(
                            "The value is missing, but `replace_missing_with_defaults` was set to `False`."
                        )
                    return arr
                _raise_unsupported_missing_value_strategy(missing_value_strategy)

        # ── Slow path ────────────────────────────────────────────────────────
        # Values need Python-level coercion and/or contain Ellipsis sentinels.
        # Dispatch on strategy first so we build the output list exactly once.
        _coerce = self._arrow_coerce
        _coerce_for_err = self._coerce
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
                    # ... → default, explicit None stays null
                    return pa.array(
                        [_prim_default if x is ... else (None if x is None else _coerce(x)) for x in values],
                        type=pa_type,
                    )
                # non-nullable: ... and None both filled with default
                return cast(
                    Union[pa.Array, pa.ChunkedArray],
                    pc.fill_null(
                        pa.array([None if x is ... else (None if x is None else _coerce(x)) for x in values], type=pa_type),
                        pa.scalar(_prim_default, type=pa_type),
                    ),
                )
            if missing_value_strategy == "default_or_error":
                if has_default:
                    if is_nullable:
                        # ... → default, explicit None stays null
                        return pa.array(
                            [_prim_default if x is ... else (None if x is None else _coerce(x)) for x in values],
                            type=pa_type,
                        )
                    return cast(
                        Union[pa.Array, pa.ChunkedArray],
                        pc.fill_null(
                            pa.array([None if x is ... else (None if x is None else _coerce(x)) for x in values], type=pa_type),
                            pa.scalar(_prim_default, type=pa_type),
                        ),
                    )
                # No default: coerce and raise on sentinels in one pass
                pa_values: list[Any] = []
                for x in values:
                    if x is ... or (x is None and not is_nullable):
                        raise TypeError("The value is missing, and this feature has no default value.")
                    pa_values.append(None if x is None else _coerce(x))
                return pa.array(pa_values, type=pa_type)
            if missing_value_strategy == "error":
                # Coerce and raise on sentinels in one pass
                pa_values: list[Any] = []
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
                    _coerce_for_err(val)
                except (TypeError, ValueError) as scan_e:
                    feature_part = f" for feature '{feature_name}'" if feature_name is not None else ""
                    raise TypeError(
                        f"Could not convert '{val}' to `{self.rich_type}`{feature_part}: {scan_e}"
                    ) from scan_e
            # If the scan found nothing (iterator already consumed, or all values were
            # sentinels), re-raise the original error — but never swallow MissingValueError.
            if not isinstance(e, MissingValueError):
                feature_part = f" for feature '{feature_name}'" if feature_name is not None else ""
                raise TypeError(f"Could not convert a value to `{self.rich_type}`{feature_part}: {e}") from e
            raise

    def from_rich_to_primitive(
        self,
        value: Any,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> Any:
        if value is ... or (value is None and not self._is_nullable):
            if missing_value_strategy == "allow":
                return cast(Any, value)
            elif missing_value_strategy == "default_or_error":
                if self._has_default:
                    return self.primitive_default
                raise TypeError("The value is missing, and this feature has no default value.")
            elif missing_value_strategy == "default_or_allow":
                if self._has_default:
                    return self.primitive_default
                return cast(Any, value)
            elif missing_value_strategy == "error":
                raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
            else:
                _raise_unsupported_missing_value_strategy(missing_value_strategy)
        if value is None:
            return cast(Any, None)
        return self._coerce(cast(Any, value))

    def from_rich_to_json(
        self,
        value: Any,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        if value is ... or (value is None and not self._is_nullable):
            if missing_value_strategy == "allow":
                return cast(TJSON, value)
            if missing_value_strategy == "default_or_error":
                if self._has_default:
                    return self._serialize_to_json(self.primitive_default)
                raise TypeError("The value is missing, and this feature has no default value.")
            if missing_value_strategy == "default_or_allow":
                if self._has_default:
                    return self._serialize_to_json(self.primitive_default)
                return cast(TJSON, value)
            if missing_value_strategy == "error":
                raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
            _raise_unsupported_missing_value_strategy(missing_value_strategy)
        if value is None:
            return None
        return self._serialize_to_json(self._coerce(cast(Any, value)))

    def from_json_to_primitive(self, value: Any) -> Any:
        if value is None or value is ...:
            return None
        return self._json_coerce(value)

    def from_json_to_pyarrow(self, values: Sequence[Any]) -> Union[pa.Array, pa.ChunkedArray]:
        _json_coerce = self._json_coerce
        return pa.array(
            [None if x is None or x is ... else _json_coerce(x) for x in values],
            type=self.pyarrow_dtype,
        )

    def from_primitive_to_pyarrow(self, value: Iterable[Any]) -> Union[pa.Array, pa.ChunkedArray]:
        return pa.array(value, type=self.pyarrow_dtype)

    def from_pyarrow_to_primitive(self, values: Union[pa.Array, pa.ChunkedArray]) -> list:
        return values.to_pylist()

    def from_pyarrow_to_json(
        self,
        values: "pa.Array | pa.ChunkedArray",
        options: "FeatureEncodingOptions" = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> "Sequence[TJSON]":
        return values.to_pylist()

    def from_primitive_to_json(
        self,
        value: "TPrimitive",
        options: "FeatureEncodingOptions" = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> "TJSON":
        return cast("TJSON", value)

    def from_pyarrow_to_rich(self, values: pa.Array | pa.ChunkedArray, /) -> list:
        return values.to_pylist()

    def from_json_to_rich(self, value: Any) -> Any:
        return self.from_json_to_primitive(value)


# Types whose FeatureConverter._coerce_fn accepts a wider set of inputs than
# the declared Python type (e.g. DatetimeFeatureConverter accepts date/str in
# addition to datetime).  Used by ListFeatureConverter and
# DataclassFeatureConverter to decide whether per-element coercion is needed.
_SCALAR_COERCIBLE_TYPES: Tuple[type, ...] = (bool, datetime, date, time, timedelta)


def _scalar_coerce_fn(item_converter: "FeatureConverter[Any, Any]") -> "Callable[[Any], Any] | None":
    """Return a None-safe coerce closure for *item_converter* if it is a scalar
    converter whose ``_coerce_fn`` accepts a wider input set than its declared
    type (datetime/date/time/timedelta), or ``None`` otherwise.

    Called once at converter construction time; the returned closure is stored
    and called per-element at runtime with no extra dispatch overhead.
    """
    if (
        isinstance(item_converter, _ScalarConverterBase)
        and type(item_converter)._rich_type_value in _SCALAR_COERCIBLE_TYPES  # type: ignore[attr-defined]
    ):
        coerce_fn = type(item_converter)._coerce_fn  # type: ignore[attr-defined]
        return lambda x, _c=coerce_fn: None if x is None else _c(x)
    return None
