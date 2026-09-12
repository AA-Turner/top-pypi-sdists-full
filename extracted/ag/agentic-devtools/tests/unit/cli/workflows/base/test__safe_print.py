"""Tests for _safe_print helper."""

import pytest

from agentic_devtools.cli.workflows.base import _safe_print


class _Cp1252Stream:
    """Stream that rejects non-ASCII text like a cp1252 console."""

    encoding = "cp1252"

    def __init__(self) -> None:
        self.writes: list[str] = []

    def write(self, text: str) -> int:
        if any(ord(character) > 127 for character in text):
            raise UnicodeEncodeError("charmap", text, 0, len(text), "character maps to <undefined>")
        self.writes.append(text)
        return len(text)

    def flush(self) -> None:
        return None


class _FailingStream:
    """Stream that raises a non-encoding error for every write."""

    def write(self, text: str) -> int:
        raise RuntimeError("write failed")

    def flush(self) -> None:
        return None


def test_safe_print_preserves_stderr_destination_for_fallback() -> None:
    """Should write ASCII fallback output to the requested stderr stream."""
    stream = _Cp1252Stream()

    _safe_print("⚠️ warning \u2603", file=stream)

    output = "".join(stream.writes)
    assert "[WARN] warning ?" in output
    assert output.isascii()


def test_safe_print_propagates_non_encoding_errors() -> None:
    """Should not hide failures unrelated to text encoding."""
    with pytest.raises(RuntimeError, match="write failed"):
        _safe_print("message", file=_FailingStream())
