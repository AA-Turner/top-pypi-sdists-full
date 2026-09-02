import math
import re
from collections.abc import Mapping, Sequence
from types import MappingProxyType
from typing import Any, cast

# A type definition for basic JSON-like structures
JsonPrimitive = str | int | float | bool | None
JsonValue = JsonPrimitive | Sequence[Any] | Mapping[str, Any]
JsonSequence = Sequence[JsonValue]
JsonMapping = Mapping[str, JsonValue]

_CREDENTIAL_EXACT_MATCHES: frozenset[str] = frozenset(
    {
        "password",
        "token",
        "api_key",
        "secret",
        "authorization",
        "client_secret",
        "bearer_token",
        "access_token",
        "refresh_token",
        "session_key",
        "signing_key",
        "api_secret",
    }
)

_CREDENTIAL_TOKEN_WORDS: frozenset[str] = frozenset(
    {
        "password",
        "token",
        "secret",
        "authorization",
    }
)

_CREDENTIAL_SUFFIX_ALIASES: frozenset[tuple[str, str]] = frozenset(
    {
        ("api", "key"),
        ("session", "key"),
        ("signing", "key"),
    }
)


def _is_fuzzy_credential_alias(parts: tuple[str, ...]) -> bool:
    if len(parts) < 2:
        return False
    if parts[-1] in _CREDENTIAL_TOKEN_WORDS:
        return True
    return tuple(parts[-2:]) in _CREDENTIAL_SUFFIX_ALIASES


_CAMEL_UPPER_BOUNDARY = re.compile(r"([A-Z]+)([A-Z][a-z])")
_CAMEL_LOWER_BOUNDARY = re.compile(r"([a-z\d])([A-Z])")


def _normalize_key(key: str) -> str:
    """Normalize a key to snake_case for matching against credential patterns.

    Handles camelCase boundaries (``accessToken`` → ``access_token``,
    ``APIKey`` → ``api_key``), hyphen separators (``api-key`` → ``api_key``),
    and case folding.
    """
    s = _CAMEL_UPPER_BOUNDARY.sub(r"\1_\2", key)
    s = _CAMEL_LOWER_BOUNDARY.sub(r"\1_\2", s)
    return s.lower().replace("-", "_")


def _is_credential_key(key: str) -> bool:
    normalized_key = _normalize_key(key)
    if normalized_key in _CREDENTIAL_EXACT_MATCHES:
        return True

    parts = tuple(part for part in normalized_key.split("_") if part)
    return _is_fuzzy_credential_alias(parts)


def _validate_json_key(key: Any) -> str:
    if not isinstance(key, str):
        raise TypeError("JSON object keys must be strings")
    return key


def _validate_json_leaf(value: Any) -> JsonPrimitive:
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"Non-finite float values are not valid JSON: {value!r}")
        return value
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    raise TypeError(f"Unsupported JSON value type: {type(value).__name__}")


def freeze_json(value: JsonValue) -> JsonValue:
    """
    Recursively freezes a JSON-like structure into an immutable form.
    Dictionaries become MappingProxyType, lists become tuples.
    Also redacts credential keys during the freezing process.
    """
    if isinstance(value, Mapping):
        mapping_val = cast(Mapping[str, JsonValue], value)
        return MappingProxyType(
            {
                validated_key: "<redacted>" if _is_credential_key(validated_key) else freeze_json(v)
                for k, v in mapping_val.items()
                for validated_key in (_validate_json_key(k),)
            }
        )
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        seq_val = cast(Sequence[JsonValue], value)
        return tuple(freeze_json(v) for v in seq_val)
    return _validate_json_leaf(value)


def freeze_json_verbatim(value: JsonValue) -> JsonValue:
    """
    Recursively freezes a JSON-like structure into an immutable form
    without redacting any values. Dictionaries become MappingProxyType,
    lists become tuples.

    Use this for transport payloads (e.g. ``TaskRequest.parameters``) that
    must reach the provider intact; use ``freeze_json`` for audit artifacts
    or metadata where credential redaction is desired.
    """
    if isinstance(value, Mapping):
        mapping_val = cast(Mapping[str, JsonValue], value)
        return MappingProxyType(
            {
                validated_key: freeze_json_verbatim(v)
                for k, v in mapping_val.items()
                for validated_key in (_validate_json_key(k),)
            }
        )
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        seq_val = cast(Sequence[JsonValue], value)
        return tuple(freeze_json_verbatim(v) for v in seq_val)
    return _validate_json_leaf(value)


def thaw_json(value: JsonValue) -> JsonValue:
    """
    Rehydrates a canonically frozen JSON structure back into a standard
    JSON-serializable form (dict and list).
    """
    if isinstance(value, Mapping):
        mapping_val = cast(Mapping[str, JsonValue], value)
        return {_validate_json_key(k): thaw_json(v) for k, v in mapping_val.items()}
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        seq_val = cast(Sequence[JsonValue], value)
        return [thaw_json(v) for v in seq_val]
    return _validate_json_leaf(value)


def redact_credentials(value: JsonValue) -> JsonValue:
    """
    Recursively redacts credentials in a mutable JSON structure
    without freezing it.
    """
    if isinstance(value, Mapping):
        mapping_val = cast(Mapping[str, JsonValue], value)
        return {
            validated_key: "<redacted>" if _is_credential_key(validated_key) else redact_credentials(v)
            for k, v in mapping_val.items()
            for validated_key in (_validate_json_key(k),)
        }
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        seq_val = cast(Sequence[JsonValue], value)
        return [redact_credentials(v) for v in seq_val]
    return _validate_json_leaf(value)
