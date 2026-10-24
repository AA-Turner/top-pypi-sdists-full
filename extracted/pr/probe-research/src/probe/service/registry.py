"""The service's registry of agent sessions: who is alive, and since which generation.

A session is ALIVE when its mode is not `off` and its owner is live:

  owner {pid, start_time}  that exact process still runs (plan X3). The pid
                           alone is never enough: a recycled pid names a process
                           with another start time, and that reads as dead.
  owner null               heartbeat-only (pi, an older hook, a platform that
                           cannot name the agent): alive while its registrant
                           re-registers within the TTL, never "dead on silence"
                           before that.

GENERATIONS order registrations of one session id. A higher generation
replaces the owner (a session resumed in a new agent process); a lower one is
refused; the same one refreshes. An owner's exit ends only the generation that
registered it, so a stale exit can never drop a resumed session.

Persisted to `sessions.json` on every change, so a restarted service (a crash,
later an update) knows its live sessions before any registrant re-sends.

Stdlib only (the start path; plan S1).
"""

from __future__ import annotations

import json
import os
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from . import procid
from .protocol import ErrorCode, Mode, RefusedReason, RpcError

#: A heartbeat-only owner is alive this long after its last register (API v1).
HEARTBEAT_TTL_S = 120.0
#: How long an ended (sid, generation) keeps refusing a late re-register.
TOMBSTONE_S = 600.0
REGISTRY_VERSION = 1


class Outcome:
    NEW = "new"
    REPLACED = "replaced"
    REFRESHED = "refreshed"
    #: The owner named is not running (gone, a zombie, a recycled pid): not stored.
    DEAD = "dead"


@dataclass
class Session:
    sid: str
    harness: str
    mode: str
    owner: dict | None
    generation: int
    registered_at: float
    heartbeat_at: float
    #: False once the owner's exit was seen. Unknown (unreadable start) counts as live.
    owner_live: bool = True
    #: The session's own state folder (`$XDG_STATE_HOME/probe`, or the default)
    #: when its registrant said (plan D13): where its daemon worker, its runs
    #: and a setup it started keep their locks. None: an older registrant.
    state_dir: str | None = None
    #: Its registrant was no more confined than the service (`caller.sandboxed`)
    #: at its last register: only then does the service act for the session
    #: with this user's own key (its run alerts, plan Q2). Never stored: the
    #: next heartbeat says it again.
    unconfined: bool = False
    #: Whether its registrant's environment allows automatic diagnostic
    #: reports (`session.register`'s `report_env`, crash-report plan B2); None:
    #: it did not say (an older registrant), which the watch reads as no.
    report_env: bool | None = None

    def alive(self, now: float, ttl: float) -> bool:
        if self.mode == Mode.OFF:
            return False
        if self.owner is None:
            return now - self.heartbeat_at < ttl
        return self.owner_live

    def public(self, now: float, ttl: float) -> dict:
        return {
            "sid": self.sid,
            "harness": self.harness,
            "mode": self.mode,
            "alive": self.alive(now, ttl),
            "owner": dict(self.owner) if self.owner else None,
            "generation": self.generation,
            "registered_at": self.registered_at,
        }

    def stored(self) -> dict:
        return {
            "sid": self.sid,
            "harness": self.harness,
            "mode": self.mode,
            "owner": self.owner,
            "generation": self.generation,
            "registered_at": self.registered_at,
            "heartbeat_at": self.heartbeat_at,
            "state_dir": self.state_dir,
            # The keeper reads it here (no service to ask: `watch.sessions_on_disk`).
            "report_env": self.report_env,
        }


@dataclass
class Registration:
    outcome: str
    session: Session
    #: The registration this one replaced (Outcome.REPLACED), for its watcher.
    previous: Session | None = None


