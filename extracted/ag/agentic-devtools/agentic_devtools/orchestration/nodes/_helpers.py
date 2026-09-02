"""Shared helper utilities for work-on-issue node implementations.

Provides issue key parsing, provider detection, LLM call wrappers,
and repository context discovery helpers.
"""

from __future__ import annotations

import logging
import re
import subprocess
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def utc_now() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Issue key parsing and provider detection
# ---------------------------------------------------------------------------

_JIRA_KEY_PATTERN = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")


def detect_issue_provider(issue_key: str) -> str:
    """Detect whether an issue key is Jira or GitHub format.

    Args:
        issue_key: The issue key to classify.

    Returns:
        ``"jira"`` for PROJECT-NNN format, ``"github"`` for numeric or #N format.
    """
    cleaned_issue_key = issue_key.strip()
    if not cleaned_issue_key:
        return "github"
    # Strip leading # for GitHub issues
    normalized = cleaned_issue_key.lstrip("#")
    if normalized.isdigit():
        return "github"
    jira_candidate = cleaned_issue_key.upper()
    if _JIRA_KEY_PATTERN.match(jira_candidate):
        return "jira"
    return "github"


def normalize_issue_key(issue_key: str) -> str:
    """Normalize an issue key for consistent usage.

    Strips leading ``#`` characters from GitHub issue numbers.

    Args:
        issue_key: Raw issue key input.

    Returns:
        Normalized issue key string.
    """
    cleaned_issue_key = issue_key.strip()
    if cleaned_issue_key.startswith("#"):
        return cleaned_issue_key.lstrip("#")
    return cleaned_issue_key


def normalize_github_issue_number(issue_key: str) -> str:
    """Normalize and validate a GitHub issue number.

    Removes a leading ``#`` (if present) and requires the remaining value to be
    a positive ASCII integer.

    Args:
        issue_key: Raw GitHub issue identifier.

    Returns:
        Normalized issue number string, or ``""`` when invalid.
    """
    normalized = normalize_issue_key(issue_key)
    if not normalized or not normalized.isascii() or not normalized.isdigit():
        return ""
    if not any(c != "0" for c in normalized):
        return ""
    return normalized


# ---------------------------------------------------------------------------
# Subprocess helpers
# ---------------------------------------------------------------------------


