"""Completion summaries combine work without exposing the internal job queue."""

from copy import deepcopy
from datetime import datetime, timezone

import pytest

from probe.cli import import_progress as progress


def session(ident, items, done=0, state="running", **fields):
    return {
        "id": ident, "kind": "transcripts", "state": state,
        "created_at": "2026-09-11T08:00:00Z", "attempt": 1,
        "payload": {"account": {"customer_id": "lab"}, "files": [
            {"agent": "codex", "session_id": item, "sha256": "hash", "size": 10}
            for item in items
        ]},
        "progress": {"completion_completed": done, "completion_total": len(items),
                     "completion_ids": [["codex", item] for item in items[:done]], **fields},
    }


def test_running_and_overlapping_queued_sessions_are_one_unique_total():
    jobs = [session("first", ["a", "b", "c"], 2),
            session("second", ["a", "b", "c", "d"], state="queued")]
    original = deepcopy(jobs)
    result = progress.summarize(jobs, "transcripts")
    assert result.completed == 2 and result.total == 4 and result.fraction == .5
    assert result.state == "Importing"
    assert jobs == original


def test_disjoint_and_different_snapshots_are_not_deduplicated():
    first = session("first", ["a", "b"], 1)
    second = session("second", ["a", "c"], 1)
    second["payload"]["files"][0]["sha256"] = "new-snapshot"
    result = progress.summarize([first, second], "transcripts")
    assert (result.completed, result.total) == (2, 4)


def test_legacy_processing_counters_do_not_claim_completed_imports():
    first = session("first", ["a", "b", "c"], 2)
    first["progress"] = {"completed": 2, "total": 3}
    second = session("second", ["a", "b", "c", "d"], state="queued")
    second["progress"] = {"message": "Queued"}
    result = progress.summarize([first, second], "transcripts")
    assert (result.completed, result.total) == (0, 4) and not result.measured


def test_completion_does_not_disappear_when_a_job_finishes_during_the_queue():
    first = session("first", ["a", "b"], 2, state="succeeded")
    first["finished_at"] = "2026-09-11T09:00:00Z"
    second = session("second", ["a", "b", "c"], state="running")
    result = progress.summarize([first, second], "transcripts")
    assert (result.completed, result.total) == (2, 3)


def test_new_work_does_not_include_unrelated_completed_history():
    old = session("old", ["a", "b"], 2, state="succeeded")
    old["finished_at"] = "2026-09-10T09:00:00Z"
    result = progress.summarize([old, session("new", ["c"])], "transcripts")
    assert (result.completed, result.total) == (0, 1)


@pytest.mark.parametrize("state", ["failed", "interrupted", "succeeded"])
def test_stopped_file_imports_stay_visible(state):
    job = {"id": "f", "kind": "folder", "state": state,
           "payload": {"targets": ["a", "b", "c"]},
           "progress": {"completion_completed": 1, "completion_total": 3}}
    result = progress.summarize([job], "folder")
    assert result.title == "File imports" and result.total == 3
    assert result.state == ("Partially complete" if state == "succeeded" else "Needs attention")


@pytest.mark.parametrize("done", [0, 1])
def test_a_successful_byte_limited_job_does_not_claim_unfinished_sessions(done):
    job = session("limited", ["a", "b", "c"], done, state="succeeded")
    result = progress.summarize([job], "transcripts")
    assert result.state == "Partially complete"
    assert (result.completed, result.total, result.fraction) == (done, 3, done / 3)


@pytest.mark.parametrize("later_items, expected", [(["d"], (2, 4)), (["b", "c"], (2, 2))])
def test_later_success_only_completes_the_same_approved_session_snapshots(later_items, expected):
    limited = session("limited", ["a", "b", "c"], 1, state="succeeded")
    later = session("later", later_items, len(later_items), state="succeeded")
    later.update(created_at="2026-09-11T10:00:00Z", finished_at="2026-09-11T11:00:00Z")
    result = progress.summarize([limited, later], "transcripts")
    assert (result.completed, result.total) == expected
    assert result.state == ("Complete" if expected[0] == expected[1] else "Partially complete")
    assert result.fraction == expected[0] / expected[1]


