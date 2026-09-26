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
THE rule (TypeScript, defined once): @ai-matrx/content-ir
source/fence-nesting.ts — the source tokenizer and matrx-frontend's splitters
import it; this module is held to it by the generated vectors. Guards: processing/blocks/tests/test_nested_fence_splitting.py
and the shared package-generated vectors,
processing/blocks/tests/test_fence_nesting_vectors.py.
"""

from __future__ import annotations

from typing import Literal

InnerFenceLine = Literal["content", "open-nested", "close-nested", "close-outer"]

#: Fence languages whose body is itself a markdown document.
NESTING_FENCE_LANGUAGES: frozenset[str] = frozenset({"markdown", "md", "mdx"})


#: The whitespace a fence line may carry: CommonMark's ASCII whitespace ONLY.
#: Defined explicitly because Python's ``str.strip()`` also strips U+0085 and
#: U+001C–U+001F while JavaScript's ``trim()`` strips U+FEFF instead — the two
#: twins disagreed on such lines (verify-RC-B3 residual R4). Mirrors
#: ``FENCE_WHITESPACE`` in the TypeScript rule.
FENCE_WHITESPACE = " \t\n\r\f\v"


def trim_fence_line(line: str) -> str:
    """Strip FENCE_WHITESPACE (and nothing else) from both ends of a line."""
    return line.strip(FENCE_WHITESPACE)


#: The whitespace around a fence OPENER and inside its info string: exactly
#: JavaScript's ``String#trim()`` / ``/\s/`` set (ECMAScript WhiteSpace +
#: LineTerminator), because the renderer parses openers that way. Python's
#: ``str.strip()`` / ``str.split()`` differ on U+0085, U+001C–U+001F (not JS
#: whitespace) and U+FEFF (JS whitespace) — verify-RC-B3 residual R4′. Mirrors
#: ``FENCE_OPENER_WHITESPACE`` in the TypeScript rule; the shared vectors pin it.
FENCE_OPENER_WHITESPACE = (
    "\t\n\v\f\r \u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007"
    "\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000\ufeff"
)


def parse_fence_opener(line: str) -> tuple[int, str] | None:
    """Parse a backtick fence OPENER the renderer's way: ``(ticks, lang)`` or None."""
    trimmed = line.strip(FENCE_OPENER_WHITESPACE)
    ticks = 0
    while ticks < len(trimmed) and trimmed[ticks] == "`":
        ticks += 1
    if ticks < 3:
        return None
    info = trimmed[ticks:].lstrip(FENCE_OPENER_WHITESPACE)
    end = 0
    while end < len(info) and info[end] not in FENCE_OPENER_WHITESPACE:
        end += 1
    return ticks, info[:end]


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
    info = trim_fence_line(trimmed[ticks:])
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
