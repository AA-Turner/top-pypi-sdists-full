"""notice the CLI reinstalled under the worker, or its AI libraries missing, and leave with the right code."""

from __future__ import annotations
import os
from probe import analytics as telemetry
from pathlib import Path
from probe.daemon.trace import trace as trace_mod
#: How often the missing-libraries line reaches `daemon-errors.log` per session:
#: a supervisor that retries would otherwise add one every few minutes.
LIBS_MISSING_LOG_EVERY_S = 3600.0


_INSTALL_ROOT = Path(__file__).resolve().parents[2]


def install_root() -> Path:
    """The folder this worker's code was loaded from (`probe/`)."""
    return _INSTALL_ROOT


def _install_stamp() -> tuple[int, int] | None:
    """Which `probe/__init__.py` this is: `uv tool` writes it anew on a reinstall,
    with the install's time (its size and mtime, not its inode, which a network
    mount may change on its own)."""
    try:
        st = (install_root() / "__init__.py").stat()
    except OSError:
        return None
    return st.st_size, st.st_mtime_ns


def _dist_info() -> Path | None:
    """This version's `probe_research-<version>.dist-info` beside `probe/`, when the
    install has one there (`uv tool` does; an editable checkout does not)."""
    from probe import __version__

    path = install_root().parent / f"probe_research-{__version__}.dist-info"
    try:
        return path if path.is_dir() else None
    except OSError:
        return None


#: The install this worker started from.
_INSTALL_STAMP = _install_stamp()
_DIST_INFO = _dist_info()


def install_replaced() -> bool:
    """Was the CLI reinstalled under this worker? `uv tool` either moves its folder
    (a new Python: `lib/python3.13` -> `lib/python3.14`, the old one gone) or
    replaces its files where they are (`probe update`). Either way the worker's next
    read of its own files -- a skill, a prompt, a first import -- would fail or be
    the new version's. An unreadable folder (a stale network mount) is not a
    reinstall, and neither is an install whose `__init__.py` could not be read
    when the worker started (a zip or frozen build): nothing to compare. A new
    version also takes its `dist-info` folder's place, gone even where a file this
    worker reads was only renamed."""
    if _INSTALL_STAMP is None:
        return False
    try:
        if _DIST_INFO is not None:
            _DIST_INFO.stat()
        st = (install_root() / "__init__.py").stat()
    except (FileNotFoundError, NotADirectoryError):
        return True
    except OSError:
        return False
    return (st.st_size, st.st_mtime_ns) != _INSTALL_STAMP


def ai_libraries_importable() -> bool:
    """Both halves the daemon imports unconditionally, the pair
    `probe.cli.daemon_cli.ai_libraries` checks: a half-installed `daemon` extra
    must take the missing-libraries exit, not crash at a later import."""
    try:
        import pydantic_ai  # noqa: F401
        import pydantic_ai_harness  # noqa: F401
    except ImportError:
        return False
    return True


def libs_missing_exit_code() -> int:
    """How a worker without its AI libraries leaves: EXIT_RETRY_LIBS to a
    supervisor that retries (SUPERVISOR_RETRIES_LIBS_ENV), else
    EXIT_DO_NOT_RESPAWN, which an older tap holds until the switch moves."""
    return EXIT_RETRY_LIBS if os.environ.get(SUPERVISOR_RETRIES_LIBS_ENV) == "1" else EXIT_DO_NOT_RESPAWN


def _libs_missing_log_due(session_id: str) -> bool:
    """Whether this session's missing-libraries line is due in `daemon-errors.log`
    (at most once per LIBS_MISSING_LOG_EVERY_S): a stamp file, because each retry
    is a fresh process. It lives in the session's own folder, which `sweep_stale`
    deletes with the session."""
    directory = trace_mod.session_dir(session_id)
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError:
        return True
    return telemetry.report_due(str(directory), "libs-missing", interval_s=LIBS_MISSING_LOG_EVERY_S)
from probe.daemon.worker.supervisor import EXIT_DO_NOT_RESPAWN, EXIT_RETRY_LIBS, SUPERVISOR_RETRIES_LIBS_ENV  # noqa: E402 -- pieces need each other; the front door loads this one first
