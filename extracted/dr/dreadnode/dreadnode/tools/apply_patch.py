"""
Apply a multi-file patch using a structured, LLM-friendly format.

Patch format (designed to avoid line-number counting):

    *** Begin Patch
    *** Add File: path/to/new.py
    +line1
    +line2
    *** Update File: path/to/existing.py
    *** Move to: path/to/renamed.py
    @@ def some_function():
     context line
    -old line
    +new line
    *** End of File
    *** Delete File: path/to/old.py
    *** End Patch

Ported from opencode's TypeScript implementation.
"""

import re
import typing as t
from dataclasses import dataclass, field
from pathlib import Path

import aiofiles

from dreadnode.agents.tools import tool

# --- Types -------------------------------------------------------------------


@dataclass
class UpdateChunk:
    """A single chunk within an update hunk."""

    old_lines: list[str]
    new_lines: list[str]
    context: str | None = None
    is_eof: bool = False


@dataclass
class Hunk:
    """A file-level operation in a patch."""

    type: t.Literal["add", "delete", "update"]
    path: str
    contents: str = ""
    move_to: str | None = None
    chunks: list[UpdateChunk] = field(default_factory=list)


# --- Unicode normalization ---------------------------------------------------

_UNICODE_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"[\u2018\u2019\u201a\u201b]"), "'"),
    (re.compile(r"[\u201c\u201d\u201e\u201f]"), '"'),
    (re.compile(r"[\u2010\u2011\u2012\u2013\u2014\u2015]"), "-"),
    (re.compile(r"\u2026"), "..."),
    (re.compile(r"\u00a0"), " "),
]


def _normalize_unicode(s: str) -> str:
    """Convert smart quotes, dashes, ellipsis, NBSP to ASCII equivalents."""
    for pattern, replacement in _UNICODE_REPLACEMENTS:
        s = pattern.sub(replacement, s)
    return s


# --- Patch parser ------------------------------------------------------------


def _parse_header(line: str) -> tuple[str, str] | None:
    """Parse a file-operation header line.

    Returns (operation, path) or None if not a header.
    """
    for prefix in ("*** Add File: ", "*** Delete File: ", "*** Update File: "):
        if line.startswith(prefix):
            op = prefix.split()[1].lower()  # "add", "delete", "update"
            path = line[len(prefix) :].strip()
            return op, path
    return None


def _parse_add_content(lines: list[str], start: int) -> tuple[str, int]:
    """Parse content lines for an Add File hunk.

    Returns (content_string, next_index).
    """
    content_lines: list[str] = []
    i = start
    while i < len(lines):
        if lines[i].startswith("***"):
            break
        if lines[i].startswith("+"):
            content_lines.append(lines[i][1:])
        i += 1
    content = "\n".join(content_lines)
    if content and not content.endswith("\n"):
        content += "\n"
    return content, i


def _parse_update_chunks(lines: list[str], start: int) -> tuple[list[UpdateChunk], int]:
    """Parse update chunks for an Update File hunk.

    Returns (chunks, next_index).
    """
    chunks: list[UpdateChunk] = []
    i = start

    while i < len(lines) and not lines[i].startswith("***"):
        if not lines[i].startswith("@@"):
            i += 1
            continue

        context = lines[i][2:].strip() or None
        i += 1

        old_lines: list[str] = []
        new_lines: list[str] = []
        is_eof = False

        while i < len(lines) and not lines[i].startswith("@@"):
            line = lines[i]

            if line == "*** End of File":
                is_eof = True
                i += 1
                break

            # Any other *** header means we've left this hunk.
            if line.startswith("***"):
                break

            if line.startswith(" "):
                content = line[1:]
                old_lines.append(content)
                new_lines.append(content)
            elif line.startswith("-"):
                old_lines.append(line[1:])
            elif line.startswith("+"):
                new_lines.append(line[1:])

            i += 1

        chunks.append(
            UpdateChunk(
                old_lines=old_lines,
                new_lines=new_lines,
                context=context,
                is_eof=is_eof,
            )
        )

    return chunks, i


