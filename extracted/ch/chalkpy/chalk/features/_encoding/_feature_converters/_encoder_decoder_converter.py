from __future__ import annotations

from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterable,
    Optional,
    Sequence,
    Tuple,
)

from typing_extensions import get_origin

import pyarrow as pa

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.utils.json import TJSON

from ._base import (
    _DEFAULT_FEATURE_ENCODING_OPTIONS,
    FeatureConverter,
    MissingValueError,
    _raise_unsupported_missing_value_strategy,
)

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportMissingSuperCall=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false, reportUnnecessaryIsInstance=false


class EncoderDecoderFeatureConverter(FeatureConverter[Any, Any]):
    """Feature converter for custom encoder/decoder pairs.

    Wraps a base converter (derived from the pyarrow dtype alone) and
    intercepts rich↔primitive via the provided encoder/decoder callables.
    All pyarrow, protobuf, and json operations delegate to the base converter.
    """

    # Cache key: (rich_type, pyarrow_dtype, encoder, decoder, rich_default, is_nullable)
    # encoder/decoder cached by identity (they're functions/methods).
    _cache: ClassVar[Dict[Tuple[Any, ...], "EncoderDecoderFeatureConverter"]] = {}

    @classmethod
    def new(
        cls,
        rich_type: type,
        pyarrow_dtype: pa.DataType,
        encoder: Callable[[Any], Any],
        decoder: Optional[Callable[[Any], Any]],
        rich_default: Any,
        is_nullable: bool,
        *,
        base_converter: "FeatureConverter",
    ) -> "EncoderDecoderFeatureConverter":
        key = (rich_type, pyarrow_dtype, id(encoder), id(decoder), id(rich_default) if rich_default not in (..., None) else rich_default, is_nullable)
        cached = cls._cache.get(key)
        if cached is not None:
            return cached
        inst = cls.__new__(cls)
        inst._init(rich_type, pyarrow_dtype, encoder, decoder, rich_default, is_nullable, base_converter)
        cls._cache[key] = inst
        return inst

    def _init(
        self,
        rich_type: type,
        pyarrow_dtype: pa.DataType,
        encoder: Callable[[Any], Any],
        decoder: Optional[Callable[[Any], Any]],
        rich_default: Any,
        is_nullable: bool,
        base_converter: "FeatureConverter",
    ) -> None:
        # Use the origin type for isinstance checks — subscripted generics like
        # dict[str, str] raise TypeError, and Union/Optional origins (typing.Union)
        # are also not valid isinstance arguments.  Fall back to object (always True)
        # for those — the encoder/decoder will handle type coercion anyway.
        import typing as _typing
        origin = get_origin(rich_type)
        if origin is None:
            self._rich_type_inst: type = rich_type if isinstance(rich_type, type) else object
        elif origin is _typing.Union:
            self._rich_type_inst = object
        else:
            self._rich_type_inst = origin
        self._encoder_fn = encoder
        self._decoder_fn = decoder
        self._rich_default_val = rich_default
        self._is_nullable_val = is_nullable
        self._base = base_converter
        # Primitive default: encode the rich default if present; None for nullable no-default.
        if rich_default is not ... and rich_default is not None:
            self._primitive_default_val: Any = encoder(rich_default)
            self._has_default_val = True
        elif rich_default is None:
            self._primitive_default_val = None
            self._has_default_val = True
        else:
            self._primitive_default_val = ...
            self._has_default_val = False

    # ── properties ────────────────────────────────────────────────────────────

    @property
    def rich_type(self) -> type:
        t = self._rich_type_inst
        if self._is_nullable_val:
            from typing import Optional as _Optional
            return _Optional[t]  # type: ignore[return-value]
        return t

    @property
    def primitive_type(self) -> type:
        return self._base.primitive_type

    @property
    def pyarrow_dtype(self) -> pa.DataType:
        return self._base.pyarrow_dtype

    @property
    def protobuf_dtype(self) -> pb.ArrowType:
        return self._base.protobuf_dtype

    @property
    def polars_dtype(self) -> Any:
        return self._base.polars_dtype

    @property
    def encoder(self) -> Callable[[Any], Any]:
        return self._encoder_fn

    @property
    def decoder(self) -> Optional[Callable[[Any], Any]]:
        return self._decoder_fn

    @property
    def is_nullable(self) -> bool:
        return self._is_nullable_val

    @property
    def has_default(self) -> bool:
        return self._has_default_val

    @property
    def pyarrow_default(self) -> "ellipsis | pa.Array | pa.ChunkedArray":
        if not self._has_default_val:
            return ...
        return pa.array(
            [None if self._primitive_default_val is None else self._primitive_default_val],
            type=self._base.pyarrow_dtype,
        )

    @property
    def primitive_default(self) -> Any:
        if not self._has_default_val:
            raise ValueError("No default value specified")
        return self._primitive_default_val

    @property
    def rich_default(self) -> Any:
        return self._rich_default_val

    def has_nontrivial_rich_type(self) -> bool:
        return True

    # ── missing value ─────────────────────────────────────────────────────────

    def is_value_missing(self, value: Any) -> bool:
        return value is ...

    def is_rich_valid(self, value: Any) -> bool:
        try:
            prim = self.from_rich_to_primitive(value, "default_or_error")
            pa.scalar(prim, type=self.pyarrow_dtype)
            return True
        except (TypeError, ValueError):
            return False

    def _handle_missing(self, value: Any, missing_value_strategy: MissingValueStrategy) -> Any:
        if missing_value_strategy == "allow":
            return value
        if missing_value_strategy in ("default_or_allow", "default_or_error"):
            if self._has_default_val:
                return self._primitive_default_val
            if missing_value_strategy == "default_or_error":
                raise TypeError("The value is missing, and this feature has no default value.")
            return value
        if missing_value_strategy == "error":
            raise MissingValueError("The value is missing, but `replace_missing_with_defaults` was set to `False`.")
        _raise_unsupported_missing_value_strategy(missing_value_strategy)

    # ── rich ↔ primitive ──────────────────────────────────────────────────────

    def from_rich_to_primitive(
        self,
        value: Any,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> Any:
        if self.is_value_missing(value):
            return self._handle_missing(value, missing_value_strategy)
        if value is None:
            # Delegate None to base so struct types expand to null-field dict, scalars stay None.
            return self._base.from_rich_to_primitive(None)
        # Normalize via decode first so that primitive values (e.g. dicts) are round-tripped
        # correctly (matches GenericFeatureConverter behaviour).
        if not isinstance(value, self._rich_type_inst):
            value = self.from_primitive_to_rich(value)
        return self._encoder_fn(value)

    def from_primitive_to_rich(self, value: Any) -> Any:
        if self._decoder_fn is None:
            return self._base.from_primitive_to_rich(value)
        if isinstance(value, self._rich_type_inst):
            return value
        if value is None:
            # Expand None via base (struct → null-field dict, scalar → None), then decode.
            null_prim = self._base.from_primitive_to_rich(None)
            if null_prim is None:
                return None  # scalar types: None stays None, don't invoke decoder
            return self._decoder_fn(null_prim)
        return self._decoder_fn(value)

    # ── rich ↔ pyarrow ────────────────────────────────────────────────────────

    def from_rich_to_pyarrow(
        self,
        values: "Sequence[Any]",
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        feature_name: "str | None" = None,
    ) -> "pa.Array | pa.ChunkedArray":
        prims = [self.from_rich_to_primitive(v, missing_value_strategy) for v in values]
        return self._base.from_primitive_to_pyarrow(prims)

    def from_pyarrow_to_rich(self, values: "pa.Array | pa.ChunkedArray", /) -> Sequence[Any]:
        return [self.from_primitive_to_rich(p) for p in self._base.from_pyarrow_to_primitive(values)]

    # ── primitive ↔ pyarrow ───────────────────────────────────────────────────

    def from_primitive_to_pyarrow(self, values: "Iterable[Any]") -> "pa.Array | pa.ChunkedArray":
        return self._base.from_primitive_to_pyarrow(values)

    def from_pyarrow_to_primitive(self, values: "pa.Array | pa.ChunkedArray") -> Sequence[Any]:
        return self._base.from_pyarrow_to_primitive(values)

    # ── json ↔ * ──────────────────────────────────────────────────────────────

    def from_primitive_to_json(
        self,
        value: Any,
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        return self._base.from_primitive_to_json(value, options)

    def from_json_to_primitive(self, value: "TJSON") -> Any:
        return self._base.from_json_to_primitive(value)

    def from_rich_to_json(
        self,
        value: Any,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        prim = self.from_rich_to_primitive(value, missing_value_strategy)
        return self._base.from_primitive_to_json(prim, options)

    def from_json_to_rich(self, value: TJSON) -> Any:
        return self.from_primitive_to_rich(self._base.from_json_to_primitive(value))

    def from_pyarrow_to_json(
        self,
        values: "pa.Array | pa.ChunkedArray",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> "Sequence[TJSON]":
        return self._base.from_pyarrow_to_json(values, options)

    def from_json_to_pyarrow(self, values: "Sequence[TJSON]") -> "pa.Array | pa.ChunkedArray":
        return self._base.from_json_to_pyarrow(values)

    # ── protobuf ↔ * ─────────────────────────────────────────────────────────

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        return self._base.from_pyarrow_to_protobuf(value)

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        return self._base.from_protobuf_to_pyarrow(pb_value)

    def from_primitive_to_protobuf(self, value: Any) -> pb.ScalarValue:
        return self._base.from_primitive_to_protobuf(value)

    def from_rich_to_protobuf(
        self,
        value: Any,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = self.from_rich_to_primitive(value, missing_value_strategy)
        return self._base.from_primitive_to_protobuf(prim)