@dataclass
class Registry:
    path: Path
    ttl: float = HEARTBEAT_TTL_S
    clock: Callable[[], float] = time.time
    #: `procid.alive`, swappable so a unit test needs no real process.
    owner_alive: Callable[[int, str], bool | None] = procid.alive
    sessions: dict = field(default_factory=dict)
    #: sid -> (generation it ended at, refuse re-registers until)
    tombstones: dict = field(default_factory=dict)

    # -- queries -------------------------------------------------------------

    def alive_count(self) -> int:
        now = self.clock()
        return sum(1 for session in self.sessions.values() if session.alive(now, self.ttl))

    def daemon_alive(self) -> bool:
        """Is a live session registered in daemon mode (its worker recording)?"""
        now = self.clock()
        return any(s.mode == Mode.DAEMON and s.alive(now, self.ttl) for s in self.sessions.values())

    def daemon_unseen(self) -> bool:
        """Is a live daemon-mode session registered WITHOUT its state folder?
        Its worker's lock may sit where the updater cannot look (an older
        registrant under XDG_STATE_HOME), so only the registration says a
        worker records."""
        now = self.clock()
        return any(
            s.mode == Mode.DAEMON and s.state_dir is None and s.alive(now, self.ttl) for s in self.sessions.values()
        )

    def live_sids(self) -> set:
        """The ids of every live session."""
        now = self.clock()
        return {s.sid for s in self.sessions.values() if s.alive(now, self.ttl)}

    def state_dirs(self) -> set:
        """Every live session's state folder its registrant named (plan D13)."""
        now = self.clock()
        return {s.state_dir for s in self.sessions.values() if s.state_dir and s.alive(now, self.ttl)}

    def owners(self) -> dict:
        """`{(owner pid, owner start time): session}` of every live session with an owner."""
        now = self.clock()
        return {
            (s.owner["pid"], s.owner["start_time"]): s
            for s in self.sessions.values()
            if s.owner is not None and s.alive(now, self.ttl)
        }

    def listing(self) -> list[dict]:
        now = self.clock()
        return [s.public(now, self.ttl) for s in sorted(self.sessions.values(), key=lambda s: s.registered_at)]

    def expired(self) -> list[Session]:
        """Heartbeat-only sessions past the TTL (the caller drops them)."""
        now = self.clock()
        return [
            s for s in self.sessions.values() if s.owner is None and now - s.heartbeat_at >= self.ttl
        ]

    def next_expiry(self) -> float | None:
        """When the earliest heartbeat-only session lapses (wall clock), if any."""
        due = [s.heartbeat_at + self.ttl for s in self.sessions.values() if s.owner is None]
        return min(due) if due else None

    # -- changes -------------------------------------------------------------

    def _refuse_stale(self, sid: str, generation: int) -> None:
        current = self.sessions.get(sid)
        if current is not None and generation < current.generation:
            raise RpcError(
                ErrorCode.REFUSED,
                f"generation {generation} is older than the registered {current.generation}",
                {"reason": RefusedReason.STALE_GENERATION, "generation": current.generation},
            )
        tomb = self.tombstones.get(sid)
        if current is None and tomb is not None:
            ended, until = tomb
            if self.clock() >= until:
                del self.tombstones[sid]
            elif generation <= ended:
                raise RpcError(
                    ErrorCode.REFUSED,
                    f"generation {generation} of this session already ended",
                    {"reason": RefusedReason.STALE_GENERATION, "generation": ended},
                )

    def register(
        self, sid: str, harness: str, mode: str, owner: dict | None, generation: int, state_dir: str | None = None,
        report_env: bool | None = None,
    ) -> Registration:
        self._refuse_stale(sid, generation)
        now = self.clock()
        current = self.sessions.get(sid)
        same_owner = current is not None and current.owner == owner
        if current is not None and current.generation == generation and same_owner:
            current.harness = harness
            current.mode = mode
            current.heartbeat_at = now
            current.state_dir = state_dir
            if report_env is not None:
                # A register that says nothing (`session.record`'s, for a hosted
                # session) leaves what its link said.
                current.report_env = report_env
            self.save()
            return Registration(Outcome.REFRESHED, current)
        if owner is not None and self.owner_alive(owner["pid"], owner["start_time"]) is False:
            # Never stored: a dead owner cannot hold the service, and storing it
            # would only wait for an exit event that already happened.
            dead = Session(sid, harness, mode, owner, generation, now, now, owner_live=False, state_dir=state_dir,
                           report_env=report_env)
            return Registration(Outcome.DEAD, dead, current)
        if report_env is None and current is not None:
            report_env = current.report_env  # what its registrant said last, until it says again
        session = Session(sid, harness, mode, owner, generation, now, now, state_dir=state_dir, report_env=report_env)
        self.sessions[sid] = session
        self.tombstones.pop(sid, None)
        self.save()
        if current is None:
            return Registration(Outcome.NEW, session)
        return Registration(Outcome.REPLACED, session, current)

    def end(self, sid: str, generation: int) -> Session | None:
        """`session.end` (a hint; the owner's exit is the truth).

        Idempotent: ending a session that is not here (already ended, never
        registered, dropped on its owner's exit) answers nothing and remembers
        the generation, so a late register cannot revive it. A LOWER generation
        than the registered one is refused: it is a superseded registrant, and
        the resumed session is not its to end. A higher one ends the session,
        as a higher register would replace it.
        """
        current = self.sessions.get(sid)
        if current is None:
            ended = self.tombstones.get(sid, (-1, 0.0))[0]
            self.tombstones[sid] = (max(ended, generation), self.clock() + TOMBSTONE_S)
            return None
        if generation < current.generation:
            self._refuse_stale(sid, generation)
        removed = self.drop(sid, current.generation)
        if removed is not None and generation > removed.generation:
            self.tombstones[sid] = (generation, self.clock() + TOMBSTONE_S)
        return removed

    def drop(self, sid: str, generation: int) -> Session | None:
        """Remove (sid, generation) -- an owner exit, a lapse, an end. Other
        generations of the sid are left alone."""
        current = self.sessions.get(sid)
        if current is None or current.generation != generation:
            return None
        del self.sessions[sid]
        self.tombstones[sid] = (generation, self.clock() + TOMBSTONE_S)
        self.save()
        return current

    # -- disk ----------------------------------------------------------------

    def save(self) -> None:
        payload = {
            "v": REGISTRY_VERSION,
            "saved_at": self.clock(),
            "sessions": [s.stored() for s in self.sessions.values()],
        }
        try:
            fd, tmp = tempfile.mkstemp(prefix=self.path.name + ".", suffix=".tmp", dir=str(self.path.parent))
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    json.dump(payload, handle, separators=(",", ":"))
                os.replace(tmp, self.path)
            except BaseException:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
                raise
        except OSError:
            pass  # the registrants re-send within 30 s; a lost write costs nothing more

    def load(self) -> list[Session]:
        """Restore what a previous service knew: owners still running, and
        heartbeat-only sessions still inside their TTL. Returns what was kept."""
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return []
        if not isinstance(data, dict) or data.get("v") != REGISTRY_VERSION:
            return []
        now = self.clock()
        kept: list[Session] = []
        for raw in data.get("sessions") or []:
            try:
                session = Session(
                    sid=str(raw["sid"]),
                    harness=str(raw["harness"]),
                    mode=str(raw["mode"]),
                    owner=raw["owner"] if raw.get("owner") is None else {
                        "pid": int(raw["owner"]["pid"]),
                        "start_time": str(raw["owner"]["start_time"]),
                    },
                    generation=int(raw["generation"]),
                    registered_at=float(raw["registered_at"]),
                    heartbeat_at=float(raw["heartbeat_at"]),
                    state_dir=raw["state_dir"] if isinstance(raw.get("state_dir"), str) else None,
                    report_env=raw["report_env"] if isinstance(raw.get("report_env"), bool) else None,
                )
            except (KeyError, TypeError, ValueError):
                continue
            if session.mode not in (Mode.DAEMON, Mode.INLINE, Mode.OFF):
                continue
            if session.owner is None:
                if now - session.heartbeat_at >= self.ttl:
                    continue
            elif self.owner_alive(session.owner["pid"], session.owner["start_time"]) is False:
                continue
            self.sessions[session.sid] = session
            kept.append(session)
        self.save()
        return kept
