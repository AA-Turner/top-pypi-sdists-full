from __future__ import annotations

from importlib.util import find_spec
from types import ModuleType
from typing import Any, TypeGuard


def get_attrs() -> ModuleType | None:
    try:
        if find_spec("attrs") is None:
            return None
        import attrs
    except (ImportError, ValueError):
        return None
    return attrs


def is_attrs_class(value: Any) -> TypeGuard[type[Any]]:
    attrs = get_attrs()
    return attrs is not None and isinstance(value, type) and attrs.has(value)


def is_attrs_instance(value: Any) -> bool:
    attrs = get_attrs()
    return attrs is not None and attrs.has(value.__class__)


def attrs_fields(value: type) -> tuple[Any, ...]:
    attrs = get_attrs()
    if attrs is None:
        raise ImportError("attrs")
    return tuple(attrs.fields(value))
