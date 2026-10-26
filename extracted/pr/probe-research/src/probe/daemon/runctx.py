"""One daemon run's own state, inside a process that hosts several (plan H1, H3, H4).

The daemon was written as one `probe daemon worker` process per session, so a
module global held that session's value: the refusal-fallback model, the
settings the server pushed, the HTTP client, the alert gate's base URL, the
environment. The daemon host (`probe.daemon.host`) runs every session's worker
in one process, one thread and one asyncio loop per run, so each of those values
must be the RUN's.

    Run           one hosted run: its session id, its token (the lease's
                  `owner`), its environment, its slots. Entered with `enter`
                  on the run's own thread; a ContextVar carries it into every
                  task of the run's loop and every `asyncio.to_thread` call
                  (those copy the context; `loop.run_in_executor` does not, so
                  `executor` gives a run's loop threads that enter it too)
    Shared        a module-level value: the module global itself when no run is
                  entered (a one-session process, and the tests that patch the
                  global), else the run's own copy
    ContextEnviron  `os.environ` answering from the run's environment
                  (`install`, once, in the host only); a process that never
                  installs it keeps the real `os.environ`

A child started without `env=` inherits the process's C-level environment, not
this mapping: every child the daemon starts passes `env=` (a guard test).

Stdlib only.
"""

from __future__ import annotations

import concurrent.futures
import contextlib
import contextvars
import os
import threading
import uuid
from collections.abc import Callable, Iterator, MutableMapping
from dataclasses import dataclass, field


@dataclass
class Run:
    session_id: str
    #: The session's environment (a copy): what `os.environ` answers inside the run.
    #: Never printed: it holds the session's keys.
    env: dict | None = field(default=None, repr=False)
    #: The lease's `owner` (`lease.renew`): two runs of one session in one
    #: process share a pid, never a token.
    token: str = field(default_factory=lambda: uuid.uuid4().hex)
    slots: dict = field(default_factory=dict, repr=False)


_RUN: contextvars.ContextVar[Run | None] = contextvars.ContextVar("probe_daemon_run", default=None)


def current() -> Run | None:
    """The run entered in this context, or None (a one-session process)."""
    return _RUN.get()


def token() -> str | None:
    """The current run's lease token, or None outside a hosted run."""
    run = _RUN.get()
    return None if run is None else run.token


@contextlib.contextmanager
def enter(run: Run) -> Iterator[Run]:
    """Run the block (and every task and `to_thread` call it starts) as `run`."""
    reset = _RUN.set(run)
    try:
        yield run
    finally:
        _RUN.reset(reset)


def executor(run: Run, *, max_workers: int | None = None,
             on_thread: Callable[[], None] | None = None) -> concurrent.futures.ThreadPoolExecutor:
    """A default executor for a run's loop whose threads are the run's: work handed
    to `loop.run_in_executor` sees the run's environment and slots too.
    `on_thread` runs first on each new thread (the host names it for a crash)."""

    def start() -> None:
        _RUN.set(run)
        if on_thread is not None:
            on_thread()

    return concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers, thread_name_prefix=f"run-{run.session_id[:12]}", initializer=start)


_MISSING = object()


class Shared:
    """A module-level value that is the run's own inside a hosted run.

    `Shared(globals(), "_NAME", factory)`: outside a run it IS the module global
    `_NAME` (read and written through the module's dict, so a test that patches
    the global still sees its value); inside a run each run starts from
    `factory()` (or None) and keeps its own."""

    def __init__(self, module_globals: dict, name: str, factory: Callable[[], object] | None = None) -> None:
        self._globals = module_globals
        self._name = name
        self._key = f"{module_globals.get('__name__', '?')}.{name}"
        self._factory = factory

    def get(self):
        run = _RUN.get()
        if run is None:
            return self._globals[self._name]
        value = run.slots.get(self._key, _MISSING)
        if value is _MISSING:
            value = run.slots.setdefault(self._key, self._factory() if self._factory is not None else None)
        return value

    def set(self, value) -> None:
        run = _RUN.get()
        if run is None:
            self._globals[self._name] = value
        else:
            run.slots[self._key] = value


class ContextEnviron(MutableMapping):
    """`os.environ` for a process that hosts runs: inside a run, the run's own
    environment (reads, writes, deletes, iteration, `copy()`); outside one, the
    process's."""

    def __init__(self, base: MutableMapping) -> None:
        self._base = base

    def _env(self) -> MutableMapping:
        run = _RUN.get()
        return self._base if run is None or run.env is None else run.env

    def __getitem__(self, key: str) -> str:
        return self._env()[key]

    def __setitem__(self, key: str, value: str) -> None:
        self._env()[key] = value

    def __delitem__(self, key: str) -> None:
        del self._env()[key]

    def __iter__(self) -> Iterator[str]:
        return iter(list(self._env()))

    def __len__(self) -> int:
        return len(self._env())

    def __contains__(self, key: object) -> bool:
        return key in self._env()

    def copy(self) -> dict:
        return dict(self._env().items())

    @property
    def base(self) -> MutableMapping:
        return self._base

    def __repr__(self) -> str:
        return f"ContextEnviron({'run' if _RUN.get() is not None else 'process'})"


_install_lock = threading.Lock()


def install() -> ContextEnviron:
    """Make `os.environ` the current run's (once per process: the host's start)."""
    with _install_lock:
        current_env = os.environ
        if isinstance(current_env, ContextEnviron):
            return current_env
        wrapped = ContextEnviron(current_env)
        os.environ = wrapped  # type: ignore[assignment] -- `os.getenv` reads the same global
        return wrapped


def uninstall() -> None:
    """Undo `install` (tests)."""
    with _install_lock:
        if isinstance(os.environ, ContextEnviron):
            os.environ = os.environ.base  # type: ignore[assignment]


#: Path-valued variables a session may set relative to its folder. A
#: per-process worker entered the session's folder before reading them; a hosted
#: run never changes directory, so they are made absolute against it (plan H2).
RELATIVE_PATH_VARS = ("PROBE_CONFIG_PATH", "SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE",
                      "XDG_CONFIG_HOME", "XDG_STATE_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME", "KIMI_CODE_HOME",
                      "CODEX_HOME", "CLAUDE_CONFIG_DIR", "PI_CODING_AGENT_DIR", "PROBE_OUTBOX_DIR", "PROBE_SPOOL_DIR",
                      "PROBE_READS_DIR", "PROBE_DEVICE_ID_PATH", "PROBE_BOX_DIR", "PROBE_BACKFILL_STATE_DIR")


def absolute_paths(env: dict, cwd: str) -> dict:
    """`env` with every relative RELATIVE_PATH_VARS value joined to `cwd`
    (SSL_CERT_DIR is a list of folders: each part)."""
    out = dict(env)
    for name in RELATIVE_PATH_VARS:
        value = out.get(name)
        if not value:
            continue
        parts = value.split(os.pathsep) if name == "SSL_CERT_DIR" else [value]
        # "~/x" is the reader's to expand, as it was before.
        fixed = [p if not p or os.path.isabs(p) or p.startswith("~") else os.path.normpath(os.path.join(cwd, p))
                 for p in parts]
        out[name] = os.pathsep.join(fixed)
    return out
