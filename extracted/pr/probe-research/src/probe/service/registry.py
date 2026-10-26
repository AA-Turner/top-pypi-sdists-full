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

THE REGISTRANT (#3360). Any process of this user reaches the service's socket,
the agent's own shell among them, and `session.list` names every session's id
and generation. So each registration remembers the process that made it (the
pid and start time the kernel names for its connection, or this service
itself: `SERVICE`), and only that process, or this service, may END it, name
it another OWNER, or move it OUT OF DAEMON MODE (`holds`). Anyone else is
refused (`Bound.NOT_REGISTRANT`) while that process runs and the session's
agent does. Other same-owner registers stay open to every caller: the recorder
hand-offs (`session.record` from a hook, a `tap watch` taking its session back)
re-register from another process with the owner unchanged, and an old tap
cannot prove anything more. Such a register moves the registrant only where
nobody holds the registration (`_vacant`: no registrant known, as for a session
open across the upgrade; its registrant exited; or this service registered it
and no longer records it), and never moves the state folder or the report
consent of one somebody holds.

DAEMON OWNERS (#3360). An agent process once registered in daemon mode is
remembered (`daemon_owners`) until it exits, whatever later registrations say:
`action.run` and `desktop.request` refuse a caller under it
(`server._caller_sessions`) even after its session was ended, replaced or
re-registered `inline`. Every register naming daemon mode adds to it, refused
or not, and a running agent is never dropped to make room (the list grows past
`MAX_DAEMON_OWNERS`, exited agents going first), so a forged registration can
make the refusal wider, never narrower. Only a process that looks like a coding
agent is remembered (`caller.agent_like`): a fake daemon registration naming
the desktop app or `systemd --user` ends with that registration. One naming
another running agent still sticks to that agent until it exits.

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
from .caller import Bound, agent_like, same_process
from .protocol import ErrorCode, Mode, RefusedReason, RpcError

#: A heartbeat-only owner is alive this long after its last register (API v1).
HEARTBEAT_TTL_S = 120.0
#: How long an ended (sid, generation) keeps refusing a late re-register.
TOMBSTONE_S = 600.0
REGISTRY_VERSION = 1
#: The registrant of a registration this service made itself (`session.record`'s
#: hosted links connect from this process; a resumed recorder registers here).
#: Stored as is, so the next service is the registrant of what it resumes.
SERVICE = "service"
#: Past this many daemon owners (`daemon_owners`) the exited ones are dropped
#: first; running ones are never dropped, so the list grows past it if it must.
MAX_DAEMON_OWNERS = 256
#: At most this many processes are remembered as checked and not an agent.
MAX_NOT_AGENTS = 1024


def _agent_process(pid: int, start: str) -> bool:
    return agent_like(pid)


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
    #: The process that registered it (`{pid, start_time}`), `SERVICE`, or None:
    #: unknown (a registry an older service wrote), which binds nothing (#3360).
    registrant: dict | str | None = None

    def alive(self, now: float, ttl: float) -> bool:
        if self.mode == Mode.OFF:
            return False
        if self.owner is None:
            return now - self.heartbeat_at < ttl
        return self.owner_live

    def agent_live(self, now: float, ttl: float) -> bool:
        """Does its agent still run, whatever its mode? `alive` without the
        mode: an off session's agent is watched like any other's."""
        if self.owner is None:
            return now - self.heartbeat_at < ttl
        return self.owner_live

    def public(self, now: float, ttl: float) -> dict:
        return {
            "sid": self.sid,
            "harness": self.harness,
            "mode": self.mode,
            "alive": self.alive(now, ttl),
            # `alive` is False for every session in mode off by design; this
            # says whether its agent runs (`probe doctor`'s "(off)").
            "agent_live": self.agent_live(now, ttl),
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
            "registrant": self.registrant,
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
    #: (owner pid, owner start time) -> {"sid", "harness", "at"}: every agent
    #: process ever registered in daemon mode, until it exits (#3360; module doc).
    daemon_owners: dict = field(default_factory=dict)
    #: Does the process (pid, start) look like a coding agent (`caller.agent_like`)?
    agent_like: Callable[[int, str], bool] = _agent_process
    #: Does this service still record `sid` (its hosted recorder runs)? The
    #: service sets it; a registry on its own reads every one as recorded.
    service_records: Callable[[str], bool] = lambda sid: True
    #: Owners checked and found not to be agents (never asked twice).
    _not_agents: set = field(default_factory=set)
    #: The list's size at which exited owners are next looked for.
    _prune_at: int = 0

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

    def owned(self, pid: int, start: str) -> list[Session]:
        """Every live session whose owner is the process (pid, start): a forged
        registration under the same owner never hides the real one."""
        now = self.clock()
        return [
            s for s in self.sessions.values()
            if s.owner is not None and s.alive(now, self.ttl)
            and s.owner["pid"] == pid and s.owner["start_time"] == start
        ]

    def daemon_owner(self, pid: int, start: str) -> dict | None:
        """`{"sid", "harness"}` when the process (pid, start) was registered in
        daemon mode and has not been seen to exit, else None."""
        return self.daemon_owners.get((pid, start))

    def daemon_agent_runs(self, sid: str) -> bool:
        """Does an agent remembered as registered for `sid` in daemon mode still
        run? (A session id a caller's environment names: Linux, where this is a
        /proc read; the agent of an ended registration is watched by nothing.)"""
        return any(
            entry["sid"] == sid and self.owner_alive(pid, start) is not False
            for (pid, start), entry in list(self.daemon_owners.items())
        )

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

    def holds(self, current: Session, caller: dict | str | None) -> bool:
        """May `caller` end `current`, name it another owner, or move it out of
        daemon mode (#3360)? This service may; so may the process that
        registered it. Anyone else only where nobody holds it (`_vacant`), or
        once the session's agent has exited (a session that is over is anyone's
        to take up again: a resume). `caller` None: a connection whose process
        the kernel did not name."""
        if caller == SERVICE:
            return True
        if isinstance(caller, dict) and same_process(current.registrant, caller):
            return True
        return self._vacant(current) or not self._agent_runs(current)

    def _vacant(self, current: Session) -> bool:
        """Does nobody hold this registration: no registrant known (a registry
        an older service wrote), its registrant has exited, or this service
        registered it and no longer records the session?"""
        registrant = current.registrant
        if registrant is None:
            return True
        if registrant == SERVICE:
            return not self.service_records(current.sid)
        return self.owner_alive(registrant["pid"], registrant.get("start_time") or "") is False

    def _agent_runs(self, session: Session) -> bool:
        """Does the session's agent still run (whatever its mode; unknown: yes)?"""
        if session.owner is None:
            return self.clock() - session.heartbeat_at < self.ttl
        return self.owner_alive(session.owner["pid"], session.owner["start_time"]) is not False

    def _refuse_unbound(self, current: Session, caller: dict | str | None, what: str) -> None:
        if not self.holds(current, caller):
            raise RpcError(
                ErrorCode.REFUSED,
                f"refused: session {current.sid} was registered by another process; only it (or the Probe "
                f"service) may {what}",
                {"reason": Bound.NOT_REGISTRANT},
            )

    def note_daemon_owner(self, owner: dict | None, sid: str, harness: str, *, known_alive: bool = False) -> None:
        """Remember `owner` as an agent registered in daemon mode (module doc).
        Unless `known_alive`, an owner not running is not remembered (it could
        never be anyone's ancestor again); nor is one that does not look like a
        coding agent (`agent_like`). Past `MAX_DAEMON_OWNERS` the exited ones
        go first, looked for again only once the list has doubled since; a
        running one is never dropped."""
        if not isinstance(owner, dict):
            return
        key = (owner["pid"], owner["start_time"])
        if key in self.daemon_owners or key in self._not_agents:
            return
        if not known_alive and self.owner_alive(*key) is False:
            return
        if not self.agent_like(*key):
            if len(self._not_agents) >= MAX_NOT_AGENTS:
                self._not_agents.clear()
            self._not_agents.add(key)
            return
        if len(self.daemon_owners) >= max(MAX_DAEMON_OWNERS, self._prune_at):
            for gone in [k for k in self.daemon_owners if self.owner_alive(*k) is False]:
                del self.daemon_owners[gone]
            self._prune_at = 2 * len(self.daemon_owners)
        self.daemon_owners[key] = {"sid": sid, "harness": harness, "at": self.clock()}
        self.save()  # also when the register that named it is refused next

    def forget_daemon_owner(self, owner: dict | None) -> None:
        """The agent process `owner` exited: nothing can run under it any more."""
        if isinstance(owner, dict) and self.daemon_owners.pop((owner["pid"], owner["start_time"]), None) is not None:
            self.save()

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
        report_env: bool | None = None, caller: dict | str | None = SERVICE,
    ) -> Registration:
        """`session.register` from `caller` (`holds`: `SERVICE` for this
        service's own, else the connecting process `{pid, start_time}`, None
        when the kernel named none). A register naming another owner than the
        live registration's is refused unless the caller holds it."""
        current = self.sessions.get(sid)
        if mode == Mode.DAEMON:
            # Before any refusal: a register the service turns down still says
            # which agent runs under the daemon (the set only narrows on exits).
            same = current is not None and current.owner == owner and current.owner_live
            self.note_daemon_owner(owner, sid, harness, known_alive=same)
        self._refuse_stale(sid, generation)
        now = self.clock()
        if current is not None and current.owner != owner:
            self._refuse_unbound(current, caller, "name it another owner")
        if current is not None and current.mode == Mode.DAEMON and mode != Mode.DAEMON:
            self._refuse_unbound(current, caller, "move it out of daemon mode")
        registrant_calls = isinstance(caller, dict) and current is not None and same_process(current.registrant, caller)
        # A caller the kernel named takes up a registration nobody holds (a
        # session open across the upgrade, a hand-off whose registrant left).
        takes = (isinstance(caller, dict) and current is not None and not registrant_calls
                 and self._vacant(current))
        bound = current is not None and (caller == SERVICE or registrant_calls or takes)
        same_owner = current is not None and current.owner == owner
        if current is not None and current.generation == generation and same_owner:
            current.harness = harness
            current.mode = mode
            current.heartbeat_at = now
            if bound or current.state_dir is None:
                # Its folder is what its registrant said: a same-owner register
                # from another process cannot move where the service looks.
                current.state_dir = state_dir
            if report_env is not None and (bound or current.report_env is None):
                # A register that says nothing (`session.record`'s, for a hosted
                # session) leaves what its link said.
                current.report_env = report_env
            if caller == SERVICE or takes:
                current.registrant = caller
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
        registrant = caller
        if same_owner and not bound:
            # A hand-off's register (`session.record` from a hook, a `tap watch`
            # taking its session back): the session goes on, its registrant,
            # folder and report consent with it.
            registrant = current.registrant
            state_dir = current.state_dir if current.state_dir is not None else state_dir
            report_env = current.report_env if current.report_env is not None else report_env
        session = Session(sid, harness, mode, owner, generation, now, now, state_dir=state_dir, report_env=report_env,
                          registrant=registrant)
        self.sessions[sid] = session
        self.tombstones.pop(sid, None)
        self.save()
        if current is None:
            return Registration(Outcome.NEW, session)
        return Registration(Outcome.REPLACED, session, current)

    def end(self, sid: str, generation: int, caller: dict | str | None = SERVICE) -> Session | None:
        """`session.end` (a hint; the owner's exit is the truth).

        Idempotent: ending a session that is not here (already ended, never
        registered, dropped on its owner's exit) answers nothing and remembers
        the generation, so a late register cannot revive it. A LOWER generation
        than the registered one is refused: it is a superseded registrant, and
        the resumed session is not its to end. A higher one ends the session,
        as a higher register would replace it. A registered session is ended
        only by a caller that `holds` it (#3360): its registrant or this service.
        """
        current = self.sessions.get(sid)
        if current is None:
            ended = self.tombstones.get(sid, (-1, 0.0))[0]
            self.tombstones[sid] = (max(ended, generation), self.clock() + TOMBSTONE_S)
            return None
        if generation < current.generation:
            self._refuse_stale(sid, generation)
        self._refuse_unbound(current, caller, "end it")
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
            # A service before #3360 reads none of it (it keeps `v` 1).
            "daemon_owners": [
                {"pid": pid, "start_time": start, **entry} for (pid, start), entry in self.daemon_owners.items()
            ],
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
                    registrant=_stored_registrant(raw.get("registrant")),
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
        for raw in data.get("daemon_owners") or []:
            try:
                pid, start = int(raw["pid"]), str(raw["start_time"])
                entry = {"sid": str(raw["sid"]), "harness": str(raw["harness"]), "at": float(raw["at"])}
            except (KeyError, TypeError, ValueError):
                continue
            # `exists`, never `alive`: a `ps` per owner on macOS is no start-up
            # cost to pay for a record that matches nothing once its owner is gone.
            if pid > 1 and start and procid.exists(pid) and len(self.daemon_owners) < MAX_DAEMON_OWNERS:
                self.daemon_owners[(pid, start)] = entry
        self.save()
        return kept


def _stored_registrant(raw: object) -> dict | str | None:
    """A stored registrant: `SERVICE`, `{pid, start_time}`, else None (unknown)."""
    if raw == SERVICE:
        return SERVICE
    if isinstance(raw, dict):
        try:
            return {"pid": int(raw["pid"]), "start_time": str(raw.get("start_time") or "")}
        except (KeyError, TypeError, ValueError):
            return None
    return None
