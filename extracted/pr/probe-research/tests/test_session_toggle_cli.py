"""`probe session toggle`: flip between `on` and `read`.

The command exists so nobody has to know which way the switch points before
throwing it -- not the researcher in a shell, and not the model reconciling a
machine where the skill's activation hook is absent (before this, that path
made the model CHOOSE between `track` and `untrack` from its own reading of
prior state, which is exactly the judgment a toggle removes).

The one property that matters: `toggle` resolves "current" identically to
`status` -- explicit signal first, machine default otherwise -- so toggling
can never disagree with what the status line was showing.
"""

from __future__ import annotations

import json

import pytest

from probe import cli
from probe.sdk import session_marker

SESSION_ID = "cli-toggle-1111-2222-333333333333"


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    """Session id from the agent env, marker state and config isolated."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_CONFIG_PATH", raising=False)
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SESSION_ID)
    monkeypatch.delenv("CODEX_THREAD_ID", raising=False)
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)


def _toggle(capsys) -> dict:
    assert cli.main(["session", "toggle"]) in (0, None)
    return json.loads(capsys.readouterr().out)


def test_toggle_flips_both_ways_from_undecided(isolated, capsys):
    """Undecided reads as the machine default (ships `full`), and the lap is
    TWO: `on` and `read` are the only states the bare switch visits, and each
    answer names what it left.

    `off` is deliberately not on this lap -- see
    `test_the_bare_switch_never_lands_on_off`."""
    assert session_marker.session_state(SESSION_ID) is None

    # The JSON says the WORDS; the marker keeps the stored spelling. Both are
    # checked on every press, because that gap is the whole compat story.
    for was, now, stored in (
        ("on", "read", "read-only"),
        ("read", "on", "full"),
        ("on", "read", "read-only"),
    ):
        out = _toggle(capsys)
        assert (out["was"], out["state"]) == (was, now)
        assert session_marker.session_state(SESSION_ID) == stored

    # ...and the two-valued file the old clients read came back with it.
    assert session_marker.tracking_signal(SESSION_ID) == "off"


def test_the_bare_switch_never_lands_on_off(isolated, capsys):
    """`off` is reachable only by TYPING it, and one press leaves it for `read`.

    The bare switch is thrown without reading anything. Under `off` an agent
    makes no Probe calls, so it cannot find prior work AND cannot know what it
    missed -- a state nobody should arrive in by one press too many, because
    nothing about the session afterwards shows that they did.
    """
    for _ in range(6):
        out = _toggle(capsys)
        assert out["state"] != "off", "a bare press must never land on off"

    # Typed, it goes there.
    assert cli.main(["session", "state", "off"]) in (0, None)
    capsys.readouterr()
    assert session_marker.session_state(SESSION_ID) == "off"

    # And one press leaves for `read` -- the smallest change that gives back
    # what `off` took away -- not for `on`, which would also resume recording
    # nobody asked to resume.
    out = _toggle(capsys)
    assert (out["was"], out["state"]) == ("off", "read")
    assert session_marker.session_state(SESSION_ID) == "read-only"


def test_toggle_agrees_with_status_about_current(isolated, capsys):
    """The resolution rule is shared, not coincidentally similar: whatever
    `status` says the state is, `toggle` advances from exactly that."""
    assert cli.main(["session", "status"]) in (0, None)
    before = json.loads(capsys.readouterr().out)["state"]

    out = _toggle(capsys)
    assert out["was"] == before
    # `before` is a WORD off the JSON; `next_state` walks the stored names, so
    # the comparison goes back through the one mapping rather than a second
    # copy of the cycle written out here.
    landed = session_marker.state_label(
        session_marker.next_state(session_marker.state_for_label(before))
    )
    assert out["state"] == landed

    assert cli.main(["session", "status"]) in (0, None)
    after = json.loads(capsys.readouterr().out)
    assert after["state"] == landed
    assert after["decided_by"] == "session"


def test_toggle_after_explicit_untrack_advances_from_read_only(isolated, capsys):
    """`untrack` is read-only, not the hard off, so the next press lands on on.

    That is the whole point of keeping the alias pointed at read-only: what it
    has always done is stop RECORDING, and a researcher who typed it did not ask
    to stop searching. The press back out of it must not overshoot into `off`,
    which is a state they never asked for at all."""
    assert cli.main(["session", "untrack"]) in (0, None)
    capsys.readouterr()
    assert session_marker.session_state(SESSION_ID) == "read-only"
    out = _toggle(capsys)
    assert (out["was"], out["state"]) == ("read", "on")


def test_explicit_session_option_wins_over_env(isolated, capsys):
    other = "cli-toggle-9999-8888-777777777777"
    assert cli.main(["session", "toggle", "--session", other]) in (0, None)
    out = json.loads(capsys.readouterr().out)
    assert out["session_id"] == other
    assert session_marker.tracking_signal(other) == "off"
    assert session_marker.tracking_signal(SESSION_ID) is None


@pytest.mark.parametrize(
    ("command", "existing"),
    [("track", "off"), ("untrack", "on")],
)
def test_session_switch_fails_when_the_authoritative_state_did_not_change(
    isolated, monkeypatch, capsys, command, existing
):
    assert session_marker.set_tracking(SESSION_ID, existing == "on")
    monkeypatch.setattr(session_marker, "set_tracking", lambda _session, _on: False)

    assert cli.main(["session", command]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "could not set tracking" in captured.err
    assert session_marker.tracking_signal(SESSION_ID) == existing


@pytest.mark.parametrize("command", [["toggle"], ["state", "off"]])
def test_state_moving_commands_fail_when_the_write_did_not_land(
    isolated, monkeypatch, capsys, command
):
    """The same contract on the three-valued path. A host switch only has an
    exit code, so success must mean the authoritative READ-BACK agrees --
    otherwise a caller announces an opt-out that is not in force."""
    assert session_marker.set_session_state(SESSION_ID, "full")
    monkeypatch.setattr(
        session_marker, "set_session_state", lambda _session, _state: False
    )

    assert cli.main(["session", *command]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "could not set probe state" in captured.err
    assert session_marker.session_state(SESSION_ID) == "full"


def test_inherit_is_refused_without_folder(isolated, capsys):
    assert cli.main(["session", "default", "inherit"]) == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "expected 'on', 'read' or 'off'" in captured.err


def test_machine_default_without_folder_keeps_existing_json(isolated, capsys):
    assert cli.main(["session", "default"]) in (0, None)
    assert json.loads(capsys.readouterr().out) == {
        "machine_default": "on",
        "config": str(session_marker.config_path()),
        "note": "per-session `probe session state` overrides this",
    }

    assert cli.main(["session", "default", "off"]) in (0, None)
    assert json.loads(capsys.readouterr().out) == {
        "machine_default": "off",
        "config": str(session_marker.config_path()),
    }


def test_status_preserves_machine_default_label_without_a_folder_override(
    isolated, capsys
):
    assert cli.main(["session", "status"]) in (0, None)

    out = json.loads(capsys.readouterr().out)
    assert out["signal"] is None
    assert out["tracking"] is True
    assert out["decided_by"] == "machine default"


def test_status_names_an_environment_default(isolated, monkeypatch, capsys):
    monkeypatch.setenv("PROBE_SESSION_TRACKING", "off")

    assert cli.main(["session", "status"]) in (0, None)

    out = json.loads(capsys.readouterr().out)
    assert out["signal"] is None
    assert out["tracking"] is False
    assert out["decided_by"] == "environment"


def test_initialize_is_hidden_from_researcher_facing_help(isolated, capsys):
    """The host bridge must not look like a fourth way to move the switch."""
    assert cli.main(["session", "--help"]) in (0, None)

    help_text = " ".join(capsys.readouterr().out.split())
    assert "initialize" not in help_text


def test_status_in_the_daemon_state_lists_the_agents_own_writes(isolated, capsys):
    """An agent unsure whether a write is its own reads the gate's list here.

    In a live trial the agent spent 2.5 of 8.5 minutes reading the gate's source
    because no surface named the list; `daemon.agent_writes` IS that list, so it
    cannot drift from what the gate lets through.
    """
    import time

    assert session_marker.set_session_state(SESSION_ID, session_marker.STATE_DAEMON)
    lease = session_marker.lease_path(SESSION_ID)
    lease.parent.mkdir(parents=True, exist_ok=True)
    now = time.time()
    lease.write_text(
        json.dumps(
            {"v": session_marker.LEASE_VERSION, "writer": "daemon", "pid": 1,
             "expires_at": now + 60, "renewed_at": now, "reason": None}
        )
    )

    assert cli.main(["session", "status"]) in (0, None)

    out = json.loads(capsys.readouterr().out)
    assert out["writes_allowed"] is False
    daemon = out["daemon"]
    assert daemon["status"] == session_marker.DAEMON_LIVE
    assert daemon["agent_writes"] == sorted(session_marker.DAEMON_AGENT_WRITES)
    assert {"exec", "run start", "run end", "log"} <= set(daemon["agent_writes"])
    # Daemon v2: the daemon creates the containers runs are filed in.
    assert not {"project create", "experiment create", "group create"} & set(daemon["agent_writes"])
    assert daemon["agent_writes_in_run"] == ["artifact add"]
    assert "--directed" in daemon["directed"]


def test_status_outside_the_daemon_state_has_no_daemon_block(isolated, capsys):
    assert session_marker.set_session_state(SESSION_ID, session_marker.STATE_FULL)
    assert cli.main(["session", "status"]) in (0, None)
    assert json.loads(capsys.readouterr().out)["daemon"] is None
