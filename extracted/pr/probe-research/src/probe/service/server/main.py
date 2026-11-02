"""`python -m probe.service`: one instance per machine (the life-long lock), bind the socket, log, then serve."""

from __future__ import annotations

import asyncio
import contextlib
import os
import sys
import threading

from ...foundation.service_api import paths
from ..sessions.sessions import HEARTBEAT_TTL_S, Registry
from ..watch.incident import Family
from ..watch.bounds import log_traceback
from probe.service.server.legacy_door import LegacyDoor, _bind, _take_lock
from probe.service.server.lifecycle import STOPPING_NAME
from probe.service.server.policy import _env_float, _version, log
from probe.service.server.server import DISCOVERY_S, GRACE_S, Service
#: Test-only overrides (API v1, "Lifecycle"). Nothing in production sets them.
GRACE_ENV = "PROBE_SERVICE_GRACE_S"
DISCOVERY_ENV = "PROBE_SERVICE_DISCOVERY_S"
TTL_ENV = "PROBE_SERVICE_TTL_S"
#: The log is cut over to `service.log.1` at start once it passes this.
MAX_LOG_BYTES = 256 * 1024


# -- process entry ------------------------------------------------------------


def _open_log() -> int | None:
    path = paths.log_path()
    try:
        if path.stat().st_size > MAX_LOG_BYTES:
            os.replace(path, path.with_name(path.name + ".1"))
    except OSError:
        pass
    try:
        return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0), 0o600)
    except OSError:
        return None


def _name_holder(fd: int) -> None:
    """Write `<pid> <start time>` into the lock file this service holds: the
    guard (D5) finds a replacement that hangs without answering there, and
    stops that exact process (`guard.holder`). Never raises."""
    from ...foundation.service_api import procid

    with contextlib.suppress(OSError):
        os.ftruncate(fd, 0)
        os.lseek(fd, 0, os.SEEK_SET)
        os.write(fd, f"{os.getpid()} {procid.start_time(os.getpid()) or ''}\n".encode())


def _thread_exception(service: Service, args) -> None:
    """`threading.excepthook`: never raises."""
    try:
        if args.exc_type is SystemExit:
            return
        import traceback

        text = "".join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback))
        name = args.thread.name if args.thread is not None else "?"
        # A thread's name carries a pid or a counter: its site is the name without digits.
        site = "".join(ch for ch in name if not ch.isdigit())
        log_traceback(log, f"thread {name}: unhandled {args.exc_type.__name__}", text, gate=service._tracebacks,
                      key=("thread", site, args.exc_type.__name__))
        service.watch.note(Family.SERVICE_ERROR, "thread_exception", facts={
            "thread": name, "type": args.exc_type.__name__, "traceback": text,
        })
    except Exception:  # noqa: BLE001
        pass


def run_service() -> int:
    """`python -m probe.service`: one instance; exits 0 when idle or as a duplicate.
    Never while `probe uninstall` runs (its barrier is LIVE): exits 0 at once,
    before it makes a folder or writes a file."""
    from ...foundation import service_api as client

    if client.uninstall_barrier() is not None:
        with contextlib.suppress(OSError, ValueError):
            print(f"probe service: not started: {client.UNINSTALLING_MESSAGE}", file=sys.stderr)
        return 0
    try:
        sock_path = paths.ensure_dirs()
    except OSError as exc:
        log(f"cannot use {paths.service_dir()}: {exc}")
        return 1
    lock_fd = _take_lock()
    if lock_fd is None:
        return 0  # another service runs: this one is the duplicate
    from .. import watch

    # The service before this one, as it named itself in the lock file: read
    # before this one names itself there (crash-report plan B2).
    previous = watch.previous_holder()
    _name_holder(lock_fd)
    log_fd = _open_log()
    if log_fd is not None and not os.isatty(2):
        os.dup2(log_fd, 1)
        os.dup2(log_fd, 2)
    with contextlib.suppress(Exception):
        import faulthandler

        # A fatal signal's traceback (a crash in C, an abort) lands in service.log too.
        faulthandler.enable(file=sys.stderr, all_threads=True)
    with contextlib.suppress(OSError):
        (paths.service_dir() / STOPPING_NAME).unlink()
    # How it ended: no stop record on this boot, or a recorded crash, is a
    # `service_crash` to report (`watch.last_run`; this one's own record next).
    crashed = watch.last_run(previous, _version())
    if paths.WINDOWS:
        listen, bound = paths.pipe_name(), None
    else:
        try:
            listen = _bind(sock_path)
        except OSError as exc:
            log(f"cannot bind {sock_path}: {exc}")
            watch.record_crash(f"cannot bind the socket: {exc}", "")
            return 1
        bound = os.stat(sock_path)
    registry = Registry(paths.registry_path(), ttl=_env_float(TTL_ENV, HEARTBEAT_TTL_S))
    service = Service(
        registry=registry,
        grace_s=_env_float(GRACE_ENV, GRACE_S),
        discovery_s=_env_float(DISCOVERY_ENV, DISCOVERY_S),
        legacy=None if paths.WINDOWS else LegacyDoor(),
    )
    if crashed is not None:
        why = crashed.pop("reason")
        service.statepost.crashed = why
        log(f"the service before this one ended without stopping ({why}): reported once consent allows")
        service.watch.note(Family.SERVICE_CRASH, why, facts=crashed)
    # A thread's unhandled exception: logged with its traceback, and counted
    # for `service_error` (crash-report plan B2).
    threading.excepthook = lambda args: _thread_exception(service, args)
    try:
        reason = asyncio.run(service.run(listen))
    except Exception as exc:  # noqa: BLE001
        import traceback

        text = traceback.format_exc()
        log_traceback(log, f"crashed: {exc!r}", text)
        # What the next service reports (`watch.last_run`): this one wrote no stop record.
        watch.record_crash(repr(exc), text)
        reason = "crash"
    finally:
        # Unlink only OUR socket, and before the lock goes (process exit): a new
        # service can bind only after that, so this never removes its socket.
        with contextlib.suppress(OSError):
            st = os.stat(sock_path)
            if bound is not None and (st.st_dev, st.st_ino) == (bound.st_dev, bound.st_ino):
                os.unlink(sock_path)
        with contextlib.suppress(OSError):
            (paths.service_dir() / STOPPING_NAME).unlink()
    log(f"exited ({reason})")
    return 0 if reason != "crash" else 1
