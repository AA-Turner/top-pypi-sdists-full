"""Every surface that tells the agent who writes what in the `daemon` state says
the same thing, and says what the CLI gate actually does.

THE ONE FACT: you launch and instrument runs, and the daemon records. The
agent's: starting runs (no project needed), the run's own data and `run end`.
The daemon's: everything else, the project, experiment and sweep group a run is
filed in included. A write the researcher asks for takes `--directed`.

In a live trial an agent spent 2.5 of 8.5 minutes reading the gate's source,
because six texts described the split six ways and none matched the gate's
list. The surfaces:

    S2  the flip notice             tracking_guard.FLIP_NOTICE["daemon"], pi DAEMON_LIVE_NOTICE
    S3  the session-start context   session_marker.DAEMON_CONTEXT, pi DAEMON_CONTEXT
    (S4, the `probe` skill's `daemon` row, is gone: the daemon is the wizard's
    "Who records", not a switch position; Richard 2026-09-29.)
    (S5, track-work's section 0, is gone: in the daemon profile the main agent
    has no track-work, and the writer's version carries filing; daemon reads 09-28.)
    S6  the CLI gate's refusal      session_marker.DENY_REASON_DAEMON
    S7  the after-the-fact notice   tracking_guard.MESSAGE_DAEMON

S1, the CLAUDE.md pointer paragraph (`agent_rules.POINTER_BODY`), is the owner's
own wording and is deliberately not held to this test yet. pi's copies are
pinned to the Python ones verbatim by `test_companion_pi_parity.py`; here they
are held to the same nouns so a drift in either shows up by name.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from probe.sdk import session_marker
from tests.test_companion_pi_parity import HOOKS, _load
from tests.test_companion_pi_parity import _ts_string as _pi_string

AGENT = Path(__file__).resolve().parents[1]


def _surfaces() -> dict[str, str]:
    guard = _load("_guard_split_texts", HOOKS / "tracking_guard.py")
    version_check = _load("_vc_split_texts", HOOKS / "version_check.py")
    return {
        "S2 flip notice": guard.FLIP_NOTICE["daemon"],
        "S2 pi flip notice": _pi_string("DAEMON_LIVE_NOTICE"),
        "S3 session start": version_check.DAEMON_CONTEXT,
        "S3 pi session start": _pi_string("DAEMON_CONTEXT"),
        "S6 gate refusal": session_marker.DENY_REASON_DAEMON,
        "S7 after the fact": guard.MESSAGE_DAEMON,
    }


SURFACES = sorted(_surfaces())


@pytest.mark.parametrize("surface", SURFACES)
def test_every_surface_names_what_the_agent_creates_and_the_escape(surface):
    text = _surfaces()[surface]
    for word in ("project", "experiment", "group", "--directed"):
        assert word in text, f"{surface} does not name {word!r}: {text!r}"


@pytest.mark.parametrize("surface", ["S2 flip notice", "S2 pi flip notice", "S3 session start",
                                     "S3 pi session start", "S6 gate refusal"])
def test_the_long_surfaces_say_the_agent_ends_its_runs(surface):
    assert "run end" in _surfaces()[surface], surface


@pytest.mark.parametrize("surface", SURFACES)
def test_no_em_dashes(surface):
    assert "\u2014" not in _surfaces()[surface], surface


@pytest.mark.parametrize("surface", ["S2 flip notice", "S2 pi flip notice", "S3 session start",
                                     "S3 pi session start", "S7 after the fact"])
def test_no_surface_hands_the_agent_the_containers(surface):
    """Daemon v2 (D2, S11): the agent launches and instruments runs; creating the
    project, experiment and sweep group is the daemon's, and the gate refuses the
    agent those creates (see the next test). A text that still says "yours: create
    the project" sends the agent into a refusal every time."""
    text = " ".join(_surfaces()[surface].split())
    yours = text.split("Yours:", 1)[1].split("The daemon's:", 1)[0] if "Yours:" in text else ""
    for word in ("creat", "experiment", "group"):
        assert word not in yours, f"{surface} gives the agent {word!r}: {yours!r}"
    assert "the daemon" in text.lower() and "creat" in text, surface


def test_the_flip_carries_the_whole_session_start_text():
    """A session that moves to `daemon` mid-conversation never sees SessionStart."""
    surfaces = _surfaces()
    assert surfaces["S3 session start"] in surfaces["S2 flip notice"]
    assert surfaces["S3 session start"] == session_marker.DAEMON_CONTEXT


def test_the_words_match_the_gate():
    """What the texts call the agent's is what the gate lets through, and what they
    call the daemon's it refuses. A text and a list that disagree is the bug."""
    agent = session_marker.DAEMON_AGENT_WRITES
    for key in ("exec", "run start", "run child", "run fork", "run end", "log", "snapshot",
                "span add", "trial add"):
        assert key in agent, key
    # Daemon v2 (D2, S11): runs start floating; the containers are the daemon's.
    for matched in ("probe notes push", "probe artifact add", "probe paper add", "probe run tag",
                    "probe run set", "probe edge add", "probe group set", "probe project create",
                    "probe experiment create", "probe group create"):
        assert not session_marker.daemon_allows_agent(matched), matched
    # A file the run attaches itself is the run's own data (see DAEMON_RUN_WRITES).
    assert session_marker.DAEMON_RUN_WRITES == frozenset({"artifact add"})
