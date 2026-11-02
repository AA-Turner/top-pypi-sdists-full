"""Trust rules: changes that don't alter meaning — empty new files, whitespace,
line wrapping, inter-token spacing, and punctuation/quote style."""

from __future__ import annotations

from itertools import pairwise

from ..diff import DiffCode, DiffFile, DiffHunk
from .delta import paired_changed_lines, paired_token_delta
from .helpers import extension, leading_indent
from .labels import Trust
from .linescan import collapse_ws_outside_strings, consume_string, scan_string
from .tokens import OP, STRING, Token

# The deeply-tested core the content rules (`_style`, `_line_length`) share: the
# JS/TS family + Python. These have free-form whitespace (so a reflow is neutral)
# and use `'`/`"`/`;`/`,` interchangeably enough for `_style` — and they're the
# ones we've actually validated. Other brace languages (Go, Rust, Java, C, …) are
# plausible but unverified per-language — add them here only with a test corpus.
# Data/markup (csv, tsv, yaml, md, …) stays out entirely: there a newline, comma,
# or quote can be semantic, so these rules would hide real changes.
_CORE_CONTENT_LANGUAGES = frozenset(
    ["js", "jsx", "ts", "tsx", "mjs", "mts", "cjs", "cts", "py"]
)


def _empty_file(file: DiffFile, hunk: DiffHunk) -> Trust | None:
    # A brand-new file's hunk is all additions, so "empty" is just "all blank".
    if not hunk.is_new_file:
        return None
    if all(not line.content.strip() for line in hunk.lines):
        return Trust.EMPTY_FILE
    return None


def _whitespace(file: DiffFile, hunk: DiffHunk) -> Trust | None:
    # Same language gate as the other content rules: in data/markup a blank line
    # is often semantic (a Markdown paragraph break, a line inside a YAML block
    # scalar), so only the validated code languages qualify.
    if extension(file) not in _CORE_CONTENT_LANGUAGES:
        return None
    # KNOWN LIMITATION: a blank-line-only change *inside* a multi-line string
    # literal (a `'''…'''` docstring, a template literal, a heredoc) changes the
    # string's value, but reads as trivial here. We can't tell from a single hunk
    # whether a blank line falls inside a literal — the opening delimiter is
    # usually above the hunk, out of view — so this rare case is accepted rather
    # than guarded with an unreliable heuristic.
    changed = hunk.changed_lines
    if changed and all(not line.content.strip() for line in changed):
        return Trust.WHITESPACE
    return None


# A wrapped line "continues" to the next when it ends inside an open bracket,
# with a `\`, or on an operator / opener / comma / dot / colon — never on an
# identifier, value, closer, or `;`. That separates a real reflow from two
# statements joined (a Python suite boundary, a JS ASI point), where the newline
# is semantic and joining changes meaning.
_CONTINUATION_CHARS = frozenset("=+-*/%<>&|^~,.:?([{")


def _bracket_delta(text: str) -> int:
    """Net bracket-depth change of `text`, ignoring brackets inside strings."""
    depth = 0
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch in "\"'`":
            i = consume_string(text, i)
            continue
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        i += 1
    return depth


def _is_reflow(lines: list[DiffCode]) -> bool:
    """True if `lines` is one statement wrapped across lines: every break (all but
    the last) sits inside an open bracket, ends with `\\`, or ends on a
    continuation operator. Otherwise the join crosses a statement boundary and the
    newline is not neutral."""
    depth = 0
    for line in lines[:-1]:
        stripped = line.content.rstrip()
        depth += _bracket_delta(line.content)
        if (
            depth > 0
            or stripped.endswith("\\")
            or (stripped and stripped[-1] in _CONTINUATION_CHARS)
        ):
            continue
        return False
    return True