def parse_patch(patch_text: str) -> list[Hunk]:
    """Parse a patch string into a list of hunks.

    Raises:
        ValueError: If the patch format is invalid or empty.
    """
    cleaned = patch_text.replace("\r\n", "\n").replace("\r", "\n").strip()
    lines = cleaned.split("\n")

    begin_idx = -1
    end_idx = -1
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "*** Begin Patch" and begin_idx == -1:
            begin_idx = idx
        if stripped == "*** End Patch":
            end_idx = idx

    if begin_idx == -1 or end_idx == -1 or begin_idx >= end_idx:
        raise ValueError("Invalid patch format: missing *** Begin Patch / *** End Patch markers")

    hunks: list[Hunk] = []
    i = begin_idx + 1

    while i < end_idx:
        header = _parse_header(lines[i])
        if header is None:
            i += 1
            continue

        op, path = header

        if op == "add":
            contents, i = _parse_add_content(lines, i + 1)
            hunks.append(Hunk(type="add", path=path, contents=contents))

        elif op == "delete":
            hunks.append(Hunk(type="delete", path=path))
            i += 1

        elif op == "update":
            i += 1
            move_to: str | None = None
            if i < end_idx and lines[i].startswith("*** Move to: "):
                move_to = lines[i][len("*** Move to: ") :].strip()
                i += 1
            chunks, i = _parse_update_chunks(lines, i)
            hunks.append(Hunk(type="update", path=path, move_to=move_to, chunks=chunks))

    if not hunks:
        raise ValueError("Empty patch: no file operations found")

    return hunks


# --- Fuzzy sequence matching -------------------------------------------------

Comparator = t.Callable[[str, str], bool]


def _try_match(
    lines: list[str],
    pattern: list[str],
    start_index: int,
    compare: Comparator,
    eof: bool = False,
) -> int:
    """Try to find pattern in lines using the given comparator.

    Returns the start index of the match, or -1 if not found.
    """
    if not pattern:
        return -1

    # EOF anchor: try matching from end of file first.
    if eof:
        from_end = len(lines) - len(pattern)
        if from_end >= start_index:
            if all(compare(lines[from_end + j], pattern[j]) for j in range(len(pattern))):
                return from_end

    # Forward search from start_index.
    for i in range(start_index, len(lines) - len(pattern) + 1):
        if all(compare(lines[i + j], pattern[j]) for j in range(len(pattern))):
            return i

    return -1


def seek_sequence(
    lines: list[str],
    pattern: list[str],
    start_index: int,
    eof: bool = False,
) -> int:
    """Find pattern in lines using progressively fuzzier matching.

    4-pass approach:
    1. Exact match
    2. Trailing whitespace ignored (rstrip)
    3. All surrounding whitespace ignored (strip)
    4. Unicode-normalized + stripped

    Returns the start index of the match, or -1 if not found.
    """
    if not pattern:
        return -1

    # Pass 1: exact
    idx = _try_match(lines, pattern, start_index, lambda a, b: a == b, eof)
    if idx != -1:
        return idx

    # Pass 2: rstrip
    idx = _try_match(lines, pattern, start_index, lambda a, b: a.rstrip() == b.rstrip(), eof)
    if idx != -1:
        return idx

    # Pass 3: strip
    idx = _try_match(lines, pattern, start_index, lambda a, b: a.strip() == b.strip(), eof)
    if idx != -1:
        return idx

    # Pass 4: unicode-normalized + strip
    return _try_match(
        lines,
        pattern,
        start_index,
        lambda a, b: _normalize_unicode(a.strip()) == _normalize_unicode(b.strip()),
        eof,
    )


# --- Chunk application -------------------------------------------------------


def compute_replacements(
    original_lines: list[str],
    chunks: list[UpdateChunk],
    file_path: str,
) -> list[tuple[int, int, list[str]]]:
    """Compute (start_idx, old_count, new_lines) replacements for each chunk.

    Raises:
        ValueError: If a chunk's pattern cannot be found in the file.
    """
    replacements: list[tuple[int, int, list[str]]] = []
    line_index = 0

    for chunk in chunks:
        # Context-based seeking.
        if chunk.context:
            ctx_idx = seek_sequence(original_lines, [chunk.context], line_index)
            if ctx_idx == -1:
                raise ValueError(f"Failed to find context in {file_path}: {chunk.context!r}")
            line_index = ctx_idx + 1

        # Pure insertion (no old lines to match).
        if not chunk.old_lines:
            insert_idx = (
                len(original_lines) - 1
                if original_lines and original_lines[-1] == ""
                else len(original_lines)
            )
            replacements.append((insert_idx, 0, chunk.new_lines))
            continue

        # Try to match old_lines in the file.
        pattern = chunk.old_lines
        new_slice = chunk.new_lines
        found = seek_sequence(original_lines, pattern, line_index, chunk.is_eof)

        # Retry without trailing empty line.
        if found == -1 and pattern and pattern[-1] == "":
            pattern = pattern[:-1]
            if new_slice and new_slice[-1] == "":
                new_slice = new_slice[:-1]
            found = seek_sequence(original_lines, pattern, line_index, chunk.is_eof)

        if found == -1:
            preview = "\n".join(chunk.old_lines[:5])
            if len(chunk.old_lines) > 5:
                preview += "\n..."
            raise ValueError(f"Failed to find expected lines in {file_path}:\n{preview}")

        replacements.append((found, len(pattern), new_slice))
        line_index = found + len(pattern)

    replacements.sort(key=lambda r: r[0])
    return replacements


