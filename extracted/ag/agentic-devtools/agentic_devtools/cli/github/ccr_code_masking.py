"""Public code-span masking helpers for CCR review-body parsers."""

from __future__ import annotations

import re

_FENCE_DELIM_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")
_INLINE_CODE_RE = re.compile(r"(?<!`)(?P<ticks>`+)(?!`)[^\n]*?(?<!`)(?P=ticks)(?!`)")


def mask_fenced_blocks(text: str) -> str:
    """Return *text* with every fenced-code line replaced by equal-length spaces.

    Offsets are preserved so a match found on the masked text can be used to
    slice the original. Fenced excerpts may contain Markdown headings and
    formatting that must not be mistaken for review-body structure.
    """
    masked: list[str] = []
    open_delim: str | None = None
    for line in text.split("\n"):
        match = _FENCE_DELIM_RE.match(line)
        if open_delim is None:
            if match:
                if match.group(1).startswith("`") and "`" in line[match.end() :]:
                    masked.append(line)
                    continue
                open_delim = match.group(1)
                masked.append(" " * len(line))
                continue
            masked.append(line)
            continue
        if (
            match
            and match.group(1)[0] == open_delim[0]
            and len(match.group(1)) >= len(open_delim)
            and line[match.end() :].strip() == ""
        ):
            open_delim = None
        masked.append(" " * len(line))
    return "\n".join(masked)


def mask_inline_code(text: str) -> str:
    """Return *text* with every inline code span replaced by equal-length spaces.

    Offsets are preserved, exactly as in :func:`mask_fenced_blocks`, so results
    from either masking can be compared or used to slice the original.
    """
    return _INLINE_CODE_RE.sub(lambda match: " " * len(match.group(0)), text)
