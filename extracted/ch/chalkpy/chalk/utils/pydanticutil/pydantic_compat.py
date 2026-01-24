from __future__ import annotations

import json
from inspect import isclass
from typing import Any, TypeGuard

import pydantic
from packaging import version
from pydantic import BaseModel

try:
    from pydantic.v1 import BaseModel as V1BaseModel
except ImportError:
    V1BaseModel = None

is_pydantic_v1 = version.parse(pydantic.__version__).major == 1


def _is_pydantic_v1_basemodel(type_: type) -> TypeGuard[type[BaseModel]]:
    return V1BaseModel is not None and issubclass(type_, V1BaseModel)


def _is_pydantic_v1_basemodel_instance(v: object) -> TypeGuard[BaseModel]:
    return V1BaseModel is not None and isinstance(v, V1BaseModel)


def is_pydantic_basemodel(type_: object) -> TypeGuard[type[BaseModel]]:
    """Check if a type is a Pydantic BaseModel."""
    return isclass(type_) and (issubclass(type_, BaseModel) or _is_pydantic_v1_basemodel(type_))


def is_pydantic_basemodel_instance(v: object) -> TypeGuard[BaseModel]:
    return isinstance(v, BaseModel) or _is_pydantic_v1_basemodel_instance(v)


def get_pydantic_output_structure(model: type[BaseModel]) -> str:
    if is_pydantic_v1 or _is_pydantic_v1_basemodel(model):
        return model.schema_json()
    else:
        return json.dumps(model.model_json_schema())  # pyright: ignore[reportAttributeAccessIssue]


def parse_pydantic_model(model: type[BaseModel], json_str: str) -> BaseModel:
    if is_pydantic_v1 or _is_pydantic_v1_basemodel(model):
        return model.parse_raw(json_str)
    else:
        return model.model_validate_json(json_str)  # pyright: ignore[reportAttributeAccessIssue]


def construct_pydantic_model(model: type[BaseModel], /, **kwargs: Any) -> BaseModel:
    if is_pydantic_v1 or _is_pydantic_v1_basemodel(model):
        return model.construct(**kwargs)
    else:
        return model.model_construct(**kwargs)  # pyright: ignore[reportAttributeAccessIssue]


def get_pydantic_model_dict(model: BaseModel) -> dict[str, Any]:
    if is_pydantic_v1 or _is_pydantic_v1_basemodel_instance(model):
        return model.dict()
    else:
        return model.model_dump()  # pyright: ignore[reportAttributeAccessIssue]


def get_pydantic_model_json(model: BaseModel) -> str:
    if is_pydantic_v1 or _is_pydantic_v1_basemodel_instance(model):
        return model.json()
    else:
        return model.model_dump_json()  # pyright: ignore[reportAttributeAccessIssue]


def get_pydantic_field_type(model: type[BaseModel], field_name: str) -> type | None:
    """Get the type of a field from a Pydantic BaseModel, supporting both v1 and v2."""
    if is_pydantic_v1 or _is_pydantic_v1_basemodel(model):
        # Pydantic v1: use __fields__ and .type_
        if field_name in model.__fields__:
            return model.__fields__[field_name].type_
    else:
        # Pydantic v2: use model_fields and .annotation
        if field_name in model.model_fields:  # pyright: ignore[reportAttributeAccessIssue]
            return model.model_fields[field_name].annotation  # pyright: ignore[reportAttributeAccessIssue]
    return None
