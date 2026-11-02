"""the update child: stop one (ours or a previous service's) that ran past its time limit, and record it."""

from __future__ import annotations

import asyncio
import contextlib
import os
import time
from dataclasses import dataclass, replace

from .quiet import barrier
from ..actions import children
from ...foundation.service_api.vocabularies import (
    StepState,
    UpdateStep)
from probe.service.updater.quiet.workers import _args
from probe.service.updater.settings import log


# -- an update child past UPDATE_TIMEOUT_S -----------------------------------------


def span(seconds: float) -> str:
    """`30 min`, `90 s`: a time limit as a person reads it."""
    return f"{seconds / 60:.0f} min" if seconds >= 120 else f"{seconds:g} s"


#: `record_stopped`, off the loop, waited for this long at most.
RECORD_WAIT_S = 10.0


def record_stopped(detail: str, *, version: str, since: float) -> bool:
    """A stopped update child, in the record `probe doctor` prints
    (`last_attempt`): failed, `detail` its reason. What the child recorded
    itself since `since` (its start) is kept, failed with this detail: the
    agents it finished, or its own account of the stop. Read and written under
    one hold of the record's lock, never waited for (`amend_attempt`): a child
    that would not stop may hold it. Whether it was written. Blocking (file
    I/O): off the loop. Never raises."""
    try:
        from probe.shared.updates import autoupdate

        now = int(time.time())

        def failed(prior):
            if prior is not None and prior.at >= int(since):
                return replace(prior, at=now, ok=False, detail=detail)
            return autoupdate.Attempt(at=now, ok=False, detail=detail, from_version=version)

        return autoupdate.amend_attempt(failed, wait=False)
    except Exception:  # noqa: BLE001 -- a diagnostic
        return False


async def record_stopped_off_loop(detail: str, *, version: str, since: float) -> None:
    """`record_stopped` in a thread, waited for RECORD_WAIT_S at most."""
    try:
        written = await asyncio.wait_for(
            asyncio.to_thread(record_stopped, detail, version=version, since=since), RECORD_WAIT_S
        )
    except asyncio.TimeoutError:
        written = False
    if not written:
        log("could not write the stopped update into autoupdate.json (its lock is held)")


@dataclass(frozen=True)
class Overrun:
    """An update child a service before this one started, still running past
    the limit: the process (pid, kernel start time) the barrier names."""

    pid: int
    start: str
    #: When it started (the barrier's `created_at`, written as it started).
    since: float


def _is_update_child(pid: int) -> bool:
    """Is `pid`'s command line `<python> -I -m probe.core.run update`?"""
    words = _args(pid)
    if not words:
        return False
    words = [w for w in words if w]
    return any(
        words[i] == "-m" and words[i + 1 : i + 3] == [children.CORE_MODULE, "update"] and i + 3 == len(words)
        for i in range(len(words) - 2)
    )


def overrun_update(limit_s: float, now: float | None = None) -> Overrun | None:
    """The update child a service before this one started and left running
    (`Updater._apply`: the barrier names the child once it runs, and stays up
    while it does), when it is still running `limit_s` after its start. Only
    that child, proven three ways: the barrier names it, (pid, kernel start
    time) is still that exact process (a reused pid has another start time:
    `procid.alive`), and its command line is `probe.core.run update`. A person's
    `probe wizard`, the app's Update action (an action, which raises no barrier)
    or anything else holding `wizard.lock` is never named here. Unknown (the
    start time cannot be read) is no. Blocking (`ps` off Linux): off the loop."""
    data = barrier.read()
    if data is None:
        return None
    try:
        pid = int(data.get("pid", 0))
        start = str(data.get("start_time") or "")
        since = float(data.get("created_at"))
    except (TypeError, ValueError):
        return None
    now = time.time() if now is None else now
    if pid <= 1 or pid == os.getpid() or not start or not now - since >= limit_s:
        return None  # not past the limit (a clock set back reads as not past)
    from ...foundation.service_api import procid

    if procid.alive(pid, start) is not True or not _is_update_child(pid):
        return None
    return Overrun(pid, start, since)


