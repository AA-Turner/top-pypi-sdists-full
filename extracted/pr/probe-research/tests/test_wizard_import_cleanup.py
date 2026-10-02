"""Wizard exits preserve imports; signing out or uninstalling clears them."""

import os
import signal
from pathlib import Path
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

from probe.cli import import_jobs, import_jobs_ui, onboarding_complete, setup, tui
from probe.cli.actions import Action
from probe.cli.capabilities import Capabilities
from tests import test_wizard_auth_entry as auth
from tests import test_wizard_install_completion as install_tests

entry = auth.entry
main = auth.main
installation = install_tests.installation


@pytest.fixture
def saved_import(entry, monkeypatch):
    monkeypatch.setattr(import_jobs, "_launch", import_jobs._read)
    job = import_jobs.enqueue("folder", {"approved": True}, "Saved import")
    # No process was spawned: settle that observation before checking that Exit
    # preserves the saved record. The real-worker cases below cover liveness.
    import_jobs.get_job(job['id'])
    return Path(job["log_path"]).parent


@pytest.mark.parametrize("selection", [Action.EXIT, None, tui.BACK])
def test_quit_from_main_menu_preserves_local_imports(saved_import, monkeypatch, selection):
    monkeypatch.setattr(setup, "run_action_menu", lambda caps: selection)
    before = (saved_import / 'job.json').read_text()
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert (saved_import / 'job.json').read_text() == before
    assert len(import_jobs.list_jobs()) == 1


@pytest.mark.parametrize("exception", [KeyboardInterrupt, main.typer.Abort])
def test_ctrl_c_preserves_local_imports(saved_import, monkeypatch, exception):
    def interrupt(caps):
        raise exception

    monkeypatch.setattr(setup, "run_action_menu", interrupt)
    before = (saved_import / 'job.json').read_text()
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code != 0
    assert (saved_import / 'job.json').read_text() == before


@pytest.mark.parametrize('navigation', ['dashboard', 'main_menu', 'exit', 'interrupt'])
def test_leaving_onboarding_complete_preserves_imports(saved_import, installation, monkeypatch, navigation):
    shown = []

    def handoff(base):
        shown.append(base)
        if navigation == 'interrupt':
            raise KeyboardInterrupt
        if navigation == 'exit':
            return import_jobs_ui.Navigation.EXIT
        return navigation == 'dashboard'

    monkeypatch.setattr(onboarding_complete, 'show', handoff)
    result = CliRunner().invoke(main.app, ["install", "--agent", "claude"])
    assert (result.exit_code != 0) is (navigation == 'interrupt'), result.output
    assert shown
    assert installation.registrations[-1][1] is True
    assert saved_import.exists()


def test_quitting_the_post_import_monitor_preserves_imports(saved_import, monkeypatch):
    monkeypatch.setattr(main, "_import_past_sessions", lambda **k: ["Session import queued."])
    monkeypatch.setattr(import_jobs_ui, "show_imports", lambda **k: import_jobs_ui.Navigation.EXIT)
    with pytest.raises(main.typer.Exit):
        main._run_selected_imports(
            {setup.BackfillChoice.PAST_SESSIONS}, caps=Capabilities(),
            base_now="https://api.test", folder=None, selected_agents=("claude_code",),
            telemetry=None,
        )
    assert saved_import.exists()


def test_quitting_the_import_selector_preserves_already_started_imports(saved_import, monkeypatch):
    monkeypatch.setattr(setup, 'run_backfill_offer', lambda *a, **k: None)
    with pytest.raises(main.typer.Exit):
        main._select_and_run_imports(
            caps=Capabilities(), base_now='https://api.test', folder=None,
            selected_agents=('claude_code',), telemetry=None,
        )
    assert saved_import.exists()


@pytest.mark.parametrize('interrupt', [False, True])
def test_leaving_wizard_keeps_real_background_worker_alive(entry, monkeypatch, tmp_path, interrupt):
    from tests.test_import_jobs import _await_job, _fake_worker_package

    _fake_worker_package(tmp_path, monkeypatch, """
        import time

        def run_background_job(payload, *, progress):
            while True:
                progress('Still importing', completed=1, total=3)
                time.sleep(.02)
    """)
    job = import_jobs.enqueue('transcripts', {'approval': 'saved'}, 'Background import')
    active = _await_job(job['id'], lambda row: row['progress']['message'] == 'Still importing')

    def leave(_caps):
        if interrupt:
            raise KeyboardInterrupt
        return Action.EXIT

    monkeypatch.setattr(setup, 'run_action_menu', leave)
    try:
        result = CliRunner().invoke(main.app, ['wizard'])
        assert (result.exit_code != 0) is interrupt, result.output
        assert import_jobs._alive(active['pid'], active['pid_identity'])
        saved = import_jobs.get_job(job['id'])
        assert saved['state'] == import_jobs.State.RUNNING
        assert saved['payload'] == job['payload']
        assert saved['progress']['completed'] == 1
        assert Path(job['log_path']).is_file()
    finally:
        import_jobs.cancel(job['id'])
        if import_jobs._alive(active['pid'], active['pid_identity']):
            os.kill(active['pid'], signal.SIGKILL)


def test_sign_out_clears_imports_before_capture_or_credentials(saved_import, monkeypatch):
    monkeypatch.setattr(setup, "capture_token_sources", lambda source: ())

    def release():
        assert not saved_import.exists()
        return ["Signed out."]

    monkeypatch.setattr(setup, "release_credentials", release)
    lines = setup.sign_out(("claude_code",))
    assert "Imports stopped and local import history cleared." in lines


def test_uninstall_clears_imports_before_removing_plugins(saved_import, monkeypatch):
    def stop_capture(mode):
        assert not saved_import.exists()
        return SimpleNamespace(summary=lambda: "Stopped.", warnings=[], plugin_removed=False)

    monkeypatch.setattr(setup, "turn_off", stop_capture)
    monkeypatch.setattr(setup, "uninstall_plugin", lambda name: SimpleNamespace(ok=True))
    monkeypatch.setattr(setup, "apply_agent_rules", lambda enabled: [])
    monkeypatch.setattr(setup.autoupdate, "forget", lambda: None)
    setup.remove_everything(Capabilities(agent_source="claude_code"))
    assert not saved_import.exists()


def test_declining_uninstall_keeps_saved_imports(saved_import, monkeypatch):
    monkeypatch.setattr(setup, "confirm_removal", lambda source: False)
    from tests.test_wizard_auth_entry import apply_wizard_action

    result = apply_wizard_action(
        Action.UNINSTALL, caps=Capabilities(agent_source="claude_code"),
        base_now="https://api.test", yes=False, tracking=None, capture=None,
        auto_update=None, agent_rules=None, uninstall=False, configured=True,
    )
    assert result is None
    assert saved_import.exists()


def test_standalone_logout_clears_imports_before_revoking_token(saved_import, monkeypatch):
    from contextlib import nullcontext

    def revoke():
        assert not saved_import.exists()

    monkeypatch.setattr(main, "_client", lambda: nullcontext(SimpleNamespace(logout=revoke)))
    result = CliRunner().invoke(main.app, ["logout"])
    assert result.exit_code == 0, result.output
    assert not saved_import.exists()
