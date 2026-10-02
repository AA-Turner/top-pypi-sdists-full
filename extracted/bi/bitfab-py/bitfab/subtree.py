"""Automatic span capture for the dynamic call subtree under a traced root.

``Bitfab.trace`` annotates one function; every first-party function called
beneath it, at any depth, records a span without being wrapped. Capture uses
``sys.monitoring`` (3.12+) scoped to the traced call: events are installed on
entry and removed on exit, so code outside a traced call pays nothing.
"""

from __future__ import annotations

import contextlib
import inspect
import os
import site
import sys
import sysconfig
import threading
import uuid
from collections.abc import Iterator
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any, Callable

from bitfab.constants import _replay_context
from bitfab.trace_metadata import record_caller_trace_metadata
from bitfab.warn_once import warn_once

SUPPORTED = sys.version_info >= (3, 12)

AUTO_TRACE_PROTOCOL = "py-auto-v1"

DEFAULT_MAX_DEPTH: int | None = None
DEFAULT_MAX_CAPTURED_SUBTREE_SPANS = 500

MAX_DEPTH_LIMIT = "max_depth"
MAX_CAPTURED_SUBTREE_SPANS_LIMIT = "max_captured_subtree_spans"
TRUNCATION_LIMIT_ORDER = (
    MAX_DEPTH_LIMIT,
    MAX_CAPTURED_SUBTREE_SPANS_LIMIT,
)
TRUNCATED_BY_METADATA_KEY = "bitfab.truncated_by"
DROPPED_SPANS_METADATA_KEY = "bitfab.dropped_spans"

_PREFERRED_TOOL_IDS = (3, 4)

# Frames the interpreter creates for expressions rather than for a function the
# author wrote. A lambda inside map() runs once per element, so recording these
# turns one logical call into thousands of spans.
_SYNTHETIC_NAMES = frozenset(
    {"<lambda>", "<genexpr>", "<listcomp>", "<setcomp>", "<dictcomp>", "<module>"}
)

EmitSpan = Callable[..., None]


def is_passthrough_wrapper(code: Any) -> bool:
    """Whether this looks like a decorator's wrapper: ``(*args, **kwargs)`` and
    nothing else. Such a frame adds a span per decorator without adding a step
    the author would recognize in their own call tree."""
    return (
        code.co_argcount == 0
        and code.co_kwonlyargcount == 0
        and bool(code.co_flags & inspect.CO_VARARGS)
        and bool(code.co_flags & inspect.CO_VARKEYWORDS)
    )


def _library_prefixes() -> tuple[str, ...]:
    paths = set()
    for key in ("stdlib", "platstdlib", "purelib", "platlib"):
        value = sysconfig.get_paths().get(key)
        if value:
            paths.add(os.path.realpath(value))
    try:
        for value in site.getsitepackages():
            paths.add(os.path.realpath(value))
    except AttributeError:
        pass
    try:
        user_site = site.getusersitepackages()
        if user_site:
            paths.add(os.path.realpath(user_site))
    except AttributeError:
        pass
    paths.add(os.path.realpath(os.path.dirname(__file__)))
    return tuple(p + os.sep for p in sorted(paths))


_LIBRARY_PREFIXES = _library_prefixes()

_never_first_party: dict[str, bool] = {}


def is_library_code(filename: str) -> bool:
    """Whether this file can never be first-party under any session.

    Only such files are safe to permanently de-instrument with ``DISABLE``:
    the decision must hold for every traced root in the process, not just the
    one running now, because ``DISABLE`` is not scoped to a session.
    """
    cached = _never_first_party.get(filename)
    if cached is not None:
        return cached

    if not filename or filename.startswith("<"):
        result = True
    else:
        real = os.path.realpath(filename)
        result = real.startswith(_LIBRARY_PREFIXES)

    _never_first_party[filename] = result
    return result


