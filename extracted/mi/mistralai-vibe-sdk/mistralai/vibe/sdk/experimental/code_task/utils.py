"""Shared helpers for programmatic tool calling."""

import re


def to_snake_case(name: str) -> str:
    """Convert camelCase/kebab-case to snake_case."""
    if "_" in name and name == name.lower():
        return name
    s = re.sub(r"([A-Z])", r"_\1", name).lower().lstrip("_")
    return s.replace("-", "_")
