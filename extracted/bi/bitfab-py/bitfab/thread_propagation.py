"""Carry Bitfab trace context across thread dispatch boundaries.

``_span_stack`` and ``_replay_context`` are ``ContextVar``s, so they follow
Python's context rules: direct awaits, ``asyncio`` tasks, and
``asyncio.to_thread`` inherit them, while ``ThreadPoolExecutor.submit`` (which
``loop.run_in_executor`` routes through) and ``threading.Thread.start`` start
the callable in a context that never saw them. A ``@span`` call behind those
two boundaries finds no parent, roots its own single-span trace, and replay
mocking never fires there.

``install()`` interposes on exactly those two seams. ``submit`` captures the
submitting thread's Bitfab state per work item, the only granularity that is
correct for pooled threads, which are created once and reused across traces.
``Thread.start`` captures at start time, which is correct for one-shot threads
because a thread's start is its submission; pool-internal worker threads and
the SDK's own span-transport threads are excluded so a long-lived dispatch
loop can never pin the context of whichever trace happened to spawn it.
Callables that already carry a context (``asyncio.to_thread`` submits
``Context.run``) pass through untouched. Only Bitfab's own variables are
carried (the span stack, the replay context, the seed context, and the submit
origin: the identity of the thread that called submit()/start(), recorded onto
worker spans as ``runtime.submit_thread_id``), so no other library's
contextvars change behavior.

``Thread.start``'s replacement for ``run`` is installed as a bound method
(``types.MethodType``), not as a plain function on the instance. Other
libraries that patch ``Thread.start`` read ``self.run.__func__`` and then call
it with the thread as the first argument (Sentry's threading integration does
exactly this). A plain function has no ``__func__``, so those libraries call
the function itself with an extra argument and the worker thread dies with
``Thread.run() takes 1 positional argument but 2 were given``. The bound method
gives them the ``__func__`` they look for, and the wrapper ignores the thread
argument they pass because the callable it holds is already bound.

Installed by ``Bitfab(trace_across_threads=True)`` or
``BITFAB_TRACE_ACROSS_THREADS=1``. Process-global, idempotent, and fail-open:
any capture or wrap failure degrades to the unwrapped stdlib call.
"""

from __future__ import annotations

import contextlib
import contextvars
import functools
import threading
import types
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

from bitfab.constants import _replay_context, _seed_context, _submit_origin

_install_lock = threading.Lock()
_installed = False
_original_submit: Callable[..., Any] | None = None
_original_thread_start: Callable[..., Any] | None = None

_CapturedState = tuple[Any, Any, Any, dict[str, Any]]


def _span_stack_var() -> contextvars.ContextVar[Any]:
    from bitfab.client import _span_stack

    return _span_stack


def _capture() -> _CapturedState | None:
    try:
        stack = _span_stack_var().get()
        replay_ctx = _replay_context.get()
        seed_ctx = _seed_context.get()
    except Exception:
        return None
    if not stack and not replay_ctx and not seed_ctx:
        return None
    submitter = threading.current_thread()
    origin = {"thread_id": submitter.ident, "thread_name": submitter.name}
    return (stack, replay_ctx, seed_ctx, origin)


@contextlib.contextmanager
def _entered(state: _CapturedState) -> Any:
    stack, replay_ctx, seed_ctx, origin = state
    span_var = _span_stack_var()
    span_token = span_var.set(stack)
    replay_token = _replay_context.set(replay_ctx)
    seed_token = _seed_context.set(seed_ctx)
    origin_token = _submit_origin.set(origin)
    try:
        yield
    finally:
        span_var.reset(span_token)
        _replay_context.reset(replay_token)
        _seed_context.reset(seed_token)
        _submit_origin.reset(origin_token)


def _bind(state: _CapturedState, fn: Callable[..., Any]) -> Callable[..., Any]:
    def bound(*args: Any, **kwargs: Any) -> Any:
        with _entered(state):
            return fn(*args, **kwargs)

    with contextlib.suppress(Exception):
        functools.update_wrapper(bound, fn)
    return bound


def _bind_run(
    thread: threading.Thread, state: _CapturedState, run: Callable[..., Any]
) -> Callable[..., Any]:
    def bound_run(_thread: threading.Thread, *args: Any, **kwargs: Any) -> Any:
        with _entered(state):
            return run(*args, **kwargs)

    with contextlib.suppress(Exception):
        functools.update_wrapper(bound_run, getattr(run, "__func__", run))
    return types.MethodType(bound_run, thread)


def _carries_own_context(fn: Callable[..., Any]) -> bool:
    while isinstance(fn, functools.partial):
        fn = fn.func
    return isinstance(getattr(fn, "__self__", None), contextvars.Context)


def _is_excluded_thread(thread: threading.Thread) -> bool:
    modules = (
        getattr(getattr(thread, "_target", None), "__module__", None),
        type(thread).__module__,
    )
    return any(
        m is not None
        and _in_package(m, ("concurrent.futures", "bitfab", "opentelemetry"))
        for m in modules
    )


def _in_package(module: str, packages: tuple[str, ...]) -> bool:
    return any(module == p or module.startswith(f"{p}.") for p in packages)


def _patched_submit(
    self: Any, fn: Callable[..., Any], /, *args: Any, **kwargs: Any
) -> Any:
    original = _original_submit
    assert original is not None
    try:
        if _carries_own_context(fn):
            return original(self, fn, *args, **kwargs)
        state = _capture()
    except Exception:
        return original(self, fn, *args, **kwargs)
    if state is None:
        return original(self, fn, *args, **kwargs)
    return original(self, _bind(state, fn), *args, **kwargs)


def _patched_thread_start(self: threading.Thread) -> None:
    original = _original_thread_start
    assert original is not None
    try:
        if not _is_excluded_thread(self):
            state = _capture()
            if state is not None:
                self.run = _bind_run(self, state, self.run)  # type: ignore[method-assign]
    except Exception:
        pass
    return original(self)


def install() -> None:
    """Install both dispatch patches, once per process."""
    global _installed, _original_submit, _original_thread_start
    with _install_lock:
        if _installed:
            return
        _original_submit = ThreadPoolExecutor.submit
        _original_thread_start = threading.Thread.start
        ThreadPoolExecutor.submit = _patched_submit  # type: ignore[method-assign]
        threading.Thread.start = _patched_thread_start  # type: ignore[method-assign]
        _installed = True


def uninstall() -> None:
    """Restore the stdlib methods. For tests; never call in production."""
    global _installed
    with _install_lock:
        if not _installed:
            return
        ThreadPoolExecutor.submit = _original_submit  # type: ignore[method-assign,assignment]
        threading.Thread.start = _original_thread_start  # type: ignore[method-assign,assignment]
        _installed = False


def installed() -> bool:
    """True while the patches are active."""
    return _installed
