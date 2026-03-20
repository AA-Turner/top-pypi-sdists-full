from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from anyio import Path as AsyncPath

from exponent.core.remote_execution.cli_rpc_types import ApplyPatchToolInput, ApplyPatchToolResult
from exponent.core.remote_execution.utils import safe_read_file

_HUNK_HEADER_RE = re.compile(
    r"^@@ -(?P<old_start>\d+)(?:,(?P<old_count>\d+))? \+(?P<new_start>\d+)(?:,(?P<new_count>\d+))? @@(?: .*)?$"
)
_DIFF_HEADER_PREFIXES = ("diff --git ", "index ", "--- ", "+++ ")
_CONTEXT_HUNK_PREFIX = "@@ "
_EMPTY_CONTEXT_HUNK = "@@"
_END_OF_FILE_MARKER = "*** End of File"
_NO_NEWLINE_MARKER = r"\ No newline at end of file"


class ApplyPatchError(ValueError):
    pass


@dataclass
class _DiffLine:
    prefix: str
    text: str
    has_newline: bool = True


@dataclass(frozen=True)
class _UnifiedDiffHunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: tuple[_DiffLine, ...]


@dataclass(frozen=True)
class _ContextDiffHunk:
    change_context: str | None
    lines: tuple[_DiffLine, ...]
    is_end_of_file: bool = False


@dataclass(frozen=True)
class _FileLine:
    text: str
    has_newline: bool


async def execute_apply_patch_tool(
    input_data: ApplyPatchToolInput,
    working_directory: str,
) -> ApplyPatchToolResult:
    try:
        display_path, absolute_path = _resolve_patch_paths(input_data.path, working_directory)
    except ApplyPatchError as exc:
        return ApplyPatchToolResult(status="failed", output=str(exc))

    if input_data.operation_type == "create_file":
        return await _create_file(display_path, absolute_path, input_data.diff or "")
    if input_data.operation_type == "update_file":
        return await _update_file(display_path, absolute_path, input_data.diff or "")
    if input_data.operation_type == "delete_file":
        return await _delete_file(display_path, absolute_path)
    return ApplyPatchToolResult(
        status="failed",
        output=f"apply_patch received an unknown operation type: {input_data.operation_type}",
    )


async def _create_file(
    display_path: str,
    absolute_path: Path,
    diff: str,
) -> ApplyPatchToolResult:
    try:
        exists = await AsyncPath(absolute_path).exists()
    except (OSError, PermissionError) as exc:
        return ApplyPatchToolResult(
            status="failed",
            output=f"Could not inspect '{display_path}' before applying the patch: {exc!s}",
        )
    if exists:
        return ApplyPatchToolResult(
            status="failed",
            output=f"Cannot create '{display_path}' because it already exists.",
        )

    try:
        new_content = apply_unified_diff(original_text="", diff=diff)
    except ApplyPatchError as exc:
        return ApplyPatchToolResult(
            status="failed",
            output=f"Could not build '{display_path}' from the patch: {exc!s}",
        )

    try:
        await _ensure_parent_dir(absolute_path)
        await AsyncPath(absolute_path).write_text(new_content)
    except OSError as exc:
        return ApplyPatchToolResult(status="failed", output=f"Could not write '{display_path}': {exc!s}")
    return ApplyPatchToolResult(status="completed", output=f"Applied patch to create '{display_path}'.")


async def _update_file(
    display_path: str,
    absolute_path: Path,
    diff: str,
) -> ApplyPatchToolResult:
    original_text_or_error = await _read_existing_file(display_path, absolute_path)
    if isinstance(original_text_or_error, ApplyPatchToolResult):
        return original_text_or_error

    try:
        new_content = apply_unified_diff(original_text=original_text_or_error, diff=diff)
    except ApplyPatchError as exc:
        return ApplyPatchToolResult(
            status="failed",
            output=f"Could not apply the patch to '{display_path}': {exc!s}",
        )

    try:
        await AsyncPath(absolute_path).write_text(new_content)
    except OSError as exc:
        return ApplyPatchToolResult(status="failed", output=f"Could not write '{display_path}': {exc!s}")
    return ApplyPatchToolResult(status="completed", output=f"Applied patch to update '{display_path}'.")


