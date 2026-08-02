from __future__ import annotations

import logging
import os
import shutil
import subprocess
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Final
from typing import Literal
from typing import Optional

import structlog
from structlog.stdlib import BoundLogger
from structlog.stdlib import LoggerFactory
from structlog.types import EventDict

# Keys that are "internal implementation detail" and should not appear in final output.
_PRIVATE_KEYS: Final[tuple[str, ...]] = ("_fmt", "_rendered")


# ----------------------------
# Helpers: parsing + processors
# ----------------------------


def _parse_log_level(level_str: str | None) -> int:
    """
    Convert a string like "INFO" into a logging level int.

    Unknown/missing values default to INFO.
    """
    s = (level_str or "INFO").upper().strip()
    return logging._nameToLevel.get(s, logging.INFO)


def _render_fmt(_: Any, __: str, event_dict: EventDict) -> EventDict:
    """
    If `_fmt` is present, render it using `.format(**event_dict)` and store the
    result in `_rendered`.

    Example:
        log.info("startup", _fmt="Hello {user}", user="Ada")

    If formatting fails, we keep logging and include a helpful error in `_rendered`.
    """
    fmt = event_dict.get("_fmt")
    if not fmt:
        return event_dict

    try:
        event_dict["_rendered"] = str(fmt).format(**event_dict)
    except Exception as e:
        event_name = event_dict.get("event", "log")
        event_dict["_rendered"] = f"{event_name} (format_error={type(e).__name__}: {e})"
    return event_dict


def _drop_private_keys(_: Any, __: str, event_dict: EventDict) -> EventDict:
    """Remove internal keys such as `_fmt` and `_rendered` from the final output."""
    for k in _PRIVATE_KEYS:
        event_dict.pop(k, None)
    return event_dict


def _humanize_event(_: Any, __: str, event_dict: EventDict) -> EventDict:
    """
    Human output behavior:

    - If `_rendered` exists, replace `event` with the rendered human message.
    - Preserve the original event name in `_event_original` for debugging.
    """
    rendered = event_dict.pop("_rendered", None)
    if rendered is None:
        return event_dict

    event_dict.setdefault("_event_original", event_dict.get("event"))
    event_dict["event"] = rendered
    return event_dict


def _jsonify_event(_: Any, __: str, event_dict: EventDict) -> EventDict:
    """
    JSON output behavior:

    - Keep the structured `event` name untouched (useful for querying).
    - If `_rendered` exists, store it as `msg` for human readability.
    """
    rendered = event_dict.pop("_rendered", None)
    if rendered is None:
        return event_dict

    event_dict.setdefault("msg", rendered)
    return event_dict


# ----------------------------
# Speech support (optional)
# ----------------------------


def _which(cmd: str) -> bool:
    """Return True if `cmd` exists on PATH."""
    return shutil.which(cmd) is not None


def _default_speak_command() -> list[str] | None:
    """
    Pick a reasonable default speech command for the current OS.

    - macOS: `say`
    - Linux: `espeak` (if installed)
    - Windows: PowerShell SAPI (best-effort)
    """
    if sys.platform == "darwin" and _which("say"):
        return ["say"]
    if sys.platform.startswith("linux") and _which("espeak"):
        return ["espeak"]
    if sys.platform.startswith("win"):
        # Best-effort Windows SAPI via PowerShell.
        if _which("powershell") or _which("pwsh"):
            ps = "pwsh" if _which("pwsh") else "powershell"
            # We'll append the text argument later.
            return [
                ps,
                "-NoProfile",
                "-Command",
                "Add-Type -AssemblyName System.Speech; "
                "$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                "$speak.Speak($args[0]);",
            ]
    return None