def apply_replacements(
    lines: list[str],
    replacements: list[tuple[int, int, list[str]]],
) -> list[str]:
    """Apply replacements in reverse order to avoid index shifting."""
    result = list(lines)
    for start_idx, old_count, new_segment in reversed(replacements):
        del result[start_idx : start_idx + old_count]
        for j, line in enumerate(new_segment):
            result.insert(start_idx + j, line)
    return result


def derive_new_content(
    original_content: str,
    chunks: list[UpdateChunk],
    file_path: str,
) -> str:
    """Apply update chunks to file content, returning the new content."""
    original_lines = original_content.split("\n")

    # Drop trailing empty element for consistent line counting.
    if original_lines and original_lines[-1] == "":
        original_lines.pop()

    replacements = compute_replacements(original_lines, chunks, file_path)
    new_lines = apply_replacements(original_lines, replacements)

    # Ensure trailing newline.
    if not new_lines or new_lines[-1] != "":
        new_lines.append("")

    return "\n".join(new_lines)


# --- Tool --------------------------------------------------------------------


@tool
async def apply_patch(
    patch_text: t.Annotated[str, "The full patch text describing all file changes"],
    *,
    cwd: t.Annotated[str | None, "Working directory (defaults to current)"] = None,
) -> str:
    """
    Apply a multi-file patch to the filesystem.

    The patch format is a file-oriented diff envelope. You MUST include
    a header to specify the action for each file. Each operation starts
    with one of three headers:

    - ``*** Add File: <path>`` — create a new file. Every following
      line is a ``+`` line (the initial contents).
    - ``*** Delete File: <path>`` — remove an existing file.
    - ``*** Update File: <path>`` — patch an existing file in place.
      Optionally add ``*** Move to: <path>`` to rename it.

    Update sections use ``@@`` context anchors and ``+``/``-``/`` ``
    line prefixes (space = context, ``-`` = remove, ``+`` = add).

    Example::

        *** Begin Patch
        *** Add File: hello.txt
        +Hello world
        *** Update File: src/app.py
        *** Move to: src/main.py
        @@ def greet():
        -print("Hi")
        +print("Hello, world!")
        *** Delete File: obsolete.txt
        *** End Patch

    Important:

    - You MUST wrap the patch in ``*** Begin Patch`` / ``*** End Patch``.
    - You MUST prefix new lines with ``+`` even when creating a new file.
    - Context anchors (``@@``) help locate the right place in the file —
      use a nearby function signature or unique line.

    Args:
        patch_text: The complete patch text.
        cwd: Working directory for resolving relative paths.

    Returns:
        Summary of applied changes.
    """
    base = Path(cwd) if cwd else Path.cwd()
    hunks = parse_patch(patch_text)

    summary: list[str] = []

    for hunk in hunks:
        file_path = base / hunk.path if not Path(hunk.path).is_absolute() else Path(hunk.path)

        if hunk.type == "add":
            file_path.parent.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(file_path, "w") as f:
                await f.write(hunk.contents)
            summary.append(f"A {hunk.path}")

        elif hunk.type == "delete":
            if not file_path.exists():
                raise FileNotFoundError(f"Cannot delete, file not found: {hunk.path}")
            file_path.unlink()
            summary.append(f"D {hunk.path}")

        elif hunk.type == "update":
            if not file_path.exists():
                raise FileNotFoundError(f"Cannot update, file not found: {hunk.path}")
            if not file_path.is_file():
                raise ValueError(f"Cannot update, not a file: {hunk.path}")

            async with aiofiles.open(file_path) as f:
                content = await f.read()

            new_content = derive_new_content(content, hunk.chunks, hunk.path)

            if hunk.move_to:
                target = (
                    base / hunk.move_to
                    if not Path(hunk.move_to).is_absolute()
                    else Path(hunk.move_to)
                )
                target.parent.mkdir(parents=True, exist_ok=True)
                async with aiofiles.open(target, "w") as f:
                    await f.write(new_content)
                file_path.unlink()
                summary.append(f"R {hunk.path} -> {hunk.move_to}")
            else:
                async with aiofiles.open(file_path, "w") as f:
                    await f.write(new_content)
                summary.append(f"M {hunk.path}")

    return f"Applied patch ({len(hunks)} file(s)):\n" + "\n".join(summary)
