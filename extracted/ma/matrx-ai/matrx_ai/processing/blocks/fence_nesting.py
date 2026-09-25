"""THE ONE NESTED-FENCE RULE for a ```markdown / ```md / ```mdx fence.

Models write a markdown document inside a ```markdown fence and put their own
```python ... ``` blocks inside it with the SAME three backticks. Under strict
CommonMark the first inner bare ``` closes the outer fence: the document ends
mid-way, the rest leaks out as prose, and the outer closing ``` opens a
phantom code block that swallows everything after it.

The rule, for MARKDOWN-language fences only (every other language keeps strict
CommonMark — a ```bash heredoc is code, not a document):
  - a fence line WITH an info string (```python) opens a nested fence;
  - a bare fence line (``` with at least the opener's tick count) closes the
    innermost nested fence while one is open, and closes the outer fence only
    when none is;
  - a longer outer fence (````markdown) keeps working exactly as before — an
    inner ``` is shorter than the opener, so it is plain content;
  - if the text ENDS with a nested fence still open, the extraction is redone
    under strict CommonMark (the unclosed inner fence must not eat the outer
    closer and the rest of the message).

Spec (one copy): common-docs/systems/content-ir-system/NESTED-FENCES.md.
Frontend twin: matrx-frontend components/markdown-core/fence-nesting.ts —
both sides split a message identically. Guard:
tests/test_nested_fence_splitting.py.
"""

from __future__ import annotations

from typing import Literal

InnerFenceLine = Literal["content", "open-nested", "close-nested", "close-outer"]

#: Fence languages whose body is itself a markdown document.
NESTING_FENCE_LANGUAGES: frozenset[str] = frozenset({"markdown", "md", "mdx"})


def fence_nests_inner_fences(language: str | None) -> bool:
    """True when a fence opened with this info-string language nests inner fences."""
    return bool(language) and language.lower() in NESTING_FENCE_LANGUAGES


def classify_inner_fence_line(
    trimmed: str, open_ticks: int, nests: bool, nested_depth: int
) -> InnerFenceLine:
    """Classify one TRIMMED line inside an open backtick fence."""
    ticks = 0
    while ticks < len(trimmed) and trimmed[ticks] == "`":
        ticks += 1
    if ticks < 3:
        return "content"
    info = trimmed[ticks:].strip()
    if info == "":
        if ticks < open_ticks:
            return "content"
        if nests and nested_depth > 0:
            return "close-nested"
        return "close-outer"
    # A fence line with an info string never closes anything (CommonMark).
    # Inside a markdown fence it opens a nested one — unless the outer opener
    # is LONGER, in which case the inner fence is already plain content.
    if nests and ticks >= open_ticks and "`" not in info:
        return "open-nested"
    return "content"
