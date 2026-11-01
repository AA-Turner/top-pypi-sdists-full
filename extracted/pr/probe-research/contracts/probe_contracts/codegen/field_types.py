"""FieldType: a record field's annotation as a small tree each renderer walks."""

from __future__ import annotations

import inspect
import types
import typing
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Literal, Union
from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

_SCALARS: dict[Any, str] = {
    UUID: "uuid",
    str: "str",
    int: "int",
    float: "float",
    bool: "bool",
    datetime: "datetime",
    dict: "dict",
}


@dataclass(frozen=True)
class FieldType:
    """`kind` is scalar, list, optional, enum, model or literal."""

    kind: str
    name: str = ""                       # scalar name, or the enum/model class name
    inner: FieldType | None = None       # list item / optional value
    values: tuple[str, ...] = ()         # literal values


def describe(annotation: Any) -> FieldType:
    """The FieldType of a record field's annotation; refuses a shape no renderer knows."""
    if annotation in _SCALARS:
        return FieldType("scalar", _SCALARS[annotation])
    origin = typing.get_origin(annotation)
    args = typing.get_args(annotation)
    if origin in (Union, types.UnionType):
        rest = [a for a in args if a is not type(None)]
        if len(rest) == 1 and len(args) == 2:
            return FieldType("optional", inner=describe(rest[0]))
    elif origin is list and len(args) == 1:
        return FieldType("list", inner=describe(args[0]))
    elif origin is Literal and all(isinstance(a, str) for a in args):
        return FieldType("literal", values=tuple(args))
    elif inspect.isclass(annotation) and issubclass(annotation, Enum):
        return FieldType("enum", annotation.__name__)
    elif inspect.isclass(annotation) and issubclass(annotation, BaseModel):
        return FieldType("model", annotation.__name__)
    raise TypeError(f"codegen cannot render the annotation {annotation!r}")


@dataclass(frozen=True)
class Default:
    """A field's default: none (required), a value, or a factory (`dict` / `list`)."""

    required: bool
    value: Any = None
    factory: str = ""


def default_of(info: FieldInfo) -> Default:
    if info.default_factory is not None:
        factory = getattr(info.default_factory, "__name__", "")
        if factory not in ("dict", "list"):
            raise TypeError(f"codegen cannot render the default factory {info.default_factory!r}")
        return Default(required=False, factory=factory)
    if info.default is PydanticUndefined:
        return Default(required=True)
    return Default(required=False, value=info.default)


def doc_of(cls: type) -> str:
    """The class's own docstring, cleaned; never one inherited from a base."""
    return inspect.cleandoc(cls.__dict__.get("__doc__") or "")
