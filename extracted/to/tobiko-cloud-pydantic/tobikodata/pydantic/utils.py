from __future__ import annotations

import json
import typing as t

import pydantic
from pydantic_core import to_jsonable_python  # pants: no-infer-dep


def value_to_json(value: t.Any) -> str:
    return json.dumps(to_jsonable_python(value))


def serialize_value(value: t.Any) -> str:
    if isinstance(value, (list, dict, pydantic.BaseModel)):  # noqa: TID251
        return value_to_json(value)
    return value