def _contiguous_replacement(hunk: DiffHunk) -> bool:
    """True when the hunk's changed lines form ONE deletions-then-additions block
    with no context line inside it. A reflow rewraps one statement in place;
    deletions that bracket a context line mean code crossed a statement boundary,
    and joining the sides would compare a reordering as if it were a rewrap."""
    seen_deletion = False
    seen_addition = False
    done = False
    for line in hunk.lines:
        if line.is_context():
            if seen_deletion or seen_addition:
                done = True
            continue
        if done:
            return False  # a second changed block — not one replacement
        if line.is_deletion():
            if seen_addition:
                return False  # deletions after additions — interleaved blocks
            seen_deletion = True
        else:
            seen_addition = True
    return True


def _has_line_comment(text: str, prefix: str, quotes: str) -> bool:
    """True if `text` starts a line comment outside a string literal. Unlike
    `strip_inline_comment`, no whitespace-before-prefix requirement: for reflow
    safety a glued comment (`foo()// note`) swallows a join just the same."""
    i, n = 0, len(text)
    while i < n:
        if text[i] in quotes:
            i = consume_string(text, i)
        elif text.startswith(prefix, i):
            return True
        else:
            i += 1
    return False


def _join_crosses_string(lines: list[DiffCode]) -> bool:
    """True if a join between these lines lands INSIDE a multi-line string
    literal (a `\"\"\"…\"\"\"` body, a `` `…` `` template literal spanning lines).

    `_line_length` joins the lines with a space to compare the reflow. When a
    break sits inside a string, that space replaces a real interior newline, so
    the string's *value* changes (`\"SELECT a,\\nb\"` -> `\"SELECT a, b\"`) yet both
    sides join to the same text — the change would be hidden. Detect it by
    tracking string state across the lines: any non-last line that ends inside
    an unclosed string means the following join is inside that string.
    """
    open_delim: str | None = None  # delimiter of a string still open at line end
    for line in lines[:-1]:
        text = line.content
        i, n = 0, len(text)
        if open_delim is not None:  # continuing a string opened on an earlier line
            close = text.find(open_delim)
            if close == -1:
                return True  # still open across this join
            i, open_delim = close + len(open_delim), None
        while i < n:
            if text[i] in "\"'`":
                delim = text[i] * 3 if text[i : i + 3] == text[i] * 3 else text[i]
                close = scan_string(text, i)
                if close is None:  # opens a string that runs past end-of-line
                    open_delim = delim
                    break
                i = close
            else:
                i += 1
        if open_delim is not None:
            return True
    return False


def _line_length(file: DiffFile, hunk: DiffHunk) -> Trust | None:
    """Code wrapped/unwrapped across lines: identical content after joining."""
    # In data/markup a newline separates records, so joining two lines isn't neutral.
    ext = extension(file)
    if ext not in _CORE_CONTENT_LANGUAGES:
        return None
    added, removed = hunk.added_lines, hunk.removed_lines
    if not added or not removed:
        return None
    # Wrapping/unwrapping changes the line count; an equal-count edit is a
    # same-shape change (handled by _style), not a reflow.
    if len(added) == len(removed):
        return None
    # The joined comparison below flattens line positions, so it's only sound
    # when the change is one contiguous replacement — deletions bracketing a
    # context line would let moved code read as a neutral rewrap.
    if not _contiguous_replacement(hunk):
        return None
    # Default-deny: a neutral reflow requires every break on BOTH sides to be a
    # continuation (inside brackets / `\` / an operator). A break anywhere at
    # statement level means the newline is semantic (a Python suite, a JS ASI
    # point), so the "reflow" isn't neutral — decline rather than hide it.
    if not (_is_reflow(added) and _is_reflow(removed)):
        return None
    # A break INSIDE a multi-line string (a triple-quote body, a template
    # literal) means the join splices the string's value (interior newline ->
    # space). collapse_ws_outside_strings preserves interiors, but the join
    # itself already changed them, so decline rather than hide a literal edit.
    if _join_crosses_string(added) or _join_crosses_string(removed):
        return None
    # Indentation is semantic in Python (block scope); a reflow that also shifts
    # the statement's own indent is a dedent/indent, not a neutral wrap. Only the
    # FIRST line carries the statement's indent (continuation lines are naturally
    # re-indented), and `collapse_ws_outside_strings` strips leading space — so
    # without this guard an indent change would compare equal and be hidden.
    if leading_indent(added[0].content) != leading_indent(removed[0].content):
        return None
    # A line comment runs to end-of-line, so joining a commented line with the
    # next drags the next line's code INTO the comment (`foo(a, // why` + `b)`
    # joins to a line where `b)` is comment text). Even when the joined texts
    # compare equal, that join is never neutral — decline if any line but the
    # last starts a line comment. A comment on the LAST line is fine (nothing is
    # joined after it), and block comments are fine (`/* … */` spans the join
    # unchanged either way).
    prefix = "#" if ext == "py" else "//"
    quotes = "\"'" if ext == "py" else "\"'`"
    for side in (added, removed):
        if any(_has_line_comment(line.content, prefix, quotes) for line in side[:-1]):
            return None
    # Collapse only the whitespace *between* tokens — preserving string interiors
    # so a real edit inside a literal can't masquerade as a reflow.
    joined_added = collapse_ws_outside_strings(" ".join(line.content for line in added))
    joined_removed = collapse_ws_outside_strings(
        " ".join(line.content for line in removed)
    )
    if joined_added and joined_added == joined_removed:
        return Trust.LINE_LENGTH
    return None


