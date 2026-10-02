"""The watch: notice that a registered process is gone, and say so.

WHAT THIS REPORTS, AND WHAT IT DOES NOT. A sibling process cannot reap another
process, so this can never read an exit status the way `probe exec` reads its
own child's. What it can do -- and what nothing else in the system can -- is
observe that the process owning a run STOPPED EXISTING, at a known second,
while the run was still open.

That is worth reporting on its own for two reasons.

The server already infers a death, but only from silence: the heartbeat goes
stale after 900 seconds and the reaper sweeps every 120, so a dead run is
noticed somewhere between fifteen and seventeen minutes later. This notices in
one poll interval, and it is not an inference -- the process is gone or it is
not.

And the two facts are different facts. A stale heartbeat means "nothing has
reported recently", which a wedged process, a full disk and a network partition
all produce while the job is still alive. A vanished pid means the job is
actually gone. Only one of those is worth waking somebody for, and until now
they were indistinguishable.

WHY THE EVIDENCE IS WRITTEN AS A SPAN. Spans are already client-writable,
already tenant-isolated, already attached to the run a reader opens. Findings
are not: `run_findings` is written server-side, and giving a node process its
own write door to that table is a larger claim than this phase needs. So the
agent records what it saw, and the server decides what it means -- which is
also the honest division, because this process knows a pid disappeared and
knows nothing whatsoever about why.

EVERYTHING HERE IS FAIL-OPEN. A watcher that cannot reach the API, cannot read
a registry entry or cannot import psutil records nothing and disturbs nobody.
It never signals, never kills and never touches a running process.
"""

from __future__ import annotations

import logging
import os
import time
import uuid
from pathlib import Path
from typing import Any

from probe.box import registry

logger = logging.getLogger(__name__)

#: How often the registry is swept. A process death is an edge, so the only
#: cost of a short interval is a `psutil` call per live run, and the only cost
#: of a long one is delay in noticing. Ten seconds puts detection two orders of
#: magnitude inside the reaper's fifteen minutes while staying invisible.
DEFAULT_INTERVAL_SECONDS = 10.0

#: Nothing registered for this long and the watcher exits rather than idling
#: forever on somebody's laptop. A later run spawns a new one.
IDLE_EXIT_SECONDS = 900.0


def _tunable(name: str, fallback: float, env=None) -> float:
    """A cadence an operator can change without a release.

    The watcher is a DETACHED process: nobody holds a handle to it and nothing
    passes it arguments, so a module constant is unreachable once it is
    running. Both knobs are therefore read from the environment at startup,
    the way the hardware rail reads `PROBE_HW_INTERVAL`. A malformed value
    falls back rather than refusing to start -- this component must never be
    the reason a box has no watcher.
    """
    env = os.environ if env is None else env
    raw = env.get(name)
    if raw is None:
        return fallback
    try:
        return float(raw)
    except (TypeError, ValueError):
        logger.warning("box: ignoring malformed %s=%r", name, raw)
        return fallback


#: The span this writes. Deliberately NOT `diagnostic`: that type carries a
#: scrubbed exception chain and `app/notifications/evidence.py` parses it as
#: one. A node observation is not a traceback and must not be read as one.
SPAN_TYPE = "node_event"

#: Span ids are minted by the CLIENT -- `SpanCreate.id` is required and has no
#: default, so a payload without one is refused with a 422. That refusal is
#: silent by design here (reporting is best-effort and swallows), which is the
#: worst possible combination: every death would be noticed and none reported.
#: An integration test against the real router is what found it; the client
#: fake accepted anything.
#:
#: DETERMINISTIC, like the trajectory connector's ids, so the write is
#: idempotent. One process death is one event, and a watcher that somehow
#: reports it twice -- a retry, an overlapping sweep -- must upsert the same
#: row rather than leave two identical observations on the run.
_SPAN_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "probe.box.node-agent")


def _span_id(run_id: str, pid: object, event: str) -> str:
    return str(uuid.uuid5(_SPAN_NAMESPACE, f"{run_id}:{pid}:{event}"))


def _client_for(entry: dict[str, Any]):
    """A client aimed at wherever this run reports. Built per entry, because a
    box can host runs from more than one context."""
    from probe.sdk.client import Client
    from probe.sdk.config import Settings

    settings = Settings.load(context=entry.get("context") or None)
    if entry.get("base_url"):
        settings.base_url = entry["base_url"]
    # async_writes=False: this is a short-lived observer, not a training loop.
    # It should deliver now and find out immediately if it cannot.
    return Client(settings=settings, async_writes=False)


def _iso(epoch: float) -> str:
    """A tz-aware ISO timestamp, which `SpanCreate` requires."""
    from datetime import datetime
    from probe._compat import UTC

    return datetime.fromtimestamp(epoch, tz=UTC).isoformat()


