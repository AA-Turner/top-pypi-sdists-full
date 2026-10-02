"""Back revisits reversible import forms; Skip advances without starting work."""

from contextlib import nullcontext

import pytest

from probe.cli import backfill as bf, backfill_transcripts as bt, tui
from probe.cli import backfill_import, backfill_run, import_jobs, import_jobs_ui, import_job_messages
from tests import test_backfill_transcripts as transcript_tests

lane = transcript_tests.lane


@pytest.fixture(autouse=True)
def no_external_work(monkeypatch):
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "working", lambda *a, **k: nullcontext())
    monkeypatch.setattr(import_jobs, "enqueue", lambda *a, **k: pytest.fail("Queued after Back or Skip"))
    monkeypatch.setattr(backfill_import, "enqueue_auto_import", lambda **k: pytest.fail("Imported after Back or Skip"))
    monkeypatch.setattr(backfill_run, "execute", lambda **k: pytest.fail("Scanned after Back or Skip"))


@pytest.mark.parametrize("opt_in", [False, True])
@pytest.mark.parametrize("answer", [tui.BACK, tui.SKIP])
def test_session_source_back_is_distinct_from_skip(lane, monkeypatch, opt_in, answer):
    monkeypatch.setattr(bt, "choose_sources", lambda available: answer)
    monkeypatch.setattr(bt, "discover", lambda **k: pytest.fail("Scanned after source Back or Skip"))
    _, result = lane(interactive=True, back_to_selection=opt_in)
    assert result is tui.BACK if opt_in and answer is tui.BACK else result == ["Skipped the agent sessions."]


def test_session_review_back_reopens_selected_sources_before_leaving(lane, monkeypatch):
    choices, scans = [], []
    discover = bt.discover

    def choose(available, *, selected=None):
        choices.append((available, selected))
        return (bt.CODEX,) if len(choices) == 1 else tui.BACK

    monkeypatch.setattr(bt, "choose_sources", choose)
    monkeypatch.setattr(bt, "discover", lambda **k: scans.append(k) or discover(**k))
    monkeypatch.setattr(tui, "review", lambda *a: tui.BACK)
    _, result = lane(interactive=True, back_to_selection=True)
    assert result is tui.BACK
    assert choices == [((bt.CLAUDE, bt.CODEX, bt.PI), None),
                       ((bt.CLAUDE, bt.CODEX, bt.PI), (bt.CODEX,))]
    assert len(scans) == 1


def test_session_back_then_approve_reuses_preparation_and_enqueues_once(lane, monkeypatch):
    scans, prepared, queued, selections = [], [], [], []
    discover = bt.discover
    reviews = iter([tui.BACK, "import"])

    def choose(available, *, selected=None):
        selections.append(selected)
        return (bt.CLAUDE,)

    monkeypatch.setattr(bt, "choose_sources", choose)
    monkeypatch.setattr(bt, "discover", lambda **k: scans.append(k) or discover(**k))
    monkeypatch.setattr(bt, "_background_payload", lambda *a, **k: prepared.append(k) or {"approved": True})
    monkeypatch.setattr(tui, "review", lambda *a: next(reviews))
    monkeypatch.setattr(import_jobs, "enqueue", lambda *a, **k: queued.append(a) or {"id": "job"})
    monkeypatch.setattr(import_jobs_ui, "show_started_import", lambda job: job)
    monkeypatch.setattr(import_job_messages, "enqueue_report", lambda *a: ["Queued."])
    _, result = lane(interactive=True, background=True, back_to_selection=True)
    assert result == ["Queued."]
    assert selections == [None, (bt.CLAUDE,)]
    assert len(scans) == len(prepared) == len(queued) == 1


@pytest.mark.parametrize("opt_in", [False, True])
def test_session_review_skip_still_advances(lane, monkeypatch, opt_in):
    monkeypatch.setattr(tui, "review", lambda *a: "skip")
    _, result = lane(interactive=True, back_to_selection=opt_in)
    assert result == ["Skipped the agent sessions."]


