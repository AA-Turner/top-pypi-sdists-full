"""Diff-anchor selection for recovered CCR findings using captured diff and tree state."""

from __future__ import annotations

import ast
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from agentic_devtools.cli.ci.review_thread_tree_paths import _source_path_exists_in_captured_trees
from agentic_devtools.cli.github.ccr_review_format import ccr_path_match_key


@dataclass(frozen=True)
class ReviewThreadAnchor:
    """A validated changed-line position suitable for a GitHub inline comment."""

    path: str
    line: int
    side: str = "RIGHT"


@dataclass(frozen=True)
class AnchorSelection:
    """Selected diff anchor, fallback status, and source-filename match."""

    anchor: ReviewThreadAnchor
    used_fallback: bool
    matched_source_path: bool = False


@dataclass
class _DiffAnchorCollection:
    changed_lines: list[ReviewThreadAnchor]
    hunk_lines: list[ReviewThreadAnchor]
    diff_paths: set[str]
    ambiguous_paths: set[str]
    current_path: str = ""
    original_path: str = ""
    old_line: int | None = None
    new_line: int | None = None
    in_hunk: bool = False


def _decode_git_path(path: str) -> str | None:
    if not path.startswith('"'):
        return path
    try:
        encoded_path = "".join(
            "".join(f"\\x{byte:02x}" for byte in character.encode("utf-8")) if ord(character) > 127 else character
            for character in path
        )
        return ast.literal_eval(f"b{encoded_path}").decode("utf-8")
    except SyntaxError, ValueError, UnicodeDecodeError:
        return None


def _record_git_header_paths(diff_header: str, collection: _DiffAnchorCollection) -> None:
    if diff_header.startswith("a/") and '"' not in diff_header and diff_header.count(" b/") > 1:
        for separator in re.finditer(r" b/", diff_header):
            collection.ambiguous_paths.add(diff_header[: separator.start()].removeprefix("a/"))
            collection.ambiguous_paths.add(diff_header[separator.end() :])
        return
    match = re.match(r'^("(?:\\.|[^"])*"|a/[^"]*) ("(?:\\.|[^"])*"|b/[^"]*)$', diff_header)
    if match is None:
        return
    for path in match.groups():
        decoded = _decode_git_path(path)
        if decoded is not None:
            prefix = "a/" if decoded.startswith("a/") else "b/"
            collection.diff_paths.add(decoded.removeprefix(prefix))


def _record_file_marker(line: str, *, prefix: str, side: str, collection: _DiffAnchorCollection) -> None:
    path = _decode_git_path(line[len(prefix) :])
    if path is None:
        if side == "LEFT":
            collection.original_path = ""
        else:
            collection.current_path = ""
        return
    path = path.removeprefix("a/" if side == "LEFT" else "b/")
    if path == "/dev/null":
        path = ""
    elif path:
        collection.diff_paths.add(path)
    if side == "LEFT":
        collection.original_path = path
    else:
        collection.current_path = path


def _record_hunk_line(line: str, collection: _DiffAnchorCollection) -> None:
    old_line = collection.old_line
    new_line = collection.new_line
    if old_line is None or new_line is None or not line:
        return
    if line.startswith("+"):
        if collection.current_path:
            anchor = ReviewThreadAnchor(collection.current_path, new_line)
            collection.changed_lines.append(anchor)
            collection.hunk_lines.append(anchor)
        collection.new_line = new_line + 1
    elif line.startswith(" "):
        context_path = collection.current_path or collection.original_path
        if context_path:
            line_number = new_line if collection.current_path else old_line
            side = "RIGHT" if collection.current_path else "LEFT"
            collection.hunk_lines.append(ReviewThreadAnchor(context_path, line_number, side=side))
        collection.old_line = old_line + 1
        collection.new_line = new_line + 1
    elif line.startswith("-"):
        if collection.original_path:
            anchor = ReviewThreadAnchor(collection.original_path, old_line, side="LEFT")
            collection.changed_lines.append(anchor)
            collection.hunk_lines.append(anchor)
        collection.old_line = old_line + 1


