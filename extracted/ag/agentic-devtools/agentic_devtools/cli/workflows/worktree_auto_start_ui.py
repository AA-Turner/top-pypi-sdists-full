"""Worktree setup capability helpers."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from datetime import UTC

from agentic_devtools.file_locking import FileLockError, locked_file

from .worktree_setup_helpers import _contains_windows_cmd_metacharacters, find_workspace_file


def _write_pending_auto_start_marker(
    worktree_path: str,
    run_id: str,
    start_prompt: str,
    model: str | None = None,
) -> None:
    """Write a JSON marker file for the terminal-send fallback mechanism.

    The marker is written to ``<worktree_path>/.vscode/pending-auto-start.json``
    and contains the parameters needed to reconstruct the
    ``agdt-copilot-auto-start`` command line if the primary ``runOn: folderOpen``
    task does not fire.

    This is a best-effort operation: errors are printed to stderr but never
    raised to the caller.
    """
    from datetime import datetime

    from .worktree_setup import (
        _AUTO_START_FILE_LOCK_TIMEOUT_SECONDS,
        _AUTO_START_TASK_LABEL,
        _PENDING_AUTO_START_FILENAME,
        _get_pending_auto_start_marker_lock_path,
    )

    vscode_dir = os.path.join(worktree_path, ".vscode")
    marker_path = os.path.join(vscode_dir, _PENDING_AUTO_START_FILENAME)
    marker = {
        "run_id": run_id,
        "start_prompt": start_prompt,
        "model": model,
        "worktree_path": worktree_path,
        "created_utc": datetime.now(UTC).isoformat(),
        "task_label": _AUTO_START_TASK_LABEL,
    }
    try:
        with locked_file(
            _get_pending_auto_start_marker_lock_path(worktree_path),
            mode="a+",
            exclusive=True,
            timeout=_AUTO_START_FILE_LOCK_TIMEOUT_SECONDS,
        ):
            os.makedirs(vscode_dir, exist_ok=True)
            with open(marker_path, "w", encoding="utf-8") as fh:
                json.dump(marker, fh, indent=2, ensure_ascii=False)
    except (FileLockError, OSError) as exc:
        print(
            f"Warning: failed to write pending auto-start marker at {marker_path}: {exc}",
            file=sys.stderr,
        )


def _cleanup_pending_auto_start_marker(worktree_path: str, expected_run_id: str | None = None) -> None:
    """Delete the pending auto-start marker file if it exists.

    Cleanup is scoped to ``expected_run_id`` and fails closed when the caller
    does not provide a non-blank owning run ID. Best-effort: errors are printed
    to stderr but never raised.
    """
    from .worktree_setup import (
        _AUTO_START_FILE_LOCK_TIMEOUT_SECONDS,
        _PENDING_AUTO_START_FILENAME,
        _get_pending_auto_start_marker_lock_path,
    )

    marker_path = os.path.join(worktree_path, ".vscode", _PENDING_AUTO_START_FILENAME)
    try:
        if not isinstance(expected_run_id, str):
            return
        normalized_expected_run_id = expected_run_id.strip()
        if not normalized_expected_run_id:
            return
        if not os.path.isdir(worktree_path):
            return
        if os.path.exists(marker_path):
            with locked_file(
                _get_pending_auto_start_marker_lock_path(worktree_path),
                mode="a+",
                exclusive=True,
                timeout=_AUTO_START_FILE_LOCK_TIMEOUT_SECONDS,
            ):
                try:
                    with open(marker_path, encoding="utf-8") as fh:
                        marker = json.load(fh)
                except OSError, json.JSONDecodeError, ValueError:
                    return
                if not isinstance(marker, dict):
                    return
                marker_run_id = marker.get("run_id")
                if not isinstance(marker_run_id, str):
                    return
                if marker_run_id.strip() != normalized_expected_run_id:
                    return
                os.remove(marker_path)
    except (FileLockError, OSError) as exc:
        print(
            f"Warning: failed to remove pending auto-start marker at {marker_path}: {exc}",
            file=sys.stderr,
        )


def _focus_vscode_window(worktree_path: str) -> bool:
    """Bring the VS Code window for the given worktree to focus.

    Calls ``code <target>`` where *target* is the ``.code-workspace`` file
    if one exists, otherwise the worktree folder path.  When VS Code
    already has a window open for this folder, the CLI brings it to
    focus; when no window exists, a new one is opened (acceptable —
    ``sendSequence`` will target it).

    Returns ``True`` when the ``code`` process exits with returncode 0,
    ``False`` on any error.
    """
    target = find_workspace_file(worktree_path) or worktree_path
    try:
        use_shell = platform.system() == "Windows"
        if use_shell and _contains_windows_cmd_metacharacters(target):
            print(
                "Warning: refusing to focus VS Code on Windows because "
                f"path contains cmd.exe metacharacters: {target!r}",
                file=sys.stderr,
            )
            return False
        proc = subprocess.run(  # nosec B602 - shell=True only on Windows to find 'code.cmd' via PATH; metacharacter check above guards the path
            ["code", target],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
            shell=use_shell,
        )
    except OSError, subprocess.TimeoutExpired:
        print("--- Pre-focus: 'code' command failed or timed out. ---")
        return False

    if proc.returncode != 0:
        print(f"--- Pre-focus: 'code' exited with code {proc.returncode}. ---")
        return False

    return True


def _open_log_in_vscode(log_file_path: str, worktree_path: str) -> None:
    """Open the Copilot session log file in VS Code for live monitoring.

    Uses ``code <log_file_path>`` to request opening the file in VS Code.
    The CLI decides which window receives the file (often the most recently
    active window). Best-effort: errors are printed to stderr but never raised.

    Args:
        log_file_path: Absolute path to the ``.log`` file.
        worktree_path: The worktree root (used for context in messages).
    """
    try:
        log_file_path = os.path.abspath(log_file_path)
        use_shell = platform.system() == "Windows"
        if use_shell and _contains_windows_cmd_metacharacters(log_file_path):
            print(
                "Warning: refusing to open log file in VS Code on Windows because "
                f"path contains cmd.exe metacharacters: {log_file_path!r}",
                file=sys.stderr,
            )
            return
        proc = subprocess.run(  # nosec B602 - shell=True only on Windows to find 'code.cmd' via PATH; args is a fixed list, and the metacharacter check above guards the path
            ["code", log_file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
            shell=use_shell,
        )
        if proc.returncode == 0:
            print(f"--- Opened Copilot session log in VS Code: {log_file_path} (worktree: {worktree_path}) ---")
        else:
            print(
                f"Warning: 'code' exited with {proc.returncode} when opening log file "
                f"{log_file_path!r} (worktree: {worktree_path}).",
                file=sys.stderr,
            )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(
            f"Warning: could not open log file in VS Code: {exc} (worktree: {worktree_path}, file: {log_file_path!r})",
            file=sys.stderr,
        )


def _shell_quote(s: str) -> str:
    """Quote a string for safe embedding in a shell command.

    Uses :func:`shlex.quote` on non-Windows platforms. On Windows, wraps
    the string in double quotes, doubles embedded double quotes, and
    doubles percent signs to avoid ``%VAR%`` expansion by ``cmd.exe``.

    Note: The quoted strings are embedded in a VS Code terminal
    ``sendSequence`` text payload. The data originates from the
    ``pending-auto-start.json`` marker file that we wrote ourselves, so
    injection risk is minimal.
    """
    if platform.system() == "Windows":
        # This Windows branch does not attempt full cmd.exe metacharacter
        # escaping. It only doubles embedded double quotes and percent
        # signs, then wraps the result in double quotes.
        escaped = s.replace('"', '""').replace("%", "%%")
        return '"' + escaped + '"'
    import shlex  # noqa: PLC0415 — lazy import; not needed on Windows

    return shlex.quote(s)
