"""The service's watch: what fails here reaches the Probe team as one automatic report (plan B2, rev 5).

    the subsystems ──note(family, reason, sid, facts, env)──> a counter per family
                     (recorders, workers, hooks.run,           (and session), over a
                     the hook queue, background work,          15-min window: at its
                     the loop and threads, the updater,        threshold, an incident
                     the tap's load)
    the start      ──note(service_crash)────────────────────> the last service died
                     (`last_run`: service.run against         without a stop record on
                     last-stop.json and the boot id)          this boot, or crashed
    the loop, at once ──> each new incident takes a snapshot of the sessions whose
                     agent runs AT THAT MOMENT (`voters`: the registered ones,
                     including one switched to mode off -- a session that STARTS
                     off never registers, so it is not among them), the very
                     next turn of the loop after its note, whatever the report
                     slot is doing; with the environment it happened in (a
                     session's, a hook event's, an SDK caller's) they decide:
                     any one that says no drops it, now and for good
    every SCAN_S   ──> the update barrier (read here only, never where a note comes from)
                   ──> every SLOW_CHECK_S (the first scan too), the same on two runs:
                       one outbox queue holding writes nothing here will send
                       without a person (`outbox_stuck`), live sessions' transcripts
                       waiting CAPTURE_STALL_S past their last receipt (one
                       `capture_stalled` for the machine), either dropped while it
                       waits for a retry once a check no longer sees it; and,
                       beside the scan and with the consent its report would need,
                       each key the CLI config holds not answered within
                       CREDENTIAL_CHECK_S (`watch.json` keeps when), asked once
                       (`credential_refused`, once per key)
                   ──> for the sessions the service does not supervise: their daemon
                       lease released with `error`/`gateway`/`unauthorized` (not a
                       `gateway` marked offline), or
                       expired (`hung` / `not_running`); a hosted recorder whose
                       beat is STALL_S old (`stalled`); a `tap watch` session whose
                       heartbeat is GONE_S old (`gone`, once per registration): each the same on two scans
                       in a row, its agent still running, and never in the
                       WAKE_GRACE_S after the machine slept (wall time ran ahead of
                       monotonic time between two scans)
                   ──> a rejected release in guard.json, once per version
                   ──> the oldest incident waiting for the slot:
    one child      ──`probe.core.run report` (a READ, `children.run_read`), at
                     most one at a time, killed at REPORT_TIMEOUT_S, never an
                     action (an action takes the one slot and holds updates off);
                     what it answered goes to service.log and `service.status`
                     (`public`); a report is settled only by `sent`, `deduped`
                     or `disabled:*` (`deduped` not after a failed try: that is
                     its own claim), else (but for `unauthorized` and
                     `too_large`: the child kept its claim) tried again every
                     RETRY_S for RETRY_FOR_S, each try asking the sessions of
                     ITS moment too;
                     a once-ever one (a rejected version, a tap that would not
                     load, a failing update streak) is then never noted again

Consent is `probe.analytics.report_policy`'s rule: a session family asks that
session -- the environment its recorder or worker runs with, else what its
registrant said (`session.register`'s `report_env`, a bool the registrant
computed, taken as said), else no; a machine family asks every session whose
agent runs and the environment it happened in, and only an incident noted with
no session at all asks the login shell (its variables) and the CLI config. The
report child then checks only what it is handed: a session's own variables, or
for every other report `{}` and the CLI config's backend.

Never while discovering (the sessions are still coming back: an incident noted
then is decided once they are, by the sessions of its moment AND those back by
then -- one whose consent was not yet known at its moment is asked then), and
never while an update cycle runs, drains
the workers or holds its barrier: a hand-over is no failure, so what fails
meanwhile is not counted, and nothing is sent until it is over.

`last_run` and `record_crash` keep the service's own record (`service.run`,
`last-crash.json`); the keeper reads the sessions from disk with
`sessions_on_disk` and decides as a machine family does (`decide_machine`).

Stdlib only at import (the start path; plan S1): the consent rule and the
CLI config are read on a thread, when there is something to send.
"""

from __future__ import annotations

import asyncio
import collections
import contextlib
import threading
import time
from collections.abc import Callable, Mapping

