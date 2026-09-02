# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


import base64
from typing import Any

#: Storage-key suffix for a metadata value whose in-memory form is ``bytes``.
#: A key spelled differently from its field is NORMAL here — see the root
#: CLAUDE.md rule "A persisted shape has ONE deserializer"; the decode side is
#: :func:`decode_binary_metadata`, consumed by ``reconstruct_content``.
B64_SUFFIX = "__b64"


def encode_binary_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """JSON-safe, LOSSLESS encoding of a content block's metadata.

    ``bytes`` values ride under ``<key>__b64``; everything else is passed
    through verbatim, and a value that is neither bytes nor JSON-serializable
    is dropped (it could not have survived a jsonb write anyway).

    🚨 This is the ONLY sanctioned way to put binary provider-continuity
    material (Gemini's ``google_thought_signature``, OpenAI's
    ``encrypted_content``) into a serialized content block. The human-readable
    ``<bytes length=N>`` placeholder that ``_sanitize_metadata`` produces is a
    DISPLAY form for ``__repr__`` and must never reach a dict that anything
    rebuilds a request from: a Gemini turn re-issued with the placeholder as
    its ``thoughtSignature`` dies inside the SDK with 151 validation errors
    before the request leaves the process (the 2026-08-16 wire-replay defect).
    """
    import json

    encoded: dict[str, Any] = {}
    for key, value in metadata.items():
        if isinstance(value, (bytes, bytearray)):
            encoded[f"{key}{B64_SUFFIX}"] = base64.b64encode(bytes(value)).decode("ascii")
            continue
        try:
            json.dumps(value)
        except (TypeError, ValueError):
            continue  # non-JSON-serializable, non-bytes — drop
        encoded[key] = value
    return encoded


#: The DISPLAY placeholders `_sanitize_metadata` / `_sanitize_signature` emit.
#: A serialized payload containing one was written by a redacting serializer and
#: the real value is GONE — it can be read by a human but never re-issued.
_DISPLAY_PLACEHOLDER_PREFIXES = ("<bytes length=", "<str length=", "<bytes len=")


def contains_display_placeholder(payload: Any) -> bool:
    """True if any string in ``payload`` is a redaction placeholder.

    The ONE definition of "this recorded payload is not re-issuable because its
    binary material was replaced by a human-readable stand-in". Consumers that
    rebuild a request from a recording (wire replay, proof selection) ask this
    rather than each inventing its own string test — and rather than discovering
    it as 151 opaque SDK validation errors.
    """
    if isinstance(payload, str):
        return payload.startswith(_DISPLAY_PLACEHOLDER_PREFIXES)
    if isinstance(payload, dict):
        return any(contains_display_placeholder(value) for value in payload.values())
    if isinstance(payload, (list, tuple)):
        return any(contains_display_placeholder(item) for item in payload)
    return False


def decode_binary_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """Inverse of :func:`encode_binary_metadata` — ``<key>__b64`` back to bytes.

    Corrupt base64 omits that ONE key rather than crashing the rebuild: this
    runs on every conversation-history reconstruction, and a cosmetic decode
    failure must never take a live request down.
    """
    decoded: dict[str, Any] = {}
    for key, value in metadata.items():
        if key.endswith(B64_SUFFIX) and isinstance(value, str):
            try:
                decoded[key[: -len(B64_SUFFIX)]] = base64.b64decode(value)
            except Exception:
                continue
        else:
            decoded[key] = value
    return decoded


def truncate_base64_in_dict(d: Any, min_length: int = 100) -> Any:
    """
    Recursively truncate base64 data in any dict structure for debug printing.

    Looks for common base64 field names across all API formats:
    - Google: inlineData.data
    - OpenAI: image.data, data
    - Anthropic: source.data
    - Generic: base64_data, base64, data (if looks like base64)

    Args:
        d: The dict/list/value to process
        min_length: Minimum string length to consider for truncation (default 100)

    Returns:
        A copy with base64 data truncated to "<N chars>" format

    Example:
        >>> payload = message.to_google_content()
        >>> print(truncate_base64_in_dict(payload))  # Safe for debug output
    """
    if isinstance(d, dict):
        result = {}
        for key, value in d.items():
            # Known base64 field names
            if (
                key in ("data", "base64_data", "base64")
                and isinstance(value, str)
                and len(value) > min_length
            ):
                # Check if it looks like base64 (alphanumeric + /+=)
                if all(c.isalnum() or c in "/+=" for c in value[:100]):
                    result[key] = f"<{len(value)} chars>"
                else:
                    result[key] = value
            else:
                result[key] = truncate_base64_in_dict(value, min_length)
        return result
    elif isinstance(d, list):
        return [truncate_base64_in_dict(item, min_length) for item in d]
    else:
        return d
