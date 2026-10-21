"""`probe capy sync`: what an old Capy timer runs after Capy support was removed.

It must take down everything the removed `probe capy connect` left -- the
capture credential (revoked first, with the server it was paired to, while
its token can still authenticate), the saved Capy key, the thread mirror and
its upload journal, then the timer itself, last -- touch nothing else, never
raise, and be a no-op after.
"""

from __future__ import annotations

import http.client
import json
import sqlite3
import urllib.error
from pathlib import Path
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

from probe.cli import capy_retire

SESSION = "4b0e5a63-6a7c-5f2c-9f3e-0c9a1d2b3c4d"


def _journal(root: Path, name: str, session_id: str) -> Path:
    folder = root / name
    folder.mkdir(parents=True)
    with sqlite3.connect(folder / "state.sqlite3") as db:
        db.execute("CREATE TABLE sessions(session_id TEXT PRIMARY KEY, state TEXT NOT NULL)")
        db.execute("CREATE TABLE pending(session_id TEXT PRIMARY KEY, body BLOB NOT NULL, digest TEXT NOT NULL)")
        db.execute("INSERT INTO sessions VALUES (?, 'open')", (session_id,))
    return folder


@pytest.fixture
def leftovers(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict:
    home = Path.home()
    state = home / capy_retire.STATE_ROOT
    plugin = state / "probe-research-tap"
    plugin.mkdir(parents=True)
    (plugin / ".token").write_text("capture-token\n")
    (plugin / ".config").write_text('{"api_base_url": "https://config.example"}')
    (plugin / "capy.json").write_text('{"api_key": "secret", "base_url": "https://paired.example/"}')
    (state / "threads").mkdir()
    (state / "threads" / f"{SESSION}.jsonl").write_text("{}\n")
    plist = home / "Library" / "LaunchAgents" / f"{capy_retire.LAUNCHD_LABEL}.plist"
    plist.parent.mkdir(parents=True)
    plist.write_text("<plist/>")
    units = home / ".config" / "systemd" / "user"
    units.mkdir(parents=True)
    for suffix in (".timer", ".service"):
        (units / f"{capy_retire.TIMER_NAME}{suffix}").write_text("[Unit]\n")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(home / ".config"))
    # A shell pointing Probe elsewhere must not pick the revoke's server.
    monkeypatch.setenv("PROBE_BASE_URL", "https://elsewhere.example")
    journals = tmp_path / "transcripts"
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(journals))
    capy_journal = _journal(journals, "capy-hash", SESSION)
    other_journal = _journal(journals, "claude-hash", "11111111-2222-3333-4444-555555555555")

    calls: dict = {"run": [], "revoked": []}

    def run(argv):
        # Records whether the folder holding the key was already gone.
        calls["run"].append((argv, state.exists()))
        return True

    monkeypatch.setattr(capy_retire, "_run", run)
    monkeypatch.setattr(capy_retire.shutil, "which", lambda name: f"/usr/bin/{name}")

    class _Response:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    monkeypatch.setattr(
        "probe.cli.capabilities._credential_opener",
        lambda: SimpleNamespace(open=lambda request, timeout: calls["revoked"].append(
            (request.full_url, request.get_header("Authorization"), (plugin / ".token").exists())
        ) or _Response()),
    )
    return {"state": state, "plist": plist, "units": units, "calls": calls,
            "capy_journal": capy_journal, "other_journal": other_journal}


@pytest.mark.parametrize("system", ["Darwin", "Linux"])
def test_retire_revokes_with_the_paired_server_then_removes_everything(leftovers, monkeypatch, system):
    monkeypatch.setattr(capy_retire.platform, "system", lambda: system)
    lines = capy_retire.retire()
    assert lines == list(capy_retire.REMOVED)
    assert leftovers["calls"]["revoked"] == [("https://paired.example/agent-tap/revoke", "Bearer capture-token", True)]
    assert not leftovers["state"].exists()
    assert not leftovers["plist"].exists()
    assert not any(leftovers["units"].iterdir())
    assert not leftovers["capy_journal"].exists()
    assert leftovers["other_journal"].exists(), "another agent's journal is not Capy's"
    commands = [argv[0] for argv, _ in leftovers["calls"]["run"]]
    if system == "Darwin":
        assert commands == ["launchctl"]
    else:
        assert commands == ["systemctl", "systemctl"]
    assert capy_retire.retire() == []


def test_the_launchd_job_goes_last(leftovers, monkeypatch):
    """Removing the job stops the run doing it: everything else first."""
    monkeypatch.setattr(capy_retire.platform, "system", lambda: "Darwin")
    capy_retire.retire()
    assert leftovers["calls"]["run"] == [(["launchctl", "remove", capy_retire.LAUNCHD_LABEL], False)]


@pytest.mark.parametrize("failure", ["offline", "bad-status", "no-scheme"])
def test_a_failed_revoke_still_takes_everything_down(leftovers, monkeypatch, failure):
    monkeypatch.setattr(capy_retire.platform, "system", lambda: "Darwin")
    plugin = leftovers["state"] / "probe-research-tap"
    if failure == "no-scheme":
        (plugin / "capy.json").write_text('{"base_url": "paired.example"}')
    else:
        error = urllib.error.URLError("offline") if failure == "offline" else http.client.BadStatusLine("x")

        def fail(request, timeout):
            raise error

        monkeypatch.setattr("probe.cli.capabilities._credential_opener", lambda: SimpleNamespace(open=fail))
    assert capy_retire.retire() == list(capy_retire.REMOVED)
    assert not leftovers["state"].exists()
    assert not leftovers["plist"].exists()


