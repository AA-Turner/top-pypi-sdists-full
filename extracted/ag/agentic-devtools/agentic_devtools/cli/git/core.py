"""
Core utilities for git CLI commands.

This module provides low-level helpers used by git operations:
- State management helpers
- Git command execution
- Temporary file handling
"""

import sys
import tempfile
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from subprocess import CompletedProcess
from typing import NoReturn

from ...state import get_value
from ..subprocess_utils import run_safe

# State keys
STATE_COMMIT_MESSAGE = "commit_message"
STATE_COMMIT_MESSAGE_TITLE = "commit_message_title"
STATE_OVERWRITE_COMMIT_MESSAGE_TITLE = "overwrite_commit_message_title"
STATE_DRY_RUN = "dry_run"
STATE_SKIP_STAGE = "skip_stage"
STATE_SKIP_PUBLISH = "skip_publish"
STATE_SKIP_PUSH = "skip_push"
STATE_SKIP_REBASE = "skip_rebase"
STATE_LAST_COMMIT_MESSAGE = "git.last_commit_message"

# Boolean truthy values for state parsing
_TRUTHY_VALUES = (True, "true", "1", "yes")


class GitError(RuntimeError):
    """Raised by :func:`run_git_safe` when a git command exits non-zero.

    Unlike :func:`run_git` (which calls ``sys.exit`` on failure), ``run_git_safe``
    raises this exception so that node code can catch it and convert it into a
    structured ``BlockedState`` result rather than terminating the host process.

    Attributes:
        returncode: The git command's non-zero exit code.
        stderr: The command's captured stderr (stripped).
        args_list: The git arguments that were run (without the leading ``git``).
    """

    def __init__(self, returncode: int, stderr: str, args_list: list[str]) -> None:
        self.returncode = returncode
        self.stderr = stderr
        self.args_list = args_list
        joined = " ".join(args_list)
        message = f"git {joined} failed with exit code {returncode}"
        if stderr:
            message = f"{message}: {stderr}"
        super().__init__(message)


def _raise_git_os_error(exc: OSError, args: list[str]) -> NoReturn:
    """Raise :class:`GitError` for git process startup/environment failures."""
    returncode = exc.errno if isinstance(exc.errno, int) and exc.errno > 0 else 1
    stderr = str(exc).strip() or exc.__class__.__name__
    raise GitError(returncode, stderr, list(args)) from exc


def run_git_safe(args: list[str], cwd: str | None = None) -> CompletedProcess:
    """Run a git command, raising :class:`GitError` on failure instead of exiting.

    This is the non-exiting counterpart to :func:`run_git`, intended for use inside
    LangChain node boundaries where a ``sys.exit`` (raised by ``run_git(check=True)``)
    would terminate the whole process. ``shell=False`` is passed explicitly because
    ``run_safe`` defaults to ``shell=True`` on Windows for list args, which is unsafe
    for git commands that may include user-controlled text.

    Args:
        args: Git command arguments (e.g. ``["add", "."]``), without the leading
            ``git``.
        cwd: Optional working directory in which to run the command. Node code MUST
            forward the target worktree path here so operations run inside the
            worktree rather than the caller's process CWD.

    Returns:
        The :class:`CompletedProcess` on success (exit code 0).

    Raises:
        GitError: If the git command exits non-zero or the git process cannot be
            started in the requested environment.
    """
    try:
        result = run_safe(
            ["git", *args],
            capture_output=True,
            text=True,
            shell=False,
            cwd=cwd,
        )
    except OSError as exc:
        _raise_git_os_error(exc, args)
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        raise GitError(result.returncode, stderr, list(args))
    return result


def run_git_capture(args: list[str], cwd: str | None = None) -> CompletedProcess:
    """Run a git command and return the result WITHOUT raising on failure.

    The non-raising counterpart to :func:`run_git_safe`, for probe commands where
    a non-zero exit code is an expected, meaningful outcome (e.g. ``rev-parse
    --verify``, ``diff --quiet``, an attempted ``rebase`` that may conflict, or a
    ``stash pop`` that may fail). Callers inspect ``result.returncode`` themselves.

    ``shell=False`` is passed explicitly for the same safety reason as
    :func:`run_git_safe`.

    Args:
        args: Git command arguments (without the leading ``git``).
        cwd: Optional working directory in which to run the command.

    Returns:
        The :class:`CompletedProcess`, regardless of exit code.

    Raises:
        GitError: If the git process cannot be started in the requested
            environment.
    """
    try:
        return run_safe(
            ["git", *args],
            capture_output=True,
            text=True,
            shell=False,
            cwd=cwd,
        )
    except OSError as exc:
        _raise_git_os_error(exc, args)


def get_bool_state(key: str, default: bool = False) -> bool:
    """
    Get a boolean value from state.

    Args:
        key: The state key to read
        default: Default value if key not found

    Returns:
        Boolean value
    """
    value = get_value(key)
    if value is None:
        return default
    return value in _TRUTHY_VALUES


def run_git(*args: str, check: bool = True) -> CompletedProcess:
    """
    Run a git command and return the result.

    Uses run_safe for keyboard interrupt protection and proper encoding.

    Args:
        *args: Git command arguments (e.g., 'add', '.')
        check: If True, raise on non-zero exit code

    Returns:
        CompletedProcess result

    Raises:
        SystemExit: If check=True and git command fails
    """
    cmd = ["git"] + list(args)
    result = run_safe(
        cmd,
        capture_output=True,
        text=True,
        shell=False,
    )

    if check and result.returncode != 0:
        error_msg = f"Error: git {' '.join(args)} failed"
        print(error_msg, file=sys.stderr)
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        sys.exit(result.returncode)

    return result


def get_current_branch() -> str:
    """
    Get the current git branch name.

    Returns:
        The current branch name

    Raises:
        SystemExit: If not on a branch (detached HEAD) or unable to determine
    """
    result = run_git("rev-parse", "--abbrev-ref", "HEAD")
    branch = result.stdout.strip()

    if not branch or branch == "HEAD":
        print(
            "Error: Unable to determine current branch name (detached HEAD?)",
            file=sys.stderr,
        )
        sys.exit(1)

    return branch


def get_commit_message() -> str:
    """
    Get the commit message from state.

    The message is retrieved from the 'commit_message' key in state.
    Multiline messages are supported natively!

    Returns:
        The commit message string

    Raises:
        SystemExit: If no commit message is set in state
    """
    message = get_value(STATE_COMMIT_MESSAGE)

    if not message:
        print(
            f'Error: No commit message set. Use: agdt-set {STATE_COMMIT_MESSAGE} "Your message"'
            f"\n  Alternatively, configure a commit template at .agdt/config/commit-template.j2"
            f"\n  and set the required state keys (versionControl.commitMessageTitle, issue_key, etc.)",
            file=sys.stderr,
        )
        sys.exit(1)

    return str(message)


@contextmanager
def temp_message_file(message: str) -> Generator[str, None, None]:
    """
    Create a temporary file with the commit message.

    This context manager ensures the temp file is cleaned up properly.

    Args:
        message: The commit message to write

    Yields:
        Path to the temporary file
    """
    temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8")
    try:
        temp_file.write(message)
        temp_file.close()  # Close before git reads it (Windows compatibility)
        yield temp_file.name
    finally:
        try:
            Path(temp_file.name).unlink(missing_ok=True)
        except OSError:
            pass  # Best effort cleanup
