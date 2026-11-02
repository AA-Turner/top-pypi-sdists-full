"""Parse and validate exact text diffs for pipeline preservation checks."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping, Sequence
from typing import Literal, NamedTuple

_HUNK_PATTERN = re.compile(r"^@@ -\d+(?:,(\d+))? \+\d+(?:,(\d+))? @@(?: .*)?$")
_PATH_ESCAPES = {"a": 7, "b": 8, "t": 9, "n": 10, "v": 11, "f": 12, "r": 13, '"': 34, "\\": 92}
_EMPTY_BLOB_HASHES = (hashlib.sha1(b"blob 0\0").hexdigest(), hashlib.sha256(b"blob 0\0").hexdigest())


class _PathConstraint(NamedTuple):
    kind: Literal["old", "new", "file_mode", "invalid"]
    path: str = ""


class _HunkLineState(NamedTuple):
    old_remaining: int
    new_remaining: int
    changed_line_count: int
    previous_content: bool


class _HunkResult(NamedTuple):
    next_index: int
    changed_line_count: int


class _PatchMetadataState(NamedTuple):
    rename_from: str
    rename_to: str
    similarity_index: str


class _PatchMetadata(NamedTuple):
    hunk_count: int
    changed_line_count: int
    rename_from: str
    rename_to: str
    similarity_index: str


class _IndexHashes(NamedTuple):
    old_hash: str
    new_hash: str


class _PatchPaths(NamedTuple):
    old: str | None
    new: str | None
    file_mode: bool


def _quoted_path_end(header: str, position: int) -> int | None:
    end = position + 1
    while end < len(header):
        if header[end] == "\\":
            end += 2
        elif header[end] == '"':
            return end
        else:
            end += 1
    return None


def _decode_quoted_path(header: str, position: int, end: int) -> str | None:
    encoded = bytearray()
    index = position + 1
    while index < end:
        char = header[index]
        if char != "\\":
            encoded.extend(char.encode("utf-8"))
            index += 1
            continue
        index += 1
        if header[index] in "01234567":
            octal_end = index + 1
            while octal_end < min(index + 3, end) and header[octal_end] in "01234567":
                octal_end += 1
            encoded.append(int(header[index:octal_end], 8))
            index = octal_end
            continue
        escaped = _PATH_ESCAPES.get(header[index])
        if escaped is None:
            return None
        encoded.append(escaped)
        index += 1
    try:
        return encoded.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _read_path(header: str, position: int) -> tuple[str, int] | None:
    if position >= len(header):
        return None
    if header[position] != '"':
        return header[position:], len(header)
    end = _quoted_path_end(header, position)
    if end is None:
        return None
    path = _decode_quoted_path(header, position, end)
    return (path, end + 1) if path is not None else None


def _patch_path(line: str, prefix: str, git_prefix: str) -> str | None:
    header = line.removeprefix(prefix)
    if header.startswith('"'):
        path_result = _read_path(line, len(prefix))
        if path_result is None or path_result[1] != len(line):
            return None
        path = path_result[0]
    else:
        path = header.split("\t", maxsplit=1)[0]
    if path == "/dev/null" or path.startswith(git_prefix):
        return path.removeprefix(git_prefix)
    return None


def _git_header_pairs(header: str) -> list[tuple[str, str]] | None:
    pairs: list[tuple[str, str]] = []
    if header.startswith('"'):
        old_path_result = _read_path(header, 0)
        if old_path_result is None:
            return None
        old_path, position = old_path_result
        if position >= len(header) or header[position] != " ":
            return None
        new_path_result = _read_path(header, position + 1)
        if new_path_result is None or new_path_result[1] != len(header):
            return None
        return [(old_path, new_path_result[0])]
    for separator in range(len(header)):
        if not (header.startswith(" b/", separator) or header.startswith(' "b/', separator)):
            continue
        old_path = header[:separator]
        new_path_result = _read_path(header, separator + 1)
        if new_path_result is not None and new_path_result[1] == len(header):
            pairs.append((old_path, new_path_result[0]))
    return pairs


def _patch_path_constraint(line: str) -> _PathConstraint | None:
    if line.startswith(("--- ", "+++ ")):
        is_old_path = line.startswith("--- ")
        prefix, git_prefix = ("--- ", "a/") if is_old_path else ("+++ ", "b/")
        kind: Literal["old", "new"] = "old" if is_old_path else "new"
        path = _patch_path(line, prefix, git_prefix)
        return _PathConstraint(kind, path) if path is not None else _PathConstraint("invalid")
    if line.startswith(("rename from ", "rename to ")):
        rename = _rename_path(line)
        if rename is None:
            return _PathConstraint("invalid")
        prefix, path = rename
        return _PathConstraint("old" if prefix == "rename from " else "new", path)
    if line.startswith(("new file mode ", "deleted file mode ")):
        return _PathConstraint("file_mode")
    return None


def _patch_path_constraints(diff_lines: list[str], line_number: int) -> _PatchPaths | None:
    old_path = None
    new_path = None
    has_file_mode_metadata = False
    for line in diff_lines[line_number + 1 :]:
        if line.startswith("diff --git ") or line.startswith("@@ "):
            break
        constraint = _patch_path_constraint(line)
        if constraint is None:
            continue
        if constraint.kind == "old":
            old_path = constraint.path
        elif constraint.kind == "new":
            new_path = constraint.path
        elif constraint.kind == "file_mode":
            has_file_mode_metadata = True
        else:
            return None
    return _PatchPaths(old_path, new_path, has_file_mode_metadata)


def _matching_path_pair(
    header: str,
    diff_lines: list[str],
    line_number: int,
    expected_inventory: set[str],
) -> tuple[str, str] | None:
    path_pairs = _git_header_pairs(header)
    if path_pairs is None:
        return None
    matches = [
        (old_path, new_path)
        for old_path, new_path in path_pairs
        if old_path.startswith("a/")
        and old_path[2:]
        and new_path.startswith("b/")
        and new_path[2:] in expected_inventory
    ]
    if len(matches) > 1:
        constraints = _patch_path_constraints(diff_lines, line_number)
        if constraints is None:
            return None
        if constraints.old is not None or constraints.new is not None:
            matches = [
                (old_path, new_path)
                for old_path, new_path in matches
                if (constraints.old in (None, "/dev/null") or old_path[2:] == constraints.old)
                and (constraints.new in (None, "/dev/null") or new_path[2:] == constraints.new)
            ]
        elif constraints.file_mode:
            matches = [(old_path, new_path) for old_path, new_path in matches if old_path[2:] == new_path[2:]]
    if len(matches) != 1 or not matches[0][1][2:]:
        return None
    return matches[0]


def _collect_file_patches(
    diff_lines: list[str], expected_inventory: set[str]
) -> list[tuple[str, str, list[str]]] | None:
    file_patches: list[tuple[str, str, list[str]]] = []
    current_old_path = ""
    current_new_path = ""
    current_lines: list[str] = []
    for line_number, line in enumerate(diff_lines):
        if line.startswith("diff --git "):
            if current_old_path:
                file_patches.append((current_old_path, current_new_path, current_lines))
            pair = _matching_path_pair(line.removeprefix("diff --git "), diff_lines, line_number, expected_inventory)
            if pair is None:
                return None
            current_old_path, current_new_path = pair[0][2:], pair[1][2:]
            current_lines = []
        elif not current_old_path:
            return None
        else:
            current_lines.append(line)
    file_patches.append((current_old_path, current_new_path, current_lines))
    return file_patches


def _consume_hunk_line(
    line: str,
    old_remaining: int,
    new_remaining: int,
    changed_line_count: int,
    previous_content: bool,
) -> _HunkLineState | None:
    if line == r"\ No newline at end of file":
        if not previous_content:
            return None
    elif line.startswith(" "):
        old_remaining -= 1
        new_remaining -= 1
        previous_content = True
    elif line.startswith("-"):
        old_remaining -= 1
        changed_line_count += 1
        previous_content = True
    elif line.startswith("+"):
        new_remaining -= 1
        changed_line_count += 1
        previous_content = True
    else:
        return None
    if old_remaining < 0 or new_remaining < 0:
        return None
    return _HunkLineState(old_remaining, new_remaining, changed_line_count, previous_content)


def _consume_hunk(patch_lines: list[str], index: int) -> _HunkResult | None:
    match = _HUNK_PATTERN.fullmatch(patch_lines[index])
    if match is None:
        return None
    old_remaining = int(match.group(1) or "1")
    new_remaining = int(match.group(2) or "1")
    if old_remaining + new_remaining == 0:
        return None
    index += 1
    changed_line_count = 0
    previous_content = False
    while old_remaining or new_remaining:
        if index >= len(patch_lines):
            return None
        state = _consume_hunk_line(
            patch_lines[index],
            old_remaining,
            new_remaining,
            changed_line_count,
            previous_content,
        )
        if state is None:
            return None
        old_remaining = state.old_remaining
        new_remaining = state.new_remaining
        changed_line_count = state.changed_line_count
        previous_content = state.previous_content
        index += 1
    while index < len(patch_lines) and patch_lines[index] == r"\ No newline at end of file":
        index += 1
    if index < len(patch_lines) and not patch_lines[index].startswith("@@ "):
        return None
    return _HunkResult(index, changed_line_count)


def _rename_path(line: str) -> tuple[str, str] | None:
    prefix = "rename from " if line.startswith("rename from ") else "rename to "
    path_result = _read_path(line, len(prefix))
    if path_result is None or path_result[1] != len(line):
        return None
    return prefix, path_result[0]


def _is_supported_patch_metadata(line: str) -> bool:
    return line.startswith(
        (
            "index ",
            "--- ",
            "+++ ",
            "new file mode ",
            "deleted file mode ",
            "old mode ",
            "new mode ",
            "similarity index ",
            "dissimilarity index ",
            "rename from ",
            "rename to ",
            "copy from ",
            "copy to ",
        )
    )


def _consume_patch_metadata(
    line: str,
    rename_from: str,
    rename_to: str,
    similarity_index: str,
) -> _PatchMetadataState | None:
    if line.startswith(("Binary files ", "GIT binary patch")):
        return None
    if line.startswith(("rename from ", "rename to ")):
        rename = _rename_path(line)
        if rename is None:
            return None
        prefix, path = rename
        if prefix == "rename from ":
            return None if rename_from else _PatchMetadataState(path, rename_to, similarity_index)
        return None if rename_to else _PatchMetadataState(rename_from, path, similarity_index)
    if line.startswith("similarity index "):
        if similarity_index:
            return None
        similarity_index = line
    if not _is_supported_patch_metadata(line):
        return None
    return _PatchMetadataState(rename_from, rename_to, similarity_index)


def _read_patch_metadata(patch_lines: list[str]) -> _PatchMetadata | None:
    index = 0
    hunk_count = 0
    changed_line_count = 0
    rename_from = ""
    rename_to = ""
    similarity_index = ""
    while index < len(patch_lines):
        if patch_lines[index].startswith("@@ "):
            hunk = _consume_hunk(patch_lines, index)
            if hunk is None:
                return None
            index = hunk.next_index
            hunk_count += 1
            changed_line_count += hunk.changed_line_count
            continue
        state = _consume_patch_metadata(patch_lines[index], rename_from, rename_to, similarity_index)
        if state is None:
            return None
        rename_from = state.rename_from
        rename_to = state.rename_to
        similarity_index = state.similarity_index
        index += 1
    if bool(rename_from) != bool(rename_to):
        return None
    return _PatchMetadata(hunk_count, changed_line_count, rename_from, rename_to, similarity_index)


def _parse_index_hashes(patch_line: str) -> _IndexHashes | None:
    match = re.fullmatch(r"index ([0-9a-f]{7,64})\.\.([0-9a-f]{7,64})", patch_line)
    return _IndexHashes(*match.groups()) if match is not None and len(match.group(1)) == len(match.group(2)) else None


def _valid_empty_rename(patch_lines: list[str], similarity_index: str) -> bool:
    has_mode_change = len(patch_lines) == 5
    if has_mode_change and (
        re.fullmatch(r"old mode 100(?:644|755)", patch_lines[0]) is None
        or re.fullmatch(r"new mode 100(?:644|755)", patch_lines[1]) is None
        or patch_lines[0].removeprefix("old mode ") == patch_lines[1].removeprefix("new mode ")
    ):
        return False
    rename_metadata = patch_lines[2:] if has_mode_change else patch_lines
    return bool(
        similarity_index == "similarity index 100%"
        and len(rename_metadata) == 3
        and rename_metadata[0] == similarity_index
        and rename_metadata[1].startswith("rename from ")
        and rename_metadata[2].startswith("rename to ")
    )


def _valid_empty_file_addition(new_path: str, patch_lines: list[str]) -> bool:
    if (
        len(patch_lines) not in {2, 4}
        or re.fullmatch(r"new file mode 100(?:644|755)", patch_lines[0]) is None
        or (len(patch_lines) == 4 and (patch_lines[2] != "--- /dev/null" or patch_lines[3] != f"+++ b/{new_path}"))
    ):
        return False
    hashes = _parse_index_hashes(patch_lines[1])
    return (
        hashes is not None
        and hashes.old_hash == "0" * len(hashes.old_hash)
        and any(empty_hash.startswith(hashes.new_hash) for empty_hash in _EMPTY_BLOB_HASHES)
    )


def _valid_empty_file_deletion(patch_lines: list[str]) -> bool:
    if len(patch_lines) != 2 or re.fullmatch(r"deleted file mode 100(?:644|755)", patch_lines[0]) is None:
        return False
    hashes = _parse_index_hashes(patch_lines[1])
    return (
        hashes is not None
        and any(empty_hash.startswith(hashes.old_hash) for empty_hash in _EMPTY_BLOB_HASHES)
        and hashes.new_hash == "0" * len(hashes.new_hash)
    )


def _valid_empty_patch(
    new_path: str,
    patch_lines: list[str],
    rename_from: str,
    similarity_index: str,
) -> bool:
    if rename_from:
        return _valid_empty_rename(patch_lines, similarity_index)
    if patch_lines and patch_lines[0].startswith("new file mode "):
        return _valid_empty_file_addition(new_path, patch_lines)
    if patch_lines and patch_lines[0].startswith("deleted file mode "):
        return _valid_empty_file_deletion(patch_lines)
    return False


def _valid_file_patch(
    old_path: str,
    new_path: str,
    patch_lines: list[str],
    expected_change_count: int,
) -> bool:
    if not patch_lines:
        return False
    metadata = _read_patch_metadata(patch_lines)
    if metadata is None:
        return False
    if metadata.rename_from and (metadata.rename_from != old_path or metadata.rename_to != new_path):
        return False
    if metadata.hunk_count == 0 and not _valid_empty_patch(
        new_path, patch_lines, metadata.rename_from, metadata.similarity_index
    ):
        return False
    return expected_change_count == metadata.changed_line_count


def validated_exact_diff_fingerprint(
    exact_diff: str,
    expected_files: Sequence[str],
    expected_change_counts: Mapping[str, int],
) -> str:
    """Return a content hash only for a complete, text-only patch matching its file inventory."""
    if not exact_diff or not exact_diff.endswith("\n") or not expected_files:
        return ""
    expected_inventory = set(expected_files)
    if (
        len(expected_inventory) != len(expected_files)
        or not isinstance(expected_change_counts, Mapping)
        or set(expected_change_counts) != expected_inventory
        or any(type(changes) is not int or changes < 0 for changes in expected_change_counts.values())
    ):
        return ""
    file_patches = _collect_file_patches(exact_diff.split("\n")[:-1], expected_inventory)
    if file_patches is None:
        return ""
    inventory = [new_path for _, new_path, _ in file_patches]
    if len(inventory) != len(expected_inventory) or set(inventory) != expected_inventory:
        return ""
    if not all(
        _valid_file_patch(old_path, new_path, patch_lines, expected_change_counts[new_path])
        for old_path, new_path, patch_lines in file_patches
    ):
        return ""
    return f"exact-diff-sha256:{hashlib.sha256(exact_diff.encode('utf-8')).hexdigest()}"
