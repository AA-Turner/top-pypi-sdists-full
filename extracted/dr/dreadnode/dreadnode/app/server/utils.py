"""Server utility functions."""

from __future__ import annotations

import typing as t

import orjson


def _default_serializer(obj: t.Any) -> t.Any:
    """Default serializer for types orjson doesn't handle natively."""
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    if hasattr(obj, "__str__"):
        return str(obj)
    raise TypeError(f"Type is not JSON serializable: {type(obj).__name__}")


def safe_json_dumps(obj: t.Any) -> str:
    """JSON dumps using orjson (handles NaN/Infinity as null, faster serialization)."""
    return orjson.dumps(
        obj,
        default=_default_serializer,
        option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NON_STR_KEYS,
    ).decode("utf-8")
