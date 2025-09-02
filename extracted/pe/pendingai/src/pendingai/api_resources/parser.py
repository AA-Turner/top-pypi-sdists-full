#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from typing import Any, TypeVar

from typing_extensions import get_args, get_origin

from pendingai.api_resources.object import ListObject, Object

T = TypeVar("T", bound=Any)


def cast_resource(obj_type: type[Object], value: Any) -> Object:
    assert isinstance(value, dict)
    return obj_type(**value)


def cast_resource_list(obj_type: type[ListObject[T]], value: Any) -> ListObject[T]:
    assert isinstance(value, dict) and "data" in value
    resource_type: type[Any] = next(iter(get_args(obj_type)), type(None))
    assert issubclass(resource_type, dict)
    data: list[Any] = [cast(resource_type, v) for v in value.pop("data")]
    return obj_type(data=data, **value)


def cast(obj_type: type[Any], value: Any) -> Any:
    assert len(get_args(obj_type)) < 2, "Multiple generics not supported."

    origin: Any | None = get_origin(obj_type)
    dtargs: type[Any] | None = next(iter(get_args(obj_type)), None)
    if origin is None:
        return obj_type(**value if isinstance(obj_type, dict) else value)
    elif issubclass(origin, ListObject):
        return cast_resource_list(obj_type, value)
    elif issubclass(origin, Object):
        return cast_resource(obj_type, value)
    elif issubclass(origin, list):
        assert dtargs is not None
        return [cast(dtargs, v) for v in value]
    elif issubclass(origin, dict):
        return value if isinstance(value, dict) else dict(value)
    raise Exception
