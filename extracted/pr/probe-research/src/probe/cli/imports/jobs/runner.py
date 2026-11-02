"""run one approved job in this worker process: ownership lock, progress estimate, stall reports, what it remembers in its job file."""

from __future__ import annotations

import argparse
import math
import os
import signal
import sys
import threading
import time
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from pathlib import Path

from ....foundation.durable.durable import now_iso


#: How often a worker that is still waiting for a connection re-reports the
#: stall. Ten minutes keeps an overnight disconnection to a readable handful of
#: events while still bounding how long a new stall stays invisible.
STALL_REPORT_INTERVAL_S = 600.0
#: How long a worker waits for its connection before the first stall report.
#: A blip that one or two retries ride out is not a stall; without this every
#: transient 5xx paged #usage with "Import stuck" for an import that finished.
STALL_GRACE_S = 300.0
_active_job: Path | None = None  # One worker per process; launch threads share it.
#: The running attempt's agent meter (`import_agent_settings.Meter`), beside
#: `_active_job` and for the same reason: one worker per process. `_dispatch`
#: hands it to the folder lane; `run_worker` reports it on `import_job.finished`.
_attempt_meter = None


def prepared_approval_digest() -> str | None:
    """The automatic folder worker's durable transition into exact delivery."""
    return _read(_active_job).get("prepared_approval") if _active_job is not None else None


def remember_prepared_approval(digest: str) -> None:
    """A missing plan after this marker is an error, never permission to replan."""
    if _active_job is not None:
        _update(_active_job, prepared_approval=digest)


def remember_skipped(summary: dict) -> None:
    """What a folder worker's walk skipped by rule (`backfill.Census.skipped_json`),
    on the job record the desktop reads. Counts and root-relative folder names
    only; a foreground import has no active job and records nothing."""
    if _active_job is not None:
        _check_payload(summary)
        _update(_active_job, skipped=summary)


class _ProgressEstimate:
    """Estimate delivery time from observed work, never queue or scan duration."""

    def __init__(self, *, start_on_advance: bool = False):
        self.baseline = None
        self.latest = None
        self.start_on_advance = start_on_advance
        self.ready = not start_on_advance

    def update(self, previous: dict, fields: dict) -> dict:
        phase = fields.get("phase", previous.get("phase"))
        changed_phase = "phase" in fields and phase != previous.get("phase")
        result = {} if changed_phase else {
            key: previous[key] for key in (
                "completed", "total", "phase", "stage", "stage_completed", "stage_total",
                "completion_completed", "completion_total", "completion_ids",
                "eta_seconds", "eta_updated_at",
            ) if key in previous
        }
        result.update(fields)
        counter_keys = ("completion_completed", "completion_total") if any(
            key in result for key in ("completion_completed", "completion_total")
        ) else ("completed", "total")
        completed_key, total_key = counter_keys
        measured = all(
            isinstance(result.get(key), (int, float))
            and not isinstance(result[key], bool) and math.isfinite(result[key])
            for key in counter_keys
        ) and 0 <= result[completed_key] <= result[total_key] and result[total_key] > 0
        if changed_phase or phase == "scanning" or fields.get("waiting_for_connection") or not measured:
            self.baseline = self.latest = None
            result.pop("eta_seconds", None)
            result.pop("eta_updated_at", None)
            if phase == "scanning" or fields.get("waiting_for_connection") or not measured:
                return result
        # A message-only update retains the previous observation, but does not
        # manufacture another sample or count elapsed connection retry time.
        if any(key not in fields for key in counter_keys):
            return result
        now = time.monotonic()
        completed, total = result[completed_key], result[total_key]
        if self.baseline is None or self.latest is None or (
            self.latest[1:] != (total, counter_keys) or completed < self.latest[0]
        ):
            self.baseline = (now, completed)
            self.latest = (completed, total, counter_keys)
            self.ready = not self.start_on_advance
            result.pop("eta_seconds", None)
            result.pop("eta_updated_at", None)
            return result
        if completed > self.latest[0]:
            if not self.ready:
                # Folder work can prepare for minutes before its first new
                # receipt. Start timing at that receipt, including on resume
                # when the initial count already includes earlier deliveries.
                self.baseline = (now, completed)
                self.latest = (completed, total, counter_keys)
                self.ready = True
                result.pop("eta_seconds", None)
                result.pop("eta_updated_at", None)
                return result
            elapsed, advanced = now - self.baseline[0], completed - self.baseline[1]
            if elapsed >= 1 and advanced > 0:
                result["eta_seconds"] = (total - completed) * elapsed / advanced
                result["eta_updated_at"] = now_iso()
        self.latest = (completed, total, counter_keys)
        return result