def package_root_of(fn: Callable[..., Any]) -> str | None:
    """Directory treated as first-party for a root decorated on ``fn``.

    Walks up from the defining module while ``__init__.py`` exists, so a
    function in ``myapp/services/orders.py`` yields ``myapp/``.
    """
    module = sys.modules.get(getattr(fn, "__module__", "") or "")
    filename = getattr(module, "__file__", None)
    if not filename:
        code = getattr(fn, "__code__", None)
        filename = getattr(code, "co_filename", None)
    if not filename:
        return None

    directory = os.path.dirname(os.path.realpath(filename))
    while True:
        parent = os.path.dirname(directory)
        if parent == directory:
            break
        if not os.path.exists(os.path.join(parent, "__init__.py")):
            break
        directory = parent
    return directory


def roots_for(fn: Callable[..., Any]) -> tuple[str, ...]:
    root = package_root_of(fn)
    return (root + os.sep,) if root else ()


@dataclass
class _Open:
    code: Any
    span_id: str | None
    parent_span_id: str
    name: str
    inputs: dict[str, Any]
    started_at: str
    emit: bool = True
    counts_toward_depth: bool = True
    nested_trace: Session | None = None
    span_type: str = "function"
    mirror: bool = False
    variant: str | None = None
    result: Any = None
    error: str | None = None
    closed: bool = False
    framework_span: bool = False
    resume_beneath: tuple[_Open, ...] = ()
    declared: bool = False


@dataclass(eq=False)
class Session:
    trace_id: str
    root_span_id: str
    label: str
    emit: EmitSpan
    now: Callable[[], str]
    roots: tuple[str, ...]
    max_depth: int | None = DEFAULT_MAX_DEPTH
    max_captured_subtree_spans: int = DEFAULT_MAX_CAPTURED_SUBTREE_SPANS
    content_off: Callable[[str], bool] | None = None
    exclude: frozenset[str] = frozenset()
    include_wrappers: bool = False
    mock_on_replay_default: bool = False
    root_code: Any = None
    root_span_context: Any = None
    link_pending: bool = False
    captured_subtree_count: int = 0
    truncated: bool = False
    dropped_spans: int = 0
    fired_limits: set[str] = field(default_factory=set)
    _owns_cache: dict[str, bool] = field(default_factory=dict)
    _path_cache: dict[str, str] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def relative_path(self, filename: str) -> str:
        cached = self._path_cache.get(filename)
        if cached is not None:
            return cached
        real = os.path.realpath(filename)
        result = os.path.basename(real)
        for root in self.roots:
            if real.startswith(root):
                package = os.path.basename(root.rstrip(os.sep))
                tail = real[len(root) :].split(os.sep)
                result = "/".join((package, *tail)) if package else "/".join(tail)
                break
        self._path_cache[filename] = result
        return result

    def owns(self, filename: str) -> bool:
        """Cached because this runs on every call inside a traced subtree, and
        ``realpath`` walks the filesystem. A racing duplicate computation is
        harmless; the answer is a pure function of the filename."""
        cached = self._owns_cache.get(filename)
        if cached is not None:
            return cached
        result = bool(self.roots) and os.path.realpath(filename).startswith(self.roots)
        self._owns_cache[filename] = result
        return result

    def hidden_by_sim_plan(self, span_name: str) -> bool:
        if self.content_off is None:
            return False
        try:
            return self.content_off(span_name)
        except Exception:
            return False

    def exceeds_depth(self, depth: int) -> bool:
        return self.max_depth is not None and depth >= self.max_depth

    def _drop_for(self, limit: str) -> None:
        self.truncated = True
        self.fired_limits.add(limit)
        self.dropped_spans += 1

    def refuse_for_depth(self) -> None:
        with self._lock:
            self._drop_for(MAX_DEPTH_LIMIT)

    def take_discovery_budget(self) -> bool:
        with self._lock:
            if self.captured_subtree_count >= self.max_captured_subtree_spans:
                self._drop_for(MAX_CAPTURED_SUBTREE_SPANS_LIMIT)
                return False
            self.captured_subtree_count += 1
            return True

    def truncation_metadata(self) -> dict[str, Any] | None:
        with self._lock:
            if not self.fired_limits:
                return None
            return {
                TRUNCATED_BY_METADATA_KEY: ",".join(
                    limit
                    for limit in TRUNCATION_LIMIT_ORDER
                    if limit in self.fired_limits
                ),
                DROPPED_SPANS_METADATA_KEY: self.dropped_spans,
            }

    def warn_if_truncated(self) -> None:
        """A trace that silently stops partway is worse than a small one: the
        gap looks like code that never ran. Say so, once per traced function."""
        if not self.truncated:
            return
        warn_once(
            f"subtree-truncated:{self.label}",
            f"'{self.label}' hit a subtree capture limit (max_captured_subtree_spans="
            f"{self.max_captured_subtree_spans}, max_depth={self.max_depth}) "
            "and its trace is "
            "incomplete. Raise the limits, or narrow what is traced with "
            "exclude=[...].",
        )