def report_vanished(entry: dict[str, Any], *, noticed_at: float | None = None) -> bool:
    """Record that this run's process is gone. Returns whether it landed."""
    noticed = time.time() if noticed_at is None else noticed_at
    try:
        client = _client_for(entry)
    except Exception as exc:  # noqa: BLE001 -- an unreachable context is not fatal
        logger.debug("box: no client for %s: %s", entry.get("run_id"), exc)
        return False
    try:
        client.write(
            "POST",
            f"/v1/runs/{entry['run_id']}/spans",
            {
                "spans": [
                    {
                        "id": _span_id(entry["run_id"], entry.get("pid"), "process_vanished"),
                        "span_type": SPAN_TYPE,
                        "name": "process_vanished",
                        # CLOSED, and instantaneous. An observation has no
                        # duration -- the process was there and then was not --
                        # so both ends are the moment it was noticed.
                        #
                        # Leaving `ended_at` unset was the first shape and was
                        # wrong twice over: the span would sit open forever in
                        # the UI, and `app/notifications/evidence.py` reads
                        # OPEN spans to decide which phase a run died in. Only
                        # the status saved it from rendering as "died inside
                        # node_event/process_vanished", which is one predicate
                        # away from being a lie in a crash email.
                        "started_at": _iso(noticed),
                        "ended_at": _iso(noticed),
                        # Not `failed`: nothing here failed. The observation
                        # succeeded; what it observed is in the attributes.
                        "status": "completed",
                        "attributes": {
                            "observer": "node-agent",
                            "event": "process_vanished",
                            # What was watched, so a reader can tell this from a
                            # guess. The host matters: on a multi-node job the
                            # box that lost the process is the one to look at.
                            "pid": entry.get("pid"),
                            "host": entry.get("host"),
                            "registered_at": entry.get("registered_at"),
                            "noticed_at": noticed,
                            # How long the process was alive as far as this
                            # watcher could see. Not the run's duration: the run
                            # may have been open before this process claimed it.
                            "observed_seconds": (
                                round(noticed - float(entry["registered_at"]), 1)
                                if entry.get("registered_at")
                                else None
                            ),
                        },
                    }
                ]
            },
            strict=False,
        )
        _report_writer_gone(client, entry)
        return True
    except Exception as exc:  # noqa: BLE001 -- capture never raises at a caller
        logger.debug("box: could not report %s: %s", entry.get("run_id"), exc)
        return False


def _report_writer_gone(client, entry: dict[str, Any]) -> None:
    """SDK reliability 2.2: the same death, as a status report. The span above
    explains it; this lets the server end a sole-writer run now instead of
    after the reaper's window. Only to a server that declares the route, and
    only when the entry names the writer (entries from older SDKs do not)."""
    writer = entry.get("writer") or {}
    if not writer.get("session_id") or writer.get("write_epoch") is None:
        return
    try:
        if not client.supports_feature("run_writer_gone"):
            return
        client.report_writer_gone(
            str(entry["run_id"]),
            {
                "session_id": str(writer["session_id"]),
                "write_epoch": int(writer["write_epoch"]),
                "observed_by": "node_agent",
                "host": entry.get("host"),
                "pid": entry.get("pid"),
                "sole_writer": bool(writer.get("sole_writer")),
            },
        )
    except Exception as exc:  # noqa: BLE001 -- the reaper still ends the run
        logger.debug("box: writer-gone for %s not sent: %s", entry.get("run_id"), exc)


def sweep(directory: Path | str | None = None) -> dict[str, int]:
    """One pass. Returns a small tally for the caller's logs and for tests."""
    alive = gone = reported = 0
    for entry in registry.entries(directory):
        if not registry.is_local(entry):
            # Another machine's (or container's) run, in a directory a shared
            # HOME makes common: its pid means nothing here. Not ours to judge,
            # count or remove.
            continue
        if registry.process_is_alive(entry):
            alive += 1
            continue
        gone += 1
        if report_vanished(entry):
            reported += 1
        # Removed either way. A run whose process is gone has nothing left to
        # watch, and an entry that could not be reported must not be retried
        # forever -- the server's reaper is still behind this as the backstop.
        registry.deregister(entry["run_id"], directory=directory)
    return {"alive": alive, "gone": gone, "reported": reported}


def watch_forever(
    *,
    interval: float | None = None,
    idle_exit_seconds: float | None = None,
    directory: Path | str | None = None,
    now=time.monotonic,
    sleep=time.sleep,
) -> dict[str, int]:
    """Sweep until nothing has been registered for `idle_exit_seconds`.

    Both cadences default to the environment rather than to a module constant
    bound at import: the watcher runs detached, so an operator who wants a
    different interval has no other way to ask for one. `now` and `sleep` are
    injectable so a test can drive this without spending the wall clock it
    describes.
    """
    every = (
        _tunable("PROBE_BOX_INTERVAL", DEFAULT_INTERVAL_SECONDS)
        if interval is None
        else float(interval)
    )
    if idle_exit_seconds is None:
        idle_exit_seconds = _tunable("PROBE_BOX_IDLE_EXIT", IDLE_EXIT_SECONDS)
    if every <= 0:
        return {"alive": 0, "gone": 0, "reported": 0, "sweeps": 0}
    totals = {"alive": 0, "gone": 0, "reported": 0, "sweeps": 0}
    last_seen = now()
    while True:
        tally = sweep(directory)
        totals["gone"] += tally["gone"]
        totals["reported"] += tally["reported"]
        totals["alive"] = tally["alive"]
        totals["sweeps"] += 1
        if tally["alive"] or tally["gone"]:
            last_seen = now()
        elif now() - last_seen >= idle_exit_seconds:
            return totals
        sleep(every)


def enabled(env=None) -> bool:
    """OPT-IN, matching the hardware rail. This one reads process tables and,
    in later phases, kernel logs; that is not something to switch on for
    somebody without asking."""
    env = os.environ if env is None else env
    return str(env.get("PROBE_BOX", "0")).strip().lower() in ("1", "true", "on")
