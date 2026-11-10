"""This process's one console tee: started at ``import probe`` for a script, taken by the run it opens, rotated
when that run closes, and at exit dropped (no run) or sent as the last run's next version (run-logs plan T14/T15).

Imported by ``probe/__init__.py``: stdlib and two light leaves only until a tee starts (the CLI imports probe too).
"""

from __future__ import annotations

import atexit
import contextlib
import os
import sys
import threading
from collections.abc import Callable
from typing import Any

#: The switches that turn the console log off before any run exists (outputs/ reads the same names).
LOG_ENV = "PROBE_CAPTURE_LOG"
OUTPUTS_ENV = "PROBE_CAPTURE_OUTPUTS"
#: `probe.sdk.settings.settings.MODE_ENV`; a disabled process records nothing, so it tees nothing.
MODE_ENV = "PROBE_MODE"
DISABLED_MODE = "disabled"
OFF = frozenset({"0", "false", "no", "off"})
#: `outputs.host_registry.LOG_OWNER_ENV`: a launcher on this host (`probe exec`) tees this process.
LOG_OWNER_ENV = "PROBE_CAPTURE_LOG_OWNER"
#: Set while this process tees itself, for its children: ``dev:inode`` of the stream fd 1 is. A child whose
#: own fd 1 is that stream (a spawn-method worker, a subprocess) already lands in this tee: no second one.
TEED_ENV = "PROBE_CAPTURE_TEED"

#: (exit-time sender) the last finished run's: called with ``(path, stats)`` of what printed after it, or
#: None when nothing more will come (the next run took that output as its head, or the tee stopped or died).
AfterRun = Callable[[Any], None]

_current: ProcessTee | None = None
_lock = threading.Lock()
_is_atexit_armed = False
#: Set while a caller opens a run with capture off and then keeps that run's log itself (`keep_held_window`).
_is_window_kept = False


class ProcessTee:
    """fds 1/2 teed by one helper for this process's life, and which run (if any) owns the file it writes now.
    ``is_held``: no run owns it; nobody keeps it unless one takes it (`take`) or the last run's sender does."""

    def __init__(self, tee: Any, *, is_held: bool) -> None:
        self.tee = tee
        self.pid = os.getpid()
        self.is_held = is_held
        #: The capture window that owns the current file, or None.
        self.owner: object | None = None
        self._after_run: AfterRun | None = None

    @property
    def path(self) -> str:
        return self.tee.log_path

    @property
    def helper_pid(self) -> int | None:
        return self.tee.helper_pid

    @property
    def is_usable(self) -> bool:
        """This process's, and still teeing (the helper did not die)."""
        return self.pid == os.getpid() and self.tee.is_active

    def take(self, owner: object, *, recovery_entry: str | None, should_watch_parent: bool, is_live: bool) -> bool:
        """``owner`` (a run's capture window) owns the current file from here: what was printed so far is its
        head. A held file is adopted through the helper; False when the helper did not answer."""
        if self.owner is not None or not self.is_usable:
            return False
        if self.is_held and not self.tee.adopt(
            recovery_entry=recovery_entry, should_watch_parent=should_watch_parent, is_live=is_live
        ):
            return False
        self.owner, self.is_held = owner, False
        after, self._after_run = self._after_run, None
        if after is not None:
            _call(after, None)  # what printed after the last run is this run's head
        return True

    def release(self, owner: object, *, after_run: AfterRun | None = None) -> tuple[str, dict | None, bool]:
        """``owner``'s run closes: ``(its log's path, stats or None, whether the tee goes on)``. The file is
        finished and the tee goes on into a fresh held one (`InProcessTee.rotate`); ``after_run`` then sends
        what prints next, at exit, unless another run takes it. No answer from the helper: it is stopped, as
        before this existed (`InProcessTee.stop`)."""
        path = self.path
        if owner is not self.owner or not self.is_usable or is_interactive():
            # An interactive session (a REPL now or after the script): what is typed there echoes through stdout and
            # is no run's, so the tee ends with the run, as before T15.
            return path, self.stop(), False
        next_path = _reserve_held_path()
        try:
            stats = self.tee.rotate(next_path) if next_path is not None else None
        except Exception:  # noqa: BLE001 -- the stop below is today's path
            stats = None
        if stats is None:
            stats = self.stop()
            if next_path is not None:
                _remove_files(next_path)
            return path, stats, False
        self.owner, self.is_held = None, True
        self._after_run = after_run
        return path, stats, True

    def stop(self) -> dict | None:
        """Put fds 1/2 back and wait for the current file's stats. The tee is gone for this process, so a
        finished run still waiting for what printed after it is told nothing more comes."""
        global _current
        with _lock:
            if _current is self:
                _current = None
        if os.environ.get(TEED_ENV) == self.tee.get_identity():
            os.environ.pop(TEED_ENV, None)
        self.owner = None
        stats = self.tee.stop()
        self.drop_after_run()
        return stats

    def drop_after_run(self) -> None:
        """The last finished run's sender gets None: it removes its kept local copy (never a forked copy's)."""
        if self.pid != os.getpid():
            return
        after, self._after_run = self._after_run, None
        if after is not None:
            _call(after, None)

    def finish_at_exit(self) -> None:
        """Interpreter exit: a held file nobody keeps is dropped (no wait); one that holds what printed after
        the last run finished goes to that run's sender. A file a run still owns is that run's close's, or its
        recovery's (the helper hands it on at EOF)."""
        if self.pid != os.getpid() or self.owner is not None:
            return
        after, self._after_run = self._after_run, None
        if after is not None and is_interactive():
            _call(after, None)  # a REPL ran after the run (`PYTHONINSPECT` set late): what was typed is never sent
            after = None
        if not self.tee.is_active:
            if after is not None:
                _call(after, None)  # the helper is gone: nothing more to read; the kept copy goes
            return
        if after is None:
            self.tee.discard()
            return
        path = self.path
        _call(after, (path, self.stop()))

    def end_window(self) -> None:
        """A run opened with its log off: nothing printed from here is any run's. What printed after the last
        run goes to that run now; a held file no run took is dropped. Either way the tee stops."""
        if self.pid != os.getpid() or self.owner is not None:
            return
        after, self._after_run = self._after_run, None
        if after is None:
            self.tee.discard()
            self.stop()
            return
        path = self.path
        _call(after, (path, self.stop()))


