"""
cvc.core.logging — CVC-native logging setup (Phase 1A native port).

Provides a single :func:`setup_logging` entry point that the CVC CLI and
gateway call early in their startup path. Mirrors the behavior of the
vendored logging module but depends only on the Python stdlib
+ :mod:`cvc.core.time` + :mod:`cvc.core.utils`.

Log files (under ``$CVC_HOME/logs/`` or ``~/.cvc/logs/``):

    agent.log    — INFO+, all CVC/tool/session activity (main log)
    errors.log   — WARNING+, errors and warnings only (quick triage)
    gateway.log  — INFO+, gateway-only events (when ``mode="gateway"``)

All files use :class:`logging.handlers.RotatingFileHandler` with the
redacting formatter so secrets are never written to disk.

Component separation: ``gateway.log`` only receives records whose logger
name starts with one of the ``COMPONENT_PREFIXES['gateway']`` prefixes;
``agent.log`` is the catch-all.

Session context: call :func:`set_session_context` at the start of a
conversation and :func:`clear_session_context` when done.  All log lines
emitted on that thread will include ``[session_id]`` for filtering.
"""

from __future__ import annotations

import logging
import os
import re
import threading
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Sequence

__all__ = [
    "setup_logging",
    "setup_verbose_logging",
    "set_session_context",
    "clear_session_context",
    "COMPONENT_PREFIXES",
    "get_cvc_home",
    "RedactingFormatter",
]


# ---------------------------------------------------------------------------
# CVC home resolution (mirrors the bridge module behaviour)
# ---------------------------------------------------------------------------

def get_cvc_home() -> Path:
    """Return CVC's home directory, honouring ``$CVC_HOME``/``$HERMES_HOME``.

    Resolution order:
        1. ``$CVC_HOME`` env var
        2. ``$HERMES_HOME`` env var (legacy compatibility)
        3. ``~/.cvc`` (default)

    The directory is created if missing.
    """
    val = (
        os.environ.get("CVC_HOME")
        or os.environ.get("HERMES_HOME")
        or os.path.expanduser("~/.cvc")
    ).strip()
    home = Path(val).expanduser()
    home.mkdir(parents=True, exist_ok=True)
    return home


# ---------------------------------------------------------------------------
# Session context
# ---------------------------------------------------------------------------

_session_context = threading.local()

_SID_RE = re.compile(r"[^A-Za-z0-9._-]")


def _safe_sid(sid: str) -> str:
    """Sanitize a session id for log-line inclusion (defense in depth)."""
    return _SID_RE.sub("_", sid)[:64] if sid else ""


def set_session_context(session_id: str) -> None:
    """Tag the current thread's log records with ``[session_id]``."""
    _session_context.session_id = _safe_sid(session_id)


def clear_session_context() -> None:
    """Drop the session tag for the current thread."""
    _session_context.session_id = None


# ---------------------------------------------------------------------------
# Record factory
# ---------------------------------------------------------------------------

_FACTORY_INSTALLED_ATTR = "_cvc_session_injector"


def _install_session_record_factory() -> None:
    """Install a LogRecord factory that injects ``session_tag`` on every record."""
    current = logging.getLogRecordFactory()
    if getattr(current, _FACTORY_INSTALLED_ATTR, False):
        return

    def _factory(*args, **kwargs):
        record = current(*args, **kwargs)
        sid = getattr(_session_context, "session_id", None)
        record.session_tag = f" [{sid}]" if sid else ""  # type: ignore[attr-defined]
        return record

    setattr(_factory, _FACTORY_INSTALLED_ATTR, True)
    logging.setLogRecordFactory(_factory)


# Install immediately on import — session_tag is available on all records
# from this point forward, even before setup_logging() is called.
_install_session_record_factory()


# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------

class _ComponentFilter(logging.Filter):
    """Only pass records whose logger name starts with one of *prefixes*."""

    def __init__(self, prefixes: Sequence[str]) -> None:
        super().__init__()
        self._prefixes = tuple(prefixes)

    def filter(self, record: logging.LogRecord) -> bool:
        return record.name.startswith(self._prefixes)


