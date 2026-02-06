from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import anyio
from anyio import Path as AsyncPath

BEGIN_PATCH = "*** Begin Patch"
END_PATCH = "*** End Patch"
ADD_FILE = "*** Add File: "
DELETE_FILE = "*** Delete File: "
UPDATE_FILE = "*** Update File: "
MOVE_TO = "*** Move to: "
EOF_MARKER = "*** End of File"
CHANGE_CONTEXT = "@@ "
EMPTY_CHANGE_CONTEXT = "@@"


class PatchError(Exception):
    pass


class InvalidPatchError(PatchError):
    pass


class InvalidHunkError(PatchError):
    def __init__(self, message: str, line_number: int) -> None:
        super().__init__(message)
        self.line_number = line_number


@dataclass
class UpdateFileChunk:
    change_context: str | None
    old_lines: list[str]
    new_lines: list[str]
    is_end_of_file: bool = False


@dataclass
class AddFile:
    path: str
    contents: str


@dataclass
class DeleteFile:
    path: str


@dataclass
class UpdateFile:
    path: str
    move_path: str | None
    chunks: list[UpdateFileChunk]


Hunk = AddFile | DeleteFile | UpdateFile


@dataclass
class AffectedPaths:
    added: list[Path]
    modified: list[Path]
    deleted: list[Path]


def parse_patch(patch: str) -> list[Hunk]:
    lines = _normalize_lines(patch)
    lines = _check_patch_boundaries_lenient(lines)
    if len(lines) < 2:
        raise InvalidPatchError("The first line of the patch must be '*** Begin Patch'")
    hunks: list[Hunk] = []
    remaining = lines[1:-1]
    line_number = 2
    index = 0
    while index < len(remaining):
        hunk, consumed = _parse_one_hunk(remaining[index:], line_number)
        hunks.append(hunk)
        index += consumed
        line_number += consumed
    return hunks


def _normalize_lines(patch: str) -> list[str]:
    return [line.rstrip("\r") for line in patch.strip().split("\n")]


def _check_patch_boundaries_lenient(lines: list[str]) -> list[str]:
    try:
        _check_patch_boundaries_strict(lines)
        return lines
    except InvalidPatchError as err:
        if not lines:
            raise err
        first = lines[0]
        last = lines[-1]
        if first in ("<<EOF", "<<'EOF'", '<<"EOF"') and last.endswith("EOF") and len(lines) >= 4:
            inner = lines[1:-1]
            _check_patch_boundaries_strict(inner)
            return inner
        raise err


def _check_patch_boundaries_strict(lines: list[str]) -> None:
    if not lines:
        raise InvalidPatchError("The first line of the patch must be '*** Begin Patch'")
    first = lines[0].strip()
    last = lines[-1].strip()
    if first != BEGIN_PATCH:
        raise InvalidPatchError("The first line of the patch must be '*** Begin Patch'")
    if last != END_PATCH:
        raise InvalidPatchError("The last line of the patch must be '*** End Patch'")


def _parse_one_hunk(lines: list[str], line_number: int) -> tuple[Hunk, int]:
    first_line = lines[0].strip()
    if first_line.startswith(ADD_FILE):
        path = first_line[len(ADD_FILE) :]
        contents = ""
        parsed_lines = 1
        for add_line in lines[1:]:
            if add_line.startswith("+"):
                contents += add_line[1:] + "\n"
                parsed_lines += 1
            else:
                break
        return AddFile(path=path, contents=contents), parsed_lines
    if first_line.startswith(DELETE_FILE):
        path = first_line[len(DELETE_FILE) :]
        return DeleteFile(path=path), 1
    if first_line.startswith(UPDATE_FILE):
        path = first_line[len(UPDATE_FILE) :]
        remaining = lines[1:]
        parsed_lines = 1
        move_path = None
        if remaining and remaining[0].startswith(MOVE_TO):
            move_path = remaining[0][len(MOVE_TO) :]
            remaining = remaining[1:]
            parsed_lines += 1

        chunks: list[UpdateFileChunk] = []
        while remaining:
            if remaining[0].strip() == "":
                parsed_lines += 1
                remaining = remaining[1:]
                continue
            if remaining[0].startswith("***"):
                break
            chunk, chunk_lines = _parse_update_file_chunk(remaining, line_number + parsed_lines, len(chunks) == 0)
            chunks.append(chunk)
            parsed_lines += chunk_lines
            remaining = remaining[chunk_lines:]

        if not chunks:
            raise InvalidHunkError(f"Update file hunk for path '{path}' is empty", line_number)
        return UpdateFile(path=path, move_path=move_path, chunks=chunks), parsed_lines

    raise InvalidHunkError(
        f"'{first_line}' is not a valid hunk header. Valid hunk headers: "
        f"'*** Add File: {{path}}', '*** Delete File: {{path}}', "
        f"'*** Update File: {{path}}'",
        line_number,
    )


