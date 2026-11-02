"""who may call which method (Policy per method, confined callers, request screening) and the service's own log."""

from __future__ import annotations
import os
import sys
import time

from ..actions import caller
from ..jobs.background.background import is_other_network
from ...foundation.service_api.vocabularies import (
    BackgroundRefusal,
    RefusedReason)
from ...foundation.service_api.wire import Method


#: Methods this service answers that are not in `protocol.METHODS` (that file is
#: byte-copied into the tap): only this release's own CLI calls them.
DAEMON_HOST_METHOD = "daemon.host"
LOCAL_METHODS = frozenset({DAEMON_HOST_METHOD})


class Policy:
    """What a method does for its caller (`METHOD_POLICY`), which decides who may call it."""

    #: Answers from what the service knows: anyone (of this user) may ask.
    READ = "read"
    #: Ends or stops what is the caller's own (or the service): benign, anyone.
    CONTROL = "control"
    #: Runs or stores work outside the caller -- a child, a recorder, a hold
    #: that keeps updates off, an upload: never for a caller this service
    #: cannot rule out being confined (`caller.sandboxed`, `is_other_network`).
    #: Refused before its handler is reached, whatever the handler checks.
    WORK = "work"


#: Every method, classified (tests/test_service_background.py fails on one
#: missing). A method added to `protocol.METHODS` without a class is WORK.
METHOD_POLICY = {
    Method.HELLO: Policy.READ,
    Method.STATUS: Policy.READ,
    Method.SESSION_LIST: Policy.READ,
    Method.EVENTS_SUBSCRIBE: Policy.READ,
    Method.ACTION_STATUS: Policy.READ,
    Method.ACTION_EVENTS: Policy.READ,
    Method.UPDATE_STATUS: Policy.READ,
    Method.SESSION_RECORDING: Policy.READ,
    # Only the session's registrant (or this service) may end it (#3360,
    # `registry.Registry.holds`), checked in the registry.
    Method.SESSION_END: Policy.CONTROL,
    Method.ACTION_CANCEL: Policy.CONTROL,
    Method.STOP: Policy.CONTROL,
    # Not a read: a `refresh` starts a `probe status` child that sends the
    # stored token and each agent's capture token through the proxy and CA
    # the request's `context` names.
    Method.STATUS_GET: Policy.WORK,
    # Stops ANY session's recorder by its id (`session.list` names them all):
    # the same as `recorders.finish`, one session at a time.
    Method.SESSION_FINISH: Policy.WORK,
    Method.ACTION_RUN: Policy.WORK,
    Method.UPDATE_CHECK_NOW: Policy.WORK,
    # It only records what the desktop app reports, but that record decides
    # when the app next checks for its update: a caller in a sandbox must not
    # be able to write it (a forged `current` would hold the check off 6 h).
    Method.UPDATE_APP_RESULT: Policy.WORK,
    Method.SESSION_REGISTER: Policy.WORK,
    Method.SESSION_RECORD: Policy.WORK,
    Method.HOOKS_HOST: Policy.WORK,
    Method.HOOKS_RUN: Policy.WORK,
    Method.HOOKS_QUEUE: Policy.WORK,
    Method.RECORDERS_FINISH: Policy.WORK,
    DAEMON_HOST_METHOD: Policy.WORK,
    Method.RUN_HOLD: Policy.WORK,
    Method.RUN_RELEASE: Policy.WORK,
    Method.MANIFEST_REFRESH: Policy.WORK,
    Method.OUTBOX_DRAIN: Policy.WORK,
    Method.BOX_WATCH: Policy.WORK,
    Method.TELEMETRY_SEND: Policy.WORK,
    # The mailbox writes and claims files for its session (Q2); a desktop
    # request runs a child that reads this user's credentials (Q6). Each of
    # their handlers already refused a sandboxed caller, in this same shape.
    Method.MAILBOX_POST: Policy.WORK,
    Method.MAILBOX_CLAIM: Policy.WORK,
    Method.MAILBOX_ANSWER: Policy.WORK,
    Method.DESKTOP_REQUEST: Policy.WORK,
    # Each starts or schedules a child on the caller's say (a status-line
    # fetch, the team note's sync, an import's worker); their handlers
    # already refused a sandboxed caller (Q4), as `_refuse_sandboxed`.
    Method.STATUSLINE_REFRESH: Policy.WORK,
    Method.NOTES_SYNC: Policy.WORK,
    Method.IMPORT_START: Policy.WORK,
}