from ...foundation.service_api import paths
from ...foundation.compose.compose import compose
from probe.service.watch.bounds import bounded_facts
from probe.service.watch.conditions.capture import _no_receipts
from probe.service.watch.conditions.credentials import CredentialCheckMixin, configured_key_ids, credential_verdicts
from probe.service.watch.conditions.guard import GuardCheckMixin
from probe.service.watch.conditions.outbox import OutboxReadMixin, outbox_condition
from probe.service.watch.consent import ConsentMixin, consent_env, login_env
from probe.service.watch.files import STATE_NAME, read_json, write_json
from probe.service.watch.incident import Family, Incident, SESSION_FAMILIES
from probe.service.watch.loop import LoopSideMixin
from probe.service.watch.reports import RECENT, ReportsMixin
from probe.service.watch.service_record import MAX_ONCE
from probe.service.watch.settings import (
    DEDUPE_S,
    KEEP_EVENTS,
    KEPT_WHILE_UPDATING,
    MAX_PENDING,
    REPORT_READ,
    REPORT_TIMEOUT_S,
    SCAN_ENV,
    SCAN_S,
    WINDOW_S,
    _env_float,
    reports_enabled,
)
#: Events in WINDOW_S that make an incident (absent: the first one does).
THRESHOLDS = {Family.SERVICE_ERROR: 3, Family.RECORDER: 3, Family.HOOK_HOST: 3, Family.HOOK: 3}


async def _run_report(params: dict) -> tuple[int | None, object]:
    from ..actions import children

    return await children.run_read(REPORT_READ, params, timeout=REPORT_TIMEOUT_S)


def _never() -> bool:
    return False


