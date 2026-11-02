"""String-literal-aware scanning of a single source line.

Helpers that normalize a line's whitespace for comparison (`collapse_ws`,
`collapse_ws_outside_strings`) or skip past a string literal (`consume_string`)
without being fooled by a quote's contents. They live apart from the rules so
each rule module stays readable rather than mixing rules with char-scanners.

Conservative by design: `collapse_ws_outside_strings` leaves string interiors
intact, so a real edit inside a literal can't masquerade as a harmless reflow.
"""

from __future__ import annotations


def collapse_ws(text: str) -> str:
    """Collapse all whitespace runs to single spaces and trim."""
    return " ".join(text.split())


def collapse_ws_outside_strings(text: str, quotes: str = "\"'`") -> str:
    """Collapse whitespace runs, but leave the contents of string literals intact.

    Used by wrap detection: re-wrapping code only moves whitespace *between*
    tokens, never inside a string. Collapsing string interiors too would let a
    real edit like `"a  b"` -> `"a b"` look like a harmless reflow.
    """
    out: list[str] = []
    i, n = 0, len(text)
    pending_space = False
    while i < n:
        ch = text[i]
        if ch in quotes:
            close = consume_string(text, i)
            out.append(text[i:close])
            i = close
            pending_space = False
        elif ch.isspace():
            if out and not pending_space:
                out.append(" ")
                pending_space = True
            i += 1
        else:
            out.append(ch)
            pending_space = False
            i += 1
    return "".join(out).rstrip()


def scan_string(text: str, i: int) -> int | None:
    """Index just past the string opened at `text[i]`, or None if it is never
    closed. Escapes are skipped forward (`\\` consumes the next char), so an
    escaped quote or backslash right before the close (`"a\\\\"`) can't end the
    string early. This is the single place the escape rule lives — both
    `consume_string` (below) and the tokenizer build on it."""
    quote = text[i]
    # A triple-quoted string (`'''…'''` / `\"\"\"…\"\"\"`) is one delimiter, not three:
    # pairwise scanning would close on the first apostrophe inside
    # (`'''don't'''`) and desync everything after it — a `#` later in the
    # literal would read as a comment. An unclosed triple continues on another
    # line, which a single-line scanner can't judge, so it stays None (callers
    # decline).
    if quote in "\"'" and text[i : i + 3] == quote * 3:
        close = text.find(quote * 3, i + 3)
        return None if close == -1 else close + 3
    i += 1
    n = len(text)
    while i < n:
        if text[i] == "\\":
            i += 2  # skip an escaped char (e.g. \\ or \")
            continue
        if text[i] == quote:
            return i + 1
        i += 1
    return None


def consume_string(text: str, i: int) -> int:
    """Given `i` at an opening quote, return the index just past its close, or the
    end of the text if the string is unterminated — the form scanners want when
    they treat an unterminated literal as running to end-of-line (vs the
    tokenizer, which uses `scan_string` directly to bail on a `None`)."""
    close = scan_string(text, i)
    return len(text) if close is None else close