@dataclass(frozen=True)
class SpeakConfig:
    """
    Controls the optional "speaking logs" feature.

    By default speaking is OFF. Enable with LOG_SPEAK=1.

    - enabled: whether speech is active
    - min_level: only speak events at or above this level (default ERROR)
    - cmd: speech command to run; if None we auto-detect
    """

    enabled: bool = field(
        default_factory=lambda: os.getenv("LOG_SPEAK", "0").lower() in ("1", "true", "yes", "on")
    )
    min_level: int = field(
        default_factory=lambda: _parse_log_level(os.getenv("LOG_SPEAK_LEVEL", "ERROR"))
    )
    cmd: str | None = field(default_factory=lambda: os.getenv("LOG_SPEAK_CMD"))


def speak(text: str, *, config: SpeakConfig | None = None) -> None:
    """
    Speak the given `text` out loud (best-effort, optional).

    This is intentionally safe:
    - If speech is disabled, does nothing.
    - If the platform has no speech engine installed, does nothing.
    - If the command fails, it does not crash your program.

    Usage:
        from enhanced_logging import speak
        speak("Deploy finished successfully!")

    Tip:
        It's often nicer to speak only errors:

        >>> speak("Database is down!", config=SpeakConfig(enabled=True, min_level=logging.ERROR))
    """
    cfg = config or SpeakConfig()
    if not cfg.enabled:
        return

    cmd: list[str] | None
    if cfg.cmd:
        # Allow override like: LOG_SPEAK_CMD="say"
        cmd = cfg.cmd.split()
    else:
        cmd = _default_speak_command()

    if not cmd:
        return

    try:
        subprocess.Popen(
            [*cmd, text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )  # noqa: S603,S607
    except Exception:
        # Never let speech crash your program.
        return


def _maybe_speak(_: Any, __: str, event_dict: EventDict) -> EventDict:
    """
    Structlog processor: speaks rendered/human message for high-severity events.

    It uses SpeakConfig from env vars. It's a no-op unless LOG_SPEAK=1.
    """
    cfg = SpeakConfig()
    if not cfg.enabled:
        return event_dict

    # Determine level from structlog's "level" field (e.g. "info", "error")
    level_name = str(event_dict.get("level", "")).upper()
    lvl = logging._nameToLevel.get(level_name, logging.INFO)
    if lvl < cfg.min_level:
        return event_dict

    # Prefer rendered message, else fall back to event.
    msg = event_dict.get("_rendered") or event_dict.get("event")
    if msg:
        speak(str(msg), config=cfg)
    return event_dict


# ----------------------------
# Main logging configuration
# ----------------------------

LogFormat = Literal["human", "json"]
CallsiteMode = Literal["auto", "0", "1", "false", "true", "no", "yes", "off", "on"]


@dataclass(frozen=True)
class LogConfig:
    """
    Configuration for logging.

    You can pass this explicitly to `configure_logging(LogConfig(...))`, or rely
    on environment variables.

    Fields:
        - format: "human" or "json" (env: LOG_FORMAT)
        - level: int logging level (env: LOG_LEVEL)
        - utc_timestamps: use UTC timestamps (env: LOG_UTC)
        - keep_existing_handlers: keep existing root handlers (env: LOG_KEEP_HANDLERS)
        - callsite: "auto" or force on/off (env: LOG_CALLSITE)
        - app_name: optional app name to bind into logs (env: LOG_APP_NAME)
    """

    format: LogFormat = field(
        default_factory=lambda: os.getenv("LOG_FORMAT", "human").lower().strip() or "human"
    )
    level: int = field(default_factory=lambda: _parse_log_level(os.getenv("LOG_LEVEL")))
    utc_timestamps: bool = field(
        default_factory=lambda: os.getenv("LOG_UTC", "1").lower() in ("1", "true", "yes", "on")
    )
    keep_existing_handlers: bool = field(
        default_factory=lambda: os.getenv("LOG_KEEP_HANDLERS", "0").lower()
        in ("1", "true", "yes", "on")
    )
    callsite: str = field(
        default_factory=lambda: os.getenv("LOG_CALLSITE", "auto").lower().strip() or "auto"
    )
    app_name: str = field(default_factory=lambda: os.getenv("LOG_APP_NAME", "").strip())

    def want_callsite(self) -> bool:
        """
        Decide whether to add filename/function/line fields.

        - If LOG_CALLSITE explicitly forces on/off, respect it.
        - Otherwise (auto), enable callsite for DEBUG and lower.
        """
        v = self.callsite
        if v in ("1", "true", "yes", "on"):
            return True
        if v in ("0", "false", "no", "off"):
            return False
        return self.level <= logging.DEBUG


_CONFIG: LogConfig | None = None


def _base_processors(cfg: LogConfig) -> list[Any]:
    """
    Processors applied to both human and json output.

    These add useful fields (timestamp, level), exception formatting, and `_fmt`
    rendering.
    """
    procs: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso", utc=cfg.utc_timestamps),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        _render_fmt,
        _maybe_speak,  # safe no-op unless LOG_SPEAK=1
    ]

    if cfg.want_callsite():
        procs.insert(
            2,
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                }
            ),
        )
    return procs


