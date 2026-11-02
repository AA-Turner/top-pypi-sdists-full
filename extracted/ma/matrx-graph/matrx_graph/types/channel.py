from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

from matrx_graph.errors import ChannelError
from matrx_graph.types.primitives import Reducer

JsonValue = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]


class ChannelSpec(BaseModel):
    """Declarative spec for a channel in a workflow definition.

    Channels hold JSON-serializable values only. Pydantic models are dumped at
    write time via .model_dump(mode='json'). This rule is enforced in the
    channel manager and makes checkpoints round-trip losslessly.
    """

    model_config = {"frozen": True}

    name: str = Field(min_length=1, max_length=120)
    reducer: Reducer = "replace"
    description: str | None = None
    default: Any = None

    @field_validator("default")
    @classmethod
    def _default_must_be_json(cls, v: Any) -> Any:
        if v is None:
            return v
        _ensure_json(v, path=("default",))
        return v


def _ensure_json(value: Any, path: tuple[str, ...] = ()) -> None:
    """Raise ChannelError if value is not JSON-serializable (strict, no coercion)."""
    if value is None or isinstance(value, bool | int | float | str):
        return
    if isinstance(value, list):
        for i, item in enumerate(value):
            _ensure_json(item, path + (f"[{i}]",))
        return
    if isinstance(value, dict):
        for k, item in value.items():
            if not isinstance(k, str):
                loc = ".".join(path) or "<root>"
                raise ChannelError(
                    f"Channel value at {loc} has non-string dict key {k!r}; "
                    f"JSON requires string keys."
                )
            _ensure_json(item, path + (k,))
        return
    loc = ".".join(path) or "<root>"
    raise ChannelError(
        f"Channel value at {loc} is of type {type(value).__name__!r}; "
        f"channels accept JSON-serializable values only. "
        f"Dump Pydantic models with .model_dump(mode='json') at the call site."
    )


def coerce_to_json(value: Any) -> Any:
    """Dump a Pydantic model to JSON-safe form; leave plain JSON values alone.

    Raises ChannelError if the result is still not JSON-serializable.
    """
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")
    _ensure_json(value)
    return value
