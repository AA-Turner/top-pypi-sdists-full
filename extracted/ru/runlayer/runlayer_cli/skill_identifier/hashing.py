"""Minimal SHA256 + normalization for skill identifier computation.

Duplicates the subset of backend mcp_identifiers hashing/normalization
needed for deterministic skill fingerprinting.
"""

import hashlib
import unicodedata

FIELD_DELIMITER = "|||"


def sha256_hash(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def normalize_text(text: str) -> str:
    return unicodedata.normalize("NFC", text.strip())


def _escape_delimiter(text: str, delimiter: str) -> str:
    text = text.replace("\\", "\\\\")
    text = text.replace(delimiter, f"\\{delimiter}")
    return text


def hash_fields(*fields: str) -> str:
    normalized = [normalize_text(f) for f in fields]
    escaped = [_escape_delimiter(f, FIELD_DELIMITER) for f in normalized]
    hash_input = FIELD_DELIMITER.join(escaped)
    return sha256_hash(hash_input)
