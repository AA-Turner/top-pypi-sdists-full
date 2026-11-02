"""registered sessions: watch each owner's pid, expire the gone, and the session views the watch and hint lane read."""

from __future__ import annotations
import contextlib
import time
from ..hints.state import followed as hint_sessions
from ..mail.watch import Target, default_state
from ..sessions.receipts import journal_roots
from ...foundation.service_api.vocabularies import (
    MailboxPart,
    SESSION_TOPICS,
    EndReason,
    Topic,
    Mode)
from ..sessions.sessions import Session
from ..watch.consent import Live
from probe.service.server.policy import log
#: How long `session.list` waits for its sessions' receipts (`receipts.py`)
#: before it answers with the last ones read: the listing is on every
#: `probe status`'s one-second path.
RECEIPTS_WAIT_S = 0.25


class SessionsMixin:
    """Part of Service: its methods run with `self` the Service; compose() folds them into Service."""

    # -- the watch's view (crash-report plan B2) ---------------------------------

    def _updating(self) -> bool:
        """An update cycle runs (it drains the daemon workers, raises its
        barrier): what fails meanwhile is its hand-over, which the watch neither
        counts nor reports. Two attributes: cheap from any thread, never a file
        (the barrier itself is read by the watch's scan, `_barrier_up`)."""
        updater = getattr(self, "updater", None)
        return updater is not None and (updater.in_progress() or updater.applying)

    def _live_sessions(self) -> list:
        """Every live registered session (on the loop)."""
        now = time.time()
        return [s for s in self.registry.sessions.values() if s.alive(now, self.registry.ttl)]

    def _voters(self) -> list:
        """Every registered session whose agent runs, mode off included (it is
        never "live", but its opt-out counts): a report's consent (on the loop)."""
        now = time.time()
        out = []
        for session in self.registry.sessions.values():
            running = session.owner_live if session.owner is not None else now - session.heartbeat_at < self.registry.ttl
            if running:
                hosted = self._hosted_env(session.sid)
                out.append(Live(session.sid, hosted_env=dict(hosted) if hosted is not None else None,
                                report_env=session.report_env))
        return out

    async def _watch_receipts(self) -> dict:
        """The delivery receipts of each live session whose agent runs (the
        watch's `capture_stalled`), from the same cache `session.list` reads,
        asked for the same sessions it asks for (every registered one): the
        cache keeps the answers of the sessions its last read asked about."""
        live = {s.sid for s in self._live_sessions() if s.owner is None or s.owner_live}
        if not live:
            return {}
        envs = [rec.params.get("env") for rec in list(self.recorders.recordings.values())]
        found = await self.receipts.get(
            [s["sid"] for s in self.registry.listing()], journal_roots(envs), wait=RECEIPTS_WAIT_S,
            claims=self.recorders.claims(),
        )
        return {sid: receipts for sid, receipts in found.items() if sid in live}

    def _recorder_beats(self) -> list:
        """Each hosted recorder inside `hosted.record` that beat during this
        run of it (`tap.hosted.Controls.beat`; an older tap never does): the age
        of its last beat, for the watch's `stalled` (on the loop)."""
        now = time.monotonic()
        out = []
        for rec in list(self.recorders.recordings.values()):
            controls = rec.controls
            if rec.thread is None or not rec.thread.is_alive() or controls.stop.is_set() or controls.pause.is_set():
                continue
            beaten = getattr(controls, "beaten", None)
            if not rec.in_record or not isinstance(beaten, float) or beaten < rec.record_since:
                continue
            out.append({"sid": rec.sid, "beat_age_s": now - beaten, "owner": rec.params.get("owner")})
        return out

    def _hosted_env(self, sid: str) -> dict | None:
        """The environment a hosted session's recorder runs with (`session.record`'s)."""
        rec = self.recorders.recordings.get(sid)
        env = rec.params.get("env") if rec is not None else None
        return env if isinstance(env, dict) else None

    # -- sessions ------------------------------------------------------------

    def _watch(self, session: Session) -> None:
        if session.owner is None or self.watcher is None:
            return
        key = (session.sid, session.generation)
        self.watcher.watch(
            key,
            session.owner["pid"],
            session.owner["start_time"],
            lambda: self._owner_exited(session.sid, session.generation),
        )

    def _owner_exited(self, sid: str, generation: int) -> None:
        dropped = self.registry.drop(sid, generation)
        if dropped is not None:
            self.registry.forget_daemon_owner(dropped.owner)
            log(f"session {sid} (generation {generation}): owner {dropped.owner['pid']} exited")
            self._emit(Topic.SESSION_ENDED, {"sid": sid, "generation": generation, "reason": EndReason.OWNER_EXIT})
            self.recorders.wake(sid)
            self._session_gone()
        self.reevaluate()

    def _session_gone(self) -> None:
        self.status_cache.invalidate()
        self.updater.session_ended()
        self.mailwatch.changed()

    def _watch_targets(self, extra: dict | None = None) -> set:
        """Every session a SESSION_TOPICS subscriber waits on: the ones it
        named, and every live registered one for a subscriber that named none.
        `extra` (sid -> state folder) counts sessions a subscription would add."""
        targets: set = set()
        default = None
        named = [conn.sessions for conn in self.connections if conn.topics & SESSION_TOPICS and conn.sessions]
        everyone = any(conn.topics & SESSION_TOPICS and not conn.sessions for conn in self.connections)
        for sessions in named + ([extra] if extra else []):
            for sid, state in sessions.items():
                if state is None:
                    default = default or default_state()
                targets.add(Target(sid, state or default))
        if everyone:
            now = time.time()
            for session in self.registry.sessions.values():
                if session.alive(now, self.registry.ttl):
                    if session.state_dir is None:
                        default = default or default_state()
                    targets.add(Target(session.sid, session.state_dir or default))
        return targets

    def _daemon_sessions(self) -> list:
        """`(sid, state folder)` of every live daemon-mode session an
        unconfined registrant registered, for the run-alert poller (which asks
        only for those whose worker wants it)."""
        now = time.time()
        return [
            (s.sid, s.state_dir or default_state())
            for s in sorted(self.registry.sessions.values(), key=lambda s: s.registered_at)
            if s.mode == Mode.DAEMON and s.unconfined and s.alive(now, self.registry.ttl)
        ]

    def _hint_sessions(self) -> list:
        """The sessions the hint lane reads (`hints.followed`): asked on its own
        thread, from snapshots of the recordings and the registry."""
        return hint_sessions(
            list(self.recorders.recordings.values()), list(self.registry.sessions.values()),
            now=time.time(), ttl=self.registry.ttl, default_state=default_state(),
        )

    def _hint_posted(self, sid: str) -> None:
        """From the hint lane's thread: a hint posted or withdrawn in `sid`'s
        mailbox. Its watchers hear at once, as for `mailbox.post`."""
        loop = self._loop
        if loop is not None:
            with contextlib.suppress(RuntimeError):
                loop.call_soon_threadsafe(
                    self._emit, Topic.MAILBOX_CHANGED, {"sid": sid, "parts": [MailboxPart.MESSAGES]}
                )

    def _schedule_expiry(self) -> None:
        if self._loop is None:
            return
        if self._expiry_handle is not None:
            self._expiry_handle.cancel()
            self._expiry_handle = None
        due = self.registry.next_expiry()
        if due is not None:
            delay = max(0.0, due - time.time()) + 0.01
            self._expiry_handle = self._loop.call_later(delay, self._expire)

    def _expire(self) -> None:
        self._expiry_handle = None
        for session in self.registry.expired():
            if self.registry.drop(session.sid, session.generation) is not None:
                log(f"session {session.sid}: heartbeat lapsed")
                self._emit(
                    Topic.SESSION_ENDED,
                    {"sid": session.sid, "generation": session.generation, "reason": EndReason.EXPIRED},
                )
                self._session_gone()
        self._schedule_expiry()
        self.reevaluate()