def _agent_meter():
    """A meter for this attempt's coding agents (`import_agent_settings`), or
    None when this process cannot build one. Same rule as `_telemetry`: its
    absence costs the measurement, never the import."""
    try:
        from ..agent_settings import Meter

        return Meter()
    except Exception:
        return None


def _agent_props(meter) -> dict:
    """What this attempt's agents ran at and cost, for `import_job.finished`:
    per-lane settings, launches, refusals, cache hits and token sums
    (`Meter.properties`). Metadata only. Never raises."""
    try:
        return meter.properties() if meter is not None else {}
    except Exception:
        return {}


def run_worker(job_id: str, *, directory: Path | None = None) -> int:
    """Run one approved request under a process-lifetime ownership lock."""
    global _active_job, _attempt_meter

    folder = _directory(job_id, directory)
    with ExitStack() as ownership:
        # Status reads hold state.lock while briefly probing worker.lock. Wait
        # for that probe before claiming ownership, or a newborn worker can
        # mistake the reader for another worker and exit without an attempt.
        # The lifetime lock stays nonblocking: an existing worker can need
        # state.lock for progress, so waiting on its lock here would deadlock.
        with _job_lock(folder, "state.lock"):
            if not ownership.enter_context(_try_lock(folder / "worker.lock")):
                return 0
        job = _read(folder)
        if job.get("cancel_requested") or job["state"] in (State.SUCCEEDED, State.CANCELED):
            return 0
        # A new process cannot inherit the approving wizard's context object,
        # so it replays that session off the record. Without this the
        # completion lands in its own session and no funnel can join it to the
        # approval that asked for it.
        tel = _context(job)
        try:
            _reclaim_children(folder)
        except JobError as exc:
            failed = _update(folder, state=State.FAILED, error=_clean(exc), finished_at=now_iso())
            _emit_finished(failed, "launch_failed", tel=tel, failure_kind="reclaim")
            _report_failure(folder, failed, failure_kind="reclaim")
            return 1
        job = _update(
            folder, state=State.RUNNING, pid=os.getpid(),
            pid_identity=_process_identity(os.getpid()), attempt=job["attempt"] + 1,
            started_at=now_iso(), finished_at=None, error=None,
            progress=_progress_message(job["progress"], "Starting the approved import."),
        )
        if job.get("cancel_requested"):
            return 130

        estimate = _ProgressEstimate(start_on_advance=job["kind"] == Kind.FOLDER)
        progress_lock = threading.Lock()
        # One per ATTEMPT, across its connection and unit retries: the attempt
        # is what `import_job.finished` reports, failures included.
        meter = _agent_meter()

        def progress(message: str, **fields):
            if _read(folder).get("cancel_requested"):
                raise _Interrupted
            _check_payload(fields)
            # Folder callbacks can arrive from several worker threads. Keep
            # their observation and persisted state in the same order.
            with progress_lock:
                previous_progress = _read(folder)["progress"]
                if (job["kind"] == Kind.TRANSCRIPTS and "completion_ids" in fields
                        and fields.get("phase", previous_progress.get("phase")) != "scanning"
                        and previous_progress.get("phase") != "scanning"):
                    # A retry checks the same immutable approved sessions from
                    # the beginning. Already-finalized receipts remain valid;
                    # their identity must not disappear during that replay.
                    identities = [*previous_progress.get("completion_ids", []), *fields["completion_ids"]]
                    if all(isinstance(item, (list, tuple)) and len(item) == 2
                           and all(isinstance(part, str) for part in item) for item in identities):
                        fields["completion_ids"] = [list(item) for item in sorted({tuple(item) for item in identities})]
                        fields["completion_completed"] = len(fields["completion_ids"])
                update = estimate.update(previous_progress, fields)
                update["message"] = _clean(message)
                _update(folder, progress=update)
            print(f"{now_iso()} {_clean(message)}", flush=True)

        def interrupt(_signal, _frame):
            raise _Interrupted

        previous_job, _active_job = _active_job, folder
        previous_meter, _attempt_meter = _attempt_meter, meter
        previous = {}
        if threading.current_thread() is threading.main_thread():
            for number in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
                previous[number] = signal.getsignal(number)
                signal.signal(number, signal.SIG_IGN if number == signal.SIGHUP else interrupt)
        try:
            descriptor = os.open(folder / "output.log", os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
            with os.fdopen(descriptor, "a", encoding="utf-8", buffering=1) as output:
                with redirect_stdout(output), redirect_stderr(output):
                    print(f"{now_iso()} Starting attempt {job['attempt']}.", flush=True)
                    try:
                        with _serial_lane(job, folder):
                            retry_delay = 2
                            retries = 0
                            unit_retries = 0
                            waited = 0.0
                            # A disconnected laptop retries forever, so the
                            # stall is a LEVEL and not an edge. Report it once
                            # the wait passes STALL_GRACE_S, then at most once
                            # per STALL_REPORT_INTERVAL_S of continued waiting:
                            # an event per retry would turn one bad afternoon
                            # into hundreds.
                            reported = None
                            while True:
                                if _read(folder).get("cancel_requested"):
                                    raise _Interrupted
                                attempt_started = time.monotonic()
                                try:
                                    result = _dispatch(job["kind"], job["payload"], progress)
                                    break
                                except RetryableJobError as exc:
                                    # No coding-agent process may survive into
                                    # the next replay of this same approval.
                                    from .. import folder as backfill

                                    backfill.stop_all()
                                    _reclaim_children(folder)
                                    if isinstance(exc, UnitRetryJobError):
                                        # Bounded by the batches' attempt limit,
                                        # and not a stall: no connection wait.
                                        unit_retries += 1
                                        progress(
                                            f"{_clean(exc)} Retrying in {retry_delay}s.",
                                            retry_in=retry_delay, unit_retries=unit_retries,
                                        )
                                        time.sleep(retry_delay)
                                        continue
                                    if retries:
                                        # A retry that times out is waiting
                                        # time too, not only the sleep after it.
                                        waited += time.monotonic() - attempt_started
                                    retries += 1
                                    progress(
                                        f"Waiting for connection. Retrying in {retry_delay}s. {_clean(exc)}",
                                        waiting_for_connection=True,
                                        retry_in=retry_delay, network_retries=retries,
                                    )
                                    if waited >= STALL_GRACE_S and (
                                        reported is None or waited - reported >= STALL_REPORT_INTERVAL_S
                                    ):
                                        reported = waited
                                        _emit_stalled(
                                            _read(folder), "waiting_for_connection", tel=tel,
                                            network_retries=retries,
                                            waiting_seconds=round(waited, 1),
                                        )
                                    waited += retry_delay
                                    # Keep the lifetime locks, but no state lock,
                                    # while waiting. Signals still interrupt it.
                                    time.sleep(retry_delay)
                                    retry_delay = min(retry_delay * 2, 60)
                                    progress("Connection retry: resuming saved import progress.")
                        lines = result.splitlines() if isinstance(result, str) else list(result or [])
                        for line in lines:
                            print(_clean(line), flush=True)
                        done = _update(
                            folder, state=State.SUCCEEDED, pid=None, finished_at=now_iso(),
                            report=[_clean(line) for line in lines[-20:]],
                            progress=_progress_message(_read(folder)["progress"], "Import finished."),
                        )
                        _emit_finished(
                            done, "succeeded", tel=tel, network_retries=retries or None,
                            unit_retries=unit_retries or None, **_agent_props(meter),
                        )
                        return 0
                    except (_Interrupted, KeyboardInterrupt):
                        stopped = _update(
                            folder, state=State.INTERRUPTED, pid=None, finished_at=now_iso(),
                            progress=_progress_message(_read(folder)["progress"], "Worker interrupted; saved work can resume."),
                        )
                        if not stopped.get("cancel_requested"):
                            # A cancel arrives as a signal and lands here too;
                            # `_cancel_locked` owns that event and knows it was
                            # deliberate. Two terminal events for one job would
                            # be one import counted twice, as both.
                            _emit_finished(stopped, "interrupted", tel=tel, **_agent_props(meter))
                        return 130
                    except Exception as exc:
                        # HTTP exception strings can carry signed URLs or auth
                        # headers. Only lane-authored JobError prose is displayable.
                        reason = _clean(exc) if isinstance(exc, JobError) else f"Import failed ({type(exc).__name__})."
                        print(reason, flush=True)
                        broken = _update(
                            folder, state=State.FAILED, pid=None, finished_at=now_iso(), error=reason,
                            progress=_progress_message(_read(folder)["progress"], "Import needs attention before retrying."),
                        )
                        # The TYPE, never `reason`: lane-authored prose is safe
                        # to show a person but can name a folder, and a
                        # formatted httpx error can carry a signed URL.
                        _emit_finished(
                            broken, "failed", tel=tel,
                            failure_kind="refused" if isinstance(exc, JobError) else type(exc).__name__,
                            network_retries=retries or None, **_agent_props(meter),
                        )
                        _report_failure(
                            folder, broken,
                            failure_kind="refused" if isinstance(exc, JobError) else type(exc).__name__,
                        )
                        return 1
        finally:
            try:
                from .. import folder as backfill

                backfill.stop_all()
                _reclaim_children(folder)
            except JobError as exc:
                broken = _update(
                    folder, state=State.FAILED, pid=None, error=_clean(exc), finished_at=now_iso(),
                )
                _emit_finished(broken, "failed", tel=tel, failure_kind="cleanup", **_agent_props(meter))
                _report_failure(folder, broken, failure_kind="cleanup")
                raise
            finally:
                _active_job = previous_job
                _attempt_meter = previous_meter
                for number, handler in previous.items():
                    signal.signal(number, handler)


def main() -> None:
    # The old module's --help text, which its door (the package) keeps as its docstring.
    parser = argparse.ArgumentParser(description=sys.modules[__package__].__doc__)
    parser.add_argument("job_id")
    parser.add_argument("--directory", type=Path)
    # The Probe service's report of a worker it started that exited non-zero
    # (`probe.service.jobs.imports`): `_launch_failed`, never a worker run.
    parser.add_argument("--launch-failed", type=int, default=None, help=argparse.SUPPRESS)
    parser.add_argument("--attempt", type=int, default=None, help=argparse.SUPPRESS)
    parser.add_argument("--exit-code", type=int, default=None, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.launch_failed is not None:
        if args.attempt is None or not args.exit_code or not _ID.fullmatch(args.job_id):
            raise SystemExit(2)
        _launch_failed(_directory(args.job_id, args.directory), args.launch_failed, args.attempt, args.exit_code)
        raise SystemExit(0)
    raise SystemExit(run_worker(args.job_id, directory=args.directory))
from probe.cli.imports.jobs.errors import JobError, RetryableJobError, UnitRetryJobError, _Interrupted  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.jobs.failure_report import _report_failure  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.jobs.kind import Kind, _dispatch  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.jobs.kinds.transcripts import _serial_lane  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.jobs.store import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    State,
    _ID,
    _check_payload,
    _clean,
    _directory,
    _job_lock,
    _progress_message,
    _read,
    _try_lock,
    _update,
)
from probe.cli.imports.jobs.telemetry import _context, _emit_finished, _emit_stalled  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.jobs.workers import _launch_failed, _process_identity, _reclaim_children  # noqa: E402 -- pieces need each other; the front door loads this one first


if __name__ == "__main__":
    # Hooks import the canonical module, so `-m` runs that module's main, never this copy.
    import importlib

    importlib.import_module("probe.cli.imports.jobs.runner").main()