def test_a_step_that_fails_is_reported_and_the_rest_still_run(leftovers, monkeypatch):
    monkeypatch.setattr(capy_retire.platform, "system", lambda: "Darwin")

    def refuse(path, *a, **k):
        raise PermissionError(path)

    monkeypatch.setattr(capy_retire.shutil, "rmtree", refuse)
    lines = capy_retire.retire()
    assert len(lines) == 1 and lines[0].startswith("! Some of Capy's leftovers could not be removed")
    assert str(leftovers["state"]) in lines[0]
    assert not leftovers["plist"].exists(), "the timer step still ran"


def test_an_environment_override_is_never_deleted(leftovers, monkeypatch, tmp_path):
    """The removed row's override variables are not followed: a path in someone's
    environment (a shared folder, the project) keeps every file."""
    shared = tmp_path / "research"
    shared.mkdir()
    (shared / f"{SESSION}.jsonl").write_text("{}\n")
    (shared / ".token").write_text("someone else's\n")
    monkeypatch.setenv("PROBE_CAPY_THREADS_DIR", str(shared))
    monkeypatch.setenv("PROBE_CAPY_TAP_PLUGIN_DIR", str(shared))
    monkeypatch.setattr(capy_retire.platform, "system", lambda: "Darwin")
    capy_retire.retire()
    assert sorted(p.name for p in shared.iterdir()) == [".token", f"{SESSION}.jsonl"]


def test_a_symlinked_folder_loses_the_link_not_its_target(monkeypatch, tmp_path):
    target = tmp_path / "elsewhere"
    target.mkdir()
    (target / "keep.txt").write_text("mine\n")
    link = Path.home() / capy_retire.STATE_ROOT
    link.parent.mkdir(parents=True)
    link.symlink_to(target)
    monkeypatch.setattr(capy_retire, "_run", lambda argv: pytest.fail(f"ran {argv}"))
    assert capy_retire.retire() == list(capy_retire.REMOVED)
    assert not link.is_symlink() and (target / "keep.txt").exists()


def test_nothing_to_remove_touches_nothing(monkeypatch):
    monkeypatch.setattr(capy_retire, "_run", lambda argv: pytest.fail(f"ran {argv}"))
    assert capy_retire.retire() == []


@pytest.mark.parametrize("command", ["sync", "disconnect"])
def test_the_old_commands_take_it_down_and_name_the_crontab_once(leftovers, monkeypatch, command):
    from probe.cli.main import app

    monkeypatch.setattr(capy_retire.platform, "system", lambda: "Darwin")
    first = CliRunner().invoke(app, ["capy", command, "--quiet"])
    assert first.exit_code == 0, first.output
    assert not leftovers["state"].exists()
    assert "crontab" in first.stderr
    again = CliRunner().invoke(app, ["capy", command, "--quiet"])
    assert again.exit_code == 0 and again.output == "", "a crontab line runs it every 10 minutes: no mail after the first"


def test_the_shim_is_hidden_from_help():
    import typer.main

    from probe.cli.main import app

    assert typer.main.get_command(app).commands["capy"].hidden
    assert "capy" not in CliRunner().invoke(app, ["--help"]).output


def test_an_update_takes_it_down(leftovers, monkeypatch):
    from probe.cli import updater, upgrading

    monkeypatch.setattr(capy_retire.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(upgrading.updater, "fetch_latest", lambda base: {})
    monkeypatch.setattr(upgrading.updater, "detect_install", lambda: updater.Install(updater.Method.EDITABLE))
    monkeypatch.setattr(
        upgrading.updater,
        "upgrade_cli",
        lambda i, c, t: updater.CliResult(ran=False, ok=True, changed=False, before=c, after=c, message="skipped"),
    )
    outcome = upgrading.perform_update(base_url="https://x", include_plugin=False)
    assert not leftovers["state"].exists() and not leftovers["plist"].exists()
    assert any(capy_retire.REMOVED[0] in line for line in outcome.lines)


def test_sign_out_takes_it_down(leftovers, monkeypatch):
    from probe.cli import setup

    monkeypatch.setattr(capy_retire.platform, "system", lambda: "Darwin")
    lines = setup.release_credentials()
    assert not leftovers["state"].exists()
    assert capy_retire.REMOVED[0] in lines


def test_an_agent_with_no_daemon_profile_has_no_failing_recorder_row(monkeypatch):
    """The desktop app's "Setup did not finish": an agent outside the daemon's
    reach got a row that could never be ok, so the switch never read complete."""
    import sys

    import probe.cli.main  # noqa: F401
    from probe.cli import json_events
    from probe.cli import setup as wizard
    from probe.sdk import session_marker

    main = sys.modules["probe.cli.main"]

    rows = []
    monkeypatch.setattr(json_events, "enabled", lambda: True)
    monkeypatch.setattr(json_events, "agent_result", lambda source, **row: rows.append((source, row)))
    monkeypatch.setattr(session_marker, "recorder", lambda source: session_marker.RECORDER_DAEMON)
    recorder_source = wizard.RECORDER_SOURCES[0]
    caps = {recorder_source: SimpleNamespace(configured=True), "agent_without_a_profile": SimpleNamespace(configured=True)}
    main._record_recorder(session_marker.RECORDER_DAEMON, caps, ["Agent keeps recording itself: it has no daemon profile yet."])
    assert [source for source, _ in rows] == [recorder_source]
    assert all(row["ok"] for _, row in rows)
    assert json.dumps([row for _, row in rows])  # plain data
