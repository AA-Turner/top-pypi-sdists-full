"""Shared field-coercion helpers for struct-like converters.

This module is the single home for :func:`_build_to_primitive_converter` and
:func:`_build_to_rich_converter`.  All struct-kind modules
(_dataclass_converter, _pydantic_converter, _attrs_converter) import these
functions from here at the top level, keeping their own import graphs clean.

The circular dependency between struct kinds and _factory is confined entirely
to the lazy imports inside this module's two public functions.
"""

from __future__ import annotations

import dataclasses as _dataclasses
import enum as _enum_module
from typing import Any, Callable, List, cast

from typing_extensions import get_args, get_origin

from chalk.utils.attrs_utils import is_attrs_class
from chalk.utils.collections import unwrap_optional_and_annotated_if_needed

from ._base import _SCALAR_COERCIBLE_TYPES, _scalar_coerce_fn  # pyright: ignore[reportPrivateUsage]


def _build_to_primitive_converter(typ: type) -> "Callable[[Any], Any] | None":
    """Return a closure that converts a value of *typ* to its primitive form, or ``None`` if
    the type is already primitive (no conversion needed).

    Handles arbitrary nesting: dataclasses, pydantic models, attrs classes, ``list[T]``,
    and combinations thereof.  ``Optional[T]`` / ``Annotated[T, ...]`` wrappers are
    stripped before dispatch.  Struct-kind and factory imports are lazy to avoid circular
    import cycles at module load time.
    """
    inner = unwrap_optional_and_annotated_if_needed(typ)

    if _dataclasses.is_dataclass(inner) and isinstance(inner, type):
        from ._dataclass_converter import _build_dc_to_dict  # pyright: ignore[reportPrivateUsage]
        return _build_dc_to_dict(inner)

    if is_attrs_class(inner):
        from ._attrs_converter import _build_attrs_to_dict  # pyright: ignore[reportPrivateUsage]
        return _build_attrs_to_dict(inner)

    from ._pydantic_converter import _is_pydantic_model, _build_model_to_dict  # pyright: ignore[reportPrivateUsage]
    if _is_pydantic_model(inner):
        return _build_model_to_dict(cast(type, inner))  # pyright: ignore[reportPrivateUsage]

    origin = get_origin(inner)
    if origin in (list, List):
        args = get_args(inner)
        if args:
            item_conv = _build_to_primitive_converter(args[0])
            if item_conv is not None:
                return lambda lst, _c=item_conv: None if lst is None else [_c(x) for x in lst]

    if isinstance(inner, type) and issubclass(inner, _enum_module.Enum):
        # Extract the primitive value; wrap in the enum's value type for safety.
        members = list(inner)
        val_type: type = type(members[0].value) if members else str
        return lambda v, _vt=val_type: None if v is None else _vt(v.value) if isinstance(v, _enum_module.Enum) else _vt(v)

    if inner in _SCALAR_COERCIBLE_TYPES:
        from ._factory import make_feature_converter as _make_fc
        fc = _make_fc(name="", is_nullable=True, rich_type=typ)
        closure = _scalar_coerce_fn(fc)
        if closure is not None:
            return closure

    return None


def _build_to_rich_converter(typ: type) -> "Callable[[Any], Any] | None":
    """Return a closure that converts a primitive value back to *typ*, or ``None`` if
    the type is already primitive (no conversion needed).

    Mirrors :func:`_build_to_primitive_converter` in the reverse direction.  All
    struct-kind and factory imports are lazy.
    """
    inner = unwrap_optional_and_annotated_if_needed(typ)

    if _dataclasses.is_dataclass(inner) and isinstance(inner, type):
        from ._dataclass_converter import _build_dict_to_dc  # pyright: ignore[reportPrivateUsage]
        return _build_dict_to_dc(inner)

    if is_attrs_class(inner):
        from ._attrs_converter import _build_dict_to_attrs  # pyright: ignore[reportPrivateUsage]
        return _build_dict_to_attrs(inner)

    from ._pydantic_converter import _is_pydantic_model, _build_dict_to_model  # pyright: ignore[reportPrivateUsage]
    if _is_pydantic_model(inner):
        return _build_dict_to_model(cast(type, inner))  # pyright: ignore[reportPrivateUsage]

    origin = get_origin(inner)
    if origin in (list, List):
        args = get_args(inner)
        if args:
            item_conv = _build_to_rich_converter(args[0])
            if item_conv is not None:
                return lambda lst, _c=item_conv: None if lst is None else [_c(x) for x in lst]

    if isinstance(inner, type) and issubclass(inner, _enum_module.Enum):
        ec = inner
        members = list(ec)
        val_type = type(members[0].value) if members else str
        def _prim_to_enum(v: Any, _ec: type = ec, _vt: type = val_type) -> Any:
            if v is None:
                return None
            if isinstance(v, _ec):
                return v
            return _ec(_vt(v))
        return _prim_to_enum

    return None
