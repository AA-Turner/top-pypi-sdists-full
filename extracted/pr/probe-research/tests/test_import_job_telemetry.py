"""Whether an approved import ever FINISHED -- the half the wizard cannot see.

`backfill.summary` and `transcripts.summary` fire when a lane hands work to a
detached worker, and report it as queued at 0% coverage. That is honest and it
is also the end of what the wizard knows: the import runs in another process,
minutes or hours later, and until now nothing reported how it ended.

The worker is the one place both lanes converge, so it carries the funnel. It
replays the APPROVING session off the job record, because a completion in its
own session is a number nobody can join to the person who asked for it.
"""

from __future__ import annotations

import os

import pytest

from probe.cli import import_jobs as jobs
from probe.cli import telemetry as tm


@pytest.fixture
def queued(monkeypatch, tmp_path):
    """Jobs land on disk; nothing is actually spawned."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("PROBE_BASE_URL", "https://api.research.prbe.ai")
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    launches = []

    class Child:
        pid = os.getpid()

        def wait(self):
            return 0

    monkeypatch.setattr(
        jobs.subprocess, "Popen", lambda argv, **kwargs: launches.append(argv) or Child(),
    )
    return launches


@pytest.fixture(autouse=True)
def captured(monkeypatch):
    """The queue seam, always -- `queued` turns telemetry ON for this module,
    and a test here that forgot to ask for the records would otherwise start a
    real sender thread."""
    records: list[dict] = []
    monkeypatch.setattr(tm, "_sender", None)
    monkeypatch.setattr(tm, "_flush_registered", True)
    monkeypatch.setattr(tm._Sender, "start", lambda self: None)
    monkeypatch.setattr(tm._Sender, "put", lambda self, rec: records.append(rec))
    return records


@pytest.fixture
def approving(monkeypatch):
    """A wizard session, as the process that approves an import would have."""
    context = tm.TelemetryContext(
        session_id="wizardsession", via=tm.Via.WIZARD, invoked_by=tm.InvokedBy.HUMAN,
    )
    monkeypatch.setattr(tm, "_current", context)
    return context


def _events(records):
    return [record["event"] for record in records]


def _props(records, event):
    return next(record["properties"] for record in records if record["event"] == event)


def _enqueue(kind=jobs.Kind.TRANSCRIPTS, approval="review-1"):
    return jobs.enqueue(kind, {"approval_id": approval}, "Approved conversations")


def _release(job):
    """Drop the stubbed worker's pid, which is this test process's own.

    `clear_all` refuses to tear down a job running in the caller's process --
    correctly -- and the fake Popen hands back `os.getpid()`.
    """
    jobs._update(jobs._directory(job["id"]), pid=None, launch_pid=None, pid_identity=None)


# --- the approval -----------------------------------------------------------


@pytest.mark.parametrize("kind", [jobs.Kind.TRANSCRIPTS, jobs.Kind.FOLDER])
def test_an_approval_becoming_durable_work_is_counted(queued, captured, approving, kind):
    job = _enqueue(kind)
    enqueued = _props(captured, tm.EVENT_IMPORT_JOB_ENQUEUED)
    assert enqueued["kind"] == kind
    assert enqueued["job_id"] == job["id"]
    assert enqueued["resumed"] is False
    assert enqueued["session_id"] == "wizardsession"


def test_a_repeat_of_the_same_approval_is_not_a_second_enqueue(queued, captured, approving):
    first = _enqueue()
    captured.clear()
    assert _enqueue()["id"] == first["id"]
    assert _events(captured) == []


def test_the_approving_session_rides_the_record_not_the_payload(queued, approving):
    """The payload's hash IS the job id. A session id in there would give the
    same approval a different identity per run and defeat deduplication."""
    job = _enqueue()
    saved = jobs.get_job(job["id"])
    assert saved["origin"]["session_id"] == "wizardsession"
    assert saved["origin"]["via"] == "wizard"
    assert "session_id" not in str(saved["payload"])
    assert jobs._identity(saved["kind"], saved["payload"]) == job["id"]


def test_an_approval_made_with_telemetry_off_records_no_session(queued, monkeypatch):
    monkeypatch.setenv("PROBE_TELEMETRY", "off")
    monkeypatch.setattr(tm, "_current", None)
    job = _enqueue()
    assert jobs.get_job(job["id"])["origin"] is None


# --- the worker's verdict ---------------------------------------------------


def test_a_finished_import_reports_under_the_session_that_approved_it(
    queued, captured, approving, monkeypatch,
):
    """The whole point: the completion has to be joinable to the approval, and
    the worker is a new process that inherits nothing."""
    job = _enqueue()
    monkeypatch.setattr(jobs, "_dispatch", lambda *args: ["Finished."])
    captured.clear()
    monkeypatch.setattr(tm, "_current", None)  # a fresh process knows nothing
    assert jobs.run_worker(job["id"]) == 0
    done = _props(captured, tm.EVENT_IMPORT_JOB_FINISHED)
    assert done["outcome"] == tm.ImportJobOutcome.SUCCEEDED
    assert done["session_id"] == "wizardsession"
    assert done["via"] == "wizard" and done["invoked_by"] == "human"
    assert done["kind"] == jobs.Kind.TRANSCRIPTS
    assert done["attempt"] == 1
    assert "duration_seconds" in done


def test_a_failed_import_names_the_kind_of_failure_and_never_its_text(
    queued, captured, approving, monkeypatch,
):
    job = _enqueue()

    def refuse(*args):
        raise jobs.JobError("the reviewed folder /home/someone/secret moved")

    monkeypatch.setattr(jobs, "_dispatch", refuse)
    captured.clear()
    assert jobs.run_worker(job["id"]) == 1
    done = _props(captured, tm.EVENT_IMPORT_JOB_FINISHED)
    assert done["outcome"] == tm.ImportJobOutcome.FAILED
    assert done["failure_kind"] == "refused"
    assert "secret" not in str(done), "lane prose can name a path"


def test_an_unexpected_crash_reports_its_type_not_its_message(
    queued, captured, approving, monkeypatch,
):
    def explode(*args):
        raise ZeroDivisionError("/home/someone/secret")

    job = _enqueue()
    monkeypatch.setattr(jobs, "_dispatch", explode)
    captured.clear()
    assert jobs.run_worker(job["id"]) == 1
    done = _props(captured, tm.EVENT_IMPORT_JOB_FINISHED)
    assert done["failure_kind"] == "ZeroDivisionError"
    assert "secret" not in str(done)


def test_an_interrupted_worker_is_separable_from_a_failure(
    queued, captured, approving, monkeypatch,
):
    def interrupt(*args):
        raise KeyboardInterrupt

    job = _enqueue()
    monkeypatch.setattr(jobs, "_dispatch", interrupt)
    captured.clear()
    assert jobs.run_worker(job["id"]) == 130
    assert _props(captured, tm.EVENT_IMPORT_JOB_FINISHED)["outcome"] == (
        tm.ImportJobOutcome.INTERRUPTED
    )


def test_a_canceled_import_is_a_decision_not_an_interruption(
    queued, captured, approving, monkeypatch,
):
    """A cancel reaches a running worker as a signal, which the worker's own
    terminal path can only read as an interruption. One stopped import must
    produce ONE terminal event, and it must be the one saying a person chose
    this -- otherwise a deliberate stop is filed as a laptop closing."""
    job = _enqueue()
    _release(job)  # no live worker: the stubbed Popen hands back our own pid
    captured.clear()
    assert jobs.cancel(job["id"])["state"] == jobs.State.CANCELED
    finished = [row for row in captured if row["event"] == tm.EVENT_IMPORT_JOB_FINISHED]
    assert len(finished) == 1
    assert finished[0]["properties"]["outcome"] == tm.ImportJobOutcome.CANCELED
    assert finished[0]["properties"]["session_id"] == "wizardsession"


def test_a_worker_signalled_by_a_cancel_stays_quiet(queued, captured, approving, monkeypatch):
    """The worker's interrupted path runs for a cancel too. It must not also
    report, or one import lands in the funnel twice, as two different things."""
    job = _enqueue()
    folder = jobs._directory(job["id"])

    def interrupt(*args):
        jobs._update(folder, cancel_requested=True)
        raise KeyboardInterrupt

    monkeypatch.setattr(jobs, "_dispatch", interrupt)
    captured.clear()
    assert jobs.run_worker(job["id"]) == 130
    assert [row for row in captured if row["event"] == tm.EVENT_IMPORT_JOB_FINISHED] == []


# --- stalls -----------------------------------------------------------------


def test_a_worker_waiting_for_a_connection_says_so_once_not_per_retry(
    queued, captured, approving, monkeypatch,
):
    """A disconnected laptop retries forever. The stall is a LEVEL, and an
    event per retry turns one bad afternoon into hundreds of them."""
    attempts = {"n": 0}

    def flaky(*args):
        attempts["n"] += 1
        if attempts["n"] < 4:
            raise jobs.RetryableJobError("connection reset")
        return ["Finished."]

    job = _enqueue()
    monkeypatch.setattr(jobs, "_dispatch", flaky)
    monkeypatch.setattr(jobs.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(jobs, "_reclaim_children", lambda folder: None)
    captured.clear()
    assert jobs.run_worker(job["id"]) == 0
    stalls = [row for row in captured if row["event"] == tm.EVENT_IMPORT_JOB_STALLED]
    assert len(stalls) == 1, "three retries, one report"
    assert stalls[0]["properties"]["reason"] == tm.ImportJobStall.WAITING_FOR_CONNECTION
    assert stalls[0]["properties"]["network_retries"] == 1
    assert _props(captured, tm.EVENT_IMPORT_JOB_FINISHED)["network_retries"] == 3


def test_a_worker_that_vanished_is_reported_by_whoever_reads_the_record_next(
    queued, captured, approving, monkeypatch,
):
    """Nothing emits this at the moment it happens: the process that would
    have is the one that died."""
    job = _enqueue()
    folder = jobs._directory(job["id"])
    jobs._update(folder, state=jobs.State.RUNNING, pid=None, pid_identity=None)
    captured.clear()
    assert jobs.get_job(job["id"])["state"] == jobs.State.INTERRUPTED
    stalled = _props(captured, tm.EVENT_IMPORT_JOB_STALLED)
    assert stalled["reason"] == tm.ImportJobStall.WORKER_VANISHED
    assert stalled["session_id"] == "wizardsession"
    # A LEVEL, reported on the transition only: an interrupted job is re-read
    # on every status refresh, and a per-read event would fire hundreds of times.
    captured.clear()
    jobs.get_job(job["id"])
    assert _events(captured) == []


# --- work thrown away -------------------------------------------------------


def test_clearing_imports_says_how_much_unfinished_work_went_with_them(
    queued, captured, approving, monkeypatch,
):
    """Uninstall and the wizard's Exit both clear approved imports. What was
    discarded is unreadable a moment later, so the count has to ride here."""
    monkeypatch.setattr(jobs, "_dispatch", lambda *args: ["Finished."])
    done = _enqueue(approval="finished")
    jobs.run_worker(done["id"])
    _release(done)  # success clears `pid`, but `launch_pid` outlives it
    _release(_enqueue(jobs.Kind.FOLDER, approval="still-going"))
    captured.clear()
    assert jobs.clear_all() == 2
    cleared = _props(captured, tm.EVENT_IMPORT_JOB_CLEARED)
    assert cleared["jobs"] == 2 and cleared["unfinished"] == 1
    assert cleared["kinds"] == ["folder", "transcripts"]


def test_clearing_nothing_reports_nothing(queued, captured, approving):
    assert jobs.clear_all() == 0
    assert _events(captured) == []


# --- the vocabulary ---------------------------------------------------------


def test_every_outcome_the_worker_can_report_is_a_declared_one():
    """The worker passes bare strings, because the pinned source tree it runs
    from may not carry `telemetry.py` at all. Nothing else pins the two
    together, so a rename on one side would silently split the funnel."""
    import re
    from pathlib import Path

    source = Path(jobs.__file__).read_text()
    outcomes = set(re.findall(r'_emit_finished\([^,]+,\s*"([a-z_]+)"', source))
    reasons = set(re.findall(r'_emit_stalled\([^,]+,\s*"([a-z_]+)"', source))
    assert outcomes and reasons, "the regex stopped matching the call sites"
    assert outcomes <= {value.value for value in tm.ImportJobOutcome}
    assert reasons <= {value.value for value in tm.ImportJobStall}


def test_telemetry_is_never_load_bearing_for_the_worker(queued, monkeypatch):
    """A worker runs from the pinned copy of `probe/` that existed when its
    approval was made, and that tree carries only what the lanes need. An
    unconditional import here did not merely stop reporting the import -- it
    stopped the import."""
    monkeypatch.setattr(jobs, "_telemetry", lambda: None)
    monkeypatch.setattr(jobs, "_dispatch", lambda *args: ["Finished."])
    job = _enqueue()
    assert jobs.get_job(job["id"])["origin"] is None
    assert jobs.run_worker(job["id"]) == 0
    assert jobs.get_job(job["id"])["state"] == jobs.State.SUCCEEDED
    _release(job)
    assert jobs.clear_all() == 1