def _string_value(text: str) -> str:
    """The value of a `'`/`"` string literal, delimiter-agnostic — so `'a'` and
    `"a"` compare equal but a change to the *contents* does not. Delimiter escapes
    are normalized (`'it\\'s'` and `"it's"` both decode to `it's`); a backtick
    template literal is returned verbatim (its semantics aren't delimiter-style)."""
    quote = text[0]
    if quote not in "\"'":
        return text
    return text[1:-1].replace("\\" + quote, quote)


def _style_key(
    tokens: list[Token], collapse_comma: bool, collapse_semicolon: bool
) -> list[object]:
    """A token key in which only *stylistic* differences collapse: quote-delimiter
    style (strings compare by decoded value), plus a trailing `,`/`;` when
    `collapse_comma`/`collapse_semicolon` say it is stylistic here. Everything else
    — identifiers, operators, numbers, string *contents* — is compared verbatim, so
    a real change survives.

    Trailing punctuation isn't always stylistic: a Python trailing comma builds a
    tuple (`(x,)`, `x = a,`, `a[1,]`), and a JS/TS trailing semicolon can be
    ASI-load-bearing. In those cases the flag is False and the punctuation stays in
    the key, so the change is never hidden as style."""
    key: list[object] = []
    n = len(tokens)
    for i, tok in enumerate(tokens):
        if collapse_semicolon and tok.kind == OP and tok.text == ";" and i == n - 1:
            continue  # trailing semicolon
        if (
            collapse_comma
            and tok.kind == OP
            and tok.text == ","
            and (
                i == n - 1 or (tokens[i + 1].kind == OP and tokens[i + 1].text in ")]}")
            )
        ):
            # A line-final comma is treated as a trailing comma (stylistic in
            # JS/TS). KNOWN RESIDUAL: a comma-separated declaration written one
            # per line (`let a = 1,` / `b = 2`) is also line-final, so dropping
            # the separator reads as style — a real scope change (under sloppy
            # mode; strict mode throws). Distinguishing it needs the next line,
            # which this per-pair rule can't see; not worth showing every
            # multi-line trailing-comma reformat to close a narrow, usually-loud
            # case.
            continue  # trailing comma (line end, or before a closer)
        # Tag string values so a literal can't collide with an identifier of the
        # same text (a `'foo'` -> `foo` change must stay visible).
        key.append(("str", _string_value(tok.text)) if tok.kind == STRING else tok.text)
    return key


