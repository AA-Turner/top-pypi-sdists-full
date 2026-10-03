"""The installer and main menu observe the same durable import jobs."""

import asyncio
from copy import deepcopy
from datetime import datetime, timezone
import importlib
from types import SimpleNamespace

import pytest
from prompt_toolkit.application import create_app_session
from prompt_toolkit.data_structures import Size
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput

from probe.cli import import_jobs, import_jobs_ui as ui, tui
from tests.test_setup_wizard import _caps, isolate  # noqa: F401 -- isolated wizard state

# Every test here drives a prompt_toolkit app session and asserts on the frames
# it rendered. That is a finished-render measurement, so it belongs in the serial
# lane with the pty tests -- see the `tui` marker in agent/pyproject.toml.
pytestmark = pytest.mark.tui


def _choices(choices):
    return choices() if callable(choices) else choices


def _job(job_id, kind, label, state):
    return {
        "id": job_id, "kind": kind, "label": label, "state": state,
        "progress": {"message": "Reading approved work", "completion_total": 4,
                     "completion_completed": 4 if state == import_jobs.State.SUCCEEDED else 1},
        "error": None, "started_at": "2026-09-09T10:00:00Z", "finished_at": None,
        "report": [], "log_path": f"/tmp/import-tests/{job_id}/output.log",
    }


@pytest.fixture
def jobs(monkeypatch):
    saved = [
        _job("a" * 32, import_jobs.Kind.TRANSCRIPTS, "Sessions · Claude Code and Codex",
             import_jobs.State.RUNNING),
        _job("b" * 32, import_jobs.Kind.FOLDER, "Folder · research", import_jobs.State.FAILED),
    ]
    saved[1]["error"] = "Restore the approved folder before resuming."
    monkeypatch.setattr(import_jobs, "list_jobs", lambda: saved)
    monkeypatch.setattr(import_jobs, "get_job", lambda job_id: next(
        job for job in saved if job["id"] == job_id
    ))
    monkeypatch.setattr(import_jobs, "recover_jobs", lambda: [])

    def forbidden(*args, **kwargs):
        pytest.fail("Viewing imports must not enqueue or explicitly restart an import")

    monkeypatch.setattr(import_jobs, "enqueue", forbidden)
    monkeypatch.setattr(import_jobs, "resume", forbidden)
    monkeypatch.setattr(import_jobs, "cancel", forbidden)
    return saved


@pytest.mark.parametrize("onboarding", [False, True])
def test_monitor_shows_both_import_kinds_and_returns_to_menu_without_stopping_them(
    monkeypatch, jobs, onboarding
):
    original = deepcopy(jobs)
    recovery = []
    monkeypatch.setattr(import_jobs, "recover_jobs", lambda: recovery.append(True))

    def review(title, lines, choices, **kwargs):
        assert title == "Your imports" and callable(lines)
        text = "\n".join(lines())
        assert "Session imports" in text and "Claude Code and Codex" not in text
        assert "File imports" in text and "Folder · research" not in text
        assert "Importing" in text and "Needs attention" in text
        assert "Restore the approved folder" not in text
        assert _choices(choices) == [
            ("View details or resume", ui.Navigation.DETAILS),
            ("Return to main menu", ui.Navigation.MENU),
        ]
        return ui.Navigation.MENU

    monkeypatch.setattr(tui, "review", review)
    assert ui.show_imports(onboarding=onboarding) is ui.Navigation.MENU
    assert jobs == original
    assert recovery == [True]


@pytest.mark.parametrize("has_jobs", [False, True])
def test_monitor_keeps_verbose_notices_behind_the_details_action(monkeypatch, jobs, has_jobs):
    notices = ["No local coding sessions were found.", "Folder import needs attention: sign in again."]
    if not has_jobs:
        jobs.clear()
    pages = []

    def review(title, lines, choices, **kwargs):
        pages.append(title)
        rendered = lines() if callable(lines) else lines
        if title == "Your imports":
            assert not any(notice in rendered for notice in notices)
            assert "Session import" in "\n".join(rendered)
            assert "File imports" in "\n".join(rendered)
            return ui.Navigation.DETAILS if len(pages) == 1 else ui.Navigation.MENU
        assert title == ("Existing imports" if has_jobs else "Import details")
        assert all(notice in rendered for notice in notices)
        return ui.Navigation.BACK

    monkeypatch.setattr(tui, "review", review)
    assert ui.show_imports(onboarding=True, notices=notices) is ui.Navigation.MENU
    assert len(pages) == 3


