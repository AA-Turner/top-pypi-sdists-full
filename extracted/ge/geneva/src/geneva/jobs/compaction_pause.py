# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Pause the LanceDB Enterprise agent's automatic compaction of a table while
Geneva jobs run on it (GEN-994).

The agent compacts tables on its own schedule. A compaction that rewrites a
fragment a running job is about to commit to fails the job (GEN-871) and
orphans its checkpoints, which are keyed by fragment id. The agent takes each
table's maintenance policy from the table itself: the JSON object under the
``lancedb.table_overrides`` config key, which it reads before planning a
compaction and again before starting one. Turning compaction off there stops
new compactions and cancels pending ones when they come up for admission; one
already running finishes.

So a job turns automatic compaction of its table off with an ordinary Lance
config commit on that table, and the last Geneva job on the table whose driver
is still alive turns it back on when it finishes. No Enterprise service is
contacted. Geneva tags its pause (``job_types.compaction.paused_by_geneva``) so
that it only ever undoes its own pause: compaction an operator turned off stays
off. Every other field of the object is kept as it was.

A driver shows it is alive through its heartbeat (:mod:`geneva.jobs.heartbeat`).
While its heartbeat is not landing, it renews its hold inside the tag instead,
in the same object a resume has to change, so no resume can take a live driver
for a dead one. A driver that can do neither for long enough that it might be
taken for dead stops before its next commit (:func:`check_compaction_hold`).

Lance rejects a config commit whose key changed after it was read, so each
update re-reads the object and retries instead of overwriting a concurrent
change.

