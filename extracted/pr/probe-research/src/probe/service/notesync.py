"""`notes.sync`: the team note's sync, run once per machine and debounced (plan Q4).

The team note is ONE file per machine (`<state>/team-note/probe-team-note.md`),
shared by every session on it, and three hook events sync it: a session's start
(`probe agent-rules refresh; probe notes sync`, plus `probe feedback flush` when
an approved feedback waits), every Stop (`probe notes sync --push-only`) and a
session's end (`probe notes sync`). Each used to spawn a detached `probe` of its
own, per session and per event. Where a service answers, the hook asks it
instead and returns; the service runs them as one job per context:

    debounced       a request starts a run DEBOUNCE_S later; what arrives
                    meanwhile joins it (five sessions' Stops are one push)
    one at a time   while a run is in flight, requests join the ONE run right
                    after it (`queued`), never a second run beside it
    merged          a run does the most anyone asked: `reconcile` covers
                    `push`; every agent's `agent-rules refresh` asked for runs
                    (once each, `PROBE_AGENT` set to it, "" for the CLI's own
                    default), then the note's sync, then `feedback flush`
    the commands    `probe <args>` with the CLI's own interpreter and the
                    caller's context as its environment; each bounded by
                    TIMEOUT_S, their output discarded as the detached spawn's
                    was; none starts while the service's own update replaces
                    the CLI's files in place (`held`: the run waits)
    holds           a run waiting or in flight keeps the service up: a
                    session's end is the sync that must not be lost

A caller in a sandbox is refused (the commands would run outside it), and a hook
whose environment holds a credential the service cannot be given
(`protocol.CREDENTIAL_ENV`) does not ask: those hooks spawn the commands as before.
A run handed off at the service's stop runs beside the command still running
there: both take the instruction file's own lock (`team_note_file.
instruction_lock_path`), so they never write it at once.

Stdlib only (the start path; plan S1).
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field

from . import children, paths
from .protocol import JobOutcome, NotesMode

#: A burst of hooks (several sessions' Stops, a start right after an end) is one run.
DEBOUNCE_S = 2.0
#: One command past this is killed (`notes sync` makes a few requests).
TIMEOUT_S = 120.0
#: Contexts with a job at once; past it a request is refused (the hook spawns its own).
MAX_JOBS = 8
#: `agent-rules refresh`es one run may do.
MAX_AGENTS = 8


@dataclass
class _Wanted:
    reconcile: bool = False
    #: PROBE_AGENT values for `agent-rules refresh` ("" = unset), in the order asked.
    agents: dict = field(default_factory=dict)
    feedback: bool = False

    def add(self, mode: str, agents: list, feedback: bool) -> None:
        self.reconcile = self.reconcile or mode == NotesMode.RECONCILE
        for agent in agents:
            if len(self.agents) < MAX_AGENTS:
                self.agents.setdefault(agent, None)
        self.feedback = self.feedback or feedback

    def commands(self) -> list[tuple[list[str], dict]]:
        """`(probe args, extra environment)` for each command, in order."""
        out: list[tuple[list[str], dict]] = []
        for agent in self.agents:
            out.append((["agent-rules", "refresh"], {"PROBE_AGENT": agent} if agent else {}))
        out.append((["notes", "sync"] if self.reconcile else ["notes", "sync", "--push-only"], {}))
        if self.feedback:
            out.append((["feedback", "flush"], {}))
        return out


@dataclass
class _Job:
    env: dict
    wanted: _Wanted | None = None
    timer: asyncio.TimerHandle | None = None
    running: asyncio.Task | None = None
    #: The running run's commands not started yet.
    remaining: list = field(default_factory=list)


class NoteSync:
    def __init__(
        self,
        *,
        log: Callable[[str], None],
        changed: Callable[[], None] = lambda: None,
        held: Callable[[], bool] = lambda: False,
    ) -> None:
        self.log = log
        self._changed = changed
        #: True while no `probe` may start (an in-place update replaces its files).
        self.held = held
        self.jobs: dict[str, _Job] = {}
        self._closed = False
        #: Runs so far, and the last one's outcome (`service.status`; the tests read it).
        self.runs = 0
        self.last: dict | None = None

    @staticmethod
    def key(env: dict) -> str:
        return json.dumps(sorted(env.items()))

    def request(self, env: dict, mode: str, agents: list, feedback: bool) -> dict:
        """`{outcome: scheduled | queued}`, or `{outcome: null, reason}` when it
        cannot be taken (the hook then spawns its own)."""
        if self._closed:
            return {"outcome": None, "reason": "the service is stopping"}
        key = self.key(env)
        job = self.jobs.get(key)
        if job is None:
            for old, idle in list(self.jobs.items()):
                if idle.wanted is None and idle.timer is None and idle.running is None:
                    del self.jobs[old]
            if len(self.jobs) >= MAX_JOBS:
                return {"outcome": None, "reason": "busy: too many contexts syncing"}
            job = self.jobs[key] = _Job(dict(env))
        if job.wanted is None:
            job.wanted = _Wanted()
        job.wanted.add(mode, agents, feedback)
        if job.running is not None:
            return {"outcome": JobOutcome.QUEUED}
        if job.timer is None:
            job.timer = asyncio.get_running_loop().call_later(DEBOUNCE_S, self._start, job)
            self._changed()
        return {"outcome": JobOutcome.SCHEDULED}

    def _start(self, job: _Job) -> None:
        job.timer = None
        if self._closed or job.running is not None or job.wanted is None:
            return
        if self.held():
            job.timer = asyncio.get_running_loop().call_later(DEBOUNCE_S, self._start, job)
            return
        wanted, job.wanted = job.wanted, None
        job.running = asyncio.ensure_future(self._run(job, wanted))
        self._changed()

    async def _run(self, job: _Job, wanted: _Wanted) -> None:
        self.runs += 1
        results = []
        started = time.time()
        job.remaining = wanted.commands()
        while job.remaining:
            args, extra = job.remaining.pop(0)
            try:
                code = await children.run_command(
                    children.cli_argv(args),
                    env=children.cli_env({**job.env, **extra}),
                    cwd=str(paths.home()),
                    timeout=TIMEOUT_S,
                )
                outcome = "timed out" if code is None else code
            except OSError as exc:
                outcome = f"could not start: {exc}"
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001 -- the next command still runs
                outcome = f"failed: {exc!r}"
            results.append({"command": " ".join(args), "agent": extra.get("PROBE_AGENT"), "exit": outcome})
        self.last = {
            "at": started,
            "mode": NotesMode.RECONCILE if wanted.reconcile else NotesMode.PUSH,
            "commands": results,
        }
        # 2: `notes sync` found a conflict, which the file now carries (markers);
        # a person resolves it. Anything else but 0 is worth a line in the log.
        failed = ["%s: %s" % (r["command"], r["exit"]) for r in results if r["exit"] not in (0, 2)]
        if failed:
            self.log("notes.sync: " + "; ".join(failed))
        job.running = None
        if job.wanted is not None and not self._closed:
            job.timer = asyncio.get_running_loop().call_later(DEBOUNCE_S, self._start, job)
        self._changed()

    def in_flight(self) -> bool:
        return any(j.timer is not None or j.running is not None for j in self.jobs.values())

    def public(self) -> dict:
        return {
            "running": any(j.running is not None for j in self.jobs.values()),
            "waiting": any(j.timer is not None or (j.wanted is not None) for j in self.jobs.values()),
            "runs": self.runs,
            "last": json.loads(json.dumps(self.last)) if self.last else None,
        }

    def close(self) -> None:
        """The service stops: a run waiting or half done is handed to ONE
        detached shell, as the hooks used to spawn it, so a session's last
        sync is not lost with the service (the command that is running goes
        on by itself: `children.spawn_watched`)."""
        self._closed = True
        for job in self.jobs.values():
            if job.timer is not None:
                job.timer.cancel()
                job.timer = None
            left = list(job.remaining) + (job.wanted.commands() if job.wanted is not None else [])
            job.remaining, job.wanted = [], None
            if job.running is not None:
                with contextlib.suppress(Exception):
                    job.running.cancel()
            if left:
                self._hand_off(job.env, left)

    def _hand_off(self, env: dict, commands: list) -> None:
        import shlex
        import subprocess

        line = "; ".join(
            " ".join([*(f"{k}={shlex.quote(v)}" for k, v in extra.items()), *map(shlex.quote, children.cli_argv(args))])
            for args, extra in commands
        )
        try:
            subprocess.Popen(  # noqa: S603 -- /bin/sh over our own quoted argv
                ["/bin/sh", "-c", line],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=str(paths.home()),
                env=children.cli_env(env),
                start_new_session=True,
                close_fds=True,
            )
            self.log(f"notes.sync: the service is stopping; {len(commands)} command(s) handed to a detached shell")
        except OSError as exc:
            self.log(f"notes.sync: could not hand the sync off ({exc}); the next session's sync carries it")