def test_expired_completion_stays_in_details_but_not_overview(monkeypatch, jobs):
    class Clock:
        @staticmethod
        def now(_zone):
            return datetime(2026, 9, 12, 12, tzinfo=timezone.utc)

    monkeypatch.setattr(ui, "datetime", Clock)
    completed = jobs[1]
    completed.update(state=import_jobs.State.SUCCEEDED, finished_at="2026-09-10T12:00:00Z", error=None)
    completed["progress"].update(completion_completed=1154, completion_total=1154)
    original = deepcopy(jobs)
    text = "\n".join(ui.active_progress_lines())
    assert "Session imports · Importing" in text
    assert "File imports · Complete" not in text and "1,154" not in text
    assert "1,154" not in "\n".join(ui._all_imports())
    seen_details = []

    def review(title, lines, choices, **kwargs):
        if title == "Existing imports":
            assert any(value == completed["id"] for _, value in _choices(choices))
            return completed["id"]
        seen_details.append(title)
        assert "1154/1154" in "\n".join(lines())
        return ui.Navigation.BACK

    monkeypatch.setattr(tui, "review", review)
    ui._choose_import()
    assert seen_details == [completed["label"]]
    assert jobs == original


def test_active_progress_combines_session_jobs_and_keeps_file_bar(monkeypatch, jobs):
    jobs[1].update(state=import_jobs.State.RUNNING, progress={"completion_completed": 2, "completion_total": 9})
    waiting = _job("c" * 32, import_jobs.Kind.TRANSCRIPTS, "2372 sessions from Codex", import_jobs.State.QUEUED)
    waiting["progress"] = {"message": "Queued."}
    waiting["payload"] = {"files": [{}] * 2372}
    jobs.insert(0, waiting)
    original = deepcopy(jobs)
    lines = ui.active_progress_lines()
    text = "\n".join(lines)
    assert len(lines) == 5
    assert "Session imports" in lines[0] and "Importing" in lines[0]
    assert "1/2,376" in lines[1] and lines[1].style == "class:pointer"
    assert "File imports" in lines[3] and "2/9" in lines[4]
    assert sum("─" in line or "━" in line for line in lines) == 2
    assert all(job["id"] not in text for job in jobs)
    assert "Reading approved work" not in text
    assert jobs == original
    assert ui.active_progress_lines([]) == []


def test_folder_scan_advances_to_importing_in_the_same_live_bar(monkeypatch, jobs):
    folder = jobs[1]
    folder.update(state=import_jobs.State.RUNNING, progress={
        "phase": "scanning", "completed": 3, "total": 9,
        "message": "Reading samples", "stage": "survey",
    })
    lines = ui.active_progress_lines()
    assert len(lines) == 5
    assert "File imports" in lines[3] and "Scanning" in lines[3]
    assert "0 files complete" in lines[4] and "━" not in lines[4]
    assert "Scanning" in "\n".join(ui._summary(folder))
    folder["progress"] = {"phase": "importing", "completion_completed": 5, "completion_total": 10}
    updated = ui.active_progress_lines()
    assert len(updated) == 5 and "Importing" in updated[3]
    assert "5/10" in updated[4] and "steps" not in updated[4]
    folder["progress"]["waiting_for_connection"] = True
    assert "Waiting for connection" in ui.active_progress_lines()[3]