With the deployment's Job Registry root configured, a job also waits for
compactions already running on its table before it plans. That reads the
registry and never writes to it (see :mod:`geneva.jobs.job_registry_reader`).
"""

from __future__ import annotations

import enum
import json
import logging
import threading
import time
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

import attrs

from geneva.config import ConfigBase, str_to_bool
from geneva.jobs.heartbeat import (
    DEFAULT_HEARTBEAT_INTERVAL_S,
    DEFAULT_LEASE_INTERVALS,
    DriverLiveness,
)
from geneva.jobs.job_registry_reader import (
    RegistryTableRef,
    in_flight_compactions,
    reader_for,
)
from geneva.utils import dt_now_utc

if TYPE_CHECKING:
    from collections.abc import Callable, Collection

    from geneva.jobs.heartbeat import DriverHeartbeatWriter

_LOG = logging.getLogger(__name__)

# The table config key the agent reads a table's maintenance policy from.
TABLE_OVERRIDES_CONFIG_KEY = "lancedb.table_overrides"
# Tags a pause as Geneva's, inside ``job_types.compaction``.
PAUSE_MARKER = "paused_by_geneva"
# Shown to anyone reading the overrides, e.g. ``lancedb admin table overrides
# get``. A person who sees ``enabled: false`` next to Geneva's tag can't tell it
# will be undone, and Geneva can't tell their ``enabled: false`` from its own
# (the value is identical), so the tag says how to keep compaction off.
PAUSE_NOTE = (
    "Set by Geneva while its jobs run; Geneva turns compaction back on when "
    "they end. To keep it off, set previous_enabled to false, or delete this "
    "entry and keep enabled false."
)

# Env vars holding CompactionPauseConfig; forwarded to Ray workers.
COMPACTION_PAUSE_ENV_PREFIX = "GENEVA_COMPACTION_PAUSE__"

_MAX_UPDATE_ATTEMPTS = 5
# geneva_jobs statuses of a job that has not finished.
_UNFINISHED_STATUSES = ("RUNNING", "PENDING")
# How many of its own heartbeat leases a driver must be silent for before its
# job stops holding the pause: 30 min at the default 30 s heartbeat interval.
DEFAULT_STALE_LEASES = 15.0
# The lease of a driver whose heartbeats are turned off.
_DEFAULT_LEASE_S = DEFAULT_HEARTBEAT_INTERVAL_S * DEFAULT_LEASE_INTERVALS

# Inside Geneva's tag: holds renewed by drivers whose heartbeat is not landing,
# as {job_id: {"at": <iso time>, "valid_s": <seconds>}}.
RENEWALS_KEY = "renewals"
# A driver renews after this fraction of a renewal's validity without a landed
# heartbeat, so it gets several tries before a resumer could release it.
_RENEW_FRACTION = 1 / 3
# A driver stops committing once nothing has shown its hold for this fraction of
# a renewal's validity: a third of the window before any resume could release
# it, which covers clock skew between hosts and a commit already in flight.
_FENCE_FRACTION = 2 / 3
# How often a driver checks whether its hold needs renewing; no I/O unless so.
_KEEPER_POLL_S = 60.0
# How often a running job reads its table's overrides to check that its pause is
# still in place, e.g. that no one ran ``lancedb admin table overrides reset``.
# Each check opens the table's latest version, so it isn't done every poll.
_CHECK_EVERY_S = 300.0
_KEEPER_STOP_TIMEOUT_S = 30.0


@attrs.define
class CompactionPauseConfig(ConfigBase):
    """Whether jobs pause the Enterprise agent's automatic compaction of their
    table; off unless ``GENEVA_COMPACTION_PAUSE__ENABLED`` is true.

    A Geneva job on the table whose ``geneva_jobs`` row is PENDING or RUNNING
    keeps compaction paused while its driver shows it is alive. That is judged
    from the driver, not the row, which a live driver can leave untouched for a
    long time while it plans or waits:

    - **Heartbeat:** a job holds while its driver heartbeat has landed within
      ``..._STALE_LEASES`` of the driver's own leases (15: 30 min at the default
      30 s heartbeat interval; 0: a driver whose heartbeat stops never
      releases).
    - **Renewal:** while its heartbeat is not landing, the driver renews its hold
      in the pause's own tag every third of that window. A resume re-reads the
      tag in the commit that would undo the pause, so a renewal always wins.
    - **Released:** a job whose driver exited, or has gone silent on both for
      longer, no longer holds. Nor does one whose driver never wrote a
      heartbeat: it hasn't started, or predates this and never paused.
    - **Fence:** a driver silent on both for two thirds of that window stops
      before its next commit that replaces fragments, and its job fails, so it
      never commits after it could have been released.

    The next Geneva job on the table to end resumes compaction, as does the
    submitter when Ray reports a driver lost, or :func:`resume_if_idle`.

    Operators keep the last word, through the overrides they already edit:

    - **Keep compaction off** after Geneva's jobs end: set ``previous_enabled``
      to ``false`` in Geneva's tag, or delete the tag and keep
      ``enabled: false``. Compaction off without the tag is never touched.
    - **Turn compaction on** while jobs run: delete the tag and set
      ``enabled: true``. Running jobs leave it on and record that they're
      exposed.
    - **A reset** (``lancedb admin table overrides reset``) while jobs run is
      undone: each running job checks its pause every 5 min and pauses again.

    With ``..._JOB_REGISTRY_ROOT_URI`` (the agent's ``jobRegistryRootUri``, e.g.
    ``s3://bucket/lancedb-system``) and ``..._JOB_REGISTRY_DATABASE`` (the
    Enterprise database name) set, a job also waits for compactions already
    running on its table before planning (``..._COMPACTION_WAIT_TIMEOUT_S``, 0
    to skip). It first pauses ``..._COMPACTION_SETTLE_S`` so that a compaction
    admitted just before the pause has been recorded, then checks every
    ``..._COMPACTION_POLL_INTERVAL_S``.
    """

    enabled: bool = attrs.field(default=False, converter=str_to_bool)
    stale_leases: float = attrs.field(default=DEFAULT_STALE_LEASES, converter=float)
    job_registry_root_uri: str | None = attrs.field(default=None)
    job_registry_database: str | None = attrs.field(default=None)
    job_registry_region: str | None = attrs.field(default=None)
    compaction_wait_timeout_s: float = attrs.field(default=3600.0, converter=float)
    compaction_settle_s: float = attrs.field(default=10.0, converter=float)
    compaction_poll_interval_s: float = attrs.field(default=30.0, converter=float)

    @classmethod
    def name(cls) -> str:
        return "geneva_compaction_pause"


class PauseOutcome(enum.Enum):
    """What pausing found."""

    PAUSED = "paused"
    """Compaction was on; Geneva turned it off."""
    ALREADY_PAUSED = "already_paused"
    """Another Geneva job had already paused it."""
    DISABLED_BY_POLICY = "disabled_by_policy"
    """An operator had turned it off; Geneva leaves it to them."""
    FAILED = "failed"
    """Pausing failed; the job runs with compaction possibly on."""


def _parse_overrides(raw: str | None) -> dict[str, Any]:
    if raw is None:
        return {}
    overrides = json.loads(raw)
    if not isinstance(overrides, dict):
        raise ValueError(f"{TABLE_OVERRIDES_CONFIG_KEY} is not a JSON object")
    return overrides


def _section(parent: dict[str, Any], key: str) -> dict[str, Any]:
    """``parent[key]``, created empty if absent."""
    section = parent.setdefault(key, {})
    if not isinstance(section, dict):
        raise ValueError(f"{TABLE_OVERRIDES_CONFIG_KEY} {key} is not a JSON object")
    return section


def update_table_overrides(
    open_dataset: Callable[[], Any],
    change: Callable[[dict[str, Any]], bool],
) -> bool:
    """Apply ``change`` to a table's overrides; True if it wrote them.

    ``change`` edits the parsed object in place and returns whether it changed
    anything. An object left empty removes the key. When another commit changed
    the key after it was read, Lance rejects the write, and the change is
    applied again to the object as it now is.
    """
    for attempt in range(1, _MAX_UPDATE_ATTEMPTS + 1):
        ds = open_dataset()
        overrides = _parse_overrides(ds.config().get(TABLE_OVERRIDES_CONFIG_KEY))
        if not change(overrides):
            return False
        value = json.dumps(overrides, separators=(",", ":")) if overrides else None
        try:
            ds.update_config({TABLE_OVERRIDES_CONFIG_KEY: value})
        except OSError:
            if attempt == _MAX_UPDATE_ATTEMPTS:
                raise
            _LOG.info(
                "Table overrides changed while being updated; retrying", exc_info=True
            )
            continue
        return True
    return False  # pragma: no cover - the last attempt returns or raises


@attrs.define(frozen=True)
class HoldRenewal:
    """A running job's renewal of its hold, recorded in Geneva's tag."""

    job_id: str
    # How long the renewal keeps the job holding without another one.
    valid_s: float


def _renewal_fresh(entry: Any, now: datetime) -> bool:
    try:
        at = datetime.fromisoformat(entry["at"])
        return now < at + timedelta(seconds=float(entry["valid_s"]))
    except (KeyError, TypeError, ValueError):
        _LOG.warning("Ignoring malformed compaction hold renewal %r", entry)
        return False


def _fresh_renewals(
    marker: Any, now: datetime, ignore: Collection[str] = ()
) -> list[str]:
    """Ids of jobs, other than those in ``ignore``, whose renewal in Geneva's
    tag still holds the pause."""
    renewals = marker.get(RENEWALS_KEY) if isinstance(marker, dict) else None
    if not isinstance(renewals, dict):
        return []
    return [
        job_id
        for job_id, entry in renewals.items()
        if job_id not in ignore and _renewal_fresh(entry, now)
    ]


def _renew(marker: dict[str, Any], renewal: HoldRenewal, now: datetime) -> None:
    """Record ``renewal`` in Geneva's tag, dropping renewals that have lapsed."""
    renewals = marker.get(RENEWALS_KEY)
    kept = (
        {k: v for k, v in renewals.items() if _renewal_fresh(v, now)}
        if isinstance(renewals, dict)
        else {}
    )
    kept[renewal.job_id] = {"at": now.isoformat(), "valid_s": renewal.valid_s}
    marker[RENEWALS_KEY] = kept


