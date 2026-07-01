from __future__ import annotations

import atexit
import platform
import sys
import threading
from collections.abc import Mapping
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Optional, Protocol, TypeVar, overload

from .config import load_config
from .db import setup_db
from .serialize import monkeypatch_queryset_repr

if TYPE_CHECKING:
    from .profiler import KoloProfiler

    if sys.version_info >= (3, 12):
        from .monitoring import KoloMonitor
    else:
        KoloMonitor = Any

logger = __import__("logging").getLogger("kolo")

# Throttling for auto-emit subprocess spawning
_auto_emit_lock = threading.Lock()
_auto_emit_last_spawn: float = 0.0
_AUTO_EMIT_COOLDOWN_SECONDS: float = 0.5  # Max one spawn per 500ms
_auto_emit_followup_timer: threading.Timer | None = None
_auto_emit_pending_db_paths: list[Path | None] = []

# Lock to prevent TOCTOU race condition during activation.
# Without this, two concurrent requests could both pass the _is_already_active()
# check before either claims the sys.monitoring tool ID, causing a ValueError.
_activation_lock = threading.Lock()


def save_trace_in_thread(
    profiler,
    auto_emit: bool = False,
    db_path: Path | None = None,
):
    def save_then_emit():
        profiler.save()
        # Spawn subprocess AFTER save completes, so the trace is in the DB
        if auto_emit:
            _spawn_auto_emit(db_path=db_path)

    if platform.machine() == "wasm32":  # pragma: no cover
        save_then_emit()
    else:
        name = "kolo-save_trace_in_db"
        # daemon=False explicitly: Thread inherits the parent's daemon flag
        # by default, so if kolo.enable() is called from a daemon thread, the
        # save thread would also be daemon and CPython would not wait for it
        # at interpreter shutdown, re-exposing the C-extension-teardown race.
        threading.Thread(target=save_then_emit, name=name, daemon=False).start()


def _build_emit_subprocess_kwargs(db_path: Path | None) -> dict[str, Any]:
    import os
    import subprocess

    env = os.environ.copy()
    # Use the system local timezone in the subprocess. Django often sets
    # TZ=UTC, which would otherwise leak into emitted folder timestamps.
    env.pop("TZ", None)
    # Prevent the auto-emit subprocess from tracing itself when KOLO=1 is set.
    # Belt-and-suspenders: disable tracing and remove activation triggers.
    env["KOLO_DISABLE"] = "1"
    env.pop("KOLO", None)

    # db_path is <parent>/.kolo/.internal/db.sqlite3, so KOLO_PATH is <parent>.
    if db_path is not None:
        env["KOLO_PATH"] = str(db_path.parent.parent.parent)

    popen_kwargs: dict[str, Any] = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "env": env,
    }

    if sys.platform == "win32":  # pragma: no cover
        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        popen_kwargs["creationflags"] = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    else:
        popen_kwargs["start_new_session"] = True
        popen_kwargs["close_fds"] = True

    return popen_kwargs


def _spawn_auto_emit_subprocess(db_path: Path | None) -> None:
    import subprocess

    try:
        subprocess.Popen(
            [sys.executable, "-m", "kolo._emit_auto"],
            **_build_emit_subprocess_kwargs(db_path),
        )
    except (OSError, ValueError) as e:
        logger.debug("Failed to spawn auto-emit subprocess: %s", e)


def _schedule_auto_emit_followup_locked(delay: float, db_path: Path | None) -> None:
    global _auto_emit_followup_timer

    if db_path not in _auto_emit_pending_db_paths:
        _auto_emit_pending_db_paths.append(db_path)

    if _auto_emit_followup_timer is not None and _auto_emit_followup_timer.is_alive():
        return

    timer = threading.Timer(delay, _run_auto_emit_followup)
    timer.name = "kolo-auto-emit-followup"
    # Do not inherit a daemon request thread here. A throttled follow-up still
    # needs to survive shutdown long enough to run or be flushed synchronously.
    timer.daemon = False
    _auto_emit_followup_timer = timer
    timer.start()