def test_standalone_session_review_back_preserves_report_contract(lane, monkeypatch):
    monkeypatch.setattr(tui, "review", lambda *a: tui.BACK)
    _, result = lane(interactive=True)
    assert result == ["Skipped the agent sessions."]


@pytest.mark.parametrize("stage", ["sources", "review"])
def test_session_ctrl_c_keeps_aborting(lane, monkeypatch, stage):
    if stage == "sources":
        monkeypatch.setattr(bt, "choose_sources", lambda available: None)
    else:
        monkeypatch.setattr(tui, "review", lambda *a: None)
    with pytest.raises(KeyboardInterrupt):
        lane(interactive=True, back_to_selection=True)


@pytest.fixture
def folder_lane(tmp_path, monkeypatch):
    monkeypatch.setattr(bf, "choose_folder_wandb", lambda *a, **k: (None, False))
    monkeypatch.setattr(bf, "available_agents", lambda: [bf.Agent.CLAUDE, bf.Agent.CODEX])
    monkeypatch.setattr(bf, "which_agent", lambda a: "/test/agent")
    monkeypatch.setattr(bf, "too_old", lambda *a: None)
    monkeypatch.setattr(bf, "choose_directory", lambda start: tmp_path)
    monkeypatch.setattr(bf, "choose_agent", lambda available, **k: bf.Agent.CODEX)
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a: tui.SKIP)

    def run(**kwargs):
        return bf.run(client_factory=lambda: pytest.fail("Client opened without consent"),
                      start=tmp_path, background=True, **kwargs)

    return run


@pytest.mark.parametrize("opt_in", [False, True])
@pytest.mark.parametrize("answer", [tui.BACK, tui.SKIP])
def test_folder_first_picker_back_is_distinct_from_skip(folder_lane, monkeypatch, opt_in, answer):
    monkeypatch.setattr(bf, "choose_directory", lambda start: answer)
    result = folder_lane(back_to_selection=opt_in)
    assert result is (tui.BACK if opt_in and answer is tui.BACK else None)


def test_folder_agent_back_reopens_directory_at_selected_folder(folder_lane, tmp_path, monkeypatch):
    starts = []

    def directory(start):
        starts.append(start)
        return tmp_path if len(starts) == 1 else tui.BACK

    monkeypatch.setattr(bf, "choose_directory", directory)
    monkeypatch.setattr(bf, "choose_agent", lambda available: tui.BACK)
    assert folder_lane(back_to_selection=True) is tui.BACK
    assert starts == [tmp_path, tmp_path]


def test_folder_mode_back_reopens_agent_with_previous_choice(folder_lane, monkeypatch):
    selected = []
    modes = iter([tui.BACK, tui.SKIP])

    def agent(available, **kwargs):
        selected.append(kwargs.get("selected"))
        return bf.Agent.CODEX

    monkeypatch.setattr(bf, "choose_agent", agent)
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a: next(modes))
    assert folder_lane(back_to_selection=True) is None
    assert selected == [None, bf.Agent.CODEX]


def test_folder_mode_back_skips_hidden_agent_step(folder_lane, tmp_path, monkeypatch):
    starts = []
    monkeypatch.setattr(bf, "available_agents", lambda: [bf.Agent.CLAUDE])
    monkeypatch.setattr(bf, "choose_agent", lambda *a, **k: pytest.fail("One agent is not a step"))
    monkeypatch.setattr(bf, "choose_directory", lambda start: starts.append(start) or (tmp_path if len(starts) == 1 else tui.SKIP))
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a: tui.BACK)
    assert folder_lane(back_to_selection=True) is None
    assert starts == [tmp_path, tmp_path]


def test_folder_mode_back_with_explicit_inputs_returns_to_shared_selector(folder_lane, tmp_path, monkeypatch):
    monkeypatch.setattr(bf, "choose_directory", lambda start: pytest.fail("Explicit folder has no picker"))
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a: tui.BACK)
    assert folder_lane(folder=tmp_path, agent=bf.Agent.CLAUDE, back_to_selection=True) is tui.BACK


