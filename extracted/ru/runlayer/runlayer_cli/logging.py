"""Logging configuration for Runlayer CLI."""

import logging
import os
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import structlog

from runlayer_cli import __version__
from runlayer_cli.paths import get_runlayer_dir

DAILY_LOG_RETENTION_DAYS = 14
DAILY_LOG_TOTAL_CAP_BYTES = 100 * 1024 * 1024
SCHEDULED_TASK_LOG_MAX_BYTES = 10 * 1024 * 1024


def _log_file_name(command: str) -> str:
    """Generate log file name based on command and version."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    version_str = __version__.replace(".", "-")
    return f"runlayer-v{version_str}-{command}-{date_str}.log"


def _get_log_file_path(command: str) -> Path:
    """Generate log file path based on command and version."""
    log_dir = get_runlayer_dir() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / _log_file_name(command)


def _daily_log_date(path: Path) -> datetime | None:
    if not path.name.startswith("runlayer-v") or not path.name.endswith(".log"):
        return None
    stem_parts = path.name.removesuffix(".log").rsplit("-", maxsplit=3)
    if len(stem_parts) != 4 or stem_parts[0] == "runlayer-v":
        return None
    try:
        return datetime.strptime("-".join(stem_parts[1:]), "%Y-%m-%d")
    except ValueError:
        return None


def _sweep_daily_logs(log_dir: Path, protected_path: Path) -> None:
    """Best-effort retention for Runlayer's date-named log files."""
    try:
        paths = list(log_dir.iterdir())
    except OSError:
        return

    cutoff = datetime.now().date() - timedelta(days=DAILY_LOG_RETENTION_DAYS)
    candidates: list[tuple[datetime, str, Path, int]] = []
    for path in paths:
        log_date = _daily_log_date(path)
        if log_date is None:
            continue

        if log_date.date() < cutoff and path != protected_path:
            try:
                path.unlink()
                continue
            except OSError:
                pass

        try:
            size = path.stat().st_size
        except OSError:
            continue
        candidates.append((log_date, path.name, path, size))

    total_size = sum(candidate[3] for candidate in candidates)
    for _, _, path, size in sorted(candidates):
        if total_size <= DAILY_LOG_TOTAL_CAP_BYTES:
            break
        if path == protected_path:
            continue
        try:
            path.unlink()
        except OSError:
            continue
        total_size -= size


def _open_log_file_handler(command: str) -> tuple[logging.FileHandler, Path] | None:
    """Open the log file handler, falling back to a temp dir when ~/.runlayer
    isn't writable (e.g. root-owned after a sudo run). Logging must never abort
    the command, so a total failure returns None instead of raising."""
    for get_path in (
        lambda: _get_log_file_path(command),
        lambda: _temp_log_file_path(command),
    ):
        try:
            path = get_path()
            _sweep_daily_logs(path.parent, protected_path=path)
            return logging.FileHandler(path, mode="a", encoding="utf-8"), path
        except OSError:
            continue
    return None


def _temp_log_file_path(command: str) -> Path:
    log_dir = Path(tempfile.gettempdir()) / "runlayer-logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / _log_file_name(command)


def get_log_file_path(command: str) -> Path:
    """Get the log file path for a command."""
    return _get_log_file_path(command)


def _get_log_level() -> int:
    """Get log level from environment variable, defaulting to INFO."""
    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    return getattr(logging, level_name, logging.INFO)


# Operator-facing log for the Windows SYSTEM ``AIWatchScan`` task. SYSTEM's
# ``~/.runlayer`` resolves to the systemprofile tree (invisible to operators),
# so the all-users orchestrator mirrors its full (parent) process log output
# here — the orchestrator summary + per-profile result lines plus any setup /
# error output — the path the deploy docs point operators at. SYSTEM can write
# it.
SCHEDULED_TASK_LOG_PATH = Path(r"C:\ProgramData\Runlayer\Logs\scheduled-task.log")


def _rotate_scheduled_task_log_if_needed(path: Path) -> None:
    """Best-effort single-backup rotation before the shared log is opened."""
    try:
        if path.stat().st_size > SCHEDULED_TASK_LOG_MAX_BYTES:
            path.replace(path.with_name(f"{path.name}.1"))
    except OSError:
        pass


def _shared_processors() -> list[structlog.types.Processor]:
    """structlog processors shared by every handler's formatter."""
    return [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]


def _build_formatter() -> structlog.stdlib.ProcessorFormatter:
    """The plain (no-color) console formatter used for file + stderr output."""
    return structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=_shared_processors(),
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(
                colors=False, exception_formatter=structlog.dev.plain_traceback
            ),
        ],
    )


