"""
Surgical file editing tools with fuzzy matching.

Implements sophisticated text replacement with multiple fallback strategies
for handling whitespace, indentation, and minor formatting differences.

Strategies (in order, most strict to most lenient):
1. Simple exact match
2. Line-trimmed comparison (ignores per-line leading/trailing whitespace)
3. Block anchor matching (first/last line anchors + Levenshtein middle)
4. Whitespace normalized matching (collapses all whitespace to single space)
5. Indentation flexible matching (ignores common indentation)
6. Escape normalized matching (unescapes \\n, \\t, etc.)
7. Trimmed boundary matching (strips leading/trailing whitespace from find)
"""

import re
import typing as t
from collections.abc import Iterator
from pathlib import Path

import aiofiles

from dreadnode.agents.tools import tool

Replacer = t.Callable[[str, str], Iterator[str]]


# --- Utilities ----------------------------------------------------------------


def _levenshtein(a: str, b: str) -> int:
    """Levenshtein distance between two strings."""
    if not a or not b:
        return max(len(a), len(b))

    matrix = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        matrix[i][0] = i
    for j in range(len(b) + 1):
        matrix[0][j] = j

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost,
            )

    return matrix[len(a)][len(b)]


def _extract_block(content_lines: list[str], start: int, end: int, content: str) -> str:
    """Extract a block of lines [start, end] from content as a substring."""
    start_idx = sum(len(line) + 1 for line in content_lines[:start])
    end_idx = start_idx + sum(
        len(content_lines[start + k]) + (1 if k < end - start else 0)
        for k in range(end - start + 1)
    )
    return content[start_idx:end_idx]


def _unescape(s: str) -> str:
    """Unescape common escape sequences in a string."""
    _ESCAPE_MAP = {  # noqa: N806
        "n": "\n",
        "t": "\t",
        "r": "\r",
        "'": "'",
        '"': '"',
        "`": "`",
        "\\": "\\",
        "\n": "\n",
        "$": "$",
    }

    def _replace(m: re.Match[str]) -> str:
        return _ESCAPE_MAP.get(m.group(1), m.group(0))

    return re.sub(r"\\(n|t|r|'|\"|`|\\|\n|\$)", _replace, s)


# --- Replacer strategies -----------------------------------------------------


def _simple_replacer(content: str, find: str) -> Iterator[str]:
    """Exact match — the baseline strategy."""
    if find in content:
        yield find


def _line_trimmed_replacer(content: str, find: str) -> Iterator[str]:
    """Match with trimmed line comparison (preserves original whitespace)."""
    content_lines = content.split("\n")
    find_lines = find.split("\n")

    if find_lines and find_lines[-1] == "":
        find_lines.pop()

    if not find_lines:
        return

    for i in range(len(content_lines) - len(find_lines) + 1):
        matches = True

        for j in range(len(find_lines)):
            if content_lines[i + j].strip() != find_lines[j].strip():
                matches = False
                break

        if matches:
            start_idx = sum(len(line) + 1 for line in content_lines[:i])
            end_idx = start_idx + sum(
                len(content_lines[i + k]) + (1 if k < len(find_lines) - 1 else 0)
                for k in range(len(find_lines))
            )
            yield content[start_idx:end_idx]