async def _delete_file(
    display_path: str,
    absolute_path: Path,
) -> ApplyPatchToolResult:
    path = AsyncPath(absolute_path)
    try:
        exists = await path.exists()
    except (OSError, PermissionError) as exc:
        return ApplyPatchToolResult(
            status="failed",
            output=f"Could not inspect '{display_path}' before applying the patch: {exc!s}",
        )
    if not exists:
        return ApplyPatchToolResult(
            status="failed",
            output=f"Cannot delete '{display_path}' because it does not exist.",
        )

    try:
        await path.unlink()
    except OSError as exc:
        return ApplyPatchToolResult(status="failed", output=f"Could not delete '{display_path}': {exc!s}")
    return ApplyPatchToolResult(status="completed", output=f"Applied patch to delete '{display_path}'.")


async def _read_existing_file(display_path: str, absolute_path: Path) -> str | ApplyPatchToolResult:
    path = AsyncPath(absolute_path)
    try:
        exists = await path.exists()
    except (OSError, PermissionError) as exc:
        return ApplyPatchToolResult(
            status="failed",
            output=f"Could not read '{display_path}' before applying the patch: {exc!s}",
        )

    if not exists:
        return ApplyPatchToolResult(
            status="failed",
            output=f"Could not read '{display_path}' before applying the patch: File not found",
        )

    try:
        if await path.is_dir():
            return ApplyPatchToolResult(
                status="failed",
                output=f"Could not read '{display_path}' before applying the patch: {absolute_path} is a directory",
            )
    except (OSError, PermissionError) as exc:
        return ApplyPatchToolResult(
            status="failed",
            output=f"Could not read '{display_path}' before applying the patch: {exc!s}",
        )

    try:
        return await safe_read_file(path)
    except PermissionError:
        return ApplyPatchToolResult(
            status="failed",
            output=f"Could not read '{display_path}' before applying the patch: Permission denied: cannot read {absolute_path}",
        )
    except UnicodeDecodeError:
        return ApplyPatchToolResult(
            status="failed",
            output=f"Could not read '{display_path}' before applying the patch: File appears to be binary or has invalid text encoding",
        )
    except Exception as exc:
        return ApplyPatchToolResult(
            status="failed",
            output=f"Could not read '{display_path}' before applying the patch: Error reading file: {exc!s}",
        )


async def _ensure_parent_dir(path: Path) -> None:
    parent = path.parent
    if str(parent) != ".":
        await AsyncPath(parent).mkdir(parents=True, exist_ok=True)


def _resolve_patch_paths(raw_path: str, working_directory: str) -> tuple[str, Path]:
    candidate = raw_path.strip()
    if not candidate:
        raise ApplyPatchError("apply_patch paths must not be empty.")
    if "\\" in candidate:
        raise ApplyPatchError("apply_patch paths must use forward slashes.")

    normalized_path = PurePosixPath(candidate)
    if normalized_path.is_absolute():
        display_path = normalized_path.as_posix()
        return display_path, Path(display_path)

    display_path = _validate_workspace_relative_path(candidate)
    return display_path, Path(working_directory, display_path)


def _validate_workspace_relative_path(path: str) -> str:
    candidate = path.strip()
    if not candidate:
        raise ApplyPatchError("apply_patch paths must not be empty.")
    if "\\" in candidate:
        raise ApplyPatchError("apply_patch paths must use forward slashes.")

    normalized_path = PurePosixPath(candidate)
    if normalized_path.is_absolute():
        raise ApplyPatchError("apply_patch paths must be relative to the workspace root.")

    cleaned_parts = []
    for part in normalized_path.parts:
        if part in {"", "."}:
            continue
        if part == "..":
            raise ApplyPatchError("apply_patch paths must stay within the workspace root.")
        cleaned_parts.append(part)

    if not cleaned_parts:
        raise ApplyPatchError("apply_patch paths must point to a file inside the workspace root.")

    return PurePosixPath(*cleaned_parts).as_posix()


