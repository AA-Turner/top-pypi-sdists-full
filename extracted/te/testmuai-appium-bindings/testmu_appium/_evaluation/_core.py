"""Deterministic comparison primitives (transforms + operators + composite) used by the
binding's assertion and branch evaluation, with color normalization backed by the static
NAMED_COLORS map instead of webcolors. Stdlib-only — safe to import without playwright/aiohttp."""
import json
import re as _re_mod

from ._colors import NAMED_COLORS


def _normalize_color(value: str) -> str:
    """Normalize a CSS color value to canonical rgb(R, G, B) format."""
    value = value.strip().lower()
    rgb_match = _re_mod.match(
        r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*[\d.]+\s*)?\)",
        value,
    )
    if rgb_match:
        r, g, b = int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3))
        return f"rgb({r}, {g}, {b})"
    hex_match = _re_mod.match(r"#([0-9a-f]{6})$", value)
    if hex_match:
        hex_str = hex_match.group(1)
        r, g, b = int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)
        return f"rgb({r}, {g}, {b})"
    hex3_match = _re_mod.match(r"#([0-9a-f]{3})$", value)
    if hex3_match:
        hex_str = hex3_match.group(1)
        r = int(hex_str[0] * 2, 16)
        g = int(hex_str[1] * 2, 16)
        b = int(hex_str[2] * 2, 16)
        return f"rgb({r}, {g}, {b})"
    # Named color via static CSS map (parity with webcolors.name_to_hex)
    hexval = NAMED_COLORS.get(value)
    if hexval is not None:
        return _normalize_color(hexval)
    return value


def apply_transforms(value: str, transforms: list[str], json_path: str | None) -> str:
    """Apply ordered transforms to a stored value before comparison."""
    for t in transforms:
        if t == "strip":
            value = value.strip()
        elif t == "lowercase":
            value = value.lower()
        elif t == "string_to_float":
            cleaned = _re_mod.sub(r"[^\d,.\-]", "", value)
            cleaned = cleaned.replace(",", "")
            match = _re_mod.search(r"-?\d+\.?\d*", cleaned)
            if match:
                value = str(float(match.group()))
        elif t == "extract_number":
            cleaned = _re_mod.sub(r"[^\d,.\-]", "", value)
            cleaned = cleaned.replace(",", "")
            match = _re_mod.search(r"-?\d+", cleaned)
            if match:
                value = match.group()
        elif t == "json_path" and json_path:
            try:
                data = json.loads(value)
                for segment in json_path.split("."):
                    if isinstance(data, dict):
                        data = data[segment]
                    elif isinstance(data, list):
                        data = data[int(segment)]
                value = str(data)
            except (KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
                pass
        elif t == "color_normalize":
            value = _normalize_color(value)
    return value


def _values_equal(a: str, b: str) -> bool:
    """Smart equality: numeric, then JSON structural, then string."""
    if a == b:
        return True
    try:
        fa, fb = float(a), float(b)
        if fa == fb:
            return True
    except (ValueError, TypeError):
        pass
    try:
        ja = json.loads(a)
        jb = json.loads(b)
        if ja == jb:
            return True
    except (json.JSONDecodeError, ValueError, TypeError):
        pass
    return False


def _try_parse_collection(value: str):
    """Try to parse a string as a JSON/Python list or dict."""
    stripped = value.strip()
    if not stripped:
        return None
    if not ((stripped.startswith("[") and stripped.endswith("]")) or
            (stripped.startswith("{") and stripped.endswith("}"))):
        return None
    try:
        parsed = json.loads(stripped)
        if isinstance(parsed, (list, dict)):
            return parsed
    except (json.JSONDecodeError, ValueError):
        pass
    try:
        converted = stripped.replace("'", '"')
        parsed = json.loads(converted)
        if isinstance(parsed, (list, dict)):
            return parsed
    except (json.JSONDecodeError, ValueError):
        pass
    if stripped.startswith("[") and stripped.endswith("]"):
        inner = stripped[1:-1].strip()
        if inner:
            items = [item.strip() for item in inner.split(",")]
            return items
    return None


def _deep_contains(needle: str, haystack) -> bool:
    """Recursively check if needle exists as a value in a collection."""
    if isinstance(haystack, dict):
        for value in haystack.values():
            if _deep_contains(needle, value):
                return True
        return False
    elif isinstance(haystack, list):
        for item in haystack:
            if _deep_contains(needle, item):
                return True
        return False
    else:
        return _values_equal(needle, str(haystack))


def _compare(actual: str, expected: str, operator: str) -> bool:
    """Deterministic comparison of actual vs expected using operator."""
    if operator == "equals":
        return _values_equal(actual, expected)
    elif operator == "contains":
        parsed = _try_parse_collection(actual)
        if parsed is not None:
            return _deep_contains(expected, parsed)
        return expected in actual
    elif operator == "not_contains":
        parsed = _try_parse_collection(actual)
        if parsed is not None:
            return not _deep_contains(expected, parsed)
        return expected not in actual
    elif operator == "not_equals":
        return not _values_equal(actual, expected)
    elif operator == "gt":
        try:
            return float(actual) > float(expected)
        except (ValueError, TypeError):
            return False
    elif operator == "gte":
        try:
            return float(actual) >= float(expected)
        except (ValueError, TypeError):
            return False
    elif operator == "lt":
        try:
            return float(actual) < float(expected)
        except (ValueError, TypeError):
            return False
    elif operator == "lte":
        try:
            return float(actual) <= float(expected)
        except (ValueError, TypeError):
            return False
    elif operator == "has_key":
        parsed = _try_parse_collection(actual)
        if isinstance(parsed, dict):
            return expected in parsed
        return False
    elif operator == "true":
        return actual.lower() in ("true", "yes", "1")
    elif operator == "false":
        return actual.lower() in ("false", "no", "0")
    return False
