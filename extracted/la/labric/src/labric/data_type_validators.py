from __future__ import annotations

from datetime import datetime


def parse_bool(
    value: str | int | float | bool,
    acceptable_truthy_values: list[str] | None = None,
    acceptable_falsey_values: list[str] | None = None,
    case_sensitive: bool = False,
) -> bool:
    if acceptable_truthy_values is None:
        acceptable_truthy_values = ["true", "1", "yes"]
    if acceptable_falsey_values is None:
        acceptable_falsey_values = ["false", "0", "no"]
    if isinstance(value, (int, float, bool)) and float(value).is_integer():
        value = int(value)
    value = str(value).strip()
    if not case_sensitive:
        value = value.lower()
        acceptable_truthy_values = [v.lower() for v in acceptable_truthy_values]
        acceptable_falsey_values = [v.lower() for v in acceptable_falsey_values]
    if value in acceptable_truthy_values:
        return True
    if value in acceptable_falsey_values:
        return False
    raise ValueError(f"Invalid boolean value: {value}")


def parse_int(
    value: str | int | float,
    allow_empty: bool = False,
    truncate_floats: bool = True,
) -> int | None:
    if isinstance(value, str):
        value = value.strip()
        if not value:
            if allow_empty:
                return None
            raise ValueError("Invalid integer value: empty string")
        try:
            return int(value)
        except ValueError:
            pass
    elif isinstance(value, int) and not isinstance(value, bool):
        return value
    try:
        value_as_float = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid integer value: {value}")
    if not value_as_float.is_integer() and not truncate_floats:
        raise ValueError(
            f"Invalid integer value: {value} is not a whole number. Set truncate_floats=True to allow truncation."
        )
    return int(value_as_float)


def parse_float(value: str | int | float, allow_empty: bool = False) -> float | None:
    if isinstance(value, str):
        value = value.strip()
        if not value:
            if allow_empty:
                return None
            raise ValueError("Invalid float value: empty string")
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid float value: {value}")


def parse_datetime(
    value: str | datetime,
    formats: list[str] | None = None,
    allow_empty: bool = False,
) -> datetime | None:
    if isinstance(value, datetime):
        return value
    value = str(value).strip()
    if not value:
        if allow_empty:
            return None
        raise ValueError("Invalid datetime value: empty string")
    for fmt in formats or ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise ValueError(f"Invalid datetime value: {value}")
