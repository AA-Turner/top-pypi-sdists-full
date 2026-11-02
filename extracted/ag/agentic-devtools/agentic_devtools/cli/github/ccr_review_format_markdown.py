"""Focused helpers for CCR review-body parsing."""

from __future__ import annotations

import re

from agentic_devtools.cli.github.ccr_code_masking import (
    mask_fenced_blocks as _mask_fenced_blocks,
)
from agentic_devtools.cli.github.ccr_code_masking import (
    mask_inline_code as _mask_inline_code,
)

__all__ = [
    "_FENCE_DELIM_RE",
    "_INLINE_CODE_COMPARISON_RE",
    "_INLINE_CODE_RE",
    "_mask_fenced_blocks",
    "_mask_inline_code",
]

_FENCE_DELIM_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")


_INLINE_CODE_RE = re.compile(r"(?<!`)(?P<ticks>`+)(?!`)[^\n]*?(?<!`)(?P=ticks)(?!`)")

_INLINE_CODE_COMPARISON_RE = re.compile(r"(?<!`)(?P<ticks>`+)(?!`)(?s:.*?)(?<!`)(?P=ticks)(?!`)")