COMPONENT_PREFIXES = {
    "gateway": ("gateway", "cvc.gateway"),
    "agent": ("cvc.agent", "run_agent", "model_tools", "batch_runner"),
    "tools": ("cvc.tools", "tools"),
    "cli": ("cvc.cli", "cli"),
    "cron": ("cvc.cron", "cron"),
}


# ---------------------------------------------------------------------------
# Redacting formatter
# ---------------------------------------------------------------------------

# Patterns we always redact. Conservative — better to over-redact than leak.
_REDACT_PATTERNS = [
    re.compile(r"(?i)(sk-[A-Za-z0-9_-]{20,})"),                  # OpenAI-style keys
    re.compile(r"(?i)(anthropic-[A-Za-z0-9_-]{20,})"),           # Anthropic API keys
    re.compile(r"(?i)(sk-ant-[A-Za-z0-9_-]{20,})"),
    re.compile(r"(?i)(ghp_[A-Za-z0-9]{30,})"),                    # GitHub PAT
    re.compile(r"(?i)(xai-[A-Za-z0-9]{20,})"),                   # xAI keys
    re.compile(r"(?i)(AIza[0-9A-Za-z_-]{30,})"),                 # Google API keys
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]+"),                 # Bearer tokens
    re.compile(r"(?i)(api[_-]?key[\"'=:\s]+)([A-Za-z0-9._\-]{8,})"),
    re.compile(r"(?i)(token[\"'=:\s]+)([A-Za-z0-9._\-]{8,})"),
    re.compile(r"(?i)(password[\"'=:\s]+)([^\s\"']{4,})"),
    re.compile(r"(?i)(secret[\"'=:\s]+)([A-Za-z0-9._\-]{8,})"),
]


class RedactingFormatter(logging.Formatter):
    """Formatter that scrubs well-known secret patterns from log messages.

    Defensive — applied to the formatted string, not just the raw message,
    so it covers any extras that may have been added by handlers/filters.
    """

    def __init__(self, fmt: str, *args, **kwargs) -> None:
        super().__init__(fmt, *args, **kwargs)
        self._patterns = tuple(_REDACT_PATTERNS)

    def format(self, record: logging.LogRecord) -> str:
        text = super().format(record)
        for pat in self._patterns:
            text = pat.sub("[REDACTED]", text)
        return text


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

_LOG_FORMAT = "%(asctime)s %(levelname)s%(session_tag)s %(name)s: %(message)s"
_LOG_FORMAT_VERBOSE = "%(asctime)s - %(name)s - %(levelname)s%(session_tag)s - %(message)s"

_NOISY_LOGGERS = (
    "openai",
    "openai._base_client",
    "httpx",
    "httpcore",
    "asyncio",
    "hpack",
    "hpack.hpack",
    "grpc",
    "modal",
    "urllib3",
    "urllib3.connectionpool",
    "websockets",
    "charset_normalizer",
    "markdown_it",
)

_logging_initialized = False


def _add_rotating_handler(
    logger: logging.Logger,
    path: Path,
    *,
    level: int,
    max_bytes: int,
    backup_count: int,
    formatter: logging.Formatter,
    log_filter: Optional[logging.Filter] = None,
) -> None:
    """Attach a :class:`RotatingFileHandler` to *logger* (idempotent)."""
    resolved = path.resolve()
    for existing in logger.handlers:
        if (
            isinstance(existing, RotatingFileHandler)
            and Path(getattr(existing, "baseFilename", "")).resolve() == resolved
        ):
            return  # already attached

    path.parent.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(
        str(path), maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8",
    )
    handler.setLevel(level)
    handler.setFormatter(formatter)
    if log_filter is not None:
        handler.addFilter(log_filter)
    logger.addHandler(handler)


def _read_logging_config() -> tuple[Optional[str], Optional[int], Optional[int]]:
    """Best-effort read of ``logging.*`` from ``$CVC_HOME/config.yaml``."""
    try:
        from cvc.core.utils import safe_json_loads  # noqa: F401  (unused; placeholder)
        import yaml  # local import — config may not be loaded yet
        config_path = get_cvc_home() / "config.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            log_cfg = cfg.get("logging", {})
            if isinstance(log_cfg, dict):
                return (
                    log_cfg.get("level"),
                    log_cfg.get("max_size_mb"),
                    log_cfg.get("backup_count"),
                )
    except Exception:
        pass
    return (None, None, None)