def _parse_update_file_chunk(
    lines: list[str], line_number: int, allow_missing_context: bool
) -> tuple[UpdateFileChunk, int]:
    if not lines:
        raise InvalidHunkError("Update hunk does not contain any lines", line_number)

    if lines[0] == EMPTY_CHANGE_CONTEXT:
        change_context = None
        start_index = 1
    elif lines[0].startswith(CHANGE_CONTEXT):
        change_context = lines[0][len(CHANGE_CONTEXT) :]
        start_index = 1
    else:
        if not allow_missing_context:
            raise InvalidHunkError(
                f"Expected update hunk to start with a @@ context marker, got: '{lines[0]}'",
                line_number,
            )
        change_context = None
        start_index = 0

    if start_index >= len(lines):
        raise InvalidHunkError("Update hunk does not contain any lines", line_number + 1)

    chunk = UpdateFileChunk(change_context=change_context, old_lines=[], new_lines=[], is_end_of_file=False)
    parsed_lines = 0
    for line in lines[start_index:]:
        if line == EOF_MARKER:
            if parsed_lines == 0:
                raise InvalidHunkError("Update hunk does not contain any lines", line_number + 1)
            chunk.is_end_of_file = True
            parsed_lines += 1
            break
        if line == "":
            chunk.old_lines.append("")
            chunk.new_lines.append("")
            parsed_lines += 1
            continue
        first = line[0]
        if first == " ":
            chunk.old_lines.append(line[1:])
            chunk.new_lines.append(line[1:])
        elif first == "+":
            chunk.new_lines.append(line[1:])
        elif first == "-":
            chunk.old_lines.append(line[1:])
        else:
            if parsed_lines == 0:
                raise InvalidHunkError(
                    "Unexpected line found in update hunk: "
                    f"'{line}'. Every line should start with ' ' "
                    "(context line), '+' (added line), or '-' (removed line)",
                    line_number + 1,
                )
            break
        parsed_lines += 1

    return chunk, parsed_lines + start_index


async def apply_patch(patch: str, base_dir: Path | str | None = None) -> AffectedPaths:
    hunks = parse_patch(patch)
    base_path = Path(base_dir) if base_dir is not None else None
    return await _apply_hunks_to_files(hunks, base_path)


async def _apply_hunks_to_files(hunks: list[Hunk], base_dir: Path | None) -> AffectedPaths:
    if not hunks:
        raise PatchError("No files were modified.")

    added: list[Path] = []
    modified: list[Path] = []
    deleted: list[Path] = []

    for hunk in hunks:
        if isinstance(hunk, AddFile):
            path = _resolve_path(hunk.path, base_dir)
            parent = path.parent
            if parent and str(parent) != ".":
                await AsyncPath(parent).mkdir(parents=True, exist_ok=True)
            await AsyncPath(path).write_text(hunk.contents)
            added.append(path)
        elif isinstance(hunk, DeleteFile):
            path = _resolve_path(hunk.path, base_dir)
            await AsyncPath(path).unlink()
            deleted.append(path)
        elif isinstance(hunk, UpdateFile):
            path = _resolve_path(hunk.path, base_dir)
            new_contents = await _derive_new_contents_from_chunks(path, hunk.chunks)
            if hunk.move_path:
                dest = _resolve_path(hunk.move_path, base_dir)
                parent = dest.parent
                if parent and str(parent) != ".":
                    await AsyncPath(parent).mkdir(parents=True, exist_ok=True)
                await AsyncPath(dest).write_text(new_contents)
                await AsyncPath(path).unlink()
                modified.append(dest)
            else:
                await AsyncPath(path).write_text(new_contents)
                modified.append(path)
        else:
            raise PatchError(f"Unknown hunk type: {hunk!r}")

    return AffectedPaths(added=added, modified=modified, deleted=deleted)


def _resolve_path(path: str, base_dir: Path | None) -> Path:
    candidate = Path(path)
    if base_dir is not None and not candidate.is_absolute():
        return base_dir / candidate
    return candidate


async def _derive_new_contents_from_chunks(path: Path, chunks: list[UpdateFileChunk]) -> str:
    try:
        original_contents = await AsyncPath(path).read_text()
    except OSError as err:
        raise PatchError(f"Failed to read file to update {path}") from err

    original_lines = original_contents.split("\n")
    if original_lines and original_lines[-1] == "":
        original_lines.pop()

    replacements = _compute_replacements(original_lines, path, chunks)
    new_lines = _apply_replacements(original_lines, replacements)
    if not new_lines or new_lines[-1] != "":
        new_lines.append("")
    return "\n".join(new_lines)