@pytest.mark.parametrize("state", ["succeeded", "canceled"])
def test_completed_partial_snapshot_does_not_keep_old_history_in_new_work(state):
    limited = session("limited", ["a", "b"], 1, state="succeeded")
    completed = session("completed", ["a", "b"], 2, state=state)
    completed["finished_at"] = "2026-09-11T09:00:00Z"
    new = session("new", ["c"])
    new["created_at"] = "2026-09-12T08:00:00Z"
    result = progress.summarize([limited, completed, new], "transcripts")
    assert (result.completed, result.total, result.state) == (0, 1, "Importing")


def test_partial_file_job_is_counted_once_with_later_success():
    jobs = [{"id": name, "kind": "folder", "state": "succeeded",
             "created_at": f"2026-09-11T0{hour}:00:00Z", "finished_at": "2026-09-11T10:00:00Z",
             "progress": {"completion_completed": done, "completion_total": 3}}
            for name, hour, done in (("partial", 8, 1), ("finished", 9, 3))]
    result = progress.summarize(jobs, "folder")
    assert (result.completed, result.total, result.state) == (4, 6, "Partially complete")


def test_no_file_import_has_an_explicit_empty_state():
    result = progress.summarize([session("a", ["one"])], "folder")
    assert (result.title, result.state, result.fraction) == ("File imports", "Not started", 0)


@pytest.mark.parametrize("kind", ["transcripts", "folder"])
def test_canceled_import_does_not_keep_overview_work_unfinished(kind):
    canceled = session("canceled", ["a", "b", "c"], 1, state="canceled")
    canceled["kind"] = kind
    original = deepcopy(canceled)
    result = progress.summarize([canceled], kind)
    assert result.state == "Not started" and not result.active

    running = session("running", ["a", "b"], 1)
    running["kind"] = kind
    result = progress.summarize([canceled, running], kind)
    assert (result.state, result.completed, result.total) == ("Importing", 1, 2)
    assert canceled == original


@pytest.mark.parametrize("fields", [
    {"phase": "scanning", "completed": 3, "total": 9},
    {"message": "Reading reviewed files", "completed": 10, "total": 10},
    {"completed": 10, "total": 10, "completion_completed": 2, "completion_total": 10},
])
def test_scanning_and_preparation_do_not_fill_the_delivery_bar(fields):
    job = {"id": "f", "kind": "folder", "state": "running", "progress": fields}
    result = progress.summarize([job], "folder")
    expected = fields.get("completion_completed", 0)
    assert result.completed == expected
    assert result.fraction == (expected / 10 if expected else 0)


def test_active_job_never_claims_final_completion():
    result = progress.summarize([session("a", ["one"], 1)], "transcripts")
    assert result.state == "Finishing" and result.fraction < 1


def test_eta_uses_completion_delta_and_resets_on_wait_or_retry():
    estimates = progress.Estimates()
    job = session("a", list("abcdefghij"), 1)
    assert estimates.rate(job, 100) is None
    job["progress"]["completion_completed"] = 3
    assert estimates.rate(job, 160) == pytest.approx(2 / 60)
    job["progress"]["waiting_for_connection"] = True
    assert estimates.rate(job, 170) is None
    job["progress"].pop("waiting_for_connection")
    assert estimates.rate(job, 200) is None
    job["progress"]["completion_completed"] = 4
    assert estimates.rate(job, 230) == pytest.approx(1 / 30)
    job["attempt"] = 2
    assert estimates.rate(job, 240) is None


def test_category_eta_includes_remaining_queued_sessions_without_double_counting(monkeypatch):
    first = session("first", list("abcd"), 1)
    second = session("queued", list("abcdef"), state="queued")
    estimates = progress.Estimates()
    monkeypatch.setattr(progress.time, "monotonic", lambda: 100)
    assert progress.summarize([first, second], "transcripts", estimates).eta is None
    first["progress"].update(completion_completed=2, completion_ids=[["codex", "a"], ["codex", "b"]])
    monkeypatch.setattr(progress.time, "monotonic", lambda: 160)
    result = progress.summarize([first, second], "transcripts", estimates)
    assert result.eta == 240  # four unique sessions left, one per minute


