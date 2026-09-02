"""
GitHub Copilot CLI session management.

Provides utilities for starting and managing Copilot CLI sessions
programmatically, supporting both interactive and non-interactive modes,
with session ID tracking and state persistence.

Binary variants
---------------
Two Copilot CLI variants are supported:

* **Standalone binary** (preferred) – invoked as ``copilot -i <prompt>``
  (interactive) or ``copilot -p <prompt>`` (non-interactive).  The
  standalone binary has **no** ``suggest`` subcommand.
* **``gh copilot`` extension** (fallback) – invoked as
  ``gh copilot suggest <prompt>``.

The ``_build_copilot_args`` helper selects the correct variant at runtime.

Research notes
--------------
The standalone binary requires ``--allow-all`` when running in
non-interactive mode; without it shell-command tool invocations (including
``agdt-*`` commands, ``python``, ``gh``, etc.) are rejected with "Permission
denied and could not request permission from user".  ``--allow-all`` is
equivalent to ``--allow-all-tools --allow-all-paths --allow-all-urls`` and
grants the full set of permissions required for autonomous workflow execution.
``_build_copilot_args`` therefore appends ``--allow-all`` to the argument
list for the standalone-binary non-interactive path.

Interactive sessions also receive ``--allow-all`` by default
(``allow_all=True``) so that an auto-started session does not block on the
interactive "Enable all permissions" confirmation prompt that ``--autopilot``
otherwise displays.  Callers can pass ``allow_all=False`` to restore
interactive permission prompting.  The ``gh copilot`` extension fallback does
not support these flags and is left unchanged.

The standalone binary also supports ``--autopilot`` for interactive sessions.
When ``--autopilot`` is passed the agent executes tasks autonomously without
requiring the user to press Tab to activate autopilot mode.  This flag is only
meaningful for interactive (``-i``) sessions; non-interactive (``-p``) sessions
already run autonomously via ``--allow-all``.  The ``gh copilot`` extension
fallback does not support ``--autopilot``; a warning is emitted when autopilot
is requested but only the fallback is available.

For non-interactive sessions the full prompt text is written to a file on
disk, and a short file-reference instruction is passed via ``-p`` instead of
the raw prompt content.  This avoids reliability issues with multiline /
special-character content in Windows command-line argument passing and gives
the agent an unambiguous first action (read the instruction file).

Fallback behaviour
------------------
When neither the standalone binary nor the ``gh copilot`` extension is
available the session cannot be started.  The module logs a warning and
prints the prompt to stdout so that the user or pipeline can invoke a
session manually.
"""

import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
import uuid
import warnings
from contextlib import suppress
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import IO

from agentic_devtools.file_locking import FileLockError, locked_state_file
from agentic_devtools.state import get_state_dir, read_modify_write_state, set_value

from ..subprocess_utils import run_safe

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Default Copilot model used as ultimate fallback when no model is configured
# in project config and none is supplied via --model.
DEFAULT_COPILOT_MODEL = "gpt-4o"


def get_default_copilot_model() -> str:
    """Return the default Copilot model for workflow sessions.

    Resolution order:
    1. ``default_copilot_model`` in ``.agdt/config/project.json`` (set by
       ``agdt-setup`` model selection prompt).
    2. :data:`DEFAULT_COPILOT_MODEL` hardcoded constant (``"gpt-4o"``).

    Returns:
        A non-empty model identifier string.
    """
    try:
        from agentic_devtools.cli.config.project_config import get_effective_project_config_value

        configured = get_effective_project_config_value("default_copilot_model")
        if configured and configured.strip():
            return configured.strip()
    except Exception:
        pass
    return DEFAULT_COPILOT_MODEL


# State key namespace
_COPILOT_NS = "copilot"

# Log file directory (relative to state dir)
_LOG_DIR_NAME = "background-tasks/logs"

# Prompt file naming pattern
_PROMPT_FILE_PATTERN = "copilot-session-{session_id}-prompt.md"

# Structured lifecycle log marker prefix
_LOG_PREFIX = "[agdt-copilot-session]"

# Heartbeat interval in seconds for non-interactive session lifecycle logging
_HEARTBEAT_INTERVAL_SECONDS = 60

# Managed install path for the standalone copilot binary
_MANAGED_COPILOT = Path.home() / ".agdt" / "bin" / ("copilot.exe" if sys.platform == "win32" else "copilot")

# Maximum prompt length (in characters) that can safely be passed as a
# CLI argument.  The standalone binary receives the prompt via ``-i`` or
# ``-p``; the ``gh copilot`` extension receives it as a positional
# argument to ``gh copilot suggest``.  Windows' CreateProcess imposes a
# 32,767-character limit on the entire command line; we leave headroom
# for the command prefix and OS overhead.
_MAX_GH_COPILOT_ARGV_LENGTH = 30_000

# Safe length limit for the pre-processed inline prompt passed via argv.
# Truncation is applied to the prompt content (before ``_build_copilot_args``
# checks ``_MAX_GH_COPILOT_ARGV_LENGTH``) so that the final single-line
# version produced by ``_inline_prompt`` (after ``\n`` → ``<br>`` replacement
# and appending the backup file-reference suffix) still sits at least 100
# characters below the hard cap.  This gap is a conservative safety margin
# for the rest of the command line (flags, executable path, OS overhead) and
# guards against minor miscounts in edge-case content.
_SAFE_ARGV_LENGTH = 29_900


# ---------------------------------------------------------------------------
# Public dataclass
# ---------------------------------------------------------------------------


@dataclass
class CopilotSessionResult:
    """Result returned by :func:`start_copilot_session`.

    Attributes:
        session_id: Unique identifier for the session (UUID4 hex).
        mode: ``"interactive"`` or ``"non-interactive"``.
        prompt_file: Absolute path to the temporary prompt file.
        start_time: ISO-8601 UTC timestamp when the session was started.
        pid: Process ID for non-interactive sessions; ``None`` for
            interactive sessions (where the process has already exited
            when this object is returned).
        process: The :class:`subprocess.Popen` handle for non-interactive
            sessions; ``None`` for interactive sessions.
        log_file: Absolute path to the session log file for non-interactive
            sessions; ``None`` for interactive sessions.
    """

    session_id: str
    mode: str
    prompt_file: str
    start_time: str
    pid: int | None = field(default=None)
    process: subprocess.Popen | None = field(default=None, repr=False)  # type: ignore[type-arg]
    log_file: str | None = field(default=None)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class CopilotChildAliveError(RuntimeError):
    """Raised when a Copilot startup abort cannot confirm the child process exited.

    The child process may still be running.  Callers that track ownership
    claims (e.g. the delayed-fallback verifier) must **not** release or
    unmark those claims when they catch this exception — the live child
    continues to hold the session mutex.

    The original exception that triggered the abort is chained as
    :attr:`__cause__` and is always an instance of :class:`Exception`.
    """


