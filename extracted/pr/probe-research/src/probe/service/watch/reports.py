"""send the oldest due incident as one report child at a time, and read what it answered."""

from __future__ import annotations

import asyncio
from probe.service.watch.conditions.credentials import _UUID
from probe.service.watch.consent import config_base_url
from probe.service.watch.incident import Incident, SESSION_FAMILIES
from probe.service.watch.keeper import KEPT_CLAIM, outcome, taken
from probe.service.watch.settings import RATE_LIMITED_RETRY_S, RETRY_FOR_S, RETRY_S
#: The last reports `public` names.
RECENT = 5


class ReportsMixin:
    """Part of Watch: its methods run with `self` the Watch; compose() folds them into Watch."""

    async def _send_next(self) -> None:
        """The oldest incident due, as one report child (one at a time); one
        whose consent says no is dropped."""
        if self._closed or self._sending or self._child is not None:
            return
        # Taken before the first await: a scan and a note's kick may both ask.
        self._sending = True
        try:
            self._triage()
            if self.discovering() or self._quiet():
                return
            now = self.clock()
            with self._lock:
                waiting = [i for i in self._pending.values() if i.not_before <= now]
            if not waiting:
                return
            base_url = await asyncio.to_thread(config_base_url)
            for incident in waiting:
                if incident.verdict is None:
                    incident.verdict = await self._consent(incident, base_url)
                allowed, why, env = incident.verdict
                if not allowed:
                    self._drop(incident, why)
                    continue
                self._start_child(incident, env)
                return
        finally:
            self._sending = False

    def _drop(self, incident: Incident, why: str) -> None:
        with self._lock:
            # A newer event of the same key noted meanwhile goes with it: settled.
            self._pending.pop(incident.key, None)
            self._settled[incident.key] = self.clock()
        sid = f" (session {incident.sid})" if incident.sid else ""
        self.log(f"watch: {incident.family} ({incident.reason}){sid} not reported: {why}")

    def _start_child(self, incident: Incident, env: dict) -> None:
        with self._lock:
            self._pending.pop(incident.key, None)
            self._settled[incident.key] = self.clock()
        sid, facts = incident.sid, incident.facts
        if sid is not None and not _UUID.match(sid):
            # The `report` read would refuse the whole report over it.
            sid, facts = None, {**facts, "session": incident.sid}
        params = {"auto": True, "family": incident.family, "reason": incident.reason, "sid": sid,
                  "env": dict(env), "facts": facts}
        self._child = asyncio.ensure_future(self._report(incident, params))

    async def _report(self, incident: Incident, params: dict) -> None:
        sid = f" (session {incident.sid})" if incident.sid else ""
        tried = self.clock()
        try:
            value = None
            try:
                code, value = await self.run_report(params)
            except OSError as exc:
                said = f"could not start: {exc}"
            else:
                said = outcome(code, value)
            self.reports += 1
            self._recent.append({"family": incident.family, "reason": incident.reason, "sid": incident.sid,
                                 "answer": said, "at": tried})
            settled = taken(value)
            if settled and incident.first_try is not None and isinstance(value, dict) \
                    and value.get("skipped") == "deduped":
                settled = False  # the failed try's own claim of the window, not a report
            # Refused for its credentials, or too large: the child kept its claim
            # of the window (`report.RELEASED_ON`), so a retry would only answer
            # `deduped`. Not retried and not settled once-ever: the next window tries.
            kept = isinstance(value, dict) and value.get("skipped") in KEPT_CLAIM
            if not settled and not kept:
                # Tried again later, once-ever or not: a failed send (offline,
                # the server, killed) is no report, and settling it would hold
                # a recurring family back for DEDUPE_S with nothing sent.
                first = incident.first_try if incident.first_try is not None else tried
                if self.clock() - first < RETRY_FOR_S:
                    # Its consent is asked again then, of that moment's sessions too.
                    wait = RATE_LIMITED_RETRY_S if isinstance(value, dict) and value.get("skipped") == "rate_limited" \
                        else RETRY_S
                    incident.first_try, incident.not_before, incident.verdict = first, self.clock() + wait, None
                    with self._lock:
                        self._pending.setdefault(incident.key, incident)
                    said += f"; again in {wait / 60:.0f} min"
            self.log(f"watch: report {incident.family} ({incident.reason}){sid}: {said}")
            # A session family's `deduped` is the child's (family, session)
            # window, which another registration's report may hold: not this one's.
            deduped = isinstance(value, dict) and value.get("skipped") == "deduped"
            if incident.once is not None and settled and not (deduped and incident.family in SESSION_FAMILIES):
                await asyncio.to_thread(self._mark_once, incident.once)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001
            self.log(f"watch: report {incident.family}{sid} failed: {exc!r}")
        finally:
            self._child = None
            if not self._closed:
                self._spawn(self._send_next())