def test_compact_monitor_stays_at_two_bars_with_many_jobs_and_failures(monkeypatch, jobs):
    monkeypatch.setattr(tui, "columns", lambda: 80)
    monkeypatch.setattr(tui, "rows", lambda: 24)
    jobs.extend(_job(str(index) * 32, import_jobs.Kind.TRANSCRIPTS, f"Earlier import {index}",
                     import_jobs.State.QUEUED) for index in range(3, 8))
    jobs.append(_job("f" * 32, import_jobs.Kind.TRANSCRIPTS, "Failed session import", import_jobs.State.FAILED))
    with tui.onboarding(lambda: ["Install Probe · Step 4 of 4", tui.progress_bar(0.75)]):
        lines = ui._all_imports(onboarding=True)
    text = "\n".join(lines)
    assert len(lines) == 5
    assert "needs attention" in text and "+5 more" not in text
    assert sum("─" in line or "━" in line for line in lines) == 2
    assert all(len(line) <= tui.CONTENT_WIDTH for line in lines)
    assert "File imports" in text and "Needs attention" in text


def test_completed_history_is_one_complete_category(monkeypatch, jobs):
    jobs[0]["state"] = import_jobs.State.SUCCEEDED
    jobs[0]["progress"]["completion_completed"] = 4
    jobs.append(_job("c" * 32, import_jobs.Kind.TRANSCRIPTS, "Older sessions", import_jobs.State.SUCCEEDED))
    text = "\n".join(ui._all_imports())
    assert text.count("Session imports · Complete") == 1 and "100%" in text
    assert "Older sessions" not in text and "1/4" not in text.split("File imports")[0]


@pytest.mark.parametrize("width,height", [(80, 24), (120, 40)])
def test_two_import_bars_and_navigation_fit_the_onboarding_monitor(monkeypatch, jobs, width, height):
    from tests.test_tui_review import _row, _run

    jobs[1].update(state=import_jobs.State.RUNNING, progress={"completion_completed": 6, "completion_total": 10})
    waiting = _job("c" * 32, import_jobs.Kind.TRANSCRIPTS, "2372 sessions from Codex", import_jobs.State.QUEUED)
    waiting["progress"] = {"message": "Queued."}
    jobs.append(waiting)
    answer, frames = _run(
        monkeypatch, ["\x1b"], width=width, height=height,
        onboarding=lambda: ["Install Probe · Step 4 of 4", tui.progress_bar(0.75)],
        render=lambda: ui.show_imports(onboarding=True, notices=["Long plan detail that belongs behind Details."]),
    )
    assert answer is ui.Navigation.MENU
    frame = frames[0]
    text = "\n".join(frame)
    assert _row(frame, "Session imports") < _row(frame, "File imports")
    assert sum("─" in line or "━" in line for line in frame) == 3  # includes onboarding bar
    assert "1 sessions complete" in text and "6/10" in text and "+1 more" not in text
    assert _row(frame, "View details") < _row(frame, "Return to main menu")
    assert "Exit — imports continue" not in text
    assert "esc menu" in text and "Reopen:" not in text
    assert _row(frame, "esc menu") > _row(frame, "View details")
    assert "Long plan detail" not in text


def test_opening_details_and_resuming_retains_the_original_job_id(monkeypatch, jobs):
    target = jobs[1]
    target["report"] = ["One approved file is still pending."]
    resumed = []
    calls = []

    def resume(job_id):
        resumed.append(job_id)
        assert job_id == target["id"]
        target.update(state=import_jobs.State.RUNNING, error=None)
        return target

    def review(title, lines, choices, **kwargs):
        calls.append(title)
        text = "\n".join(lines() if callable(lines) else lines)
        if len(calls) == 1:
            return ui.Navigation.DETAILS
        if title == "Existing imports":
            assert {job["id"] for job in jobs}.issubset({value for _, value in _choices(choices)})
            return target["id"]
        if title == target["label"]:
            assert target["id"] in text and target["log_path"] in text
            assert "One approved file is still pending." in text
            if not resumed:
                assert any(value is ui.Navigation.RESUME for _, value in _choices(choices))
                return ui.Navigation.RESUME
            assert "Importing" in text
            assert not any(value is ui.Navigation.RESUME for _, value in _choices(choices))
            return ui.Navigation.BACK
        return ui.Navigation.MENU

    monkeypatch.setattr(import_jobs, "resume", resume)
    monkeypatch.setattr(tui, "review", review)
    assert ui.show_imports() is ui.Navigation.MENU
    assert resumed == [target["id"]]
    assert calls == ["Your imports", "Existing imports", target["label"],
                     target["label"], "Your imports"]


