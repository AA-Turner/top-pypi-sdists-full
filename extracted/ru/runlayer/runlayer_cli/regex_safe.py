"""RE2-backed regex API — the runtime replacement for stdlib ``re``.

CLI mirror of the canonical ``backend/app/core/regex_safe.py``, trimmed to
the surface the CLI uses. `subn`, and the `finditer_filtered`/`sub_filtered`
decomposition helpers, are deliberately absent: the two call sites that used
the latter both left because a rejected candidate costs a forward rescan, so
they are O(matches x len) on match-dense input. Re-add from the backend copy
verbatim if a real need appears, and check match density before doing so.
Runtime code imports this module instead of ``re``/``regex`` (enforced by
``scripts/check_regex_engine.py``). RE2 is linear-time — no catastrophic
backtracking, so no ReDoS timeouts (ENG-4056).

RE2 cannot express lookaround or in-pattern backreferences (they break the
linear-time guarantee; ``error`` is raised at compile). Semantics that differ
from stdlib and must be audited at every migration site:

- ``\\d \\w \\s \\b`` are ASCII-only (stdlib is Unicode-aware) — use
  ``STDLIB_WS`` (or a Python post-filter) where Unicode parity matters.
- ``$`` matches end-of-text only, never before a trailing newline.
- ``\\Z`` is rejected — RE2 spells it ``\\z``.
- ``re.VERBOSE``/``(?x)`` is not supported.
- Replacement templates in ``sub`` DO support ``\\1``/``\\g<name>``.
"""

from __future__ import annotations

from collections.abc import Callable
from enum import IntFlag
from typing import Any, Protocol, cast

import re2

__all__ = [
    "DOTALL",
    "IGNORECASE",
    "MULTILINE",
    "STDLIB_WS",
    "STDLIB_WS_BODY",
    "Flags",
    "Match",
    "Pattern",
    "compile",
    "error",
    "escape",
    "findall",
    "fullmatch",
    "match",
    "search",
    "split",
    "sub",
]

error = re2.error

# Exact stdlib-`re` `\s` (str mode) as an explicit RE2 character class. RE2's
# `\s` is ASCII-only ([\t\n\f\r ]); migration sites where Unicode whitespace
# is user-visible swap `\s` for this to keep stdlib behavior. Pinned by an
# exhaustive codepoint sweep in the backend's test_regex_safe.py.
STDLIB_WS_BODY = r"\t-\r \x1c-\x1f\x85\p{Z}"
STDLIB_WS = rf"[{STDLIB_WS_BODY}]"


class Match(Protocol):
    """The subset of the re2 match surface runtime code relies on."""

    def group(self, *index: int | str) -> Any: ...
    def groups(self, default: Any = None) -> tuple[Any, ...]: ...
    def start(self, group: int | str = 0) -> int: ...
    def end(self, group: int | str = 0) -> int: ...
    def span(self, group: int | str = 0) -> tuple[int, int]: ...
    def expand(self, template: str) -> str: ...


class Pattern(Protocol):
    """The subset of the re2 compiled-pattern surface runtime code relies on."""

    def search(
        self, text: str, pos: int = 0, endpos: int | None = None
    ) -> Match | None: ...
    def match(
        self, text: str, pos: int = 0, endpos: int | None = None
    ) -> Match | None: ...
    def fullmatch(
        self, text: str, pos: int = 0, endpos: int | None = None
    ) -> Match | None: ...
    def findall(self, text: str) -> list[Any]: ...
    def split(self, text: str, maxsplit: int = 0) -> list[Any]: ...
    def sub(
        self, repl: str | Callable[[Match], str], text: str, count: int = 0
    ) -> str: ...


class Flags(IntFlag):
    """Supported flags. VERBOSE is intentionally absent (RE2 has no ``(?x)``)."""

    NOFLAG = 0
    IGNORECASE = 1
    I = 1  # noqa: E741 - mirrors stdlib re.I
    MULTILINE = 2
    M = 2
    DOTALL = 4
    S = 4


IGNORECASE = Flags.IGNORECASE
MULTILINE = Flags.MULTILINE
DOTALL = Flags.DOTALL

