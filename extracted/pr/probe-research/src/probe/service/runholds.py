"""The training runs a `probe exec` wraps on this machine, as the service sees them.

    run.hold     a `probe exec` names the run it wraps and itself (`{pid,
                 start_time}`) once its run is open: the updater's quiet check
                 (X1) reads it as a run in flight, without a lock-file scan and
                 in whatever state folder that run keeps its lock. Watched like
                 a session's owner (pidfd / kqueue / a poll): the hold goes when
                 that process exits, however it exits
    run.release  its run is over: the hold leaves the listing now, but its
                 process still holds updates off until it exits (it is still
                 cleaning up, importing from the env an update replaces); only
                 that process (or one it runs under) may release its hold
    runs.json    0600, beside the registry: the holds a restarted service
                 picks up, released ones still running included (marked
                 `released`); one whose process is gone is dropped as it loads

The run's flock (`probe._shared.run_lock`) stays: it is what a service from
before this, the CLI's own updater and the update child read, so a hold only
adds to it. A hold never keeps the service alive: with no service there is no
updater to protect the run from, and the next service loads it.

Stdlib only (the start path; plan S1).
"""

from __future__ import annotations

import json
import os
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from . import procid

RUNS_NAME = "runs.json"
RUNS_VERSION = 1
#: Holds kept at once: far past any real number of concurrent wrapped runs
#: (a sweep is tens). A hold past it is refused, never another one dropped.
MAX_HOLDS = 512


@dataclass(frozen=True)
class Hold:
    run: str
    owner: dict
    since: float

    @property
    def key(self) -> tuple:
        """The pid watcher's key: never a session's `(sid, generation)`."""
        return ("run", self.run, self.owner["pid"])

    def public(self) -> dict:
        return {"run": self.run, "pid": self.owner["pid"], "since": self.since}

    def stored(self) -> dict:
        return {"run": self.run, "owner": dict(self.owner), "since": self.since}


class RunHolds:
    def __init__(
        self,
        path: Path,
        *,
        owner_alive: Callable[[int, str], bool | None] = procid.alive,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self.path = path
        self.owner_alive = owner_alive
        self.clock = clock
        self.holds: dict[tuple, Hold] = {}
        #: Released holds whose process still runs: no longer listed, still
        #: busy for the updater until that process exits. Saved too (marked
        #: `released`): a service that restarts before that exit keeps them.
        self.releasing: dict[tuple, Hold] = {}

    # -- queries -------------------------------------------------------------

    def live(self) -> bool:
        """Does anything hold updates off: a hold, or a released one's process?"""
        return bool(self.holds or self.releasing)

    def public(self) -> list[dict]:
        return [h.public() for h in sorted(self.holds.values(), key=lambda h: h.since)]

    # -- changes -------------------------------------------------------------

    def add(self, run: str, owner: dict) -> tuple[Hold | None, bool]:
        """`(hold, new)`; `(None, False)` when MAX_HOLDS are held already.
        The caller checked the owner runs."""
        key = ("run", run, owner["pid"])
        current = self.holds.get(key)
        if current is not None and current.owner == owner:
            return current, False
        # Released owners still running count too: every hold a restart must
        # restore fits the limit, so `load` never has to drop one.
        taken = len(self.holds) + len(self.releasing) - (1 if key in self.releasing else 0)
        if current is None and taken >= MAX_HOLDS:
            return None, False
        hold = Hold(run, dict(owner), self.clock())
        self.holds[key] = hold
        self.releasing.pop(key, None)
        self.save()
        return hold, True

    def release(self, run: str, chain: set, pid: int | None = None) -> list[Hold]:
        """The holds of `run` whose owner `(pid, start time)` is in `chain`
        (the caller and the processes it runs under), only `pid`'s when named.
        They leave the listing and stay in `releasing` until their process
        exits (`drop`). Returns them."""
        gone = [
            h for h in self.holds.values()
            if h.run == run and (h.owner["pid"], h.owner["start_time"]) in chain
            and (pid is None or h.owner["pid"] == pid)
        ]
        for hold in gone:
            del self.holds[hold.key]
            self.releasing[hold.key] = hold
        if gone:
            self.save()
        return gone

    def drop(self, hold: Hold) -> bool:
        """Its owner exited: this exact hold goes, held or released (a newer
        one of the same key stays)."""
        if self.releasing.get(hold.key) is hold:
            del self.releasing[hold.key]
            self.save()
            return True
        if self.holds.get(hold.key) is not hold:
            return False
        del self.holds[hold.key]
        self.save()
        return True

    # -- disk ----------------------------------------------------------------

    def save(self) -> None:
        payload = {
            "v": RUNS_VERSION,
            "holds": [h.stored() for h in self.holds.values()]
            + [{**h.stored(), "released": True} for h in self.releasing.values()],
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
            pass  # the run's flock still says it runs

    def load(self) -> list[Hold]:
        """What a previous service held, for owners still running, and the
        released ones whose process still runs (`releasing` again). Returns
        every one kept, for the caller to watch its owner."""
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return []
        if not isinstance(data, dict) or data.get("v") != RUNS_VERSION:
            return []
        kept: list[Hold] = []
        for raw in data.get("holds") or []:
            try:
                owner = {"pid": int(raw["owner"]["pid"]), "start_time": str(raw["owner"]["start_time"])}
                hold = Hold(str(raw["run"]), owner, float(raw["since"]))
            except (KeyError, TypeError, ValueError):
                continue
            if not hold.run or owner["pid"] <= 1 or self.owner_alive(owner["pid"], owner["start_time"]) is False:
                continue
            # No limit here: everything saved was admitted under it (a file
            # from before the combined limit may hold more; dropping one would
            # let an update run under its still-running owner).
            (self.releasing if raw.get("released") is True else self.holds)[hold.key] = hold
            kept.append(hold)
        self.save()
        return kept