def _new_marker(
    compaction: dict[str, Any], renewal: HoldRenewal | None, now: datetime
) -> dict[str, Any]:
    """Geneva's tag for a pause it is about to make of ``compaction``.

    ``previous_enabled`` is what resuming puts back: ``true`` if compaction was
    explicitly on, ``null`` if it was unset. It is always written, so an
    operator reading the overrides can set it to ``false`` to keep compaction
    off after Geneva's jobs end (see :data:`PAUSE_NOTE`).
    """
    previous = compaction.get("enabled")
    marker: dict[str, Any] = {
        "paused_at": now.isoformat(),
        "previous_enabled": previous if isinstance(previous, bool) else None,
        "note": PAUSE_NOTE,
    }
    if renewal is not None:
        _renew(marker, renewal, now)
    return marker


def pause_compaction(
    open_dataset: Callable[[], Any], *, renewal: HoldRenewal | None = None
) -> PauseOutcome:
    """Turn the table's automatic compaction off, unless it is off already.

    With ``renewal``, also records in Geneva's tag that the renewing job still
    holds the pause, turning compaction off again if it had been resumed.
    """
    outcome = PauseOutcome.PAUSED

    def change(overrides: dict[str, Any]) -> bool:
        nonlocal outcome
        compaction = _section(_section(overrides, "job_types"), "compaction")
        now = dt_now_utc()
        if PAUSE_MARKER in compaction:
            outcome = PauseOutcome.ALREADY_PAUSED
            if renewal is None:
                return False
            marker = compaction[PAUSE_MARKER]
            if not isinstance(marker, dict):
                raise ValueError(f"{PAUSE_MARKER} is not a JSON object")
            _renew(marker, renewal, now)
            return True
        if compaction.get("enabled") is False:
            outcome = PauseOutcome.DISABLED_BY_POLICY
            return False
        outcome = PauseOutcome.PAUSED
        # Built before ``enabled`` is overwritten, to remember what was there.
        compaction[PAUSE_MARKER] = _new_marker(compaction, renewal, now)
        compaction["enabled"] = False
        return True

    update_table_overrides(open_dataset, change)
    return outcome


def _resume(
    open_dataset: Callable[[], Any], ignore: Collection[str]
) -> tuple[bool, list[str]]:
    """Undo Geneva's pause unless a renewal still holds it. Returns whether it
    resumed, and the ids of jobs whose renewal kept it paused."""
    renewed_by: list[str] = []

    def change(overrides: dict[str, Any]) -> bool:
        nonlocal renewed_by
        job_types = overrides.get("job_types")
        if not isinstance(job_types, dict):
            return False
        compaction = job_types.get("compaction")
        if not isinstance(compaction, dict) or PAUSE_MARKER not in compaction:
            return False
        renewed_by = _fresh_renewals(compaction[PAUSE_MARKER], dt_now_utc(), ignore)
        if renewed_by:
            return False
        marker = compaction.pop(PAUSE_MARKER)
        # Only an ``enabled: false`` is Geneva's to undo. Anything else is an
        # operator's choice made while the table was paused (``true`` to turn
        # compaction on, or deleting ``enabled``), and it is kept as it is.
        if compaction.get("enabled") is False:
            # ``previous_enabled`` is what the table had before the pause, or
            # what an operator asked for since: ``false`` keeps compaction off,
            # and with the tag gone that ``enabled: false`` is theirs from now on.
            previous = (
                marker.get("previous_enabled") if isinstance(marker, dict) else None
            )
            if isinstance(previous, bool):
                compaction["enabled"] = previous
            else:
                del compaction["enabled"]
        if not compaction:
            del job_types["compaction"]
        if not job_types:
            del overrides["job_types"]
        return True

    resumed = update_table_overrides(open_dataset, change)
    return resumed, renewed_by


