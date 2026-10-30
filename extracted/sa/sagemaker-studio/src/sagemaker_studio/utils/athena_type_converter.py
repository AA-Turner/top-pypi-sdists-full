"""Convert Athena GetQueryResults string values into Python values."""

import binascii
import json
import re
from datetime import datetime
from decimal import Decimal, DecimalException
from typing import Any, Callable, Dict, Optional

from dateutil.tz import gettz


def _date(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()


def _timestamp(value: str):
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")


def _timestamp_with_tz(value: str):
    timestamp, _, zone = value.rpartition(" ")
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=gettz(zone))


def _time(value: str):
    return datetime.strptime(value, "%H:%M:%S.%f").time()


def _boolean(value: str):
    if not value:
        return None
    normalized = value.lower()
    if normalized in ("1", "true", "t", "yes", "y", "on"):
        return True
    if normalized in ("0", "false", "f", "no", "n", "off"):
        return False
    raise ValueError(f"invalid truth value {value!r}")


def _decimal(value: str):
    return Decimal(value) if value else None


def _binary(value: str):
    return binascii.a2b_hex("".join(value.split(" ")))


def _native_scalar(value: str) -> Any:
    normalized = value.lower()
    if normalized == "null":
        return None
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
        return int(value)
    if "." in value and value.replace(".", "", 1).replace("-", "", 1).isdigit():
        return float(value)
    return value


def _split_top_level(value: str):
    parts = []
    current = []
    braces = brackets = 0
    for char in value:
        if char == "{":
            braces += 1
        elif char == "}":
            braces -= 1
        elif char == "[":
            brackets += 1
        elif char == "]":
            brackets -= 1
        elif char == "," and braces == 0 and brackets == 0:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    if current:
        parts.append("".join(current).strip())
    return parts


def _array(value: str):
    if not (value.startswith("[") and value.endswith("]")):
        return None
    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        pass
    inner = value[1:-1].strip()
    if not inner:
        return []
    if "[" in inner:
        return None
    result = []
    for item in _split_top_level(inner):
        if not item:
            continue
        if item.startswith("{") and item.endswith("}"):
            parsed = _struct(item)
            if parsed is not None:
                result.append(parsed)
            continue
        if any(char in item for char in '[]="'):
            continue
        result.append(_native_scalar(item))
    return result or None


def _map(value: str):
    if not (value.startswith("{") and value.endswith("}")):
        return None
    preview = value[1:10] if len(value) > 10 else value[1:-1]
    if '"' in preview or value.startswith('{"'):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
    inner = value[1:-1].strip()
    if not inner:
        return {}
    if any(char in inner for char in "()[]"):
        return None
    result = {}
    for pair in inner.split(","):
        if "=" not in pair:
            continue
        key, item = (part.strip() for part in pair.split("=", 1))
        if any(char in key for char in '{}="') or any(char in item for char in '{}="'):
            continue
        result[str(_native_scalar(key))] = _native_scalar(item)
    return result or None


def _struct(value: str):
    if not (value.startswith("{") and value.endswith("}")):
        return None
    preview = value[1:10] if len(value) > 10 else value[1:-1]
    if '"' in preview or value.startswith('{"'):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
    inner = value[1:-1].strip()
    if not inner:
        return {}
    if "=" not in inner:
        return {str(i): _native_scalar(item.strip()) for i, item in enumerate(inner.split(","))}
    result = {}
    for pair in inner.split(","):
        if "=" not in pair:
            continue
        key, item = (part.strip() for part in pair.split("=", 1))
        if any(char in key for char in '{}="') or any(char in item for char in '{}="'):
            continue
        result[key] = _native_scalar(item)
    return result or None


_CONVERTERS: Dict[str, Callable[[str], Any]] = {
    "boolean": _boolean,
    "tinyint": int,
    "smallint": int,
    "integer": int,
    "bigint": int,
    "float": float,
    "real": float,
    "double": float,
    "timestamp": _timestamp,
    "timestamp with time zone": _timestamp_with_tz,
    "date": _date,
    "time": _time,
    "varbinary": _binary,
    "array": _array,
    "map": _map,
    "row": _struct,
    "decimal": _decimal,
    "json": json.loads,
}


def convert_athena_value(value: Optional[str], type_name: str) -> Any:
    """Convert one Row/Datum value with PyAthena 3.19-compatible semantics.

    Unknown types and scalar conversion failures retain their raw string. Complex native values
    intentionally use PyAthena's stricter contract: unsupported nested or fully filtered
    array/map/row representations return ``None``; valid JSON containers remain intact.
    """
    if value is None:
        return None
    base = re.sub(r"\([^)]*\)", "", (type_name or "").lower()).strip()
    converter = _CONVERTERS.get(base)
    if converter is None:
        return value
    try:
        return converter(value)
    except (TypeError, ValueError, DecimalException, binascii.Error, json.JSONDecodeError):
        return value
