from __future__ import annotations

import json
import types
from typing import (
    Any,
    Dict,
    FrozenSet,
    Generic,
    List,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
    cast,
    final,
)

import pyarrow as pa
from typing_extensions import get_args, get_origin

from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.pyarrow import rich_to_pyarrow, pyarrow_to_primitive
from chalk.features._encoding.rich import structure_primitive_to_rich, unstructure_rich_to_primitive
from chalk.features.feature_wrapper import UnresolvedFeature
from chalk.utils.collections import unwrap_annotated_if_needed, unwrap_optional_and_annotated_if_needed
from chalk.utils.json import TJSON, is_pyarrow_json_type

from ._base import (
    _DEFAULT_FEATURE_ENCODING_OPTIONS,
    _TPrim,
    _TPrimCo,
    _TPrimCon,
    _TRich,
    _TRichCo,
    _TRichCon,
    MissingValueError,
)
from ._primitive_converter import PrimitiveFeatureConverter

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportMissingSuperCall=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false, reportImplicitStringConcatenation=false


class TEncoder(Protocol[_TPrimCo, _TRichCon]):
    def __call__(self, value: _TRichCon, /) -> _TPrimCo: ...


class TDecoder(Protocol[_TPrimCon, _TRichCo]):
    def __call__(self, value: _TPrimCon, /) -> _TRichCo: ...


def _encode_json(t: Any) -> str:
    return json.dumps(t)


def _decode_json(s: str) -> Any:
    return cast(Any, json.loads(s))


def _to_old_style_type(origin: object):
    if origin is list:
        return List
    elif origin is tuple:
        return Tuple
    elif origin is set:
        return Set
    elif origin is frozenset:
        return FrozenSet
    elif origin is dict:
        return Dict
    elif hasattr(types, "UnionType"):
        # Only available in python >=3.10
        if origin is getattr(types, "UnionType"):
            return Union
    return origin


def canonicalize_typ(x: object):
    """Canonicalize a type annotation for equality checking.
    New-style types are replaced with old-style types, and
    annotated markers are ignored. Specifically:

    - typing.Annotated -> unwrapped
    - list             -> typing.List
    - tuple            -> typing.Tuple
    - set              -> typing.Set
    - frozenset        -> typing.Frozenset
    - dict             -> typing.Dict
    - union            -> typing.Union
    """

    if x is None:
        x = type(None)
    x = unwrap_annotated_if_needed(x)
    origin, args = get_origin(x), get_args(x)
    if origin is None:
        return _to_old_style_type(x)
    origin = _to_old_style_type(origin)
    args = tuple(canonicalize_typ(x) for x in args)
    return origin[args]  # type: ignore -- pyright doesn't understand metaprogramming


@final
class JSONCodec:
    encode: TEncoder[str, Any] = _encode_json
    decode: TDecoder[str, Any] = _decode_json