def resume_compaction(
    open_dataset: Callable[[], Any], *, exclude_job_id: str | None = None
) -> bool:
    """Undo Geneva's pause of the table's compaction; True if it did.

    The pause stays while any job other than ``exclude_job_id`` has a renewal in
    Geneva's tag that still holds it. ``enabled`` goes back to the tag's
    ``previous_enabled``: as it was before the pause, or ``false`` if an
    operator set that to keep compaction off. An ``enabled: true``, or a
    deleted ``enabled``, that an operator set while it was paused is kept, as
    is every other field. Deleting ``paused_by_geneva`` and keeping
    ``enabled: false`` also keeps compaction off.
    """
    return _resume(open_dataset, () if exclude_job_id is None else (exclude_job_id,))[0]


def _released_because(
    history: Any, job_id: str, stale_leases: float, now: datetime
) -> str | None:
    """Why the job's heartbeat no longer holds the pause, or None if it does.

    A heartbeat that can't be read raises: nothing can be told about the driver.
    """
    heartbeat = history.get_heartbeat(job_id)
    if heartbeat is None:
        return "its driver has written no heartbeat"
    liveness = heartbeat.liveness(now)
    if liveness is DriverLiveness.EXITED:
        return "its driver exited without recording a final status"
    silent_s = (now - heartbeat.written_at).total_seconds()
    if (
        liveness is DriverLiveness.STALE
        and stale_leases > 0
        and silent_s > stale_leases * heartbeat.lease_s
    ):
        return (
            f"no heartbeat from its driver for {silent_s / 60:.0f} min "
            f"({stale_leases:g} leases of {heartbeat.lease_s:g} s)"
        )
    return None


def jobs_holding_pause(
    history: Any,
    table_name: str,
    *,
    exclude_job_id: str | None = None,
    stale_leases: float = DEFAULT_STALE_LEASES,
    now: datetime | None = None,
) -> list[str]:
    """Ids of Geneva jobs on ``table_name``, other than ``exclude_job_id``, whose
    driver heartbeat keeps its compaction paused: PENDING or RUNNING, with a
    heartbeat that is not exited or silent too long (see
    :class:`CompactionPauseConfig`). Renewals are checked by the resume itself.

    Jobs are matched by table name, so a same-named table in another namespace
    of the same database also counts; that only keeps compaction paused longer.
    """
    now = now or dt_now_utc()
    holding = []
    for status in _UNFINISHED_STATUSES:
        for job in history.list_jobs(table_name=table_name, status=status):
            if job.job_id == exclude_job_id:
                continue
            if reason := _released_because(history, job.job_id, stale_leases, now):
                _LOG.debug(
                    "Job %s does not hold the compaction pause of table %s: %s",
                    job.job_id,
                    table_name,
                    reason,
                )
                continue
            holding.append(job.job_id)
    return holding


def _finished(history: Any, job_ids: list[str]) -> set[str]:
    """Those of ``job_ids`` whose ``geneva_jobs`` row has a final status. A job
    with no row here, say from another jobs table, is not known to be finished."""
    finished = set()
    for job_id in job_ids:
        statuses = [
            getattr(job.status, "value", job.status) for job in history.get(job_id)
        ]
        if statuses and not set(statuses) & set(_UNFINISHED_STATUSES):
            finished.add(job_id)
    return finished


def _renewal_valid_s(stale_leases: float, lease_s: float) -> float:
    """How long a renewal holds: as long as a silent heartbeat would."""
    return (stale_leases if stale_leases > 0 else DEFAULT_STALE_LEASES) * lease_s


class _KeeperStoppedError(Exception):
    """The job ended while its hold was being renewed."""


class CompactionPauseLapsedError(Exception):
    """A job's hold on its table's compaction pause may have lapsed, so it stops
    instead of committing over fragments a compaction may have rewritten."""