# One shared Options instance: re2.compile's internal LRU cache is keyed by
# (pattern, options), so a per-call Options object would defeat caching.
# log_errors=False stops RE2's C++ layer from writing parse failures to stderr.
_OPTIONS = re2.Options()
_OPTIONS.log_errors = False

_INLINE = {Flags.IGNORECASE: "i", Flags.MULTILINE: "m", Flags.DOTALL: "s"}


def _wrap(pattern: str, flags: Flags) -> str:
    """Fold flags into the pattern as an inline non-capturing group.

    ``(?ims:...)`` does not introduce a capturing group, so group numbering
    is identical to the unwrapped pattern.
    """
    if not flags:
        return pattern
    letters = "".join(c for f, c in _INLINE.items() if flags & f)
    return f"(?{letters}:{pattern})"


def _reject_byte_escape(pattern: str) -> None:
    """Reject ``\\C`` (RE2: match any single BYTE, even in UTF-8 mode).

    A byte-matcher cannot honor this wrapper's str contract: its matches can
    start or end inside a multibyte character, so spans are wrong in str mode
    (observed: ``\\C`` on ``"é"`` yields (0, 1), (1, 2) — past the end of a
    one-char string). No caller wants byte semantics from a str API, so fail
    at compile with a clear reason. Mirrored verbatim from the backend
    canonical (drift-guarded directly).
    """
    i, n = 0, len(pattern)
    in_quote = False  # inside \Q...\E every char is literal, \C included
    while i < n:
        if in_quote:
            # RE2 does NO escape processing inside \Q...\E: a backslash is a
            # plain literal and the quote ends at the first literal 2-char
            # \E. Advancing by escape PAIRS here desynced on `\Q\\E\C` — the
            # pair-walk ate the backslash RE2 uses for \E, stayed in-quote,
            # and let a live \C through. Scan one char at a time.
            if pattern[i] == "\\" and i + 1 < n and pattern[i + 1] == "E":
                in_quote = False
                i += 2
                continue
            i += 1
            continue
        if pattern[i] == "\\" and i + 1 < n:
            nxt = pattern[i + 1]
            if nxt == "Q":
                in_quote = True
            elif nxt == "C":
                raise error(
                    r"\C matches a raw byte and can split multibyte "
                    "characters, so str match offsets cannot be kept "
                    "correct; it is not supported"
                )
            i += 2  # an escape pair; `\\C` is a literal backslash then C
            continue
        i += 1


def compile(pattern: str, flags: Flags = Flags.NOFLAG) -> Pattern:  # noqa: A001 - mirrors stdlib re.compile
    _reject_byte_escape(pattern)
    return cast(Pattern, re2.compile(_wrap(pattern, flags), options=_OPTIONS))


def _as_pattern(pattern: str | Pattern, flags: Flags) -> Pattern:
    if isinstance(pattern, str):
        return compile(pattern, flags)
    if flags:
        raise ValueError("cannot pass flags with a pre-compiled pattern")
    return pattern


def search(
    pattern: str | Pattern, text: str, flags: Flags = Flags.NOFLAG
) -> Match | None:
    return _as_pattern(pattern, flags).search(text)


def match(
    pattern: str | Pattern, text: str, flags: Flags = Flags.NOFLAG
) -> Match | None:
    return _as_pattern(pattern, flags).match(text)


def fullmatch(
    pattern: str | Pattern, text: str, flags: Flags = Flags.NOFLAG
) -> Match | None:
    return _as_pattern(pattern, flags).fullmatch(text)


def findall(
    pattern: str | Pattern, text: str, flags: Flags = Flags.NOFLAG
) -> list[Any]:
    return _as_pattern(pattern, flags).findall(text)


def sub(
    pattern: str | Pattern,
    repl: str | Callable[[Match], str],
    text: str,
    count: int = 0,
    flags: Flags = Flags.NOFLAG,
) -> str:
    return _as_pattern(pattern, flags).sub(repl, text, count)


def split(
    pattern: str | Pattern,
    text: str,
    maxsplit: int = 0,
    flags: Flags = Flags.NOFLAG,
) -> list[Any]:
    return _as_pattern(pattern, flags).split(text, maxsplit)


def escape(text: str) -> str:
    return cast(str, re2.escape(text))
