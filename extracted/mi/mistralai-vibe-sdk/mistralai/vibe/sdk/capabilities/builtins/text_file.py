import os
import stat
from pathlib import Path

from mistralai.vibe.sdk.capabilities.utils import candidate_encodings

SNIFF_BYTES = 4_096


def read_text_file(file_path: Path, *, max_bytes: int) -> tuple[str, str]:
    """Read a bounded regular text file and return its content and encoding."""
    try:
        file_status = file_path.stat()
    except FileNotFoundError as exc:
        raise ValueError(f"File not found at: {file_path}") from exc
    except OSError as exc:
        raise ValueError(f"Error reading {file_path}: {exc}") from exc
    if stat.S_ISDIR(file_status.st_mode):
        raise ValueError(f"Path is a directory, not a file: {file_path}")
    if not stat.S_ISREG(file_status.st_mode):
        raise ValueError(f"Path is not a regular file: {file_path}")

    try:
        with file_path.open("rb") as handle:
            opened_file_status = os.fstat(handle.fileno())
            if not stat.S_ISREG(opened_file_status.st_mode):
                raise ValueError(f"Path is not a regular file: {file_path}")
            if opened_file_status.st_size > max_bytes:
                raise ValueError(f"File exceeds {max_bytes} byte edit limit: {file_path}")
            raw = handle.read(max_bytes + 1)
    except FileNotFoundError as exc:
        raise ValueError(f"File not found at: {file_path}") from exc
    except IsADirectoryError as exc:
        raise ValueError(f"Path is a directory, not a file: {file_path}") from exc
    except OSError as exc:
        raise ValueError(f"Error reading {file_path}: {exc}") from exc
    if len(raw) > max_bytes:
        raise ValueError(f"File exceeds {max_bytes} byte edit limit: {file_path}")

    for encoding in candidate_encodings(raw[:SNIFF_BYTES]):
        try:
            content = raw.decode(encoding, errors="strict")
        except UnicodeDecodeError:
            continue
        if _looks_binary(content, raw, encoding):
            raise ValueError(f"Binary files are not supported: {file_path}")
        return content, encoding

    raise ValueError(f"Could not decode text file with supported encodings: {file_path}")


def _looks_binary(content: str, raw: bytes, encoding: str) -> bool:
    has_control_characters = any(
        character not in "\t\n\r\v\f\x1c\x1d\x1e\x85"
        and (ord(character) < 32 or 127 <= ord(character) <= 159)
        for character in content[:SNIFF_BYTES]
    )
    has_unexpected_null = encoding not in {"utf-16", "utf-32"} and b"\x00" in raw
    return has_control_characters or has_unexpected_null
