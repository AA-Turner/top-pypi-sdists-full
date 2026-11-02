"""service.hello/status/stop and session.register/record/recording/end/list, events.subscribe."""

from __future__ import annotations

import asyncio
import time

from ...actions import caller
from ...mail.watch import MAX_TARGETS
from ...sessions.receipts import by_harness, journal_roots
from ....foundation.service_api.wire import (
    API_VERSION,
    ErrorCode,
    Method,
    RpcError,
    invalid_params)
from ....foundation.service_api.vocabularies import (
    CAPS,
    CLIENTS,
    MODES,
    MAX_SUBSCRIBE_SESSIONS,
    SESSION_TOPICS,
    TOPICS,
    EndReason,
    RefusedReason,
    StopReason,
    Topic,
    Mode)
from ....foundation.service_api.env import (
    REPORT_ENV,
    BASE_URL_ENV)
from ....foundation.service_api.params import (
    need_bool,
    need_choice,
    need_context,
    need_int,
    need_owner,
    need_sessions,
    need_state_dir,
    need_str)
from ...sessions.sessions import Outcome
from probe.service.server.connections.connections import Connection
from probe.service.server.policy import log, session_env_names
from probe.service.server.tracking import RECEIPTS_WAIT_S


class SessionHandlersMixin:
    """Part of Service: its methods run with `self` the Service; compose() folds them into Service."""

    # -- methods -------------------------------------------------------------

    def _hello(self, conn: Connection, params: dict) -> dict:
        client = need_choice(params, "client", CLIENTS)
        need_str(params, "client_version", max_len=64)
        api = params.get("api")
        if not isinstance(api, int) or isinstance(api, bool):
            raise invalid_params("api must be an integer")
        if api != API_VERSION:
            raise RpcError(
                ErrorCode.UNSUPPORTED_API,
                f"unsupported_api: this service speaks api {API_VERSION}",
                {"supported": [API_VERSION]},
            )
        keepalive = need_bool(params, "keepalive")
        conn.hello = True
        conn.client = client
        conn.keepalive = keepalive
        self.reevaluate()
        return {
            "service_version": self.version,
            "api": API_VERSION,
            "pid": self.pid,
            "started_at": self.started_at,
            "state": self.state,
            "caps": sorted(CAPS),
            # The env it runs from: a rebuild of the same version lives in a
            # folder of its own (`<v>+g<N>`), which the guard tells apart by it.
            "env": self.env,
        }

    def _status(self, conn: Connection, params: dict) -> dict:
        until = None
        if self.discovering:
            until = self.started_at + self.discovery_s
        return {
            "service_version": self.version,
            "pid": self.pid,
            "started_at": self.started_at,
            "state": self.state,
            "sessions": self.registry.alive_count(),
            "app_clients": len(self._app_connections()),
            "update": self.updater.public(),
            "actions": {
                "running": self.actions.busy_holder(),
                # Waiting for an update to let go of the slot, oldest first.
                "queued": self.actions.queued_ids(),
            },
            "discovering_until": until,
            "hook_hosts": self.hookhosts.public(),
            "hook_queue": self.hook_queue.public(),
            "recorders": self.recorders.public(),
            "workers": self.workers.public(),
            "daemon_host": self.workers.daemon_host.public() if self.workers.daemon_host is not None else None,
            "runs": self.runs.public(),
            # The sessions whose mailbox and held questions a subscriber waits on (Q2).
            "watched": len(self._watch_targets()),
            "background": self.background.public(),

            "imports": self.imports.public(),
            "statusline": self.statusline.public(),
            "notes": self.notes.public(),
            # What fails here and what was reported (crash-report plan B2).
            "watch": self.watch.public(),
            # Probe's hooks in Codex, kept approved (#3617).
            "codex_trust": self.codex_trust.public(),
        }

    def _stop(self, conn: Connection, params: dict) -> dict:
        if self.updater.in_progress():
            raise RpcError(ErrorCode.REFUSED, "refused: an update is running", {"reason": RefusedReason.UPDATING})
        if self.actions.pending():
            raise RpcError(
                ErrorCode.REFUSED, "refused: an action is running or waiting", {"reason": RefusedReason.ACTION_RUNNING}
            )
        conn.after_reply = lambda: self.stop(StopReason.STOP)
        return {"stopping": True}

    def _register(self, conn: Connection, params: dict) -> dict:
        sid = need_str(params, "sid", max_len=128)
        harness = need_str(params, "harness", max_len=64)
        mode = need_choice(params, "mode", MODES)
        owner = need_owner(params)
        generation = need_int(params, "generation")
        state_dir = need_state_dir(params)
        # Whether the registrant's environment allows automatic reports (plan
        # B2): a bool, else unsaid (an older registrant: None, read as no).
        report_env = params.get(REPORT_ENV)
        report_env = report_env if isinstance(report_env, bool) else None
        who = self._caller_of(conn)
        try:
            reg = self.registry.register(sid, harness, mode, owner, generation, state_dir, report_env, caller=who)
        except RpcError as exc:
            self._log_unbound(exc, Method.SESSION_REGISTER, sid, who)
            raise
        # Whether the service may poll for it with the user's key (`alertpoll`):
        # never for a registrant in a sandbox, which names the state folder the
        # answers go to. `session.record` refused those already; None: this service.
        reg.session.unconfined = conn is None or not caller.sandboxed(conn.peer_pid)
        if reg.outcome != Outcome.DEAD:
            # Every register, a heartbeat's too: after a restart the sessions
            # come back from `sessions.json` unconfirmed, and only their next
            # register says they may be polled for (both start only once).
            self.alerts.changed()
            self.mailwatch.changed()
            # A session's mode may have moved (off -> on): the hint lane looks again.
            self.hints.changed()
        now = time.time()
        if reg.outcome in (Outcome.NEW, Outcome.REPLACED):
            if reg.previous is not None and self.watcher is not None:
                self.watcher.cancel((reg.previous.sid, reg.previous.generation))
            self._watch(reg.session)
            log(
                f"session {sid} registered ({reg.outcome}, {harness}, {mode}, generation {generation}, "
                f"owner {owner['pid'] if owner else 'heartbeat'})"
            )
            self._emit(
                Topic.SESSION_STARTED,
                {
                    "sid": sid,
                    "harness": harness,
                    "mode": mode,
                    "generation": generation,
                    "alive": reg.session.alive(now, self.registry.ttl),
                },
            )
            self.status_cache.invalidate()
        self._schedule_expiry()
        self.reevaluate()
        return {"alive": reg.session.alive(now, self.registry.ttl) if reg.outcome != Outcome.DEAD else False}

    def _record(self, conn: Connection, params: dict) -> dict:
        """`session.record` (plan A2): `session.register`, then this session's
        recorder on a thread here. `{recording: false, ...}` (the tap then
        starts its own `tap watch`) when it cannot be: a caller in a sandbox, no owner, no loadable tap, or a newer tap than the one loaded
        (`restart: true`: the service restarts onto it, the caller asks the
        next one)."""
        if caller.sandboxed(conn.peer_pid):
            # Its recorder would run here, outside that sandbox, with the
            # environment (PATH included) the caller sent.
            return {"recording": False, "reason": "sandboxed"}
        refused = self.recorders.check(params)
        if refused is not None:
            if refused.get("restart"):
                self._restart_for_update(StopReason.TAP_UPDATE)
            return refused
        # Probe off: taken (no `tap watch` records it instead), held, and
        # registered `off`, which is never alive and never an owner gone: before
        # this a `tap watch` of an off session asked every minute and was told
        # `owner_gone` each time, while it recorded on (live test, bug F).
        off = self._session_off(params)
        if not self.recorders.live(params.get("sid")):
            # Recorded here already: its link keeps the registration (a second
            # generation from here would make the link step back for good).
            registered = self._register(conn, {**params, "mode": Mode.OFF} if off else params)
            if registered.get("alive") is False and not off:
                return {"recording": False, "reason": "owner_gone"}
        answer = self.recorders.record(params)
        self.hints.changed()
        return answer

    def _recording(self, conn: Connection, params: dict) -> dict:
        """`session.recording`: is the session recorded here now? Its switch is
        looked at first, so a CLI that just moved it (`probe session state`)
        has its gap opened or closed at this moment (`capture_gate`). `off`:
        Probe is off for it, so nothing of it is captured."""
        sid = params.get("sid")
        self.recorders.look(sid)
        answer = {"recording": self.recorders.recording(sid)}
        if self.recorders.held_off(sid):
            answer["off"] = True
        return answer

    def _end(self, conn: Connection, params: dict) -> dict:
        sid = need_str(params, "sid", max_len=128)
        generation = need_int(params, "generation")
        who = self._caller_of(conn)
        try:
            removed = self.registry.end(sid, generation, who)
        except RpcError as exc:
            self._log_unbound(exc, Method.SESSION_END, sid, who)
            raise
        if removed is not None:
            if self.watcher is not None:
                self.watcher.cancel((removed.sid, removed.generation))
            log(f"session {sid} ended")
            self._emit(Topic.SESSION_ENDED, {"sid": sid, "generation": removed.generation, "reason": EndReason.END})
            self.recorders.wake(sid)
            self._session_gone()
            self._schedule_expiry()
            self.reevaluate()
        return {}

    async def _list(self, conn: Connection, params: dict) -> dict:
        """`session.list`: every registered session, each with its delivery
        `receipts` (plan D29; `receipts.py`), and `harnesses`, the same per
        agent. `receipts: false` leaves both out (a caller that only counts)."""
        sessions = self.registry.listing()
        if not need_bool(params, "receipts", default=True):
            return {"sessions": sessions}
        envs = [rec.params.get("env") for rec in list(self.recorders.recordings.values())]
        found = await self.receipts.get(
            [s["sid"] for s in sessions], journal_roots(envs), wait=RECEIPTS_WAIT_S, claims=self.recorders.claims()
        )
        for session in sessions:
            session["receipts"] = found.get(session["sid"])
        return {"sessions": sessions, "harnesses": by_harness(sessions)}

    async def _subscribe(self, conn: Connection, params: dict) -> dict:
        """`events.subscribe`. For a SESSION_TOPICS topic, `sessions` (and the
        `state_dir` they keep their files under) say whose mailbox to watch;
        the answer comes once their files are baselined (`MailWatch.baseline`),
        so a change after it is an event, and a refused one watches nothing
        new. Watching only reads, so a caller in a sandbox may watch too, but
        only live registered sessions, where they registered their files. At
        most MAX_SUBSCRIBE_SESSIONS a connection, MAX_TARGETS a machine."""
        topics = params.get("topics")
        if not isinstance(topics, list) or not topics or not all(isinstance(t, str) for t in topics):
            raise invalid_params("topics must be a non-empty list of topic names")
        unknown = sorted(set(topics) - TOPICS)
        if unknown:
            raise invalid_params(f"unknown topics {unknown}")
        sessions = need_sessions(params)
        state_dir = need_state_dir(params)
        if not set(topics) & SESSION_TOPICS and not sessions:
            conn.topics |= set(topics)  # nothing new to watch: no baseline either
            return {}
        added = dict.fromkeys(sessions or (), state_dir)
        if await asyncio.to_thread(caller.sandboxed, conn.peer_pid):
            # Watching only reads, but a caller in a sandbox names only live
            # registered sessions, watched where they keep their files: never
            # a folder of its choosing (a hung mount, a planted FIFO), never
            # every session's held questions.
            if not sessions:
                raise invalid_params("a caller in a sandbox must name its sessions")
            now = time.time()
            for sid in sessions:
                registered = self.registry.sessions.get(sid)
                if registered is None or not registered.alive(now, self.registry.ttl):
                    raise invalid_params(f"session {sid!r} is not registered")
                added[sid] = registered.state_dir
        if len({**conn.sessions, **added}) > MAX_SUBSCRIBE_SESSIONS:
            raise invalid_params(f"a connection watches at most {MAX_SUBSCRIBE_SESSIONS} sessions")
        if len(self._watch_targets(added)) > MAX_TARGETS:
            raise RpcError(ErrorCode.BUSY, f"busy: more than {MAX_TARGETS} sessions are watched")
        before = (set(conn.topics), dict(conn.sessions))
        conn.topics |= set(topics)
        conn.sessions.update(added)
        if not await self.mailwatch.baseline():
            conn.topics, conn.sessions = before  # refused: it watches nothing new
            raise RpcError(ErrorCode.BUSY, "busy: the watched sessions' files could not be read in time")
        return {}

    async def _status_get(self, conn: Connection, params: dict) -> dict:
        refresh = need_bool(params, "refresh")
        max_age = params.get("max_age")
        if max_age is not None and (
            not isinstance(max_age, (int, float)) or isinstance(max_age, bool) or not 0 <= max_age <= 3600
        ):
            raise invalid_params("max_age must be a number of seconds from 0 to 3600")
        return await self.status_cache.get(self._context(params), refresh=refresh, max_age=max_age)

    def _context(self, params: dict) -> dict:
        """The request's context as the child's environment, its endpoint
        checked (plan D10): the CLI config's stored token follows
        `PROBE_BASE_URL`, so a child runs only with an https endpoint that
        config already names. Anything else is refused, and the app runs the
        CLI itself, with its own environment, as it does on any refusal."""
        env = need_context(params, session_env_names())
        url = env.get(BASE_URL_ENV)
        if url is not None and not caller.known_endpoint(url, env):
            raise invalid_params(
                "base_url must be an https endpoint this machine's Probe CLI is already signed in to"
            )
        return env
