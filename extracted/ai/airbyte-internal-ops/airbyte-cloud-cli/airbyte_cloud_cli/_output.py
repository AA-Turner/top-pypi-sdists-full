# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Output helpers for `airbyte-cloud` commands."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any


def _json_sanitize(value: object) -> object:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return _json_sanitize(asdict(value))
    if hasattr(value, "model_dump"):
        return _json_sanitize(value.model_dump(mode="json"))  # type: ignore[no-any-return,unused-ignore]
    if hasattr(value, "to_dict"):
        return _json_sanitize(value.to_dict())  # type: ignore[no-any-return,unused-ignore]
    if isinstance(value, Mapping):
        return {str(key): _json_sanitize(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, bytes | bytearray | str):
        return [_json_sanitize(item) for item in value]
    return str(value)


def json_output(value: Any) -> None:
    """Print a JSON response to stdout."""
    print(json.dumps(_json_sanitize(value), indent=2))
