"""Going Back through optional imports never reapplies a completed install."""

import pytest
from typer.testing import CliRunner

from probe.cli import backfill, backfill_transcripts, import_jobs, onboarding_complete, setup, tui
from tests import test_wizard_install_completion as install_tests
from tests.test_tui_review import _run

entry = install_tests.entry
installation = install_tests.installation
main = install_tests.main
run_selected_imports = main._run_selected_imports


@pytest.mark.parametrize("agent,count", [("claude", 1), ("both", 2)])
@pytest.mark.parametrize("back_from", ["sessions", "folder"])
def test_back_reopens_import_choices_without_reinstalling(
    installation, entry, monkeypatch, agent, count, back_from,
):
    calls, defaults, queued = [], [], []
    session = setup.BackfillChoice.PAST_SESSIONS
    folder = setup.BackfillChoice.PROJECT_FOLDER
    answers = iter([{session, folder}, {folder}])
    monkeypatch.setattr(main, "_run_selected_imports", run_selected_imports)
    monkeypatch.setattr(main, "_backfill_client", lambda: object())
    monkeypatch.setattr(import_jobs, "_launch", import_jobs._read)
    monkeypatch.setattr(setup, "run_action_menu", lambda *a: pytest.fail("Back escaped import setup"))
    monkeypatch.setattr(onboarding_complete, "show", lambda base: calls.append("dashboard") or True)

    def offer(sources, **kwargs):
        assert len(installation.registrations) == count
        assert installation.registrations[-1][1] is True
        assert kwargs["back_to_menu"] is True
        defaults.append(kwargs["defaults"])
        calls.append("choices")
        return next(answers)

    def sessions(**kwargs):
        assert kwargs["back_to_selection"] is True
        calls.append("sessions")
        if back_from == "sessions":
            return tui.BACK
        job = import_jobs.enqueue("transcripts", {"approved": True}, "Already started")
        queued.append(job["id"])
        return ["Session import queued."]

    def files(**kwargs):
        assert kwargs["back_to_selection"] is True
        calls.append("folder")
        if back_from == "folder" and calls.count("folder") == 1:
            return tui.BACK
        return []

    monkeypatch.setattr(setup, "run_backfill_offer", offer)
    monkeypatch.setattr(backfill_transcripts, "run_lane", sessions)
    monkeypatch.setattr(backfill, "run", files)
    result = CliRunner().invoke(main.app, ["install", "--agent", agent])
    assert result.exit_code == 0, result.output
    assert defaults == [None, {session, folder} if back_from == "sessions" else {folder}]
    assert calls == (["choices", "sessions", "choices", "folder", "dashboard"]
                     if back_from == "sessions" else
                     ["choices", "sessions", "folder", "choices", "folder", "dashboard"])
    assert len(installation.registrations) == count
    assert len(installation.work) == count * 4
    assert [event for event, _ in entry].count("confirm") == 1
    assert {job["id"] for job in import_jobs.list_jobs()} == set(queued)


def test_deselecting_both_after_back_still_finishes_onboarding(installation, monkeypatch):
    choices = [set(setup.BackfillChoice), set()]
    monkeypatch.setattr(main, "_run_selected_imports", run_selected_imports)
    monkeypatch.setattr(setup, "run_backfill_offer", lambda *a, **k: choices.pop(0))
    monkeypatch.setattr(main, "_import_past_sessions", lambda **k: tui.BACK)
    monkeypatch.setattr(onboarding_complete, "show", lambda base: True)
    monkeypatch.setattr(setup, "run_action_menu", lambda *a: pytest.fail("must finish onboarding"))
    result = CliRunner().invoke(main.app, ["install", "--agent", "claude"])
    assert result.exit_code == 0, result.output
    assert len(installation.registrations) == 1 and not choices


def test_import_selector_main_menu_action_leaves_install_complete(installation, monkeypatch):
    from probe.cli.actions import Action

    menu = []
    monkeypatch.setattr(setup, "run_backfill_offer", lambda *a, **k: tui.BACK)
    monkeypatch.setattr(setup, "run_action_menu", lambda *a: menu.append(True) or Action.EXIT)
    result = CliRunner().invoke(main.app, ["install", "--agent", "claude"])
    assert result.exit_code == 0, result.output
    assert menu == [True]
    assert len(installation.registrations) == 1
    assert not installation.handoffs


@pytest.mark.tui
def test_review_left_returns_back_without_approving(monkeypatch):
    result, _ = _run(
        monkeypatch, ["\x1b[D"],
        render=lambda: tui.review("Review import", ["No files have been uploaded."], [("Import", "import")]),
    )
    assert result is tui.BACK


