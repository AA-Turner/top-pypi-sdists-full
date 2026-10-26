"""The update path updates Probe's pi package whatever agent runs it.

It used to print "pi: not managed by this CLI" for pi and skip pi entirely for
everyone else, so an Update from a plain terminal -- or Claude Code's
auto-update -- left pi on whatever package it was installed with (2026-10-02:
a 0.2.x package under a 0.206 CLI, so pi never switched to the daemon).
"""

from __future__ import annotations

import pytest

from probe.cli import pi_config, upgrading
from probe.cli.claude_cli import Result


@pytest.fixture
def pi_dir(tmp_path):
    directory = tmp_path / "pi-pkg"
    directory.mkdir()
    return directory


@pytest.fixture
def pi_installed(monkeypatch, pi_dir):
    versions = iter([(0, 2, 3), (0, 3, 0)])
    calls: list[int] = []
    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: pi_dir)
    monkeypatch.setattr(pi_config, "installed_package_version", lambda env=None: next(versions))
    monkeypatch.setattr(pi_config, "update_package", lambda env=None: calls.append(1) or Result(ok=True, detail="updated"))
    return calls


def test_the_pi_lines_say_what_moved(pi_installed):
    step = upgrading._update_pi_package()
    assert step.lines == ["pi package:", "  updated 0.2.3 → 0.3.0 (run /reload in open pi sessions (or restart them) to apply)"]
    assert step.ok and pi_installed == [1]


def test_a_failed_pi_update_fails_and_says_how_to_do_it_by_hand(monkeypatch, pi_dir):
    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: pi_dir)
    monkeypatch.setattr(pi_config, "installed_package_version", lambda env=None: (0, 2, 3))
    monkeypatch.setattr(pi_config, "update_package", lambda env=None: Result(ok=False, detail="offline"))

    step = upgrading._update_pi_package()

    assert step.lines[1] == f"  ! not updated (offline); run `pi update {pi_config.MIRROR_GIT_SOURCE}`"
    assert step.ok is False and "offline" in step.detail


def test_no_pi_package_means_no_pi_step(monkeypatch):
    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: None)
    monkeypatch.setattr(pi_config, "update_package", lambda env=None: pytest.fail("pi is not installed"))
    assert upgrading._update_pi_package().lines == []


@pytest.mark.parametrize("cli_ok,plugin_ok", [(True, True), (False, True), (True, False)])
def test_update_stream_reports_real_stage_boundaries(monkeypatch, cli_ok, plugin_ok):
    from probe.cli import updater
    from probe.core import events

    emitted = []
    monkeypatch.setenv("PROBE_AGENT", "pi")
    monkeypatch.setattr(updater, "fetch_latest", lambda base: {})
    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL))
    monkeypatch.setattr(upgrading, "_report_attempt", lambda *a, **k: None)

    def cli(install, current, target):
        assert emitted[-1]["name"] == events.Step.UPDATE_CLI
        assert emitted[-1]["status"] == events.Status.STARTED
        assert emitted[-2]["name"] == events.Step.UPDATE_MANIFEST
        assert emitted[-2]["status"] == events.Status.DONE
        return updater.CliResult(ran=True, ok=cli_ok, changed=False, before=current,
                                 after=current, message="checked")

    def plugins():
        assert emitted[-1]["name"] == events.Step.UPDATE_INTEGRATIONS
        assert emitted[-1]["status"] == events.Status.STARTED
        return upgrading._PiUpdate([], ok=plugin_ok, detail="" if plugin_ok else "failed")

    monkeypatch.setattr(updater, "upgrade_cli", cli)
    monkeypatch.setattr(upgrading, "_update_pi_package", plugins)
    with events.session(True, sink=emitted.append):
        outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)

    stages = [event for event in emitted if event["event"] == events.Event.STEP]
    completed = [event for event in stages if event["status"] != events.Status.STARTED]
    assert [event["name"] for event in completed] == [
        "update_manifest", "update_cli", "update_integrations", "verify_update",
    ]
    assert [event["status"] for event in completed] == [
        events.Status.DONE,
        events.Status.DONE if cli_ok else events.Status.FAILED,
        events.Status.DONE if plugin_ok else events.Status.FAILED,
        events.Status.DONE,
    ]
    assert outcome.ok is (cli_ok and plugin_ok)


def test_pi_update_runs_with_pi_open_and_clears_an_old_deferral(monkeypatch, pi_installed):
    """Waiting for pi to exit never ended for pi agents running around the clock
    (strand-ai, 2026-10-15): it runs whatever pi is doing, and a running pi
    keeps what it loaded until `/reload` or a restart. An older CLI's deferral
    left the owed marker set; the update clears it."""
    from probe.cli import autoupdate

    autoupdate.mark_pi_update_pending(True)

    step = upgrading._update_pi_package()

    assert pi_installed == [1], "pi update ran"
    assert step.ok and step.code is upgrading.update_report.PiStep.UPDATED
    assert step.lines == ["pi package:", "  updated 0.2.3 → 0.3.0 (run /reload in open pi sessions (or restart them) to apply)"]
    assert not autoupdate.pi_update_pending(), "nothing owed any more"


