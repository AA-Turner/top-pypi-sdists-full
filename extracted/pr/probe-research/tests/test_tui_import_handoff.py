"""A queued session import can be watched or left without changing its worker."""

from copy import deepcopy
from types import SimpleNamespace

import pytest

from probe.cli import backfill_transcripts as bt
from probe.cli import import_job_messages, import_jobs, import_jobs_ui as ui, tui
from tests.test_backfill_transcripts import lane as lane
from tests.test_tui_review import _run

pytestmark = pytest.mark.tui


@pytest.fixture
def saved_import(monkeypatch):
    job = {
        "id": "a" * 32, "kind": "transcripts", "label": "Sessions from Claude Code",
        "state": import_jobs.State.RUNNING, "error": None,
        "progress": {"message": "Reading approved sessions", "completion_completed": 1, "completion_total": 4},
    }
    reads, mutations = [], []

    def get_job(job_id):
        reads.append(job_id)
        return deepcopy(job)

    def observe_mutation(*args, **kwargs):
        mutations.append((args, kwargs))
        return deepcopy(job)

    monkeypatch.setattr(import_jobs, "get_job", get_job)
    for name in ("enqueue", "resume", "recover_jobs", "spawn_child"):
        monkeypatch.setattr(import_jobs, name, observe_mutation)
    return SimpleNamespace(job=job, reads=reads, mutations=mutations)


def test_automatic_scanning_handoff_can_be_left_before_upload(monkeypatch, saved_import):
    saved_import.job.update(
        kind="folder", label="Folder · Odyssey", payload={"auto_approve": True},
        progress={"phase": "scanning", "stage": "survey", "completed": 2, "total": 9,
                  "message": "Reading samples"},
    )
    result, frames = _run(
        monkeypatch, ["\r"], width=80, height=24,
        onboarding=lambda: ["Install Probe · Step 4 of 4", tui.progress_bar(0.75)],
        render=lambda: ui.show_started_import(saved_import.job),
    )
    text = "\n".join(frames[0])
    assert "Scanning" in text and "2/9 steps" in text and "Continue setup" in text
    assert "Scanning and importing continue in the background." in text
    assert "Existing imports" in text
    assert result["id"] == saved_import.job["id"] and saved_import.mutations == []


@pytest.mark.parametrize("onboarding", [False, True])
@pytest.mark.parametrize("kind", [import_jobs.Kind.TRANSCRIPTS, import_jobs.Kind.FOLDER])
@pytest.mark.parametrize("key", ["\r", "\x1b", "\x03"], ids=["enter", "escape", "ctrl-c"])
def test_leaving_started_import_keeps_the_saved_worker_untouched(monkeypatch, saved_import, onboarding, kind, key):
    saved_import.job["kind"] = kind
    original = deepcopy(saved_import.job)
    returned = []
    interrupted = []

    def handoff():
        try:
            returned.append(ui.show_started_import(original))
        except KeyboardInterrupt:
            interrupted.append(True)

    _, frames = _run(
        monkeypatch, [key], height=40, render=handoff,
        onboarding=(lambda: ["Install Probe · Step 4 of 4", tui.progress_bar(0.75)]) if onboarding else None,
    )
    text = "\n".join(frames[0])
    subject = "Folder" if kind == import_jobs.Kind.FOLDER else "Session"
    assert f"{subject} import status" in text and "Importing" in text
    assert "W&B" not in text
    assert "The import continues in the background." in text
    assert ("Continue setup" in text) is onboarding
    assert "stay here to watch it finish" in text
    assert "Existing imports" in text
    assert interrupted == ([True] if key == "\x03" else [])
    assert returned == ([] if key == "\x03" else [original])
    if returned:
        assert returned[0] is not original
    assert saved_import.job == original
    assert saved_import.reads and set(saved_import.reads) == {original["id"]}
    assert saved_import.mutations == []


def test_unreadable_started_import_retains_the_last_saved_snapshot(monkeypatch, saved_import):
    original = deepcopy(saved_import.job)

    def unreadable(job_id):
        raise import_jobs.JobError("The saved import job could not be read.")

    monkeypatch.setattr(import_jobs, "get_job", unreadable)
    answer, frames = _run(
        monkeypatch, ["\r"], height=40, render=lambda: ui.show_started_import(original),
    )
    text = "\n".join(frames[0])
    assert "its current status is unavailable" in text
    assert "The saved import job could not be read." in text
    assert "check Existing imports later" in text
    assert answer == original and saved_import.mutations == []


