"""Captured Git-tree path checks used when promoting review findings."""

from __future__ import annotations

from collections.abc import Callable, Iterable

from agentic_devtools.cli.github.ccr_review_format import ccr_path_match_key


def _source_path_exists_in_captured_trees(
    base_sha: str,
    head_sha: str,
    run_git: Callable[[Iterable[str]], str],
    source_path: str,
) -> bool | None:
    """Return exact-path presence across captured trees, or ``None`` if uncertain."""
    if ccr_path_match_key(source_path) == source_path:
        return None
    try:
        _ = source_path.encode("utf-8")
    except UnicodeEncodeError:
        return None
    unavailable = False
    pathspec = f":(literal){source_path}"
    for commit_sha in dict.fromkeys((base_sha, head_sha)):
        try:
            paths = run_git(["ls-tree", "-r", "--full-tree", "-z", "--name-only", commit_sha, "--", pathspec])
        except OSError, RuntimeError:
            unavailable = True
            continue
        if source_path in paths.split("\0"):
            return True
    return None if unavailable else False