def _block_anchor_replacer(content: str, find: str) -> Iterator[str]:
    """Match using first/last line as anchors with fuzzy middle matching."""
    content_lines = content.split("\n")
    find_lines = find.split("\n")

    if len(find_lines) < 3:
        return

    if find_lines and find_lines[-1] == "":
        find_lines.pop()

    if len(find_lines) < 2:
        return

    first_line = find_lines[0].strip()
    last_line = find_lines[-1].strip()

    # Collect candidate blocks with matching first/last lines.
    candidates: list[tuple[int, int]] = []
    for i, line in enumerate(content_lines):
        if line.strip() != first_line:
            continue
        for j in range(i + 2, len(content_lines)):
            if content_lines[j].strip() == last_line:
                candidates.append((i, j))
                break

    if not candidates:
        return

    # Single candidate: accept unconditionally (matching opencode behavior).
    if len(candidates) == 1:
        start, end = candidates[0]
        yield _extract_block(content_lines, start, end, content)
        return

    # Multiple candidates: pick best by Levenshtein similarity of middle lines.
    best_match: tuple[int, int] | None = None
    max_similarity = -1.0

    for start, end in candidates:
        actual_size = end - start + 1
        lines_to_check = min(len(find_lines) - 2, actual_size - 2)

        if lines_to_check <= 0:
            similarity = 1.0
        else:
            similarity = 0.0
            for j in range(1, min(len(find_lines) - 1, actual_size - 1)):
                orig = content_lines[start + j].strip()
                search = find_lines[j].strip()
                max_len = max(len(orig), len(search))
                if max_len == 0:
                    continue
                dist = _levenshtein(orig, search)
                similarity += (1 - dist / max_len) / lines_to_check

        if similarity > max_similarity:
            max_similarity = similarity
            best_match = (start, end)

    if best_match and max_similarity >= 0.3:
        start, end = best_match
        yield _extract_block(content_lines, start, end, content)