def configure_logging(config: LogConfig | None = None) -> None:
    """
    Configure stdlib logging + structlog.

    Call this once, early in your program (usually in the entry point under
    `if __name__ == "__main__":`).

    Typical usage:

        from enhanced_logging import configure_logging, get_logger

        def main():
            configure_logging()
            log = get_logger(__name__)
            log.info("startup", _fmt="Hello {who}", who="world")

        if __name__ == "__main__":
            main()

    Notes:
    - We configure the ROOT logger so libraries using `logging.getLogger(...)` will also emit through the same handler.
    - We ensure there is at least one StreamHandler writing to stdout.
    """
    global _CONFIG

    cfg = config or LogConfig()
    _CONFIG = cfg

    root = logging.getLogger()
    root.setLevel(cfg.level)

    if not cfg.keep_existing_handlers:
        root.handlers.clear()

    shared = _base_processors(cfg)

    if cfg.format == "json":
        formatter_processors = [
            structlog.processors.format_exc_info,
            _jsonify_event,
            _drop_private_keys,
            structlog.processors.JSONRenderer(),
        ]
    else:
        formatter_processors = [
            _humanize_event,
            _drop_private_keys,
            structlog.dev.ConsoleRenderer(),
        ]

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared,
        processors=formatter_processors,
        keep_exc_info=False,
        keep_stack_info=False,
    )

    if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(cfg.level)
        handler.setFormatter(formatter)
        root.addHandler(handler)
    else:
        for handler in root.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(cfg.level)
                handler.setFormatter(formatter)

    structlog.configure(
        processors=[
            *shared,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=LoggerFactory(),
        wrapper_class=BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None, **bind: Any) -> BoundLogger:
    """
    Get a structlog logger that follows the module configuration.

    - If logging was not configured yet, we auto-configure it with defaults. (This is convenient, but in larger apps you should still call `configure_logging()` explicitly at startup.)

    Parameters:
        - name: logger name (use `__name__` in most modules)
        - bind: extra fields to attach to every log call from this logger

    Example:

        log = get_logger(__name__, component="worker")
        log.info("job_started", job_id="abc123")
    """
    global _CONFIG
    if _CONFIG is None:
        configure_logging()

    assert _CONFIG is not None
    logger_name = name or __name__
    log = structlog.get_logger(logger_name)

    if _CONFIG.app_name:
        log = log.bind(app=_CONFIG.app_name)
    if bind:
        log = log.bind(**bind)
    return log


@contextmanager
def log_context(**fields: Any) -> Iterator[None]:
    """
    Temporarily bind context variables so that *all* logs inside the block
    automatically include them.

    This is great for request IDs, job IDs, or tenant names.

    Example:

        log = get_logger(__name__)

        with log_context(request_id="req-123", user_id=42):
            log.info("handling_request")
            do_work()
            log.info("done")

    The context fields are automatically removed when the block exits.
    """
    structlog.contextvars.bind_contextvars(**fields)
    try:
        yield
    finally:
        structlog.contextvars.unbind_contextvars(*fields.keys())
