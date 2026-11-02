"""Minimal source tokenizer for the type-annotation trust rule.

The rule has to tell a type-annotation ``:`` from a suite / dict / ternary /
lambda / object-value / case-label colon. That is a lexing question, so rather
than scan bytes with ever-more special cases (which kept springing leaks) we
tokenize the line first and reason about token *roles*.

Deliberately conservative and NOT a full parser: a line it can't cleanly
tokenize — an unterminated string or block comment, or brackets left open, i.e.
part of a multi-line construct it can't judge in isolation — yields ``None``, and
the rule then declines to label rather than guess. Only the two languages the
annotation rule supports (Python and TypeScript/TSX) are modeled.
"""

from __future__ import annotations

from functools import lru_cache

from .helpers import BLOCK_COMMENT_DELIMITERS, LINE_COMMENT_PREFIXES
from .linescan import scan_string

WORD = "word"  # identifier or keyword
OP = "op"  # a punctuation/operator token (`:`, `->`, `(`, `,`, `=`, …)
STRING = "string"  # a whole string literal, delimiters included
NUMBER = "number"


class Token:
    __slots__ = ("end", "kind", "start", "text")

    def __init__(self, kind: str, text: str, start: int, end: int) -> None:
        self.kind = kind
        self.text = text
        self.start = start  # char offset of the token in its source line
        self.end = end  # char offset just past the token

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"<{self.kind} {self.text!r}>"


# extension -> (line-comment prefixes, (block open, close) | None), derived from
# the shared syntax tables (helpers.py) so the tokenizer and the comments rule
# can never disagree about what starts a comment.
_COMMENTS: dict[str, tuple[tuple[str, ...], tuple[str, str] | None]] = {
    ext: (LINE_COMMENT_PREFIXES[ext], BLOCK_COMMENT_DELIMITERS.get(ext))
    for ext in ("py", "ts", "tsx")
}

_QUOTES = "\"'`"
# The bracket vocabulary, shared with the annotation span-walker (annotations.py)
# so depth tracking can't diverge between the two.
OPEN_BRACKETS, CLOSE_BRACKETS = "([{", ")]}"


# Cached: the three token-delta rules (`_style`, `_spacing`,
# `_type_annotations`) each tokenize the same changed lines as a hunk walks the
# rule chain, and tokenizing is the dominant per-hunk cost. The cache returns
# the SAME list to every caller — treat it as read-only.
@lru_cache(maxsize=4096)
def tokenize(line: str, ext: str) -> list[Token] | None:
    """Tokenize a single source line, or None if it can't be judged in isolation.

    Returns None on an unterminated string/block comment or unbalanced brackets —
    all signs the line is part of a multi-line construct — so callers stay
    conservative (no label) instead of guessing at a fragment.
    """
    comment_prefixes, block = _COMMENTS.get(ext, ((), None))
    tokens: list[Token] = []
    i, n = 0, len(line)
    depth = 0
    while i < n:
        ch = line[i]
        if ch.isspace():
            i += 1
        elif comment_prefixes and line.startswith(comment_prefixes, i):
            break  # rest of the line is a comment
        elif block and line.startswith(block[0], i):
            end = line.find(block[1], i + len(block[0]))
            if end == -1:
                return None  # unterminated block comment -> multi-line
            i = end + len(block[1])
        elif ch in _QUOTES:
            close = scan_string(line, i)
            if close is None:
                return None  # unterminated string -> multi-line
            tokens.append(Token(STRING, line[i:close], i, close))
            i = close
        elif ch.isalpha() or ch == "_":
            j = i + 1
            while j < n and (line[j].isalnum() or line[j] == "_"):
                j += 1
            tokens.append(Token(WORD, line[i:j], i, j))
            i = j
        elif ch.isdigit():
            j = i + 1
            while j < n and (line[j].isalnum() or line[j] in "._"):
                j += 1
            tokens.append(Token(NUMBER, line[i:j], i, j))
            i = j
        elif line.startswith("->", i):
            tokens.append(Token(OP, "->", i, i + 2))
            i += 2
        else:
            if ch in OPEN_BRACKETS:
                depth += 1
            elif ch in CLOSE_BRACKETS:
                depth -= 1
                if depth < 0:
                    return None  # more closers than openers -> can't be a line
            tokens.append(Token(OP, ch, i, i + 1))
            i += 1
    if depth != 0:
        return None  # brackets left open -> part of a multi-line construct
    return tokens