class _HoldKeeper:
    """Renews a running job's hold in Geneva's tag while its driver heartbeat
    is not landing, so no resume takes the live driver for a dead one. Also
    tracks whether the hold may have lapsed, so the job stops committing."""

    def __init__(
        self,
        *,
        job_id: str,
        table_name: str,
        open_dataset: Callable[[], Any],
        heartbeat: DriverHeartbeatWriter | None,
        stale_leases: float,
        renewed: bool,
        on_event: Callable[[str], None] | None,
        poll_s: float = _KEEPER_POLL_S,
    ) -> None:
        lease_s = heartbeat.lease_s if heartbeat is not None else _DEFAULT_LEASE_S
        self.renewal = HoldRenewal(job_id, _renewal_valid_s(stale_leases, lease_s))
        self._renew_after_s = self.renewal.valid_s * _RENEW_FRACTION
        self._table_name = table_name
        self._open_dataset = open_dataset
        self._heartbeat = heartbeat
        self._stale_leases = stale_leases
        self._on_event = on_event
        self._fence_s = self.renewal.valid_s * _FENCE_FRACTION
        self._poll_s = min(poll_s, self._renew_after_s)
        self._lock = threading.Lock()
        # When something last showed other jobs this one holds the pause.
        self._last_shown: float | None = None
        self._heartbeat_landed = False
        self._lapsed_after_s: float | None = None
        self._lapse_reported = False
        self._turned_on_reported = False
        self._failures = 0
        now = time.monotonic()
        self._check_every_s = min(_CHECK_EVERY_S, self._renew_after_s)
        self._last_checked = now
        self._last_renewed = now if renewed else None
        since = None if heartbeat is None else heartbeat.seconds_since_written()
        if since is not None:
            self.heartbeat_landed(now - since)
        if renewed:
            self.shown(now)
        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=self._run, name=f"geneva-compaction-hold-{job_id}", daemon=True
        )

    def start(self) -> None:
        self._thread.start()

    def stop(self, timeout: float = _KEEPER_STOP_TIMEOUT_S) -> None:
        """Stop renewing, waiting at most ``timeout`` for a renewal in flight."""
        self._stop.set()
        if self._thread.ident is not None:
            self._thread.join(timeout)

    def _fenced(self) -> bool:
        # A landed heartbeat holds until the row is final when silence never
        # releases, so the hold can't lapse after one.
        return not (self._stale_leases <= 0 and self._heartbeat_landed)

    def shown(self, at: float) -> None:
        """Record that a heartbeat or renewal written at monotonic time ``at``
        showed this job's hold. A gap since the previous one long enough for the
        hold to lapse is latched before the gap is forgotten."""
        with self._lock:
            last = self._last_shown
            if last is not None and self._fenced() and at - last >= self._fence_s:
                self._latch(at - last)
            if last is None or at > last:
                self._last_shown = at

    def heartbeat_landed(self, written: float) -> None:
        """Listener for the driver's heartbeat writer."""
        self.shown(written)
        self._heartbeat_landed = True

    def renew_due(self) -> bool:
        """Whether the hold needs renewing: no heartbeat has landed lately, and
        it wasn't renewed lately."""
        since = (
            None if self._heartbeat is None else self._heartbeat.seconds_since_written()
        )
        if since is not None and (
            self._stale_leases <= 0 or since < self._renew_after_s
        ):
            return False
        return (
            self._last_renewed is None
            or time.monotonic() - self._last_renewed >= self._renew_after_s
        )

    def silent_s(self) -> float:
        """Seconds since anything last showed other jobs that this one holds the
        pause: a landed heartbeat, or a renewal."""
        if not self._fenced():
            return 0.0
        last = self._last_shown
        # Pausing either waits for a heartbeat or renews, so one is always set.
        return 0.0 if last is None else time.monotonic() - last

    def check_held(self) -> None:
        """Raise :class:`CompactionPauseLapsedError` once the hold may have
        lapsed. Sticky: a resume may already have let a compaction start."""
        self._note_lapse()
        if self._lapsed_after_s is not None:
            raise CompactionPauseLapsedError(
                f"Job {self.renewal.job_id} stopped before committing: nothing "
                f"showed its hold on the compaction pause of table "
                f"{self._table_name} for {self._lapsed_after_s / 60:.0f} min, so a "
                "compaction may have rewritten its fragments. Run it again; its "
                "checkpoints keep the work it finished."
            )

    def _latch(self, silent: float) -> None:
        if self._lapsed_after_s is not None:
            return
        self._lapsed_after_s = silent
        _LOG.warning(
            "Job %s showed no hold on the compaction pause of table %s for "
            "%.0f min; it stops before its next commit",
            self.renewal.job_id,
            self._table_name,
            silent / 60,
        )

    def _note_lapse(self) -> None:
        with self._lock:
            silent = self.silent_s()
            if silent >= self._fence_s:
                self._latch(silent)
            lapsed_after = self._lapsed_after_s
            report = lapsed_after is not None and not self._lapse_reported
            self._lapse_reported = self._lapse_reported or report
        if report and lapsed_after is not None:
            _report(
                self._on_event,
                f"Compaction pause may have lapsed: no heartbeat or renewal for "
                f"{lapsed_after / 60:.0f} min; stopping before the next commit",
            )

    def _open_unless_stopped(self) -> Any:
        # Checked before each attempt, so a renewal never lands after the job's
        # own resume once it has stopped the keeper.
        if self._stop.is_set():
            raise _KeeperStoppedError
        return self._open_dataset()

    def renew(self) -> None:
        """Renew the hold, pausing again if the pause was wiped. Never raises."""
        self.check_pause(renew=True)

    def check_due(self) -> bool:
        """Whether it's time to check that the pause is still in place."""
        return time.monotonic() - self._last_checked >= self._check_every_s

    def check_pause(self, *, renew: bool) -> None:
        """Check that the table is still paused for this job, and with ``renew``
        record this job's hold in Geneva's tag. Never raises.

        Everything is decided inside one compare-and-swap update of the
        overrides, so a concurrent edit by an operator or another job makes this
        re-read and decide again, and is never overwritten:

        - **Geneva's tag is there:** the pause is in place. With ``renew``, this
          job's renewal is added to the tag, also beside an ``enabled: true`` an
          operator set in place: compaction is left on, and the job records once
          that it is exposed.
        - **No tag, ``enabled: false``:** an operator took compaction over and
          keeps it off. That protects the job just as well; nothing to write.
        - **No tag, ``enabled: true``:** an operator turned compaction on while
          the job runs. Removing the tag and setting ``true`` is deliberate, so
          it's left on and recorded on the job, not fought.
        - **No tag and no ``enabled``:** the pause was wiped, typically by
          ``lancedb admin table overrides reset``, and nobody asked for
          compaction. Pause again and record it on the job.
        """
        # Read before the update, so it is never later than the renewal's time.
        started = time.monotonic()
        found: str | None = None
        wrote_renewal = False

        def change(overrides: dict[str, Any]) -> bool:
            nonlocal found, wrote_renewal
            wrote_renewal = False
            compaction = _section(_section(overrides, "job_types"), "compaction")
            enabled = compaction.get("enabled")
            if PAUSE_MARKER in compaction:
                found = "turned_on" if enabled is True else "paused"
                if not renew:
                    return False
                marker = compaction[PAUSE_MARKER]
                if not isinstance(marker, dict):
                    raise ValueError(f"{PAUSE_MARKER} is not a JSON object")
                _renew(marker, self.renewal, dt_now_utc())
                wrote_renewal = True
                return True
            if enabled is False:
                found = "kept_off"
                return False
            if enabled is True:
                found = "turned_on"
                return False
            found = "wiped"
            compaction[PAUSE_MARKER] = _new_marker(
                compaction, self.renewal if renew else None, dt_now_utc()
            )
            compaction["enabled"] = False
            wrote_renewal = renew
            return True

        try:
            update_table_overrides(self._open_unless_stopped, change)
        except _KeeperStoppedError:
            return
        except Exception:  # noqa: BLE001 - the next poll retries
            self._failures += 1
            _LOG.warning(
                "Failed to check job %s's hold on the compaction pause of table %s "
                "(%d consecutive failures)",
                self.renewal.job_id,
                self._table_name,
                self._failures,
                exc_info=self._failures == 1,
            )
            return
        self._failures = 0
        self._last_checked = started
        # What other jobs can now see: a renewal written into the tag, whatever
        # ``enabled`` says beside it, or an operator's own ``enabled: false``,
        # which no resume can undo, so the job is as protected as by its own
        # hold. Either way the next renewal isn't due before its time.
        if wrote_renewal or found == "kept_off":
            self._last_renewed = started
            self.shown(started)
        if found == "wiped":
            _LOG.warning(
                "The compaction pause of table %s was removed while job %s runs; "
                "paused it again",
                self._table_name,
                self.renewal.job_id,
            )
            _report(
                self._on_event,
                "Compaction pause was removed while this job runs, e.g. by an "
                "overrides reset; paused it again",
            )
        elif found == "turned_on" and not self._turned_on_reported:
            self._turned_on_reported = True
            _LOG.warning(
                "Compaction of table %s was turned on by hand while job %s runs; "
                "leaving it on",
                self._table_name,
                self.renewal.job_id,
            )
            _report(
                self._on_event,
                "Compaction was turned on by hand while this job runs; leaving it on",
            )

    def _run(self) -> None:
        while not self._stop.wait(self._poll_s):
            # Before renewing, so a renewal can't hide how long the hold went
            # unshown; shown() also latches a gap the renewal closes.
            self._note_lapse()
            if self.renew_due():
                self.renew()
            elif self.check_due():
                self.check_pause(renew=False)


