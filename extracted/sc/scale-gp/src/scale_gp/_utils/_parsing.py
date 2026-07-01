from __future__ import annotations

import inspect
from typing import Any, cast

import pydantic

from scale_gp._types import NOT_GIVEN, NotGiven
from scale_gp._compat import PYDANTIC_V1, model_json_schema
from scale_gp.types.beta import completion_create_params
from scale_gp._utils._utils import is_given


def is_pydantic_basemodel(type_: type) -> bool:
    # NOTE: is_basemodel_type from _models only checks if it is a scale_gp BaseModel
    # not a pydantic BaseModel
    return issubclass(type_, pydantic.BaseModel)


def is_dataclass_like_type(typ: type) -> bool:
    """Returns True if the given type likely used `@pydantic.dataclass`"""
    return hasattr(typ, "__pydantic_config__")


def to_json_schema(model: type[pydantic.BaseModel] | pydantic.TypeAdapter[Any]) -> dict[str, Any]:
    if inspect.isclass(model) and is_pydantic_basemodel(model):
        schema = model_json_schema(model)
    elif not PYDANTIC_V1 and isinstance(model, pydantic.TypeAdapter):
        schema = model.json_schema()
    else:
        raise TypeError(f"Non BaseModel types are only supported with Pydantic v2+ - {model}")

    return schema


# Inspired by https://github.com/openai/openai-python/blob/main/src/openai/lib/_parsing/_completions.py
# Note that this does not validate the output schema like OpenAI does and also does not set strict = True.
def type_to_response_format_param(
    response_format: completion_create_params.ResponseFormat | NotGiven,
) -> completion_create_params.ResponseFormat | NotGiven:
    if not is_given(response_format):
        return NOT_GIVEN

    # type checkers don't narrow the negation of a `TypeGuard` as it isn't
    # a safe default behaviour but we know that at this point the `response_format`
    # can only be a `type`
    response_format = cast(type, response_format)

    json_schema_type: type[pydantic.BaseModel] | pydantic.TypeAdapter[Any] | None = None

    if is_pydantic_basemodel(response_format):
        name = response_format.__name__
        json_schema_type = response_format
    elif is_dataclass_like_type(response_format):
        name = response_format.__name__
        json_schema_type = pydantic.TypeAdapter(response_format)
    else:
        return response_format

    return {
        "type": "json_schema",
        "json_schema": {
            "schema": to_json_schema(json_schema_type),
            "name": name,
        },
    }