_session: ContextVar[tuple[Session, ...]] = ContextVar(
    "bitfab_subtree_session", default=()
)
_open: ContextVar[dict[Session, tuple[_Open, ...]] | None] = ContextVar(
    "bitfab_subtree_open", default=None
)

_local = threading.local()

# Entries for generators and coroutines that are suspended: off the stack, but
# their spans are still open. The frame itself is retained until its session
# ends, preventing an abandoned generator's frame id from being reused for a
# different call.
_suspended: dict[Session, dict[Any, _Open]] = {}
_suspended_lock = threading.Lock()

_install_lock = threading.Lock()
_installed = 0
_tool_id: int | None = None


def current_session() -> Session | None:
    sessions = _session.get()
    return sessions[-1] if sessions else None


def _reentrant() -> bool:
    return getattr(_local, "busy", False)


@contextlib.contextmanager
def uncaptured() -> Iterator[None]:
    busy = _reentrant()
    _local.busy = True
    try:
        yield
    finally:
        _local.busy = busy


def qualified_span_name(qualname: str) -> str:
    """Readable span name: ``Order.process`` for a method, ``helper`` for a
    closure. A qualified name spells a nested function
    ``outer.<locals>.helper``, which is noise in a span tree."""
    if "<locals>." in qualname:
        qualname = qualname.rsplit("<locals>.", 1)[1]
    return qualname


def _span_name(code: Any) -> str:
    return qualified_span_name(code.co_qualname)


def function_identity(session: Session, code: Any) -> tuple[str, str, int]:
    path = session.relative_path(code.co_filename)
    return (
        f"{AUTO_TRACE_PROTOCOL}:{path}#{code.co_qualname}",
        path,
        code.co_firstlineno,
    )


def _args_of(frame: Any, code: Any) -> dict[str, Any]:
    count = code.co_argcount + code.co_kwonlyargcount
    names = code.co_varnames[:count]
    if names and names[0] in ("self", "cls"):
        names = names[1:]
    local_vars = frame.f_locals
    return {name: local_vars.get(name) for name in names}


def _stands_in(entry: _Open) -> bool:
    return not entry.emit or entry.mirror


def _innermost_parent(stack: tuple[_Open, ...]) -> _Open | None:
    return next(
        (
            entry
            for entry in reversed(stack)
            if entry.span_id is not None and not (entry.framework_span and entry.closed)
        ),
        None,
    )


def _innermost_frame(stack: tuple[_Open, ...]) -> int | None:
    return next(
        (
            index
            for index in range(len(stack) - 1, -1, -1)
            if not stack[index].framework_span
        ),
        None,
    )


def _without(stack: tuple[_Open, ...], index: int) -> tuple[_Open, ...]:
    return tuple(
        entry
        for position, entry in enumerate(stack)
        if position != index and not (entry.framework_span and entry.closed)
    )


