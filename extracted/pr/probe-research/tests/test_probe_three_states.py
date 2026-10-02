"""The four things the three-state switch must never get wrong.

Each of these guards a failure that is SILENT in production -- nothing errors,
nothing logs, and the researcher finds out from the dashboard or not at all.
They are grouped here rather than spread through the four existing tracking
suites because they are about the STATE MACHINE and its migration, not about
any one surface's behaviour, and because a reviewer asking "what stops the bad
thing" should find them in one file.

    1. An older client must never read a new opt-out as consent.
    2. One keypress must advance exactly one step, however many shapes it is
       seen in.
    3. `off` must actually refuse an MCP read, in every spelling of the name.
    4. An existing `off` must migrate to read-only, never to the new `off`.
"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

AGENT_ROOT = Path(__file__).resolve().parents[1]
PLUGIN = AGENT_ROOT / "plugins" / "probe-research"
SESSION_ID = "11111111-2222-3333-4444-555555555555"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    hooks_dir = str(path.parent)
    added = hooks_dir not in sys.path
    if added:
        sys.path.insert(0, hooks_dir)
    try:
        spec.loader.exec_module(module)
    finally:
        if added:
            sys.path.remove(hooks_dir)
    return module


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_CONFIG_PATH", raising=False)
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.delenv("PROBE_SESSION_STATE", raising=False)
    return tmp_path


@pytest.fixture
def marker(env):
    return _load("_marker_three_state", PLUGIN / "hooks" / "_session_marker.py")


@pytest.fixture
def guard(env):
    return _load("_guard_three_state", PLUGIN / "hooks" / "tracking_guard.py")


def _run(guard, monkeypatch, capsys, payload) -> str:
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    guard.main()
    return capsys.readouterr().out


# ---------------------------------------------------------------------------
# 1. AN OLDER CLIENT MUST NEVER READ A NEW OPT-OUT AS CONSENT.
# ---------------------------------------------------------------------------


def _as_an_old_client_would(marker, session_id: str) -> bool:
    """What a pre-three-state `is_tracking` resolves to, re-implemented.

    Deliberately a COPY of the old logic rather than a call into the current
    module: the thing under test is what code we no longer control does with
    bytes we write today, and calling today's reader would test nothing.
    Lifted from `tracking_signal` + `is_tracking` as they shipped:

        read <sid>.tracking; "on" -> True, "off" -> False
        anything else, or no file -> the machine default -> DEFAULT_TRACKING
    """
    try:
        value = (
            marker.tracking_signal_path(session_id)
            .read_text(encoding="utf-8")
            .strip()
            .lower()
        )
    except OSError:
        value = None
    if value == "on":
        return True
    if value == "off":
        return False
    if marker._legacy_off_path(session_id).is_file():
        return False
    return marker.DEFAULT_TRACKING  # ships True


@pytest.mark.parametrize("state", ["read-only", "off"])
def test_an_old_client_never_reads_a_new_opt_out_as_tracking(marker, state):
    """THE ONE-WAY DOOR. Files written today are read by every version ever
    installed, and the old reader resolves anything it does not recognise --
    including a MISSING file -- to the shipped default, which is ON.

    So writing the three-valued name into `<sid>.tracking`, or cutting over to
    `<sid>.state` and leaving the old file behind, both end the same way: a
    researcher who asked for read-only or off gets recorded anyway, with
    nothing anywhere saying so. The compat write is what makes that unsayable.
    """
    assert marker.set_session_state(SESSION_ID, state)
    assert marker.session_state(SESSION_ID) == state
    assert _as_an_old_client_would(marker, SESSION_ID) is False


def test_an_old_client_still_sees_full_as_tracking(marker):
    """The other direction, so the projection is not just "always off"."""
    assert marker.set_session_state(SESSION_ID, "full")
    assert _as_an_old_client_would(marker, SESSION_ID) is True


def test_the_compat_file_is_never_left_holding_a_word_it_cannot_parse(marker):
    for state in marker.STATES:
        assert marker.set_session_state(SESSION_ID, state)
        raw = marker.tracking_signal_path(SESSION_ID).read_text(encoding="utf-8")
        assert raw.strip() in ("on", "off"), f"{state} wrote {raw!r} for old readers"


# ---------------------------------------------------------------------------
# 2. ONE KEYPRESS, ONE STEP.
# ---------------------------------------------------------------------------

_SHAPES = [
    {"hook_event_name": "UserPromptSubmit", "prompt": "/probe"},
    {
        "hook_event_name": "UserPromptSubmit",
        "prompt": "<command-name>/probe-research:probe</command-name>",
    },
    {
        "hook_event_name": "PostToolUse",
        "tool_name": "Skill",
        "tool_input": {"skill": "probe-research:probe"},
    },
]


def test_one_invocation_seen_in_every_shape_advances_exactly_one_step(
    guard, marker, monkeypatch, capsys, tmp_path
):
    """A harness delivers ONE typed command as up to three events. With two
    states a double-move cancelled out and nobody noticed; with three it
    advances twice, so one press would land two states from what was asked.

    The claim is what prevents it, and it must store the RESOLVED STATE rather
    than the direction -- a stored "advance" replayed is still two advances.
    """
    for payload in _SHAPES:
        _run(guard, monkeypatch, capsys, {**payload, "session_id": SESSION_ID,
                                          "cwd": str(tmp_path)})
        assert guard._session_marker.session_state(SESSION_ID) == "read-only"


def test_a_repeat_of_a_shape_already_seen_is_a_second_press(
    guard, monkeypatch, capsys, tmp_path
):
    """The other half: convergence is scoped to ONE invocation, so the
    researcher pressing again -- which arrives as a shape already seen -- must
    move, however soon it comes. A claim that swallowed it would be a switch
    that does nothing."""
    payload = {"hook_event_name": "UserPromptSubmit", "prompt": "/probe",
               "session_id": SESSION_ID, "cwd": str(tmp_path)}
    for expected in ("read-only", "full", "read-only", "full"):
        _run(guard, monkeypatch, capsys, payload)
        assert guard._session_marker.session_state(SESSION_ID) == expected


def test_the_bare_switch_never_lands_on_off(guard, monkeypatch, capsys, tmp_path):
    """`off` is reachable only by TYPING it. The bare switch is thrown without
    reading anything -- often mid-thought, to quiet a session -- and under `off`
    an agent makes no Probe calls at all: it cannot find prior work AND cannot
    know what it missed. Every answer afterwards is quietly poorer with nothing
    on screen to say so, which is why one press too many must not be able to
    get there."""
    payload = {"hook_event_name": "UserPromptSubmit", "prompt": "/probe",
               "session_id": SESSION_ID, "cwd": str(tmp_path)}
    for _ in range(6):
        _run(guard, monkeypatch, capsys, payload)
        assert guard._session_marker.session_state(SESSION_ID) != "off"

    # Typed, it goes there -- and one press leaves for `read-only`, the smallest
    # change that gives back what `off` took away.
    typed = dict(payload, prompt="/probe off")
    _run(guard, monkeypatch, capsys, typed)
    assert guard._session_marker.session_state(SESSION_ID) == "off"
    _run(guard, monkeypatch, capsys, payload)
    assert guard._session_marker.session_state(SESSION_ID) == "read-only"


def test_the_press_says_where_it_landed(guard, monkeypatch, capsys, tmp_path):
    """A cycle has no readout. Neither the researcher nor the model can know
    where one press landed, and leaving it to the skill's prose would make the
    model's knowledge depend on obeying prose -- which the guard refuses to do
    for the write itself."""
    payload = {"hook_event_name": "UserPromptSubmit", "prompt": "/probe",
               "session_id": SESSION_ID, "cwd": str(tmp_path)}
    for expected in ("read-only", "full", "read-only"):
        out = _run(guard, monkeypatch, capsys, payload)
        hso = json.loads(out)["hookSpecificOutput"]
        assert hso["additionalContext"] == guard.FLIP_NOTICE[expected]


def test_a_converging_shape_announces_nothing(
    guard, monkeypatch, capsys, tmp_path
):
    """Three announcements for one press would read as three presses."""
    said = [
        _run(guard, monkeypatch, capsys, {**p, "session_id": SESSION_ID,
                                         "cwd": str(tmp_path)})
        for p in _SHAPES
    ]
    assert said[0], "the sighting that resolved the target must announce"
    assert said[1:] == ["", ""], f"a converging shape spoke: {said}"


# ---------------------------------------------------------------------------
# 3. `off` REFUSES A READ, IN EVERY SPELLING OF THE TOOL NAME.
# ---------------------------------------------------------------------------

_MCP_SPELLINGS = [
    "mcp__probe-research__browse",
    "mcp__plugin_probe-research_probe-research__browse",
    "mcp__probe_research__search_knowledge",
    "mcp__plugin_probe-research_probe-research__entity",
]


@pytest.mark.parametrize("tool", _MCP_SPELLINGS)
def test_off_denies_a_probe_mcp_read_however_the_install_spells_it(
    guard, monkeypatch, capsys, tmp_path, tool
):
    """The same tool has a different full name depending on how the plugin was
    installed, so a hardcoded list of five names silently misses. Matching the
    SERVER in the name is what survives that."""
    guard._session_marker.set_session_state(SESSION_ID, "off")
    out = _run(guard, monkeypatch, capsys, {
        "hook_event_name": "PreToolUse", "tool_name": tool,
        "session_id": SESSION_ID, "tool_input": {}, "cwd": str(tmp_path),
    })
    hso = json.loads(out)["hookSpecificOutput"]
    assert hso["permissionDecision"] == "deny"
    reason = hso["permissionDecisionReason"]
    assert "OFF" in reason
    # The deny must name the COST, not just the refusal: an agent that cannot
    # look has no way to tell an empty result from a genuine absence.
    assert "cannot know what you missed" in reason
    assert "does not backfill" in reason


@pytest.mark.parametrize("state", ["full", "read-only"])
@pytest.mark.parametrize("tool", _MCP_SPELLINGS)
def test_only_off_gates_reads(guard, monkeypatch, capsys, tmp_path, state, tool):
    """`read-only` exists BECAUSE reads survive it. A gate that fired here
    would delete the distinction the third state was added to make."""
    guard._session_marker.set_session_state(SESSION_ID, state)
    assert _run(guard, monkeypatch, capsys, {
        "hook_event_name": "PreToolUse", "tool_name": tool,
        "session_id": SESSION_ID, "tool_input": {}, "cwd": str(tmp_path),
    }) == ""


def test_an_unrelated_tool_is_never_touched(guard, monkeypatch, capsys, tmp_path):
    guard._session_marker.set_session_state(SESSION_ID, "off")
    for tool in ("Read", "Edit", "mcp__github__list_issues", "WebFetch"):
        assert _run(guard, monkeypatch, capsys, {
            "hook_event_name": "PreToolUse", "tool_name": tool,
            "session_id": SESSION_ID, "tool_input": {}, "cwd": str(tmp_path),
        }) == "", f"denied {tool}"


@pytest.mark.parametrize(
    "command",
    ["probe session state full", "probe session status", "probe outbox status"],
)
def test_off_never_walls_off_the_escape_hatch(
    guard, monkeypatch, capsys, tmp_path, command
):
    """Denying the switch itself would leave the researcher unable to release
    the state they set, and denying `outbox status` would strand queued work in
    silence -- `off` stops the automatic report, so asking is the only way left
    to see it."""
    guard._session_marker.set_session_state(SESSION_ID, "off")
    assert _run(guard, monkeypatch, capsys, {
        "hook_event_name": "PreToolUse", "tool_name": "Bash",
        "session_id": SESSION_ID, "tool_input": {"command": command},
        "cwd": str(tmp_path),
    }) == "", f"denied {command}"


def test_off_denies_a_probe_read_typed_into_bash(
    guard, monkeypatch, capsys, tmp_path
):
    """Two doors, one meaning. Locking the MCP tools while leaving the CLI open
    teaches the model the gate is advisory, which is how a warning layer
    dies."""
    guard._session_marker.set_session_state(SESSION_ID, "off")
    out = _run(guard, monkeypatch, capsys, {
        "hook_event_name": "PreToolUse", "tool_name": "Bash",
        "session_id": SESSION_ID, "tool_input": {"command": "probe project list"},
        "cwd": str(tmp_path),
    })
    assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_cleanup_survives_every_state(guard, monkeypatch, capsys, tmp_path):
    """"Record nothing" is not "prevent cleanup". The first thing a researcher
    does after finding an untracked session's writes is delete them, and a
    layer that fought that would make the mess it exists to prevent
    permanent."""
    for state in guard._session_marker.STATES:
        guard._session_marker.set_session_state(SESSION_ID, state)
        assert _run(guard, monkeypatch, capsys, {
            "hook_event_name": "PreToolUse", "tool_name": "Bash",
            "session_id": SESSION_ID,
            "tool_input": {"command": "probe project delete x"},
            "cwd": str(tmp_path),
        }) == "", f"{state} blocked a delete"


# ---------------------------------------------------------------------------
# 4. AN EXISTING OPT-OUT MIGRATES TO read-only, NEVER TO THE NEW off.
# ---------------------------------------------------------------------------


def test_a_legacy_off_marker_becomes_read_only(marker):
    """It was written by somebody who meant "stop recording, keep searching" --
    the switch has never gated reads. Mapping it to the new `off` would take
    away reads they never gave up, retroactively and silently."""
    path = marker.tracking_signal_path(SESSION_ID)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("off\n", encoding="utf-8")
    assert marker.session_state(SESSION_ID) == "read-only"
    assert marker.state_allows_reads("read-only") is True


def test_the_pre_0_30_off_spelling_becomes_read_only_too(marker):
    legacy = marker._legacy_off_path(SESSION_ID)
    legacy.parent.mkdir(parents=True, exist_ok=True)
    legacy.write_text("", encoding="utf-8")
    assert marker.session_state(SESSION_ID) == "read-only"


def test_a_legacy_on_marker_becomes_full(marker):
    path = marker.tracking_signal_path(SESSION_ID)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("on\n", encoding="utf-8")
    assert marker.session_state(SESSION_ID) == "full"


def test_the_new_off_is_reachable_only_by_naming_it(marker):
    """Nothing that predates the third state can produce it."""
    assert marker.set_tracking(SESSION_ID, False) and marker.session_state(SESSION_ID) != "off"
    assert marker.set_session_state(SESSION_ID, "off")
    assert marker.session_state(SESSION_ID) == "off"


@pytest.mark.parametrize(
    ("stored", "expected"),
    [
        ({"session_tracking": "off"}, "read-only"),
        ({"session_tracking": "on"}, "full"),
        ({"session_state": "off"}, "off"),
        ({"session_state": "off", "session_tracking": "off"}, "off"),
        ({"session_state": "read-only", "session_tracking": "off"}, "read-only"),
        ({}, None),
    ],
)
def test_a_stored_default_keeps_the_meaning_it_was_written_with(
    marker, stored, expected
):
    """The same collision one level up. A config saying `session_tracking: off`
    predates the third state; reading the new hard `off` out of it would take
    reads away from every folder and machine already configured."""
    assert marker._stored_state(stored) == expected


def test_an_unrecognised_default_resolves_to_full_not_to_something_quieter(marker):
    """A typo must not silently stop recording someone's research -- and now,
    must not silently stop them searching either."""
    assert marker._stored_state({"session_state": "reedonly"}) is None
    assert marker.default_session_state({"defaults": {"session_state": "nope"}}) == "full"


# ---------------------------------------------------------------------------
# 5. THE FIXES A PRE-LANDING REVIEW FOUND. Each of these shipped broken in an
#    earlier commit on this branch and each failed silently.
# ---------------------------------------------------------------------------


_TOOL_SHAPES = [
    {
        "hook_event_name": "PostToolUse",
        "tool_name": "Skill",
        "tool_input": {"skill": "probe-research:probe"},
    },
    {
        "hook_event_name": "UserPromptSubmit",
        "prompt": "<skill>\n<name>probe-research:probe</name>\n</skill>",
    },
]


@pytest.mark.parametrize("payload", _TOOL_SHAPES)
def test_an_agent_loading_the_switch_can_never_move_it(
    guard, monkeypatch, capsys, tmp_path, payload
):
    """THE WORST BUG ON THIS BRANCH, and it shipped for four commits.

    `probe` was put in BARE_FLIP_SLUGS on the reasoning that a switch-only skill
    has no manual for an agent to open, so a bare sighting can only be a person.
    But a skill is a TOOL the model can call, and this one has a body worth
    loading: an agent asked what state Probe is in, or told to check before
    writing, invokes it. On the bare class that invocation ADVANCES the cycle --
    so from `off`, the model reading the switch's own documentation turned Probe
    back ON, and the state whose entire purpose is "no Probe" was undone by an
    agent trying to respect it.

    Both shapes here are ones the MODEL can produce: Claude Code's Skill tool
    call, and Codex's `<skill>` activation block.
    """
    guard._session_marker.set_session_state(SESSION_ID, "off")
    out = _run(guard, monkeypatch, capsys, {
        **payload, "session_id": SESSION_ID, "cwd": str(tmp_path),
    })
    assert guard._session_marker.session_state(SESSION_ID) == "off", (
        "an agent's own bare invocation moved the switch"
    )
    assert out == "", f"it also announced a move it should not have made: {out}"


def test_a_person_typing_it_bare_still_advances(guard, monkeypatch, capsys, tmp_path):
    """The other half: locking the tool shape must not lock the typed one."""
    guard._session_marker.set_session_state(SESSION_ID, "off")
    _run(guard, monkeypatch, capsys, {
        "hook_event_name": "UserPromptSubmit", "prompt": "/probe",
        "session_id": SESSION_ID, "cwd": str(tmp_path),
    })
    # Out of `off`, a press lands on `read-only`, not on `full`: it gives back
    # what `off` took away without also resuming recording nobody asked for.
    assert guard._session_marker.session_state(SESSION_ID) == "read-only"


def test_the_boolean_default_writer_moves_both_keys(marker, tmp_path, monkeypatch):
    """The two-valued writer, which the wizard no longer uses but callers still
    reach for (`probe session track/untrack`, anything holding a bool).

    Readers prefer `session_state`, so writing only `session_tracking` left a
    stale `full` winning: the caller reported tracking off and every new session
    kept recording.
    """
    marker.write_default_state("full")
    assert marker.default_session_state() == "full"

    marker.write_default_tracking(False)
    assert marker.default_session_state() == "read-only", (
        "the boolean writer left a stale session_state winning"
    )
    assert marker.default_tracking() is False


def test_a_torn_pair_never_reads_as_recording(marker):
    """Two writers interleaving four writes can leave `.state=off` beside
    `.tracking=on`. Every reader here resolves through the canonical file, so
    the pair is eventually consistent rather than contradictory -- the
    alternative was the guard refusing writes while the status line, the capture
    check and the wizard all believed the session was recording.
    """
    marker.set_session_state(SESSION_ID, "off")
    # Simulate the losing writer's late compat write landing after the winner's.
    marker.tracking_signal_path(SESSION_ID).write_text("on\n", encoding="utf-8")

    assert marker.session_state(SESSION_ID) == "off"
    assert marker.tracking_signal(SESSION_ID) == "off"
    assert marker.is_tracking(marker.tracking_signal(SESSION_ID)) is False


def test_the_seed_never_deletes_a_newer_decision(marker, monkeypatch):
    """A seed that lost the race used to delete the winner's canonical file.

    What remained was the winner's compat file, which migrates to `read-only` --
    so an explicit `off` that landed a microsecond earlier came back with reads
    reopened, and nothing anywhere said so.
    """
    # The seed reads "undecided", then a concurrent setter publishes `off`.
    real = marker.session_state
    monkeypatch.setattr(marker, "session_state", lambda sid: None)
    marker.set_session_state(SESSION_ID, "off")
    monkeypatch.setattr(marker, "session_state", real)

    assert marker.set_session_state_if_absent(SESSION_ID, "full") is False
    assert marker.session_state(SESSION_ID) == "off", "the seed erased the winner"


def test_off_denies_the_shared_artifact_reads(guard, monkeypatch, capsys, tmp_path):
    """`probe shared list` and `shared download` read the TEAM'S artifacts.

    `shared` reads as machine plumbing beside `context` and `token`, which is
    why it was left out, and that left a door into exactly the content `off`
    exists to stop reaching.
    """
    guard._session_marker.set_session_state(SESSION_ID, "off")
    for command in ("probe shared list", "probe shared download abc123"):
        out = _run(guard, monkeypatch, capsys, {
            "hook_event_name": "PreToolUse", "tool_name": "Bash",
            "session_id": SESSION_ID, "tool_input": {"command": command},
            "cwd": str(tmp_path),
        })
        assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "deny", (
            f"{command} reached the team's artifacts under off"
        )


# ---------------------------------------------------------------------------
# 5. THE WORDS MAY BE RENAMED. THE BYTES MAY NOT.
# ---------------------------------------------------------------------------
#
# The states are CALLED `on` / `read` / `off` and STORED as `full` /
# `read-only` / `off`. That gap is load-bearing, not an oversight: the config
# file and the session marker are read by every other copy of this module on
# the machine -- a vendored hook, an older plugin, a pi extension on its own
# release train -- and their `normalize_state` cannot know a word this version
# invented. An unrecognised value there resolves to DEFAULT_STATE, which is
# recording. So a rename that reached the bytes would turn somebody's opt-out
# into consent on exactly the machines that are half-upgraded, which is failure
# 1 at the top of this file wearing a new hat.


def test_the_stored_bytes_keep_the_older_spelling(marker, tmp_path):
    """The compat pin. If this fails, an older client on this machine is about
    to read an opt-out as consent -- not a cosmetic diff."""
    import json as jsonlib

    marker.write_default_state(marker.STATE_READ_ONLY)
    stored = jsonlib.loads(marker.config_path().read_text(encoding="utf-8"))
    assert stored["defaults"]["session_state"] == "read-only", stored["defaults"]
    assert stored["defaults"]["session_tracking"] == "off", stored["defaults"]

    marker.set_session_state(SESSION_ID, marker.STATE_READ_ONLY)
    assert marker.state_path(SESSION_ID).read_text(encoding="utf-8").strip() == "read-only"


def test_the_words_and_the_states_are_one_list(marker):
    """`STATE_WORDS` is the switch's in the same order, and every word resolves
    back to the state it names. A word with no state (or a state with no word)
    is a surface that will print `None` at somebody. `daemon` keeps its word for
    the JSON readers, but is no switch position (Richard 2026-09-29)."""
    assert tuple(marker.STATE_LABELS) == marker.STATES
    assert marker.STATE_WORDS == tuple(marker.state_label(s) for s in marker.SWITCH_STATES)
    assert marker.STATE_WORDS == ("on", "read", "off")
    for state in marker.STATES:
        assert marker.state_for_label(marker.state_label(state)) == state
        assert marker.normalize_state(marker.state_label(state)) == state


def test_both_spellings_are_accepted_wherever_a_state_is_typed(marker):
    """The old words keep working -- a resumed transcript, muscle memory, a
    script somebody wrote last month, and the pi extension, which deliberately
    still SENDS `read-only` because it meets older CLIs too."""
    for word in ("read", "read-only", "readonly", "read_only", "ro"):
        assert marker.normalize_state(word) == marker.STATE_READ_ONLY, word
    for word in ("on", "full", "true", "enabled"):
        assert marker.normalize_state(word) == marker.STATE_FULL, word
    assert marker.normalize_state("off") == marker.STATE_OFF


def test_the_guard_takes_the_same_spellings_the_marker_does(guard, marker):
    """Two lists, one vocabulary. The guard parses what a person TYPED at the
    skill; the marker parses what is STORED and what the CLI was handed. A word
    one of them accepts and the other does not is a switch that moves on pi and
    not in Claude Code, or vice versa."""
    assert set(marker.TRACKING_READ_ONLY_VALUES) == guard.READ_ONLY_WORDS
    # The other two lists are deliberately NOT equal -- the guard also takes the
    # direction words a person speaks at a skill (`stop`, `resume`), which are
    # not values anything stores. The words this version PRINTS have to be in
    # both, and that is what is pinned.
    for state in marker.STATES:
        word = marker.state_label(state)
        assert word in (
            guard.ON_WORDS | guard.READ_ONLY_WORDS | guard.OFF_WORDS | guard.DAEMON_WORDS
        ), word


def test_typing_probe_read_lands_on_read_only(guard, monkeypatch, capsys, tmp_path):
    """The new word, end to end through the hook that actually moves it."""
    guard._session_marker.set_session_state(SESSION_ID, "full")
    out = _run(guard, monkeypatch, capsys, {
        "hook_event_name": "UserPromptSubmit", "prompt": "/probe read",
        "session_id": SESSION_ID, "cwd": str(tmp_path),
    })
    assert guard._session_marker.session_state(SESSION_ID) == "read-only"
    assert "READ" in json.loads(out)["hookSpecificOutput"]["additionalContext"]
