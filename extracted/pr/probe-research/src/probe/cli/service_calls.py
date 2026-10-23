"""What the CLI asks the Probe service, for the local work the service owns.

    view()              `probe status` and `probe doctor`: is it running (its
                        version, pid, state), the sessions it has registered
                        and their mode, the recorders it runs, its warm hook
                        hosts, the runs `probe exec` holds, and its updater
                        (a cycle running, the last check, a deferral)
    finish_recorders()  `probe capture off` for one agent: the recorders it
                        runs for that agent finish now, not at their next
                        killswitch check
    hold_run() / release_run()
                        `probe exec`: its run, so the updater's quiet check
                        sees it without a lock-file scan
    refresh_manifest()  the every-command version check: the service refreshes
                        a stale manifest cache instead of a detached child

Each one never STARTS the service (an agent session, the desktop app or
`probe service start` does), is bounded by a short timeout, never raises, and
returns "no answer" when no service answers -- or one from before its method,
or on Windows, where none runs -- and the caller then does what it did before.
The service is on this machine (a Unix socket in a folder only this user can
write): none of this is a network call, and with no socket file there (no
service runs) no socket is even opened.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field

from probe._compat import StrEnum

#: `probe status` / `probe doctor`: the whole read, every call included.
VIEW_TIMEOUT_S = 1.0
#: `probe exec`'s hold and release: on the path to the wrapped command's start.
HOLD_TIMEOUT_S = 0.5
#: The every-command check: it must never stall a command (a `probe log` in a
#: training loop); the service answers at once and refreshes in a child.
MANIFEST_TIMEOUT_S = 0.5
#: `probe capture off`: how long the service's recorders get to finish.
FINISH_WAIT_S = 5.0
#: ... and how long the call may take beyond that.
FINISH_TIMEOUT_S = 2.0

#: What a person is told when no service runs.
STARTS_WITH = "it starts with the next coding-agent session, or run `probe service start`"


class Reach(StrEnum):
    """`service.reach` in `probe status --json`."""

    ANSWERED = "answered"
    #: Nothing answers at its socket: none runs (or it is restarting).
    NOT_RUNNING = "not_running"
    #: It refused the call, or its folder is not this user's alone.
    REFUSED = "refused"
    #: It did not answer in time, or answered something unreadable.
    UNREACHABLE = "unreachable"
    #: No service on this platform yet (Windows).
    UNSUPPORTED = "unsupported"


def _version() -> str:
    try:
        from probe import __version__

        return str(__version__)
    except Exception:  # noqa: BLE001
        return "unknown"


def _reachable() -> bool:
    """POSIX, and a service socket file to connect to (this machine's, or the
    one a service from before the machine key listens on). No file, no
    socket opened: a machine where no service runs pays two `stat`s."""
    if os.name != "posix":
        return False
    try:
        from probe.service import paths

        return any(path.exists() for path in (paths.socket_path(), paths.legacy_socket_path()))
    except Exception:  # noqa: BLE001 -- then the connect below says what is wrong
        return True


# -- view ------------------------------------------------------------------------


def _blank(reach: Reach, error: str | None = None) -> dict:
    return {
        "reach": reach.value,
        "running": {Reach.ANSWERED: True, Reach.NOT_RUNNING: False}.get(reach),
        "error": error,
        "version": None,
        "pid": None,
        "state": None,
        "started_at": None,
        "sessions": [],
        "recorders": [],
        "hook_hosts": [],
        "runs": [],
        "update": dict.fromkeys(
            (
                "enabled",
                "in_progress",
                "step",
                "last_check",
                "last_ok",
                "next_check",
                "deferred_reason",
                "deferred_at",
                "deferred_since",
            )
        ),
    }


def _of(value: object, kind: type | tuple) -> object:
    """`value` when it is of `kind` (never a bool for a number), else None."""
    if isinstance(value, bool) and kind is not bool:
        return None
    return value if isinstance(value, kind) else None


def _rows(items: object, keys: dict) -> list[dict]:
    """Each object of `items`, cut to `keys` (`name: kind`), unreadable ones dropped."""
    if not isinstance(items, list):
        return []
    return [{name: _of(item.get(name), kind) for name, kind in keys.items()} for item in items if isinstance(item, dict)]


def _filled(status: dict, listing: object) -> dict:
    out = _blank(Reach.ANSWERED)
    number = (int, float)
    out.update(
        version=_of(status.get("service_version"), str),
        pid=_of(status.get("pid"), int),
        state=_of(status.get("state"), str),
        started_at=_of(status.get("started_at"), number),
        sessions=_rows(
            listing.get("sessions") if isinstance(listing, dict) else None,
            {"sid": str, "harness": str, "mode": str, "alive": bool},
        ),
        recorders=_rows(status.get("recorders"), {"sid": str, "alive": bool, "last": str, "failures": int}),
        hook_hosts=_rows(status.get("hook_hosts"), {"root": str, "pid": int}),
        runs=_rows(status.get("runs"), {"run": str, "pid": int, "since": number}),
    )
    update = status.get("update")
    if isinstance(update, dict):
        last = update.get("last_result")
        deferred = update.get("deferred")
        deferred = deferred if isinstance(deferred, dict) else {}
        out["update"] = {
            "enabled": _of(update.get("enabled"), bool),
            "in_progress": _of(update.get("in_progress"), bool),
            "step": _of(update.get("step"), str),
            "last_check": _of(update.get("last_check"), number),
            "last_ok": _of(last.get("ok"), bool) if isinstance(last, dict) else None,
            "next_check": _of(update.get("next_check"), number),
            "deferred_reason": _of(deferred.get("reason"), str),
            "deferred_at": _of(deferred.get("at"), number),
            "deferred_since": _of(update.get("deferred_since"), number),
        }
    return out


def view(timeout: float = VIEW_TIMEOUT_S) -> dict:
    """The service's own view (`service` in `probe status --json`), within
    `timeout` seconds in all. Never starts it, never raises."""
    if os.name != "posix":
        return _blank(Reach.UNSUPPORTED)
    if not _reachable():
        return _blank(Reach.NOT_RUNNING)
    try:
        from probe.service import client
        from probe.service.protocol import Client, Method
    except Exception as exc:  # noqa: BLE001 -- a status read never raises
        return _blank(Reach.UNREACHABLE, f"the service client could not load ({type(exc).__name__})")
    deadline = time.monotonic() + timeout

    def left(conn) -> None:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError
        conn.sock.settimeout(remaining)

    try:
        with client.Connection.open(timeout) as conn:
            left(conn)
            conn.hello(Client.CLI, _version())
            left(conn)
            status = conn.call(Method.STATUS)
            left(conn)
            listing = conn.call(Method.SESSION_LIST)
    except (FileNotFoundError, ConnectionRefusedError):
        return _blank(Reach.NOT_RUNNING)
    except PermissionError:
        return _blank(Reach.REFUSED, "its folder is not private to this user, so Probe will not ask it")
    except client.ServiceError as exc:
        return _blank(Reach.REFUSED, exc.message or f"error {exc.code}")
    except TimeoutError:
        return _blank(Reach.UNREACHABLE, f"it did not answer within {timeout:g} s")
    except (OSError, ValueError) as exc:
        return _blank(Reach.UNREACHABLE, f"the connection failed ({exc})" if str(exc) else "the connection failed")
    if not isinstance(status, dict):
        return _blank(Reach.UNREACHABLE, "its answer could not be read")
    return _filled(status, listing)


def when(epoch: object) -> str:
    if not isinstance(epoch, (int, float)) or isinstance(epoch, bool):
        return "never"
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(epoch))


def _count(n: int, word: str) -> str:
    return f"{n} {word}" + ("" if n == 1 else "s")


def summary(view_: dict | None) -> str:
    """One line for a person (`probe status`)."""
    if not isinstance(view_, dict):
        return "unknown"
    reach = view_.get("reach")
    if reach == Reach.NOT_RUNNING:
        return f"not running ({STARTS_WITH})"
    if reach == Reach.UNSUPPORTED:
        return "does not run on this system yet"
    if reach != Reach.ANSWERED:
        return f"{reach or 'unknown'}: {view_.get('error') or 'no answer'}"
    parts = [str(view_.get("state") or "running")]
    if view_.get("version"):
        parts.append(str(view_["version"]))
    if view_.get("pid"):
        parts.append(f"pid {view_['pid']}")
    sessions = [s for s in view_.get("sessions") or [] if s.get("alive")]
    parts.append(_count(len(sessions), "live session"))
    recorders = view_.get("recorders") or []
    if recorders:
        parts.append(f"{len(recorders)} recorded by it")
    runs = view_.get("runs") or []
    if runs:
        parts.append(_count(len(runs), "run") + " in flight")
    update = view_.get("update") or {}
    if update.get("in_progress"):
        parts.append(f"updating now ({update.get('step') or 'starting'})")
    elif update.get("deferred_reason"):
        parts.append(f"update deferred: {update['deferred_reason']}")
    return " · ".join(parts)


def update_text(update: dict) -> str:
    """The updater in one line (`probe doctor`)."""
    if update.get("in_progress"):
        return f"updating now ({update.get('step') or 'starting'})"
    parts = []
    if update.get("enabled") is False:
        parts.append("automatic updates off")
    verdict = {True: " (ok)", False: " (failed)"}.get(update.get("last_ok"), "")
    parts.append(f"last check {when(update.get('last_check'))}{verdict}")
    if update.get("enabled") and update.get("next_check") is not None:
        parts.append(f"next {when(update.get('next_check'))}")
    return ", ".join(parts)


# -- capture off -------------------------------------------------------------------


@dataclass
class Finished:
    """What `recorders.finish` did: the sessions whose recorder finished, and
    those still finishing when the wait ran out. `error`: the service runs but
    could not be asked, or not confirmed (no answer in time, a refusal, an
    older service that hosts recorders): a recorder it hosts may still be
    uploading, so the caller must not call capture off."""

    finished: list[str] = field(default_factory=list)
    unfinished: list[str] = field(default_factory=list)
    error: str | None = None


def finish_recorders(harness: str, *, wait: float | None = None) -> Finished | None:
    """Ask the service to finish every recorder it runs for `harness` (an
    agent's registry id), waiting up to `wait` (FINISH_WAIT_S) for them.

    None ONLY when no service runs (no socket file, or nothing listening at
    it, or Windows): then it hosts nothing. A service that runs and does not
    confirm is a `Finished` with `error`, never None. One from before
    `recorders.finish` is asked what it records: nothing is a confirmed none."""
    if not _reachable():
        return None
    from probe.service import client
    from probe.service.protocol import ErrorCode

    try:
        answer = client.finish_recorders(
            harness, wait=FINISH_WAIT_S if wait is None else wait, client_version=_version(),
            timeout=FINISH_TIMEOUT_S,
        )
    except (FileNotFoundError, ConnectionRefusedError):
        return None  # a socket file nobody listens at: no service, nothing hosted
    except client.ServiceError as exc:
        if exc.code == ErrorCode.UNKNOWN_METHOD:
            return _older_service()
        return Finished(error=f"the Probe service refused ({exc.message or exc.code})")
    except Exception as exc:  # noqa: BLE001 -- a timeout, a broken connection: not confirmed
        return Finished(error=f"the Probe service did not answer ({type(exc).__name__})")
    finished, unfinished = answer.get("finished"), answer.get("unfinished")
    if not isinstance(finished, list) or not isinstance(unfinished, list):
        return Finished(error="the Probe service's answer could not be read")
    return Finished(
        [s for s in finished if isinstance(s, str)], [s for s in unfinished if isinstance(s, str)]
    )


def _older_service() -> Finished:
    """A service from before `recorders.finish`: hosting nothing is a confirmed
    none; hosting anything cannot be confirmed stopped (its recorders stop at
    their next killswitch check)."""
    from probe.service import client
    from probe.service.protocol import Method

    try:
        status = client.call(Method.STATUS, client_version=_version(), timeout=FINISH_TIMEOUT_S)
    except Exception as exc:  # noqa: BLE001
        return Finished(error=f"an older Probe service did not say what it records ({type(exc).__name__})")
    recorders = status.get("recorders") if isinstance(status, dict) else None
    live = [r for r in recorders or [] if isinstance(r, dict) and r.get("alive")]
    if not live:
        return Finished()
    return Finished(
        error=f"an older Probe service records {len(live)} session(s) and cannot be asked to stop them; "
        "they stop at their next killswitch check"
    )


# -- probe exec ----------------------------------------------------------------------


def hold_run(run_id: str) -> dict | None:
    """Tell the service this process wraps `run_id`. Its `{pid, start_time}`
    owner record when the service holds it (pass it to `release_run`), else
    None: the run's lock file is all an updater sees, as before."""
    if not _reachable() or not isinstance(run_id, str) or not run_id:
        return None
    try:
        from probe.service import client

        owner = client.owner_of(os.getpid())
        if owner is None:
            return None
        answer = client.hold_run(run_id, owner, client_version=_version(), timeout=HOLD_TIMEOUT_S)
    except Exception:  # noqa: BLE001 -- never in the way of the run
        return None
    return owner if answer.get("held") is True else None


def release_run(run_id: str, owner: dict | None) -> None:
    """The run is over: the service drops its hold now (it would at this
    process's exit anyway). Never raises."""
    if not _reachable() or not run_id:
        return
    try:
        from probe.service import client

        client.release_run(run_id, owner, client_version=_version(), timeout=HOLD_TIMEOUT_S)
    except Exception:  # noqa: BLE001 -- the hold goes with this process
        pass


# -- the manifest ----------------------------------------------------------------------

#: The cache override the service cannot be told (not a context variable):
#: with it set, the detached refresher keeps writing where it points.
_CACHE_OVERRIDE_ENV = "PROBE_VERSION_CACHE"


#: Context variables that change nothing about a refresh: left out, so one
#: refresh serves every session of the machine (the service keys on context).
_NOT_FOR_THE_MANIFEST = frozenset({"PROBE_SESSION_STATE", "PROBE_SESSION_TRACKING"})


def manifest_context() -> dict:
    """Where the cache, the config and the network are for THIS process, as
    the service's context (`protocol.CONTEXT_ENV`): its child then writes the
    same cache, for the same endpoint, through the same proxy."""
    from probe.service.protocol import CONTEXT_ENV

    return {
        name: os.environ[name]
        for name in sorted(CONTEXT_ENV - _NOT_FOR_THE_MANIFEST)
        if os.environ.get(name)
    }


def refresh_manifest() -> bool:
    """Ask the service to refresh the cached release manifest, without waiting
    for it. True when it is refreshing it now (started, or already running):
    the caller spawns nothing. False: spawn the detached refresher as before --
    also on `recent`: this process asks only with a stale cache, and a refresh
    of it that finished within the service's cooldown (shorter than the cache's
    TTL and back-off) would have left it fresh, so that one did not land (its
    child failed, or an older core refused the request)."""
    if not _reachable() or os.environ.get(_CACHE_OVERRIDE_ENV):
        return False
    try:
        from probe.service import client
        from probe.service.protocol import CheckOutcome

        answer = client.refresh_manifest(manifest_context(), client_version=_version(), timeout=MANIFEST_TIMEOUT_S)
    except Exception:  # noqa: BLE001 -- no service, an older one, a refused context
        return False
    return answer.get("outcome") in (CheckOutcome.STARTED, CheckOutcome.RUNNING)