def _allocate(
    session: Session,
    stack: tuple[_Open, ...],
    span_name: str | None = None,
    *,
    declared: bool = False,
) -> tuple[str, str | None]:
    parent = _innermost_parent(stack)
    parent_span_id = parent.span_id if parent else session.root_span_id
    if declared:
        return parent_span_id, str(uuid.uuid4())
    depth = sum(entry.counts_toward_depth for entry in stack)
    if session.exceeds_depth(depth):
        session.refuse_for_depth()
        return parent_span_id, None
    hidden = span_name is not None and session.hidden_by_sim_plan(span_name)
    if not hidden and not session.take_discovery_budget():
        return parent_span_id, None
    return parent_span_id, str(uuid.uuid4())


def _args_from_call(
    code: Any, args: tuple[Any, ...], kwargs: dict[str, Any] | None
) -> dict[str, Any]:
    count = code.co_argcount + code.co_kwonlyargcount
    names = list(code.co_varnames[:count])
    if names and names[0] in ("self", "cls"):
        names = names[1:]
    inputs: dict[str, Any] = dict(zip(names, args, strict=False))
    extra = args[len(names) :]
    if extra:
        inputs["args"] = list(extra)
    inputs.update(kwargs or {})
    return inputs


def _emit_entry(
    session: Session,
    entry: _Open,
    result: Any,
    error: str | None,
    experiment_id: str | None = None,
) -> None:
    function_id, function_file, function_line = function_identity(session, entry.code)
    nested = entry.nested_trace
    session.emit(
        experiment_id=experiment_id,
        span_id=entry.span_id,
        parent_span_id=entry.parent_span_id,
        span_name=entry.name,
        inputs=entry.inputs,
        result=result,
        error=error,
        started_at=entry.started_at,
        ended_at=session.now(),
        function_id=function_id,
        function_file=function_file,
        function_line=function_line,
        span_type=entry.span_type,
        variant=entry.variant,
        declared_node=entry.declared,
        nested_trace=(
            {
                "trace_id": nested.trace_id,
                "trace_function_key": nested.label,
                "span_id": nested.root_span_id,
            }
            if nested is not None
            else None
        ),
    )


def _record_enclosing_span(nested: Session, span_id: str) -> None:
    context = nested.root_span_context
    if context is None:
        return
    link = context.get("enclosingTrace")
    if link is not None:
        link["span_id"] = span_id


def _on_start(code: Any, instruction_offset: int) -> Any:
    if is_library_code(code.co_filename):
        return sys.monitoring.DISABLE

    sessions = _session.get()
    if not sessions or _reentrant():
        return None

    _local.busy = True
    try:
        stacks = _open.get() or {}
        updated = dict(stacks)
        frame = sys._getframe(1)
        innermost = sessions[-1]
        nested = (
            innermost
            if innermost.link_pending and innermost.root_code is code
            else None
        )
        enclosing_of_nested = sessions[-2] if len(sessions) > 1 else None
        for session in sessions:
            if not session.owns(code.co_filename):
                continue
            if code.co_name in session.exclude or code.co_name in _SYNTHETIC_NAMES:
                continue
            if not session.include_wrappers and is_passthrough_wrapper(code):
                continue

            stack = stacks.get(session, ())
            if stack and stack[-1].code is code and _stands_in(stack[-1]):
                continue

            declared = nested is not None and session is not innermost
            parent_span_id, span_id = _allocate(
                session, stack, _span_name(code), declared=declared
            )
            entry = _Open(
                code=code,
                span_id=span_id,
                parent_span_id=parent_span_id,
                name=_span_name(code),
                inputs=_args_of(frame, code) if span_id else {},
                started_at=session.now() if span_id else "",
                nested_trace=nested if session is not innermost else None,
                declared=declared,
            )
            selective = (_replay_context.get() or {}).get("selective_replay")
            if selective is not None and span_id is not None and session is innermost:
                # Monitoring cannot skip a body. Register its live boundary so
                # configured descendants can match their recorded parent and
                # execution coverage includes automatically observed calls.
                selective.enter(
                    trace_function_key=session.label,
                    span_name=entry.name,
                    span_id=span_id,
                    parent_span_id=parent_span_id,
                    inputs=[],
                    kwargs=entry.inputs,
                    safety_mock=False,
                    can_reuse_output=False,
                    reuse_allowed=False,
                )
            if (
                span_id is not None
                and nested is not None
                and session is enclosing_of_nested
            ):
                _record_enclosing_span(nested, span_id)
            updated[session] = (*stack, entry)
        if nested is not None:
            nested.link_pending = False
        _open.set(updated)
    except Exception:
        pass
    finally:
        _local.busy = False
    return None


