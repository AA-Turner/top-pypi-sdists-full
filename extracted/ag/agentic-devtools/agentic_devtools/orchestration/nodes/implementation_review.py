"""Implementation review node: self-review generated code for quality.

Scans generated code for debug statements (breakpoint, pdb, debug prints)
and TODO/FIXME/HACK/XXX markers. Routes back to implementation
if issues are found.
"""

from __future__ import annotations

import re
from typing import Any

from agentic_devtools.orchestration.nodes._helpers import resolve_repo_root, utc_now
from agentic_devtools.orchestration.state_schema import WorkOnIssueState

# Patterns that indicate leftover debug code
_DEBUG_PATTERNS = [
    re.compile(r"\bbreakpoint\(\)"),
    re.compile(r"\bpdb\.set_trace\(\)"),
    re.compile(r"\bprint\(.*(debug|DEBUG)"),
    re.compile(r"\bimport pdb\b"),
    re.compile(r"\bimport ipdb\b"),
]

_TODO_PATTERN = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b", re.IGNORECASE)


def implementation_review_node(state: WorkOnIssueState) -> dict[str, Any]:
    """Review generated code for quality issues.

    Checks for debug statements, TODO/FIXME markers, and other
    quality concerns. Sets error to route back to implementation
    if issues are found.
    """
    raw_paths = state.get("affected_paths", [])
    affected_paths: list[str] = (
        [str(p) for p in raw_paths if not isinstance(p, bool)] if isinstance(raw_paths, list) else []
    )
    issues: list[str] = []

    repo_root = resolve_repo_root(state)

    # Guard: when setup_result checkpoints an explicit worktree path that is now
    # gone or invalid, resolve_repo_root returns None. Silently skipping the review
    # and advancing to verification would hide the stale worktree. Return a blocking
    # error so the caller can trigger a fresh setup instead.
    # Dry runs record a simulated path that never exists on disk, so skip this guard
    # and fall through to the repo_root is None clean-skip path below.
    _is_dry_run = bool(state.get("dry_run")) if isinstance(state, dict) else False
    _setup = state.get("setup_result") if isinstance(state, dict) else None
    if not _is_dry_run and repo_root is None and _setup is not None and getattr(_setup, "worktree_path", None):
        _wt_path = _setup.worktree_path
        error_msg = f"Setup worktree '{_wt_path}' is no longer accessible; implementation review aborted"
        return {
            "step": "implementation_review",
            "error": error_msg,
            "verification_ready": False,
            "events": [
                {
                    "event": "implementation_review_blocked",
                    "timestamp": utc_now(),
                    "signals": {"verification_ready": False, "reason": "worktree_unavailable"},
                }
            ],
        }

    if repo_root is None:
        return {
            "step": "implementation_review",
            "error": None,
            "verification_ready": True,
            "events": [
                {
                    "event": "implementation_review_completed",
                    "timestamp": utc_now(),
                    "signals": {"verification_ready": True, "skipped": "no_repo_root"},
                }
            ],
        }

    # Scan each affected file
    for path_str in affected_paths:
        # Resolve the joined path and verify it stays inside the repository.
        # A corrupted path containing ".." segments would otherwise escape
        # repo_root and could expose arbitrary files outside the repository.
        # Path.resolve() uses strict=False by default so it never raises OSError;
        # relative_to() raises ValueError when the path escapes repo_root.
        try:
            file_path = (repo_root / path_str).resolve()
            file_path.relative_to(repo_root)
        except ValueError:
            continue
        if not file_path.exists() or not file_path.is_file():
            continue
        if not path_str.endswith(".py"):
            continue

        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        file_issues = _scan_file(path_str, content)
        issues.extend(file_issues)

    if issues:
        error_msg = "Implementation review found issues:\n" + "\n".join(f"- {i}" for i in issues)
        return {
            "step": "implementation_review",
            "error": error_msg,
            "verification_ready": False,
            "events": [
                {
                    "event": "implementation_review_issues_found",
                    "timestamp": utc_now(),
                    "signals": {"issue_count": len(issues)},
                }
            ],
        }

    return {
        "step": "implementation_review",
        "error": None,
        "verification_ready": True,
        "events": [
            {
                "event": "implementation_review_completed",
                "timestamp": utc_now(),
                "signals": {"verification_ready": True},
            }
        ],
    }


def _scan_file(path: str, content: str) -> list[str]:
    """Scan a single file for quality issues."""
    issues: list[str] = []

    for line_num, line in enumerate(content.splitlines(), 1):
        for pattern in _DEBUG_PATTERNS:
            if pattern.search(line):
                issues.append(f"{path}:{line_num}: Debug statement found: {line.strip()}")

        if _TODO_PATTERN.search(line):
            issues.append(f"{path}:{line_num}: TODO/FIXME marker: {line.strip()}")

    return issues
