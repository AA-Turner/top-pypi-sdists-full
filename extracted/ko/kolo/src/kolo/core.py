from __future__ import annotations

import platform
import sys
import threading
from collections.abc import Mapping
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Optional, Protocol, TypeVar, overload

import httpx

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


def save_trace_in_thread(profiler):
    if platform.machine() == "wasm32":
        profiler.save()
    else:
        name = "kolo-save_trace_in_db"
        threading.Thread(target=profiler.save, name=name).start()


def upload_trace_in_thread(profiler, upload_token):
    def upload():
        trace = profiler.build_trace()
        try:
            from .upload import upload_to_dashboard

            response = upload_to_dashboard(trace, upload_token)
            response.raise_for_status()
        except httpx.HTTPError:
            logger.exception("Failed to upload trace to Kolo dashboard.")

    if platform.machine() == "wasm32":
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
            if sys.monitoring.get_tool(sys.monitoring.PROFILER_ID):  # type: ignore[attr-defined]
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

    def _activate(self) -> None:
        """
        Internal activation logic.

        Activates Kolo profiling/monitoring. If already active, logs a message
        and returns early.
        """
        if self._is_already_active():
            logger.debug(
                "Kolo already active, skipping duplicate activation from %s",
                self.source,
            )
            return

        # self.db_path is typically not set,
        # but we make use of it in tests.
        if self.db_path is None:
            db_path = setup_db()
        else:
            db_path = self.db_path

        monkeypatch_queryset_repr()

        # Default to monitoring on Python 3.12+
        default_use_monitoring = sys.version_info >= (3, 12)
        use_monitoring = self.config.get("use_monitoring", default_use_monitoring)
        if sys.version_info >= (3, 12) and use_monitoring:
            from .monitoring import activate_monitoring

            monitor = self.register_monitor(db_path)
            activate_monitoring(monitor)
            self._monitor = monitor
            self.trace_id = monitor.trace_id
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

    def __enter__(self):
        self._activate()
        return self

    def register_monitor(self, db_path):
        if self.config.get("use_rust", True):
            try:
                from ._kolo import register_monitor
            except ImportError as e:
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

    def save_trace_profiler(self):
        assert self._profiler is not None

        if self.one_trace_per_test:
            return

        if not self.save_in_thread:
            self._profiler.save()
            return

        if self.upload_token:
            upload_trace_in_thread(self._profiler, self.upload_token)
        else:
            save_trace_in_thread(self._profiler)

    def save_trace_monitor(self):
        assert self._monitor is not None

        if self.one_trace_per_test:
            return

        if not self.save_in_thread:
            self._monitor.save()
            return

        if self.upload_token:
            upload_trace_in_thread(self._monitor, self.upload_token)
        else:
            save_trace_in_thread(self._monitor)

    def _deactivate(self, *exc) -> None:
        """
        Internal deactivation logic.

        Deactivates profiling/monitoring, saves traces, and handles inline output.
        """
        if self._profiler is not None:
            self._profiler.__exit__(*exc)
            self.save_trace_profiler()
            self._profiler = None

        if self._monitor is not None:
            from .monitoring import disable_monitoring  # type: ignore[attr-defined]

            disable_monitoring(self._monitor)
            self.save_trace_monitor()
            self._monitor = None

        if self.inline:
            assert self.trace_id is not None
            self._output_inline_trace()

    def __exit__(self, *exc) -> None:
        self._deactivate(*exc)

    def _output_inline_trace(self):
        """Output the compact trace representation to stderr."""
        import asyncio

        import click

        from .cli_mcp_shared import get_compact_traces
        from .db import setup_db

        db_path = self.db_path if self.db_path else setup_db()

        async def _get_inline_compact():
            results = await get_compact_traces(
                db_path,
                trace_id=self.trace_id,
                returns=self.inline_returns,
            )
            if results:
                trace_id, compact_repr = results[0]
                click.echo(compact_repr, err=True)

        asyncio.run(_get_inline_compact())


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
            True if activation succeeded, False if already active (skipped)
        """
        if self._enabled._is_already_active():
            logger.debug("KOLO=1: Tracing already active, skipping auto-activation")
            return False

        self._enabled._activate()
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
            self._save_latest_trace_file()
        except Exception as e:
            # Don't crash during shutdown - log to stderr
            import sys

            print(f"Kolo cleanup error during shutdown: {e}", file=sys.stderr)
            import traceback

            traceback.print_exc(file=sys.stderr)

    def _save_latest_trace_file(self):
        """
        Save the compact representation of the trace to .kolo/latest.txt
        and print a link to stderr.
        """
        if not self.trace_id:
            return

        from .cli_mcp_shared import get_compact_trace_sync
        from .db import load_trace_with_size_from_db

        db_path = self._enabled.db_path if self._enabled.db_path else setup_db()

        try:
            _, _, size, trace_data = load_trace_with_size_from_db(
                db_path, self.trace_id
            )
            compact_repr = get_compact_trace_sync(trace_data, size)

            latest_path = db_path.parent / "latest.txt"

            with open(latest_path, "w", encoding="utf-8") as f:
                f.write(compact_repr)

            latest_path_display = latest_path.absolute()
            print(
                f"\nTrace captured using KOLO=1\n{latest_path_display}",
                file=sys.stderr,
            )
        except Exception as e:
            # If trace loading fails (e.g. if it wasn't saved yet), just ignore
            # We don't want to spam stderr with errors during shutdown
            print(
                f"Error occurred while saving trace using KOLO=1: {e}",
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
    _save_in_thread: bool = False,
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
    _save_in_thread=False,
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