def _style_delta(
    old_tokens: list[Token],
    new_tokens: list[Token],
    collapse_comma: bool,
    collapse_semicolon: bool,
) -> bool | None:
    """Compare one line pair: True if it differs ONLY in style (semicolons /
    trailing commas / quote delimiters), False if token-identical, None to
    decline (a non-style difference remains)."""
    old_key = _style_key(old_tokens, collapse_comma, collapse_semicolon)
    new_key = _style_key(new_tokens, collapse_comma, collapse_semicolon)
    if old_key != new_key:
        return None  # a non-style difference remains
    # Style-only iff the tokens themselves differ (a quote delimiter or trailing
    # punctuation). If the raw tokens match, any remaining difference is in a
    # comment or whitespace the tokenizer drops — not this rule's job (leave it
    # for _comments), so don't claim it as style.
    return [t.text for t in old_tokens] != [t.text for t in new_tokens]


# Line-leading characters that, under JS/TS Automatic Semicolon Insertion,
# continue the previous statement rather than start a new one. A leading `/` is
# also a continuation (regex literal or division) but is handled separately, since
# `//` and `/*` start comments, not statements.
_ASI_LEADERS = frozenset(("(", "[", "`", "+", "-"))


def _continues_previous_line(text: str) -> bool:
    """True if `text` begins with a token that, under JS/TS ASI, attaches to the
    previous line instead of starting a new statement."""
    stripped = text.lstrip()
    if not stripped:
        return False
    if stripped[0] in _ASI_LEADERS:
        return True
    # A leading `/` is a regex literal or division that continues the line above —
    # unless it opens a comment (`//`, `/*`), which is inert.
    return stripped[0] == "/" and not stripped.startswith(("//", "/*"))


def _asi_hazard(hunk: DiffHunk) -> bool:
    """True if the hunk's new-file side has a statement line that continues the
    previous non-blank line under JS/TS Automatic Semicolon Insertion. There,
    adding or removing a trailing `;` on the line above merges or splits two
    statements — a real behavior change — so `_style` must not treat that `;` as
    stylistic. ASI ignores blank lines, so we compare against the last non-blank
    line, not the strictly-adjacent one.

    When only blank lines are visible after the last changed line, the statement
    ASI would merge with sits past the context window — the scan can't prove the
    `;` inert, so that counts as a hazard too (default-deny). A hunk that ENDS on
    the changed line is different: git always emits trailing context when lines
    exist, so that's the end of the file and there is nothing to merge with."""
    prev_nonblank = ""
    last_nonblank_changed = False
    blanks_after = False
    for line in hunk.lines:
        if line.is_deletion():
            continue
        if prev_nonblank and _continues_previous_line(line.content):
            return True
        if line.content.strip():
            prev_nonblank = line.content
            last_nonblank_changed = line.is_addition()
            blanks_after = False
        else:
            blanks_after = True
    return last_nonblank_changed and blanks_after


def _style(file: DiffFile, hunk: DiffHunk) -> Trust | None:
    """Paired lines that differ only in semicolons, quotes, or trailing commas.

    Python tokenizes under the `py` dialect and the JS family under `ts` — they
    can't share one dialect, because `//` is a line comment in JS but floor
    DIVISION in Python (tokenizing `x // 2` as `ts` would drop `// 2` as a comment
    and hide a divisor change). The two semantic splits — a Python trailing comma
    builds a tuple, a JS/TS trailing semicolon can be ASI-load-bearing — are
    handled by `collapse_comma`/`collapse_semicolon`."""
    ext = extension(file)
    if ext not in _CORE_CONTENT_LANGUAGES:
        return None  # elsewhere ';'/','/quotes may be semantic (data, char literals)
    # The positional pairing gate runs first, so the O(hunk-lines) ASI scan
    # below never runs for hunks the pairing would reject anyway.
    pairs = paired_changed_lines(hunk)
    if pairs is None:
        return None
    dialect = "py" if ext == "py" else "ts"
    collapse_comma = ext != "py"  # a Python trailing comma builds a tuple
    # Python has no ASI, so its `;` is always stylistic; in JS/TS a trailing `;` is
    # only stylistic when no following line continues the statement.
    collapse_semicolon = ext == "py" or not _asi_hazard(hunk)
    return (
        Trust.STYLE
        if paired_token_delta(
            pairs,
            dialect,
            lambda old, new, o, n: _style_delta(
                o, n, collapse_comma, collapse_semicolon
            ),
        )
        else None
    )