class GenericFeatureConverter(PrimitiveFeatureConverter[_TPrim, _TRich], Generic[_TPrim, _TRich]):
    """Feature converter that deals with rich types. It supports everything that the primitive feature converter supports.

    However, since it deals with Rich types, it can only be constructed from the source code, since rich type information
    is not stored in serialized graphs."""

    def __init__(
        self,
        name: str,
        is_nullable: bool,
        rich_type: Union[Type[_TRich], ellipsis] = ...,
        primitive_default: Union[_TPrim, ellipsis] = ...,
        rich_default: Union[_TRich, ellipsis] = ...,
        pyarrow_dtype: Optional[pa.DataType] = None,
        encoder: Optional[TEncoder[_TPrim, _TRich]] = None,
        decoder: Optional[TDecoder[_TPrim, _TRich]] = None,
    ) -> None:
        self._rich_type = unwrap_annotated_if_needed(rich_type)

        if pyarrow_dtype is None:
            if rich_type is ...:
                raise ValueError("Either the `rich_type` or `pyarrow_dtype` must be provided")
            pyarrow_dtype = rich_to_pyarrow(rich_type, name)

        if rich_type is ...:
            if rich_default != ...:
                raise ValueError(
                    "The `rich_default` cannot be used without the `rich_type`. Perhaps specify the `primitive_default` instead?"
                )
            if is_nullable and primitive_default is ...:
                primitive_default = cast(_TPrim, None)

        else:
            if primitive_default != ...:
                raise ValueError(
                    "The `primitive_default` cannot be used when specifying the `rich_type`. Instead, specify the `rich_default`."
                )
            if is_nullable and rich_default is ...:
                rich_default = cast(_TRich, None)

        # In the future, we will require the rich type to be not-none and remove the primitive default flag,
        # and then we can simplify the code as follows:
        # if pyarrow_dtype is None:
        #     if rich_type is ...:
        #         raise ValueError("Either the `rich_type` or `pyarrow_dtype` must be provided")
        #     pyarrow_dtype = rich_to_pyarrow(rich_type, name)

        # elif is_nullable and rich_default is ...:
        #     rich_default = cast(_TRich, None)

        if rich_type is ...:
            if encoder is not None:
                raise ValueError("An encoder cannot be specified without also specifying the `rich_type`")
            if decoder is not None:
                raise ValueError("An encoder cannot be specified without also specifying the `rich_type`")
        self._encoder = encoder
        self._decoder = decoder
        self._rich_default = rich_default
        self._primitive_type = pyarrow_to_primitive(pyarrow_dtype, name)
        self._pyarrow_dtype = pyarrow_dtype
        self._is_nullable = is_nullable

        # This field is also set in the super() call, but must be initialized here
        # because it is also used for error handling inside of `from_rich_to_primitive`.
        self._name = name
        if rich_default != ...:
            # In notebook environments, UnresolvedFeature may be used as a placeholder
            # for features that can't be resolved due to a stale registry.
            # Treat these as missing defaults since they're not concrete values.
            if isinstance(rich_default, UnresolvedFeature):
                rich_default = ...
            else:
                # The missing value strategy doesn't really matter because rich_default is not missing
                primitive_default = self.from_rich_to_primitive(rich_default, missing_value_strategy="allow")
        super().__init__(
            name, is_nullable=is_nullable, pyarrow_dtype=pyarrow_dtype, primitive_default=primitive_default
        )

    @property
    def rich_type(self) -> Type[_TRich]:
        if self._rich_type is ...:
            raise ValueError(
                "Rich types cannot be used as the GenericFeatureConverter was created without providing a `rich_type`"
            )
        return cast(Type[_TRich], self._rich_type)

    @property
    def rich_default(self) -> _TRich:
        if self._rich_default is ...:
            raise ValueError(f"Feature '{self._name}' has no default value")
        return self._rich_default

    def is_rich_valid(self, value: _TRich) -> bool:
        """Returns true if value has a valid rich type"""
        try:
            prim = self.from_rich_to_primitive(value, "default_or_error")
            pa.scalar(prim, type=self.pyarrow_dtype)
            return True
        except (TypeError, ValueError):
            return False

    def from_rich_to_pyarrow(
        self,
        values: Sequence[Union[_TRich, ellipsis, None]],
        /,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        feature_name: str | None = None,
    ) -> Union[pa.Array, pa.ChunkedArray]:
        prim_values = [self.from_rich_to_primitive(x, missing_value_strategy) for x in values]
        return self.from_primitive_to_pyarrow(prim_values)

    def from_rich_to_protobuf(
        self,
        value: Union[_TRich, ellipsis, None],
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> Any:
        return self.from_primitive_to_protobuf(self.from_rich_to_primitive(value, missing_value_strategy))

    def from_rich_to_primitive(
        self,
        value: Union[_TRich, ellipsis, None],
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> _TPrim:
        # Ensure that the rich value is indeed the rich type
        # For example, if a string is passed in for a datetime value, convert it into a datetime
        if self.is_value_missing(value):
            if missing_value_strategy == "allow":
                return cast(_TPrim, value)
            elif missing_value_strategy in ("default_or_error", "default_or_allow"):
                if self.has_default:
                    return self.primitive_default
                elif missing_value_strategy == "default_or_error":
                    raise TypeError(
                        f"The value for feature '{self._name}' is missing, and this feature has no default value."
                    )
                else:
                    return cast(_TPrim, value)
            elif missing_value_strategy == "error":
                raise MissingValueError(
                    f"The value for feature '{self._name}' is missing, but `replace_missing_with_defaults` was set to `False`."
                )
            else:
                raise ValueError(
                    (
                        f"Unsupported missing value strategy: {missing_value_strategy}. "
                        "It must be one of 'allow', 'default_or_allow', 'default_or_error', or 'error'."
                    )
                )
        value = self.from_primitive_to_rich(cast(_TPrim, value))
        return self._to_primitive(value)

    def from_rich_to_json(
        self,
        value: Union[_TRich, ellipsis, None],
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
        options: FeatureEncodingOptions = _DEFAULT_FEATURE_ENCODING_OPTIONS,
    ) -> TJSON:
        prim_val = self.from_rich_to_primitive(value, missing_value_strategy)
        return self.from_primitive_to_json(prim_val, options=options)

    def from_pyarrow_to_rich(self, values: Union[pa.Array, pa.ChunkedArray], /) -> Sequence[_TRich]:
        return [self.from_primitive_to_rich(x) for x in self.from_pyarrow_to_primitive(values)]

    @property
    def encoder(self) -> Optional[TEncoder[_TPrim, _TRich]]:
        return self._encoder

    @property
    def decoder(self) -> Optional[TDecoder[_TPrim, _TRich]]:
        return self._decoder

    def _to_primitive(self, val: _TRich) -> _TPrim:
        if val is None or self._encoder is None:
            # Structuring null values to the primitive type to ensure that a singular null for an entire struct
            # is propagated to individual struct fields -- e.g.
            # class LatLong:
            #     lat: Optional[float]
            #     long: Optional[float]
            # then self._from_prim(None) == LatLong(None, None)
            # Using self.primitive_type, rather than self._rich_type, as the primitive type
            # might not be registered on the converter for custom classes
            try:
                x = unstructure_rich_to_primitive(val)
            except (TypeError, ValueError) as e:
                raise TypeError(
                    f"Could not convert '{val}' to `{self.primitive_type}` for feature '{self._name}': {e}"
                ) from e
            if x is None and not self._is_nullable:
                raise ValueError(f"Feature '{self._name}' is null, but it cannot be nullable")
            try:
                return cast(_TPrim, structure_primitive_to_rich(x, self.primitive_type))
            except (TypeError, ValueError) as e:
                raise TypeError(
                    f"Could not convert '{val}' to `{self.primitive_type}` for feature '{self._name}': {e}"
                ) from e
        return self._encoder(val)

    def _from_prim(self, val: Union[_TPrim, _TRich]) -> _TRich:
        if self._rich_type is ...:
            raise ValueError(
                "Rich types cannot be used as the GenericFeatureConverter was created without providing a `rich_type`"
            )
        if val is None:
            # Structuring null values to the primitive type to ensure that a singular null for an entire struct
            # is propagated to individual struct fields -- e.g.
            # class LatLong:
            #     lat: Optional[float]
            #     long: Optional[float]
            # then self._from_prim(None) == LatLong(None, None)
            # Using self.primitive_type, rather than self._rich_type, as the primitive type
            # might not be registered on the converter for custom classes
            try:
                val = structure_primitive_to_rich(cast(_TPrim, val), cast(Type[_TRich], self.primitive_type))
            except (TypeError, ValueError) as e:
                raise TypeError(
                    f"Could not convert '{val}' to `{self.primitive_type}` for feature '{self._name}': {e}"
                ) from e
        if self._decoder is None:
            try:
                return structure_primitive_to_rich(cast(_TPrim, val), self._rich_type)
            except (TypeError, ValueError) as e:
                raise TypeError(
                    f"Could not convert '{val}' to `{self._rich_type}` for feature '{self._name}': {e}"
                ) from e
        # is_pyarrow_json_type is only needed to handle python 3.8
        if is_pyarrow_json_type(self.pyarrow_dtype) or isinstance(
            val, unwrap_optional_and_annotated_if_needed(self._rich_type)
        ):
            return cast(_TRich, val)
        if val is None:
            # If the value is None, then we won't call the custom converter, since those likely cannot handle null values
            # and None is perfectly valid as a "rich" type
            return cast(_TRich, None)
        return self._decoder(cast(_TPrim, val))

    def from_primitive_to_rich(self, value: Union[_TPrim, _TRich]) -> _TRich:
        return self._from_prim(value)

    def from_json_to_rich(self, value: TJSON) -> _TRich:
        prim_val = self.from_json_to_primitive(value)
        return self.from_primitive_to_rich(prim_val)

    def has_nontrivial_rich_type(self) -> bool:
        if self._encoder is not None or self._decoder is not None:
            return True

        prim_canonical = canonicalize_typ(self.primitive_type)
        rich_canonical = canonicalize_typ(self.rich_type)
        if self.is_nullable:
            # Primitive type is based off of the pyarrow dtype, which doesn't know about nullability
            # So Optional[str] will become just 'str' and needs to be re-wrapped in an Optional[] to compare w/ the rich type
            # This is mainly a hack for re-creating python Feature objects from serialize proto features (e.g. for running notebook-defined resolvers)
            # We can remove this once we support encoding more information about the rich type itself in the feature proto.
            prim_canonical = Optional[prim_canonical]
        return prim_canonical != rich_canonical