def _collect_diff_anchors(diff: str) -> _DiffAnchorCollection:
    collection = _DiffAnchorCollection([], [], set(), set())
    hunk_re = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            collection.current_path = ""
            collection.original_path = ""
            collection.old_line = None
            collection.new_line = None
            collection.in_hunk = False
            _record_git_header_paths(line.removeprefix("diff --git "), collection)
            continue
        if not collection.in_hunk and line.startswith("--- "):
            _record_file_marker(line, prefix="--- ", side="LEFT", collection=collection)
            continue
        if not collection.in_hunk and line.startswith("+++ "):
            _record_file_marker(line, prefix="+++ ", side="RIGHT", collection=collection)
            continue
        hunk = hunk_re.match(line)
        if hunk:
            collection.old_line = int(hunk.group(1))
            collection.new_line = int(hunk.group(2))
            collection.in_hunk = True
            continue
        _record_hunk_line(line, collection)
    return collection


def _source_path_matches(
    hunk_lines: list[ReviewThreadAnchor],
    source_path: str,
    diff_paths: set[str],
    ambiguous_paths: set[str],
    source_path_exists_in_captured_trees: bool | None,
) -> list[ReviewThreadAnchor]:
    matches = [anchor for anchor in hunk_lines if anchor.path == source_path]
    normalized = ccr_path_match_key(source_path)
    if (
        not matches
        and source_path not in ambiguous_paths
        and source_path not in diff_paths
        and normalized != source_path
        and source_path_exists_in_captured_trees is False
    ):
        matches = [anchor for anchor in hunk_lines if anchor.path == normalized]
    return matches


def _exact_source_anchor(
    matches: list[ReviewThreadAnchor],
    source_line: int | None,
) -> ReviewThreadAnchor | None:
    if source_line is None:
        return None
    return next(
        (anchor for anchor in matches if anchor.line == source_line and anchor.side == "RIGHT"),
        next((anchor for anchor in matches if anchor.line == source_line), None),
    )


def _same_file_fallback(
    changed_lines: list[ReviewThreadAnchor],
    source_matches: list[ReviewThreadAnchor],
    source_path: str,
    source_line: int | None,
) -> AnchorSelection | None:
    same_file = [anchor for anchor in changed_lines if anchor.path == source_path]
    if not same_file and source_matches:
        same_file = [anchor for anchor in changed_lines if anchor.path == source_matches[0].path]
    if not same_file:
        return None
    if source_line is not None:
        nearest = min(
            same_file,
            key=lambda anchor: (abs(anchor.line - source_line), anchor.side != "RIGHT"),
        )
        return AnchorSelection(nearest, used_fallback=True, matched_source_path=True)
    first_right = next((anchor for anchor in same_file if anchor.side == "RIGHT"), None)
    return AnchorSelection(first_right or same_file[0], used_fallback=True, matched_source_path=True)


def _suggested_or_first_anchor(
    changed_lines: list[ReviewThreadAnchor],
    suggested_path: str,
    suggested_line: int | None,
) -> AnchorSelection:
    if suggested_line is not None:
        suggested = next(
            (
                anchor
                for anchor in changed_lines
                if anchor.path == suggested_path and anchor.line == suggested_line and anchor.side == "RIGHT"
            ),
            None,
        )
        if suggested is None:
            suggested = next(
                (anchor for anchor in changed_lines if anchor.path == suggested_path and anchor.line == suggested_line),
                None,
            )
        if suggested is not None:
            return AnchorSelection(suggested, used_fallback=True)
    return AnchorSelection(changed_lines[0], used_fallback=True)


def select_review_anchor(
    diff: str,
    *,
    source_path: str,
    source_line: int | None,
    suggested_path: str = "",
    suggested_line: int | None = None,
    source_path_exists_in_captured_trees: bool | None = None,
    captured_tree_context: tuple[str, str, Callable[[Iterable[str]], str]] | None = None,
) -> AnchorSelection | None:
    """Choose a changed-line anchor present in the captured unified diff."""
    parsed = _collect_diff_anchors(diff)
    if not parsed.changed_lines:
        return None

    if source_path_exists_in_captured_trees is None and captured_tree_context is not None:
        source_path_exists_in_captured_trees = _source_path_exists_in_captured_trees(
            *captured_tree_context,
            source_path,
        )
    source_path_matches = _source_path_matches(
        parsed.hunk_lines,
        source_path,
        parsed.diff_paths,
        parsed.ambiguous_paths,
        source_path_exists_in_captured_trees,
    )
    source = _exact_source_anchor(source_path_matches, source_line)
    if source is not None:
        return AnchorSelection(source, used_fallback=False, matched_source_path=True)

    fallback = _same_file_fallback(
        parsed.changed_lines,
        source_path_matches,
        source_path,
        source_line,
    )
    if fallback is not None:
        return fallback
    return _suggested_or_first_anchor(parsed.changed_lines, suggested_path, suggested_line)