def _on_yield(code: Any, instruction_offset: int, retval: Any) -> Any:
    """A generator or coroutine suspending hands control back to its caller, so
    its entry has to leave the stack even though its span stays open. Without
    this, a partially consumed generator stays on the stack forever and every
    later call in that frame parents to it."""
    if is_library_code(code.co_filename):
        return sys.monitoring.DISABLE

    sessions = _session.get()
    if not sessions or _reentrant():
        return None

    _local.busy = True
    try:
        stacks = _open.get() or {}
        updated = dict(stacks)
        frame = sys._getframe(1)
        with _suspended_lock:
            for session in sessions:
                stack = stacks.get(session, ())
                index = _innermost_frame(stack)
                if index is None or stack[index].code is not code:
                    continue
                entry = stack[index]
                entry.resume_beneath = stack[index + 1 :]
                updated[session] = _without(stack, index)
                _suspended.setdefault(session, {})[frame] = entry
        _open.set(updated)
    except Exception:
        pass
    finally:
        _local.busy = False
    return None


def _reinsert(stack: tuple[_Open, ...], entry: _Open) -> tuple[_Open, ...]:
    beneath = entry.resume_beneath
    entry.resume_beneath = ()
    index = len(stack)
    while index > 0 and any(stack[index - 1] is above for above in beneath):
        index -= 1
    return (*stack[:index], entry, *stack[index:])


def _restore_suspended(frame: Any) -> None:
    sessions = _session.get()
    if not sessions or _reentrant():
        return

    _local.busy = True
    try:
        stacks = _open.get() or {}
        updated = dict(stacks)
        with _suspended_lock:
            for session in sessions:
                suspended = _suspended.get(session)
                entry = suspended.pop(frame, None) if suspended else None
                if suspended == {}:
                    del _suspended[session]
                if entry is None:
                    continue
                stack = stacks.get(session, ())
                top = _innermost_frame(stack)
                if (
                    top is not None
                    and not stack[top].emit
                    and stack[top].code is entry.code
                    and stack[top].span_id == entry.span_id
                ):
                    continue
                updated[session] = _reinsert(stack, entry)
        _open.set(updated)
    except Exception:
        pass
    finally:
        _local.busy = False


def _on_resume(code: Any, instruction_offset: int) -> Any:
    if is_library_code(code.co_filename):
        return sys.monitoring.DISABLE
    _restore_suspended(sys._getframe(1))
    return None


def _on_throw(code: Any, instruction_offset: int, exception: BaseException) -> Any:
    """A coroutine or generator resumed by ``throw()`` (task cancellation,
    ``gen.throw``) fires PY_THROW, not PY_RESUME, so without this its entry
    would stay parked in ``_suspended`` and later calls would mis-parent.
    CPython refuses DISABLE for PY_THROW, so filter instead of returning it."""
    if is_library_code(code.co_filename):
        return None
    _restore_suspended(sys._getframe(1))
    return None