# The pauses held by drivers running in this process, by job id.
_ACTIVE_PAUSES: dict[str, CompactionPause] = {}
_ACTIVE_PAUSES_LOCK = threading.Lock()


def check_compaction_hold(job_id: str | None) -> None:
    """Call before a commit that replaces fragments: raises
    :class:`CompactionPauseLapsedError` if this process's driver for ``job_id``
    may have lost its hold on the compaction pause. A no-op otherwise."""
    if not job_id:
        return
    with _ACTIVE_PAUSES_LOCK:
        pause = _ACTIVE_PAUSES.get(job_id)
    if pause is not None and pause.keeper is not None:
        pause.keeper.check_held()


@attrs.define
class CompactionPause:
    """A running job's hold on its table's compaction, from :func:`pause_for_job`."""

    table_name: str
    job_id: str
    outcome: PauseOutcome
    open_dataset: Callable[[], Any] = attrs.field(repr=False)
    history: Any = attrs.field(repr=False)
    stale_leases: float = DEFAULT_STALE_LEASES
    on_event: Callable[[str], None] | None = attrs.field(default=None, repr=False)
    keeper: _HoldKeeper | None = attrs.field(default=None, repr=False)


def _report(on_event: Callable[[str], None] | None, message: str) -> None:
    """Record ``message`` on the job, if asked. Never raises."""
    if on_event is None:
        return
    try:
        on_event(message)
    except Exception:  # noqa: BLE001 - reporting must never fail the job
        _LOG.debug("Could not record job event %r", message, exc_info=True)