def _whitespace_gaps_only(stripped: str, tokens: list[Token]) -> bool:
    """True if everything between consecutive tokens is whitespace. The tokenizer
    silently skips block comments, so without this check a mid-line `/* … */`
    edit would compare token-identical and read as a spacing change."""
    pos = 0
    for tok in tokens:
        if stripped[pos : tok.start].strip():
            return False
        pos = tok.end
    return True


def _line_tail(stripped: str, tokens: list[Token]) -> str:
    """The text after the last token — a trailing line comment, or empty."""
    return stripped[tokens[-1].end :].strip() if tokens else stripped


def _spacing_delta(
    old: DiffCode,
    new: DiffCode,
    old_tokens: list[Token],
    new_tokens: list[Token],
    dialect: str,
) -> bool | None:
    """Compare one line pair: True if only the whitespace between or after the
    tokens moved, False if the lines are identical, None to decline (something
    other than inter-token whitespace changed)."""
    if [t.text for t in old_tokens] != [t.text for t in new_tokens]:
        return None  # a token changed — not a whitespace-only edit
    # Token offsets index into the stripped line (what `paired_token_delta`
    # tokenized), so the gap/tail checks scan that same text.
    old_stripped, new_stripped = old.content.strip(), new.content.strip()
    if not _whitespace_gaps_only(old_stripped, old_tokens):
        return None  # a mid-line block comment sits in a gap
    if not _whitespace_gaps_only(new_stripped, new_tokens):
        return None
    if _line_tail(old_stripped, old_tokens) != _line_tail(new_stripped, new_tokens):
        return None  # the trailing comment changed — _comments' territory
    for (o1, o2), (n1, n2) in zip(pairwise(old_tokens), pairwise(new_tokens)):
        if (o1.end == o2.start) == (n1.end == n2.start):
            continue  # this pair's grouping didn't change
        if (o1.kind == OP) == (o2.kind == OP):
            return None  # regrouped punctuation / word+string — semantic
        if dialect == "ts" and (o1.text in "/<>" or o2.text in "/<>"):
            return None  # regex / generic ambiguity — spacing decides parse
    return old.content != new.content


def _spacing(file: DiffFile, hunk: DiffHunk) -> Trust | None:
    """Paired lines whose tokens are identical and only the whitespace between or
    after them moved — `x=1` -> `x = 1`, `f( a )` -> `f(a)`, trailing-whitespace
    trims, alignment shifts.

    Whitespace inside a string literal is a value change and never qualifies
    (string tokens compare verbatim). Two default-deny guards beyond the shared
    pairing/indent/tokenize gates in `delta.py`:

    - Regrouping punctuation is semantic even with identical token texts
      (`a + +b` vs `a ++ b` in JS, `a ** b` vs `a * * b` in Python), and so is
      gluing a word to a string (`f "x"` vs f-string `f"x"`) — a glue change is
      only trusted when exactly one side of the touching pair is punctuation.
      In JS/TS, `/`, `<`, and `>` never qualify at all: spacing decides whether
      they read as regex-vs-division or generic-vs-comparison.
    - The tokenizer skips comments, so the text after the last token (a trailing
      line comment) must match exactly and interior gaps must be pure whitespace;
      otherwise a comment edit would read as spacing. Comment-only changes stay
      `_comments`' job (this rule declines and falls through).
    """
    ext = extension(file)
    if ext not in _CORE_CONTENT_LANGUAGES:
        return None
    pairs = paired_changed_lines(hunk)
    if pairs is None:
        return None
    dialect = "py" if ext == "py" else "ts"
    return (
        Trust.SPACING
        if paired_token_delta(
            pairs,
            dialect,
            lambda old, new, o, n: _spacing_delta(old, new, o, n, dialect),
        )
        else None
    )