def _close(code: Any, result: Any, error: str | None) -> Any:
    sessions = _session.get()
    if not sessions or _reentrant():
        return None

    _local.busy = True
    try:
        frame = sys._getframe(2)
        stacks = _open.get() or {}
        updated = dict(stacks)
        with _suspended_lock:
            suspended_entries = {}
            for session in sessions:
                candidate = _suspended.get(session, {}).get(frame)
                if candidate is not None and candidate.code is code:
                    del _suspended[session][frame]
                    suspended_entries[session] = candidate
                else:
                    suspended_entries[session] = None
            for session in sessions:
                if _suspended.get(session) == {}:
                    del _suspended[session]

        for session in sessions:
            entry = suspended_entries[session]
            stack = stacks.get(session, ())
            if entry is None:
                index = _innermost_frame(stack)
                if index is None or stack[index].code is not code:
                    continue
                entry = stack[index]
                updated[session] = _without(stack, index)

            if entry.mirror:
                entry.result = result
                entry.error = error
                entry.closed = True
                continue
            if not entry.emit or entry.span_id is None:
                continue
            _emit_entry(session, entry, result, error)
        _open.set(updated)
    except Exception:
        pass
    finally:
        _local.busy = False
    return None


def _on_return(code: Any, instruction_offset: int, retval: Any) -> Any:
    if is_library_code(code.co_filename):
        return sys.monitoring.DISABLE
    return _close(code, retval, None)


def _on_unwind(code: Any, instruction_offset: int, exception: BaseException) -> Any:
    # CPython refuses DISABLE for PY_UNWIND and removes the callback when it is
    # returned, which would silently end subtree capture for the whole process
    # the first time an exception passed through library code. Filter instead.
    if is_library_code(code.co_filename):
        return None
    return _close(code, None, f"{type(exception).__name__}: {exception}")


def _is_free_threaded() -> bool:
    check = getattr(sys, "_is_gil_enabled", None)
    return check is not None and not check()


def _acquire_tool_id() -> int | None:
    for candidate in _PREFERRED_TOOL_IDS:
        try:
            sys.monitoring.use_tool_id(candidate, "bitfab")
            return candidate
        except ValueError:
            continue
    return None


def _install() -> bool:
    global _installed, _tool_id
    with _install_lock:
        if _installed:
            _installed += 1
            return _tool_id is not None

        if _is_free_threaded():
            warn_once(
                "subtree-free-threaded",
                "subtree capture is not verified on free-threaded builds; span "
                "trees may be incomplete or mis-parented under concurrency. The "
                "traced function's own span is unaffected.",
            )

        tool_id = _acquire_tool_id()
        if tool_id is None:
            warn_once(
                "subtree-no-tool-id",
                "every sys.monitoring tool id is in use (a debugger, profiler, or "
                "coverage tool holds them); the traced root still records a span but "
                "its call subtree does not.",
            )
            _installed += 1
            return False

        events = sys.monitoring.events
        sys.monitoring.register_callback(tool_id, events.PY_START, _on_start)
        sys.monitoring.register_callback(tool_id, events.PY_RETURN, _on_return)
        sys.monitoring.register_callback(tool_id, events.PY_UNWIND, _on_unwind)
        sys.monitoring.register_callback(tool_id, events.PY_YIELD, _on_yield)
        sys.monitoring.register_callback(tool_id, events.PY_RESUME, _on_resume)
        sys.monitoring.register_callback(tool_id, events.PY_THROW, _on_throw)
        sys.monitoring.set_events(
            tool_id,
            events.PY_START
            | events.PY_RETURN
            | events.PY_UNWIND
            | events.PY_YIELD
            | events.PY_RESUME
            | events.PY_THROW,
        )
        _tool_id = tool_id
        _installed = 1
        return True


def _uninstall() -> None:
    global _installed, _tool_id
    with _install_lock:
        if _installed:
            _installed -= 1
        if _installed or _tool_id is None:
            return
        try:
            sys.monitoring.set_events(_tool_id, 0)
            sys.monitoring.free_tool_id(_tool_id)
        finally:
            _tool_id = None