def attach_system_scan_log_handler() -> Path | None:
    """Mirror this (parent) process's full log output to the scheduled-task log.

    The ``AIWatchScan`` task runs ``aiwatch scan --all-users`` as SYSTEM. The
    orchestrator summary (``all_users_scan_complete``) + per-profile result
    lines (``all_users_profile_scan_*``) are emitted in this parent process, and
    SYSTEM's per-user log dir lives under ``systemprofile`` where operators never
    look. So attach an extra handler to the *root* logger — it mirrors the whole
    orchestrator process (those orchestrator lines plus any setup / error
    output), not a filtered subset — appending to
    ``C:\\ProgramData\\Runlayer\\Logs\\scheduled-task.log`` (writable by SYSTEM;
    the path the deploy docs reference). Per-profile child scans run in their own
    processes and log under the systemprofile tree, not here.

    Best-effort: call it after ``setup_logging``. No-op off Windows, and a
    non-writable path is swallowed so logging can never abort the scan. Returns
    the log path when attached, else ``None``.
    """
    if sys.platform != "win32":
        return None
    try:
        SCHEDULED_TASK_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        _rotate_scheduled_task_log_if_needed(SCHEDULED_TASK_LOG_PATH)
        handler = logging.FileHandler(
            SCHEDULED_TASK_LOG_PATH, mode="a", encoding="utf-8"
        )
        handler.setLevel(_get_log_level())
        handler.setFormatter(_build_formatter())
        logging.root.addHandler(handler)
    except OSError:
        return None
    return SCHEDULED_TASK_LOG_PATH


def ensure_base_logging_configured() -> None:
    """Install a minimal stderr logger when structlog is otherwise unconfigured.

    Entrypoint paths that never reach a command handler (``--version``,
    ``--help``, bare / invalid invocations) never call ``setup_logging``, so
    structlog falls back to its default ``PrintLogger`` (stdout, no level
    filtering) and every level — including ``debug`` — leaks to the console.
    This idempotently installs a ``LOG_LEVEL``-filtered (default INFO) bound
    logger rendering to **stderr**, so best-effort diagnostics such as the
    ``cli_command_metrics_skipped`` debug line stay silent by default and never
    touch stdout (the ``runlayer run`` stdio protocol channel).

    No-op once anything (``setup_logging``, ``silence_hook_logging``) has already
    configured structlog. No disk I/O — safe on the universal command wrapper.
    Uses the pure-structlog processors + ``PrintLoggerFactory`` (not the stdlib
    logger factory ``setup_logging`` wires up).

    ``cache_logger_on_first_use`` is left ``False`` so an already-created
    module-level logger (e.g. ``command_metrics``'s) re-binds against this config
    on its next call rather than caching a prior sink — same rationale as
    ``hook.log_silence.silence_hook_logging``.
    """
    if structlog.is_configured():
        return
    log_level = _get_log_level()
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer(
                colors=False, exception_formatter=structlog.dev.plain_traceback
            ),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=False,
    )


def setup_logging(command: str, quiet_console: bool = False) -> Path:
    """
    Setup logging for the CLI.

    Args:
        command: Command name (e.g., "run", "deploy")
        quiet_console: If True, suppress all console output (for stdio protocols)

    Returns:
        Path to the log file

    Environment Variables:
        LOG_LEVEL: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                   Defaults to INFO.
    """

    log_level = _get_log_level()

    # Configure stdlib logging handlers. File logging is best-effort: the
    # command must still run when no log location is writable.
    handlers: list[logging.Handler] = []
    file_handler_result = _open_log_file_handler(command)
    if file_handler_result is not None:
        file_handler, log_file_path = file_handler_result
        file_handler.setLevel(log_level)
        handlers.append(file_handler)
    else:
        log_file_path = get_runlayer_dir() / "logs" / _log_file_name(command)

    if not quiet_console:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(log_level)
        handlers.append(console_handler)

    logging.basicConfig(
        format="%(message)s",
        level=log_level,
        handlers=handlers,
        force=True,
    )

    # Suppress noisy HTTP request logs from httpx
    logging.getLogger("httpx").setLevel(logging.WARNING)

    structlog.configure(
        processors=_shared_processors()
        + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Set formatter on all handlers
    formatter = _build_formatter()
    for handler in logging.root.handlers:
        handler.setFormatter(formatter)

    if file_handler_result is None:
        # No handlers at all: this would reach stderr via logging.lastResort,
        # so honor quiet_console (stdio protocol sessions) and stay silent.
        if not quiet_console:
            structlog.get_logger(__name__).warning(
                "file_logging_disabled", reason="no writable log location"
            )
    elif log_file_path.parent != get_runlayer_dir() / "logs":
        structlog.get_logger(__name__).warning(
            "log_dir_not_writable_using_fallback", log_file=str(log_file_path)
        )

    return log_file_path
