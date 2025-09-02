#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from inspect import getmembers, isroutine
from typing import Any, Generic, TypeVar, get_type_hints

from pendingai.api_resources.validator import validate
from pendingai.exceptions import TypeValidationError

T = TypeVar("T", bound="Object")


class Object(dict):
    """
    Base object data structure with dictionary properties and object
    attribute-based field interaction. Used similar to a `TypedDict`
    class but with enforced data validation and flexibility.

    Usage:
    ```python
        >>> class MyObject(Obejct):
        >>>     x: int
        >>>     y: int
        >>> obj = MyObject({"x": 1}, y=2)
        >>> obj.x, obj.y
        (1, 2)
        >>> obj.y
    ```
    """

    def __init__(self, mapping: dict[str, Any] = {}, **kw_mapping: Any):
        field_mapping: dict[str, Any] = self._get_default_fields() | mapping | kw_mapping
        super().__init__(**field_mapping)
        classname: str = self.__class__.__name__
        for k, dtype in self._get_annotations().items():
            if k.startswith("_"):
                continue
            if k not in field_mapping:
                raise TypeError(f"Missing required field for '{classname}': '{k}'.")
            setattr(self, k, validate(dtype, field_mapping[k]))

    def _get_annotations(self) -> dict[str, Any]:
        return get_type_hints(self.__class__)

    def _get_default_fields(self) -> dict[str, Any]:
        members: list[tuple] = getmembers(self.__class__, lambda x: not isroutine(x))
        return dict(
            [a for a in members if "__" not in a[0] and not isinstance(a[1], type)]
        )

    def __getitem__(self, key: str) -> Any:
        if not hasattr(self, key):
            raise KeyError(key)
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        if not hasattr(self, key) or key not in self._get_annotations():
            raise KeyError(key)
        if not isinstance(value, (dt := self._get_annotations().get(key, Any))):
            raise TypeValidationError(value, dt)
        setattr(self, key, value)


class ListObject(Object, Generic[T]):
    object: str = "list"
    data: list[T]
    has_more: bool
