"""The invariant, end to end through the CLI: tracked implies captured."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from probe.cli import capture_state
from probe.cli.main import app

SID = "01a06383-6f4e-751a-b94c-bcefef19938c"
runner = CliRunner()


@pytest.fixture
def pi_session(tmp_path, monkeypatch):
    monkeypatch.setenv("PI_CODING_AGENT", "true")
    monkeypatch.setenv("PI_SESSION_ID", SID)
    monkeypatch.setenv("PROBE_AGENT", "pi")
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(tmp_path / "tap-state"))
    (tmp_path / "tap-state").mkdir()
    return tmp_path


def test_status_reports_tracked_not_captured(pi_session, monkeypatch):
    monkeypatch.setattr(
        capture_state,
        "session_capture_state",
        lambda sid, source=None: capture_state.CaptureState(False, None, "not started"),
    )
    monkeypatch.setattr(
        capture_state, "ensure_capture", lambda *a, **k: capture_state.HealResult(False, "off")
    )
    result = runner.invoke(app, ["session", "status", "--session", SID])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["capture"]["running"] is False
    assert payload["capture"]["reason"] == "not started"
    assert payload["effective"] in ("tracked, not capturing session transcript", "off")


def test_status_reports_tracked_when_a_daemon_is_live(pi_session, monkeypatch):
    monkeypatch.setattr(
        capture_state,
        "session_capture_state",
        lambda sid, source=None: capture_state.CaptureState(True, 4242, "running"),
    )
    monkeypatch.setattr(
        capture_state, "ensure_capture", lambda *a, **k: capture_state.HealResult(False, "running")
    )
    result = runner.invoke(app, ["session", "status", "--session", SID])
    payload = json.loads(result.stdout)
    assert payload["capture"]["running"] is True
    assert payload["capture"]["pid"] == 4242


def test_initialize_never_heals(pi_session, monkeypatch):
    """The pi extension calls this BEFORE its own spawn. See the spec."""
    calls = []
    monkeypatch.setattr(
        capture_state,
        "ensure_capture",
        lambda *a, **k: calls.append(a) or capture_state.HealResult(False, "off"),
    )
    monkeypatch.setattr(
        capture_state,
        "session_capture_state",
        lambda sid, source=None: capture_state.CaptureState(False, None, "not started"),
    )
    result = runner.invoke(
        app, ["session", "initialize", "--session", SID, "--cwd", str(pi_session)]
    )
    assert result.exit_code == 0
    assert calls == []
    assert json.loads(result.stdout)["capture"]["reason"] == "not started"


def test_status_heals(pi_session, monkeypatch):
    calls = []
    monkeypatch.setattr(
        capture_state,
        "ensure_capture",
        lambda *a, **k: calls.append(a) or capture_state.HealResult(True, "running"),
    )
    monkeypatch.setattr(
        capture_state,
        "session_capture_state",
        lambda sid, source=None: capture_state.CaptureState(False, None, "not started"),
    )
    runner.invoke(app, ["session", "status", "--session", SID])
    assert len(calls) == 1


# --- the strand-ai regression ---------------------------------------------
#
# Tenant strand-ai (pi-only), 2026-09-02/03: six sessions reported
# `tracking: true` and lost their transcripts. The package WAS installed --
# globally, in `~/.pi/agent/settings.json`, with `"extensions": []` -- so pi
# loaded our skills and our MCP manifest and never `index.ts`. Nothing of ours
# ran in-process, nothing spawned a daemon, and nothing said so. The sessions
# ran in fresh git worktrees carrying a folder tracking default and no
# `.pi/settings.json` of their own.
#
# Reproduced here as a CONFIGURATION, not as a mock of the outcome: the
# settings file, the filter, the worktree, the folder default, a paired tap
# state directory and no pid file anywhere. The only thing stubbed is the
# actual process spawn.

STRAND_AI_WORKTREE = ("rosetta-workers", "visium")


@pytest.fixture
def strand_ai(tmp_path, monkeypatch):
    """The exact machine shape that lost six transcripts."""
    import os
    import sys

    from probe.cli import pi_config

    agent_dir = tmp_path / "pi-agent"
    agent_dir.mkdir()
    # Global scope, extensions filtered to the empty list -- pi's own way of
    # saying "this package's skills yes, its code no".
    (agent_dir / "settings.json").write_text(
        json.dumps(
            {"packages": [{"source": pi_config.MIRROR_GIT_SOURCE, "extensions": []}]}
        ),
        encoding="utf-8",
    )

    worktree = tmp_path.joinpath(*STRAND_AI_WORKTREE)
    (worktree / ".probe").mkdir(parents=True)
    # A folder default, NOT a session signal: no extension ever ran to seed
    # one, and this is what made every surface answer "tracking: true".
    (worktree / ".probe" / "config.json").write_text(
        json.dumps({"defaults": {"session_tracking": "on"}}), encoding="utf-8"
    )

    transcript = tmp_path / "session.jsonl"
    transcript.write_text('{"type":"session"}\n', encoding="utf-8")

    tap_state = tmp_path / "tap-state"
    tap_state.mkdir()
    (tap_state / ".token").write_text("probe_ing_test", encoding="utf-8")

    tap_root = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap"
    assert (tap_root / "tap" / "__init__.py").is_file(), "the tap package moved"

    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(agent_dir))
    monkeypatch.setenv("PI_CODING_AGENT", "true")
    monkeypatch.setenv("PI_SESSION_ID", SID)
    monkeypatch.setenv("PI_SESSION_FILE", str(transcript))
    monkeypatch.setenv("PROBE_AGENT", "pi")
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(tap_state))
    monkeypatch.setenv("PROBE_PI_TAP_ROOT", str(tap_root))
    # This machine's own state and preferences must not decide the outcome.
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe-config.json"))
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.chdir(worktree)

    spawned: list[tuple[list[str], dict]] = []
    monkeypatch.setattr(
        capture_state, "_run", lambda argv, env: spawned.append((argv, env)) or 0
    )

    return {
        "worktree": worktree,
        "transcript": transcript,
        "tap_state": tap_state,
        "tap_root": tap_root,
        "spawned": spawned,
        "python": sys.executable,
        "pid_file": Path("/tmp") / f"probe-research-tap-watcher-{SID}.pid",
        "os": os,
    }


def test_the_strand_ai_shape_is_installed_but_filtered(strand_ai):
    """The premise, asserted rather than assumed.

    If pi ever stopped reporting this entry as installed, the heal below would
    refuse for the RIGHT reason on the WRONG grounds and the fixture would go
    green while capture stayed broken.
    """
    from probe.cli import pi_config

    worktree = strand_ai["worktree"]
    assert pi_config.package_entry_installed(cwd=worktree) is True
    entry = pi_config.merged_package_entry(cwd=worktree)
    assert entry.scope == "global"
    assert entry.extension_filtered_out is True
    assert not (worktree / ".pi" / "settings.json").exists()


def test_the_strand_ai_shape_has_no_daemon_before_the_heal(strand_ai):
    state = capture_state.session_capture_state(SID, "pi")
    assert state.running is False
    # Not `not installed`: the tap IS installed and paired. The session simply
    # has nothing watching it, which is the fact the old surfaces hid.
    assert state.reason == "not started"


def test_status_from_the_worktree_heals_and_refuses_to_say_tracked(strand_ai):
    """One `probe session status`, exactly as the agent ran it, does both halves.

    The heal fires (a real `tap start` argv, with pi's source and the tap on
    PYTHONPATH), and the surface still refuses to answer plain `tracked` while
    nothing is listening -- the spawn is in flight, not confirmed.
    """
    result = runner.invoke(app, ["session", "status", "--session", SID])
    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)

    # What the customer saw, and what it now says alongside it.
    assert payload["tracking"] is True
    assert payload["decided_by"] == "folder default"
    assert payload["capture"] == {"running": False, "pid": None, "reason": "not started"}
    assert payload["effective"] == "tracked, not capturing session transcript"

    assert len(strand_ai["spawned"]) == 1
    argv, env = strand_ai["spawned"][0]
    assert argv == [
        strand_ai["python"],
        "-m",
        "tap",
        "start",
        "--session-id",
        SID,
        "--cwd",
        str(strand_ai["worktree"]),
        "--transcript",
        str(strand_ai["transcript"]),
    ]
    assert env["PROBE_TAP_SOURCE"] == "pi"
    assert env["PYTHONPATH"].split(strand_ai["os"].pathsep)[0] == str(strand_ai["tap_root"])
    assert "started transcript capture" in result.stderr


def test_status_says_tracked_once_the_daemon_the_heal_started_is_live(strand_ai, monkeypatch):
    """The other end of the same invariant, and no second spawn for it."""
    monkeypatch.setattr(capture_state, "_looks_like_the_uploader", lambda pid: True)
    pid_file = strand_ai["pid_file"]
    pid_file.write_text(str(strand_ai["os"].getpid()), encoding="utf-8")
    try:
        result = runner.invoke(app, ["session", "status", "--session", SID])
    finally:
        pid_file.unlink(missing_ok=True)

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["capture"]["running"] is True
    assert payload["capture"]["reason"] == "running"
    assert payload["effective"] == "tracked"
    assert strand_ai["spawned"] == []


def test_a_second_status_inside_the_window_does_not_spawn_again(strand_ai):
    """The ten-minute heal marker, on the surface an agent actually calls."""
    runner.invoke(app, ["session", "status", "--session", SID])
    runner.invoke(app, ["session", "status", "--session", SID])
    assert len(strand_ai["spawned"]) == 1
    assert (strand_ai["tap_state"] / "heal" / SID).exists()


def test_removing_the_package_entirely_is_not_healed(strand_ai):
    """A filtered extension and a removed package must stay different cases.

    Consent is the package entry, not the filter. Reinstalling is a wizard
    action; a tracking signal never reverses an explicit opt-out.
    """
    settings = Path(strand_ai["os"].environ["PI_CODING_AGENT_DIR"]) / "settings.json"
    settings.write_text(json.dumps({"packages": []}), encoding="utf-8")
    result = capture_state.ensure_capture(SID, cwd=strand_ai["worktree"], source="pi")
    assert result == capture_state.HealResult(False, "not installed")
    assert strand_ai["spawned"] == []


def test_an_ephemeral_session_says_why_not_just_that_nothing_runs(pi_session, monkeypatch):
    """The probe reads a pid file, so every refusal it cannot see looks like
    a crashed daemon. The heal knows the real reason; the surface must show it.

    Found by the live matrix: a `--no-session` pi session reported
    `not started`, pointing at a daemon that never existed, where the spec
    promises `no session file`.
    """
    monkeypatch.setattr(
        capture_state,
        "session_capture_state",
        lambda sid, source=None: capture_state.CaptureState(False, None, "not started"),
    )
    monkeypatch.setattr(
        capture_state,
        "ensure_capture",
        lambda *a, **k: capture_state.HealResult(False, "no session file"),
    )
    result = runner.invoke(app, ["session", "status", "--session", SID])
    payload = json.loads(result.stdout)
    assert payload["capture"]["reason"] == "no session file"


def test_a_heal_reason_outside_the_vocabulary_never_reaches_the_surface(pi_session, monkeypatch):
    """`off` and `not applicable` are not capture states.

    The first is already carried by `effective`; the second says this is not
    pi. Letting either through would put a word on the status line that the
    three renderers have no rendering for.
    """
    monkeypatch.setattr(
        capture_state,
        "session_capture_state",
        lambda sid, source=None: capture_state.CaptureState(False, None, "not started"),
    )
    for refusal in ("off", "not applicable"):
        monkeypatch.setattr(
            capture_state,
            "ensure_capture",
            lambda *a, _r=refusal, **k: capture_state.HealResult(False, _r),
        )
        payload = json.loads(runner.invoke(app, ["session", "status", "--session", SID]).stdout)
        assert payload["capture"]["reason"] == "not started"
