from __future__ import annotations

import json
import types
from typing import (
    Any,
    Dict,
    FrozenSet,
    List,
    Protocol,
    Set,
    Tuple,
    Union,
    final,
)

from typing_extensions import get_args, get_origin

from chalk.utils.collections import unwrap_annotated_if_needed

from ._base import (
    _TPrimCo,
    _TPrimCon,
    _TRichCo,
    _TRichCon,
)

# pyright: reportImplicitStringConcatenation=false, reportPrivateUsage=false


class TEncoder(Protocol[_TPrimCo, _TRichCon]):
    def __call__(self, value: _TRichCon, /) -> _TPrimCo: ...


class TDecoder(Protocol[_TPrimCon, _TRichCo]):
    def __call__(self, value: _TPrimCon, /) -> _TRichCo: ...


def _encode_json(t: Any) -> str:
    return json.dumps(t)


def _decode_json(s: str) -> Any:
    return json.loads(s)


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