#: How `stop_process` (and the stop of this service's own child) ended.
Stopped = children.Stopped


async def stop_process(pid: int, start: str, grace: float) -> str:
    """Stop the process (pid, start) as `children.run_events` stops its own
    child at the limit (`children.stop`): SIGTERM, then SIGKILL past `grace`,
    to the process group it leads (an update child of this version: what is
    left of the group once it is gone too, while the group is provably still
    its own) or else to it alone (one an older service started in that
    service's group, which other processes share). The process is signalled
    only while (pid, start) is still that process, read off the loop each
    time. How it ended (`Stopped`). Never raises; cancelled, it sends nothing
    more."""
    from ...foundation.service_api import procid

    async def leader() -> bool:
        return await asyncio.to_thread(procid.alive, pid, start) is True

    group = None
    if os.name != "nt":
        with contextlib.suppress(OSError):
            if await leader() and os.getpgid(pid) == pid:
                group = pid

    def send(sig: int) -> None:
        os.kill(pid, sig)  # it alone: a group it leads is signalled by `children.stop`

    return await children.stop(leader=leader, send=send, group=group, grace=grace)


class ChildMixin:
    """Part of Updater: its methods run with `self` the Updater; compose() folds them into Updater."""

    async def _stop_previous(self, cycle_id: str) -> dict | None:
        """Before the quiet check: the update child a service before this one
        left running, past `update_timeout_s` (`overrun_update`), is stopped
        as this service stops its own at the limit (its `wizard.lock` would
        otherwise defer every cycle for a day, and a second update would then
        run beside it).
        What was done, for the step's record, or None (no such child)."""
        found = await asyncio.to_thread(overrun_update, self.update_timeout_s)
        if found is None:
            return None
        past = f"the update a service before this one started ran past {span(self.update_timeout_s)}"
        log(f"{past} (pid {found.pid}, {(time.time() - found.since) / 60:.0f} min old): stopping it")
        self._step(cycle_id, UpdateStep.CLI_AND_PLUGINS, StepState.STARTED, stopping_previous=found.pid)
        how = await stop_process(found.pid, found.start, self.update_stop_grace_s)
        if how == Stopped.GONE:
            log(f"the previous update child {found.pid} exited by itself meanwhile")
            return None
        detail = f"{past} and would not stop" if how == Stopped.RUNNING else f"{past} and was stopped"
        log(f"{detail} ({how})")
        await record_stopped_off_loop(detail, version=self.version, since=found.since)
        return {"detail": detail, "pid": found.pid, "started_at": found.since, "stopped_by": how}

    async def _overran(
        self, cycle_id: str, overran: children.Overran, done: dict, started_at: float, *, forced: str | None
    ) -> dict:
        """The update child ran past `update_timeout_s` and was stopped: the
        step failed, saying so where people look -- this step (`update.status`,
        `probe doctor`'s Updates row) and the attempt `probe doctor` prints
        (`record_stopped`). The child's own report to the server says it was
        stopped (`probe.shared.updates.update_report.merged_run`)."""
        limit = span(self.update_timeout_s)
        code = overran.code
        how = overran.how
        detail = f"the update ran past {limit} and " + ("would not stop" if how == Stopped.RUNNING else "was stopped")
        log(f"{detail} ({how})")
        await record_stopped_off_loop(detail, version=self.version, since=started_at)
        outcome: dict = {
            "detail": detail,
            "stopped_by": how,
            "exit_code": None if code is None else 128 - code if code < 0 else code,
            "ok": done.get("ok"),
            "complete": done.get("complete"),
        }
        if forced:
            outcome["forced"] = forced
        self._step(cycle_id, UpdateStep.CLI_AND_PLUGINS, StepState.FAILED, **outcome)
        return {"state": StepState.FAILED, **outcome}