def _whitespace_normalized_replacer(content: str, find: str) -> Iterator[str]:
    """Match with normalized whitespace (collapses runs of whitespace to single space)."""

    def normalize(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    normalized_find = normalize(find)
    lines = content.split("\n")

    # Single-line matches.
    for line in lines:
        if normalize(line) == normalized_find:
            yield line
        elif normalized_find in normalize(line):
            words = find.strip().split()
            if words:
                pattern = r"\s+".join(re.escape(w) for w in words)
                match = re.search(pattern, line)
                if match:
                    yield match.group(0)

    # Multi-line matches.
    find_lines = find.split("\n")
    if len(find_lines) > 1:
        for i in range(len(lines) - len(find_lines) + 1):
            block = lines[i : i + len(find_lines)]
            if normalize("\n".join(block)) == normalized_find:
                yield "\n".join(block)


def _indentation_flexible_replacer(content: str, find: str) -> Iterator[str]:
    """Match ignoring common indentation."""

    def remove_indent(text: str) -> str:
        lines = text.split("\n")
        non_empty = [line for line in lines if line.strip()]
        if not non_empty:
            return text
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        return "\n".join(line if not line.strip() else line[min_indent:] for line in lines)

    normalized_find = remove_indent(find)
    content_lines = content.split("\n")
    find_lines = find.split("\n")

    for i in range(len(content_lines) - len(find_lines) + 1):
        block = "\n".join(content_lines[i : i + len(find_lines)])
        if remove_indent(block) == normalized_find:
            yield block


def _escape_normalized_replacer(content: str, find: str) -> Iterator[str]:
    """Match after unescaping common escape sequences (\\n, \\t, \\\\, etc.).

    Handles cases where the LLM sends escaped characters that don't match
    the literal content in the file.
    """
    unescaped_find = _unescape(find)

    # No escapes were present — nothing to do (simple_replacer already tried).
    if unescaped_find == find:
        return

    # Direct match with unescaped version.
    if unescaped_find in content:
        yield unescaped_find

    # Block-level matching with unescaped comparison.
    lines = content.split("\n")
    find_lines = unescaped_find.split("\n")

    for i in range(len(lines) - len(find_lines) + 1):
        block = "\n".join(lines[i : i + len(find_lines)])
        if _unescape(block) == unescaped_find:
            yield block


def _trimmed_boundary_replacer(content: str, find: str) -> Iterator[str]:
    """Match with trimmed boundaries (strips leading/trailing whitespace from find)."""
    trimmed = find.strip()
    if trimmed == find:
        return

    # Only use block-level matching to avoid yielding substrings that lose
    # surrounding context. This also prevents duplicate yields.
    lines = content.split("\n")
    find_lines = find.split("\n")

    for i in range(len(lines) - len(find_lines) + 1):
        block = "\n".join(lines[i : i + len(find_lines)])
        if block.strip() == trimmed:
            yield block


_REPLACERS: list[Replacer] = [
    _simple_replacer,
    _line_trimmed_replacer,
    _block_anchor_replacer,
    _whitespace_normalized_replacer,
    _indentation_flexible_replacer,
    _escape_normalized_replacer,
    _trimmed_boundary_replacer,
]


# --- Core replace logic ------------------------------------------------------


def replace_string(
    content: str,
    old_string: str,
    new_string: str,
    *,
    replace_all: bool = False,
) -> str:
    """Replace old_string with new_string using fuzzy matching.

    Tries multiple matching strategies in order from most strict to most
    lenient. For non-replace_all operations, the match must be unique
    in the file content.

    Args:
        content: Original file content.
        old_string: String to find (with fuzzy matching).
        new_string: String to replace with.
        replace_all: If True, replace all occurrences.

    Returns:
        Modified content.

    Raises:
        ValueError: If old_string == new_string, not found, or ambiguous.
    """
    if old_string == new_string:
        raise ValueError("old_string and new_string must be different")

    found_any = False

    for replacer in _REPLACERS:
        for match in replacer(content, old_string):
            if match not in content:
                continue

            found_any = True

            if replace_all:
                return content.replace(match, new_string)

            # Uniqueness check: indexOf != lastIndexOf equivalent.
            idx = content.find(match)
            last_idx = content.rfind(match)
            if idx != last_idx:
                continue

            return content[:idx] + new_string + content[idx + len(match) :]

    if not found_any:
        raise ValueError("oldString not found in content")

    raise ValueError(
        "Found multiple matches for oldString. "
        "Provide more surrounding context to make the match unique."
    )


# --- Tools --------------------------------------------------------------------


@tool
async def edit_file(
    path: t.Annotated[str, "Path to the file to edit"],
    old_string: t.Annotated[str, "Text to replace (fuzzy matching supported)"],
    new_string: t.Annotated[str, "Replacement text"],
    *,
    replace_all: t.Annotated[bool, "Replace all occurrences"] = False,
    cwd: t.Annotated[str | None, "Working directory (defaults to current)"] = None,
) -> str:
    """
    Perform surgical text replacement in a file with fuzzy matching.

    You MUST use the ``read`` tool at least once before editing a file to
    understand the exact content. Preserve the exact indentation
    (tabs/spaces) as it appears in the file.

    - The edit will FAIL if ``old_string`` is not found in the file.
    - The edit will FAIL if ``old_string`` matches multiple locations.
      Provide more surrounding context to make the match unique, or use
      ``replace_all=True`` to change every occurrence.
    - For multiple edits to the same file, prefer ``multiedit``.
    - Use ``replace_all=True`` for renaming variables/functions across
      the file.

    Args:
        path: Path to the file to edit.
        old_string: Text to find (fuzzy matching supported).
        new_string: Replacement text.
        replace_all: Replace all occurrences. Default: False.
        cwd: Working directory for relative paths.

    Returns:
        Success message with edit details.
    """
    base = Path(cwd) if cwd else Path.cwd()
    file_path = base / path if not Path(path).is_absolute() else Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not file_path.is_file():
        raise ValueError(f"Not a file: {path}")

    async with aiofiles.open(file_path) as f:
        content = await f.read()

    try:
        new_content = replace_string(content, old_string, new_string, replace_all=replace_all)
    except ValueError as e:
        msg = str(e)
        if "not found" in msg:
            preview = old_string[:100] + "..." if len(old_string) > 100 else old_string
            raise ValueError(
                f"String not found in {path}. "
                f"Ensure the text exists in the file.\n"
                f"Looking for: {preview!r}"
            ) from e
        raise

    async with aiofiles.open(file_path, "w") as f:
        await f.write(new_content)

    old_lines = old_string.count("\n") + 1
    new_lines = new_string.count("\n") + 1
    diff = new_lines - old_lines
    diff_str = f"+{diff}" if diff > 0 else str(diff) if diff < 0 else "±0"

    return f"Edited {path}: replaced {old_lines} lines with {new_lines} lines ({diff_str})"


@tool
async def multiedit(
    path: t.Annotated[str, "Path to the file to edit"],
    edits: t.Annotated[
        list[dict[str, t.Any]],
        "Array of edits: [{old_string, new_string, replace_all?}, ...]",
    ],
    *,
    cwd: t.Annotated[str | None, "Working directory (defaults to current)"] = None,
) -> str:
    """
    Apply multiple edits to a single file in one operation.

    Prefer this tool over ``edit_file`` when you need to make multiple
    changes to the same file. Each edit in the array should have:

    - ``old_string``: text to find (must match file contents)
    - ``new_string``: replacement text
    - ``replace_all`` (optional): replace all occurrences

    All edits are applied **in sequence** — each edit operates on the
    result of the previous one. All edits must succeed or none are
    applied. Since edits are sequential, ensure earlier edits don't
    affect the text that later edits are trying to find.

    Args:
        path: Path to the file.
        edits: List of edit operations.
        cwd: Working directory for relative paths.

    Returns:
        Summary of all edits applied.
    """
    base = Path(cwd) if cwd else Path.cwd()
    file_path = base / path if not Path(path).is_absolute() else Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not file_path.is_file():
        raise ValueError(f"Not a file: {path}")

    async with aiofiles.open(file_path) as f:
        content = await f.read()

    applied = 0
    for i, edit in enumerate(edits):
        old_string = edit.get("old_string", "")
        new_string = edit.get("new_string", "")
        replace_all = edit.get("replace_all", False)

        if not old_string:
            raise ValueError(f"Edit {i + 1}: old_string is required")

        content = replace_string(content, old_string, new_string, replace_all=replace_all)
        applied += 1

    async with aiofiles.open(file_path, "w") as f:
        await f.write(content)

    return f"Applied {applied} edit(s) to {path}"


@tool
async def insert_lines(
    path: t.Annotated[str, "Path to the file"],
    line_number: t.Annotated[int, "Line number to insert at (1-indexed)"],
    content: t.Annotated[str, "Content to insert"],
    *,
    cwd: t.Annotated[str | None, "Working directory"] = None,
) -> str:
    """
    Insert content at a specific line number.

    Line numbers are 1-indexed. Content is inserted BEFORE the specified line.
    Use line_number=1 to insert at the beginning.
    Use a line number past the end to append.

    Args:
        path: Path to the file.
        line_number: Line to insert before (1-indexed).
        content: Content to insert.
        cwd: Working directory for relative paths.

    Returns:
        Success message.
    """
    base = Path(cwd) if cwd else Path.cwd()
    file_path = base / path if not Path(path).is_absolute() else Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    async with aiofiles.open(file_path) as f:
        lines = await f.readlines()

    if not content.endswith("\n"):
        content += "\n"

    idx = max(0, min(line_number - 1, len(lines)))
    content_lines = content.splitlines(keepends=True)
    for i, line in enumerate(content_lines):
        lines.insert(idx + i, line if line.endswith("\n") else line + "\n")

    async with aiofiles.open(file_path, "w") as f:
        await f.writelines(lines)

    return f"Inserted {len(content_lines)} line(s) at line {line_number} in {path}"


@tool
async def delete_lines(
    path: t.Annotated[str, "Path to the file"],
    start_line: t.Annotated[int, "First line to delete (1-indexed)"],
    end_line: t.Annotated[int, "Last line to delete (inclusive)"],
    *,
    cwd: t.Annotated[str | None, "Working directory"] = None,
) -> str:
    """
    Delete a range of lines from a file.

    Line numbers are 1-indexed and inclusive on both ends.

    Args:
        path: Path to the file.
        start_line: First line to delete (1-indexed).
        end_line: Last line to delete (1-indexed, inclusive).
        cwd: Working directory for relative paths.

    Returns:
        Success message with deleted line count.
    """
    base = Path(cwd) if cwd else Path.cwd()
    file_path = base / path if not Path(path).is_absolute() else Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    async with aiofiles.open(file_path) as f:
        lines = await f.readlines()

    if start_line < 1 or end_line < start_line:
        raise ValueError(f"Invalid line range: {start_line}-{end_line}")

    start_idx = start_line - 1
    end_idx = min(end_line, len(lines))

    deleted_count = end_idx - start_idx
    del lines[start_idx:end_idx]

    async with aiofiles.open(file_path, "w") as f:
        await f.writelines(lines)

    return f"Deleted {deleted_count} line(s) from {path}"