def _compute_replacements(
    original_lines: list[str], path: Path, chunks: list[UpdateFileChunk]
) -> list[tuple[int, int, list[str]]]:
    replacements: list[tuple[int, int, list[str]]] = []
    line_index = 0

    for chunk in chunks:
        if chunk.change_context is not None:
            idx = _seek_sequence(original_lines, [chunk.change_context], line_index, False)
            if idx is None:
                raise PatchError(f"Failed to find context '{chunk.change_context}' in {path}")
            line_index = idx + 1

        if not chunk.old_lines:
            insertion_idx = (
                len(original_lines) - 1 if original_lines and original_lines[-1] == "" else len(original_lines)
            )
            replacements.append((insertion_idx, 0, list(chunk.new_lines)))
            continue

        pattern = list(chunk.old_lines)
        new_slice = list(chunk.new_lines)
        found = _seek_sequence(original_lines, pattern, line_index, chunk.is_end_of_file)

        if found is None and pattern and pattern[-1] == "":
            pattern = pattern[:-1]
            if new_slice and new_slice[-1] == "":
                new_slice = new_slice[:-1]
            found = _seek_sequence(original_lines, pattern, line_index, chunk.is_end_of_file)

        if found is None:
            raise PatchError(f"Failed to find expected lines in {path}:\n" + "\n".join(chunk.old_lines))

        replacements.append((found, len(pattern), new_slice))
        line_index = found + len(pattern)

    replacements.sort(key=lambda item: item[0])
    return replacements


def _apply_replacements(lines: list[str], replacements: list[tuple[int, int, list[str]]]) -> list[str]:
    out = list(lines)
    for start, old_len, new_lines in reversed(replacements):
        del out[start : start + old_len]
        for offset, line in enumerate(new_lines):
            out.insert(start + offset, line)
    return out


def _seek_sequence(lines: list[str], pattern: list[str], start: int, eof: bool) -> int | None:
    if not pattern:
        return start
    if len(pattern) > len(lines):
        return None

    search_start = len(lines) - len(pattern) if eof and len(lines) >= len(pattern) else start
    last = len(lines) - len(pattern)
    for i in range(search_start, last + 1):
        if lines[i : i + len(pattern)] == pattern:
            return i
    for i in range(search_start, last + 1):
        if _matches_with(lines, pattern, i, str.rstrip):
            return i
    for i in range(search_start, last + 1):
        if _matches_with(lines, pattern, i, str.strip):
            return i
    for i in range(search_start, last + 1):
        if _matches_with(lines, pattern, i, _normalise):
            return i
    return None


def _matches_with(lines: list[str], pattern: list[str], start: int, fn) -> bool:
    if start + len(pattern) > len(lines):
        return False
    for offset, pat in enumerate(pattern):
        if fn(lines[start + offset]) != fn(pat):
            return False
    return True


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


def format_summary(affected: AffectedPaths) -> str:
    lines = ["Success. Updated the following files:"]
    lines.extend([f"A {path}" for path in affected.added])
    lines.extend([f"M {path}" for path in affected.modified])
    lines.extend([f"D {path}" for path in affected.deleted])
    return "\n".join(lines) + "\n"


def print_summary(affected: AffectedPaths) -> None:
    sys.stdout.write(format_summary(affected))


async def main() -> None:
    args = sys.argv[1:]
    if len(args) > 1:
        sys.stderr.write("Error: apply_patch accepts exactly one argument.\n")
        sys.exit(2)
    if args:
        patch_text = args[0]
        if not isinstance(patch_text, str):
            sys.stderr.write("Error: apply_patch requires a UTF-8 PATCH argument.\n")
            sys.exit(1)
    else:
        patch_text = sys.stdin.read()
        if not patch_text:
            sys.stderr.write("Usage: apply_patch 'PATCH'\n       echo 'PATCH' | apply_patch\n")
            sys.exit(2)
    try:
        affected = await apply_patch(patch_text)
        print_summary(affected)
    except InvalidPatchError as err:
        sys.stderr.write(f"Invalid patch: {err}\n")
        sys.exit(1)
    except InvalidHunkError as err:
        sys.stderr.write(f"Invalid patch hunk on line {err.line_number}: {err}\n")
        sys.exit(1)
    except PatchError as err:
        sys.stderr.write(f"{err}\n")
        sys.exit(1)


if __name__ == "__main__":
    anyio.run(main)
