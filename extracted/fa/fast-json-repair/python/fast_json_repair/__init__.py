"""Fast JSON repair library using Rust for performance."""

import json as _json
from typing import Any, Union

import orjson

from fast_json_repair._fast_json_repair import (
    _escape_non_ascii_json,
    _has_wide_integer,
    _repair_json_obj_rust,
    _repair_json_obj_with_log_rust,
    _repair_json_rust,
)

__version__ = "0.2.3"
__all__ = ["repair_json", "loads"]

def _serialize_valid(
    parsed: Any,
    *,
    ensure_ascii: bool,
    indent: Any,
    wide_integer: bool,
    json_dumps_args: dict[str, Any],
) -> str:
    """Serialize a valid parsed value using the fastest compatible serializer."""
    if not wide_integer and not json_dumps_args and indent in (None, 2):
        option = orjson.OPT_INDENT_2 if indent == 2 else 0
        encoded = orjson.dumps(parsed, option=option)
        if ensure_ascii:
            return _escape_non_ascii_json(encoded)
        return encoded.decode("utf-8")

    return _json.dumps(
        parsed,
        ensure_ascii=ensure_ascii,
        indent=indent,
        **json_dumps_args,
    )


def repair_json(
    json_string: str = "",
    return_objects: bool = False,
    skip_json_loads: bool = False,
    logging: bool = False,
    stream_stable: bool = False,
    **json_dumps_args: Any,
) -> Union[str, Any]:
    """
    Repair invalid JSON and return either JSON text or a parsed Python object.

    When ``logging`` is true, return ``(parsed_object, repair_events)``. Each
    event includes its type, description, context, byte position, line, and
    column.

    ``json_dumps_args`` is forwarded to :func:`json.dumps` when custom output
    formatting is requested. ``ensure_ascii`` and ``indent`` retain their
    standard ``json.dumps`` meanings.
    """
    del stream_stable  # Accepted for json_repair API compatibility.

    if not isinstance(json_string, str):
        raise TypeError(f"Expected string, got {type(json_string).__name__}")

    ensure_ascii = json_dumps_args.pop("ensure_ascii", True)
    indent = json_dumps_args.pop("indent", None)

    if not json_string.strip():
        empty_result: Any = ""
        if logging:
            return empty_result, []
        return empty_result

    parsed: Any = None
    parsed_valid_json = False
    wide_integer = False

    if not skip_json_loads:
        try:
            wide_integer = _has_wide_integer(json_string)
            parsed = _json.loads(json_string) if wide_integer else orjson.loads(json_string)
            parsed_valid_json = True
        except (orjson.JSONDecodeError, _json.JSONDecodeError, TypeError, ValueError):
            pass

    if parsed_valid_json:
        if return_objects or logging:
            result = parsed
        else:
            result = _serialize_valid(
                parsed,
                ensure_ascii=ensure_ascii,
                indent=indent,
                wide_integer=wide_integer,
                json_dumps_args=json_dumps_args,
            )
        if logging:
            return result, []
        return result

    needs_python_serializer = bool(json_dumps_args) or (
        indent is not None and (not isinstance(indent, int) or indent <= 0)
    )
    repair_log: list[dict[str, Any]] = []
    if logging:
        repaired_object, repair_log = _repair_json_obj_with_log_rust(json_string)
        result = repaired_object
    elif return_objects or needs_python_serializer:
        repaired_object = _repair_json_obj_rust(json_string)
        if return_objects:
            result = repaired_object
        else:
            result = _json.dumps(
                repaired_object,
                ensure_ascii=ensure_ascii,
                indent=indent,
                **json_dumps_args,
            )
    else:
        rust_indent = 0 if indent is None else int(indent)
        result = _repair_json_rust(json_string, bool(ensure_ascii), rust_indent)

    if logging:
        return result, repair_log
    return result


def loads(
    json_string: str,
    skip_json_loads: bool = False,
    logging: bool = False,
    stream_stable: bool = False,
    **kwargs: Any,
) -> Any:
    """Repair and parse a JSON string."""
    return repair_json(
        json_string,
        return_objects=True,
        skip_json_loads=skip_json_loads,
        logging=logging,
        stream_stable=stream_stable,
        **kwargs,
    )