def apply_unified_diff(*, original_text: str, diff: str) -> str:
    if not diff.strip():
        return original_text

    lines = _normalize_diff_lines(diff)
    diff_format = _detect_diff_format(lines)
    if diff_format == "unified":
        hunks = _parse_unified_diff_lines(lines)
        if not hunks:
            return original_text
        return _apply_unified_hunks(original_text=original_text, hunks=hunks)
    if diff_format == "context":
        hunks = _parse_context_diff_lines(lines)
        if not hunks:
            return original_text
        return _apply_context_hunks(original_text=original_text, hunks=hunks)
    return original_text


def _normalize_diff_lines(diff: str) -> list[str]:
    return [line.rstrip("\r") for line in diff.splitlines()]


def _detect_diff_format(lines: list[str]) -> str | None:
    for line in lines:
        if not line or line.startswith(_DIFF_HEADER_PREFIXES):
            continue
        if _HUNK_HEADER_RE.match(line):
            return "unified"
        if _is_context_hunk_header(line):
            return "context"
        raise ApplyPatchError(f"Unsupported apply_patch diff line: {line}")
    return None


def _apply_unified_hunks(*, original_text: str, hunks: list[_UnifiedDiffHunk]) -> str:
    original_lines = _split_file_lines(original_text)
    output_lines: list[_FileLine] = []
    source_index = 0

    for hunk in hunks:
        expected_source_index = _resolve_hunk_source_index(hunk)
        if expected_source_index < source_index:
            raise ApplyPatchError("apply_patch hunks overlap or are out of order.")
        if expected_source_index > len(original_lines):
            raise ApplyPatchError("apply_patch hunk starts past the end of the file.")

        output_lines.extend(original_lines[source_index:expected_source_index])
        source_index = expected_source_index
        hunk_source_index = source_index

        for diff_line in hunk.lines:
            if diff_line.prefix == " ":
                actual_line = _get_source_line(original_lines, source_index)
                _assert_line_matches(actual_line, diff_line.text)
                output_lines.append(actual_line)
                source_index += 1
            elif diff_line.prefix == "-":
                actual_line = _get_source_line(original_lines, source_index)
                _assert_line_matches(actual_line, diff_line.text)
                source_index += 1
            elif diff_line.prefix == "+":
                output_lines.append(_FileLine(text=diff_line.text, has_newline=diff_line.has_newline))
            else:
                raise ApplyPatchError(f"Unsupported unified diff line prefix: {diff_line.prefix}")

        consumed_old = source_index - hunk_source_index
        produced_new = sum(1 for line in hunk.lines if line.prefix != "-")
        if consumed_old != hunk.old_count:
            raise ApplyPatchError("apply_patch old-line count did not match the diff header.")
        if produced_new != hunk.new_count:
            raise ApplyPatchError("apply_patch new-line count did not match the diff header.")

    output_lines.extend(original_lines[source_index:])
    return _render_file_lines(output_lines)


def _apply_context_hunks(*, original_text: str, hunks: list[_ContextDiffHunk]) -> str:
    output_lines = _split_file_lines(original_text)
    search_index = 0

    for hunk in hunks:
        if hunk.change_context is not None:
            context_index = _seek_sequence(output_lines, [hunk.change_context], search_index, False)
            if context_index is None:
                raise ApplyPatchError(f"apply_patch could not find context line: {hunk.change_context!r}")
            search_index = context_index + 1

        pattern = [line.text for line in hunk.lines if line.prefix != "+"]
        match_index = _seek_sequence(output_lines, pattern, search_index, hunk.is_end_of_file)
        if match_index is None:
            if not pattern:
                raise ApplyPatchError("apply_patch context hunk could not determine where to insert new lines.")
            raise ApplyPatchError(
                "apply_patch diff did not match the current file contents.\nExpected lines:\n" + "\n".join(pattern)
            )

        matched_lines = output_lines[match_index : match_index + len(pattern)]
        replacement_lines = _build_context_replacement(hunk, matched_lines)
        output_lines[match_index : match_index + len(pattern)] = replacement_lines
        search_index = match_index + len(replacement_lines)

    return _render_file_lines(output_lines)


