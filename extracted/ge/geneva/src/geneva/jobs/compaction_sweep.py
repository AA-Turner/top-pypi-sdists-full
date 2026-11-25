# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Resume compaction that dead drivers left paused on other tables (GEN-1005).

A Geneva job pauses the Enterprise agent's automatic compaction of its table
while it runs, and the last job on the table to end turns it back on (see
:mod:`geneva.jobs.compaction_pause`). So does the submitter when Ray reports a
driver lost. When a driver and its submitter die together, for example when the
container running both is stopped, nobody turns it back on. Compaction of that
table then stays off until another Geneva job on it ends.

So running drivers also sweep. Once per sweep interval, across the whole
database, one of them checks a bounded set of tables from job history, and resumes
compaction that no running job holds any more. Later intervals continue where
the previous driver stopped.

Why a sweep can never resume a table under a live job
-----------------------------------------------------

The sweep resumes a table with
:func:`~geneva.jobs.compaction_pause.resume_if_idle`, the same function a job
calls when it ends. That function is safe to call at any time, from any
process, as often as you like, because it does three things in order:

1. **Checks for holders.** It lists the table's unfinished jobs and keeps the
   pause if any of them has a live driver by its heartbeat: one that hasn't
   exited and hasn't been silent past the hold window (30 min by default).
2. **Resumes in one compare-and-swap.** It reads the table's overrides,
   refuses while Geneva's tag holds a fresh renewal from any job, and
   otherwise undoes the pause in one commit made from the version it read.
   Renewals are what a live driver writes when its heartbeat isn't landing,
   so a driver that is alive but can't heartbeat is never taken for dead.
   Lance rejects the commit if anyone changed the overrides after that read,
   a driver renewing for example, and it then reads and decides again.
3. **Checks again.** After resuming, it looks for holders once more and pauses
   again for a job that started meanwhile.

It only ever undoes Geneva's own pause: the ``paused_by_geneva`` tag inside
``job_types.compaction``. Compaction that an operator turned off carries no
tag and is never touched. An operator who set ``previous_enabled: false`` in
the tag gets compaction left off when the tag is removed (see
:class:`~geneva.jobs.compaction_pause.CompactionPauseConfig`).

The sweep adds no new way to resume; it only decides which tables to call that
function on, and when. Two sweeps running at once, or a sweep racing a job's
own resume, are just two calls on the same table, and each call is its own
compare-and-swap. A driver whose hold might have lapsed also stops before its
next commit that replaces fragments (see
:func:`~geneva.jobs.compaction_pause.check_compaction_hold`), so a driver
taken for dead doesn't go on to commit over fragments that a compaction may
have rewritten. The exception is a driver suspended between that check and
its commit, a risk the pause already carries.

One sweep per interval, by one driver
-------------------------------------

Every running driver could sweep, but one sweep per interval is enough. The
drivers take turns through a lease kept in the jobs table's own Lance config,
under :data:`SWEEP_LEASE_KEY`::

    {"holder": <job id>, "claimed_at": <iso time>, "expires_at": <iso time>}

1. **Read.** Every few minutes, each driver reads the lease. While it hasn't
   expired, another driver has claimed this interval's sweep, and there is
   nothing to do.
2. **Claim.** Once the lease has expired, or if it isn't there yet, the driver
   claims it with an ``update_config`` commit. It makes that commit from the
   same dataset version it read the lease from.
3. **Exactly one claim lands.** Lance rejects a config commit when a commit
   it hasn't seen changed the same key ("Incompatible transaction"). When
   several drivers find the lease expired at once, the first claim lands and
   every other one is rejected. This is the compare-and-swap the pause
   itself relies on.
4. **The claim is the schedule.** A claim lasts one interval, and it isn't
   released after the sweep. The next sweep happens on the first claim after
   it expires, so the database is swept about once per interval, however many
   drivers run.

The lease saves work, and correctness never depends on it. A sweep that
outlasts its claim, or a driver whose clock runs ahead, can overlap another
sweep. That only means two calls to ``resume_if_idle`` on the same table,
which is safe (above). A driver that dies mid-sweep leaves the rest of the
tables for the next claim, one interval later.

Claims don't disturb the jobs table's rows: a config commit and a row append,
update or delete don't conflict, in either order. That was checked with the
row writes made through lancedb, as Geneva makes them.

Which tables
------------

