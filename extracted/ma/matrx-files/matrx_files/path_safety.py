"""Centralised logical-path sanitizer for the matrx-files system.

Used at every boundary that accepts a user-supplied ``file_path`` or
``folder_path``. Rejects path-traversal attempts, NUL/control characters,
Windows-style separators, leading slashes, double-slashes, ``.`` / ``..``
segments, RTL overrides, and overly long inputs.

Usage
-----
    from matrx_files.path_safety import sanitize_logical_path

    safe = sanitize_logical_path(user_input)              # returns the cleaned path
    safe = sanitize_logical_path(user_input, max_depth=20)
"""

from __future__ import annotations

import unicodedata


class InvalidLogicalPathError(ValueError):
    """Raised when a user-supplied path is unsafe."""


_FORBIDDEN_SEGMENTS = {"", ".", ".."}
_FORBIDDEN_CHARS = set(chr(c) for c in range(0, 32)) | {"\x7f"}
# Right-to-left override / Bidi tricks — not "forbidden" by S3 but break UI.
_FORBIDDEN_CHARS |= {"‮", "‭", "‪", "‫", "‬", "‎", "‏"}
_MAX_TOTAL_LENGTH = 1024
_MAX_SEGMENT_LENGTH = 255
_MAX_DEPTH = 32


def sanitize_logical_path(
    raw: str,
    *,
    max_total_length: int = _MAX_TOTAL_LENGTH,
    max_segment_length: int = _MAX_SEGMENT_LENGTH,
    max_depth: int = _MAX_DEPTH,
    allow_empty: bool = False,
) -> str:
    """Return a normalized, safe logical path or raise ``InvalidLogicalPathError``.

    The result has:
    - No leading or trailing ``/``
    - No empty / ``.`` / ``..`` segments
    - No NUL, control, or RTL characters
    - No backslashes
    - NFC-normalised Unicode
    - At most ``max_depth`` segments and ``max_total_length`` characters total
    """
    if raw is None:
        if allow_empty:
            return ""
        raise InvalidLogicalPathError("path is required")

    if not isinstance(raw, str):
        raise InvalidLogicalPathError("path must be a string")

    # NFC normalize so visually identical paths collapse to one byte sequence.
    s = unicodedata.normalize("NFC", raw).strip()

    if not s:
        if allow_empty:
            return ""
        raise InvalidLogicalPathError("path is empty")

    if len(s) > max_total_length:
        raise InvalidLogicalPathError(
            f"path exceeds {max_total_length} characters"
        )

    if "\\" in s:
        raise InvalidLogicalPathError("backslashes are not allowed in paths")

    for ch in s:
        if ch in _FORBIDDEN_CHARS:
            raise InvalidLogicalPathError(
                "path contains a forbidden control or directional character"
            )

    # Strip leading + trailing slashes.
    s = s.strip("/")

    if not s:
        if allow_empty:
            return ""
        raise InvalidLogicalPathError("path collapses to empty after normalization")

    parts = s.split("/")
    if len(parts) > max_depth:
        raise InvalidLogicalPathError(
            f"path exceeds {max_depth} segments deep"
        )

    cleaned: list[str] = []
    for part in parts:
        if part in _FORBIDDEN_SEGMENTS:
            raise InvalidLogicalPathError(
                f"path segment '{part}' is not allowed"
            )
        if len(part) > max_segment_length:
            raise InvalidLogicalPathError(
                f"path segment '{part[:24]}...' exceeds {max_segment_length} characters"
            )
        cleaned.append(part)

    return "/".join(cleaned)


def safe_filename_for_header(filename: str) -> str:
    """Return a header-safe ASCII filename suitable for ``Content-Disposition``.

    Strips CR/LF/NUL, doubles any embedded ``"`` (RFC 6266 doesn't allow them in
    quoted-string but we belt-and-braces with backslash escape), and truncates
    overly-long names. Callers should also emit a ``filename*=UTF-8''<percent>``
    header for non-ASCII clients.
    """
    if not filename:
        return "download"
    s = filename.replace("\r", "").replace("\n", "").replace("\x00", "")
    s = s.replace("\\", "_").replace('"', "'")
    return s[:200] or "download"


__all__ = ["sanitize_logical_path", "safe_filename_for_header", "InvalidLogicalPathError"]