def get_current() -> ProcessTee | None:
    """This process's tee while it is teeing, else None (another process's, after a fork, is not)."""
    tee = _current
    return tee if tee is not None and tee.is_usable else None


def start_at_import() -> None:
    """Called by ``import probe``: start a held tee when :func:`should_start_at_import`. Never raises, never
    blocks a script on a failure: a run then starts its own tee at ``probe.init()``, as before."""
    try:
        if should_start_at_import():
            path = _reserve_held_path()
            if path is not None:
                _start(path, is_held=True)
    except Exception:  # noqa: BLE001 -- capture is never a reason for a script not to run
        pass


@contextlib.contextmanager
def keep_held_window():
    """Around a run opened with capture off whose log the caller then keeps itself (a Miles driver: files off,
    log on, T17): its opt-out is not the person's, so the held tee waits for that log to take it."""
    global _is_window_kept
    previous, _is_window_kept = _is_window_kept, True
    try:
        yield
    finally:
        _is_window_kept = previous


def end_held_window() -> None:
    """A run opened with its log off (``capture_outputs=False``, ``PROBE_CAPTURE_LOG=0`` set after the import, a
    disabled run): the tee no run owns stops (`ProcessTee.end_window`). Never raises."""
    if _is_window_kept:
        return
    try:
        running = get_current()
        if running is not None:
            running.end_window()
    except Exception:  # noqa: BLE001 -- an opt-out never costs the run
        pass


def start_for_run(path: str, *, recovery_entry: str | None, should_watch_parent: bool) -> ProcessTee:
    """A tee started at a run's open (nothing started one at import): owned from its first byte."""
    return _start(path, is_held=False, recovery_entry=recovery_entry, should_watch_parent=should_watch_parent)


def should_start_at_import() -> bool:
    """A Python source file outside the probe package and the installed packages runs as ``__main__`` (a
    script, not the ``probe`` console script or a tool's ``-m``) and imports probe as it loads its modules,
    on posix, with fds 1/2 behind ``sys.stdout``/``sys.stderr``, the log not switched off, no REPL to follow
    (`is_interactive`), and no tee already: neither one this process started nor one a parent's stream
    carries (`TEED_ENV`) nor a launcher's on this host."""
    if os.name != "posix" or not sys.executable or get_current() is not None:
        return False
    if (os.environ.get(LOG_ENV) or "").strip().lower() in OFF:
        return False
    if (os.environ.get(OUTPUTS_ENV) or "").strip().lower() in OFF:
        return False
    if (os.environ.get(MODE_ENV) or "").strip().lower() == DISABLED_MODE:
        return False
    if not is_fd_behind_streams() or _is_teed_already() or is_interactive():
        return False
    return _is_script_main() and _is_imported_by_module_code()


def is_interactive() -> bool:
    """A person types into this process: a REPL now or after the script (``python -i``, ``PYTHONINSPECT``, the
    plain REPL, IPython). What they type echoes through stdout, so no tee runs outside a run's own window."""
    if sys.flags.interactive or sys.flags.inspect or os.environ.get("PYTHONINSPECT") or hasattr(sys, "ps1"):
        return True
    ipython = sys.modules.get("IPython")
    try:
        return ipython is not None and ipython.get_ipython() is not None
    except Exception:  # noqa: BLE001 -- an IPython that cannot say is not a session
        return False


def is_fd_behind_streams() -> bool:
    """``sys.stdout``/``sys.stderr`` write to fds 1/2: what an fd-level tee needs. A notebook kernel's
    streams are not (their ``fileno()`` is another fd or raises), and neither is a redirect inside Python."""
    try:
        return sys.stdout.fileno() == 1 and sys.stderr.fileno() == 2
    except (AttributeError, ValueError, OSError):
        return False


