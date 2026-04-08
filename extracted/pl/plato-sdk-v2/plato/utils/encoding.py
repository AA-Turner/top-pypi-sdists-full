"""Base64 encoding/decoding helpers for agent runtime payloads."""

from __future__ import annotations

import base64
import json
from typing import Any


def decode_b64_json(data: str) -> dict[str, Any]:
    """Decode a base64-encoded JSON string into a dict."""
    return json.loads(base64.b64decode(data).decode())


def decode_b64(data: str) -> str:
    """Decode a base64-encoded string."""
    return base64.b64decode(data).decode()