@compose
class Watch(
    ConsentMixin,
    LoopSideMixin,
    OutboxReadMixin,
    CredentialCheckMixin,
    GuardCheckMixin,
    ReportsMixin,
):
    """`note` from any thread (it reads nothing from disk); the rest on the service's loop."""

    def __init__(
        self,
        *,
        log: Callable[[str], None],
        loop_getter: Callable[[], asyncio.AbstractEventLoop | None],
        voters: Callable[[], list],
        updating: Callable[[], bool] = _never,
        barrier_up: Callable[[], bool] = _never,
        discovering: Callable[[], bool] = _never,
        sessions: Callable[[], list] = list,
        hosted_env: Callable[[str], dict | None] = lambda sid: None,
        supervised: Callable[[str], bool] = lambda sid: False,
        recorders: Callable[[], list] = list,
        receipts: Callable[[], object] = _no_receipts,
        outbox: Callable[[float], tuple | None] = outbox_condition,
        credentials: Callable[..., dict] = credential_verdicts,
        run_report: Callable[[dict], object] = _run_report,
        login: Callable[[], object] = login_env,
        clock: Callable[[], float] = time.time,
        monotonic: Callable[[], float] = time.monotonic,
        scan_s: float | None = None,
    ) -> None:
        self.log = log
        self._loop_getter = loop_getter
        #: An update cycle runs or applies (`Service._updating`): cheap, from any thread.
        self.updating = updating
        #: The update barrier or the workers' hold is up: reads files (and may
        #: run `ps` on macOS), so only the scan asks, on a thread.
        self.barrier_up = barrier_up
        self.discovering = discovering
        #: The live registered sessions (`registry.Session`s).
        self.sessions = sessions
        #: Every registered session whose agent runs (one switched to mode off
        #: included), as `Live`s: whose consent a report needs. Required: a
        #: default of "none" would let every machine report out.
        self.voters = voters
        #: A hosted session's environment (its recorder's), or None.
        self.hosted_env = hosted_env
        #: Is the session's daemon worker supervised here (`workers.WorkerHost`)?
        self.supervised = supervised
        #: Each hosted recorder inside `hosted.record`: `{sid, beat_age_s, owner}`.
        self.recorders = recorders
        #: The delivery receipts of the sessions whose agent runs, `{sid:
        #: receipts or None}` (`receipts.ReceiptCache`), awaited on the loop.
        self.receipts = receipts
        #: The outbox's stuck condition (`outbox_condition`), on a thread.
        self.outbox = outbox
        #: Each key's verdict (`credential_verdicts`), on a thread.
        self.credentials = credentials
        self.run_report = run_report
        self.login = login
        self.clock = clock
        self.monotonic = monotonic
        self.scan_s = scan_s if scan_s is not None else _env_float(SCAN_ENV, SCAN_S)
        self.enabled = reports_enabled()
        self._lock = threading.Lock()
        #: (family, sid) -> deque of (monotonic, facts, consent env or None): the events in the window.
        self._seen: dict = {}
        #: Incidents noted and not yet looked at by the loop (consent fixed there).
        self._fresh: list = []
        #: (family, sid) -> Incident, looked at, waiting for the slot (oldest first).
        self._pending: dict = {}
        #: (family, sid) -> when (wall) a report child last ran for it, or it was declined.
        self._settled: dict = {}
        #: Keys of `watch.json` (`once`), oldest first, read on first use.
        self._once: set | None = None
        self._once_order: list = []
        #: (family, sid) -> the condition seen at the last scan (two in a row make an incident).
        self._cond_last: dict = {}
        #: What the last scan read of the barrier (`barrier_up`).
        self._barrier = False
        #: The last scan's (wall, monotonic), and when (monotonic) a sleep was seen.
        self._tick: tuple | None = None
        self._woke_at: float | None = None
        self._last_scan: float | None = None
        self._recent: collections.deque = collections.deque(maxlen=RECENT)
        self._child: asyncio.Future | None = None
        self._sending = False
        self._timer: asyncio.TimerHandle | None = None
        self._tasks: set = set()
        self._login_cache: tuple[float, dict | None] | None = None
        #: When (monotonic) the slower checks last ran; None: on the next scan.
        self._slow_at: float | None = None
        #: The slower checks' conditions seen at their last run (two in a row make one).
        self._slow_last: dict = {}
        #: Each key's id (`_credential_id`) -> when (wall) it was last answered
        #: (`watch.json`), read on first use.
        self._credentials_at: dict = {}
        #: Each key kind's last answer (`ok`/`refused`/`unknown`), for `key_answers`.
        self._key_answers: dict = {}
        #: The credential check running in the background, if one is.
        self._credential_task: asyncio.Future | None = None
        #: Each key's id -> when (wall) it was last asked and not answered.
        self._credentials_tried: dict = {}
        #: The outbox read, while one is still on its thread.
        self._outbox_busy = False
        #: The key check's thread, while one is still running (it may outlive
        #: its deadline: a server trickling its answer), and when (wall) the
        #: next may start after one was given up on.
        self._credentials_busy = False
        self._credentials_after = 0.0
        #: Serializes `watch.json`'s writes (snapshot to file), from any thread.
        self._state_write = threading.Lock()
        #: sid -> (receipt cursor, since when seen waiting there, last seen offline)
        #: (`capture_conditions`); kept through a receipt read that failed.
        self._capture_still: dict = {}
        self._closed = False
        self.reports = 0

    # -- noting ----------------------------------------------------------------

    def note(
        self,
        family: str,
        reason: str,
        sid: str | None = None,
        facts: Mapping | None = None,
        *,
        env: Mapping | None = None,
        once: str | None = None,
        threshold: int | None = None,
    ) -> None:
        """One event of `family` (`reason`, a slug) from anywhere: at the
        family's threshold within WINDOW_S (or `threshold`) an incident, whose
        consent the loop fixes at once. `env`: the environment it happened in
        (a session's, a hook event's, an SDK caller's): its opt-out counts.
        `once`: report this key once ever. Reads no file. Never raises."""
        try:
            self._note(family, reason, sid, facts, env, once, threshold)
        except Exception as exc:  # noqa: BLE001 -- the watch never costs its caller anything
            with contextlib.suppress(Exception):
                self.log(f"watch: noting {family} failed: {exc!r}")

    def _note(self, family, reason, sid, facts, env, once, threshold) -> None:
        if self._closed or not self.enabled:
            return
        if family not in KEPT_WHILE_UPDATING and self._quiet():
            return  # an update's hand-over: what fails meanwhile is its doing
        key = (family, sid if family in SESSION_FAMILIES else None)
        # A condition two scans confirmed (`threshold`: `stalled`, `gone`, a
        # lease) is counted on its own: never with the family's other events.
        counter = key if threshold is None else (*key, reason)
        threshold = threshold if threshold is not None else THRESHOLDS.get(family, 1)
        now = self.monotonic()
        with self._lock:
            if once is not None and once in self._load_state():
                return
            seen = self._seen.setdefault(counter, collections.deque())
            seen.append((now, bounded_facts(facts), consent_env(env) if env is not None else None))
            while seen and now - seen[0][0] > WINDOW_S:
                seen.popleft()
            if len(seen) < threshold:
                return
            events = list(seen)
            seen.clear()
            settled = self._settled.get(key)
            if settled is not None and 0 <= self.clock() - settled < DEDUPE_S:
                return
            if len(events) > 1:
                detail = {"count": len(events), "window_s": WINDOW_S, "events": [f for _, f, _ in events[-KEEP_EVENTS:]]}
            else:
                detail = events[-1][1]
            envs = [e for _, _, e in events if e is not None]
            self._fresh.append(Incident(family, reason, key[1], detail, envs, once, self.clock()))
            del self._fresh[:-MAX_PENDING]
        self._kick()

    def _quiet(self) -> bool:
        """An update's hand-over is under way: the cycle (asked now, cheap) or
        the barrier (as the last scan read it)."""
        if self._barrier:
            return True
        try:
            return bool(self.updating())
        except Exception:  # noqa: BLE001 -- unknown: not quiet
            return False

    def _load_state(self) -> set:
        """`watch.json`, read once (under the lock): the once-ever keys, which
        it returns, and when each key was last answered (`_credentials_at`)."""
        if self._once is None:
            data = read_json(paths.service_dir() / STATE_NAME)
            keys = data.get("once") if isinstance(data, dict) else None
            self._once_order = [k for k in keys if isinstance(k, str)] if isinstance(keys, list) else []
            self._once = set(self._once_order)
            asked = data.get("credentials_at") if isinstance(data, dict) else None
            self._credentials_at = {
                k: float(v) for k, v in asked.items() if isinstance(k, str) and isinstance(v, (int, float))
            } if isinstance(asked, dict) else {}
            answers = data.get("key_answers") if isinstance(data, dict) else None
            self._key_answers = {
                k: v for k, v in answers.items() if isinstance(k, str) and v in ("ok", "refused", "unknown")
            } if isinstance(answers, dict) else {}
        return self._once

    def _write_state(self) -> None:
        """`watch.json`: the once-ever keys and when each key was last answered.
        Snapshot and write under one lock of their own: two writers (a
        once-ever mark, a credential check) on two threads never land an older
        snapshot last."""
        with self._state_write:
            with self._lock:
                self._load_state()
                state = {"v": 1, "once": list(self._once_order)}
                if self._credentials_at:
                    state["credentials_at"] = dict(self._credentials_at)
                if self._key_answers:
                    # Only keys answered lately: a key replaced or gone drops out with its time.
                    live = set(self._credentials_at) | set(self._credentials_tried)
                    state["key_answers"] = {k: v for k, v in self._key_answers.items() if k in live}
            write_json(paths.service_dir() / STATE_NAME, state)

    def _mark_once(self, key: str) -> None:
        with self._lock:
            keys = self._load_state()
            if key in keys:
                return
            self._once_order = (self._once_order + [key])[-MAX_ONCE:]
            self._once = set(self._once_order)
        self._write_state()

    def last_login_env(self) -> dict | None:
        """The login shell's consent variables as last read (None: never read,
        or unreadable). Never reads them: it may run at exit."""
        cached = self._login_cache
        return cached[1] if cached is not None else None

    def key_answers(self) -> dict:
        """Each key kind the CLI config holds NOW -> the API's last answer to
        that very key (`ok`, `refused`, `unknown`), None when it has not been
        asked; a key the config no longer holds is not listed. Blocking (the
        config): a thread."""
        with self._lock:
            self._load_state()
            answers = dict(self._key_answers)
        return {kind: answers.get(ident) for kind, ident in configured_key_ids().items()}

    def public(self) -> dict:
        """`service.status`'s `watch`: what `probe doctor` and the debug log show."""
        with self._lock:
            waiting = len(self._fresh) + len(self._pending)
        return {"enabled": self.enabled, "last_scan": self._last_scan, "waiting": waiting,
                "reports": list(self._recent)}

    def close(self) -> None:
        self._closed = True
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
