"""The update path updates Probe's pi package whatever agent runs it.

It used to print "pi: not managed by this CLI" for pi and skip pi entirely for
everyone else, so an Update from a plain terminal -- or Claude Code's
auto-update -- left pi on whatever package it was installed with (2026-10-02:
a 0.2.x package under a 0.206 CLI, so pi never switched to the daemon).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

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
    monkeypatch.setattr(upgrading, "_pi_running", lambda: False)
    return calls


def test_the_pi_lines_say_what_moved(pi_installed):
    step = upgrading._update_pi_package()
    assert step.lines == ["pi package:", "  updated 0.2.3 → 0.3.0"]
    assert step.ok and pi_installed == [1]


def test_a_failed_pi_update_fails_and_says_how_to_do_it_by_hand(monkeypatch, pi_dir):
    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: pi_dir)
    monkeypatch.setattr(pi_config, "installed_package_version", lambda env=None: (0, 2, 3))
    monkeypatch.setattr(pi_config, "update_package", lambda env=None: Result(ok=False, detail="offline"))
    monkeypatch.setattr(upgrading, "_pi_running", lambda: False)

    step = upgrading._update_pi_package()

    assert step.lines[1] == f"  ! not updated (offline); run `pi update {pi_config.MIRROR_GIT_SOURCE}`"
    assert step.ok is False and "offline" in step.detail


def test_no_pi_package_means_no_pi_step(monkeypatch):
    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: None)
    monkeypatch.setattr(pi_config, "update_package", lambda env=None: pytest.fail("pi is not installed"))
    assert upgrading._update_pi_package().lines == []


def test_a_running_pi_is_never_updated_under(monkeypatch, pi_dir):
    """`pi update` resets the folder a running pi loaded its extension and
    capture from: it waits for the next update instead."""
    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: pi_dir)
    monkeypatch.setattr(pi_config, "update_package", lambda env=None: pytest.fail("pi is running"))
    monkeypatch.setattr(upgrading, "_pi_running", lambda: True)

    step = upgrading._update_pi_package()

    assert step.ok and "not updated while pi is running" in step.lines[1]


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
    monkeypatch.setattr(autoupdate, "record_attempt", recorded.append)

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)

    assert outcome.ok is False
    assert recorded[-1].plugin_ok is False and "pi package not updated" in recorded[-1].plugin_detail


def test_a_running_pi_shows_up_by_its_process_title(monkeypatch):
    seen = []

    def ps(listing):
        def run(command, **kwargs):
            seen.append(command)
            return subprocess.CompletedProcess(command, 0, listing, "")

        return run

    monkeypatch.setattr(upgrading.subprocess, "run", ps("/usr/bin/python3 x\npi\n"))
    assert upgrading._pi_running()
    assert seen[-1][:2] == ["ps", "-U"], "this user's processes only"
    monkeypatch.setattr(upgrading.subprocess, "run", ps("pi-rpc\n"))
    assert upgrading._pi_running(), "pi --mode rpc titles itself pi-rpc"
    for listing in ("/usr/bin/python3 pipeline.py\n", "grep pi-coding-agent\n", "vim notes-pi.md\n"):
        monkeypatch.setattr(upgrading.subprocess, "run", ps(listing))
        assert not upgrading._pi_running(), listing


def test_pi_gone_is_a_skip_not_a_failed_update(monkeypatch, pi_dir):
    """Uninstalled pi whose settings still name us: every Claude Code or Codex
    update would otherwise report failure."""
    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: pi_dir)
    monkeypatch.setattr(pi_config, "installed_package_version", lambda env=None: (0, 2, 3))
    monkeypatch.setattr(
        pi_config, "update_package", lambda env=None: Result(ok=False, detail="pi is not on PATH", reachable=False)
    )
    monkeypatch.setattr(upgrading, "_pi_running", lambda: False)

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


def test_a_pi_update_skipped_for_a_running_pi_is_owed_until_one_runs(monkeypatch, pi_installed):
    """Every update trigger fires on "the CLI is behind", so a skip with no
    record waited for the next release: the owed marker is what pi's session
    start retries on."""
    from probe.cli import autoupdate

    monkeypatch.setattr(upgrading, "_pi_running", lambda: True)
    upgrading._update_pi_package()
    assert autoupdate.pi_update_pending()

    monkeypatch.setattr(upgrading, "_pi_running", lambda: False)
    assert upgrading._update_pi_package().ran
    assert not autoupdate.pi_update_pending()


def test_a_failed_pi_update_stays_owed_and_a_gone_pi_does_not(monkeypatch, pi_dir):
    from probe.cli import autoupdate

    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: pi_dir)
    monkeypatch.setattr(pi_config, "installed_package_version", lambda env=None: (0, 2, 3))
    monkeypatch.setattr(upgrading, "_pi_running", lambda: False)
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
    monkeypatch.setattr(autoupdate, "record_attempt", recorded.append)

    upgrading.update_owed_pi_package()

    assert recorded[-1].succeeded
    assert recorded[-1].plugin_detail == "pi package updated 0.2.3 → 0.3.0"


def test_a_second_deferral_is_not_recorded(monkeypatch, pi_dir):
    """Overwriting `last_attempt` with "pi still running" would hide the real
    attempt `probe doctor` prints."""
    from probe.cli import autoupdate

    monkeypatch.setattr(pi_config, "installed_package_dir", lambda env=None: pi_dir)
    monkeypatch.setattr(upgrading, "_pi_running", lambda: True)
    monkeypatch.setattr(autoupdate, "record_attempt", lambda attempt: pytest.fail("nothing ran"))

    upgrading.update_owed_pi_package()


def test_a_lock_that_cannot_be_opened_never_blocks_the_update(monkeypatch, tmp_path):
    from probe.sdk import session_marker

    blocker = tmp_path / "a-file"
    blocker.write_text("")
    monkeypatch.setattr(session_marker, "state_dir", lambda: blocker / "state")

    with upgrading._pi_update_lock() as held:
        assert held


@pytest.mark.skipif(not Path("/proc/self/cmdline").exists(), reason="Linux /proc only")
@pytest.mark.parametrize("ps", ["missing", "refuses -U"])
def test_without_a_working_ps_a_running_pi_shows_up_in_proc(monkeypatch, ps):
    """A slim container has no `ps`, and busybox's refuses `-U`: reading pi as
    not running there would `pi update` under it."""

    def no_ps(command, **kwargs):
        if ps == "missing":
            raise FileNotFoundError("ps")
        return subprocess.CompletedProcess(command, 1, "", "ps: unrecognized option: U")

    monkeypatch.setattr(upgrading.subprocess, "run", no_ps)
    pi = subprocess.Popen(["pi", "30"], executable="/bin/sleep")  # a process titled `pi`
    try:
        assert upgrading._pi_running()
    finally:
        pi.kill()
        pi.wait()