The sweep checks every table that has a row in ``geneva_jobs``, in any status.
Geneva only pauses a table it ran a job on, and a pause can outlive the job's
unfinished row. For example, an operator may have cancelled a dead job's row,
or a job's own resume may have failed after it finished. Reading a table's
overrides is enough to skip it when it has no Geneva tag, so most of a sweep
is reads.

Each interval checks at most 128 distinct tables and consumes at most 1,048,576
sorted history rows. Progress stores only the snapshot version and last table
name in the jobs config, separately per namespace. Later intervals filter out
names already checked, so interleaved job rows cannot spend the table budget on
the same names again. New history rows are picked up on the next full pass. If
retention removes the snapshot, discovery restarts against the latest version.

Sorting can read the entire projected table-name column; the returned-row limit
does not cap storage I/O. The cooperative 30-second check budget starts after
the first sorted batch arrives, so slow discovery cannot prevent all progress.
An in-flight call and a resume's safety re-check finish before yielding.

Per-table queries still account for every unfinished job id; their heartbeat
reads stop at the first live holder. The budget never truncates a safety decision.

Rows store only the table name, so a driver opens that name in its own
namespace; a same-named table in another namespace is swept by drivers
running there. A driver skips its own table, which it holds anyway.
"""

from __future__ import annotations

import functools
import json
import logging
import random
import threading
import time
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

import attrs

from geneva.jobs.compaction_pause import (
    DEFAULT_STALE_LEASES,
    CompactionCheckInterruptedError,
    is_paused_by_geneva,
    report_job_event,
    resume_if_idle,
)
from geneva.utils import dt_now_utc, escape_sql_string

if TYPE_CHECKING:
    from collections.abc import Callable

    from lance import LanceDataset

_LOG = logging.getLogger(__name__)

# The jobs table config key holding the sweep lease.
SWEEP_LEASE_KEY = "geneva.compaction_sweeper"
SWEEP_PROGRESS_KEY = "geneva.compaction_sweeper.progress."
# Cooperative limits: an in-flight storage call and a resume's safety re-check
# finish before yielding. At most two config commits are made per interval.
_SWEEP_BUDGET_S = 30.0
_MAX_TABLES = 128
_MAX_HISTORY_ROWS = 1_048_576
# The longest a driver goes between reads of the lease. Each read opens the
# jobs table's latest version, and that table is busy, so drivers don't read
# it constantly. Reading every few minutes is still enough for a sweep to
# follow an expired lease soon.
_CHECK_EVERY_S = 300.0
# Each wait between reads is randomized by up to this fraction either way, so
# drivers launched together don't all read the lease, and all try to claim it,
# at the same moment. This only spreads the load: the claim's compare-and-swap,
# not timing, decides who sweeps.
_CHECK_JITTER = 0.5
_STOP_TIMEOUT_S = 30.0


@attrs.define(frozen=True)
class SweepLease:
    """Which driver claimed the database's current sweep interval, and until
    when."""

    holder: str
    claimed_at: datetime
    expires_at: datetime

    def to_json(self) -> str:
        return json.dumps(
            {
                "holder": self.holder,
                "claimed_at": self.claimed_at.isoformat(),
                "expires_at": self.expires_at.isoformat(),
            },
            separators=(",", ":"),
        )

    @classmethod
    def parse(cls, raw: str | None) -> SweepLease | None:
        """The lease in ``raw``, or None when there is none. A lease that can't
        be read is treated as expired, so a bad value can't stop sweeps for
        good: the next claim replaces it."""
        if raw is None:
            return None
        try:
            value = json.loads(raw)
            lease = cls(
                holder=str(value["holder"]),
                claimed_at=datetime.fromisoformat(value["claimed_at"]),
                expires_at=datetime.fromisoformat(value["expires_at"]),
            )
            # A time without a zone can't be compared with now, and would
            # fail every claim instead of being replaced.
            if lease.claimed_at.tzinfo is None or lease.expires_at.tzinfo is None:
                raise ValueError("lease times have no time zone")
            return lease
        except (KeyError, TypeError, ValueError):
            _LOG.warning("Ignoring malformed compaction sweep lease %r", raw)
            return None


def claim_sweep(
    open_jobs_dataset: Callable[[], Any],
    *,
    holder: str,
    interval_s: float,
    now: datetime | None = None,
) -> SweepLease | None:
    """Claim the database's next sweep for ``holder``; the lease if it won.

    Returns None while another driver's claim still covers this interval, or
    when another driver's claim landed first. Both mean someone else sweeps.
    """
    now = now or dt_now_utc()
    # One dataset, at one version, for both the read and the claim. The claim
    # is then a compare-and-swap against what was read: Lance rejects it if
    # any commit after this version touched the lease.
    ds = open_jobs_dataset()
    current = SweepLease.parse(ds.config().get(SWEEP_LEASE_KEY))
    if current is not None and now < current.expires_at:
        return None
    lease = SweepLease(holder, now, now + timedelta(seconds=interval_s))
    try:
        ds.update_config({SWEEP_LEASE_KEY: lease.to_json()})
    except OSError:
        # Most often "Incompatible transaction": another driver's claim landed
        # after this version was read, and it sweeps this interval. Any other
        # failure to write also leaves the sweep to whoever claims next.
        _LOG.debug("Job %s did not claim the compaction sweep", holder, exc_info=True)
        return None
    return lease


@attrs.define
class SweepProgress:
    """Last checked name in an immutable history snapshot, shared by drivers."""

    version: int | None = None
    last_name: str = ""

    def to_json(self) -> str:
        return json.dumps(attrs.asdict(self), separators=(",", ":"))

    @classmethod
    def parse(cls, raw: str | None) -> SweepProgress:
        """Restart discovery for missing, malformed, or legacy row cursors."""
        try:
            value = json.loads(raw or "null")
            version, last_name = value["version"], value["last_name"]
            if (
                (version is not None and (type(version) is not int or version < 1))
                or not isinstance(last_name, str)
                or (version is None and last_name != "")
            ):
                raise ValueError("invalid sweep progress")
            return cls(version, last_name)
        except (KeyError, TypeError, ValueError):
            return cls()


def sweep_paused_tables(
    *,
    jobs_dataset: LanceDataset,
    history: Any,
    open_table: Callable[[str], Any],
    skip_table: str | None = None,
    stale_leases: float = DEFAULT_STALE_LEASES,
    stopped: Callable[[], bool] = lambda: False,
    progress: SweepProgress | None = None,
) -> list[str]:
    """Check the next names in sorted history; return the tables resumed.

    ``open_table`` opens a table, by name, at its latest version, as a Lance
    dataset. A table that can't be checked is skipped for this interval.
    Read from ``jobs_dataset`` or the saved snapshot. Update ``progress`` so
    another driver can continue that snapshot even when job updates reorder rows.
    """
    deadline: float | None = None

    def interrupted() -> bool:
        return stopped() or (deadline is not None and time.monotonic() >= deadline)

    progress = progress if progress is not None else SweepProgress()
    if interrupted():
        return []
    ds = jobs_dataset
    if progress.version is not None:
        try:
            ds = ds.checkout_version(progress.version)
        except OSError as exc:
            if "not found" not in str(exc).lower():
                raise
            # A newer snapshot may contain names before the saved cursor.
            _LOG.info("Compaction sweep snapshot expired; restarting discovery")
            progress.last_name = ""
    progress.version = ds.version
    # Sorting groups duplicates; the next interval skips every row of checked names.
    scanner = ds.scanner(
        columns=["table_name"],
        filter=f"table_name > '{escape_sql_string(progress.last_name)}'",
        order_by=["table_name"],
        limit=_MAX_HISTORY_ROWS,
        batch_size=8192,
        batch_readahead=2,
        fragment_readahead=2,
    )
    resumed = []
    checked = 0
    rows = 0
    with scanner.to_reader() as reader:
        while not interrupted():
            batch = next(reader, None)
            if batch is None:
                if rows < _MAX_HISTORY_ROWS:
                    progress.version, progress.last_name = None, ""
                break
            if deadline is None:
                deadline = time.monotonic() + _SWEEP_BUDGET_S
            for name in batch.column("table_name").to_pylist():
                if interrupted():
                    return resumed
                rows += 1
                if not name:
                    continue
                if name != skip_table and name != progress.last_name:
                    if checked >= _MAX_TABLES:
                        return resumed
                    checked += 1
                    open_dataset = functools.partial(open_table, name)
                    try:
                        if is_paused_by_geneva(open_dataset()) and resume_if_idle(
                            table_name=name,
                            open_dataset=open_dataset,
                            history=history,
                            stale_leases=stale_leases,
                            stopped=interrupted,
                        ):
                            resumed.append(name)
                    except CompactionCheckInterruptedError:
                        # Leave it paused; later discovery can revisit it.
                        pass
                    except Exception as exc:  # noqa: BLE001
                        _LOG.info(
                            "Compaction sweep skipped table %s: %s: %s",
                            name,
                            type(exc).__name__,
                            exc,
                        )
                progress.last_name = name
    return resumed


class CompactionSweeper:
    """Runs in a job's driver while the job runs, and sweeps the database when
    this driver wins the interval's claim (see the module docstring)."""

    def __init__(
        self,
        *,
        job_id: str,
        table_name: str,
        open_table: Callable[[str], Any],
        history: Any,
        interval_s: float,
        stale_leases: float = DEFAULT_STALE_LEASES,
        on_event: Callable[[str], None] | None = None,
        namespace: list[str] | None = None,
    ) -> None:
        self._job_id = job_id
        self._table_name = table_name
        self._open_table = open_table
        self._history = history
        self._interval_s = interval_s
        self._stale_leases = stale_leases
        self._on_event = on_event
        # Different namespaces can share history, but open different tables.
        self._progress_key = SWEEP_PROGRESS_KEY + json.dumps(
            namespace or [], separators=(",", ":")
        )
        self._check_s = min(interval_s, _CHECK_EVERY_S)
        self._failures = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=self._run, name=f"geneva-compaction-sweep-{job_id}", daemon=True
        )

    def start(self) -> None:
        self._thread.start()

    def stop(self, timeout: float = _STOP_TIMEOUT_S) -> None:
        """Stop sweeping; a resume already started finishes its safety re-check.
        Wait at most ``timeout`` for that."""
        self._stop.set()
        if self._thread.ident is not None:
            self._thread.join(timeout)

    def _open_jobs_dataset(self) -> Any:
        # to_lance: fresh — the claim is checked against every claim made so far.
        return self._history.get_table(True).to_lance()

    def sweep_once(self) -> list[str] | None:
        """Sweep if this driver wins the interval's claim. Returns the tables
        it resumed, or None if another driver sweeps this interval or the claim
        failed. Never raises."""
        try:
            lease = claim_sweep(
                self._open_jobs_dataset,
                holder=self._job_id,
                interval_s=self._interval_s,
            )
            if lease is None:
                return None
            _LOG.info(
                "Job %s claimed the compaction sweep until %s",
                self._job_id,
                lease.expires_at.isoformat(),
            )
            jobs_dataset = self._open_jobs_dataset()
            progress = SweepProgress.parse(
                jobs_dataset.config().get(self._progress_key)
            )
            resumed = sweep_paused_tables(
                jobs_dataset=jobs_dataset,
                history=self._history,
                open_table=self._open_table,
                skip_table=self._table_name,
                stale_leases=self._stale_leases,
                stopped=lambda: self._stop.is_set() or dt_now_utc() >= lease.expires_at,
                progress=progress,
            )
            ds = self._open_jobs_dataset()
            if SweepLease.parse(ds.config().get(SWEEP_LEASE_KEY)) == lease:
                # Touch the lease too: a newer claim must conflict with this
                # progress write, so an old sweeper cannot overwrite its cursor.
                ds.update_config(
                    {
                        SWEEP_LEASE_KEY: lease.to_json(),
                        self._progress_key: progress.to_json(),
                    }
                )
        except Exception:  # noqa: BLE001 - the next claim sweeps instead
            self._failures += 1
            _LOG.warning(
                "Compaction sweep by job %s failed (%d consecutive failures)",
                self._job_id,
                self._failures,
                exc_info=self._failures == 1,
            )
            return None
        self._failures = 0
        for name in resumed:
            _LOG.info(
                "Compaction sweep by job %s resumed compaction of table %s",
                self._job_id,
                name,
            )
            report_job_event(
                self._on_event,
                f"Resumed compaction of table {name}, which no running Geneva "
                "job held any more",
            )
        return resumed

    def _run(self) -> None:
        # The first read comes at a random point within one period, so drivers
        # launched in a burst spread their reads out.
        wait = random.uniform(0, self._check_s)
        while not self._stop.wait(wait):
            self.sweep_once()
            wait = self._check_s * random.uniform(1 - _CHECK_JITTER, 1 + _CHECK_JITTER)
