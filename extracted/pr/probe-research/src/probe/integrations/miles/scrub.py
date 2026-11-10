"""Make Miles arguments safe to record: credential keys and URIs scrubbed, opaque env payloads dropped."""

from __future__ import annotations

import argparse
import json
import math
import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

_CREDENTIAL_URI = re.compile(r"(?P<scheme>[A-Za-z][A-Za-z0-9+.-]*://)[^/@\s]+@")
_SENSITIVE_KEYS = {
    "api_key",
    "apikey",
    "aws_access_key_id",
    "authorization",
    "auth_token",
    "access_token",
    "bearer_token",
    "cookie",
    "credential",
    "credentials",
    "id_token",
    "password",
    "private_key",
    "refresh_token",
    "secret",
    "token",
    "wandb_key",
}
_MODEL_TOKEN_KEYS = {
    "bos_token",
    "cls_token",
    "eos_token",
    "mask_token",
    "pad_token",
    "sep_token",
    "stop_token",
    "unk_token",
}
_OPAQUE_CONFIG_KEYS = {"env", "env_report", "env_vars", "environment_variables"}


def _is_sensitive_key(key: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")
    parts = set(normalized.split("_"))
    token_secret = normalized.endswith("_token") and normalized not in _MODEL_TOKEN_KEYS
    signed_secret = normalized.endswith(("_signature", "_sig"))
    return (
        normalized in _SENSITIVE_KEYS
        or token_secret
        or signed_secret
        or bool(parts & {"password", "secret", "credential", "credentials"})
    )


def _scrub_string(value: str) -> str:
    scrubbed = _CREDENTIAL_URI.sub(r"\g<scheme><redacted>@", value)
    try:
        parsed = urlsplit(scrubbed)
    except ValueError:
        return scrubbed
    if not parsed.scheme or not parsed.netloc or not parsed.query:
        return scrubbed
    query = [
        (key, "<redacted>" if _is_sensitive_key(key) else item)
        for key, item in parse_qsl(parsed.query, keep_blank_values=True)
    ]
    return urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment)
    )


def _to_json_safe(value: Any, *, key: str = "") -> Any:
    if _is_sensitive_key(key):
        return "<redacted>"
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return _scrub_string(value)
    if isinstance(value, dict):
        return {
            str(item_key): _to_json_safe(item, key=str(item_key))
            for item_key, item in value.items()
        }
    if isinstance(value, (list, tuple, set)):
        return [_to_json_safe(item, key=key) for item in value]
    if isinstance(value, argparse.Namespace) or hasattr(type(value), "model_fields"):
        # Upstream nests configs (sglang, megatron): scrub their fields by key, never via repr.
        return _to_json_safe(vars(value), key=key)
    try:
        json.dumps(value)
    except (TypeError, ValueError):
        return repr(value)
    return value


def _capture_config(args) -> dict[str, Any]:
    """Serialize Miles arguments while excluding opaque environment payloads."""
    return {
        key: _to_json_safe(value, key=key)
        for key, value in vars(args).items()
        if key.lower() not in _OPAQUE_CONFIG_KEYS
    }


def _to_scalar(value: Any) -> float | None:
    if hasattr(value, "item") and callable(value.item):
        try:
            value = value.item()
        except (TypeError, ValueError, RuntimeError):
            return None
    if isinstance(value, (str, bytes, dict, list, tuple, set)) or value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return number if math.isfinite(number) else None
