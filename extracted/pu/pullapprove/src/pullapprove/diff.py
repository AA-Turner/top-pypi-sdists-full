from __future__ import annotations

import re
from collections.abc import Callable, Generator, Iterable, Iterator
from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .trust import Trust


class DiffFile:
    def __init__(self, *, old_path: str, new_path: str):
        self.old_path = old_path
        self.new_path = new_path
        self.hunks: list[DiffHunk] = []
        # The raw `diff --git` line plus every metadata line before the first
        # hunk (index/mode/rename/`---`/`+++`), verbatim. The client keys a
        # hunkless file's review entry on a hash of exactly these lines
        # (enumerateHunks in review-state.ts), so the file-level trust hash must
        # be built from the same bytes.
        self.header_lines: list[str] = []

    def __repr__(self) -> str:
        return f"<DiffFile old_path={self.old_path} new_path={self.new_path}>"

    def is_move(self) -> bool:
        return self.old_path != self.new_path


class DiffHunk:
    def __init__(
        self,
        *,
        old_line: int,
        old_length: int | None,
        new_line: int,
        new_length: int | None,
    ):
        self.old_line = old_line
        self.old_length = old_length
        self.new_line = new_line
        self.new_length = new_length
        self.lines: list[DiffCode] = []
        self.trust: Trust | None = None

    @property
    def is_new_file(self) -> bool:
        """True when this hunk adds a brand-new file (no old content).

        Both checks matter: a mid-file pure insertion in a zero-context diff
        (`@@ -5,0 +6,2 @@`) also has old_length 0, but only a genuinely new
        file anchors at old line 0 (`@@ -0,0 +1,N @@`)."""
        return self.old_length == 0 and self.old_line == 0

    # Cached: a hunk's lines are appended once during parsing and never mutated
    # after, but the trust rules read these accessors ~12x per hunk as they walk
    # the rule chain — recomputing the list each time is pure waste.
    @cached_property
    def changed_lines(self) -> list[DiffCode]:
        return [line for line in self.lines if not line.is_context()]

    @cached_property
    def added_lines(self) -> list[DiffCode]:
        return [line for line in self.lines if line.is_addition()]

    @cached_property
    def removed_lines(self) -> list[DiffCode]:
        return [line for line in self.lines if line.is_deletion()]


class DiffCode:
    def __init__(
        self,
        *,
        old_line_number: int | None,
        new_line_number: int | None,
        content: str,
        change_type: str,
    ):
        self.old_line_number = old_line_number
        self.new_line_number = new_line_number
        self.content = content
        self.change_type = change_type

    def is_addition(self) -> bool:
        return self.change_type == "+"

    def is_deletion(self) -> bool:
        return self.change_type == "-"

    def is_context(self) -> bool:
        return self.change_type == ""

    @property
    def line_number(self) -> int:
        """For backwards compatibility - returns the appropriate line number."""
        if self.is_deletion():
            return self.old_line_number or 0
        return self.new_line_number or 0

    def __str__(self) -> str:
        return f"{self.line_number}: {self.change_type or ' '}{self.content}"

    def __repr__(self) -> str:
        return f"<DiffCode change_type={self.change_type} old_line={self.old_line_number} new_line={self.new_line_number} content={self.content}>"

    def raw(self) -> str:
        return f"{self.change_type or ' '}{self.content}"


# git C-quote single-char escapes (a quoted diff path may use any of these).
_GIT_QUOTE_ESCAPES = {
    '"': '"',
    "\\": "\\",
    "t": "\t",
    "n": "\n",
    "r": "\r",
    "f": "\f",
    "b": "\b",
    "a": "\a",
    "v": "\v",
}


def _unquote_git_path(inner: str) -> str:
    """Decode a git C-quoted path (the text between the surrounding quotes),
    resolving backslash escapes and octal byte escapes to a UTF-8 string."""
    buf = bytearray()
    i, n = 0, len(inner)
    while i < n:
        ch = inner[i]
        if ch == "\\" and i + 1 < n:
            nxt = inner[i + 1]
            if nxt in _GIT_QUOTE_ESCAPES:
                buf.extend(_GIT_QUOTE_ESCAPES[nxt].encode())
                i += 2
                continue
            if "0" <= nxt <= "7":  # octal byte, e.g. \303 for a UTF-8 lead byte
                # Consume only consecutive octal digits (max 3) — git emits exactly
                # 3, but arbitrary stdin might not, and `int("7y", 8)` would raise.
                end = i + 2
                while end < n and end < i + 4 and "0" <= inner[end] <= "7":
                    end += 1
                buf.append(int(inner[i + 1 : end], 8) & 0xFF)
                i = end
                continue
        buf.extend(ch.encode())
        i += 1
    return buf.decode("utf-8", "replace")