def _drain_auto_emit_followup_locked() -> list[Path | None]:
    global _auto_emit_followup_timer

    pending_db_paths = list(_auto_emit_pending_db_paths)
    _auto_emit_pending_db_paths.clear()
    _auto_emit_followup_timer = None
    return pending_db_paths


def _run_auto_emit_followup() -> None:
    import time

    global _auto_emit_last_spawn

    with _auto_emit_lock:
        pending_db_paths = _drain_auto_emit_followup_locked()
        if not pending_db_paths:
            return
        _auto_emit_last_spawn = time.monotonic()

    for db_path in pending_db_paths:
        _spawn_auto_emit_subprocess(db_path)


def _flush_auto_emit_followup_on_shutdown() -> None:
    timer: threading.Timer | None

    with _auto_emit_lock:
        timer = _auto_emit_followup_timer
        if timer is not None:
            timer.cancel()
        pending_db_paths = _drain_auto_emit_followup_locked()

    if timer is not None:
        timer.join()

    for db_path in pending_db_paths:
        _spawn_auto_emit_subprocess(db_path)


atexit.register(_flush_auto_emit_followup_on_shutdown)


def _spawn_auto_emit(db_path: Path | None = None) -> None:
    """
    Spawn a subprocess to auto-emit the latest traces.

    This runs `python -m kolo._emit_auto` in a completely separate process,
    ensuring zero impact on the Django process (no GIL, no shared memory).
    The subprocess is fire-and-forget - we don't wait for it to complete.

    Uses a lightweight entry point that avoids importing heavy dependencies
    (httpx, click, django) for faster subprocess startup.

    Throttled to max once per 500ms to prevent fork-bombing under high load.
    Cooldown hits schedule one trailing follow-up so a burst still gets a
    final reconciliation after the cooldown window closes.

    If db_path is provided, KOLO_PATH is set in the subprocess environment
    so setup_db() resolves to the same .kolo directory the trace was saved
    to (important when the caller passed an explicit _db_path override).
    """
    import time

    global _auto_emit_followup_timer, _auto_emit_last_spawn

    if platform.machine() == "wasm32":  # pragma: no cover
        from ._emit_auto import auto_emit

        try:
            auto_emit(db_path=db_path)
        except Exception:
            logger.debug("auto-emit failed", exc_info=True)
        return

    if not sys.executable:
        logger.debug(
            "Cannot spawn auto-emit: sys.executable is not set (embedded Python?)"
        )
        return

    db_paths_to_spawn = [db_path]

    with _auto_emit_lock:
        now = time.monotonic()
        elapsed = now - _auto_emit_last_spawn
        if elapsed < _AUTO_EMIT_COOLDOWN_SECONDS:
            logger.debug("Deferring auto-emit spawn: cooldown active")
            _schedule_auto_emit_followup_locked(
                _AUTO_EMIT_COOLDOWN_SECONDS - elapsed, db_path
            )
            return

        if _auto_emit_pending_db_paths:
            db_paths_to_spawn = list(_auto_emit_pending_db_paths)
            _auto_emit_pending_db_paths.clear()
            if db_path not in db_paths_to_spawn:
                db_paths_to_spawn.append(db_path)

        if _auto_emit_followup_timer is not None:
            _auto_emit_followup_timer.cancel()
            _auto_emit_followup_timer = None

        _auto_emit_last_spawn = now

    for pending_db_path in db_paths_to_spawn:
        _spawn_auto_emit_subprocess(pending_db_path)


def upload_trace_in_thread(profiler, upload_token):
    def upload():
        import httpx

        trace = profiler.build_trace()
        try:
            from .upload import upload_to_dashboard

            response = upload_to_dashboard(trace, upload_token)
            response.raise_for_status()
        except httpx.HTTPError:
            logger.exception("Failed to upload trace to Kolo dashboard.")

    if platform.machine() == "wasm32":  # pragma: no cover
        upload()
    else:
        name = "kolo-upload_to_dashboard"
        threading.Thread(target=upload, name=name).start()