#: A WORK method's answer to a caller it refuses for its confinement, in the
#: shape that method's clients already read as "not here, do it yourself";
#: every other WORK method answers error REFUSED with `reason: sandboxed`.
CONFINED_ANSWERS = {
    # `reason` is new beside `refused` (older clients read `refused` alone):
    # pi runs the lane itself on exactly this one.
    Method.HOOKS_HOST: {"refused": "a caller in a sandbox", "reason": RefusedReason.SANDBOXED},
    Method.HOOKS_RUN: {"refused": "a caller in a sandbox", "reason": RefusedReason.SANDBOXED},
    Method.HOOKS_QUEUE: {"refused": "a caller in a sandbox", "reason": RefusedReason.SANDBOXED},
    Method.SESSION_RECORD: {"recording": False, "reason": RefusedReason.SANDBOXED},
    # What a tap reads as "nothing hosted here" (`tap/record_client.py`).
    Method.SESSION_FINISH: {"recording": False, "finished": False},
    # What every tap reads as "do not register this session again"
    # (`service_link`'s `alive: false`), not a refusal to retry every 2 s.
    Method.SESSION_REGISTER: {"alive": False, "reason": RefusedReason.SANDBOXED},
    Method.OUTBOX_DRAIN: {"accepted": False, "reason": BackgroundRefusal.SANDBOXED},
    Method.BOX_WATCH: {"accepted": False, "reason": BackgroundRefusal.SANDBOXED},
    Method.TELEMETRY_SEND: {"accepted": False, "reason": BackgroundRefusal.SANDBOXED},
}


def confined(pid: int | None) -> bool:
    """A caller this service cannot rule out being more confined than itself:
    `caller.sandboxed` (Landlock included), or (Linux) another network namespace."""
    return caller.sandboxed(pid) or is_other_network(pid)


def screen(pid: int | None, start: str | None) -> str | None:
    """Why a WORK request from the process `pid` (started at `start`, where
    known) is refused, or None. `RefusedReason.CALLER_GONE` when that
    process has exited (a connection handed to a child: who asks can no
    longer be checked, plan D9), else `SANDBOXED` when `confined`. A check
    that fails refuses."""
    try:
        # pid 1 (a container's entrypoint) never reads as alive to `procid`.
        if pid is not None and pid > 1:
            from ...foundation.service_api import procid

            # As `_refuse_gone_caller` asks (never `os.kill(pid, 0)`: on
            # Windows that would end the caller).
            gone = procid.alive(pid, start) is False if start else not procid.exists(pid)
            if gone:
                return RefusedReason.CALLER_GONE
        return RefusedReason.SANDBOXED if confined(pid) else None
    except Exception:  # noqa: BLE001 -- unknown counts as confined
        return RefusedReason.SANDBOXED


_session_envs: dict | None = None


def session_envs() -> dict:
    """`{harness id: its session-id variable}`, from the harness registry
    (light: stdlib only). Read once; empty if the registry cannot be."""
    global _session_envs
    if _session_envs is None:
        try:
            from probe.foundation.harness_registry import get_registry

            _session_envs = {h.id: h.session_env for h in get_registry().all() if h.session_env}
        except Exception as exc:  # noqa: BLE001 -- a context then just cannot name a session
            log(f"harness registry unreadable: {exc!r}")
            _session_envs = {}
    return _session_envs


def session_env_names() -> frozenset:
    """Every coding agent's session-id variable, which a request's `context`
    may set (`protocol.CONTEXT_ENV`)."""
    return frozenset(session_envs().values())


def _version() -> str:
    try:
        from probe import __version__

        return str(__version__)
    except Exception:  # noqa: BLE001 -- never a reason not to serve
        return "0.0.0.dev0"


def log(message: str) -> None:
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        sys.stderr.write(f"[{stamp}] probe-service[{os.getpid()}]: {message}\n")
        sys.stderr.flush()
    except (OSError, ValueError):
        pass


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError:
        return default
    return value if value >= 0 else default
