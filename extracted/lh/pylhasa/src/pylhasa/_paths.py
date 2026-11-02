from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Optional


_WINDOWS_RESERVED = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
}


@dataclass(frozen=True)
class NormalizedPath:
    raw_path: str
    raw_path_bytes: bytes
    safe_path: Optional[str]
    unsafe_reason: Optional[str]


_drive_re = re.compile(r"^[A-Za-z]:")


def normalize_path(raw_path_bytes: bytes) -> NormalizedPath:
    """Normalize an archive path into a safe, platform-neutral form."""
    raw_path = raw_path_bytes.decode("utf-8", errors="replace")
    path = raw_path.replace("\\", "/")

    if path.startswith("//"):
        return NormalizedPath(raw_path, raw_path_bytes, None, "UNC paths are not allowed")
    if path.startswith("/"):
        return NormalizedPath(raw_path, raw_path_bytes, None, "absolute paths are not allowed")
    if _drive_re.match(path):
        return NormalizedPath(raw_path, raw_path_bytes, None, "Windows drive paths are not allowed")

    path = path.lstrip("/")
    parts = [p for p in path.split("/") if p not in ("", ".")]
    for part in parts:
        if part == "..":
            return NormalizedPath(raw_path, raw_path_bytes, None, "path traversal is not allowed")

    if os.name == "nt":
        for part in parts:
            base = part.split(".")[0].upper()
            if base in _WINDOWS_RESERVED:
                return NormalizedPath(raw_path, raw_path_bytes, None, "reserved Windows name")

    safe_path = "/".join(parts)
    return NormalizedPath(raw_path, raw_path_bytes, safe_path, None)