class Enabled:
    """
    User-facing context manager and decorator for Kolo profiling.

    This class is used via kolo.enable() and can be used as:
    - Context manager: with kolo.enable(): ...
    - Decorator: @kolo.enable or @kolo.enable(config={...})

    For automatic .pth file activation, use _AutoEnabled instead.
    """

    def __init__(
        self,
        config: Mapping[str, Any] | None,
        source: str,
        one_trace_per_test: bool,
        save_in_thread: bool,
        upload_token: Optional[str],
        db_path: Optional[Path] = None,
        name: Optional[str] = None,
        inline: bool = False,
        inline_returns: bool = False,
    ):
        if config is None:
            config = {}
        self.config = load_config(config)
        self._profiler: Optional[KoloProfiler] = None
        self._monitor: Optional[KoloMonitor] = None
        self.source = source
        self.one_trace_per_test = one_trace_per_test
        self.save_in_thread = save_in_thread
        self.upload_token = upload_token
        self.db_path = db_path
        self.name = name
        self.trace_id: Optional[str] = None
        self.inline = inline
        self.inline_returns = inline_returns

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return inner

    def _is_already_active(self) -> bool:
        """
        Check if Kolo profiling/monitoring is already active.

        This checks multiple sources:
        - sys.monitoring (Python 3.12+)
        - sys.getprofile()
        - threading.getprofile() (Python < 3.12)

        Returns:
            True if profiling is active, False otherwise
        """
        # Default to monitoring on Python 3.12+
        default_use_monitoring = sys.version_info >= (3, 12)
        use_monitoring = self.config.get("use_monitoring", default_use_monitoring)

        if use_monitoring and sys.version_info >= (3, 12):
            from .monitoring import KOLO_TOOL_ID

            tool_name = sys.monitoring.get_tool(KOLO_TOOL_ID)  # type: ignore[attr-defined]
            if tool_name:
                if tool_name != "kolo":
                    logger.warning(
                        "Tool ID %d is in use by %r (expected 'kolo'). "
                        "Another tool may be using Kolo's reserved tool ID.",
                        KOLO_TOOL_ID,
                        tool_name,
                    )
                return True

        if sys.getprofile() is not None:
            return True

        # Check threading profile for Python < 3.12
        if sys.version_info < (3, 12) or not use_monitoring:
            try:
                thread_profiler = threading.getprofile()  # type: ignore[attr-defined]
            except AttributeError:
                thread_profiler = threading._profile_hook
            if thread_profiler:
                return True

        return False

    def _activate(self) -> bool:
        """
        Internal activation logic.

        Activates Kolo profiling/monitoring. If already active, logs a message
        and returns early.

        Uses a lock to prevent TOCTOU race conditions where two threads could
        both pass the _is_already_active() check before either claims the
        sys.monitoring tool ID.

        Returns:
            True if activation succeeded, False if already active or failed.
        """
        # Acquire lock to prevent race condition between check and activation.
        # This ensures only one thread can be in the activation window at a time.
        with _activation_lock:
            if self._is_already_active():
                logger.debug(
                    "Kolo already active, skipping duplicate activation from %s",
                    self.source,
                )
                return False

            # Resolve db_path once during activation so that _deactivate
            # and _output_inline_trace use the same path, even if cwd or
            # KOLO_PATH changes during tracing.  Stored in _active_db_path
            # (not self.db_path) so reused instances (e.g. @kolo.enable
            # decorator) re-resolve on each call. .resolve() turns
            # relative paths into absolute ones so they don't drift with
            # cwd changes mid-trace.
            if self.db_path is not None:
                self._active_db_path = self.db_path.resolve()
            else:
                self._active_db_path = setup_db()
            db_path = self._active_db_path

            monkeypatch_queryset_repr()

            # Default to monitoring on Python 3.12+
            default_use_monitoring = sys.version_info >= (3, 12)
            use_monitoring = self.config.get("use_monitoring", default_use_monitoring)
            if sys.version_info >= (3, 12) and use_monitoring:
                from .monitoring import activate_monitoring

                monitor = self.register_monitor(db_path)
                if activate_monitoring(monitor):
                    self._monitor = monitor
                    self.trace_id = monitor.trace_id
                else:
                    # Another profiler has claimed the tool ID; skip activation
                    return False
            else:
                from .profiler import KoloProfiler

                self._profiler = KoloProfiler(
                    db_path,
                    config=self.config,
                    source=self.source,
                    one_trace_per_test=self.one_trace_per_test,
                    name=self.name,
                )
                self._profiler.__enter__()
                self.trace_id = self._profiler.trace_id

            return True

    def __enter__(self):
        self._activate()
        return self

    def register_monitor(self, db_path):
        if self.config.get("use_rust", True):
            try:
                from ._kolo import register_monitor
            except ImportError as e:  # pragma: no cover
                # Rust extension not available (e.g. PyPy), fall back to pure Python
                logger.debug("Rust monitor import failed (%s), using Python monitor", e)
            else:
                return register_monitor(
                    str(db_path),
                    config=self.config,
                    source=self.source,
                    one_trace_per_test=self.one_trace_per_test,
                    name=self.name,
                )

        from .monitoring import KoloMonitor  # type: ignore[attr-defined]

        return KoloMonitor(
            db_path,
            config=self.config,
            source=self.source,
            one_trace_per_test=self.one_trace_per_test,
            name=self.name,
        )

    @property
    def _save_sync(self) -> bool:
        """Whether this Enabled instance should save synchronously.

        Inline output reads the trace by id from the db immediately after
        deactivation, so a background save would race against it and
        produce either a missing trace or TraceNotFoundError. We force
        synchronous save whenever the caller asked for inline output.
        """
        return not self.save_in_thread or self.inline

    def save_trace_profiler(self):
        assert self._profiler is not None

        if self.one_trace_per_test:
            return

        if self._save_sync:
            self._profiler.save()
            return

        if self.upload_token:
            upload_trace_in_thread(self._profiler, self.upload_token)
        else:
            auto_emit = self.config.get("auto_emit", True)
            save_trace_in_thread(
                self._profiler, auto_emit=auto_emit, db_path=self._active_db_path
            )

    def save_trace_monitor(self):
        assert self._monitor is not None

        if self.one_trace_per_test:
            return

        if self._save_sync:
            self._monitor.save()
            return

        if self.upload_token:
            upload_trace_in_thread(self._monitor, self.upload_token)
        else:
            auto_emit = self.config.get("auto_emit", True)
            save_trace_in_thread(
                self._monitor, auto_emit=auto_emit, db_path=self._active_db_path
            )

    def _deactivate(self, *exc) -> None:
        """
        Internal deactivation logic.

        Deactivates profiling/monitoring, saves traces, and handles inline output.
        """
        did_deactivate = False

        if self._profiler is not None:
            self._profiler.__exit__(*exc)
            self.save_trace_profiler()
            self._profiler = None
            did_deactivate = True

        if self._monitor is not None:
            from .monitoring import disable_monitoring  # type: ignore[attr-defined]

            disable_monitoring(self._monitor)
            self.save_trace_monitor()
            self._monitor = None
            did_deactivate = True

        if did_deactivate and self._save_sync:
            if self.config.get("auto_emit", True):
                _spawn_auto_emit(db_path=self._active_db_path)

        if self.inline:
            assert self.trace_id is not None
            self._output_inline_trace()

    def __exit__(self, *exc) -> None:
        self._deactivate(*exc)

    def _output_inline_trace(self):
        """Output the compact trace representation to stderr."""
        import click

        from .cli_mcp_shared import get_compact_traces

        assert self._active_db_path is not None
        db_path = self._active_db_path

        results = get_compact_traces(
            db_path,
            trace_id=self.trace_id,
            returns=self.inline_returns,
        )
        if results:
            trace_id, compact_repr = results[0]
            click.echo(compact_repr, err=True)