def _parse_unified_diff_lines(lines: list[str]) -> list[_UnifiedDiffHunk]:
    index = 0
    hunks: list[_UnifiedDiffHunk] = []

    while index < len(lines):
        line = lines[index]
        if not line:
            index += 1
            continue
        if line.startswith(_DIFF_HEADER_PREFIXES):
            index += 1
            continue

        match = _HUNK_HEADER_RE.match(line)
        if match is None:
            raise ApplyPatchError(f"Unsupported apply_patch diff line: {line}")

        old_count = int(match.group("old_count") or "1")
        new_count = int(match.group("new_count") or "1")
        index += 1

        hunk_lines: list[_DiffLine] = []
        while index < len(lines):
            next_line = lines[index]
            if _HUNK_HEADER_RE.match(next_line) or next_line.startswith(_DIFF_HEADER_PREFIXES):
                break
            if next_line == _NO_NEWLINE_MARKER:
                if not hunk_lines:
                    raise ApplyPatchError("apply_patch diff used a no-newline marker before any hunk line.")
                hunk_lines[-1].has_newline = False
                index += 1
                continue
            if next_line and next_line[0] in {" ", "+", "-"}:
                hunk_lines.append(_DiffLine(prefix=next_line[0], text=next_line[1:]))
                index += 1
                continue
            raise ApplyPatchError(f"Unsupported apply_patch hunk line: {next_line}")

        consumed_old = sum(1 for hunk_line in hunk_lines if hunk_line.prefix != "+")
        produced_new = sum(1 for hunk_line in hunk_lines if hunk_line.prefix != "-")
        if consumed_old != old_count:
            raise ApplyPatchError("apply_patch old-line count did not match the diff body.")
        if produced_new != new_count:
            raise ApplyPatchError("apply_patch new-line count did not match the diff body.")

        hunks.append(
            _UnifiedDiffHunk(
                old_start=int(match.group("old_start")),
                old_count=old_count,
                new_start=int(match.group("new_start")),
                new_count=new_count,
                lines=tuple(hunk_lines),
            )
        )

    return hunks


def _parse_context_diff_lines(lines: list[str]) -> list[_ContextDiffHunk]:
    index = 0
    hunks: list[_ContextDiffHunk] = []

    while index < len(lines):
        line = lines[index]
        if not line:
            index += 1
            continue
        if line.startswith(_DIFF_HEADER_PREFIXES):
            index += 1
            continue

        if line == _EMPTY_CONTEXT_HUNK:
            change_context = None
        elif line.startswith(_CONTEXT_HUNK_PREFIX):
            change_context = line[len(_CONTEXT_HUNK_PREFIX) :]
        else:
            raise ApplyPatchError(f"Unsupported apply_patch diff line: {line}")
        index += 1

        hunk_lines: list[_DiffLine] = []
        is_end_of_file = False
        while index < len(lines):
            next_line = lines[index]
            if _is_context_hunk_header(next_line) or next_line.startswith(_DIFF_HEADER_PREFIXES):
                break
            if next_line == _END_OF_FILE_MARKER:
                if not hunk_lines:
                    raise ApplyPatchError("apply_patch diff used an end-of-file marker before any hunk line.")
                is_end_of_file = True
                index += 1
                break
            if next_line == _NO_NEWLINE_MARKER:
                if not hunk_lines:
                    raise ApplyPatchError("apply_patch diff used a no-newline marker before any hunk line.")
                hunk_lines[-1].has_newline = False
                index += 1
                continue
            if next_line == "":
                hunk_lines.append(_DiffLine(prefix=" ", text=""))
                index += 1
                continue
            if next_line[0] in {" ", "+", "-"}:
                hunk_lines.append(_DiffLine(prefix=next_line[0], text=next_line[1:]))
                index += 1
                continue
            raise ApplyPatchError(f"Unsupported apply_patch hunk line: {next_line}")

        if not hunk_lines:
            raise ApplyPatchError("apply_patch context hunk did not contain any lines.")

        hunks.append(
            _ContextDiffHunk(change_context=change_context, lines=tuple(hunk_lines), is_end_of_file=is_end_of_file)
        )

    return hunks


def _resolve_hunk_source_index(hunk: _UnifiedDiffHunk) -> int:
    if hunk.old_count == 0:
        return hunk.old_start
    return max(hunk.old_start - 1, 0)


