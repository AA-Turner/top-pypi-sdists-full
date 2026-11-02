"""Bounded UTF-8 source files and stdin for research publications."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from labqoat.json_document import JsonDocument


class MemoryInput:
    """Load authored research content without shell interpolation or unbounded reads."""

    maximum_bytes = 2_097_152

    @staticmethod
    def text(source: str) -> str:
        """Read an explicit file or stdin within the publication byte limit."""
        if source == "-":
            text = sys.stdin.read(MemoryInput.maximum_bytes + 1)
        else:
            path = Path(source)
            if path.stat().st_size > MemoryInput.maximum_bytes:
                raise ValueError("Research input exceeds 2 MiB.")
            text = path.read_text(encoding="utf-8")
        if len(text.encode("utf-8")) > MemoryInput.maximum_bytes:
            raise ValueError("Research input exceeds 2 MiB.")
        return text

    @staticmethod
    def document(source: str) -> JsonDocument:
        """Read a JSON object for a publication or typed research properties."""
        return JsonDocument.expect_dict(json.loads(MemoryInput.text(source)))