class _AutoEnabled:
    """
    Internal class for automatic .pth file activation.

    Not a context manager - uses explicit activate/cleanup methods.
    Designed for one-way activation with atexit cleanup.

    This class should only be used internally for KOLO=1 auto-activation.
    User code should use the Enabled context manager instead.
    """

    def __init__(
        self,
        config: Mapping[str, Any] | None,
        source: str,
        one_trace_per_test: bool,
        save_in_thread: bool,
        upload_token: Optional[str],
        db_path: Optional[Path] = None,
        name: Optional[str] = None,
        inline: bool = False,
        inline_returns: bool = False,
    ):
        # Create an Enabled instance internally
        self._enabled = Enabled(
            config=config,
            source=source,
            one_trace_per_test=one_trace_per_test,
            save_in_thread=save_in_thread,
            upload_token=upload_token,
            db_path=db_path,
            name=name,
            inline=inline,
            inline_returns=inline_returns,
        )
        self._activated = False
        self.trace_id: Optional[str] = None

    def activate(self) -> bool:
        """
        Activate Kolo profiling.

        Returns:
            True if activation succeeded, False if already active or failed
        """
        if self._enabled._is_already_active():
            logger.debug("KOLO=1: Tracing already active, skipping auto-activation")
            return False

        if not self._enabled._activate():
            # Activation failed (e.g., another tool claimed the ID)
            return False

        self._activated = True

        # Expose trace_id for external access
        self.trace_id = self._enabled.trace_id

        return True

    def cleanup(self) -> None:
        """
        Cleanup and save trace.

        Called by atexit handler. Includes error handling to prevent
        crashes during interpreter shutdown.
        """
        if not self._activated:
            return

        try:
            self._enabled._deactivate(None, None, None)
            if self._enabled.config.get("auto_emit", True):
                self._print_kolotxt_path()
        except Exception as e:  # pragma: no cover
            # Don't crash during shutdown - log to stderr
            import sys

            print(f"Kolo cleanup error during shutdown: {e}", file=sys.stderr)
            import traceback

            traceback.print_exc(file=sys.stderr)

    def _print_kolotxt_path(self):
        """
        Print the kolo.txt path to stderr.

        Note: kolo.txt is updated by the auto-emit subprocess spawned in
        _deactivate(). The file may not exist yet (subprocess is
        fire-and-forget), but it will be created shortly.
        """
        # _active_db_path is resolved during _activate() and always set
        assert self._enabled._active_db_path is not None
        kolotxt_path = self._enabled._active_db_path.parent.parent / "kolo.txt"
        print(
            f"\nTrace captured using KOLO=1\n{kolotxt_path.absolute()}",
            file=sys.stderr,
        )