@pytest.mark.parametrize("stage", ["agent", "mode"])
def test_standalone_folder_back_preserves_none_contract(folder_lane, monkeypatch, stage):
    if stage == "agent":
        monkeypatch.setattr(bf, "choose_agent", lambda available: tui.BACK)
    else:
        monkeypatch.setattr(bf, "choose_import_mode", lambda *a: tui.BACK)
    assert folder_lane() is None


@pytest.mark.parametrize("stage", ["directory", "mode"])
def test_folder_ctrl_c_keeps_aborting(folder_lane, monkeypatch, stage):
    if stage == "directory":
        monkeypatch.setattr(bf, "choose_directory", lambda start: None)
    else:
        monkeypatch.setattr(bf, "choose_import_mode", lambda *a: None)
    with pytest.raises(KeyboardInterrupt):
        folder_lane(back_to_selection=True)


def test_folder_review_back_returns_to_mode_without_reopening_inputs(folder_lane, tmp_path, monkeypatch):
    events = []
    modes = iter([bf.FolderImportMode.REVIEW_FIRST, tui.SKIP])
    monkeypatch.setattr(bf, "choose_directory", lambda start: events.append("directory") or tmp_path)
    monkeypatch.setattr(bf, "choose_agent", lambda available: events.append("agent") or bf.Agent.CODEX)
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a: events.append("mode") or next(modes))

    def review(**kwargs):
        assert kwargs["back_to_selection"] is True
        assert kwargs["folder"] == tmp_path
        assert kwargs["agent"] == bf.Agent.CODEX
        events.append("review")
        return tui.BACK

    monkeypatch.setattr(backfill_run, "execute", review)
    assert folder_lane(back_to_selection=True) is None
    assert events == ["directory", "agent", "mode", "review", "mode"]


def test_folder_review_back_then_mode_back_keeps_agent_history(folder_lane, tmp_path, monkeypatch):
    choices = []
    modes = iter([bf.FolderImportMode.REVIEW_FIRST, tui.BACK, tui.SKIP])

    def agent(available, *, selected=None):
        choices.append(selected)
        return bf.Agent.CODEX

    monkeypatch.setattr(bf, "choose_agent", agent)
    monkeypatch.setattr(bf, "choose_import_mode", lambda *a: next(modes))
    monkeypatch.setattr(backfill_run, "execute", lambda **k: tui.BACK)
    assert folder_lane(back_to_selection=True) is None
    assert choices == [None, bf.Agent.CODEX]


def test_reopened_source_picker_restores_only_previous_selection(monkeypatch):
    import questionary

    rows = []
    checkbox = questionary.checkbox

    def capture(message, **kwargs):
        rows[:] = [row for row in kwargs["choices"] if getattr(row, "value", None) in (bt.CLAUDE, bt.CODEX)]
        return checkbox(message, **kwargs)

    monkeypatch.setattr(questionary, "checkbox", capture)
    monkeypatch.setattr(tui, "ask", lambda question, **kwargs: [bt.CODEX])
    monkeypatch.setattr(tui, "sectioned", lambda question, **kwargs: question)
    assert bt.choose_sources((bt.CLAUDE, bt.CODEX), selected=(bt.CODEX,)) == (bt.CODEX,)
    assert [(row.value, row.checked) for row in rows] == [(bt.CLAUDE, False), (bt.CODEX, True)]


@pytest.mark.parametrize("opt_in", [False, True])
def test_folder_agent_ctrl_c_quits_shared_flow_but_preserves_standalone_return(
    folder_lane, monkeypatch, opt_in,
):
    monkeypatch.setattr(bf, "choose_agent", lambda available: None)
    if opt_in:
        with pytest.raises(KeyboardInterrupt):
            folder_lane(back_to_selection=True)
    else:
        assert folder_lane() is None