def pause_for_job(
    *,
    table_name: str,
    job_id: str,
    open_dataset: Callable[[], Any],
    history: Any,
    heartbeat: DriverHeartbeatWriter | None = None,
    config: CompactionPauseConfig | None = None,
    on_event: Callable[[str], None] | None = None,
) -> CompactionPause | None:
    """Pause automatic compaction of a job's table while the job runs.

    ``heartbeat`` is the driver's heartbeat writer, which shows other jobs this
    one still holds the pause. Until its first heartbeat lands, and whenever
    its heartbeats stop landing, the job renews its hold in Geneva's tag
    instead.

    Returns None when pausing is not configured. When pausing fails, the job
    runs unprotected and the failure is passed to ``on_event`` to record on the
    job, but a pause is still returned: whatever a job's own pause found, the
    table may be paused for another job, and only the last job on the table to
    end can undo that. Pass the result to :func:`resume_after_job` when the job
    ends.
    """
    try:
        config = config or CompactionPauseConfig.get()
        if not config.enabled:
            return None
        # A resume only sees this job's hold once its heartbeat has landed, so
        # that comes before reading the pause; if it doesn't land, renew.
        landed = heartbeat is not None and heartbeat.wait_written(heartbeat.interval_s)
        keeper = _HoldKeeper(
            job_id=job_id,
            table_name=table_name,
            open_dataset=open_dataset,
            heartbeat=heartbeat,
            stale_leases=config.stale_leases,
            renewed=not landed,
            on_event=on_event,
        )
        outcome = pause_compaction(
            open_dataset, renewal=None if landed else keeper.renewal
        )
    except Exception as exc:  # noqa: BLE001 - pausing must never fail the job
        _LOG.warning(
            "Failed to pause automatic compaction of table %s for job %s; it is "
            "not paused",
            table_name,
            job_id,
            exc_info=True,
        )
        _report(on_event, f"Compaction not paused: {type(exc).__name__}: {exc}")
        if config is None:  # couldn't be read, so nothing says pausing is on
            return None
        return CompactionPause(
            table_name=table_name,
            job_id=job_id,
            outcome=PauseOutcome.FAILED,
            open_dataset=open_dataset,
            history=history,
            stale_leases=config.stale_leases,
            on_event=on_event,
        )
    if outcome is PauseOutcome.DISABLED_BY_POLICY:
        _LOG.info(
            "Automatic compaction of table %s is turned off by its table "
            "overrides; job %s leaves it off",
            table_name,
            job_id,
        )
        keeper = None
    else:
        _LOG.info(
            "Automatic compaction of table %s is paused for job %s (%s)",
            table_name,
            job_id,
            outcome.value,
        )
        keeper.start()
        if heartbeat is not None:
            heartbeat.add_listener(keeper.heartbeat_landed)
    pause = CompactionPause(
        table_name=table_name,
        job_id=job_id,
        outcome=outcome,
        open_dataset=open_dataset,
        history=history,
        stale_leases=config.stale_leases,
        on_event=on_event,
        keeper=keeper,
    )
    if keeper is not None:
        with _ACTIVE_PAUSES_LOCK:
            _ACTIVE_PAUSES[job_id] = pause
    return pause


def resume_if_idle(
    *,
    table_name: str,
    open_dataset: Callable[[], Any],
    history: Any,
    exclude_job_id: str | None = None,
    stale_leases: float = DEFAULT_STALE_LEASES,
) -> bool:
    """Undo Geneva's pause of a table's compaction if no Geneva job on it,
    other than ``exclude_job_id``, still holds it: through its heartbeat (see
    :func:`jobs_holding_pause`) or a renewal in Geneva's tag.

    A job that started while this was resuming found compaction still paused
    and left it alone, so this pauses again for it. Returns whether compaction
    was left running. Raises when a holder's heartbeat can't be read, leaving
    compaction paused. Also for cleanup once a dead driver's row is marked
    finished.
    """

    def holding() -> list[str]:
        return jobs_holding_pause(
            history,
            table_name,
            exclude_job_id=exclude_job_id,
            stale_leases=stale_leases,
        )

    others = holding()
    if others:
        _LOG.info(
            "Automatic compaction of table %s stays paused for %d unfinished "
            "job(s): %s",
            table_name,
            len(others),
            ", ".join(others),
        )
        return False
    ignore = set() if exclude_job_id is None else {exclude_job_id}
    resumed, renewed_by = _resume(open_dataset, ignore)
    # A job that renewed and has since finished, or whose lost driver the
    # submitter recorded, no longer holds.
    if renewed_by and (finished := _finished(history, renewed_by)):
        resumed, renewed_by = _resume(open_dataset, ignore | finished)
    if renewed_by:
        _LOG.info(
            "Automatic compaction of table %s stays paused for job(s) %s, which "
            "renewed their hold while their heartbeat was not landing",
            table_name,
            ", ".join(renewed_by),
        )
        return False
    if not resumed:
        return False
    if holding():
        pause_compaction(open_dataset)
        _LOG.info(
            "A job started on table %s while compaction was resuming; paused it again",
            table_name,
        )
        return False
    _LOG.info("Resumed automatic compaction of table %s", table_name)
    return True