F = TypeVar("F", bound=Callable[..., Any])


class CallableContextManager(Protocol):
    def __call__(self, func: F) -> F: ...  # pragma: no cover

    def __enter__(self) -> None: ...  # pragma: no cover

    def __exit__(self, *exc) -> None: ...  # pragma: no cover


@overload
def enable(_func: F) -> F:
    """Stub"""


@overload
def enable(
    config: Mapping[str, Any] | None = None,
    name: Optional[str] = None,
    source: str = "kolo.enable",
    _one_trace_per_test: bool = False,
    _save_in_thread: bool = True,
    _upload_token: Optional[str] = None,
    _db_path: Optional[Path] = None,
    _inline: bool = False,
    _inline_returns: bool = False,
) -> CallableContextManager:
    """Stub"""


def enable(
    config=None,
    *,
    name=None,
    source="kolo.enable",
    _one_trace_per_test=False,
    _save_in_thread=True,
    _upload_token=None,
    _db_path=None,
    _inline=False,
    _inline_returns=False,
):
    if config is None or isinstance(config, Mapping):
        function = None
    else:
        # Treat as a decorator called on a function
        function = config
        config = None

    enabled = Enabled(
        config=config,
        source=source,
        name=name,
        one_trace_per_test=_one_trace_per_test,
        save_in_thread=_save_in_thread,
        upload_token=_upload_token,
        db_path=_db_path,
        inline=_inline,
        inline_returns=_inline_returns,
    )

    if function is None:
        return enabled
    return enabled(function)


enabled = enable
