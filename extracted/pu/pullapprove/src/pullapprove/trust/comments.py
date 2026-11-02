"""Trust rule: hunks that only touch comments, plus the comment-syntax tables."""

from __future__ import annotations

from collections.abc import Callable

from ..diff import DiffCode, DiffFile, DiffHunk
from .delta import paired_changed_lines
from .helpers import (
    BLOCK_COMMENT_DELIMITERS,
    LINE_COMMENT_PREFIXES,
    change_suffix,
    extension,
    leading_indent,
)
from .labels import Trust
from .linescan import consume_string

# Languages whose strings can be backtick-delimited (JS/TS template literals, Go
# raw strings) — without this a `//` inside one reads as a comment.
_BACKTICK_LANGS = frozenset(
    ["js", "jsx", "ts", "tsx", "mjs", "mts", "cjs", "cts", "go"]
)

# Comments that DIRECT TOOLS rather than inform readers: linter suppressions,
# type-checker escapes, formatter/coverage toggles, compiler and bundler pragmas.
# Changing one changes how tools treat the surrounding code — a real edit, not
# comment churn — so a changed comment containing any of these is never trusted.
# Matched case-insensitively as substrings, deliberately loose: a prose comment
# that merely *mentions* a marker declines too, which only costs coverage (the
# hunk is shown), never hides a change. Start with the most common tools; extend
# as they come up.
_DIRECTIVE_MARKERS = (
    # Python
    "noqa",  # flake8/ruff suppression
    "pylint:",  # pylint suppression/config
    "nopep8",  # pep8/autopep8 suppression
    "skipcq",  # DeepSource suppression
    "type: ignore",  # mypy/pyright escape
    "pragma:",  # coverage.py (pragma: no cover)
    "doctest:",  # doctest directive (e.g. doctest: +SKIP)
    "fmt: off",  # black/ruff formatter toggles
    "fmt: on",
    "fmt: skip",
    "yapf:",  # yapf formatter toggle
    "ruff:",
    "mypy:",
    "pyright:",
    "pyre-ignore",  # Meta's Pyre type checker
    "pyre-fixme",
    "pytype:",  # Google's pytype type checker
    "isort:",
    "nosec",  # bandit
    "coding:",  # PEP 263 encoding declaration
    "coding=",
    # JS/TS
    "eslint-",  # eslint-disable / -enable / -disable-next-line / -disable-line
    "@ts-",  # @ts-ignore / @ts-expect-error / @ts-nocheck / @ts-check
    "prettier-ignore",
    "biome-ignore",
    "istanbul ignore",
    "c8 ignore",
    "v8 ignore",
    "sourcemappingurl",  # //# sourceMappingURL=…
    "webpackchunkname",  # webpack magic comments
    "webpackmode",
    # Go
    "go:build",
    "go:generate",
    "go:embed",
    "+build",
    "nolint",  # golangci-lint; also covers clang-tidy's NOLINT
    # Ruby
    "rubocop:",
    "frozen_string_literal",
    "typed:",  # sorbet
    # Shell
    "shellcheck",
    # C/C++
    "clang-format",
)


def _has_directive(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in _DIRECTIVE_MARKERS)


def _is_shebang(line: DiffCode) -> bool:
    """A `#!` interpreter line at file line 1 — execution semantics, not a
    comment (deeper in a file, `#!` is just comment text)."""
    return line.content.startswith("#!") and 1 in (
        line.old_line_number,
        line.new_line_number,
    )


def _string_quotes(ext: str) -> str:
    """The quote characters that open a string literal in this language."""
    return "\"'`" if ext in _BACKTICK_LANGS else "\"'"


def strip_inline_comment(
    line: str, prefixes: tuple[str, ...], quotes: str = "\"'"
) -> str:
    """Drop a trailing line-comment, ignoring prefixes inside string literals.

    A prefix only starts a comment at line-start or after whitespace — glued to a
    preceding token it is part of a value, not a comment (YAML/shell treat it that
    way, and a URL fragment `url: https://x/#frag` must not read as a `#` comment).
    Requiring the space is conservative elsewhere too: it can only *miss* a
    space-less comment like `x=1#c`, never hide a real change."""
    text = line.strip()
    i, n = 0, len(text)
    while i < n:
        if text[i] in quotes:
            i = consume_string(text, i)
        elif text.startswith(prefixes, i) and (i == 0 or text[i - 1].isspace()):
            return text[:i].rstrip()
        else:
            i += 1
    return text


def _block_comment_step(
    text: str, delimiters: tuple[str, str], in_block: bool
) -> tuple[bool, bool]:
    """Whether *all* of `text` is block comment, and the new in-block state.

    Walks the line so that code trailing a closed comment (`/* note */ run()`)
    is recognized as code, not swallowed by the comment.
    """
    open_, close = delimiters
    text = text.strip()
    while True:
        if in_block:
            end = text.find(close)
            if end == -1:
                return True, True  # comment runs on to the next line
            text = text[end + len(close) :].strip()
            in_block = False
        elif not text:
            return True, False  # nothing but comment(s) on this line
        elif text.startswith(open_):
            text = text[len(open_) :]
            in_block = True
        else:
            return False, False  # real code on this line


