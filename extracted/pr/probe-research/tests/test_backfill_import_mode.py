"""Automatic folder planning requires an explicit choice before any scan."""

from contextlib import nullcontext
from types import SimpleNamespace

import pytest

from probe.cli import backfill as bf, backfill_import, backfill_run, backfill_transcripts
from probe.cli import import_job_messages, import_jobs, import_jobs_ui, tui
from probe.cli.backfill_coverage import CoverageError


@pytest.fixture
def flow(monkeypatch, tmp_path):
    monkeypatch.setattr(bf, "choose_folder_wandb", lambda *a, **k: (None, False))
    state = SimpleNamespace(
        folder=tmp_path, events=[], calls={}, reply=bf.FolderImportMode.REVIEW_FIRST,
        queued={"id": "saved-job", "kind": import_jobs.Kind.FOLDER, "state": import_jobs.State.QUEUED},
        latest={"id": "saved-job", "kind": import_jobs.Kind.FOLDER, "state": import_jobs.State.RUNNING},
    )

    def choose(start):
        state.events.append("folder")
        return state.folder

    def resolve(agent, **kwargs):
        state.events.append("agent")
        return bf.Agent.CLAUDE, None

    def review(title, lines, choices):
        state.events.append("mode")
        state.calls["prompt"] = (title, lines, choices)
        return state.reply

    def execute(**kwargs):
        state.events.append("execute")
        state.calls["execute"] = kwargs
        return ["Reviewed import"]

    def enqueue(**kwargs):
        state.events.append("enqueue")
        state.calls["enqueue"] = kwargs
        return state.queued

    def handoff(job):
        state.events.append("handoff")
        assert job is state.queued
        return state.latest

    def report(job, label):
        state.events.append("report")
        assert job is state.latest and label == "Folder import"
        return ["Saved folder import is running"]

    monkeypatch.setattr(bf, "choose_directory", choose)
    monkeypatch.setattr(bf, "resolve_agent", resolve)
    monkeypatch.setattr(tui, "review", review)
    monkeypatch.setattr(backfill_run, "execute", execute)
    monkeypatch.setattr(backfill_import, "enqueue_auto_import", enqueue, raising=False)
    monkeypatch.setattr(import_jobs_ui, "show_started_import", handoff)
    monkeypatch.setattr(import_job_messages, "enqueue_report", report)
    return state


def test_review_first_is_the_default_and_uses_the_existing_scan_and_review_flow(flow):
    result = bf.run(client_factory=object, background=True)
    assert result == ["Reviewed import"]
    assert flow.events == ["folder", "agent", "mode", "execute"]
    title, lines, choices = flow.calls["prompt"]
    assert title == "Import this folder" and str(flow.folder) in "\n".join(lines)
    assert "Claude Code" in "\n".join(lines)
    assert "apply the resulting plan and upload" in "\n".join(lines)
    assert "automatically in the background" in "\n".join(lines)
    assert choices[0] == ("Review the plan first", bf.FolderImportMode.REVIEW_FIRST)
    assert choices[1] == ("Scan and import in background", bf.FolderImportMode.AUTOMATIC)
    assert choices[2] == ("Skip folder", tui.SKIP)
    assert flow.calls["execute"]["background"] is True
    assert flow.calls["execute"]["yes"] is False


def test_automatic_mode_forwards_explicit_consent_and_scope_before_the_handoff(flow):
    flow.reply = bf.FolderImportMode.AUTOMATIC
    result = bf.run(
        client_factory=object, background=True, project="project-id", concurrency=3,
        source_id="source-id", import_changed=True, import_unverified=True,
    )
    assert result == ["Saved folder import is running"]
    assert flow.events == ["folder", "agent", "mode", "enqueue", "handoff", "report"]
    assert flow.calls["enqueue"] == {
        "client_factory": object, "folder": flow.folder.resolve(), "agent": bf.Agent.CLAUDE,
        "auto_approve": True, "project": "project-id", "concurrency": 3,
        "source_id": "source-id", "import_changed": True, "import_unverified": True,
        "retry_dead": False,
    }


@pytest.mark.parametrize("reply", [tui.BACK, tui.SKIP, None], ids=["back", "skip", "quit"])
def test_leaving_the_mode_choice_never_scans_or_enqueues(flow, reply):
    flow.reply = reply
    if reply is None:
        with pytest.raises(KeyboardInterrupt):
            bf.run(client_factory=object, background=True)
    else:
        assert bf.run(client_factory=object, background=True) is None
    assert flow.events == ["folder", "agent", "mode"]


@pytest.mark.parametrize("interactive,background,yes", [
    (False, True, False), (False, True, True), (True, True, True), (True, False, False),
])
def test_headless_yes_and_foreground_calls_keep_their_existing_behavior(flow, interactive, background, yes):
    result = bf.run(client_factory=object, folder=flow.folder, interactive=interactive, background=background, yes=yes)
    assert result == ["Reviewed import"] and flow.events == ["agent", "execute"]
    assert flow.calls["execute"]["interactive"] is interactive
    assert flow.calls["execute"]["background"] is background
    assert flow.calls["execute"]["yes"] is yes


def test_automatic_folder_mode_keeps_the_optional_session_lane_separate(flow, monkeypatch):
    flow.reply = bf.FolderImportMode.AUTOMATIC
    client = object()

    def sessions(**kwargs):
        flow.events.append("sessions")
        assert kwargs == {"client": client, "interactive": True, "background": True, "budget_bytes": 1234}
        return ["Sessions queued separately"]

    monkeypatch.setattr(backfill_transcripts, "run_lane", sessions)
    result = bf.run(client_factory=lambda: nullcontext(client), background=True, transcripts=True, transcripts_budget=1234)
    assert result == ["Saved folder import is running", "Sessions queued separately"]
    assert flow.events[-2:] == ["report", "sessions"]
    assert "transcripts" not in flow.calls["enqueue"]


@pytest.mark.parametrize("error", [CoverageError("The destination could not be verified."), RuntimeError("private transport detail")])
def test_enqueue_failure_returns_safe_guidance_without_opening_a_handoff(flow, monkeypatch, error):
    flow.reply = bf.FolderImportMode.AUTOMATIC

    def fail(**kwargs):
        raise error

    monkeypatch.setattr(backfill_import, "enqueue_auto_import", fail)
    text = "\n".join(bf.run(client_factory=object, background=True))
    assert "Folder import could not start" in text
    assert "private transport detail" not in text
    assert flow.events == ["folder", "agent", "mode"]
    if isinstance(error, CoverageError):
        assert str(error) in text


@pytest.mark.parametrize("agent_result", [(None, None), (tui.BACK, None), (None, "No supported coding agent found.")])
def test_agent_exit_or_failure_does_not_open_the_mode_choice(flow, monkeypatch, agent_result):
    monkeypatch.setattr(bf, "resolve_agent", lambda *args, **kwargs: agent_result)
    result = bf.run(client_factory=object, folder=flow.folder, background=True)
    assert result == ([agent_result[1]] if agent_result[1] else None)
    assert flow.events == []