def _is_teed_already() -> bool:
    owner = (os.environ.get(LOG_OWNER_ENV) or "").strip()
    if owner:
        import socket

        if owner == socket.gethostname():
            return True
    inherited = os.environ.get(TEED_ENV)
    return bool(inherited) and inherited == _get_identity_text(1)


def _get_identity_text(fd: int) -> str | None:
    try:
        info = os.fstat(fd)
    except OSError:
        return None
    return f"{info.st_dev}:{info.st_ino}"


def _is_script_main() -> bool:
    path = getattr(sys.modules.get("__main__"), "__file__", None)
    if not isinstance(path, str) or not path.endswith(".py"):
        return False  # a console script (`probe`), `-c`, a REPL, a spawn child's bootstrap
    real = os.path.realpath(path)
    return not any(_is_within(real, root) for root in _list_installed_roots())


#: Import machinery between `probe/__init__` and the code that asked for it (`_frozen_importlib` is how the
#: interpreter's own copy names itself; runpy runs `python -m`).
_IMPORT_MACHINERY = frozenset(
    {"_frozen_importlib", "_frozen_importlib_external", "importlib", "importlib._bootstrap",
     "importlib._bootstrap_external", "runpy"}
)


def _is_imported_by_module_code() -> bool:
    """probe is imported while modules load (a script's own imports, or a library it imports at its top),
    not from inside a function: a tool reaching for probe on demand (an agent hook that finds the state
    folder through it) is not a run's work, and a helper per hook call would slow every one of them."""
    try:
        frame = sys._getframe(1)
    except (AttributeError, ValueError):
        return True
    while frame is not None:
        name = frame.f_globals.get("__name__")
        if frame.f_code.co_name != "<module>" and name != __name__ and name not in _IMPORT_MACHINERY:
            return False
        frame = frame.f_back
    return True


def _list_installed_roots() -> list[str]:
    """Where code this script did not write lives: the probe package, the installed packages, the stdlib."""
    import site

    roots = [os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))]
    roots.append(os.path.dirname(os.__file__))
    try:
        roots += list(site.getsitepackages())
        roots.append(site.getusersitepackages())
    except Exception:  # noqa: BLE001 -- an embedded interpreter's site may lack them
        pass
    return [os.path.realpath(root) for root in roots if root]


def _is_within(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


def get_logs_dir() -> str:
    """Where this process's console logs are written: `outputs.log.reserve_log_path`'s folder."""
    from ....foundation.durable import homedir

    directory = homedir.state_base() / "probe" / "logs"
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    return str(directory)


def _reserve_held_path() -> str | None:
    """A fresh file for output no run owns yet, or None (an unwritable state folder)."""
    import tempfile

    try:
        fd, path = tempfile.mkstemp(prefix=f"held.{os.getpid()}.", suffix=".log", dir=get_logs_dir())
    except OSError:
        return None
    os.close(fd)
    return path


def _remove_files(path: str) -> None:
    """A log file and every control file beside it."""
    for suffix in ("", ".meta.json", ".ready", ".stopped", ".adopt", ".adopted", ".rotate", ".discard", ".late"):
        try:
            os.unlink(path + suffix)
        except OSError:
            pass


def _start(
    path: str, *, is_held: bool, recovery_entry: str | None = None, should_watch_parent: bool = False
) -> ProcessTee:
    global _current, _is_atexit_armed
    from .tee import InProcessTee

    tee = InProcessTee(path, recovery_entry=recovery_entry, should_watch_parent=should_watch_parent, is_held=is_held)
    try:
        tee.start()
    except BaseException:
        if is_held:
            _remove_files(path)
        raise
    process_tee = ProcessTee(tee, is_held=is_held)
    identity = tee.get_identity()
    if identity:
        os.environ[TEED_ENV] = identity
    with _lock:
        replaced, _current = _current, process_tee
        if not _is_atexit_armed:
            # Registered once: at import it runs after every exit hook a run installs later (LIFO).
            atexit.register(_finish_at_exit)
            _is_atexit_armed = True
    if replaced is not None:
        replaced.drop_after_run()  # its helper died: nothing more comes for the run it held output for
    return process_tee


def _finish_at_exit() -> None:
    process_tee = _current
    if process_tee is None:
        return
    try:
        process_tee.finish_at_exit()
    except BaseException:  # noqa: BLE001 -- interpreter teardown
        pass


def _call(callback: AfterRun, value: Any) -> None:
    try:
        callback(value)
    except Exception:  # noqa: BLE001 -- what printed after a run never costs the next one
        pass


def _reset_after_fork() -> None:
    # A thread may have held the lock at the fork. The child keeps the parent's ProcessTee object but not
    # its tee: `is_usable` (the pid) keeps it from ever rotating or stopping the parent's helper.
    global _lock
    _lock = threading.Lock()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_after_fork)
