"""After a switch to a new version, make sure it runs; else switch back (plan D5).

    python -I -m probe.service.guard --from <version> --to <version> --old-python <path>
                                     [--old-pid <pid> --old-start <start time>]

Spawned detached by the service that just updated the CLI side by side
(`updater.py`, step `self`), from its OWN interpreter -- the version being
replaced, which stays on disk (`probe._shared.installs`) -- right before that
service exits for the new code. Then:

    1. wait for the old service (`--old-pid`, that exact process) to exit
       (at most GONE_S); without it, for its lock to be free
    2. start the new one (`client.ensure`, with runtime.json's interpreter:
       the new version) -- or take the one a tap or an app started first --
       and wait for it to answer `service.hello` as `--to` (at most START_S)
    3. watch it keep answering for WATCH_S, on one keep-alive connection: an
       idle service would otherwise rightly stop within the watch, and read
       as failed

All three pass: done, nothing to do (`guard.json` says ok). Any fails -- it
would not start, crashed, answered as another version, stopped answering --
the guard switches the tool path back to the previous version, points
`runtime.json` at it, marks `--to` rejected on this machine (the next update
skips it until a newer release), stops whatever runs of the new version, and
starts the service again on the old one. `guard.json` keeps what happened;
the service reports it in `update.status` and `probe doctor`.

Stdlib only, like everything the service starts with.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import signal
import sys
import time

from . import client, paths
from .protocol import Client, Method

GONE_S = 30.0
START_S = 45.0
WATCH_S = 60.0
POLL_S = 0.5
#: How long a stopped new service has to let go of the lock before SIGKILL.
STOP_WAIT_S = 10.0
GUARD_NAME = "guard.json"
#: Why the last service stopped (`record_stop`, written by the service itself
#: on its way out): a crash or a kill writes none.
LAST_STOP_NAME = "last-stop.json"
#: Deliberate restarts of the new service a watch goes on through (a newer tap,
#: a person's stop); past this many it reads as a restart loop.
MAX_RESTARTS = 3
#: Test-only overrides (the lifecycle's own pattern). Nothing in production sets them.
WATCH_ENV = "PROBE_SERVICE_GUARD_WATCH_S"


def log(message: str) -> None:
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with contextlib.suppress(OSError, ValueError):
        sys.stderr.write(f"[{stamp}] probe-service-guard[{os.getpid()}]: {message}\n")
        sys.stderr.flush()


def guard_path():
    return paths.service_dir() / GUARD_NAME


def write(record: dict) -> None:
    target = guard_path()
    tmp = target.with_name(f"{target.name}.{os.getpid()}.tmp")
    try:
        paths.private_dir(target.parent)
        with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as handle:
            json.dump(record, handle)
        os.replace(tmp, target)
    except OSError:
        pass
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


def record_stop(reason: str, version: str) -> None:
    """The service is stopping on purpose (`server.stop`): say so, for a guard
    watching it. Never raises."""
    from . import procid

    target = paths.service_dir() / LAST_STOP_NAME
    tmp = target.with_name(f"{target.name}.{os.getpid()}.tmp")
    try:
        with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as handle:
            json.dump({"pid": os.getpid(), "start": procid.start_time(os.getpid()), "reason": reason,
                       "version": version, "at": time.time()}, handle)
        os.replace(tmp, target)
    except OSError:
        pass
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


def last_stop() -> dict | None:
    try:
        data = json.loads((paths.service_dir() / LAST_STOP_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def read() -> dict | None:
    try:
        data = json.loads(guard_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _lock_free() -> bool:
    import fcntl

    try:
        fd = os.open(paths.lock_path(), os.O_RDWR | os.O_CREAT, 0o600)
    except OSError:
        return False
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return False
    else:
        fcntl.flock(fd, fcntl.LOCK_UN)
        return True
    finally:
        os.close(fd)


def _hello() -> dict | None:
    conn = client.connect(2.0)
    if conn is None:
        return None
    try:
        return conn.hello(Client.CLI, "guard")
    except (OSError, ValueError, client.ServiceError):
        return None
    finally:
        conn.close()


def _keepalive() -> tuple[object, dict] | None:
    """A keep-alive connection to whatever answers now, and its hello."""
    conn = client.connect(2.0)
    if conn is None:
        return None
    try:
        return conn, conn.hello(Client.CLI, "guard", keepalive=True)
    except (OSError, ValueError, client.ServiceError):
        conn.close()
        return None


def holder() -> tuple[int, str] | None:
    """The service holding the lock now, as it named itself in the lock file
    (`server._name_holder`): `(pid, start time)` when that process still runs."""
    from . import procid

    try:
        pid_s, _, start = paths.lock_path().read_text(encoding="utf-8").strip().partition(" ")
        pid = int(pid_s)
    except (OSError, ValueError):
        return None
    if pid <= 1 or pid == os.getpid() or not start or procid.alive(pid, start) is not True:
        return None
    return pid, start


def _gone(pid: int | None, start: str | None):
    from . import procid

    if pid and start:
        return lambda: procid.alive(pid, start) is False
    return _lock_free


def _wait(predicate, seconds: float):
    deadline = time.monotonic() + seconds
    while True:
        value = predicate()
        if value or time.monotonic() >= deadline:
            return value
        time.sleep(POLL_S)


def check(to_version: str, *, watch_s: float, old_pid: int | None = None, old_start: str | None = None) -> str | None:
    """None when `to_version` started and kept answering; else why not."""
    if not _wait(_gone(old_pid, old_start), GONE_S):
        return "the previous service did not exit"

    def answered():
        found = _keepalive()
        if found is None:
            # Start it, and connect the moment it listens: a service with
            # nothing to hold it may not wait for the next poll.
            client.ensure(wait=2.0)
            found = _keepalive()
        return found

    # `ensure` starts at most 3 services a minute: its back-off may outlast START_S.
    found = _wait(answered, START_S + client.START_WINDOW_S)
    if found is None:
        return f"the new service did not answer within {START_S + client.START_WINDOW_S:.0f} s"
    conn, first = found
    try:
        if first.get("service_version") != to_version:
            return f"the service answered as {first.get('service_version')}, not {to_version}"
        pid = first.get("pid")
        restarts = 0
        deadline = time.monotonic() + watch_s
        while time.monotonic() < deadline:
            time.sleep(POLL_S)
            try:
                conn.call(Method.STATUS)
                continue
            except (OSError, ValueError, client.ServiceError):
                pass
            stopped = last_stop()
            if stopped is not None and stopped.get("pid") == pid:
                # It stopped on purpose: a newer tap, a person, the OS -- not a crash.
                reason = stopped.get("reason")
                if reason == "update":
                    return None  # a newer CLI again: its own guard watches that one
                restarts += 1
                if restarts > MAX_RESTARTS:
                    return f"the new service restarted {restarts} times in its watch ({reason})"
                with contextlib.suppress(Exception):
                    conn.close()
                # Its restarts count against `ensure`'s 3 starts a minute: wait
                # out that window too before calling it gone.
                found = _wait(answered, START_S + client.START_WINDOW_S)
                if found is None:
                    return f"the new service did not come back after it stopped ({reason})"
                conn, again = found
                if again.get("service_version") != to_version:
                    return f"after it stopped ({reason}) the service answered as {again.get('service_version')}"
                pid = again.get("pid")
                log(f"the new service restarted on purpose ({reason}); watching pid {pid}")
                continue
            hello = _hello()
            if hello is None:
                return "the new service stopped answering"
            if hello.get("pid") != pid:
                return "the new service restarted (it crashed)"
            return "the new service dropped its connection"
        return None
    finally:
        with contextlib.suppress(Exception):
            conn.close()


def _stop_new(old_python: str) -> None:
    """Stop the new version's service: the one holding the lock (it named
    itself there; one that hangs answers nothing), else whatever answers.
    SIGTERM, then SIGKILL when it has not let go of the lock within STOP_WAIT_S."""
    found = holder()
    if found is None:
        hello = _hello()
        pid = hello.get("pid") if hello else None
        if not isinstance(pid, int) or pid <= 1:
            return
    else:
        pid = found[0]
    with contextlib.suppress(ProcessLookupError, PermissionError):
        os.kill(pid, signal.SIGTERM)
    if _wait(_lock_free, STOP_WAIT_S):
        return
    if found is not None and holder() == found:
        log(f"the new service (pid {pid}) did not stop: killing it")
        with contextlib.suppress(ProcessLookupError, PermissionError):
            os.kill(pid, signal.SIGKILL)
        _wait(_lock_free, 5.0)


def _hand_over_workers() -> None:
    """The new version runs: ask every live session's daemon worker, still on
    the old one, to hand over at its next safe point (its supervisor starts it
    again through `probe`, the new version). Never raises."""
    try:
        from . import updater
        from .registry import Registry

        registry = Registry(paths.registry_path())
        registry.load()
        asked = updater.hand_over_workers(updater.state_dirs(registry.state_dirs()))
        if asked:
            log(f"asked {asked} daemon worker(s) to move to the new version")
    except Exception as exc:  # noqa: BLE001 -- they move at their sessions' next restart
        log(f"could not ask the daemon workers to move: {exc!r}")


def switch_back(from_version: str, to_version: str, old_python: str, why: str) -> dict:
    from probe._shared import installs

    record: dict = {"at": time.time(), "from": from_version, "to": to_version, "ok": False, "reason": why}
    try:
        done = installs.switch_back()
    except Exception as exc:  # noqa: BLE001 -- say so; nothing else can be done here
        record["rollback"] = f"failed: {exc!r}"[:500]
        log(f"switch back failed: {exc!r}")
        write(record)
        return record
    if done is None:
        record["rollback"] = "no previous version to switch back to"
        write(record)
        return record
    installs.reject(to_version, why)
    with contextlib.suppress(Exception):
        client.write_runtime(old_python, from_version)
    _stop_new(old_python)
    client.ensure()
    back = _wait(_hello, START_S)
    record["rollback"] = "done"
    record["active"] = done.get("active")
    record["answering"] = back.get("service_version") if back else None
    if not back or back.get("service_version") != from_version:
        record["rollback"] = f"switched back, but {from_version} does not answer"
    write(record)
    log(f"switched back to {from_version}: {why} ({record['rollback']})")
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m probe.service.guard")
    parser.add_argument("--from", dest="from_version", required=True)
    parser.add_argument("--to", dest="to_version", required=True)
    parser.add_argument("--old-python", required=True)
    parser.add_argument("--old-pid", type=int, default=None)
    parser.add_argument("--old-start", default=None)
    args = parser.parse_args(argv)
    raw = os.environ.get(WATCH_ENV)
    try:
        watch_s = float(raw) if raw else WATCH_S
    except ValueError:
        watch_s = WATCH_S
    write({"at": time.time(), "from": args.from_version, "to": args.to_version, "ok": None, "state": "watching"})
    why = check(args.to_version, watch_s=watch_s, old_pid=args.old_pid, old_start=args.old_start)
    if why is None:
        write({"at": time.time(), "from": args.from_version, "to": args.to_version, "ok": True})
        log(f"{args.to_version} runs")
        _hand_over_workers()
        return 0
    log(f"{args.to_version} failed its check: {why}")
    switch_back(args.from_version, args.to_version, args.old_python, why)
    return 1


if __name__ == "__main__":
    sys.exit(main())