@pytest.mark.parametrize("job_index", [0, 1])
def test_copy_log_path_from_actions_or_document_keeps_details_open(monkeypatch, jobs, job_index):
    import subprocess
    from tests.test_tui_review import _run

    target = jobs[job_index]
    target["log_path"] = "/Users/researcher/研究 project/" + "long path/" * 8 + "$(literal)/output.log"
    original = deepcopy(jobs)
    copied = []
    for name in ("SSH_CONNECTION", "SSH_TTY"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(tui.sys, "platform", "darwin")
    monkeypatch.setattr(tui.shutil, "which", lambda name: name if name == "pbcopy" else None)

    def copy(command, **kwargs):
        assert command == ["pbcopy"] and not kwargs.get("shell")
        copied.append(kwargs["input"].decode("utf-8"))

    monkeypatch.setattr(subprocess, "run", copy)
    review = tui.review

    def open_details(title, lines, choices, **kwargs):
        if title == "Existing imports":
            return target["id"]
        return review(title, lines, choices, **kwargs)

    monkeypatch.setattr(tui, "review", open_details)
    _, frames = _run(
        monkeypatch, ["c", "\t", "C", "\x1b"], width=80, height=24,
        render=ui._choose_import,
    )
    assert copied == [target["log_path"]] * 2
    assert "c copy log path" in "\n".join(frames[0])
    assert "Log path copied." in "\n".join(frames[1])
    assert jobs == original


@pytest.mark.parametrize("term,message", [
    ("xterm-256color", "Copy sent; paste to check."),
    ("dumb", "Copy unavailable; select text."),
])
def test_narrow_copy_footer_keeps_terminal_or_unavailable_feedback(monkeypatch, term, message):
    from tests.test_tui_review import _run

    monkeypatch.setenv("TERM", term)
    monkeypatch.setenv("SSH_TTY", "/dev/test-terminal")
    monkeypatch.setattr(tui.shutil, "which", lambda _name: None)
    answer, frames = _run(
        monkeypatch, ["c", "\x1b"], width=40, height=24,
        render=lambda: tui.review(
            "Import details", ["Log: /home/researcher/output.log"], [("Back", ui.Navigation.BACK)],
            copy_text="/home/researcher/output.log", copy_label="log path",
            instruction="↑↓ · enter · c copy log path · tab read · esc back",
        ),
    )
    assert answer is tui.BACK
    assert "c copy" in "\n".join(frames[0])
    assert message in "\n".join(frames[1])


def test_job_that_fails_while_details_are_open_can_resume_without_leaving(monkeypatch, jobs):
    target = jobs[0]
    resumed = []
    detail_visits = []

    def resume(job_id):
        resumed.append(job_id)
        target.update(state=import_jobs.State.RUNNING, error=None)
        return target

    def review(title, lines, choices, **kwargs):
        if title == "Existing imports":
            return target["id"]
        detail_visits.append(title)
        assert title == target["label"]
        if len(detail_visits) == 1:
            assert "Importing" in "\n".join(lines())
            assert not any(value is ui.Navigation.RESUME for _, value in _choices(choices))
            target.update(state=import_jobs.State.FAILED, error="Worker could not finish.")
            assert "Needs attention" in "\n".join(lines())
            assert "Worker could not finish." in "\n".join(lines())
            assert any(value is ui.Navigation.RESUME for _, value in _choices(choices))
            return ui.Navigation.RESUME
        assert "Importing" in "\n".join(lines())
        return ui.Navigation.BACK

    monkeypatch.setattr(import_jobs, "resume", resume)
    monkeypatch.setattr(tui, "review", review)
    ui._choose_import()
    assert resumed == [target["id"]]
    assert len(detail_visits) == 2


@pytest.mark.parametrize("state,progress", [
    (import_jobs.State.QUEUED, {}),
    (import_jobs.State.RUNNING, {}),
    (import_jobs.State.RUNNING, {"waiting_for_connection": True}),
    (import_jobs.State.RUNNING, {"phase": "scanning"}),
    (import_jobs.State.SUCCEEDED, {}),
])
def test_active_or_complete_job_does_not_offer_resume(monkeypatch, jobs, state, progress):
    target = jobs[0]
    target["state"] = state
    target["progress"].update(progress)
    original = deepcopy(target)
    detail_visits = []

    def review(title, lines, choices, **kwargs):
        if title == "Existing imports":
            return target["id"]
        detail_visits.append(title)
        assert not any(value is ui.Navigation.RESUME for _, value in _choices(choices))
        return ui.Navigation.BACK

    monkeypatch.setattr(tui, "review", review)
    ui._choose_import()
    assert target == original
    assert len(detail_visits) == 1


def test_live_detail_removes_resume_and_focuses_back_when_worker_restarts(monkeypatch, jobs):
    from tests.test_tui_review import _run

    target = jobs[1]
    review = tui.review

    def open_details(title, lines, choices, **kwargs):
        if title == "Existing imports":
            return target["id"]
        return review(title, lines, choices, **kwargs)

    monkeypatch.setattr(tui, "review", open_details)
    _, frames = _run(
        monkeypatch, ["", lambda: target.update(state=import_jobs.State.RUNNING, error=None), "\r"],
        width=100, height=32, render=ui._choose_import,
    )
    assert "Resume import" in "\n".join(frames[0])
    running = "\n".join(frames[1])
    assert "Importing" in running and "Resume import" not in running
    assert "Cancel import" in running and "» Back to all imports" in running


def test_live_detail_adds_resume_when_worker_stops(monkeypatch, jobs):
    from tests.test_tui_review import _run

    target = jobs[0]
    resumed = []
    review = tui.review
    keys = ["", lambda: target.update(state=import_jobs.State.FAILED), "\x1b[A", "\r"]

    def resume(job_id):
        resumed.append(job_id)
        target.update(state=import_jobs.State.RUNNING)
        return target

    def open_details(title, lines, choices, **kwargs):
        if title == "Existing imports":
            return target["id"]
        if resumed:
            keys[:] = ["\x1b"]
        return review(title, lines, choices, **kwargs)

    monkeypatch.setattr(import_jobs, "resume", resume)
    monkeypatch.setattr(tui, "review", open_details)
    _, frames = _run(monkeypatch, keys, width=100, height=32, render=ui._choose_import)
    assert "Resume import" not in "\n".join(frames[0])
    failed = "\n".join(frames[1])
    assert "Needs attention" in failed and "Resume import" in failed
    assert "» Cancel import" in failed
    assert resumed == [target["id"]]


@pytest.mark.parametrize("state", [import_jobs.State.RUNNING, import_jobs.State.SUCCEEDED,
                                  import_jobs.State.FAILED])
def test_stale_resume_selection_cannot_restart_active_complete_or_canceling_import(monkeypatch, jobs, state):
    target = jobs[1]
    visits = []

    def review(title, lines, choices, **kwargs):
        if title == "Existing imports":
            return target["id"]
        visits.append(title)
        if len(visits) == 1:
            assert ("Resume import", ui.Navigation.RESUME) in _choices(choices)
            target.update(state=state, cancel_requested=state == import_jobs.State.FAILED)
            return ui.Navigation.RESUME
        assert not any(value is ui.Navigation.RESUME for _, value in _choices(choices))
        return ui.Navigation.BACK

    monkeypatch.setattr(tui, "review", review)
    ui._choose_import()
    assert len(visits) == 2


@pytest.mark.parametrize("job_index", [0, 1])
def test_cancel_from_detail_menu_keeps_progress_and_other_imports(monkeypatch, jobs, job_index):
    from tests.test_tui_review import _run

    target = jobs[job_index]
    other = deepcopy(jobs[1 - job_index])
    progress = deepcopy(target["progress"])
    canceled = []

    def cancel(job_id):
        canceled.append(job_id)
        target.update(state=import_jobs.State.CANCELED, error=None)
        target["progress"]["message"] = "Import canceled. Already imported work is kept."
        return target

    monkeypatch.setattr(import_jobs, "cancel", cancel)
    review = tui.review
    keys = (["\x1b[B"] if job_index == 1 else []) + ["\r"]

    def open_details(title, lines, choices, **kwargs):
        if title == "Existing imports":
            return target["id"]
        if canceled:
            # Exercise Escape after cancellation, independently of row order.
            keys[:] = ["\x1b"]
        return review(title, lines, choices, **kwargs)

    monkeypatch.setattr(tui, "review", open_details)
    _, frames = _run(
        monkeypatch, keys, width=90, height=30,
        render=ui._choose_import,
    )
    rendered = "\n".join("\n".join(frame) for frame in frames)
    assert "Cancel import" in rendered and "Canceled" in rendered
    assert "Resume import" in rendered
    assert canceled == [target["id"]]
    assert jobs[1 - job_index] == other
    assert target["progress"]["completion_completed"] == progress["completion_completed"]


@pytest.mark.parametrize("state", [import_jobs.State.QUEUED, import_jobs.State.RUNNING,
                                  import_jobs.State.FAILED, import_jobs.State.INTERRUPTED])
@pytest.mark.parametrize("job_index", [0, 1])
def test_unfinished_import_details_offer_cancel(monkeypatch, jobs, state, job_index):
    target = jobs[job_index]
    target.update(state=state)
    target["progress"]["waiting_for_connection"] = True

    def review(title, lines, choices, **kwargs):
        if title == "Existing imports":
            return target["id"]
        expected = [("Cancel import", ui.Navigation.CANCEL), ("Back to all imports", ui.Navigation.BACK)]
        if state in {import_jobs.State.FAILED, import_jobs.State.INTERRUPTED}:
            expected.insert(0, ("Resume import", ui.Navigation.RESUME))
        assert _choices(choices) == expected
        assert "W&B" not in "\n".join(lines())
        return ui.Navigation.BACK

    monkeypatch.setattr(tui, "review", review)
    ui._choose_import()


@pytest.mark.parametrize("state", [import_jobs.State.SUCCEEDED, import_jobs.State.CANCELED])
@pytest.mark.parametrize("job_index", [0, 1])
def test_terminal_import_details_do_not_offer_cancel(monkeypatch, jobs, state, job_index):
    target = jobs[job_index]
    target.update(state=state)

    def review(title, lines, choices, **kwargs):
        if title == "Existing imports":
            return target["id"]
        expected = [("Back to all imports", ui.Navigation.BACK)]
        if state == import_jobs.State.CANCELED:
            expected.insert(0, ("Resume import", ui.Navigation.RESUME))
        assert _choices(choices) == expected
        assert "W&B" not in "\n".join(lines())
        return ui.Navigation.BACK

    monkeypatch.setattr(tui, "review", review)
    ui._choose_import()


def test_canceled_import_can_resume_only_when_chosen(monkeypatch, jobs):
    target = jobs[0]
    target.update(state=import_jobs.State.CANCELED)
    resumed = []

    def resume(job_id):
        resumed.append(job_id)
        target.update(state=import_jobs.State.RUNNING)
        return target

    def review(title, lines, choices, **kwargs):
        if title == "Existing imports":
            return target["id"]
        if not resumed:
            assert ("Resume import", ui.Navigation.RESUME) in _choices(choices)
            return ui.Navigation.RESUME
        assert "Importing" in "\n".join(lines())
        return ui.Navigation.BACK

    monkeypatch.setattr(import_jobs, "resume", resume)
    monkeypatch.setattr(tui, "review", review)
    ui._choose_import()
    assert resumed == [target["id"]]


def test_finishing_while_cancel_is_selected_keeps_the_completed_result(monkeypatch, jobs):
    target = jobs[0]
    visits = []

    def review(title, lines, choices, **kwargs):
        if title == "Existing imports":
            return target["id"]
        visits.append(title)
        if len(visits) == 1:
            assert ("Cancel import", ui.Navigation.CANCEL) in _choices(choices)
            target.update(state=import_jobs.State.SUCCEEDED, report=["All sessions imported."])
            target["progress"].update(completion_completed=4)
            return ui.Navigation.CANCEL
        assert "Complete" in "\n".join(lines())
        assert "All sessions imported." in lines()
        assert not any(value == ui.Navigation.CANCEL for _, value in _choices(choices))
        return ui.Navigation.BACK

    monkeypatch.setattr(tui, "review", review)
    ui._choose_import()
    assert len(visits) == 2


def test_cancel_failure_shows_reason_without_claiming_success(monkeypatch, jobs):
    target = jobs[0]
    original = deepcopy(target)
    pages = []

    def cancel(job_id):
        assert job_id == target["id"]
        raise import_jobs.JobError("An import worker is still stopping. Try again.")

    def review(title, lines, choices, **kwargs):
        pages.append(title)
        if title == "Existing imports":
            return target["id"]
        if title == target["label"]:
            return ui.Navigation.CANCEL
        assert "still stopping" in "\n".join(lines)
        return ui.Navigation.BACK

    monkeypatch.setattr(import_jobs, "cancel", cancel)
    monkeypatch.setattr(tui, "review", review)
    ui._choose_import()
    assert pages[-1] == "Import needs attention"
    assert target == original


def test_unreadable_job_opens_an_error_page_without_a_resume_action(monkeypatch, jobs):
    calls = []

    def unreadable(job_id):
        raise import_jobs.JobError("The saved import job could not be read.")

    def review(title, lines, choices, **kwargs):
        calls.append(title)
        if title == "Existing imports":
            return jobs[1]["id"]
        assert title == "Import needs attention"
        assert "could not be read" in "\n".join(lines)
        assert not any(value is ui.Navigation.RESUME for _, value in _choices(choices))
        return ui.Navigation.BACK

    monkeypatch.setattr(import_jobs, "get_job", unreadable)
    monkeypatch.setattr(tui, "review", review)
    ui._choose_import()
    assert calls == ["Existing imports", "Import needs attention"]


def test_live_detail_displays_an_unreadable_record_notice_without_crashing(monkeypatch, jobs):
    def unreadable(job_id):
        raise import_jobs.JobError("The saved import job could not be read.")

    def review(title, lines, choices, **kwargs):
        if title == "Existing imports":
            return jobs[0]["id"]
        assert "Importing" in "\n".join(lines())
        monkeypatch.setattr(import_jobs, "get_job", unreadable)
        rendered = "\n".join(lines())
        assert "Import details are unavailable" in rendered
        assert "could not be read" in rendered
        assert "saved job was retained" in rendered
        assert _choices(choices) == [("Back to all imports", ui.Navigation.BACK)]
        return ui.Navigation.BACK

    monkeypatch.setattr(tui, "review", review)
    ui._choose_import()


def test_monitor_refreshes_progress_without_a_keypress_or_page_change(monkeypatch, jobs):
    width, height = 100, 32

    class Output(DummyOutput):
        def get_size(self):
            return Size(rows=height, columns=width)

    monkeypatch.setattr(tui, "interactive", lambda: True)
    monkeypatch.setattr(tui, "columns", lambda: width)
    monkeypatch.setattr(tui, "rows", lambda: height)
    frames = []
    applications = []
    original_ask = tui.ask

    with create_pipe_input() as pipe, create_app_session(input=pipe, output=Output()):
        def ask(question, **kwargs):
            app = question.application
            applications.append(app)

            def snapshot():
                screen = app.renderer._last_screen
                return [
                    "".join(screen.data_buffer[y][x].char for x in range(width)).rstrip()
                    for y in range(height)
                ]

            async def drive():
                await asyncio.sleep(0.05)
                frames.append(snapshot())
                jobs[0]["progress"] = {
                    "message": "Upload receipts verified", "completion_completed": 4, "completion_total": 4,
                }
                jobs[0]["state"] = import_jobs.State.SUCCEEDED
                # Do not invalidate the application: its periodic refresh must
                # notice a worker's new durable status without navigation.
                for _ in range(25):
                    await asyncio.sleep(0.1)
                    if "✔ Complete" in "\n".join(snapshot()):
                        break
                frames.append(snapshot())
                pipe.send_text("\x1b[B\r")
                await asyncio.sleep(0.1)
                if not app.is_done:
                    app.exit(exception=AssertionError("Return to main menu did not leave the imports monitor"))

            app.pre_run_callables.append(lambda: app.create_background_task(drive()))
            return original_ask(question, **kwargs)

        monkeypatch.setattr(tui, "ask", ask)
        assert ui.show_imports(onboarding=True) is ui.Navigation.MENU

    assert len(applications) == 1
    assert "1/4" in "\n".join(frames[0])
    assert "Session imports · Complete" in "\n".join(frames[1])
    assert "Upload receipts verified" not in "\n".join(frames[1])
    assert tui.progress_bar(1) in "\n".join(frames[1])
    for label in ("Your imports", "Return to main menu", "View details", "↑↓"):
        before = next(i for i, line in enumerate(frames[0]) if label in line)
        after = next(i for i, line in enumerate(frames[1]) if label in line)
        assert before == after, label


@pytest.mark.parametrize("navigation", [ui.Navigation.MENU, ui.Navigation.EXIT])
def test_main_menu_import_action_uses_the_shared_monitor(monkeypatch, jobs, navigation):
    import typer
    from probe.cli import actions, setup

    cli_main = importlib.import_module("probe.cli.main")
    calls = []
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(ui, "show_imports", lambda **kwargs: calls.append(kwargs) or navigation)

    def dispatch():
        return cli_main._run_wizard_action(
            actions.Action.IMPORT_JOBS, caps=_caps(), base_now="https://example.invalid",
            yes=False, tracking=None, capture=None, auto_update=None, agent_rules=None,
            uninstall=False, configured=True,
        )

    if navigation is ui.Navigation.EXIT:
        with pytest.raises(typer.Exit) as stopped:
            dispatch()
        assert stopped.value.exit_code == 0
    else:
        assert dispatch() is None
    assert calls == [{}]


@pytest.mark.parametrize("open_dashboard", [True, False])
def test_guided_install_finishes_with_dashboard_handoff_after_both_import_choices(
    monkeypatch, jobs, open_dashboard
):
    from typer.testing import CliRunner
    from probe.cli import actions, bootstrap, doctor, onboarding_complete, plugin_cli, setup

    cli_main = importlib.import_module("probe.cli.main")
    events = []
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_monitor_test")
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda source: source == "claude_code")
    monkeypatch.setattr(doctor, "collect", lambda: _caps(claude_available=True))
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(setup, "run_confirm_install", lambda *args, **kwargs: True)
    monkeypatch.setattr(setup, "run_backfill_offer", lambda *args, **kwargs: set(setup.BackfillChoice))
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *args, **kwargs: None)
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: pytest.fail(
        "Finishing setup must not add a press-enter pause"
    ))
    monkeypatch.setattr(setup, "run_action_menu", lambda *args, **kwargs: events.append("menu"))

    def apply(action, **kwargs):
        assert action in {actions.Action.CONFIGURE, actions.Action.BACKFILL}
        events.append(action.value)
        if action is actions.Action.CONFIGURE:
            kwargs["installation_completion"].remaining = 0
        return ["Folder import needs attention"] if action is actions.Action.BACKFILL else []

    def sessions(**kwargs):
        assert kwargs["background"] is True
        events.append("sessions")
        return ["Session import queued"]

    def handoff(_base):
        assert "Install Probe" in "\n".join(tui.onboarding_header())
        events.append("dashboard")
        return open_dashboard

    monkeypatch.setattr(cli_main, "_run_wizard_action", apply)
    monkeypatch.setattr(cli_main, "_import_past_sessions", sessions)
    monkeypatch.setattr(ui, "show_imports", lambda **k: pytest.fail("setup has its own final page"))
    monkeypatch.setattr(onboarding_complete, "show", handoff)
    result = CliRunner().invoke(cli_main.app, ["install", "--agent", "claude"])
    assert result.exit_code == 0, result.output
    expected = [actions.Action.CONFIGURE.value, "sessions", actions.Action.BACKFILL.value,
                "dashboard"]
    if not open_dashboard:
        expected.append("menu")
    assert events == expected