def _read_quoted_git_path(rest: str, i: int) -> tuple[str, int] | None:
    """Read one `"C-quoted"` `a/…` path starting at `rest[i]` (which must be the
    opening quote). Returns (decoded path, index just past the closing quote), or
    None for an unterminated quote."""
    j = i + 1
    while j < len(rest):
        if rest[j] == "\\":
            j += 2  # an escaped char can't close the quote
            continue
        if rest[j] == '"':
            return _unquote_git_path(rest[i + 1 : j]), j + 1
        j += 1
    return None


def _split_equal_git_names(rest: str) -> tuple[str, str] | None:
    """Split an unquoted `a/PATH b/PATH` header when both sides name the SAME
    path (a non-rename), returning (path, path).

    Git doesn't quote spaces, so `diff --git a/Section 1/report.py b/Section
    1/report.py` is ambiguous to a greedy ` \\w/` split (which lands on the last
    separator and mis-paths the file). But a non-rename repeats one identical
    path on both sides, so the split is exactly the center: `<p>/NAME <p>/NAME`
    with equal-length halves. Resolve it structurally, the way git's own header
    parser assumes equal names first. Returns None when the halves differ (a
    rename — handled by the caller's fallback)."""
    # rest == prefix(2) + NAME + " " + prefix(2) + NAME  ->  len 5 + 2*len(NAME)
    if len(rest) < 5 or (len(rest) - 5) % 2 != 0:
        return None
    name_len = (len(rest) - 5) // 2
    left, middle, right = (
        rest[2 : 2 + name_len],
        rest[2 + name_len : 5 + name_len],
        rest[5 + name_len :],
    )
    # Both prefixes are one word-char + "/", the separator is a space, and the
    # two names are identical.
    if left == right and re.match(r"^\w/$", rest[:2]) and re.match(r"^ \w/$", middle):
        return left, right
    return None


def parse_diff_file_line(line: str) -> DiffFile | None:
    # Cheap guard: skip the parsing on the vast majority of lines that can't match.
    if not line.startswith("diff --git "):
        return None
    # Streamed lines keep their trailing newline; a name must never absorb it.
    rest = line[len("diff --git ") :].strip()
    if '"' not in rest:
        # A non-rename repeats the same path on both sides; resolve that
        # exactly (so a space-containing path isn't mis-split). Fall back to the
        # greedy split for renames — different paths whose spaces make this line
        # genuinely ambiguous (git also emits `--- a/`/`rename from` for those).
        if names := _split_equal_git_names(rest):
            return DiffFile(old_path=names[0], new_path=names[1])
        match = re.match(r"^\w/(.*) \w/(.*)$", rest)
        if match:
            return DiffFile(
                old_path=match.group(1),
                new_path=match.group(2),
            )
        return None
    # A name with special/non-ASCII bytes is C-quoted (prefix inside the quotes),
    # e.g. `diff --git "a/caf\303\251.py" b/plain.txt` — git quotes each side
    # independently, and a BARE side may still contain spaces. Read both tokens so
    # the header is recognized — else, mid-filter, a hidden hunk before it would
    # swallow this file's whole diff — and quoted paths decoded.
    if rest.startswith('"'):
        first = _read_quoted_git_path(rest, 0)
        if first is None or first[1] >= len(rest) or rest[first[1]] != " ":
            return None
        old_path, second_start = first[0], first[1] + 1
        second_raw = rest[second_start:]
    else:
        # Bare first + quoted second: the second token starts at the ` "` split,
        # so a bare first name keeps any spaces it contains.
        split = rest.find(' "')
        if split == -1:
            return None
        old_path, second_raw = rest[:split], rest[split + 1 :]
    if second_raw.startswith('"'):
        second = _read_quoted_git_path(second_raw, 0)
        if second is None:
            return None
        new_path = second[0]
    else:
        new_path = second_raw  # bare to end of line — spaces stay in the name
    return DiffFile(
        old_path=re.sub(r"^\w/", "", old_path),
        new_path=re.sub(r"^\w/", "", new_path),
    )


def parse_diff_hunk_line(line: str) -> DiffHunk | None:
    # Cheap guard: skip the regex on the vast majority of lines that can't match.
    if not line.startswith("@@ "):
        return None
    match = re.match(r"^@@ -(\d+),?(\d+)? \+(\d+),?(\d+)? @@", line)
    if match:
        old_line, old_length, new_line, new_length = match.groups()
        return DiffHunk(
            old_line=int(old_line),
            old_length=int(old_length) if old_length else None,
            new_line=int(new_line),
            new_length=int(new_length) if new_length else None,
        )
    return None


def _lookahead(lines: Iterable[str]) -> Generator[tuple[str, bool]]:
    """Yield each line paired with whether another line follows it."""
    it = iter(lines)
    try:
        prev = next(it)
    except StopIteration:
        return
    for line in it:
        yield prev, True
        prev = line
    yield prev, False


