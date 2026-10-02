"""Saved import completion survives lifecycle changes; estimates use real work."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from probe.cli import import_jobs as jobs


@pytest.fixture
def saved_job(monkeypatch, tmp_path, request):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))

    class Child:
        pid = os.getpid()

        def wait(self):
            return 0

    monkeypatch.setattr(jobs.subprocess, "Popen", lambda *args, **kwargs: Child())
    return jobs.enqueue(getattr(request, "param", jobs.Kind.TRANSCRIPTS), {"approved": "test"}, "Import")


@pytest.mark.parametrize("exit_kind, expected", [
    ("success", jobs.State.SUCCEEDED),
    ("failure", jobs.State.FAILED),
    ("interrupt", jobs.State.INTERRUPTED),
])
def test_worker_retains_verified_completion_when_it_stops(saved_job, monkeypatch, exit_kind, expected):
    def dispatch(kind, payload, progress):
        progress("Verified conversations", completed=4, total=10,
                 completion_completed=3, completion_total=10,
                 completion_ids=[["codex", "one"], ["codex", "two"], ["codex", "three"]])
        if exit_kind == "failure":
            raise jobs.JobError("Needs a new review.")
        if exit_kind == "interrupt":
            raise jobs._Interrupted
        return ["Finished."]

    monkeypatch.setattr(jobs, "_dispatch", dispatch)
    jobs.run_worker(saved_job["id"])
    stopped = jobs.get_job(saved_job["id"])
    assert stopped["state"] == expected
    assert stopped["progress"]["completed"] == 4
    assert stopped["progress"]["completion_completed"] == 3
    assert stopped["progress"]["completion_total"] == 10
    assert len(stopped["progress"]["completion_ids"]) == 3
    assert "eta_seconds" not in stopped["progress"]


def test_orphan_detection_and_resume_keep_last_measured_work(saved_job, monkeypatch):
    folder = Path(saved_job["log_path"]).parent
    jobs._update(folder, state=jobs.State.RUNNING, progress={
        "completed": 4, "total": 10, "completion_completed": 3, "completion_total": 10,
        "eta_seconds": 70, "eta_updated_at": "2026-09-11T07:00:00Z",
    })
    interrupted = jobs.get_job(saved_job["id"])
    assert interrupted["state"] == jobs.State.INTERRUPTED
    assert interrupted["progress"]["completion_completed"] == 3
    assert "eta_seconds" not in interrupted["progress"]
    resumed = jobs.resume(saved_job["id"])
    assert resumed["state"] == jobs.State.QUEUED
    assert resumed["progress"]["completion_completed"] == 3

    def dispatch(kind, payload, progress):
        started = jobs.get_job(saved_job["id"])
        assert started["progress"]["completion_completed"] == 3
        assert "eta_seconds" not in started["progress"]
        return []

    monkeypatch.setattr(jobs, "_dispatch", dispatch)
    jobs.run_worker(saved_job["id"])


def test_transcript_start_time_begins_after_the_serial_lane_wait(saved_job, monkeypatch):
    folder = Path(saved_job["log_path"]).parent
    lane = folder.parent / "transcripts.lock"
    lane.touch()
    lane_inode = lane.stat().st_ino
    jobs._update(folder, started_at="before-the-wait", progress={"completed": 2, "total": 10})
    flock = jobs.fcntl.flock
    queued = []

    def occupied_lane(descriptor, operation):
        number = descriptor if isinstance(descriptor, int) else descriptor.fileno()
        if os.fstat(number).st_ino == lane_inode:
            if operation == jobs.fcntl.LOCK_EX | jobs.fcntl.LOCK_NB:
                raise BlockingIOError
            if operation == jobs.fcntl.LOCK_EX:
                waiting = jobs._read(folder)
                queued.append(waiting)
                assert waiting["state"] == jobs.State.QUEUED
                assert waiting["started_at"] is None
                assert waiting["progress"]["completed"] == 2
        return flock(descriptor, operation)

    monkeypatch.setattr(jobs.fcntl, "flock", occupied_lane)
    with jobs._serial_lane(saved_job, folder):
        started = jobs._read(folder)
        assert started["state"] == jobs.State.RUNNING
        assert started["started_at"] not in (None, "before-the-wait")
        assert started["progress"]["completed"] == 2
    assert len(queued) == 1


def test_eta_uses_verified_completion_and_excludes_connection_wait(saved_job, monkeypatch):
    clock = [0.0]
    monkeypatch.setattr(jobs.time, "monotonic", lambda: clock[0])
    dispatches = []

    def dispatch(kind, payload, progress):
        dispatches.append(True)
        if len(dispatches) == 1:
            progress("Starting", completed=0, total=10, completion_completed=0, completion_total=10)
            clock[0] = 10
            progress("Some failed", completed=8, total=10, completion_completed=2, completion_total=10)
            measured = jobs.get_job(saved_job["id"])["progress"]
            assert measured["eta_seconds"] == 40  # Eight actual completions at five seconds each.
            assert measured["eta_updated_at"]
            raise jobs.RetryableJobError("Connection lost.")
        progress("Checking receipts", completed=2, total=10, completion_completed=2, completion_total=10)
        assert "eta_seconds" not in jobs.get_job(saved_job["id"])["progress"]
        clock[0] += 10
        progress("Resumed", completed=4, total=10, completion_completed=4, completion_total=10)
        assert jobs.get_job(saved_job["id"])["progress"]["eta_seconds"] == 30
        return []

    def disconnected(delay):
        waiting = jobs.get_job(saved_job["id"])["progress"]
        assert waiting["completion_completed"] == 2
        assert waiting["completed"] == 8
        assert waiting["waiting_for_connection"]
        assert "eta_seconds" not in waiting
        clock[0] += 600

    monkeypatch.setattr(jobs, "_dispatch", dispatch)
    monkeypatch.setattr(jobs.time, "sleep", disconnected)
    assert jobs.run_worker(saved_job["id"]) == 0


def test_receipt_replay_keeps_verified_ids_for_the_same_frozen_job(saved_job, monkeypatch):
    attempts = []

    def dispatch(kind, payload, progress):
        attempts.append(True)
        if len(attempts) == 1:
            progress("Verified", completion_ids=[["codex", "one"], ["codex", "two"]],
                     completion_completed=2, completion_total=3)
            raise jobs.JobError("Paused for attention.")
        progress("Checking saved receipts", completion_ids=[], completion_completed=0, completion_total=3)
        checking = jobs.get_job(saved_job["id"])["progress"]
        assert checking["completion_completed"] == 2
        assert checking["completion_ids"] == [["codex", "one"], ["codex", "two"]]
        assert "eta_seconds" not in checking
        progress("Verified new session", completion_ids=[["codex", "three"]],
                 completion_completed=1, completion_total=3)
        assert jobs.get_job(saved_job["id"])["progress"]["completion_completed"] == 3
        return []

    monkeypatch.setattr(jobs, "_dispatch", dispatch)
    assert jobs.run_worker(saved_job["id"]) == 1
    jobs.resume(saved_job["id"])
    assert jobs.run_worker(saved_job["id"]) == 0
    assert len(jobs.get_job(saved_job["id"])["progress"]["completion_ids"]) == 3


def test_scan_observations_do_not_contribute_verified_ids_to_delivery(saved_job, monkeypatch):
    def dispatch(kind, payload, progress):
        progress("Scanning", phase="scanning", completion_ids=[["codex", "not-delivered"]],
                 completion_completed=1, completion_total=2)
        progress("Starting upload", phase="importing", completion_ids=[],
                 completion_completed=0, completion_total=2)
        importing = jobs.get_job(saved_job["id"])["progress"]
        assert importing["completion_ids"] == []
        assert importing["completion_completed"] == 0
        assert "eta_seconds" not in importing
        return []

    monkeypatch.setattr(jobs, "_dispatch", dispatch)
    assert jobs.run_worker(saved_job["id"]) == 0


@pytest.mark.parametrize("saved_job", [jobs.Kind.FOLDER], indirect=True)
@pytest.mark.parametrize("already_complete", [0, 3])
def test_file_eta_times_new_receipts_after_preparation(saved_job, monkeypatch, already_complete):
    clock = [0.0]
    monkeypatch.setattr(jobs.time, "monotonic", lambda: clock[0])

    def dispatch(kind, payload, progress):
        assert kind == jobs.Kind.FOLDER
        progress("Verifying saved receipts", completion_completed=already_complete, completion_total=10)
        clock[0] = 600
        progress("Reading reviewed files", completed=10, total=10,
                 completion_completed=already_complete, completion_total=10)
        assert "eta_seconds" not in jobs.get_job(saved_job["id"])["progress"]
        clock[0] = 610
        progress("Uploaded first file", completion_completed=already_complete + 1, completion_total=10)
        assert "eta_seconds" not in jobs.get_job(saved_job["id"])["progress"]
        clock[0] = 620
        progress("Uploaded second file", completion_completed=already_complete + 2, completion_total=10)
        measured = jobs.get_job(saved_job["id"])["progress"]
        assert measured["eta_seconds"] == (8 - already_complete) * 10
        return []

    monkeypatch.setattr(jobs, "_dispatch", dispatch)
    assert jobs.run_worker(saved_job["id"]) == 0


def test_scan_phase_never_gets_a_delivery_estimate_and_phase_changes_reset_it(monkeypatch):
    clock = [0.0]
    monkeypatch.setattr(jobs.time, "monotonic", lambda: clock[0])
    estimate = jobs._ProgressEstimate()
    progress = estimate.update({}, {"phase": "scanning", "completed": 0, "total": 10})
    clock[0] = 50
    progress = estimate.update(progress, {"phase": "scanning", "completed": 9, "total": 10})
    assert "eta_seconds" not in progress
    progress = estimate.update(progress, {"phase": "importing"})
    assert "completed" not in progress and "total" not in progress
    progress = estimate.update(progress, {"completed": 0, "total": 10})
    clock[0] = 60
    progress = estimate.update(progress, {"completed": 2, "total": 10})
    assert progress["eta_seconds"] == 40
    progress = estimate.update(progress, {"phase": "scanning", "completed": 1, "total": 2})
    assert "eta_seconds" not in progress


@pytest.mark.parametrize("next_sample", [
    {"completed": 1, "total": 10},  # Receipt reconciliation can correct a count.
    {"completed": 2, "total": 20},  # A new denominator describes different work.
    {"completed": 2, "total": 10, "completion_completed": 2, "completion_total": 10},
])
def test_changed_counter_resets_the_estimate(monkeypatch, next_sample):
    clock = [0.0]
    monkeypatch.setattr(jobs.time, "monotonic", lambda: clock[0])
    estimate = jobs._ProgressEstimate()
    progress = estimate.update({}, {"completed": 0, "total": 10})
    clock[0] = 10
    progress = estimate.update(progress, {"completed": 2, "total": 10})
    assert progress["eta_seconds"] == 40
    assert "eta_seconds" not in estimate.update(progress, next_sample)


def test_status_only_updates_keep_measurements_without_inventing_a_new_eta_sample(monkeypatch):
    clock = [0.0]
    monkeypatch.setattr(jobs.time, "monotonic", lambda: clock[0])
    estimate = jobs._ProgressEstimate()
    progress = estimate.update({}, {"completed": 0, "total": 10})
    clock[0] = 10
    progress = estimate.update(progress, {"completed": 2, "total": 10})
    clock[0] = 100
    assert estimate.update(progress, {}) == progress


@pytest.mark.parametrize("completed,total", [(True, 10), (1, 0), (-1, 10), (11, 10), (float("inf"), 10)])
def test_invalid_counts_never_receive_estimates(completed, total):
    progress = jobs._ProgressEstimate().update({}, {"completed": completed, "total": total})
    assert "eta_seconds" not in progress