class SubtreeCapture:
    """Context manager installing subtree capture for one traced call."""

    def __init__(
        self,
        session: Session | None,
        code: Any = None,
        *,
        finish: bool = True,
    ) -> None:
        self._session = session
        self._code = code
        self._finish = finish
        self._token = None
        self._active = False

    def __enter__(self) -> SubtreeCapture:
        if self._session is None:
            return self
        self._active = _install()
        if not self._active:
            _uninstall()
            return self
        sessions = _session.get()
        self._token = _session.set((*sessions, self._session))
        stacks = dict(_open.get() or {})
        if self._code is not None:
            stacks[self._session] = (
                _Open(
                    code=self._code,
                    span_id=self._session.root_span_id,
                    parent_span_id=self._session.root_span_id,
                    name=_span_name(self._code),
                    inputs={},
                    started_at="",
                    emit=False,
                    counts_toward_depth=False,
                ),
            )
        else:
            stacks[self._session] = ()
        _open.set(stacks)
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if not self._active:
            return
        if self._token is not None:
            _session.reset(self._token)
        stacks = dict(_open.get() or {})
        stacks.pop(self._session, None)
        _open.set(stacks)
        if self._finish:
            finish(self._session)
        _uninstall()


class BorrowedSpan:
    """Make a span emitted by ``client.span`` visible to subtree capture."""

    def __init__(
        self,
        code: Any,
        trace_id: str,
        span_id: str,
        *,
        name: str | None = None,
        span_type: str | None = None,
        args: tuple[Any, ...] = (),
        kwargs: dict[str, Any] | None = None,
        experiment_id: str | None = None,
        variant: str | None = None,
    ) -> None:
        self._code = code
        self._trace_id = trace_id
        self._span_id = span_id
        self._name = name
        self._span_type = span_type
        self._args = args
        self._kwargs = kwargs
        self._experiment_id = experiment_id
        self._variant = variant
        self._entries: dict[Session, _Open] = {}
        self._done = False

    def emit(self, output: Any, error: str | None = None) -> None:
        if self._done:
            return
        self._done = True
        for session, entry in self._entries.items():
            if not entry.mirror or entry.span_id is None:
                continue
            with contextlib.suppress(Exception):
                _emit_entry(session, entry, output, error, self._experiment_id)

    def _entry_for(self, session: Session, stack: tuple[_Open, ...]) -> _Open | None:
        if session.trace_id == self._trace_id:
            return _Open(
                code=self._code,
                span_id=self._span_id,
                parent_span_id=session.root_span_id,
                name=_span_name(self._code),
                inputs={},
                started_at="",
                emit=False,
            )
        if self._name is None:
            return None
        parent_span_id, span_id = _allocate(session, stack, self._name, declared=True)
        return _Open(
            code=self._code,
            span_id=span_id,
            parent_span_id=parent_span_id,
            name=self._name,
            inputs=_args_from_call(self._code, self._args, self._kwargs)
            if span_id
            else {},
            started_at=session.now() if span_id else "",
            span_type=self._span_type or "function",
            mirror=True,
            variant=self._variant,
            declared=True,
        )

    def __enter__(self) -> BorrowedSpan:
        if self._code is None:
            return self
        try:
            stacks = _open.get() or {}
            updated = dict(stacks)
            entries: dict[Session, _Open] = {}
            for session in _session.get():
                stack = stacks.get(session, ())
                entry = self._entry_for(session, stack)
                if entry is None:
                    continue
                updated[session] = (*stack, entry)
                entries[session] = entry
            _open.set(updated)
            self._entries = entries
        except Exception:
            pass
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        stacks = _open.get() or {}
        updated = dict(stacks)
        for session, entry in self._entries.items():
            stack = stacks.get(session, ())
            index = _innermost_frame(stack)
            if index is None or stack[index] is not entry:
                continue
            updated[session] = _without(stack, index)
        _open.set(updated)
        if exc_type is not None:
            self.emit(None, f"{exc_type.__name__}: {exc}")