def _iterate_diff_parts(
    diff: Iterable[str] | str,
) -> Generator[DiffFile | DiffHunk | DiffCode]:
    """Single source of truth for diff parsing.

    Yields files, hunk headers, and code lines in order. `iterate_diff_parts`
    filters out the hunk headers to preserve its long-standing
    `DiffFile | DiffCode` contract; `parse_diff` keeps them to group lines
    under their hunks.
    """
    current_file: DiffFile | None = None
    current_hunk: DiffHunk | None = None

    # Track where we are in the hunk as we go.
    minus_line = plus_line = 0

    # Streamed lines can still end in their newline (git's stdout does), while
    # the hosts' line iterators hand them over already stripped
    diff_iterator = (
        diff.splitlines()
        if isinstance(diff, str)
        else (line.removesuffix("\n") for line in diff)
    )

    # A bare `""` body line is ambiguous: it's either a genuine blank context
    # line (some hosts strip its leading space) or the trailing artifact that
    # `some_diff_text.split("\n")` appends when the text ends with a newline
    # (e.g. the CLI's `diff --hide`, which splits that way on purpose so its
    # two parsing passes stay aligned — see cli.py). The two are only told
    # apart by position: the split artifact is always the LAST line of the
    # whole input, with nothing after it, while a real blank context line is
    # always followed by more content (more body, the next hunk, the next
    # file, or at minimum its own file's closing newline). So a `""` only
    # counts as context when something follows it — `_lookahead` reports that
    # via `has_next`. Header count mismatches (real diffs, and this test
    # suite's fixtures, aren't always internally consistent) rule out using
    # the hunk's declared old/new length for this instead.
    for raw, has_next in _lookahead(diff_iterator):
        if new_file := parse_diff_file_line(raw):
            current_file, current_hunk = new_file, None
            new_file.header_lines.append(raw)
            yield new_file
        elif current_file:
            if new_hunk := parse_diff_hunk_line(raw):
                current_hunk = new_hunk
                minus_line, plus_line = new_hunk.old_line, new_hunk.new_line
                yield new_hunk

                # Git can pack the first context line onto the hunk header,
                # after the closing `@@` (e.g. `@@ -6,7 +6,7 @@ def foo():`).
                # Emit it as a context line so it isn't dropped.
                trailing = (
                    raw.split("@@", 2)[-1].lstrip() if raw.count("@@") > 1 else ""
                )
                if trailing:
                    yield DiffCode(
                        old_line_number=minus_line,
                        new_line_number=plus_line,
                        content=trailing,
                        change_type="",
                    )
                    minus_line += 1
                    plus_line += 1
            elif current_hunk:
                if raw.startswith("+"):
                    yield DiffCode(
                        old_line_number=None,
                        new_line_number=plus_line,
                        content=raw[1:],
                        change_type="+",
                    )
                    plus_line += 1
                elif raw.startswith("-"):
                    yield DiffCode(
                        old_line_number=minus_line,
                        new_line_number=None,
                        content=raw[1:],
                        change_type="-",
                    )
                    minus_line += 1
                elif (raw.startswith(" ") or raw == "") and (raw != "" or has_next):
                    # Context exists on both sides (some hosts strip a blank
                    # context line's leading space, hence the `""` case —
                    # matches the JS parsers in file-contents.ts/review-state.ts).
                    yield DiffCode(
                        old_line_number=minus_line,
                        new_line_number=plus_line,
                        content="" if raw == "" else raw[1:],
                        change_type="",
                    )
                    minus_line += 1
                    plus_line += 1
            elif raw != "" or has_next:
                # A metadata line between the `diff --git` line and the first
                # hunk (index/mode/rename/`---`/`+++`). Captured verbatim —
                # the client does the same (splitDiffByFile's headerLines), so
                # the two sides hash identical bytes for a hunkless file. The
                # final `""` a split("\n") appends for a newline-terminated
                # diff is an artifact, not metadata — same `has_next` test the
                # context-line branch above uses. (The served diff is never
                # newline-terminated, so the client never sees that artifact
                # and parity holds.)
                current_file.header_lines.append(raw)


def iterate_diff_parts(
    diff: Iterator[str] | str,
) -> Generator[DiffFile | DiffCode]:
    """Stream a diff as files and code lines (hunk headers omitted)."""
    for part in _iterate_diff_parts(diff):
        if not isinstance(part, DiffHunk):
            yield part


