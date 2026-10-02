"""Real folder-worker observations reach the TUI without counting scans as uploads."""

from copy import deepcopy

import pytest

from probe.cli import backfill_import, import_jobs as jobs, import_jobs_ui as ui, import_progress
from tests.test_backfill_auto_import import automatic, queued, _enqueue  # noqa: F401
from tests.test_backfill_background import background_harness, enqueue_job  # noqa: F401


@pytest.mark.parametrize("mode", ["reviewed", "automatic"])
def test_final_file_verification_keeps_approved_completion_in_the_live_tui(
    request, monkeypatch, mode,
):
    if mode == "automatic":
        h = request.getfixturevalue("automatic")
        job = _enqueue(h)
    else:
        h, requests = request.getfixturevalue("background_harness")
        h.run(background=True)
        monkeypatch.setenv("XDG_STATE_HOME", str(h.root / "jobs"))
        monkeypatch.setattr(jobs, "_launch", lambda folder: jobs._read(folder))
        job = enqueue_job("folder", requests[0], "Approved folder")

    # The final census sees new work too. Its denominator must not replace the
    # single approved file's upload count, or make that receipt disappear.
    h.after_units = lambda: (h.folder / "later.py").write_text("not approved\n")
    saved = []
    save = jobs._save

    def observe(folder, value):
        save(folder, value)
        saved.append(deepcopy(value))

    monkeypatch.setattr(jobs, "_save", observe)
    assert jobs.run_worker(job["id"]) == 0
    rechecks = [value for value in saved if
                value["progress"]["message"].startswith("Re-checking file contents")]
    assert rechecks, "the final census must report through the durable worker"
    for value in rechecks:
        assert value["progress"]["total"] == 2
        summary = import_progress.summarize([value], "folder")
        assert (summary.completed, summary.total) == (1, 1)
        assert summary.state == "Finishing" and summary.fraction < 1
        assert "Scanning" not in "\n".join(ui._started_summary(value))
    finished = jobs.get_job(job["id"])
    assert finished["progress"]["phase"] == "importing"
    assert import_progress.summarize([finished], "folder").state == "Complete"
    assert "Complete" in ui._started_summary(finished)[0]
    assert "Scanning" not in ui._started_summary(finished)[0]
    assert len(h.remote.calls) == 1 and h.report()["new"] == ["later.py"]


@pytest.mark.parametrize("state,label,waiting", [
    (jobs.State.SUCCEEDED, "Complete", False),
    (jobs.State.FAILED, "Needs attention", False),
    (jobs.State.INTERRUPTED, "Interrupted", False),
    (jobs.State.RUNNING, "Waiting for connection", True),
])
def test_legacy_scan_metadata_cannot_override_worker_status(state, label, waiting):
    job = {"id": "old-worker", "kind": "folder", "state": state, "label": "Folder",
           "progress": {"phase": "scanning", "stage": "assign", "completed": 3, "total": 3,
                        "completion_completed": 1, "completion_total": 1,
                        "waiting_for_connection": waiting}}
    heading = ui._started_summary(job)[0]
    assert label in heading and "Scanning" not in heading


def test_file_census_counts_are_not_labeled_as_agent_steps():
    job = {"id": "census", "kind": "folder", "state": "running", "label": "Folder",
           "progress": {"phase": "scanning", "stage": "assign", "stage_completed": 1,
                        "stage_total": 2, "completed": 4, "total": 5}}

    # A worker retry can return from classification to the file census while
    # staying in the scanning phase. Old classification units must be cleared.
    def persist(message, **fields):
        job["progress"] = {**jobs._ProgressEstimate().update(job["progress"], fields),
                           "message": message}

    backfill_import._census_progress(persist, "Verifying file contents")(
        completed=120, total=1154, reused=0,
    )
    text = "\n".join(ui._started_summary(job))
    assert "Scanning" in text and "120 of 1,154" in text and "steps" not in text
    assert import_progress.summarize([job], "folder").completed == 0
