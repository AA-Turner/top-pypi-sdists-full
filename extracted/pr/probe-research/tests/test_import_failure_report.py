"""Telling the PERSON their import stopped, not just telling us.

`import_job.finished` reaches PostHog, which reaches the team. Nothing reached
the researcher: the worker is detached, its terminal is usually gone by the time
it fails, and the only surface that knew was an import screen nobody had a
reason to reopen. One real import ended `2619/3857 finalized, 166 failed` and
sat there unnoticed.

So a terminal FAILURE also asks the server to email the account that approved
the job. The properties worth pinning are the ones that make that safe to leave
running unattended:

  * it never turns a crash loop into an inbox (the durable per-job dedupe),
  * it never becomes the reason an import failed (every error is swallowed),
  * and it never fires for an outcome a person already knows about.
"""

from __future__ import annotations

import os

import pytest

from probe.cli import import_jobs as jobs


@pytest.fixture
def queued(monkeypatch, tmp_path):
    """Jobs land on disk; nothing is actually spawned, nothing is sent."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("PROBE_BASE_URL", "https://api.research.prbe.ai")
    monkeypatch.setenv("PROBE_TELEMETRY", "off")

    class Child:
        pid = os.getpid()

        def wait(self):
            return 0

    monkeypatch.setattr(jobs.subprocess, "Popen", lambda argv, **kwargs: Child())


@pytest.fixture
def reports(monkeypatch) -> list[tuple[str, str, dict]]:
    """Replace the one function that touches the network."""
    posted: list[tuple[str, str, dict]] = []
    monkeypatch.setattr(
        jobs, "_post_failure_report",
        lambda context, job_id, body: posted.append((context, job_id, body)),
    )
    return posted


def _enqueue(kind=jobs.Kind.TRANSCRIPTS, payload=None):
    """An approval whose payload names the saved account, as a real one does."""
    if payload is None:
        payload = {"approval_id": "review-1", "account": {"context": "default"}}
    return jobs.enqueue(kind, payload, "Approved conversations")


def _fail(monkeypatch, message="Session import is incomplete: 2619/3857 finalized."):
    def boom(*args, **kwargs):
        raise jobs.JobError(message)

    monkeypatch.setattr(jobs, "_dispatch", boom)


# --- the report itself -------------------------------------------------------


def test_a_failed_import_asks_the_server_to_mail_its_owner(queued, reports, monkeypatch):
    job = _enqueue()
    _fail(monkeypatch)
    assert jobs.run_worker(job["id"]) == 1

    assert len(reports) == 1
    context, job_id, body = reports[0]
    assert (context, job_id) == ("default", job["id"])
    assert body["outcome"] == "failed"
    assert body["kind"] == jobs.Kind.TRANSCRIPTS
    assert body["reason"].startswith("Session import is incomplete")
    assert body["failure_kind"] == "refused"
    assert body["attempt"] == 1
    assert body["machine"]


def test_the_folder_lane_names_its_context_too(queued, reports, monkeypatch):
    """The two lanes spell the saved account differently; both must report."""
    job = _enqueue(jobs.Kind.FOLDER, {"scope": {"backend": "x"}, "context": "work"})
    _fail(monkeypatch, "The selected folder is unavailable.")
    assert jobs.run_worker(job["id"]) == 1
    assert [r[0] for r in reports] == ["work"]


def test_an_import_with_no_saved_context_reports_nothing_and_still_fails_cleanly(
    queued, reports, monkeypatch,
):
    """There is nothing to authenticate with. That is not a crash."""
    job = _enqueue(payload={"approval_id": "review-1"})
    _fail(monkeypatch)
    assert jobs.run_worker(job["id"]) == 1
    assert reports == []


# --- outcomes that must stay silent ------------------------------------------


def test_a_successful_import_reports_nothing(queued, reports, monkeypatch):
    job = _enqueue()
    monkeypatch.setattr(jobs, "_dispatch", lambda *args: ["Finished."])
    assert jobs.run_worker(job["id"]) == 0
    assert reports == []


def test_an_interrupted_import_reports_nothing(queued, reports, monkeypatch):
    """The person stopped it, or their machine did. They know."""
    def stop(*args, **kwargs):
        raise KeyboardInterrupt

    job = _enqueue()
    monkeypatch.setattr(jobs, "_dispatch", stop)
    assert jobs.run_worker(job["id"]) == 130
    assert reports == []


def test_a_connection_stall_reports_nothing(queued, reports, monkeypatch):
    """A disconnected laptop retries forever and never reaches a terminal
    failure. Mailing on the stall would mail every overnight import."""
    attempts = []

    def flaky(*args, **kwargs):
        attempts.append(1)
        if len(attempts) < 3:
            raise jobs.RetryableJobError("Waiting for connection.")
        return ["Finished."]

    job = _enqueue()
    monkeypatch.setattr(jobs, "_dispatch", flaky)
    monkeypatch.setattr(jobs.time, "sleep", lambda seconds: None)
    assert jobs.run_worker(job["id"]) == 0
    assert reports == []


# --- the dedupe --------------------------------------------------------------


def test_the_same_failure_seen_twice_mails_once(queued, reports, monkeypatch):
    """A job relaunched by recovery must not become a mail loop."""
    job = _enqueue()
    _fail(monkeypatch)
    assert jobs.run_worker(job["id"]) == 1
    folder = jobs._directory(job["id"])

    # The same terminal state, observed again without a new attempt.
    assert jobs._report_failure(folder, jobs._read(folder), failure_kind="refused") is False
    assert jobs._report_failure(folder, jobs._read(folder), failure_kind="refused") is False
    assert len(reports) == 1


def test_a_fresh_attempt_at_the_same_wall_mails_again(queued, reports, monkeypatch):
    """Somebody fixed the cause, resumed, and hit it anyway. That is news."""
    job = _enqueue()
    _fail(monkeypatch)
    assert jobs.run_worker(job["id"]) == 1
    jobs._update(jobs._directory(job["id"]), pid=None, launch_pid=None, pid_identity=None)
    jobs.resume(job["id"])
    assert jobs.run_worker(job["id"]) == 1

    assert len(reports) == 2
    assert [body["attempt"] for _, _, body in reports] == [1, 2]


def test_a_report_that_never_left_is_retried_by_the_next_observation(
    queued, reports, monkeypatch,
):
    """The stamp goes on AFTER the POST returns. Stamping first would turn one
    unreachable server into a failure nobody is ever told about."""
    job = _enqueue()
    _fail(monkeypatch)
    folder = jobs._directory(job["id"])

    def offline(context, job_id, body):
        raise OSError("network is unreachable")

    monkeypatch.setattr(jobs, "_post_failure_report", offline)
    assert jobs.run_worker(job["id"]) == 1
    assert reports == []
    assert "notified" not in jobs._read(folder)

    monkeypatch.setattr(
        jobs, "_post_failure_report",
        lambda context, job_id, body: reports.append((context, job_id, body)),
    )
    assert jobs._report_failure(folder, jobs._read(folder), failure_kind="refused") is True
    assert len(reports) == 1


# --- it can never be the reason an import failed -----------------------------


def test_a_broken_reporter_cannot_break_the_worker(queued, monkeypatch):
    job = _enqueue()
    _fail(monkeypatch)

    def explode(*args, **kwargs):
        raise RuntimeError("the notifier itself is broken")

    monkeypatch.setattr(jobs, "_post_failure_report", explode)
    # Same exit code and same durable state as if the reporter did not exist.
    assert jobs.run_worker(job["id"]) == 1
    saved = jobs.get_job(job["id"])
    assert saved["state"] == jobs.State.FAILED
    assert saved["error"].startswith("Session import is incomplete")


def test_the_reported_reason_is_the_scrubbed_job_record(queued, reports, monkeypatch):
    """Never the raw exception. `_clean` is what stands between an authored
    refusal and whatever a formatted transport error would have carried."""
    job = _enqueue()
    _fail(monkeypatch, "Bad\x00news\x07 about your import.")
    assert jobs.run_worker(job["id"]) == 1
    reason = reports[0][2]["reason"]
    assert reason == jobs.get_job(job["id"])["error"]
    assert "\x00" not in reason and "\x07" not in reason