def test_file_eta_waits_for_delivery_pace_after_preparation():
    job = {"id": "f", "kind": "folder", "state": "running", "progress": {
        "completion_completed": 3, "completion_total": 10,
    }}
    estimates = progress.Estimates()
    assert estimates.rate(job, 100) is None
    job["progress"]["completion_completed"] = 4
    assert estimates.rate(job, 700) is None  # Long preparation before first receipt.
    job["progress"]["completion_completed"] = 5
    assert estimates.rate(job, 710) == .1


def test_parallel_file_eta_waits_for_the_slowest_import():
    jobs = [{"id": name, "kind": "folder", "state": "running", "progress": {
        "completion_completed": 10, "completion_total": total,
    }} for name, total in (("slow", 100), ("fast", 20))]

    class Rates:
        def rate(self, job, now):
            return 1 if job["id"] == "slow" else 10

    assert progress.summarize(jobs, "folder", Rates()).eta == 90


@pytest.mark.parametrize("kind", ["transcripts", "folder"])
@pytest.mark.parametrize("finished, visible", [
    ("2026-09-11T11:59:59Z", False),
    ("2026-09-11T12:00:00Z", False),
    ("2026-09-11T12:00:01Z", True),
    ("2026-09-11T05:00:01-07:00", True),
])
def test_completed_overview_expires_at_24_hours(kind, finished, visible):
    job = session("finished", ["a", "b"], 2, state="succeeded")
    job.update(kind=kind, finished_at=finished)
    original = deepcopy(job)
    cutoff = datetime(2026, 9, 11, 12, tzinfo=timezone.utc)
    result = progress.summarize([job], kind, completed_since=cutoff)
    assert result.state == ("Complete" if visible else "Not started")
    assert result.total == (2 if visible else 0)
    assert job == original
    # Detailed/historical callers still see the saved completion.
    assert progress.summarize([job], kind).state == "Complete"


@pytest.mark.parametrize("state", ["running", "queued", "failed", "interrupted", "succeeded"])
def test_unfinished_work_never_expires_from_overview(state):
    job = session("unfinished", ["a", "b"], 1, state=state)
    job["finished_at"] = "2026-09-10T12:00:00Z"
    cutoff = datetime(2026, 9, 11, 12, tzinfo=timezone.utc)
    result = progress.summarize([job], "transcripts", completed_since=cutoff)
    assert result.state != "Not started"
    assert (result.completed, result.total) == (1, 2)


def test_expired_success_keeps_old_partial_sessions_settled():
    limited = session("limited", ["a", "b"], 1, state="succeeded")
    finished = session("finished", ["a", "b"], 2, state="succeeded")
    for job in (limited, finished):
        job["finished_at"] = "2026-09-11T09:00:00Z"
    cutoff = datetime(2026, 9, 11, 12, tzinfo=timezone.utc)
    assert progress.summarize([limited, finished], "transcripts", completed_since=cutoff).state == "Not started"
    new = session("new", ["c"])
    new["created_at"] = "2026-09-12T08:00:00Z"
    result = progress.summarize([limited, finished, new], "transcripts", completed_since=cutoff)
    assert (result.completed, result.total, result.state) == (0, 1, "Importing")


def test_completion_without_a_parseable_timestamp_is_retained():
    job = session("legacy", ["a"], 1, state="succeeded")
    job.update(created_at="invalid", updated_at=None, finished_at="invalid")
    cutoff = datetime(2026, 9, 11, 12, tzinfo=timezone.utc)
    assert progress.summarize([job], "transcripts", completed_since=cutoff).state == "Complete"
    job["updated_at"] = "2026-09-11T09:00:00Z"
    assert progress.summarize([job], "transcripts", completed_since=cutoff).state == "Not started"
