"""Worktree setup capability helpers."""

from __future__ import annotations

import os
import platform
import shutil
import sys
from typing import Any

_WORKFLOW_AGNOSTIC_FALLBACK_PROMPT = (
    "Please run this command now: agdt-get-next-workflow-prompt. "
    "It prints the current workflow instructions. "
    "Wait to begin any work until it has finished. "
    "The agentic-devtools workflow will guide you through each step."
)


def _parse_non_negative_timeout(value: Any) -> int | None:
    """Parse a non-negative integer timeout from persisted state."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value >= 0 else None
    if not isinstance(value, str):
        return None

    stripped_value = value.strip()
    if stripped_value.startswith(("+", "-")):
        sign = stripped_value[0]
        digits = stripped_value[1:]
    else:
        sign = ""
        digits = stripped_value
    if not digits.isdigit():
        return None
    if sign == "-":
        return None
    try:
        return int(f"{sign}{digits}")
    except ValueError, OverflowError:
        return None


def _terminal_kwargs(terminal: bool) -> dict[str, Any]:
    """Return terminal-only keyword arguments without changing default calls."""
    return {"terminal": True} if terminal else {}


def _build_session_start_prompt(prompt_file_relative_path: str) -> str:
    """Build a Copilot session start prompt that names the exact resolved prompt file.

    Uses the exact relative path from the worktree root rather than a glob pattern,
    so the model receives a path that is guaranteed to resolve regardless of state
    directory layout (scoped, ``_unscoped``, or ``AGENTIC_DEVTOOLS_STATE_DIR``
    override).

    Args:
        prompt_file_relative_path: Path to the prompt file relative to the worktree
            root, as returned by :func:`_prompt_file_relative_path`.

    Returns:
        A single-line start prompt string naming the exact file.
    """
    return (
        f"Please read this file now: {prompt_file_relative_path}. "
        "It contains the workflow instructions. "
        "Wait to begin any work until you have read it. "
        "The agentic-devtools workflow will guide you through each step."
    )


def _build_recovery_start_prompt(command: list[str] | None = None) -> str:
    """Build a single-line prompt that retries the failed setup command."""
    if not command:
        return _WORKFLOW_AGNOSTIC_FALLBACK_PROMPT

    command_text = " ".join(_quote_recovery_argument(part) for part in command)
    if platform.system() == "Windows":
        command_text = f"& {command_text}"
    return f"Please rerun this exact command now: {command_text}"


def _quote_recovery_argument(value: object) -> str:
    """Quote a recovery command argument for the terminal that will run it."""
    text = str(value).replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    if platform.system() == "Windows":
        return "'" + text.replace("'", "''") + "'"

    import shlex

    return shlex.quote(text)


def _in_test_environment() -> bool:
    """Check if running inside a pytest session.

    Returns ``True`` when ``PYTEST_CURRENT_TEST`` is set in the
    environment.  Used as a guard in functions that launch VS Code
    windows or write ``tasks.json`` with ``runOn: folderOpen`` to
    prevent unexpected side-effects during test runs.

    The check is isolated in its own function so that tests which
    need to exercise the guarded logic can ``@patch`` it to return
    ``False`` while keeping the guard active for all other tests.
    """
    return bool(os.environ.get("PYTEST_CURRENT_TEST"))


def is_vscode_available() -> bool:
    """Check if VS Code CLI is available on PATH.

    Returns:
        True if the ``code`` command is found on PATH, False otherwise.
    """
    return shutil.which("code") is not None


def _contains_windows_cmd_metacharacters(value: str) -> bool:
    """Return True when *value* contains cmd.exe metacharacters or line separators.

    When ``shell=True`` is in effect on Windows, cmd.exe interprets ``&``, ``|``,
    ``<``, ``>``, ``^``, ``%``, and ``!`` as command separators or variable
    delimiters. It also treats carriage-return/newline as command separators.
    A value that contains any of these characters must not be passed to a
    shell-spawned process without this check.
    """
    return any(ch in value for ch in "&|<>^%!\r\n")


def _contains_send_sequence_shell_metacharacters(value: str) -> bool:
    """Return True when *value* contains metacharacters dangerous in VS Code sendSequence text.

    ``sendSequence`` types text directly into the user's VS Code integrated
    terminal.  The active shell may be PowerShell, Git Bash, or any POSIX shell,
    where ``$``/backticks trigger substitution and quotes/``;`` can terminate
    or append shell statements. These characters must not appear in
    marker-derived values sent via ``sendSequence``.

    This is a superset of :func:`_contains_windows_cmd_metacharacters` — it
    covers cmd.exe metacharacters as well as cross-shell injection characters.
    """
    return any(ch in value for ch in "&|<>^%!\r\n$`;'\"")


def find_workspace_file(directory: str) -> str | None:
    """
    Find a VS Code workspace file in the given directory.

    Searches for any file matching the ``*.code-workspace`` glob pattern
    in the directory root.  Returns the full path to the first match, or
    ``None`` if no workspace file is found.

    Args:
        directory: Path to the directory to search in.

    Returns:
        Full path to the workspace file, or None if not found.
    """
    try:
        matches = sorted(
            entry.path for entry in os.scandir(directory) if entry.is_file() and entry.name.endswith(".code-workspace")
        )
        return matches[0] if matches else None
    except FileNotFoundError, NotADirectoryError:
        pass
    except OSError as exc:
        print(f"Warning: unexpected OS error scanning '{directory}': {exc}", file=sys.stderr)
    return None


def generate_workflow_branch_name(
    issue_key: str,
    issue_type: str,
    workflow_name: str,
    parent_key: str | None = None,
) -> str:
    """
    Generate a branch name based on issue type and workflow.

    Patterns:
    - Create workflows: <issueType>/<issue_key>/create-<issueType>
    - Update workflows: <issueType>/<issue_key>/update-<issueType>
    - Subtask create: subtask/<parent_key>/<issue_key>/create-subtask

    Args:
        issue_key: The Jira issue key (e.g., "PROJECT-1234")
        issue_type: The issue type (Task, Epic, Sub-task, Bug, etc.)
        workflow_name: The workflow name (create-jira-issue, create-jira-epic, etc.)
        parent_key: For subtasks, the parent issue key (e.g., "PROJECT-1233")

    Returns:
        The branch name following the pattern
    """
    # Normalize issue type to lowercase for branch naming
    normalized_type = issue_type.lower().replace(" ", "-")

    # Handle Sub-task specially
    if normalized_type == "sub-task":
        normalized_type = "subtask"

    # Determine workflow action from workflow name
    if "update" in workflow_name.lower():
        action = f"update-{normalized_type}"
    else:
        action = f"create-{normalized_type}"

    # For subtasks with a parent, include parent key
    if normalized_type == "subtask" and parent_key:
        return f"{normalized_type}/{parent_key}/{issue_key}/{action}"

    # Standard pattern: <type>/<key>/<action>
    return f"{normalized_type}/{issue_key}/{action}"