def setup_logging(
    *,
    cvc_home: Optional[Path] = None,
    log_level: Optional[str] = None,
    max_size_mb: Optional[int] = None,
    backup_count: Optional[int] = None,
    mode: Optional[str] = None,
    force: bool = False,
) -> Path:
    """Configure the CVC logging subsystem.

    Safe to call multiple times — the second call is a no-op unless
    *force* is ``True``.

    Parameters
    ----------
    cvc_home
        Override for CVC's home directory. Falls back to :func:`get_cvc_home`.
    log_level
        Minimum level for ``agent.log``. Accepts ``"DEBUG"``, ``"INFO"``,
        ``"WARNING"``, etc. Defaults to ``"INFO"`` or ``logging.level``
        from ``config.yaml``.
    max_size_mb
        Max size of each log file in MB before rotation. Defaults to 5.
    backup_count
        Number of rotated backup files to keep. Defaults to 3.
    mode
        Caller context — ``"cli"``, ``"gateway"``, ``"cron"``. When
        ``"gateway"``, an additional ``gateway.log`` file is created that
        receives only gateway-component records.
    force
        Re-run setup even if it has already been called.

    Returns
    -------
    Path
        The ``logs/`` directory where files are written.
    """
    global _logging_initialized
    home = cvc_home or get_cvc_home()
    log_dir = home / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    cfg_level, cfg_max_size, cfg_backup = _read_logging_config()

    level_name = (log_level or cfg_level or "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    max_bytes = (max_size_mb or cfg_max_size or 5) * 1024 * 1024
    backups = backup_count or cfg_backup or 3

    root = logging.getLogger()

    # --- agent.log (INFO+) — main activity log -----------------------------
    _add_rotating_handler(
        root,
        log_dir / "agent.log",
        level=level,
        max_bytes=max_bytes,
        backup_count=backups,
        formatter=RedactingFormatter(_LOG_FORMAT),
    )

    # --- errors.log (WARNING+) — quick triage log --------------------------
    _add_rotating_handler(
        root,
        log_dir / "errors.log",
        level=logging.WARNING,
        max_bytes=2 * 1024 * 1024,
        backup_count=2,
        formatter=RedactingFormatter(_LOG_FORMAT),
    )

    # --- gateway.log (INFO+, gateway component only) -----------------------
    if mode == "gateway":
        _add_rotating_handler(
            root,
            log_dir / "gateway.log",
            level=logging.INFO,
            max_bytes=5 * 1024 * 1024,
            backup_count=3,
            formatter=RedactingFormatter(_LOG_FORMAT),
            log_filter=_ComponentFilter(COMPONENT_PREFIXES["gateway"]),
        )

    if _logging_initialized and not force:
        return log_dir

    # Ensure root logger level is low enough for the handlers to fire.
    if root.level == logging.NOTSET or root.level > level:
        root.setLevel(level)

    # Suppress noisy third-party loggers.
    for name in _NOISY_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)

    _logging_initialized = True
    return log_dir


def setup_verbose_logging() -> None:
    """Enable DEBUG-level console logging for ``--verbose`` / ``-v`` mode."""
    root = logging.getLogger()

    # Avoid adding duplicate stream handlers.
    for h in root.handlers:
        if isinstance(h, logging.StreamHandler) and not isinstance(h, RotatingFileHandler):
            if getattr(h, "_cvc_verbose", False):
                return

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(RedactingFormatter(_LOG_FORMAT_VERBOSE, datefmt="%H:%M:%S"))
    handler._cvc_verbose = True  # type: ignore[attr-defined]
    root.addHandler(handler)

    # Lower root logger level so DEBUG records reach all handlers.
    if root.level > logging.DEBUG:
        root.setLevel(logging.DEBUG)

    # Keep third-party libraries at WARNING to reduce noise.
    for name in _NOISY_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)
    logging.getLogger("rex-deploy").setLevel(logging.INFO)