def _all_comment_lines(
    side_lines: list[DiffCode],
    changed: Callable[[DiffCode], bool],
    prefixes: tuple[str, ...] | None,
    block: tuple[str, str] | None,
) -> bool:
    """True if every changed, non-blank line on this SIDE is a line or block
    comment. `side_lines` is the hunk's full line sequence for one side of the
    file (context + this side's changes, in order), so block-comment state is
    tracked across the lines the way the file actually reads.

    A block comment opened on a changed line must close before the next context
    line: if it's still open there, the unchanged code on that context line is
    now INSIDE the comment — code commented out is a semantic change, not
    comment churn. The same reasoning closes the bottom of the hunk (`in_block`
    at the end would swallow code below).

    KNOWN LIMITATION (shared with `_whitespace`): a comment-prefix line that is
    actually *inside* a multi-line string literal (a JS template literal, a Python
    triple-quoted string) reads as a comment here, so editing it can be hidden as
    a comment change though the string's value changed. The opening delimiter is
    usually above the hunk, out of view, so we can't detect it from a single hunk;
    this rare case is accepted rather than guarded with an unreliable heuristic."""
    in_block = False
    for line in side_lines:
        if not changed(line):
            if in_block:
                return False  # a changed `/*` swallows this unchanged code
            continue
        text = line.content.strip()
        if not text:
            continue
        if not in_block and prefixes and text.startswith(prefixes):
            continue
        if block:
            is_comment, in_block = _block_comment_step(text, block, in_block)
            if is_comment:
                continue
        return False
    return not in_block


def _inline_comment_change(
    hunk: DiffHunk, prefixes: tuple[str, ...], quotes: str
) -> Trust | None:
    """Label hunks where paired lines differ only in their inline comments."""
    # The positional pairing gate is shared with the token-delta rules
    # (delta.paired_changed_lines); this rule then compares raw strings, not
    # tokens — comments span ~40 languages the tokenizer doesn't model.
    pairs = paired_changed_lines(hunk)
    if pairs is None:
        return None
    old_has_comment = new_has_comment = False
    for old, new in pairs:
        old_code = strip_inline_comment(old.content, prefixes, quotes)
        new_code = strip_inline_comment(new.content, prefixes, quotes)
        # Compare with leading indentation (semantic in Python), so a re-indent of
        # a commented line isn't mistaken for an unchanged-code, comment-only edit.
        if (
            not old_code
            or leading_indent(old.content) + old_code
            != leading_indent(new.content) + new_code
        ):
            return None  # the code (or its indentation) changed, not just a comment
        # The comment remainders (whatever strip_inline_comment dropped). A tool
        # directive in either one (noqa, eslint-disable, …) means tool behavior
        # changed, not prose — never trust it.
        old_comment = old.content.strip()[len(old_code) :]
        new_comment = new.content.strip()[len(new_code) :]
        if _has_directive(old_comment) or _has_directive(new_comment):
            return None
        old_has_comment = old_has_comment or bool(old_comment)
        new_has_comment = new_has_comment or bool(new_comment)
    if new_has_comment and old_has_comment:
        return Trust.COMMENTS_MODIFIED
    if new_has_comment:
        return Trust.COMMENTS_ADDED
    if old_has_comment:
        return Trust.COMMENTS_REMOVED
    return None


def _comments(file: DiffFile, hunk: DiffHunk) -> Trust | None:
    ext = extension(file)
    prefixes = LINE_COMMENT_PREFIXES.get(ext)
    block = BLOCK_COMMENT_DELIMITERS.get(ext)
    if not prefixes and not block:
        return None
    if not hunk.changed_lines:
        return None
    # A shebang selects the interpreter the file runs under — changing it is an
    # execution change that happens to be spelled in comment syntax.
    if any(_is_shebang(line) for line in hunk.changed_lines):
        return None
    # Each side reads as its own file (context + that side's changes, in order),
    # so block-comment state threads through context lines correctly.
    new_side = [line for line in hunk.lines if not line.is_deletion()]
    old_side = [line for line in hunk.lines if not line.is_addition()]
    if _all_comment_lines(
        new_side, DiffCode.is_addition, prefixes, block
    ) and _all_comment_lines(old_side, DiffCode.is_deletion, prefixes, block):
        # Every changed line is a comment, so scan them whole for tool directives.
        if any(_has_directive(line.content) for line in hunk.changed_lines):
            return None
        # change_suffix yields added/removed/modified — each a real Trust member.
        return Trust(f"comments:{change_suffix(hunk)}")
    # Fallback: paired lines whose only difference is a trailing inline comment.
    if prefixes:
        return _inline_comment_change(hunk, prefixes, _string_quotes(ext))
    return None