def borrowed_span(
    code: Any,
    trace_id: str,
    span_id: str,
    *,
    name: str | None = None,
    span_type: str | None = None,
    args: tuple[Any, ...] = (),
    kwargs: dict[str, Any] | None = None,
    experiment_id: str | None = None,
    variant: str | None = None,
) -> BorrowedSpan:
    return BorrowedSpan(
        code,
        trace_id,
        span_id,
        name=name,
        span_type=span_type,
        args=args,
        kwargs=kwargs,
        experiment_id=experiment_id,
        variant=variant,
    )


class SuppressedNode:
    """Hide one configured node while preserving capture of its descendants."""

    def __init__(
        self, code: Any, session: Session, *, all_sessions: bool = False
    ) -> None:
        self._code = code
        self._session = session
        self._all_sessions = all_sessions
        self._entries: dict[Session, _Open] = {}

    def __enter__(self) -> SuppressedNode:
        if self._code is None or self._session not in _session.get():
            return self
        sessions = _session.get() if self._all_sessions else (self._session,)
        stacks = _open.get() or {}
        updated = dict(stacks)
        for session in sessions:
            entry = _Open(
                code=self._code,
                span_id=None,
                parent_span_id=session.root_span_id,
                name=_span_name(self._code),
                inputs={},
                started_at="",
                emit=False,
                counts_toward_depth=False,
            )
            updated[session] = (*stacks.get(session, ()), entry)
            self._entries[session] = entry
        _open.set(updated)
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if not self._entries:
            return
        stacks = _open.get() or {}
        updated = dict(stacks)
        for session, entry in self._entries.items():
            stack = stacks.get(session, ())
            index = _innermost_frame(stack)
            if index is not None and stack[index] is entry:
                updated[session] = _without(stack, index)
        _open.set(updated)


def suppressed_node(
    code: Any, session: Session, *, all_sessions: bool = False
) -> SuppressedNode:
    return SuppressedNode(code, session, all_sessions=all_sessions)


def current_parent_span_id(session: Session) -> str:
    """Return the trace-owned parent for a configured node."""
    stack = (_open.get() or {}).get(session, ())
    parent = _innermost_parent(stack)
    return parent.span_id if parent is not None else session.root_span_id


def enter_framework_span(trace_id: str, span_id: str | None) -> _Open | None:
    sessions = [session for session in _session.get() if session.trace_id == trace_id]
    if not sessions:
        return None
    entry = _Open(
        code=None,
        span_id=span_id,
        parent_span_id="",
        name="",
        inputs={},
        started_at="",
        emit=False,
        counts_toward_depth=False,
        framework_span=True,
    )
    stacks = _open.get() or {}
    updated = dict(stacks)
    for session in sessions:
        updated[session] = (*stacks.get(session, ()), entry)
    _open.set(updated)
    return entry


def exit_framework_span(entry: _Open) -> None:
    entry.closed = True
    stacks = _open.get()
    if not stacks:
        return
    _open.set(
        {
            session: tuple(
                open_entry for open_entry in stack if open_entry is not entry
            )
            for session, stack in stacks.items()
        }
    )


def finish(session: Session | None) -> None:
    if session is None:
        return
    with _suspended_lock:
        _suspended.pop(session, None)
    metadata = session.truncation_metadata()
    if metadata is not None:
        record_caller_trace_metadata(session.trace_id, metadata)
    session.warn_if_truncated()


def begin(
    session: Session | None,
    code: Any = None,
    *,
    finish_on_exit: bool = True,
) -> SubtreeCapture:
    """Activate one subtree session alongside any sessions already running."""
    if not SUPPORTED or session is None:
        return SubtreeCapture(None)
    return SubtreeCapture(session, code, finish=finish_on_exit)
