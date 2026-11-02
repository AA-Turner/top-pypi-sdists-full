"""who is calling: the caller's registered session by ancestry, refusals for sandboxed, gone or foreign callers."""

from __future__ import annotations

import asyncio
import time

from ...actions import caller
from ...actions.caller import Bound, same_process
from ....foundation.service_api.wire import (
    ErrorCode,
    Method,
    RpcError)
from ....foundation.service_api.vocabularies import (
    RefusedReason,
    Mode)
from ...sessions.sessions import SERVICE, Session
from probe.service.server.connections.connections import Connection
from probe.service.server.policy import log, session_envs
#: A refused session or mailbox call is logged once per (session, process) in
#: this long: two agents on one session id retry every 2 s, and the log is
#: rotated only when the service starts.
REFUSAL_LOG_S = 600.0
#: At most this many refusals are remembered for that.
MAX_REFUSALS_LOGGED = 1024


class CallerChecksMixin:
    """Part of Service: its methods run with `self` the Service; compose() folds them into Service."""

    def _caller_of(self, conn: Connection | None) -> dict | str | None:
        """Who a registry change comes from (#3360): `registry.SERVICE` for this
        service's own (no connection, or one from this very process: a hosted
        recorder's link), else the connecting process as the kernel names it,
        `{pid, start_time}`; None when it names none. The start time is read
        once a connection where /proc did not give it at connect (`ps`)."""
        if conn is None or conn.peer_pid == self.pid:
            return SERVICE
        if conn.peer_pid is None:
            return None
        if conn.peer_identity is None:
            from ....foundation.service_api import procid

            start = conn.peer_start or procid.start_time(conn.peer_pid)
            conn.peer_identity = {"pid": conn.peer_pid, "start_time": start or ""}
        return dict(conn.peer_identity)

    def _log_unbound(self, exc: RpcError, method: str, sid: str, who: dict | str | None,
                     now: float | None = None) -> None:
        """Log a `not_registrant` refusal, once per (session, process) every
        REFUSAL_LOG_S: a newer `tap watch` of a session another agent still
        runs is refused at every retry (every 2 s) until that agent exits."""
        if isinstance(exc.data, dict) and exc.data.get("reason") == Bound.NOT_REGISTRANT:
            pid = who.get("pid") if isinstance(who, dict) else who
            if self._first_refusal((sid, pid), now):
                log(f"refused {method} of {sid} from pid {pid}: not the process that registered it"
                    f" (said once per {REFUSAL_LOG_S / 60:g} min)")

    def _first_refusal(self, key: tuple, now: float | None = None) -> bool:
        """Is `key`'s refusal the first in REFUSAL_LOG_S (then it is remembered)?"""
        now = time.monotonic() if now is None else now
        last = self._refusals_logged.get(key)
        if last is not None and now - last < REFUSAL_LOG_S:
            return False
        if len(self._refusals_logged) >= MAX_REFUSALS_LOGGED:
            self._refusals_logged = {k: t for k, t in self._refusals_logged.items() if now - t < REFUSAL_LOG_S}
            if len(self._refusals_logged) >= MAX_REFUSALS_LOGGED:
                self._refusals_logged.clear()
        self._refusals_logged[key] = now
        return True

    def _caller_session(self, conn: Connection, env: dict, seen: tuple | None = None) -> tuple:
        """`(session, daemon sid)`: the registered session the caller runs
        inside (plan D9), or None, and the id of a session the Probe daemon
        records that it runs inside, or None. Its process ancestry passes a
        session's owner (pid and start time), or (Linux) its environment names
        a registered session. EVERY match counts (#3360): a daemon-mode
        session, or an agent process once registered in daemon mode that still
        runs (`Registry.daemon_owner`, which neither a `session.end` nor a
        later register undoes), makes it a daemon caller, so a registration
        forged beside the real one cannot hide it. A session found this way
        that the context did not name joins `env` under its harness's
        variable, so `probe.core.run` refuses what it refuses there.
        `seen`: `(ancestry, environ)` read already, off the loop (`_caller_seen`)."""
        names = session_envs()
        found: Session | None = None
        daemon: str | None = None
        if conn.peer_pid is not None:
            # No owner to meet: no walk (`ps` per process on macOS, on this loop).
            walk = seen is not None or self.registry.daemon_owners or self.registry.owners()
            chain = (seen[0] if seen is not None else caller.ancestry(conn.peer_pid)) if walk else []
            for pid, start in chain:
                for session in self.registry.owned(pid, start):
                    if found is None or (session.mode == Mode.DAEMON and found.mode != Mode.DAEMON):
                        found = session
                    if session.mode == Mode.DAEMON and daemon is None:
                        daemon = session.sid
                remembered = self.registry.daemon_owner(pid, start)
                if remembered is not None and daemon is None:
                    daemon = remembered["sid"]
            carried = seen[1] if seen is not None else caller.environ(conn.peer_pid, frozenset(names.values()))
            now = time.time()
            for value in carried.values():
                candidate = self.registry.sessions.get(value)
                if candidate is not None and candidate.alive(now, self.registry.ttl):
                    if found is None:
                        found = candidate
                    if candidate.mode == Mode.DAEMON and daemon is None:
                        daemon = candidate.sid
                if daemon is None and self.registry.daemon_agent_runs(value):
                    daemon = value
        if found is not None:
            name = names.get(found.harness)
            if name and not any(env.get(n) for n in names.values()):
                env[name] = found.sid
        return found, daemon

    def _caller_seen(self, conn: Connection) -> tuple:
        """`(ancestry, environ)` of the caller, for `_caller_session`: `ps` on
        macOS, so a caller of it runs this on a thread."""
        if conn.peer_pid is None:
            return [], {}
        names = frozenset(session_envs().values())
        return caller.ancestry(conn.peer_pid), caller.environ(conn.peer_pid, names)

    def _refuse_gone_caller(self, conn: Connection) -> None:
        """The process that connected is gone (a connection handed to a child,
        which kept the session's environment): who calls can no longer be
        checked, so nothing changes on its say (plan D9)."""
        if conn.peer_pid is None:
            return
        from ....foundation.service_api import procid

        if conn.peer_start:
            gone = procid.alive(conn.peer_pid, conn.peer_start) is False
        else:
            gone = not procid.exists(conn.peer_pid)
        if gone:
            raise RpcError(
                ErrorCode.REFUSED,
                "refused: the process that opened this connection has exited; connect again",
                {"reason": RefusedReason.CALLER_GONE},
            )

    async def _refuse_foreign_mail(self, conn: Connection, sid: str, *, claim: bool) -> None:
        """Refuse a post to, or a claim from, `sid`'s mailbox by a process that
        is not the session's own (#3361). Any process of this user reaches the
        socket, and a message posted is one the session's agent is shown as
        Probe's, one claimed is one it never sees. The kernel names the caller;
        its process ancestry (pid AND start time, as for owners) decides:

            post    the session's daemon worker: a child of this service
                    (`workers.WorkerHost.pids`), or one under the process that
                    registered the session (`Session.registrant`: a `tap
                    watch` supervising its own worker, an older tap)
            claim   Probe's hooks: run under the session's agent process (its
                    registered owner), or forked from a warm hook host this
                    service runs (`hookhosts.HookHosts.pids`)
            both    this service itself

        The walk stops at this service: what runs above it says nothing. Every
        caller refused here (an older worker that outlived its service, a hook
        of a session registered without an owner) does the step on the files
        itself, as it does on any refusal: delivery never depends on this."""
        peer = conn.peer_pid
        if peer == self.pid:
            return
        session = self.registry.sessions.get(sid)
        owner = session.owner if claim and session is not None else None
        registrant = None
        if not claim and session is not None and isinstance(session.registrant, dict):
            registrant = session.registrant
        children = self.hookhosts.pids() if claim else self.workers.pids(sid)
        me = self.pid

        def belongs() -> bool:
            if peer is None:
                return False
            below = None
            for pid, start in caller.lineage(peer):
                if pid == me:
                    return below in children
                if owner is not None and pid == owner["pid"] and start == owner["start_time"]:
                    return True
                if registrant is not None and same_process(registrant, {"pid": pid, "start_time": start}):
                    return True
                below = pid
            return False

        if await asyncio.to_thread(belongs):
            return
        what = "take messages from" if claim else "post to"
        method = Method.MAILBOX_CLAIM if claim else Method.MAILBOX_POST
        # Once per (method, session) a while: each hook is a new process.
        if self._first_refusal((method, sid)):
            log(f"refused {method} for {sid} from pid {peer}: not the session's own"
                f" (said once per {REFUSAL_LOG_S / 60:g} min)")
        raise RpcError(
            ErrorCode.REFUSED,
            f"refused: only the session's own {'hooks' if claim else 'daemon worker'} may {what} its mailbox",
            {"reason": Bound.NOT_SESSION},
        )

    async def _refuse_sandboxed(self, conn: Connection) -> None:
        """Refuse a caller in a sandbox (as `hooks.host` and `session.record`
        do): a child this runs would fetch and write outside it, with the
        context it chose, and a recorder it stops is outside it too. The CLI
        then does it itself, inside. Unknown counts as sandboxed."""
        if await asyncio.to_thread(caller.sandboxed, conn.peer_pid):
            raise RpcError(
                ErrorCode.REFUSED, "refused: a caller in a sandbox", {"reason": RefusedReason.SANDBOXED}
            )
