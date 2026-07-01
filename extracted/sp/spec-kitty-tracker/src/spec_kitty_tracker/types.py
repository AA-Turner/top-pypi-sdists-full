"""Shared type aliases for the spec-kitty-tracker package."""

from __future__ import annotations

from typing import Union

# Recursive type alias — the string form avoids the forward-reference
# NameError at runtime in Python 3.11.
JSONValue = Union[
    str, int, float, bool, None, list["JSONValue"], dict[str, "JSONValue"]
]