def test_handoff_returns_a_fresh_snapshot_after_navigation(monkeypatch, saved_import):
    original = deepcopy(saved_import.job)

    def review(title, lines, choices, **kwargs):
        assert callable(lines) and "Importing" in "\n".join(lines())
        saved_import.job["state"] = import_jobs.State.SUCCEEDED
        return tui.BACK

    monkeypatch.setattr(tui, "review", review)
    result = ui.show_started_import(original)
    assert result["state"] == import_jobs.State.SUCCEEDED
    assert original["state"] == import_jobs.State.RUNNING
    assert saved_import.mutations == []


@pytest.mark.parametrize("state", [import_jobs.State.RUNNING, import_jobs.State.SUCCEEDED])
def test_approved_folder_delivery_has_folder_status_and_no_additional_review(monkeypatch, saved_import, state):
    saved_import.job.update(kind=import_jobs.Kind.FOLDER, label="Folder: research", state=state)
    if state == import_jobs.State.SUCCEEDED:
        saved_import.job["progress"]["completion_completed"] = 4

    def review(title, lines, choices, **kwargs):
        assert title == "Folder import status" and callable(lines)
        assert choices == [("Continue", ui.Navigation.CONTINUE)]
        current = "\n".join(lines())
        assert "W&B" not in current
        assert "Folder: research" in current
        if state == import_jobs.State.SUCCEEDED:
            assert "Your folder import is complete." in current
        else:
            assert "Importing" in current and "continues in the background" in current
        return tui.BACK

    monkeypatch.setattr(tui, "review", review)
    assert ui.show_started_import(deepcopy(saved_import.job)) == saved_import.job
    assert saved_import.mutations == []


@pytest.mark.parametrize("state", [import_jobs.State.SUCCEEDED, import_jobs.State.FAILED])
def test_transcript_lane_reports_the_state_returned_by_the_post_enqueue_handoff(lane, monkeypatch, state):
    events = []
    approved = {"files": ["approved-session"]}
    queued = {"id": "queued-session-job", "state": import_jobs.State.RUNNING}
    latest = {**queued, "state": state, "error": "Account needs attention." if state == "failed" else None}
    original_report = import_job_messages.enqueue_report
    monkeypatch.setattr(bt, "_background_payload", lambda *args, **kwargs: approved)

    def review(*args, **kwargs):
        events.append("approval")
        return "import"

    def enqueue(kind, payload, label):
        events.append("enqueue")
        assert kind == "transcripts" and payload is approved
        return queued

    def handoff(job):
        events.append("handoff")
        assert job is queued
        return latest

    def report(job, label):
        events.append("report")
        assert job is latest
        return original_report(job, label)

    monkeypatch.setattr(tui, "review", review)
    monkeypatch.setattr(import_jobs, "enqueue", enqueue)
    monkeypatch.setattr(ui, "show_started_import", handoff)
    monkeypatch.setattr(import_job_messages, "enqueue_report", report)
    seen, lines = lane(interactive=True, background=True)
    assert seen == {} and events == ["approval", "enqueue", "handoff", "report"]
    text = "\n".join(lines)
    assert ("already complete" if state == "succeeded" else "needs attention") in text
    assert "continues in the background" not in text


def test_yes_queues_transcripts_without_opening_the_handoff(lane, monkeypatch):
    calls = []
    monkeypatch.setattr(bt, "_background_payload", lambda *args, **kwargs: {"approved": True})
    monkeypatch.setattr(tui, "review", lambda *args, **kwargs: pytest.fail("unexpected approval prompt"))
    monkeypatch.setattr(ui, "show_started_import", lambda *args: pytest.fail("unexpected handoff"))

    def enqueue(kind, payload, label):
        calls.append((kind, payload))
        return {"id": "yes-job", "state": import_jobs.State.QUEUED}

    monkeypatch.setattr(import_jobs, "enqueue", enqueue)
    seen, lines = lane(interactive=True, background=True, yes=True)
    assert seen == {} and calls == [("transcripts", {"approved": True})]
    assert "Session import queued: yes-job" in lines


def test_partial_finished_import_keeps_its_actual_completion(monkeypatch, saved_import):
    saved_import.job.update(state=import_jobs.State.SUCCEEDED, progress={
        "completion_completed": 0, "completion_total": 4, "completion_ids": [],
    })

    def review(title, lines, choices, **kwargs):
        shown = lines()
        assert "Partially complete" in shown[0]
        assert shown[0].style == "class:instruction"
        assert shown[1] == f"{tui.progress_bar(0)}  0/4"
        assert "some items unfinished" in "\n".join(shown)
        assert "Your session import is complete" not in "\n".join(shown)
        return ui.Navigation.CONTINUE

    monkeypatch.setattr(tui, "review", review)
    ui.show_started_import(saved_import.job)
    assert saved_import.mutations == []
