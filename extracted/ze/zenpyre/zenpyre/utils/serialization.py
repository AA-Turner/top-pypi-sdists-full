r"""Contain utility functions for serializing and deserializing
objects."""

from __future__ import annotations

__all__ = ["default_serialize"]

from dataclasses import asdict, is_dataclass
from typing import Any

from pydantic import BaseModel


def default_serialize(value: Any) -> Any:
    r"""Best-effort conversion of a value into something JSON-friendly.

    Recursively converts Pydantic models (including LangChain
    messages, which are Pydantic models) via
    ``model_dump(mode="json")``, converts dataclass instances via
    ``dataclasses.asdict`` followed by recursive serialization of
    their fields (so a Pydantic model or further dataclass nested
    inside a dataclass field is still converted correctly), and
    recurses into lists/tuples/dicts. Anything else is returned
    unchanged, on the assumption it's already a plain type (``str``,
    ``int``, ``bool``, ``None``, ...).

    Used as the default value of :class:`RecordingRunnable`'s
    ``serializer`` argument, applied to the whole assembled metadata
    dict (not to input/output individually) before it's stored.

    Args:
        value: The value to convert.

    Returns:
        A JSON-friendly version of ``value``.

    Example:
        ```pycon
        >>> import dataclasses
        >>> from pydantic import BaseModel
        >>> from zenpyre.utils.serialization import default_serialize
        >>> class Answer(BaseModel):
        ...     value: int
        ...
        >>> @dataclasses.dataclass
        ... class Point:
        ...     x: int
        ...     y: int
        ...
        >>> default_serialize({"result": Answer(value=5), "items": [Answer(value=1), "x"]})
        {'result': {'value': 5}, 'items': [{'value': 1}, 'x']}
        >>> default_serialize(Point(x=1, y=2))
        {'x': 1, 'y': 2}

        ```
    """
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if is_dataclass(value) and not isinstance(value, type):
        return {k: default_serialize(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {k: default_serialize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [default_serialize(v) for v in value]
    return value
