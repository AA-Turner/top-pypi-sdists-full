from __future__ import annotations

from inspect import isclass

import pydantic
from pydantic import BaseModel
from typing_extensions import TypeGuard

try:
    from pydantic.v1 import BaseModel as V1BaseModel
except ImportError:
    V1BaseModel = None


def is_pydantic_basemodel(type_: object) -> TypeGuard[type[BaseModel]]:
    """Check if a type is a Pydantic BaseModel."""
    return isclass(type_) and (
        issubclass(type_, BaseModel) or (V1BaseModel is not None and issubclass(type_, V1BaseModel))
    )


def is_pydantic_basemodel_instance(v: object) -> TypeGuard[BaseModel]:
    return isinstance(v, BaseModel)


def is_pydantic_v1() -> bool:
    """
    True if pydantic is v1, else False
    """
    try:
        return int(pydantic.__version__.split(".")[0]) == 1
    except ImportError:
        return True