def test_an_update_killed_partway_stays_owed(monkeypatch, pi_dir):
    """`pi update` removes and reinstalls `node_modules`: an updater killed in
    the middle must leave the update owed, not forgotten."""
    from probe.cli import autoupdate

    class Killed(BaseException):
        pass

    def killed(env=None):
        raise Killed

    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: pi_dir)
    monkeypatch.setattr(pi_config, "installed_package_version", lambda env=None: (0, 2, 3))
    monkeypatch.setattr(pi_config, "update_package", killed)

    with pytest.raises(Killed):
        upgrading._update_pi_package()

    assert autoupdate.pi_update_pending()


def test_a_second_update_never_runs_pi_update_at_the_same_time(monkeypatch, pi_installed):
    with upgrading._pi_update_lock() as held:
        assert held
        step = upgrading._update_pi_package()
    assert step.ok and step.lines[1] == "  another update is updating it now"
    assert pi_installed == []


def test_a_failed_pi_update_is_recorded_as_a_failed_update(monkeypatch):
    """The detached run from pi's session start reports only through the
    attempt record: a failure written only to its lines read as success."""
    from probe.cli import autoupdate, updater

    monkeypatch.setenv("PROBE_AGENT", "pi")
    monkeypatch.setattr(upgrading.updater, "fetch_latest", lambda base: {})
    monkeypatch.setattr(upgrading.updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL))
    monkeypatch.setattr(
        upgrading.updater,
        "upgrade_cli",
        lambda i, c, t: updater.CliResult(ran=True, ok=True, changed=False, before=c, after=c, message="latest"),
    )
    monkeypatch.setattr(
        upgrading, "_update_pi_package", lambda: upgrading._PiUpdate(["pi package:", "  ! x"], ok=False, detail="pi package not updated: x")
    )
    recorded = []
    monkeypatch.setattr(autoupdate, "record_attempt", lambda attempt, **_: recorded.append(attempt))

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)

    assert outcome.ok is False
    assert recorded[-1].plugin_ok is False and "pi package not updated" in recorded[-1].plugin_detail


def test_pi_gone_is_a_skip_not_a_failed_update(monkeypatch, pi_dir):
    """Uninstalled pi whose settings still name us: every Claude Code or Codex
    update would otherwise report failure."""
    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: pi_dir)
    monkeypatch.setattr(pi_config, "installed_package_version", lambda env=None: (0, 2, 3))
    monkeypatch.setattr(
        pi_config, "update_package", lambda env=None: Result(ok=False, detail="pi is not on PATH", reachable=False)
    )

    step = upgrading._update_pi_package()

    assert step.ok and step.lines[1] == "  not updated: pi is not on PATH"


def test_a_package_folder_that_is_gone_means_no_pi_step(monkeypatch, tmp_path):
    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: tmp_path / "missing")
    monkeypatch.setattr(pi_config, "update_package", lambda env=None: pytest.fail("nothing to update"))
    assert upgrading._update_pi_package().lines == []


def test_the_pi_update_lock_lives_in_the_users_state_dir():
    from probe.sdk import session_marker

    with upgrading._pi_update_lock() as held:
        assert held
        assert (session_marker.state_dir() / "pi-update.lock").exists()


def test_a_failed_pi_update_stays_owed_and_a_gone_pi_does_not(monkeypatch, pi_dir):
    from probe.cli import autoupdate

    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: pi_dir)
    monkeypatch.setattr(pi_config, "installed_package_version", lambda env=None: (0, 2, 3))
    monkeypatch.setattr(pi_config, "update_package", lambda env=None: Result(ok=False, detail="offline"))
    upgrading._update_pi_package()
    assert autoupdate.pi_update_pending()

    monkeypatch.setattr(
        pi_config, "update_package", lambda env=None: Result(ok=False, detail="pi is not on PATH", reachable=False)
    )
    upgrading._update_pi_package()
    assert not autoupdate.pi_update_pending(), "nothing left to update with"


def test_the_owed_pi_step_records_what_pi_update_did(monkeypatch, pi_installed):
    from probe.cli import autoupdate

    recorded = []
    monkeypatch.setattr(autoupdate, "record_attempt", lambda attempt, **_: recorded.append(attempt))

    upgrading.update_owed_pi_package()

    assert recorded[-1].succeeded
    # The whole move, not only the reload hint (2026-10-15 review).
    assert recorded[-1].plugin_detail == "pi package updated 0.2.3 → 0.3.0 (run /reload in open pi sessions (or restart them) to apply)"


def test_an_owed_update_that_skips_is_not_recorded(monkeypatch, pi_installed):
    """Overwriting `last_attempt` with "another update is updating it" would
    hide the real attempt `probe doctor` prints."""
    from probe.cli import autoupdate

    monkeypatch.setattr(autoupdate, "record_attempt", lambda attempt, **_: pytest.fail("nothing ran"))

    with upgrading._pi_update_lock() as held:
        assert held
        upgrading.update_owed_pi_package()


def test_a_lock_that_cannot_be_opened_never_blocks_the_update(monkeypatch, tmp_path):
    from probe.sdk import session_marker

    blocker = tmp_path / "a-file"
    blocker.write_text("")
    monkeypatch.setattr(session_marker, "state_dir", lambda: blocker / "state")

    with upgrading._pi_update_lock() as held:
        assert held