def run_command(
    args: list[str],
    *,
    capture_output: bool = True,
    timeout: int = 300,
    cwd: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a subprocess command with standard error handling.

    Args:
        args: Command and arguments to run.
        capture_output: Whether to capture stdout/stderr.
        timeout: Timeout in seconds.
        cwd: Working directory for the command.

    Returns:
        CompletedProcess with return code and output.
    """

    def _to_text(value: bytes | str | None) -> str:
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        if isinstance(value, str):
            return value
        return ""

    try:
        return subprocess.run(
            args,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            cwd=cwd,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        partial_stdout = _to_text(exc.stdout if exc.stdout is not None else exc.output)
        partial_stderr = _to_text(exc.stderr) if exc.stderr is not None else ""
        timeout_msg = f"Command timed out after {timeout}s: {' '.join(args)}"
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=partial_stdout,
            stderr=f"{timeout_msg}\n{partial_stderr}".rstrip(),
        )
    except FileNotFoundError:
        return subprocess.CompletedProcess(
            args=args,
            returncode=127,
            stdout="",
            stderr=f"Command not found: {args[0] if args else '<empty command>'}",
        )


def _explicit_worktree_path(state: Mapping[str, Any] | None) -> str | None:
    """Return an explicit setup worktree path string from state, when present."""
    if not isinstance(state, dict):
        return None
    setup_result = state.get("setup_result")
    worktree_path = getattr(setup_result, "worktree_path", None)
    if isinstance(worktree_path, str) and worktree_path.strip():
        return worktree_path.strip()
    return None


def _validated_worktree_path(explicit_path: str, *, expected_branch: str | None = None) -> Path | None:
    """Validate explicit worktree path existence, Git root identity, and current branch.

    Returns ``None`` when the path does not exist, is not a directory, or any
    of the following checks fail:

    - ``git rev-parse --show-toplevel`` in that ``cwd`` does not resolve to
      the same directory, or
    - ``git rev-parse --git-common-dir`` does not match the current process
      checkout's common directory, or
    - ``expected_branch`` is provided and ``git symbolic-ref HEAD`` does not
      resolve to that branch (i.e. the worktree has been switched since setup).
    """
    candidate = Path(explicit_path).resolve()
    if not candidate.exists() or not candidate.is_dir():
        return None
    result = run_command(["git", "rev-parse", "--show-toplevel"], cwd=str(candidate))
    if result.returncode != 0:
        return None
    git_root = result.stdout.strip()
    if not git_root:
        return None
    if Path(git_root).resolve() != candidate:
        return None
    candidate_common = run_command(["git", "rev-parse", "--git-common-dir"], cwd=str(candidate))
    if candidate_common.returncode != 0:
        return None
    candidate_common_path = _resolve_git_common_dir(candidate_common.stdout, candidate)
    if candidate_common_path is None:
        return None
    process_common_path = _resolve_process_git_common_dir()
    if process_common_path is None:
        return None
    if candidate_common_path != process_common_path:
        return None
    if expected_branch is not None:
        symbolic_ref = run_command(["git", "symbolic-ref", "HEAD"], cwd=str(candidate))
        if symbolic_ref.returncode != 0:
            return None
        current_branch = symbolic_ref.stdout.strip().removeprefix("refs/heads/")
        if current_branch != expected_branch:
            return None
    return candidate


def _resolve_git_common_dir(raw_common_dir: str, cwd: Path) -> Path | None:
    """Resolve ``git rev-parse --git-common-dir`` output to an absolute path."""
    cleaned_common_dir = raw_common_dir.strip()
    if not cleaned_common_dir:
        return None
    common_dir = Path(cleaned_common_dir)
    if not common_dir.is_absolute():
        common_dir = (cwd / common_dir).resolve()
    else:
        common_dir = common_dir.resolve()
    return common_dir


def _resolve_process_git_common_dir() -> Path | None:
    """Resolve the process checkout's git common dir from the process cwd."""
    process_cwd = Path.cwd().resolve()
    result = run_command(["git", "rev-parse", "--git-common-dir"], cwd=str(process_cwd))
    if result.returncode != 0:
        return None
    return _resolve_git_common_dir(result.stdout, process_cwd)


def get_worktree_path(state: Mapping[str, Any] | None) -> Path | None:
    """Return a validated setup worktree path from graph state, when present.

    Validates that the worktree belongs to the same repository and is still
    checked out on ``setup_result.branch_name``.  Returns ``None`` when the
    path is missing, the repository identity does not match, or the current
    branch has been switched since the setup checkpoint was recorded.
    """
    explicit_path = _explicit_worktree_path(state)
    if explicit_path is None:
        return None
    # _explicit_worktree_path returning non-None guarantees state is a dict
    state_dict: dict[str, Any] = state  # type: ignore[assignment]
    setup_result = state_dict.get("setup_result")
    branch = getattr(setup_result, "branch_name", None)
    expected_branch: str | None = branch.strip() if isinstance(branch, str) and branch.strip() else None
    return _validated_worktree_path(explicit_path, expected_branch=expected_branch)


def resolve_repo_root(state: Mapping[str, Any] | None = None) -> Path | None:
    """Resolve repo root from setup worktree when explicit; no fallback on invalid explicit path."""
    explicit_path = _explicit_worktree_path(state)
    if explicit_path is not None:
        return get_worktree_path(state)

    result = run_command(["git", "rev-parse", "--show-toplevel"])
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve()


# ---------------------------------------------------------------------------
# Repository context discovery (FR-010)
# ---------------------------------------------------------------------------


def scan_directory_structure(
    root: Path,
    *,
    max_depth: int = 3,
    exclude_patterns: tuple[str, ...] = (
        "__pycache__",
        ".git",
        "node_modules",
        ".venv",
        "venv",
        ".agdt",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
    ),
) -> list[str]:
    """Scan directory structure for repository context.

    Args:
        root: Root directory to scan.
        max_depth: Maximum directory depth to traverse.
        exclude_patterns: Directory names to exclude.

    Returns:
        List of relative file paths found.
    """
    if max_depth <= 0:
        return []

    paths: list[str] = []
    _scan_recursive(root, root, 0, max_depth, exclude_patterns, paths)
    return sorted(paths)


def _scan_recursive(
    root: Path,
    current: Path,
    depth: int,
    max_depth: int,
    exclude_patterns: tuple[str, ...],
    results: list[str],
) -> None:
    """Recursively scan directory tree."""
    if depth >= max_depth:
        return
    try:
        entries = sorted(current.iterdir())
    except (PermissionError, FileNotFoundError):
        return
    for entry in entries:
        if entry.name in exclude_patterns:
            continue
        relative = str(entry.relative_to(root))
        if entry.is_file():
            results.append(relative)
        elif entry.is_dir():
            results.append(relative + "/")
            _scan_recursive(root, entry, depth + 1, max_depth, exclude_patterns, results)


def detect_test_conventions(root: Path) -> dict[str, Any]:
    """Detect testing conventions in the repository.

    Checks for 1:1:1 test layout (tests/unit/) and common test patterns.

    Args:
        root: Repository root path.

    Returns:
        Dictionary describing detected test conventions.
    """
    conventions: dict[str, Any] = {
        "has_tests_unit": (root / "tests" / "unit").is_dir(),
        "has_tests_dir": (root / "tests").is_dir(),
        "test_layout": "unknown",
    }
    if conventions["has_tests_unit"]:
        conventions["test_layout"] = "1:1:1"
    elif conventions["has_tests_dir"]:
        conventions["test_layout"] = "flat"
    return conventions


def _to_nonneg_int(value: Any) -> int:
    """Coerce a potentially-corrupted state value to a non-negative integer.

    Handles ``None``, ``bool``, ``str``, and numeric inputs from checkpoints
    that may have been corrupted or migrated from older state schemas.
    ``bool`` is checked before ``int`` because ``bool`` is a subclass of
    ``int`` and ``True``/``False`` should not be treated as ``1``/``0``.

    Args:
        value: Arbitrary value from workflow state.

    Returns:
        Non-negative integer (0 if coercion fails or result is negative).
    """
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return max(0, value)
    if isinstance(value, float):
        return max(0, int(value))
    if isinstance(value, str):
        try:
            return max(0, int(value))
        except ValueError:
            return 0
    return 0


def read_file_content(path: Path, *, max_chars: int = 10000) -> str:
    """Read file content with a character budget.

    Args:
        path: File path to read.
        max_chars: Maximum characters to return.

    Returns:
        File content truncated to at most max_chars characters.
    """
    _suffix = "\n... [truncated]"
    try:
        content = path.read_text(encoding="utf-8")
        if len(content) > max_chars:
            if max_chars <= len(_suffix):
                return content[:max_chars]
            return content[: max_chars - len(_suffix)] + _suffix
        return content
    except (OSError, UnicodeDecodeError):
        return ""


def get_run_id() -> str | None:
    """Return the LangGraph run_id for the current node execution.

    Returns the run_id string when called from within a LangGraph node, or
    ``None`` when called outside a runnable context (e.g. in tests or direct
    CLI invocations). Callers must handle ``None`` gracefully (idempotency
    protection is best-effort when the run_id is unavailable).
    """
    try:
        from langgraph.config import get_config

        config = get_config()
        raw = config.get("configurable", {}).get("run_id")
        return str(raw) if raw else None
    except Exception:
        return None


def build_idempotency_registry(run_id: str | None) -> Any:
    """Return an IdempotencyRegistry for the current run, or None on failure.

    Returns None when ``run_id`` is absent (outside a LangGraph context) or
    when the state directory cannot be resolved, so callers degrade gracefully.
    """
    if not run_id:
        return None
    try:
        from pathlib import Path

        from agentic_devtools.orchestration.execution.idempotency import IdempotencyRegistry
        from agentic_devtools.state import get_state_dir

        return IdempotencyRegistry(Path(get_state_dir()), run_id)
    except Exception as exc:
        logger.debug("IdempotencyRegistry unavailable: %s", exc)
        return None