def _is_context_hunk_header(line: str) -> bool:
    return line == _EMPTY_CONTEXT_HUNK or line.startswith(_CONTEXT_HUNK_PREFIX)


def _build_context_replacement(hunk: _ContextDiffHunk, matched_lines: list[_FileLine]) -> list[_FileLine]:
    replacement_lines: list[_FileLine] = []
    matched_index = 0

    for diff_line in hunk.lines:
        if diff_line.prefix == " ":
            actual_line = _get_source_line(matched_lines, matched_index)
            _assert_line_matches(actual_line, diff_line.text)
            replacement_lines.append(actual_line)
            matched_index += 1
        elif diff_line.prefix == "-":
            actual_line = _get_source_line(matched_lines, matched_index)
            _assert_line_matches(actual_line, diff_line.text)
            matched_index += 1
        elif diff_line.prefix == "+":
            replacement_lines.append(_FileLine(text=diff_line.text, has_newline=diff_line.has_newline))
        else:  # pragma: no cover - defensive branch
            raise ApplyPatchError(f"Unsupported apply_patch context line prefix: {diff_line.prefix}")

    if matched_index != len(matched_lines):
        raise ApplyPatchError("apply_patch context hunk did not consume the expected source lines.")

    return replacement_lines


def _seek_sequence(lines: list[_FileLine], pattern: list[str], start: int, eof: bool) -> int | None:
    if not pattern:
        return len(lines) if eof else start
    if len(pattern) > len(lines):
        return None

    search_start = len(lines) - len(pattern) if eof and len(lines) >= len(pattern) else start
    last_index = len(lines) - len(pattern)
    for normalizer in (_identity, str.rstrip, str.strip, _normalise):
        for index in range(search_start, last_index + 1):
            if _matches_with(lines, pattern, index, normalizer):
                return index
    return None


def _matches_with(lines: list[_FileLine], pattern: list[str], start: int, normalizer: Callable[[str], str]) -> bool:
    if start + len(pattern) > len(lines):
        return False
    for offset, expected_text in enumerate(pattern):
        if normalizer(lines[start + offset].text) != normalizer(expected_text):
            return False
    return True


def _identity(value: str) -> str:
    return value


def _split_file_lines(text: str) -> list[_FileLine]:
    if not text:
        return []

    lines: list[_FileLine] = []
    for raw_line in text.splitlines(keepends=True):
        has_newline = raw_line.endswith("\n")
        stripped = raw_line[:-1] if has_newline else raw_line
        if stripped.endswith("\r"):
            stripped = stripped[:-1]
        lines.append(_FileLine(text=stripped, has_newline=has_newline))
    return lines


def _render_file_lines(lines: list[_FileLine]) -> str:
    return "".join(line.text + ("\n" if line.has_newline else "") for line in lines)


def _get_source_line(lines: list[_FileLine], index: int) -> _FileLine:
    try:
        return lines[index]
    except IndexError as exc:  # pragma: no cover - defensive branch
        raise ApplyPatchError("apply_patch expected more source lines than were available.") from exc


def _assert_line_matches(actual_line: _FileLine, expected_text: str) -> None:
    if _same_line(actual_line.text, expected_text):
        return
    raise ApplyPatchError(
        "apply_patch diff did not match the current file contents.\n"
        f"Expected: {expected_text!r}\n"
        f"Actual: {actual_line.text!r}"
    )


def _same_line(actual: str, expected: str) -> bool:
    if actual == expected:
        return True
    if actual.rstrip() == expected.rstrip():
        return True
    if actual.strip() == expected.strip():
        return True
    return _normalise(actual) == _normalise(expected)


def _normalise(value: str) -> str:
    mapping = {
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2015": "-",
        "\u2212": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201a": "'",
        "\u201b": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u201e": '"',
        "\u201f": '"',
        "\u00a0": " ",
        "\u2002": " ",
        "\u2003": " ",
        "\u2004": " ",
        "\u2005": " ",
        "\u2006": " ",
        "\u2007": " ",
        "\u2008": " ",
        "\u2009": " ",
        "\u200a": " ",
        "\u202f": " ",
        "\u205f": " ",
        "\u3000": " ",
    }
    return "".join(mapping.get(ch, ch) for ch in value.strip())
