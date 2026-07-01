"""Per-tool output size caps to prevent context flooding."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


# Default per-tool max char counts.
DEFAULT_LIMITS: Dict[str, int] = {
    "read_file": 100_000,
    "search_files": 50_000,
    "terminal": 50_000,
    "process": 50_000,
    "web_search": 30_000,
    "web_extract": 80_000,
    "browser_snapshot": 30_000,
    "session_search": 30_000,
    "execute_code": 50_000,
    "vision_analyze": 20_000,
    "default": 40_000,
}


@dataclass
class TruncationResult:
    output: str
    truncated: bool
    original_length: int


def get_limit(tool: str, overrides: Dict[str, int] | None = None) -> int:
    if overrides and tool in overrides:
        return int(overrides[tool])
    return int(DEFAULT_LIMITS.get(tool, DEFAULT_LIMITS["default"]))


def truncate_output(tool: str, output: Any, *, overrides: Dict[str, int] | None = None) -> TruncationResult:
    text = output if isinstance(output, str) else str(output)
    limit = get_limit(tool, overrides)
    if len(text) <= limit:
        return TruncationResult(text, False, len(text))
    head = limit // 2
    tail = limit - head - 64  # leave room for the notice
    if tail < 0:
        tail = 0
    notice = f"\n\n[truncated {len(text) - limit} chars — kept first {head} + last {tail}]\n\n"
    truncated = text[:head] + notice + (text[-tail:] if tail > 0 else "")
    return TruncationResult(truncated, True, len(text))


__all__ = ["DEFAULT_LIMITS", "TruncationResult", "get_limit", "truncate_output"]