def resume_after_job(pause: CompactionPause | None) -> None:
    """Resume compaction when the last Geneva job on the table ends, whatever
    this job's own pause found: another job may have paused the table since,
    and a resume only ever undoes Geneva's pause, once no job holds it. A
    failure is recorded on the job; never raises."""
    if pause is None:
        return
    with _ACTIVE_PAUSES_LOCK:
        if _ACTIVE_PAUSES.get(pause.job_id) is pause:
            del _ACTIVE_PAUSES[pause.job_id]
    if pause.keeper is not None:
        pause.keeper.stop()
    try:
        resume_if_idle(
            table_name=pause.table_name,
            open_dataset=pause.open_dataset,
            history=pause.history,
            exclude_job_id=pause.job_id,
            stale_leases=pause.stale_leases,
        )
    except Exception as exc:  # noqa: BLE001 - the next job on the table resumes it instead
        _LOG.warning(
            "Failed to resume automatic compaction of table %s after job %s; it "
            "stays paused until another Geneva job on the table ends",
            pause.table_name,
            pause.job_id,
            exc_info=True,
        )
        _report(
            pause.on_event,
            f"Compaction left paused: {type(exc).__name__}: {exc}",
        )


def resume_after_driver_loss(
    *,
    table_name: str,
    open_dataset: Callable[[], Any],
    history: Any,
    config: CompactionPauseConfig | None = None,
) -> None:
    """Resume compaction of a table once the submitter has recorded that Ray
    lost a job's driver, unless another job still holds it. Never raises.

    The lost job is not excluded: its row is already final, and a driver that
    replaced it under the same id still holds through its own heartbeat.
    """
    try:
        config = config or CompactionPauseConfig.get()
        if not config.enabled:
            return
        resume_if_idle(
            table_name=table_name,
            open_dataset=open_dataset,
            history=history,
            stale_leases=config.stale_leases,
        )
    except Exception:  # noqa: BLE001 - the next job on the table resumes it instead
        _LOG.warning(
            "Failed to resume automatic compaction of table %s after its driver "
            "was lost; it stays paused until another Geneva job on the table ends",
            table_name,
            exc_info=True,
        )


def open_latest_dataset(table_ref: Any, *, use_worker_props: bool) -> Any:
    """A job's table (a :class:`~geneva.table.TableReference`) at its latest
    version, as a Lance dataset: what pausing and resuming read and commit to.
    ``use_worker_props`` picks the namespace's worker endpoint, for drivers."""
    from geneva.db import open_lance_dataset

    return open_lance_dataset(
        table_ref.table_uri,
        namespace_config=table_ref.namespace_config,
        table_id=table_ref.table_id,
        storage_options=table_ref.storage_options,
        use_worker_props=use_worker_props,
    )


def wait_for_compactions(
    *,
    table_id: list[str],
    config: CompactionPauseConfig | None = None,
    on_wait: Callable[[list[str]], None] | None = None,
    on_event: Callable[[str], None] | None = None,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
) -> list[str]:
    """Wait for compactions already running on a table before a job plans.

    Pausing stops the agent starting compactions, not one it already started,
    which can rewrite the fragments the job is about to plan over. Calls
    ``on_wait`` once with the compaction job ids it waits for, gives up after
    ``compaction_wait_timeout_s``, and returns the job ids it found. Giving up,
    or failing to check, is passed to ``on_event`` to record on the job. Never
    raises.
    """
    try:
        config = config or CompactionPauseConfig.get()
        if (
            not config.enabled
            or not config.job_registry_root_uri
            or not config.job_registry_database
            or config.compaction_wait_timeout_s <= 0
        ):
            return []
        reader = reader_for(config.job_registry_root_uri, config.job_registry_region)
        if reader is None:
            return []
        table = RegistryTableRef.for_table(config.job_registry_database, table_id)
        sleep(config.compaction_settle_s)
        deadline = clock() + config.compaction_wait_timeout_s
        seen: list[str] = []
        while running := in_flight_compactions(reader, table):
            if not seen and on_wait is not None:
                on_wait(running)
            seen.extend(job_id for job_id in running if job_id not in seen)
            if clock() >= deadline:
                _LOG.warning(
                    "Compaction %s of table %s still running after %.0fs; "
                    "proceeding, and the job fails if it rewrites fragments the "
                    "job planned over",
                    ", ".join(running),
                    table.dist_key,
                    config.compaction_wait_timeout_s,
                )
                _report(
                    on_event,
                    f"Stopped waiting for compaction {', '.join(running)} after "
                    f"{config.compaction_wait_timeout_s:.0f}s; planning anyway",
                )
                return seen
            _LOG.info(
                "Waiting for compaction %s of table %s to finish before planning",
                ", ".join(running),
                table.dist_key,
            )
            sleep(config.compaction_poll_interval_s)
        return seen
    except Exception as exc:  # noqa: BLE001 - checking must never fail the job
        _LOG.warning(
            "Failed to check the job registry for running compactions",
            exc_info=True,
        )
        _report(
            on_event,
            f"Could not check for running compactions: {type(exc).__name__}: {exc}",
        )
        return []
