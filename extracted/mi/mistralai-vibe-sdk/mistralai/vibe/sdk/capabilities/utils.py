"""Utility helpers for SDK capabilities."""

import locale
import sys
from pathlib import Path


def resolve_path(path: str) -> Path:
    """Resolve a potentially relative path against the current working directory."""
    file_path = Path(path).expanduser()
    if not file_path.is_absolute():
        file_path = Path.cwd() / file_path
    return file_path.resolve()


def candidate_encodings(raw: bytes) -> list[str]:
    candidates = [
        _encoding_from_bom(raw),
        "utf-8",
        locale.getpreferredencoding(False),
        "cp1252",
        "latin-1",
    ]
    return list(dict.fromkeys(encoding for encoding in candidates if encoding))


def _encoding_from_bom(raw: bytes) -> str | None:
    if raw.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    if raw.startswith(b"\xff\xfe\x00\x00") or raw.startswith(b"\x00\x00\xfe\xff"):
        return "utf-32"
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return "utf-16"
    return None


def is_windows() -> bool:
    return sys.platform == "win32"
