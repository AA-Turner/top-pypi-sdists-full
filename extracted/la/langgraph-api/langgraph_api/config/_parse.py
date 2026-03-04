from collections.abc import Callable
from typing import Annotated, TypeVar, cast, get_args, get_origin

import orjson
from pydantic import TypeAdapter
from typing_extensions import TypeForm

from langgraph_api.config.schemas import (
    CheckpointerConfig,
    ThreadTTLConfig,
)

TD = TypeVar("TD")


def parse_json(json: str | None, schema: TypeAdapter | None = None) -> dict | None:
    if not json:
        return None
    parsed = schema.validate_json(json) if schema else orjson.loads(json)
    if hasattr(parsed, "model_dump"):
        parsed = parsed.model_dump(exclude_none=True)
    return parsed or None


def parse_schema(
    schema: TypeForm[TD],
) -> Callable[[str | None], TD | None]:
    def composed(json: str | None) -> TD | None:
        return cast("TD | None", parse_json(json, schema=TypeAdapter(schema)))

    # This just gives a nicer error message if the user provides an incompatible value
    schema_type = get_args(schema)[0] if get_origin(schema) is Annotated else schema
    composed.__name__ = getattr(schema_type, "__name__", repr(schema_type))
    return composed


def parse_thread_ttl(value: str | None) -> ThreadTTLConfig | None:
    """Parse LANGGRAPH_THREAD_TTL environment variable.

    Accepts either:
    - A simple number (TTL in minutes): "60"
    - A JSON object: '{"strategy": "keep_latest", "default_ttl": 60, "sweep_limit": 500}'

    Supported strategies:
    - "delete": Remove the thread and all its data entirely
    - "keep_latest": Prune old checkpoints but keep the thread and latest state
    """
    if not value:
        return None
    if str(value).strip().startswith("{"):
        return parse_json(value.strip())
    return {
        "strategy": "delete",
        # We permit float values mainly for testing purposes
        "default_ttl": float(value),
        "sweep_interval_minutes": 5.1,
        "sweep_limit": 1000,  # Default max threads per sweep iteration
    }


def parse_checkpointer(value: str | None) -> CheckpointerConfig | None:
    if not value:
        return None

    raw = orjson.loads(value)
    if not isinstance(raw, dict):
        raise ValueError("CheckpointerConfig must be a JSON object")

    # Handle backend defaults.
    if "backend" not in raw:
        if "path" in raw:
            raw = {**raw, "backend": "custom"}
        else:
            raw = {**raw, "backend": "default"}

    parsed = TypeAdapter(CheckpointerConfig).validate_python(raw)
    return cast("CheckpointerConfig | None", parsed or None)