def parse_diff(diff: Iterable[str] | str) -> list[DiffFile]:
    """Parse a diff into files, each grouping its hunks and their lines."""
    files: list[DiffFile] = []
    current_file: DiffFile | None = None
    current_hunk: DiffHunk | None = None

    for part in _iterate_diff_parts(diff):
        if isinstance(part, DiffFile):
            current_file, current_hunk = part, None
            files.append(part)
        elif isinstance(part, DiffHunk):
            current_hunk = part
            if current_file is not None:
                current_file.hunks.append(part)
        elif current_hunk is not None:
            current_hunk.lines.append(part)

    return files


def iter_file_hunks(diff: Iterable[str] | str) -> Iterator[tuple[DiffFile, DiffHunk]]:
    """Stream each completed `(file, hunk)` pair as the diff parses, holding only
    the current hunk's lines in memory. (`parse_diff` keeps the whole tree; this
    keeps one hunk — which is all a per-hunk consumer needs.) A new file or hunk,
    and end-of-input, each flush the hunk that just finished; a hunk only exists
    after its file, so both are set whenever a pair is yielded. Files without
    hunks (binary, pure rename, mode-only) are never yielded.

    This mirrors `parse_diff`'s grouping of the same parts stream; keep the two
    in sync if that dispatch changes."""
    file: DiffFile | None = None
    hunk: DiffHunk | None = None

    for part in _iterate_diff_parts(diff):
        if isinstance(part, DiffFile):
            if file is not None and hunk is not None:
                yield file, hunk
            file, hunk = part, None
        elif isinstance(part, DiffHunk):
            if file is not None and hunk is not None:
                yield file, hunk
            hunk = part
        elif hunk is not None:
            hunk.lines.append(part)

    if file is not None and hunk is not None:
        yield file, hunk


def iter_hunkless_files(diff: Iterable[str] | str) -> Iterator[DiffFile]:
    """Stream each file that finishes with no hunks — a binary, pure-rename, or
    mode-only change. The complement of `iter_file_hunks`: that yields every
    (file, hunk) pair and never a hunkless file; this yields only the hunkless
    files. A file is only known to be hunkless once the next file starts (or the
    input ends), so each yield happens there — by which point the file's
    `header_lines` are complete."""
    file: DiffFile | None = None
    has_hunks = False

    for part in _iterate_diff_parts(diff):
        if isinstance(part, DiffFile):
            if file is not None and not has_hunks:
                yield file
            file, has_hunks = part, False
        elif isinstance(part, DiffHunk):
            has_hunks = True

    if file is not None and not has_hunks:
        yield file


def filter_diff_text(
    diff_text: str,
    keep_hunk: Callable[[str, int, int], bool],
) -> str:
    """Re-emit a unified diff, keeping only the hunks `keep_hunk` accepts.

    `keep_hunk(new_path, old_line, new_line)` is called once per hunk. Hunk
    bodies are copied verbatim — the diff is split on "\\n" only (not
    str.splitlines, which also breaks on "\\r", "\\f", and Unicode separators),
    and bytes are never rebuilt from the parsed model — so CRLF endings and any
    control characters in the content survive, and the result stays a valid
    unified diff.

    A file whose hunks are all dropped is removed, header and all. A file with
    no hunks at all — a binary, pure-rename, or mode-only change — has nothing
    to classify and is never "trusted", so it is kept unchanged. Any preamble
    before the first file (e.g. a `git show` commit message) passes through.
    """
    out: list[str] = []
    header: list[str] = []  # file-level lines buffered until a hunk is kept
    new_path: str | None = None
    in_hunk = False  # have we passed this file's first @@ yet?
    keeping = False  # is the current hunk being kept?

    def flush_unhunked_file() -> None:
        # A file with header lines but no @@ hunks (binary, pure rename, or
        # mode-only change) has nothing to classify, so emit it as-is rather
        # than dropping it. A file whose hunks were dropped has in_hunk set and
        # is intentionally skipped.
        if header and not in_hunk:
            out.extend(header)

    for line in diff_text.split("\n"):
        if file := parse_diff_file_line(line):
            flush_unhunked_file()
            new_path = file.new_path
            header = [line]
            in_hunk = False
            keeping = False
        elif new_path is not None and (hunk := parse_diff_hunk_line(line)):
            in_hunk = True
            keeping = keep_hunk(new_path, hunk.old_line, hunk.new_line)
            if keeping:
                out.extend(header)
                header = []
                out.append(line)
        elif not in_hunk:
            # File metadata before the first hunk, or preamble before any file.
            (header if new_path is not None else out).append(line)
        elif keeping:
            out.append(line)  # a body line of a kept hunk
    flush_unhunked_file()

    result = "\n".join(out)
    # The input's final newline arrives as a trailing "" split element attached
    # to the last hunk's body; if that hunk was dropped, restore the newline so
    # the output stays a well-terminated diff.
    if diff_text.endswith("\n") and result and not result.endswith("\n"):
        result += "\n"
    return result
