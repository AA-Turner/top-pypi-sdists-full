"""The main-menu import selector reuses onboarding without installing again."""

import pytest
from typer.testing import CliRunner

from probe.cli import backfill, backfill_transcripts, import_jobs_ui, setup, tui
from probe.cli.actions import Action
from probe.sdk.config import resolve
from tests import test_wizard_auth_entry as auth_fixtures

entry = auth_fixtures.entry
main = auth_fixtures.main


@pytest.fixture
def import_menu(entry, monkeypatch):
    events, calls = entry, {"sessions": [], "folder": [], "monitor": []}
    monkeypatch.setattr(main, "_run_wizard_action", auth_fixtures.apply_wizard_action)
    monkeypatch.setattr(setup, "detectable_sources", lambda: ("claude_code", "codex"))
    actions = iter((Action.IMPORT_RESEARCH, Action.EXIT))
    monkeypatch.setattr(
        setup, "run_action_menu", lambda _caps: events.append(("menu", {})) or next(actions),
    )

    def forbidden(*args, **kwargs):
        pytest.fail("Importing must not configure agents or add a Finished pause")

    monkeypatch.setattr(setup, "run_agent_menu", forbidden)
    monkeypatch.setattr(setup, "run_confirm_install", forbidden)
    monkeypatch.setattr(tui, "page", forbidden)
    monkeypatch.setattr(backfill, "resolve_agent", forbidden)

    def client():
        # Authentication must finish before either lane resolves its client.
        assert resolve().token == "probe_pat_menu_test"
        return object()

    monkeypatch.setattr(main, "_backfill_client", client)

    def session_lane(**kwargs):
        events.append(("sessions", {}))
        calls["sessions"].append(kwargs)
        assert tui.onboarding_header() == []
        return ["Session import queued."]

    def folder_lane(**kwargs):
        events.append(("folder", {}))
        calls["folder"].append(kwargs)
        kwargs["client_factory"]()
        assert tui.onboarding_header() == []
        return ["Folder import queued."]

    def monitor(**kwargs):
        events.append(("monitor", {}))
        calls["monitor"].append(kwargs)
        assert tui.onboarding_header() == []
        return import_jobs_ui.Navigation.MENU

    monkeypatch.setattr(backfill_transcripts, "run_lane", session_lane)
    monkeypatch.setattr(backfill, "run", folder_lane)
    monkeypatch.setattr(import_jobs_ui, "show_imports", monitor)
    return events, calls


@pytest.mark.parametrize("selection", [
    set(), tui.BACK, {setup.BackfillChoice.PAST_SESSIONS},
    {setup.BackfillChoice.PROJECT_FOLDER}, set(setup.BackfillChoice),
])
@pytest.mark.parametrize("agent_args", [[], ["--agent", "both"]])
def test_menu_runs_only_selected_imports_once_after_sign_in(
    import_menu, monkeypatch, selection, agent_args,
):
    events, calls = import_menu

    def choose(_sources, **kwargs):
        events.append(("choose", kwargs))
        assert kwargs["onboarding"] is False
        assert kwargs["back_to_menu"] is True
        assert kwargs["defaults"] is None
        return selection

    monkeypatch.setattr(setup, "run_backfill_offer", choose)
    result = CliRunner().invoke(main.app, ["wizard", *agent_args])
    assert result.exit_code == 0, result.output
    selected = set() if selection is tui.BACK else selection
    expected = ["signin", "menu", "choose"]
    notices = []
    if setup.BackfillChoice.PAST_SESSIONS in selected:
        expected.append("sessions")
        assert len(calls["sessions"]) == 1
        assert calls["sessions"][0]["interactive"] is True
        assert calls["sessions"][0]["background"] is True
        notices.extend(["Session import queued.", ""])
    else:
        assert not calls["sessions"]
    if setup.BackfillChoice.PROJECT_FOLDER in selected:
        expected.append("folder")
        assert len(calls["folder"]) == 1
        assert calls["folder"][0]["transcripts"] is False
        assert calls["folder"][0]["interactive"] is True
        assert calls["folder"][0]["background"] is True
        notices.extend(["Folder import queued.", ""])
    else:
        assert not calls["folder"]
    if selected:
        expected.append("monitor")
        assert calls["monitor"] == [{"onboarding": False, "notices": notices}]
    else:
        assert not calls["monitor"]
    assert [event for event, _ in events] == [*expected, "menu"]


def test_ctrl_c_on_import_selector_exits_without_running_any_lane(import_menu, monkeypatch):
    events, calls = import_menu
    monkeypatch.setattr(setup, "run_backfill_offer", lambda *_a, **_kw: None)
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert [event for event, _ in events] == ["signin", "menu"]
    assert not any(calls.values())


@pytest.mark.parametrize("answer", [None, tui.BACK], ids=["skip", "back"])
def test_folder_skip_finishes_but_back_reopens_import_choices(import_menu, monkeypatch, answer):
    events, calls = import_menu
    selections = iter([{setup.BackfillChoice.PROJECT_FOLDER}, set()])
    defaults = []

    def choose(*args, **kwargs):
        defaults.append(kwargs["defaults"])
        return next(selections)

    monkeypatch.setattr(setup, "run_backfill_offer", choose)
    monkeypatch.setattr(backfill, "run", lambda **kwargs: answer)
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert [event for event, _ in events] == ["signin", "menu", "menu"]
    assert not calls["sessions"] and not calls["monitor"]
    assert defaults == ([None, {setup.BackfillChoice.PROJECT_FOLDER}]
                        if answer is tui.BACK else [None])


def test_direct_combined_action_signs_in_and_honors_return_to_menu(import_menu, monkeypatch):
    events, calls = import_menu
    monkeypatch.setattr(setup, "run_backfill_offer", lambda *_a, **_kw: set(setup.BackfillChoice))
    monkeypatch.setattr(
        setup, "run_action_menu", lambda _caps: events.append(("menu", {})) or Action.EXIT,
    )
    result = CliRunner().invoke(main.app, ["wizard", "--action", "import-research"])
    assert result.exit_code == 0, result.output
    assert [event for event, _ in events] == ["signin", "sessions", "folder", "monitor", "menu"]
    assert len(calls["sessions"]) == len(calls["folder"]) == len(calls["monitor"]) == 1


def test_ctrl_c_during_session_review_does_not_start_folder_import(import_menu, monkeypatch):
    events, calls = import_menu
    monkeypatch.setattr(setup, "run_backfill_offer", lambda *_a, **_kw: set(setup.BackfillChoice))

    def cancel(**kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(backfill_transcripts, "run_lane", cancel)
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 130, result.output
    assert [event for event, _ in events] == ["signin", "menu"]
    assert not calls["folder"] and not calls["monitor"]


@pytest.mark.parametrize("interactive,flags", [(False, []), (True, ["--yes"])])
def test_combined_action_requires_selection_without_changing_legacy_commands(
    import_menu, monkeypatch, interactive, flags,
):
    _events, calls = import_menu
    monkeypatch.setattr(setup, "interactive", lambda: interactive)
    monkeypatch.setattr(setup, "run_backfill_offer", lambda *_a, **_kw: pytest.fail("no selector"))
    result = CliRunner().invoke(main.app, ["wizard", "--action", "import-research", *flags])
    assert result.exit_code == 2, result.output
    assert "interactive selection" in result.output
    assert "backfill" in result.output and "transcripts" in result.output
    assert not any(calls.values())