# ---------------------------------------------------------------------------
# Availability check
# ---------------------------------------------------------------------------


def _get_copilot_binary() -> str | None:
    """Return the path to the copilot binary, or ``None`` if not found.

    Checks (in order):
    1. The managed install at ``~/.agdt/bin/copilot[.exe]``.
    2. The standalone ``copilot`` binary on the system ``PATH``.

    The managed install is preferred because it is a direct executable that
    avoids the ``.bat`` → ``copilot.ps1`` indirection used by the VS Code
    Copilot Chat extension's bundled CLI.  On Windows, that ``.ps1`` file can
    be temporarily locked by the extension during activation, causing transient
    ``ERROR_SHARING_VIOLATION`` failures that are invisible to
    ``subprocess.run`` (they manifest as non-zero exit codes from the batch
    wrapper rather than ``OSError``).

    Returns:
        Absolute path string when found, ``None`` otherwise.
    """
    if _MANAGED_COPILOT.is_file():
        return str(_MANAGED_COPILOT)
    system_path = shutil.which("copilot")
    if system_path:
        return system_path
    return None


def is_gh_copilot_available() -> bool:
    """Return ``True`` if a usable Copilot CLI can be invoked on this machine.

    Checks (in order):
    1. A standalone ``copilot`` binary (system PATH or ``~/.agdt/bin/``).
    2. The ``gh copilot`` extension (legacy fallback): ``gh`` must be present
       and ``gh copilot --help`` must exit with return code 0.

    Returns:
        ``True`` when at least one check passes; ``False`` otherwise.
    """
    # Prefer standalone copilot binary
    if _get_copilot_binary() is not None:
        return True

    # Fallback: gh copilot extension
    if not shutil.which("gh"):
        return False
    try:
        result = run_safe(
            ["gh", "copilot", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
            shell=False,
        )
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _emit_log_marker(
    log_file: IO[str],
    stdout: IO[str] | None,
    event: str,
    **fields: object,
) -> None:
    """Write a structured lifecycle marker to *log_file* and optionally *stdout*.

    Format::

        [agdt-copilot-session] EVENT 2024-12-19T15:50:26+00:00 key=value ...

    Values that contain whitespace, quotes, backslashes, or non-printable
    characters are JSON-string-escaped so markers remain machine-parseable.
    Writes are flushed immediately.
    *stdout* failures are silently ignored (same resilience as ``_tee``).
    """
    timestamp = datetime.now(UTC).isoformat()
    parts = [_LOG_PREFIX, event, timestamp]
    _needs_escape = frozenset('" \\')
    for key, value in fields.items():
        str_val = str(value)
        if not str_val or any(ch in _needs_escape or ch.isspace() or not ch.isprintable() for ch in str_val):
            str_val = json.dumps(str_val)
        parts.append(f"{key}={str_val}")
    line = " ".join(parts) + "\n"

    log_file.write(line)
    log_file.flush()

    if stdout is not None:
        try:
            stdout.write(line)
            stdout.flush()
        except (OSError, ValueError):
            pass


def _make_session_id() -> str:
    """Generate a new unique session identifier (UUID4 hex string)."""
    return uuid.uuid4().hex


def _get_prompt_file_path(session_id: str) -> Path:
    """Return the path where the prompt file should be written.

    The file is placed inside the workflow state directory, following the
    same convention as other temporary files.

    Args:
        session_id: The session identifier.

    Returns:
        Absolute :class:`~pathlib.Path` for the prompt file.
    """
    state_dir = get_state_dir()
    return state_dir / _PROMPT_FILE_PATTERN.format(session_id=session_id)


def _get_log_file_path(session_id: str, start_time: str) -> Path:
    """Return the path for the non-interactive session log file.

    Args:
        session_id: The session identifier.
        start_time: ISO-8601 timestamp (used in the filename).

    Returns:
        Absolute :class:`~pathlib.Path` for the log file.
    """
    state_dir = get_state_dir()
    timestamp = start_time.replace(":", "").replace("-", "").replace(".", "_")[:18]
    filename = f"copilot_session_{timestamp}.log"
    return state_dir / _LOG_DIR_NAME / filename


def _get_jsonl_file_path(session_id: str, start_time: str) -> Path:
    """Return the path for the structured JSON Lines session log file.

    The path mirrors :func:`_get_log_file_path` but uses a ``.jsonl``
    extension instead of ``.log``.

    Args:
        session_id: The session identifier.
        start_time: ISO-8601 timestamp (used in the filename).

    Returns:
        Absolute :class:`~pathlib.Path` for the ``.jsonl`` file.
    """
    return _get_log_file_path(session_id, start_time).with_suffix(".jsonl")


def _build_copilot_args(
    prompt: str,
    *,
    interactive: bool = True,
    autopilot: bool = True,
    allow_all: bool = True,
    model: str | None = None,
) -> list[str] | None:
    """Build the copilot argument list.

    Uses the standalone ``copilot`` binary when available (preferred), falling
    back to the ``gh copilot`` extension for backward compatibility.

    Neither the standalone binary nor the ``gh copilot`` extension supports
    ``--file``.  The standalone binary accepts the prompt via ``-p``/``--prompt``
    for non-interactive use and ``-i`` for interactive use, while the
    ``gh copilot`` extension accepts the prompt as a positional ``[subject]``
    argument.  When the prompt exceeds :data:`_MAX_GH_COPILOT_ARGV_LENGTH`,
    ``None`` is returned so the caller can use a fallback.

    In non-interactive mode the standalone binary also receives
    ``--allow-all`` so that it can execute shell commands (``agdt-*``,
    ``python``, ``gh``, etc.) without prompting for permission.
    ``--allow-all`` is equivalent to ``--allow-all-tools --allow-all-paths
    --allow-all-urls``; ``--allow-all-tools`` alone is insufficient because
    shell commands such as ``gh`` and ``python`` also require path and URL
    permissions.  Without this flag every tool invocation is rejected with
    "Permission denied and could not request permission from user".

    Args:
        prompt: The full prompt text to pass to the copilot command.
        interactive: When ``True`` (default) the standalone binary receives
            ``-i`` (plus ``--allow-all`` by default — see ``allow_all``); when
            ``False`` it receives ``-p`` and ``--allow-all``.  Ignored for the
            ``gh copilot`` extension path which always uses a positional arg.
        autopilot: When ``True`` (default) and ``interactive=True``, the
            standalone binary receives ``--autopilot`` so that the agent
            executes tasks autonomously without requiring the user to press
            Tab.  Has no effect when ``interactive=False`` (non-interactive
            sessions are already autonomous via ``--allow-all``).  When the
            ``gh copilot`` extension fallback is used and both
            ``interactive=True`` and ``autopilot=True``, a warning is emitted
            because the fallback does not support ``--autopilot``.
        allow_all: When ``True`` (default) the standalone binary receives
            ``--allow-all`` (equivalent to ``--allow-all-tools
            --allow-all-paths --allow-all-urls``).  For interactive sessions
            this suppresses the "Enable all permissions" confirmation prompt
            so an auto-started session runs without user interaction; pass
            ``False`` to restore interactive permission prompting.
            Non-interactive sessions always receive ``--allow-all`` regardless
            of this flag, because their tool calls are auto-denied otherwise.
            Has no effect on the ``gh copilot`` extension fallback, which does
            not support the flag.
        model: Optional Copilot model ID (e.g. ``"gpt-4o"``).
            When not ``None`` and not empty, ``--model <model>`` is inserted
            into the standalone binary args before the ``-i``/``-p`` flag.
            The ``gh copilot suggest`` fallback does not support ``--model``;
            a warning is emitted and the flag is omitted.

    Returns:
        List of strings suitable for :func:`subprocess.Popen`, or ``None``
        when the prompt is too large for the argv path.
    """
    # Normalise: treat empty/whitespace-only model as None.
    if isinstance(model, str):
        model = model.strip() or None

    if len(prompt) > _MAX_GH_COPILOT_ARGV_LENGTH:
        return None
    standalone = _get_copilot_binary()
    if standalone:
        flag = "-i" if interactive else "-p"
        # --autopilot, --allow-all, and --model must come before -p/-i so
        # that argument parsers which stop processing flags after the first
        # positional argument still recognise them.
        args = [standalone]
        if interactive and autopilot:
            args.append("--autopilot")
        # Non-interactive sessions always need --allow-all (tool calls are
        # auto-denied otherwise). Interactive sessions receive it by default
        # so the auto-start session does not block on the "Enable all
        # permissions" confirmation prompt; allow_all=False opts back into
        # interactive permission prompting.
        if allow_all or not interactive:
            args.append("--allow-all")
        if model is not None:
            args.extend(["--model", model])
        args.extend([flag, prompt])
        return args
    if interactive and autopilot:
        warnings.warn(
            "--autopilot is not supported by the gh copilot extension fallback; autopilot mode will not be activated.",
            stacklevel=2,
        )
    if model is not None:
        warnings.warn(
            "--model is not supported by the gh copilot extension fallback; model selection will not be applied.",
            stacklevel=2,
        )
    return ["gh", "copilot", "suggest", prompt]


def build_copilot_args(
    prompt: str,
    *,
    interactive: bool = True,
    autopilot: bool = True,
    allow_all: bool = True,
    model: str | None = None,
) -> list[str] | None:
    """Build the copilot argument list (public API).

    Public wrapper around the internal argument builder.  Use this when you
    need to obtain the argument list without starting a full session — for
    example, to inject it into a VS Code ``tasks.json`` auto-start task.

    Args:
        prompt: The full prompt text to pass to the copilot command.
        interactive: When ``True`` (default) the standalone binary receives
            ``-i`` (plus ``--allow-all`` by default — see ``allow_all``); when
            ``False`` it receives ``-p`` and ``--allow-all``.
        autopilot: When ``True`` (default) and ``interactive=True``, the
            standalone binary receives ``--autopilot`` so that the agent
            executes tasks autonomously without requiring the user to press
            Tab.  Has no effect for non-interactive mode.
        allow_all: When ``True`` (default) the standalone binary receives
            ``--allow-all`` for interactive sessions so the auto-started
            session does not block on the "Enable all permissions" prompt.
            Pass ``False`` to restore interactive permission prompting.
            Non-interactive standalone-binary sessions always receive
            ``--allow-all``; the ``gh copilot suggest`` fallback does not
            support the flag and omits it regardless of this setting.
        model: Optional Copilot model ID (e.g. ``"gpt-4o"``).
            When not ``None``, ``--model <model>`` is added for the
            standalone binary.  The ``gh copilot suggest`` fallback emits
            a warning and omits the flag.

    Returns:
        List of strings suitable for :func:`subprocess.Popen`, or ``None``
        when the prompt is too large for the argv path.

    Note:
        When ``interactive=True`` and ``autopilot=True`` but only the
        ``gh copilot`` fallback is available (for example, when the
        standalone Copilot CLI binary is not installed), this function may
        emit a warning message to :data:`sys.stderr` describing the degraded
        behavior.  Callers should be prepared for this additional stderr
        output in that configuration.
    """
    return _build_copilot_args(prompt, interactive=interactive, autopilot=autopilot, allow_all=allow_all, model=model)


def _is_process_alive(pid: int) -> bool:
    """Check whether a process with the given PID is still running.

    Uses ``os.kill(pid, 0)`` on Unix/macOS and ``ctypes``
    ``kernel32.OpenProcess``/``GetExitCodeProcess``/``CloseHandle`` on Windows.

    Args:
        pid: The process ID to check.

    Returns:
        ``True`` if the process exists, ``False`` otherwise.
    """
    if pid <= 0:
        return False

    if sys.platform == "win32":  # pragma: no cover
        try:
            import ctypes

            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            ERROR_ACCESS_DENIED = 5
            # Explicitly set argtypes/restype to avoid 64-bit handle truncation
            kernel32.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
            kernel32.OpenProcess.restype = ctypes.c_void_p
            kernel32.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
            kernel32.GetExitCodeProcess.restype = ctypes.c_int
            kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
            kernel32.CloseHandle.restype = ctypes.c_int
            STILL_ACTIVE = 259

            handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            if handle:
                try:
                    exit_code = ctypes.c_ulong(0)
                    if kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                        return exit_code.value == STILL_ACTIVE
                    # Access denied still indicates the process exists.
                    if ctypes.get_last_error() == ERROR_ACCESS_DENIED:
                        return True
                    return False
                finally:
                    kernel32.CloseHandle(handle)
            # Access denied still indicates the process exists.
            if ctypes.get_last_error() == ERROR_ACCESS_DENIED:
                return True
            return False
        except (OSError, ValueError, OverflowError):
            return False
    else:
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            # Process exists but we don't own it — still alive
            return True
        except (OSError, OverflowError):
            return False


def _check_session_mutex(*, claim: bool = False) -> dict | None:
    """Check whether a Copilot session is already running for this worktree.

    Reads ``copilot.pid`` from state and verifies the process is alive.
    If a live session exists, returns a snapshot dict with the session info
    and prints a warning to stderr. If no live session exists (or the stored
    PID is stale), clears the stale PID and returns ``None`` to allow
    a new session.

    When *claim* is ``True``, this function atomically checks and claims the
    mutex under the state-file lock by writing the current process PID to
    ``copilot.pid`` before returning ``None``.

    Returns:
        A dict with session snapshot fields when a live session blocks the
        new session start, or ``None`` when no live session is active.
    """
    claimer_pid = os.getpid() if claim else None
    snapshot: dict | None = None

    with read_modify_write_state() as state:
        copilot_state = state.get(_COPILOT_NS)
        if not isinstance(copilot_state, dict):
            copilot_state = {}
            state[_COPILOT_NS] = copilot_state

        pid_value = copilot_state.get("pid")
        if pid_value is None or pid_value == "":
            if claimer_pid is not None:
                copilot_state["pid"] = claimer_pid
        else:
            # Parse the PID
            try:
                pid = int(pid_value)
            except (TypeError, ValueError):
                # Unparseable PID — clear stale value and allow
                copilot_state["pid"] = claimer_pid if claimer_pid is not None else ""
            else:
                if pid <= 0:
                    copilot_state["pid"] = claimer_pid if claimer_pid is not None else ""
                elif _is_process_alive(pid):
                    # Check if the process is alive
                    snapshot = {
                        "session_id": copilot_state.get("session_id") or "",
                        "mode": copilot_state.get("mode") or "",
                        "prompt_file": copilot_state.get("prompt_file") or "",
                        "start_time": copilot_state.get("start_time") or "",
                        "pid": pid,
                    }
                else:
                    # PID is stale — clear and (optionally) claim
                    copilot_state["pid"] = claimer_pid if claimer_pid is not None else ""

    if snapshot is not None:
        print(
            f"WARNING: A Copilot session is already running "
            f"(pid={snapshot['pid']}, session_id={snapshot['session_id']}, started={snapshot['start_time']}). "
            f"Skipping new session start.",
            file=sys.stderr,
        )
    return snapshot


def _clear_session_mutex_pid(state: dict, owner_pid: int) -> None:
    """Clear the Copilot PID in *state* when it is still owned by *owner_pid*."""
    copilot_state = state.get(_COPILOT_NS)
    if not isinstance(copilot_state, dict):
        return
    pid_value = copilot_state.get("pid")
    if not isinstance(pid_value, (int, str)):
        return
    try:
        current_pid = int(pid_value)
    except (TypeError, ValueError):
        return
    if current_pid == owner_pid:
        copilot_state["pid"] = ""


def _release_session_mutex_claim(owner_pid: int, state_file_path: Path | None = None) -> None:
    """Clear a startup mutex claim if still owned by *owner_pid*."""
    if state_file_path is not None:
        try:
            with locked_state_file(state_file_path) as fh:
                content = fh.read()
                try:
                    state = json.loads(content) if content.strip() else {}
                except json.JSONDecodeError:
                    return
                original_content = json.dumps(state, indent=2, ensure_ascii=False)
                _clear_session_mutex_pid(state, owner_pid)
                updated_content = json.dumps(state, indent=2, ensure_ascii=False)
                if updated_content == original_content:
                    return
                fh.seek(0)
                fh.write(updated_content)
                fh.truncate()
                fh.flush()
                os.fsync(fh.fileno())
        except (AttributeError, FileLockError, OSError, TypeError):
            return
        return

    with read_modify_write_state() as state:
        _clear_session_mutex_pid(state, owner_pid)


def _transfer_session_mutex_claim(old_pid: int, new_pid: int) -> bool:
    """Atomically transfer the mutex claim from *old_pid* to *new_pid*.

    Reads ``copilot.pid`` under the state-file lock; if it still equals
    *old_pid* it is replaced with *new_pid*.  If the mutex already holds
    *new_pid*, the transfer is treated as already successful. If the mutex has
    been taken by someone else the transfer is skipped.

    Returns:
        ``True`` when the mutex holds *new_pid* after this call, else
        ``False``.

    This must be called immediately after a successful :func:`subprocess.Popen`
    so that the child's PID guards the mutex before the launcher can exit.
    """
    try:
        with read_modify_write_state() as state:
            copilot_state = state.get(_COPILOT_NS)
            if not isinstance(copilot_state, dict):
                return False
            pid_value = copilot_state.get("pid")
            try:
                current = int(pid_value)  # type: ignore[arg-type]
            except (TypeError, ValueError):
                return False
            if current == new_pid:
                return True
            if current == old_pid:
                copilot_state["pid"] = new_pid
                return True
            return False
    except Exception:  # noqa: BLE001
        return False


def _persist_session_state(result: CopilotSessionResult, model: str | None = None) -> None:
    """Write session metadata to ``agdt-state.json``.

    Keys written (all under the ``copilot.`` namespace):
    - ``copilot.session_id``
    - ``copilot.mode``
    - ``copilot.prompt_file``
    - ``copilot.start_time``
    - ``copilot.pid`` (empty string when not applicable)
    - ``copilot.model_id`` (only when *model* is not ``None``)

    Args:
        result: The :class:`CopilotSessionResult` to persist.
        model: Optional Copilot model ID to persist.
    """
    set_value(f"{_COPILOT_NS}.session_id", result.session_id)
    set_value(f"{_COPILOT_NS}.mode", result.mode)
    set_value(f"{_COPILOT_NS}.prompt_file", result.prompt_file)
    set_value(f"{_COPILOT_NS}.start_time", result.start_time)
    set_value(f"{_COPILOT_NS}.pid", result.pid if result.pid is not None else "")
    if model is not None:
        set_value(f"{_COPILOT_NS}.model_id", model)


def _print_fallback_prompt(prompt: str) -> None:
    """Print the prompt to stdout as a fallback when ``gh copilot`` is unavailable.

    Args:
        prompt: The full prompt text to display.
    """
    print(
        "WARNING: gh copilot is not available. Please start a session manually with the following prompt:\n",
        file=sys.stderr,
    )
    print(prompt)


def _inline_prompt(prompt_text: str, prompt_file_path: str) -> str:
    """Convert multi-line prompt to single-line with ``<br>`` separators and backup reference.

    If the result exceeds :data:`_SAFE_ARGV_LENGTH`, the ``Repo-Specific
    Review Focus Areas`` content is truncated first (with ``...`` appended).
    If that is insufficient or the section is absent, a short
    file-reference-only prompt is returned instead so the backup path is
    always preserved.  A :func:`warnings.warn` is emitted whenever
    truncation occurs.
    """
    suffix = f"   <br>   The full prompt is also saved at: {prompt_file_path}"
    single_line = prompt_text.replace("\n", "   <br>   ") + suffix

    if len(single_line) <= _SAFE_ARGV_LENGTH:
        return single_line

    # --- Truncation path: prefer trimming Repo-Specific Focus Areas ---
    focus_marker = "## Repo-Specific Review Focus Areas"
    next_section_prefix = "\n## "

    focus_start = prompt_text.find(focus_marker)
    if focus_start != -1:
        content_start = prompt_text.find("\n", focus_start) + 1
        next_section = prompt_text.find(next_section_prefix, content_start)
        if next_section != -1:
            before = prompt_text[:content_start]
            after = prompt_text[next_section:]
            # Try with focus areas fully removed first
            stripped = before + "...\n" + after
            stripped_line = stripped.replace("\n", "   <br>   ") + suffix
            if len(stripped_line) <= _SAFE_ARGV_LENGTH:
                # Partially include focus areas to use available space
                focus_content = prompt_text[content_start:next_section]
                overhead = len(stripped_line)
                available = _SAFE_ARGV_LENGTH - overhead
                if available > 0:
                    keep = focus_content[:available]
                    last_newline = keep.rfind("\n")
                    if last_newline > 0:
                        keep = keep[:last_newline]
                    partial = before + keep + "\n...\n" + after
                    partial_line = partial.replace("\n", "   <br>   ") + suffix
                    if len(partial_line) <= _SAFE_ARGV_LENGTH:
                        warnings.warn(
                            "Prompt truncated: Repo-Specific Review Focus Areas was trimmed to fit argv limit.",
                            stacklevel=2,
                        )
                        return partial_line
                # Fall through to fully removed version
                warnings.warn(
                    "Prompt truncated: Repo-Specific Review Focus Areas fully removed to fit argv limit.",
                    stacklevel=2,
                )
                return stripped_line

    # No focus areas section or still too long — fall back to a short
    # file-reference-only prompt so the backup path is always preserved.
    warnings.warn(
        "Prompt too large for inline use; falling back to file-reference-only prompt.",
        stacklevel=2,
    )
    return f"Prompt too large to pass inline safely. The full prompt is also saved at: {prompt_file_path}"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def start_copilot_session(
    prompt: str,
    working_directory: str,
    interactive: bool = True,
    session_id: str | None = None,
    *,
    autopilot: bool = True,
    allow_all: bool = True,
    model: str | None = None,
) -> CopilotSessionResult:
    """Start a ``gh copilot`` CLI session with the given prompt.

    Behaviour:
    - Generates (or reuses) a unique session ID.
    - Writes *prompt* to a temporary file for persistence and manual
      reuse.  The full prompt text is inlined as a single line (newlines
      replaced with ``   <br>   ``) and passed as a CLI argument to the
      Copilot process in both interactive and non-interactive modes.
      A backup file reference is appended to the inlined prompt.
    - If the inlined prompt exceeds the safe argv-length limit
      (``_SAFE_ARGV_LENGTH``), the ``Repo-Specific Review Focus Areas``
      section is truncated first.  If that is insufficient or absent,
      a short file-reference-only prompt is used instead.  A warning is
      emitted whenever truncation occurs.
    - If ``_build_copilot_args`` still returns ``None`` (prompt exceeds
      ``_MAX_GH_COPILOT_ARGV_LENGTH``), the full prompt is printed to
      stdout as a fallback.
    - Starts ``copilot -i/-p <prompt>`` (standalone binary) or
      ``gh copilot suggest <prompt>`` (extension fallback).
    - In **interactive** mode the child process inherits the current
      terminal (stdin / stdout / stderr), so the user can interact with
      it directly.  This call blocks until the interactive session ends.
    - In **non-interactive** mode the child process runs in the
      background with stdout and stderr captured to a log file.  The
      call returns immediately.
    - Session metadata is written to ``agdt-state.json`` under the
      ``copilot.*`` namespace.
    - If ``gh copilot`` is not available, a warning is emitted and the
      prompt is printed to stdout so the user can start a session
      manually.

    Args:
        prompt: The full prompt text to send to the Copilot session.
        working_directory: The directory in which to run the command.
            Typically the worktree root.
        interactive: When ``True`` (default) the process runs with an
            attached terminal.  When ``False`` the process runs
            detached in the background.
        session_id: Optional pre-generated session ID.  A new UUID4 hex
            string is generated when this is ``None``.
        autopilot: When ``True`` (default) and ``interactive=True``, the
            standalone binary receives ``--autopilot`` so that the agent
            executes tasks autonomously without requiring the user to press
            Tab.  Has no effect for non-interactive mode.  When the
            ``gh copilot`` extension fallback is used and both
            ``interactive=True`` and ``autopilot=True``, a warning is
            emitted because the fallback does not support ``--autopilot``.
        allow_all: When ``True`` (default) interactive sessions receive
            ``--allow-all`` so the session runs without the interactive
            "Enable all permissions" confirmation prompt.  Pass ``False`` to
            restore prompting.  Non-interactive standalone-binary sessions
            always receive ``--allow-all``; the ``gh copilot suggest``
            fallback does not support the flag and omits it regardless of
            this setting.
        model: Optional Copilot model ID (e.g. ``"gpt-4o"``).
            Forwarded to ``_build_copilot_args`` and persisted as
            ``copilot.model_id`` in state.

    Returns:
        A :class:`CopilotSessionResult` with session metadata.

    Raises:
        OSError: If the prompt file cannot be written to disk.
        CopilotChildAliveError: If the session must be aborted after spawning
            a child process and the child's exit cannot be confirmed.  Callers
            that hold an ownership claim (e.g. the delayed-fallback verifier)
            must **not** release or unmark the claim when catching this
            exception — the unconfirmed child may still be running and
            continues to hold the session mutex.
    """
    # --- Session mutex guard -------------------------------------------------
    # Prevent duplicate sessions for the same worktree by checking if a live
    # Copilot session already exists (FR-001).
    owner_pid = os.getpid()
    existing = _check_session_mutex(claim=True)
    if existing is not None:
        return CopilotSessionResult(
            session_id=existing.get("session_id", ""),
            mode=existing.get("mode", ""),
            prompt_file=existing.get("prompt_file", ""),
            start_time=existing.get("start_time", ""),
            pid=existing.get("pid"),
            process=None,
        )

    # Pre-seed Copilot's trusted folders for the launch directory so the
    # interactive "Confirm folder trust" prompt does not block an auto-started
    # session.  Best-effort; no-ops in tests and when auto-trust is disabled.
    # Guard: only seed trust when the directory already exists on disk so that
    # a later Popen failure (invalid path) does not leave a stale entry in the
    # Copilot trustedFolders config.
    if os.path.isdir(working_directory):
        from .trust import seed_worktree_trust

        seed_worktree_trust(working_directory)

    if session_id is None:
        session_id = _make_session_id()

    # Normalise model: treat empty/whitespace-only strings as None so that
    # stdout, state, and argv all behave consistently.
    if isinstance(model, str):
        model = model.strip() or None

    start_time = datetime.now(UTC).isoformat()
    mode = "interactive" if interactive else "non-interactive"

    # --- Write prompt to temp file -------------------------------------------
    prompt_file_path = _get_prompt_file_path(session_id)
    prompt_file_path.parent.mkdir(parents=True, exist_ok=True)
    session_state_file_path = prompt_file_path.parent / "state.json"
    try:
        prompt_file_path.write_text(prompt, encoding="utf-8")
    except OSError:
        _release_session_mutex_claim(owner_pid)
        raise
    prompt_file = str(prompt_file_path)

    # --- Log model selection -------------------------------------------------
    if model:
        print(f"Copilot model: {model}")

    # --- Check availability --------------------------------------------------
    if not is_gh_copilot_available():
        warnings.warn(
            "gh copilot is not available; printing prompt to stdout as fallback.",
            stacklevel=2,
        )
        _print_fallback_prompt(prompt)
        result = CopilotSessionResult(
            session_id=session_id,
            mode=mode,
            prompt_file=prompt_file,
            start_time=start_time,
            pid=None,
            process=None,
        )
        _persist_session_state(result, model=model)
        return result

    # --- Build command -------------------------------------------------------
    # Inline the full prompt as a single line (newlines replaced with <br>
    # separators) for both interactive and non-interactive modes.  The file
    # on disk still contains the multi-line version for manual reuse.
    argv_prompt = _inline_prompt(prompt, prompt_file)
    args = _build_copilot_args(
        argv_prompt, interactive=interactive, autopilot=autopilot, allow_all=allow_all, model=model
    )

    # When the prompt is too large for safe argv passing, fall back to
    # printing the prompt.  This applies regardless of binary variant.
    if args is None:
        warnings.warn(
            "Prompt too large for copilot argv; printing prompt to stdout as fallback.",
            stacklevel=2,
        )
        _print_fallback_prompt(prompt)
        result = CopilotSessionResult(
            session_id=session_id,
            mode=mode,
            prompt_file=prompt_file,
            start_time=start_time,
            pid=None,
            process=None,
        )
        _persist_session_state(result, model=model)
        return result

    # --- Launch process -------------------------------------------------------
    if interactive:
        # Inherit stdio so the user can interact with the session.
        # This call blocks until the interactive session ends.
        # shell=False is required: gh is a proper .exe (not a .cmd batch script),
        # and the argument list contains a file path derived from user-supplied
        # prompt content; shell=True on Windows would allow cmd.exe to expand
        # %VAR% patterns inside those values.
        # Strip NODE_OPTIONS: on some systems it contains flags such as
        # ``--no-warnings`` that are intended for Node.js but are forwarded as
        # CLI arguments to the copilot binary, causing repeated
        # "error: unknown option '--no-warnings'" messages.
        env = {k: v for k, v in os.environ.items() if k != "NODE_OPTIONS"}
        try:
            process = subprocess.Popen(
                args,
                cwd=working_directory,
                shell=False,
                env=env,
            )
        except OSError:
            _release_session_mutex_claim(owner_pid)
            raise
        # Persist running PID before wait() so the session mutex can block
        # concurrent interactive starts while this foreground session is active.
        running_state = CopilotSessionResult(
            session_id=session_id,
            mode=mode,
            prompt_file=prompt_file,
            start_time=start_time,
            pid=process.pid,
            process=process,
        )
        _persist_session_state(running_state, model=model)
        process.wait()
        result = CopilotSessionResult(
            session_id=session_id,
            mode=mode,
            prompt_file=prompt_file,
            start_time=start_time,
            pid=None,  # process has already exited; PID not meaningful
            process=None,
        )
    else:
        # Non-interactive: run as background process, tee output to both the
        # log file AND the current process's stdout so that CI/pipeline systems
        # (e.g., Azure DevOps) capture the detailed Copilot output in their
        # build logs in addition to the persistent log file.
        log_file_path = _get_log_file_path(session_id, start_time)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Structured JSON Lines log alongside the human-readable log.
        jsonl_file_path = _get_jsonl_file_path(session_id, start_time)

        # Strip NODE_OPTIONS from the subprocess environment: on some systems
        # NODE_OPTIONS contains flags such as ``--no-warnings`` that are
        # intended for the Node.js runtime but are forwarded as CLI arguments
        # to the copilot binary, producing repeated
        # "error: unknown option '--no-warnings'" entries in the session log.
        env = {k: v for k, v in os.environ.items() if k != "NODE_OPTIONS"}
        try:
            process = subprocess.Popen(
                args,
                cwd=working_directory,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                start_new_session=True if sys.platform != "win32" else False,
                shell=False,
                env=env,
            )
        except OSError:
            _release_session_mutex_claim(owner_pid)
            raise

        log_fh: IO[str] | None = None
        jsonl_fh: IO[str] | None = None

        def _has_confirmed_process_exit(process_to_cleanup: subprocess.Popen[bytes]) -> bool:
            """Return whether *process_to_cleanup* has an observed terminal exit."""
            return isinstance(getattr(process_to_cleanup, "returncode", None), int)

        def _terminate_process_tree(process_to_cleanup: subprocess.Popen[bytes]) -> None:
            """Best-effort terminate *process_to_cleanup* and its descendants."""
            if sys.platform == "win32":
                try:
                    result = subprocess.run(
                        ["taskkill", "/PID", str(process_to_cleanup.pid), "/T", "/F"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        check=False,
                        shell=False,
                        timeout=5,
                    )
                    if result.returncode != 0:
                        with suppress(OSError, ValueError):
                            process_to_cleanup.kill()
                except (OSError, subprocess.TimeoutExpired):
                    with suppress(OSError, ValueError):
                        process_to_cleanup.kill()
            else:
                try:
                    os.killpg(process_to_cleanup.pid, signal.SIGKILL)  # type: ignore[attr-defined]
                except (AttributeError, ProcessLookupError, PermissionError, OSError):
                    with suppress(OSError, ValueError):
                        process_to_cleanup.kill()

        def _confirm_process_tree_exit(process_to_cleanup: subprocess.Popen[bytes]) -> bool:
            """Drain *process_to_cleanup* and confirm its process tree has exited."""
            try:
                process_to_cleanup.communicate(timeout=0.5)
                return True
            except (AttributeError, OSError, ValueError, subprocess.TimeoutExpired):
                return _has_confirmed_process_exit(process_to_cleanup)

        def _abort_noninteractive_startup(mutex_owner_pid: int, secondary_owner_pid: int | None = None) -> bool:
            """Terminate a just-started child when ownership setup fails.

            Returns ``True`` when the child process tree is confirmed to have
            exited and the mutex claim has been released.  Returns ``False``
            when exit cannot be confirmed; in that case the mutex claim is
            *retained* (so the live child continues to block new sessions)
            and a warning is printed to *stderr*.

            Callers that catch the resulting exception should propagate the
            unconfirmed-exit outcome via :class:`CopilotChildAliveError`.
            """
            exit_confirmed = False
            try:
                _terminate_process_tree(process)
                exit_confirmed = _confirm_process_tree_exit(process)
            finally:
                with suppress(AttributeError, OSError, ValueError):
                    process.stdout.close()  # type: ignore[union-attr]
                if log_fh is not None:
                    with suppress(AttributeError, OSError, ValueError):
                        log_fh.close()
                if jsonl_fh is not None:
                    with suppress(AttributeError, OSError, ValueError):
                        jsonl_fh.close()
                if exit_confirmed:
                    _release_session_mutex_claim(mutex_owner_pid, state_file_path=session_state_file_path)
                    if secondary_owner_pid is not None and secondary_owner_pid != mutex_owner_pid:
                        _release_session_mutex_claim(
                            secondary_owner_pid,
                            state_file_path=session_state_file_path,
                        )
                else:
                    print(
                        "Warning: could not confirm Copilot startup-abort process-tree exit; "
                        f"retaining mutex claim for pid {process.pid}.",
                        file=sys.stderr,
                    )
            return exit_confirmed

        # Transfer the mutex claim to the child so its PID guards the mutex
        # even if the launcher exits before startup completes.  Do not
        # continue when the transfer cannot be confirmed.
        if not _transfer_session_mutex_claim(owner_pid, process.pid):
            if not _abort_noninteractive_startup(owner_pid, process.pid):
                raise CopilotChildAliveError("Could not transfer the session mutex claim to the Copilot child.")
            raise RuntimeError("Could not transfer the session mutex claim to the Copilot child.")

        result = CopilotSessionResult(
            session_id=session_id,
            mode=mode,
            prompt_file=prompt_file,
            start_time=start_time,
            pid=process.pid,
            process=process,
            log_file=str(log_file_path),
        )
        try:
            _persist_session_state(result, model=model)
        except Exception as exc:
            if not _abort_noninteractive_startup(owner_pid, process.pid):
                retry_transfer_succeeded = _transfer_session_mutex_claim(owner_pid, process.pid)
                if not retry_transfer_succeeded:
                    print(
                        "Warning: could not persist child mutex claim after startup-abort "
                        f"verification failure; launcher pid {owner_pid} may remain recorded "
                        f"while child pid {process.pid} is still running.",
                        file=sys.stderr,
                    )
                raise CopilotChildAliveError(str(exc)) from exc
            raise

        # Open log files without a context manager; the tee thread closes
        # them after the subprocess pipe reaches EOF.
        # shell=False: same reasoning as the interactive case above.
        try:
            log_fh = open(log_file_path, "w", encoding="utf-8", errors="replace")  # noqa: WPS515
            try:
                jsonl_fh = open(jsonl_file_path, "w", encoding="utf-8", errors="replace")  # noqa: WPS515
            except OSError:
                # JSONL logging is best-effort; a creation failure (e.g.
                # permissions, read-only FS) must not prevent the session
                # from starting — .log and stdout teeing still work.
                jsonl_fh = None
            stdout_ref = sys.stdout
        except Exception as exc:
            if not _abort_noninteractive_startup(owner_pid, process.pid):
                raise CopilotChildAliveError(str(exc)) from exc
            raise

        def _tee(
            pipe: IO[bytes] | None,
            log_file: IO[str],
            stdout: IO[str] | None,
            jsonl_file: IO[str] | None = None,
            tee_process: subprocess.Popen | None = None,  # type: ignore[type-arg]
        ) -> None:
            """Read from *pipe* and mirror every line to *log_file* and *stdout*.

            When *jsonl_file* is not ``None``, each line is also written as a
            structured JSON object to the ``.jsonl`` file, and a summary entry
            is appended at EOF.

            Structured lifecycle markers (``SESSION_START``, ``SESSION_HEARTBEAT``,
            ``SESSION_END``, ``SESSION_ERROR``) are emitted to the log file and
            stdout for non-interactive session diagnostics.

            Handles *pipe* or *stdout* being ``None`` gracefully, and
            continues draining to *log_file* if stdout writes fail.
            """
            tee_start = time.monotonic()
            line_count = 0
            bytes_read = 0
            last_heartbeat = tee_start
            rc = 0
            _child_waited = False
            try:
                # Emit SESSION_START before the early-return check so that
                # partial diagnostic data is captured even when the pipe is
                # None (degenerate case).
                _emit_log_marker(
                    log_file,
                    stdout,
                    "SESSION_START",
                    session_id=session_id,
                    pid=tee_process.pid if tee_process is not None else "",
                    model=model or "default",
                    prompt_length=len(prompt),
                    working_directory=working_directory,
                )

                if pipe is None:
                    # Even without a pipe, wait for the process and emit
                    # end/error markers so lifecycle logs are never left in an
                    # indeterminate state.
                    rc = tee_process.wait() if tee_process is not None else 0
                    _child_waited = True
                    if tee_process is not None:
                        _release_session_mutex_claim(
                            tee_process.pid,
                            state_file_path=session_state_file_path,
                        )
                    if rc != 0:
                        _emit_log_marker(
                            log_file,
                            stdout,
                            "SESSION_ERROR",
                            exit_code=rc,
                            pid=tee_process.pid if tee_process is not None else "",
                        )
                    elapsed_total = round(time.monotonic() - tee_start, 1)
                    _emit_log_marker(
                        log_file,
                        stdout,
                        "SESSION_END",
                        exit_code=rc,
                        duration_seconds=elapsed_total,
                        total_bytes=0,
                        total_lines=0,
                    )
                    return

                stdout_ok = stdout is not None
                # Track JSONL health separately so a write failure (e.g.
                # disk full) doesn't abort the tee loop and starve the
                # .log / stdout sinks.
                jsonl_ok = jsonl_file is not None

                for raw_line in pipe:
                    line = raw_line.decode("utf-8", errors="replace")
                    log_file.write(line)
                    log_file.flush()

                    bytes_read += len(raw_line)
                    line_count += 1

                    # Activity-based heartbeat: emit when >= 60s since last.
                    # ``now_mono`` is intentionally reused below for the JSONL
                    # elapsed-time calculation to avoid a redundant monotonic()
                    # call per line.
                    now_mono = time.monotonic()
                    if now_mono - last_heartbeat >= _HEARTBEAT_INTERVAL_SECONDS:
                        elapsed = round(now_mono - tee_start, 1)
                        _emit_log_marker(
                            log_file,
                            stdout,
                            "SESSION_HEARTBEAT",
                            elapsed_seconds=elapsed,
                            bytes_read=bytes_read,
                            lines_read=line_count,
                        )
                        last_heartbeat = now_mono

                    if jsonl_ok:
                        try:
                            elapsed_ms = int((now_mono - tee_start) * 1000)
                            entry = {
                                "timestamp": datetime.now(tz=UTC).isoformat(),
                                "event_type": "output",
                                "content": line.rstrip("\r\n"),
                                "duration_ms": elapsed_ms,
                            }
                            jsonl_file.write(json.dumps(entry, ensure_ascii=False) + "\n")  # type: ignore[union-attr]
                            jsonl_file.flush()  # type: ignore[union-attr]
                        except (OSError, ValueError):
                            jsonl_ok = False

                    if stdout_ok:
                        try:
                            stdout.write(line)  # type: ignore[union-attr]
                            stdout.flush()  # type: ignore[union-attr]
                        except (OSError, ValueError):
                            # stdout closed/not writable (common in some CI runners).
                            # Stop mirroring but keep draining the pipe to the log.
                            stdout_ok = False

                # Collect exit code after the pipe is drained.
                rc = tee_process.wait() if tee_process is not None else 0
                _child_waited = True
                if tee_process is not None:
                    _release_session_mutex_claim(
                        tee_process.pid,
                        state_file_path=session_state_file_path,
                    )

                if rc != 0:
                    _emit_log_marker(
                        log_file,
                        stdout,
                        "SESSION_ERROR",
                        exit_code=rc,
                        pid=tee_process.pid if tee_process is not None else "",
                    )

                elapsed_total_unrounded = time.monotonic() - tee_start
                elapsed_total = round(elapsed_total_unrounded, 1)
                _emit_log_marker(
                    log_file,
                    stdout,
                    "SESSION_END",
                    exit_code=rc,
                    duration_seconds=elapsed_total,
                    total_bytes=bytes_read,
                    total_lines=line_count,
                )

                # Write summary entry at session end.
                if jsonl_ok:
                    try:
                        total_duration_ms = int(elapsed_total_unrounded * 1000)
                        summary = {
                            "timestamp": datetime.now(tz=UTC).isoformat(),
                            "event_type": "summary",
                            "content": "session_end",
                            "duration_ms": total_duration_ms,
                            "total_lines": line_count,
                        }
                        jsonl_file.write(json.dumps(summary, ensure_ascii=False) + "\n")  # type: ignore[union-attr]
                        jsonl_file.flush()  # type: ignore[union-attr]
                    except (OSError, ValueError):
                        pass
            finally:
                if not _child_waited and tee_process is not None:
                    exit_confirmed = _confirm_process_tree_exit(tee_process)
                    if not exit_confirmed:
                        _terminate_process_tree(tee_process)
                        exit_confirmed = _confirm_process_tree_exit(tee_process)
                    if exit_confirmed:
                        _release_session_mutex_claim(
                            tee_process.pid,
                            state_file_path=session_state_file_path,
                        )
                    else:
                        print(
                            "Warning: could not confirm Copilot tee-cleanup process-tree exit; "
                            f"retaining mutex claim for pid {tee_process.pid}.",
                            file=sys.stderr,
                        )
                log_file.close()
                if jsonl_file is not None:
                    jsonl_file.close()

        # daemon=False: the non-daemon thread keeps the parent process alive
        # until the subprocess finishes and its stdout pipe reaches EOF.  This
        # prevents SIGPIPE / broken-pipe in the child and ensures CI/pipeline
        # steps wait for the full Copilot session output.
        try:
            tee_thread = threading.Thread(
                target=_tee,
                args=(process.stdout, log_fh, stdout_ref, jsonl_fh, process),
                daemon=False,
            )
            tee_thread.start()
        except Exception as exc:
            if not _abort_noninteractive_startup(owner_pid, process.pid):
                raise CopilotChildAliveError(str(exc)) from exc
            raise

    if interactive:
        _persist_session_state(result, model=model)
    return result
