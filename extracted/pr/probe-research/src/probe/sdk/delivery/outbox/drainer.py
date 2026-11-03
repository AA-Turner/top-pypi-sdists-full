"""Who drains a client's queue: the `Drainer` interface and `pick_drainer`, which picks the kind
ONCE per client (detached worker, in-process thread, or nobody); DrainerMixin is Client's side."""

from __future__ import annotations
import os
import time
import warnings

from probe.foundation.compat.compat import StrEnum

#: The in-process exporter's interval, read once when a client picks its drainer (parity F2).
EXPORT_INTERVAL_ENV = "PROBE_EXPORT_INTERVAL_SEC"


class DrainerKind(StrEnum):
    """What delivers a client's queued writes."""

    #: The detached outbox worker (or the Probe service, which starts one for us).
    WORKER = "worker"
    #: The in-process exporter thread, sending through this client's own transport.
    THREAD = "thread"
    #: Nobody on its own: `flush()`/`finish()`, or a forced kick, delivers.
    NONE = "none"


class Drainer:
    """The interface every kind implements, and the NONE kind itself: it delivers nothing on
    its own. ``kick(force=True)`` hands the queue to a detached worker from any kind (a
    deferred finish, a hand-off), never past a custom transport the worker cannot replay."""

    kind = DrainerKind.NONE

    def __init__(self, directory, *, can_fork: bool, credential_env: dict | None = None) -> None:
        self.directory = str(directory)
        self.can_fork = can_fork
        #: A credential held only in code, handed to the worker it starts (R5).
        self.credential_env = credential_env

    def wake(self) -> None:
        """After an enqueue: make sure someone delivers it soon. Runs per `log()`."""

    def kick(self, *, force: bool = False) -> None:
        """Hand the queue to a detached worker. Forced kicks skip every throttle."""
        if not (force and self.can_fork):
            return
        from .. import outbox as outbox_worker

        try:
            outbox_worker.maybe_spawn(self.directory, **_with_credential(self.credential_env))
        except Exception:  # noqa: BLE001 -- best-effort; finish() waits for the worker
            pass

    def close(self, timeout: float | None = None) -> bool:
        """Stop delivering through this process; True when something was stopped."""
        return False


def _with_credential(credential_env: dict | None) -> dict:
    """`maybe_spawn`'s keyword, only when there is a code credential to hand over."""
    return {"credential_env": credential_env} if credential_env else {}


def export_interval_from_env() -> float | None:
    """`PROBE_EXPORT_INTERVAL_SEC` in seconds, or None (unset or malformed, warned)."""
    raw = os.environ.get(EXPORT_INTERVAL_ENV)
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        warnings.warn(
            f"ignoring malformed {EXPORT_INTERVAL_ENV}={raw!r}; expected seconds as a float",
            stacklevel=3,
        )
        return None


def pick_drainer(client) -> Drainer:
    """The client's drainer, picked once at construction (D1): the detached worker for every
    client on the default transport, a token passed in code riding its spawn (R5); the
    in-process thread only for an injected transport with a ``drain_interval`` (the worker
    cannot replay one); else none (`flush()` delivers)."""
    credential_env = getattr(client, "_worker_credentials", None)
    if client._drain_interval is not None:
        from .drainers.in_process import ThreadDrainer

        return ThreadDrainer(client)
    if client._auto_drain:
        from .drainers.detached import DetachedDrainer

        return DetachedDrainer(client.journal.dir, credential_env=credential_env)
    return Drainer(client.journal.dir, can_fork=client._default_transport, credential_env=credential_env)


def _at_exit(callback) -> None:
    """`atexit.register`, by a name tests can point elsewhere: a callback that
    outlives pytest runs after every monkeypatch is undone."""
    import atexit

    atexit.register(callback)


class DrainerMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def _promote_waiting_at_exit(self, run_ref: str) -> None:
        """Make sure an upload this process queued for a background credential
        scan is promoted even if no worker could be started (a frozen or
        embedded interpreter): at exit, promote what is still waiting for THIS
        process's runs -- not other processes' in a shared journal -- within
        `_EXIT_PROMOTE_SECONDS`, then kick delivery the way `_kick_drainer`
        would. Registered once. Normally a no-op: the worker or `finish()` got
        there first."""
        runs = self.__dict__.setdefault("_waiting_exit_runs", set())
        runs.add(run_ref)
        if len(runs) > 1 or getattr(self, "_waiting_exit_armed", False):
            return
        self._waiting_exit_armed = True
        journal_dir = str(self.journal.dir)
        spawn = self._default_transport and self._auto_drain
        credentials = getattr(self, "_worker_credentials", None)
        budget = self._EXIT_PROMOTE_SECONDS

        def promote() -> None:
            from .. import outbox as outbox_worker
            from ..journal.journal import Journal

            try:
                journal = Journal(journal_dir)
                deadline = time.monotonic() + budget
                promoted = 0
                for ref in sorted(runs):
                    left = deadline - time.monotonic()
                    if left <= 0:
                        break
                    promoted += journal.promote_waiting(run_ref=ref, timeout=left)
                if spawn and (promoted or journal.waiting()):
                    outbox_worker.maybe_spawn(journal_dir, **_with_credential(credentials))
            except Exception:  # noqa: BLE001 -- exit must not raise; items stay queued
                pass

        _at_exit(promote)

    def _kick_drainer(self, *, force: bool = False) -> None:
        """Wake the detached outbox worker (parity F1); `Drainer.kick` says how.

        ``force`` (deferred finish, F3): skip the mode gate and the throttle -- a
        queued terminal status must not have its one kick swallowed -- but never
        the transport gate; a worker cannot replay an injected one."""
        self._drainer.kick(force=force)
