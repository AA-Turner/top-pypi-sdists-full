"""The status-line marker: what it stores, and what it renders.

The rendering tests assert on TEXT and WIDTH rather than on a golden string,
because the properties that matter are the ones that keep the segment readable
next to a neighbour it knows nothing about: one line, bounded width, a leading
gap, and the meaning-bearing word surviving truncation.
"""

from __future__ import annotations

import json
import re
import time

import os

import pytest

from probe import version_policy
from probe.sdk import session_marker


@pytest.fixture()
def state_home(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    return tmp_path


SESSION = "32fae7ad-a401-43d0-bfef-ea032058769e"

_SGR = re.compile(r"\033\[[0-9;]*m")


def _visible(text: str) -> str:
    """What a terminal actually shows — escape sequences occupy no columns."""
    return _SGR.sub("", text)


# -- paths ------------------------------------------------------------------


def test_state_dir_agrees_with_version_policy(state_home) -> None:
    """The duplicate XDG resolution must land where the rest of the client lives.

    session_marker cannot import version_policy (it is vendored into a hook with
    no probe package), so the two definitions are guarded rather than shared.
    """
    assert session_marker.state_dir() == version_policy.state_dir()


def test_marker_path_is_under_sessions(state_home) -> None:
    assert session_marker.marker_path(SESSION).parent == session_marker.sessions_dir()


@pytest.mark.parametrize(
    "value",
    ["", "short", "../../etc/passwd", "has space", "a" * 201, None, 7],
)
def test_invalid_session_ids_are_refused(value) -> None:
    """A value that could never have been sent as a header must not mint a file."""
    assert session_marker.valid_session_id(value) is False


def test_write_refuses_a_bad_session_id(state_home) -> None:
    assert session_marker.write("../escape", {"project": "x"}) is False
    assert not session_marker.sessions_dir().exists()


# -- round trip -------------------------------------------------------------


def test_write_then_read(state_home) -> None:
    assert session_marker.write(SESSION, {"project": "folding", "run_ids": ["r1"]}) is True
    state = session_marker.read(SESSION)
    assert state["project"] == "folding"
    assert state["run_ids"] == ["r1"]
    assert isinstance(state["updated_at"], float)


def test_read_is_none_when_absent(state_home) -> None:
    assert session_marker.read(SESSION) is None


def test_read_is_none_when_malformed(state_home) -> None:
    path = session_marker.marker_path(SESSION)
    path.parent.mkdir(parents=True)
    path.write_text("{not json", encoding="utf-8")
    assert session_marker.read(SESSION) is None


def test_read_is_none_when_expired(state_home) -> None:
    session_marker.write(SESSION, {"project": "folding"})
    path = session_marker.marker_path(SESSION)
    stale = json.loads(path.read_text())
    stale["updated_at"] = time.time() - session_marker.MAX_AGE_SECONDS - 1
    path.write_text(json.dumps(stale), encoding="utf-8")
    assert session_marker.read(SESSION) is None


def test_a_future_timestamp_also_expires(state_home) -> None:
    """Clock skew or a restored backup must not pin a marker as fresh forever."""
    session_marker.write(SESSION, {"project": "folding"})
    path = session_marker.marker_path(SESSION)
    skewed = json.loads(path.read_text())
    skewed["updated_at"] = time.time() + session_marker.MAX_AGE_SECONDS + 1
    path.write_text(json.dumps(skewed), encoding="utf-8")
    assert session_marker.read(SESSION) is None


def test_write_stamps_its_own_time(state_home) -> None:
    """A caller cannot back-date a marker; the writer owns the clock."""
    session_marker.write(SESSION, {"project": "folding", "updated_at": 0})
    assert session_marker.read(SESSION) is not None


# -- from_session_work ------------------------------------------------------


def test_from_session_work_takes_the_latest_project() -> None:
    """Oldest-first in, most recent out: a status line should name what you are
    working on now, not what you opened the session with."""
    payload = {
        "projects": [
            {"slug": "first", "name": "First"},
            {"slug": "second", "name": "Second"},
        ],
        "runs": [{"entity_id": "run-1"}, {"entity_id": "run-2"}],
    }
    assert session_marker.from_session_work(payload) == {
        "project": "second",
        "run_ids": ["run-1", "run-2"],
    }


def test_from_session_work_falls_back_to_name() -> None:
    assert session_marker.from_session_work({"projects": [{"name": "Named"}]})["project"] == "Named"


@pytest.mark.parametrize(
    "payload",
    [{}, {"projects": None}, {"projects": ["not a dict"]}, {"projects": [{}]}, {"runs": "nope"}],
)
def test_from_session_work_survives_a_shape_it_does_not_know(payload) -> None:
    """The response is another service's schema; a surprise degrades, never raises."""
    out = session_marker.from_session_work(payload)
    assert out["project"] is None
    assert out["run_ids"] == []


# -- liveness ---------------------------------------------------------------


def _lease(state_home, run_id: str, *, expires_in: float) -> None:
    runs = session_marker.state_dir() / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    (runs / f"{run_id}.lease").write_text(
        json.dumps({"run": run_id, "expires_at": time.time() + expires_in}), encoding="utf-8"
    )


def test_live_when_this_sessions_run_holds_a_lease(state_home) -> None:
    _lease(state_home, "run-1", expires_in=600)
    assert session_marker.is_live({"run_ids": ["run-1"]}) is True


def test_not_live_when_the_lease_expired(state_home) -> None:
    _lease(state_home, "run-1", expires_in=-1)
    assert session_marker.is_live({"run_ids": ["run-1"]}) is False


def test_not_live_when_the_live_run_belongs_to_another_session(state_home) -> None:
    """THE INTERSECTION IS THE POINT. `run_lock.any_live()` would say yes here --
    a run IS live on this box. It is a colleague's sweep in another terminal, and
    lighting up this session's status line for it is the bug."""
    _lease(state_home, "someone-elses-run", expires_in=600)
    assert session_marker.is_live({"run_ids": ["run-1"]}) is False


def test_a_malformed_lease_reads_as_not_live(state_home) -> None:
    """Inverts run_lock's fail-closed rule on purpose: printing "running" when
    nothing runs is a confident lie, and the cost of being wrong here is a word
    on a status line rather than an update landing in a live run."""
    runs = session_marker.state_dir() / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    (runs / "run-1.lease").write_text("{truncated", encoding="utf-8")
    assert session_marker.is_live({"run_ids": ["run-1"]}) is False


def test_liveness_does_not_delete_lock_entries(state_home) -> None:
    """Read-only, unlike run_lock: this runs on every render and would race a
    starting run's own acquire."""
    _lease(state_home, "run-1", expires_in=-1)
    session_marker.live_run_ids()
    assert (session_marker.state_dir() / "runs" / "run-1.lease").exists()


@pytest.mark.parametrize("state", [None, {}, {"run_ids": []}, {"run_ids": "nope"}, "not a dict"])
def test_is_live_is_false_without_runs(state_home, state) -> None:
    assert session_marker.is_live(state) is False


# -- liveness: the server source ---------------------------------------------


def test_live_when_the_server_says_active_even_with_no_local_lock(state_home) -> None:
    """THE REMOTE CASE, and the reason the server is the source. A run executing
    on a cluster holds its lock on THAT box; reading only local locks made it
    indistinguishable from no run at all."""
    assert session_marker.is_live({"run_ids": ["run-1"], "active_run_ids": ["run-1"]}) is True


def test_live_from_the_server_needs_no_run_ids_at_all(state_home) -> None:
    """The two sources are independent: the active lookup keys on the originating
    session directly, so it does not depend on the work read having landed."""
    assert session_marker.is_live({"active_run_ids": ["run-1"]}) is True


def test_local_lock_still_wins_when_the_server_has_not_caught_up(state_home) -> None:
    """The fast path. A run started seconds ago is live locally before the next
    refresh lands, and an flock is ground truth a heartbeat cannot promise."""
    _lease(state_home, "run-1", expires_in=600)
    assert session_marker.is_live({"run_ids": ["run-1"], "active_run_ids": []}) is True


def test_not_live_when_both_sources_say_nothing(state_home) -> None:
    """Both false is the only "not running"."""
    assert session_marker.is_live({"run_ids": ["run-1"], "active_run_ids": []}) is False


@pytest.mark.parametrize("active", ["nope", [None], [""], [{}], None])
def test_a_malformed_active_list_is_not_liveness(state_home, active) -> None:
    """Another service's schema; a surprise must not assert a run is running."""
    assert session_marker.is_live({"run_ids": [], "active_run_ids": active}) is False


# -- from_active_runs --------------------------------------------------------


def test_from_active_runs_takes_the_ids() -> None:
    payload = [{"id": "run-1", "status": "running"}, {"id": "run-2"}]
    assert session_marker.from_active_runs(payload) == ["run-1", "run-2"]


@pytest.mark.parametrize(
    "payload", [None, {}, "nope", [None], ["run-1"], [{"id": 7}], [{"id": ""}], [{}]]
)
def test_from_active_runs_survives_a_shape_it_does_not_know(payload) -> None:
    assert session_marker.from_active_runs(payload) == []


# -- configured -------------------------------------------------------------


def test_configured_reads_the_v2_context_shape(tmp_path, monkeypatch) -> None:
    """Reading only the flat v1 shape silently missed every wizard install once."""
    config = tmp_path / "config.json"
    config.write_text(
        json.dumps({"current_context": "work", "contexts": {"work": {"token": "probe_pat_x"}}}),
        encoding="utf-8",
    )
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(config))
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_MCP_TOKEN", raising=False)
    assert session_marker.configured() is True


def test_configured_reads_the_flat_v1_shape(tmp_path, monkeypatch) -> None:
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"mcp_token": "probe_pat_x"}), encoding="utf-8")
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(config))
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_MCP_TOKEN", raising=False)
    assert session_marker.configured() is True


def test_not_configured_without_a_token(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "absent.json"))
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_MCP_TOKEN", raising=False)
    assert session_marker.configured() is False


def test_env_token_alone_counts_as_configured(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "absent.json"))
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_x")
    assert session_marker.configured() is True


# -- rendering --------------------------------------------------------------


def test_unconfigured_renders_nothing() -> None:
    """Someone who does not use Probe spends zero columns being told so."""
    assert session_marker.render({"project": "folding"}, configured=False, tracking=True) == ""


def test_untracked_reads_as_untracked() -> None:
    out = session_marker.render(None, configured=True, tracking=False, color=False)
    assert out.strip() == "● not tracking"


def test_read_only_is_spelled_out_not_abbreviated_to_read() -> None:
    """The status line says what the state DOES, not what the switch is called.

    `read` alone, with no neighbouring word, reads as an activity in progress
    rather than as a restriction. The switch still ACCEPTS `read` -- both
    spellings resolve -- so this is one state with one meaning, spelled for a
    reader who is glancing at a single line."""
    out = session_marker.render(
        None,
        configured=True,
        tracking=False,
        color=False,
        session_state=session_marker.STATE_READ_ONLY,
    )
    assert out.strip() == "● read-only"
    assert session_marker.normalize_state("read") == session_marker.STATE_READ_ONLY


def test_off_is_red_and_read_only_is_not() -> None:
    """RED is reserved for the one state under which an agent cannot find prior
    work AND cannot know what it missed. `read-only` still answers questions, so
    it keeps yellow; a reader who sees red has lost something."""
    off = session_marker.render(
        None, configured=True, tracking=False, color=True, session_state=session_marker.STATE_OFF
    )
    assert "\033[31m●\033[0m" in off, f"red dot when off: {off!r}"
    assert off.count("\033[") == 2, f"exactly one painted run: {off!r}"

    read_only = session_marker.render(
        None,
        configured=True,
        tracking=False,
        color=True,
        session_state=session_marker.STATE_READ_ONLY,
    )
    assert "\033[33m●\033[0m" in read_only, f"yellow dot when read-only: {read_only!r}"

    # A caller from before the third state says only "not tracking", and cannot
    # tell us which of the two it means. It must not be guessed into red.
    legacy = session_marker.render(None, configured=True, tracking=False, color=True)
    assert "\033[33m●\033[0m" in legacy and "\033[31m" not in legacy, legacy


def test_every_switch_state_has_both_a_word_and_a_colour() -> None:
    """The two are one decision. A state that got a word but no hue would be
    painted yellow by accident, which is exactly what red exists to distinguish
    it from."""
    for state in (session_marker.STATE_READ_ONLY, session_marker.STATE_OFF):
        label, hue = session_marker._STATE_SEGMENT[state]
        assert label and hue
        assert len(label) < len(session_marker._LABEL_NOT_TRACKING), (
            f"{label!r} must not widen the segment past `not tracking`"
        )
    assert session_marker.STATE_FULL not in session_marker._STATE_SEGMENT


def test_tracked_names_the_project() -> None:
    """The state is spelled out, not encoded in the glyph: a status line is read
    by people who did not install it and do not know what a filled dot means."""
    out = session_marker.render(
        {"project": "bird-sql-sft"}, configured=True, tracking=True, color=False
    )
    assert out.strip() == "● tracking → bird-sql-sft"


def test_live_adds_the_running_accent() -> None:
    out = session_marker.render(
        {"project": "bird-sql-sft"}, configured=True, tracking=True, live=True, color=False
    )
    assert out.strip() == "● tracking → bird-sql-sft · running"


@pytest.mark.parametrize("live", [False, True])
@pytest.mark.parametrize("color", [False, True])
@pytest.mark.parametrize(
    "project", ["a", "bird-sql-sft", "a-really-long-project-slug-that-keeps-going-forever"]
)
def test_the_segment_is_never_wider_than_its_ceiling(project, live, color) -> None:
    """Overflow WRAPS the status line, which reflows every other segment on it --
    the one way this can make somebody else's output worse rather than longer.

    VISIBLE width, with the escape sequences stripped. Measuring the raw string
    would count bytes nobody can see: a coloured segment would look 9 characters
    over budget and get elided for nothing, and a layout computed on the coloured
    string would truncate a name that fit.
    """
    out = session_marker.render(
        {"project": project}, configured=True, tracking=True, live=live, color=color
    )
    assert len(_visible(out)) <= session_marker.MAX_SEGMENT_CHARS


def test_colour_does_not_change_the_layout() -> None:
    """The two spellings must differ only by escape sequences."""
    for state, live in [
        (None, False),
        ({"project": "folding"}, False),
        ({"project": "x" * 60}, True),
    ]:
        plain = session_marker.render(
            state, configured=True, tracking=bool(state), live=live, color=False
        )
        painted = session_marker.render(
            state, configured=True, tracking=bool(state), live=live, color=True
        )
        assert _visible(painted) == plain


def test_the_name_budget_does_not_move_when_a_run_starts() -> None:
    """A name that shrank the moment a run started, and grew back when it ended,
    reads as the status line glitching rather than as the run changing."""
    # Longer than the budget BY CONSTRUCTION, so both renders actually elide.
    project = "a-really-long-project-slug-" + "x" * session_marker.MAX_SLUG_CHARS
    idle = session_marker.render({"project": project}, configured=True, tracking=True, color=False)
    live = session_marker.render(
        {"project": project}, configured=True, tracking=True, live=True, color=False
    )
    assert live.startswith(idle)


def test_this_labs_project_names_mostly_fit_whole() -> None:
    """The ceiling is measured against real names, not picked.

    An earlier 18-character name budget elided 47% of this lab's projects -- and
    elided them when IDLE, where the columns were sitting unused. This pins the
    property that motivated the number, so a future narrowing has to argue with
    the data rather than with a constant.
    """
    slugs = [
        "dashboard-navigation-controls",
        "dashboard-agent-ux",
        "bird-sql-sft-qwen",
        "ash-voice-agent",
        "probe-surface-validation",
        "odyssey-text-diffusion",
        "odyssey-protein-benchmarks",
        "odyssey-lr-max-hessian",
        "bfcl-toolcall-sft",
        "tiny-models-generalization",
        "swe-smith-shakedown",
        "ml-intuition",
        "next-prediction",
        "trajectory-viewer-demo",
        "agentic-rl-visibility-demo",
        "bird-sql-sft",
        "bird-sql-agentic-rl",
        "miles-nebius",
        "research-os-demo",
        "session-tracking-indicator",
    ]
    whole = sum(1 for slug in slugs if len(slug) <= session_marker.MAX_SLUG_CHARS)
    assert whole >= int(0.9 * len(slugs)), (
        f"only {whole}/{len(slugs)} of this lab's project names show whole at "
        f"MAX_SLUG_CHARS={session_marker.MAX_SLUG_CHARS}"
    )


@pytest.mark.parametrize("state", [None, {"project": "folding"}, {"project": "x" * 80}])
@pytest.mark.parametrize("live", [False, True])
@pytest.mark.parametrize("color", [False, True])
def test_the_segment_is_always_one_line(state, live, color) -> None:
    """Claude Code renders each newline as its own status row."""
    out = session_marker.render(
        state, configured=True, tracking=bool(state), live=live, color=color
    )
    assert "\n" not in out


@pytest.mark.parametrize("state", [None, {"project": "folding"}])
def test_the_segment_leads_with_a_gap(state) -> None:
    """It is concatenated with a neighbour's output; without the gap
    `…main● folding` fuses into one unreadable token."""
    out = session_marker.render(state, configured=True, tracking=bool(state), color=False)
    assert out.startswith("  ")


def test_truncation_costs_the_name_not_the_meaning() -> None:
    """Eliding "· runn…" or "tracke… →" would spend the reader's attention on
    the parts they can already infer; only the name is variable."""
    out = session_marker.render(
        # Longer than the budget BY CONSTRUCTION: a wider budget must not turn
        # this into a test of a name that fits.
        {"project": "a-really-long-project-slug-" + "x" * session_marker.MAX_SLUG_CHARS},
        configured=True,
        tracking=True,
        live=True,
        color=False,
    )
    assert out.endswith("· running")
    assert out.startswith("  ● tracking → ")
    assert "…" in out


@pytest.mark.parametrize("live", [False, True])
@pytest.mark.parametrize("state", [None, {"project": "folding"}])
def test_colour_is_always_closed(state, live) -> None:
    """An unterminated SGR run bleeds into whatever prints next.

    Counted, not eyeballed: every code opened must have a reset after it, and the
    segment must not END mid-run whichever branch produced it.
    """
    out = session_marker.render(state, configured=True, tracking=bool(state), live=live, color=True)
    opens = len(re.findall(r"\033\[(?!0m)[0-9;]*m", out))
    resets = out.count("\033[0m")
    assert opens == resets, out
    # The LAST escape sequence must be the reset, so the segment cannot end
    # inside an open run. Not `endswith`: a segment whose final visible text is
    # uncoloured (`● folding`) correctly ends in plain characters.
    assert _SGR.findall(out)[-1] == "\033[0m", out


def test_only_the_dot_is_coloured() -> None:
    """Every word stays the terminal's default, so the segment reads like its
    neighbours and the eye has exactly one place to check."""
    tracked = session_marker.render(
        {"project": "folding"}, configured=True, tracking=True, live=True, color=True
    )
    assert "\033[32m●\033[0m" in tracked, "green dot when tracked"
    assert tracked.count("\033[") == 2, f"exactly one painted run: {tracked!r}"

    untracked = session_marker.render(None, configured=True, tracking=False, color=True)
    assert "\033[33m●\033[0m" in untracked, "yellow dot when not tracking"
    assert untracked.count("\033[") == 2, f"exactly one painted run: {untracked!r}"


def test_untracked_is_not_dimmed() -> None:
    """Dim tells the reader to skip precisely when they should look: untracked is
    the state worth noticing, so it gets a colour rather than a de-emphasis."""
    out = session_marker.render(None, configured=True, tracking=False, color=True)
    assert "\033[33m" in out  # a colour, not a de-emphasis


def test_colour_can_be_turned_off_entirely() -> None:
    for state in (None, {"project": "folding"}):
        assert "\033" not in session_marker.render(
            state, configured=True, tracking=bool(state), color=False
        )


# -- prune ------------------------------------------------------------------


def test_prune_drops_old_markers_and_keeps_fresh_ones(state_home) -> None:
    import os

    session_marker.write(SESSION, {"project": "folding"})
    other = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    session_marker.write(other, {"project": "old"})
    old_path = session_marker.marker_path(other)
    ancient = time.time() - session_marker.MAX_AGE_SECONDS - 10
    os.utime(old_path, (ancient, ancient))

    session_marker.prune()

    assert session_marker.marker_path(SESSION).exists()
    assert not old_path.exists()


def test_prune_survives_a_missing_directory(state_home) -> None:
    session_marker.prune()  # must not raise


def test_both_states_use_the_same_filled_glyph() -> None:
    """The dot is a mark, not a code. A hollow ring is faint at terminal font
    sizes; the state is carried by the word, so the glyph is free to be legible."""
    untracked = session_marker.render(None, configured=True, tracking=False, color=False)
    tracked = session_marker.render(
        {"project": "folding"}, configured=True, tracking=True, color=False
    )
    assert untracked.strip().startswith("● ")
    assert tracked.strip().startswith("● ")


def test_the_states_are_distinguishable_without_colour() -> None:
    """Colour is a glance aid, never the only channel: same glyph, different word,
    so this still reads correctly under NO_COLOR and for a colour-blind reader."""
    untracked = session_marker.render(None, configured=True, tracking=False, color=False)
    tracked = session_marker.render(
        {"project": "folding"}, configured=True, tracking=True, color=False
    )
    assert "not tracking" in untracked and "not tracking" not in tracked
    assert "tracking →" in tracked


# -- the third state: tracked, but not capturing session transcript -------------------------------


def test_segment_renders_the_third_state_from_the_marker() -> None:
    out = session_marker.render(
        {"project": "rosetta", "capture": {"running": False, "reason": "not paired"}},
        configured=True,
        tracking=True,
        color=False,
    )
    assert "not capturing session transcript: not paired" in out
    assert "◐" in out


def test_segment_is_unchanged_when_capture_is_running() -> None:
    out = session_marker.render(
        {"project": "rosetta", "capture": {"running": True, "reason": "running"}},
        configured=True,
        tracking=True,
        color=False,
    )
    assert "not capturing session transcript" not in out
    assert "tracking → rosetta" in out


def test_segment_is_unchanged_when_the_marker_has_no_capture_key() -> None:
    """A marker written by an older refresh hook must still render."""
    out = session_marker.render({"project": "rosetta"}, configured=True, tracking=True, color=False)
    assert "not capturing session transcript" not in out
    assert out.strip() == "● tracking → rosetta"


@pytest.mark.parametrize(
    "capture",
    [
        None,
        "not a dict",
        {},
        {"running": False},
        {"running": False, "reason": ""},
        {"running": False, "reason": 7},
        {"running": None, "reason": "not started"},
        {"reason": "not started"},
    ],
)
def test_a_capture_value_that_does_not_say_stopped_says_nothing(capture) -> None:
    """Silence, never a guess. Only an explicit `running: False` plus a non-empty
    string reason is a state anybody measured; everything else is a marker this
    renderer does not understand, and inventing a reason for it would put a
    fabricated diagnosis on the status line."""
    out = session_marker.render(
        {"project": "rosetta", "capture": capture}, configured=True, tracking=True, color=False
    )
    assert "not capturing session transcript" not in out
    assert "◐" not in out


def test_capture_is_never_mentioned_when_tracking_is_off() -> None:
    out = session_marker.render(
        {"project": "rosetta", "capture": {"running": False, "reason": "killswitch"}},
        configured=True,
        tracking=False,
        color=False,
    )
    assert "not capturing session transcript" not in out


def test_the_third_state_is_distinguishable_from_off_without_colour() -> None:
    """`tracked, not capturing session transcript` is not `not tracking`, and a reader with no colour
    must not read one as the other: different glyph AND different words."""
    degraded = session_marker.render(
        {"project": "rosetta", "capture": {"running": False, "reason": "halted"}},
        configured=True,
        tracking=True,
        color=False,
    )
    off = session_marker.render(None, configured=True, tracking=False, color=False)
    assert "not tracking" not in degraded
    assert "tracking →" in degraded
    assert degraded.strip()[0] != off.strip()[0]


@pytest.mark.parametrize("live", [False, True])
@pytest.mark.parametrize("color", [False, True])
@pytest.mark.parametrize("project", ["a", "rosetta", "a-really-long-project-slug-that-keeps-going"])
@pytest.mark.parametrize(
    "reason",
    [
        "halted",
        "not paired",
        "not started",
        "disabled path",
        "no session file",
        "interpreter too old",
        "a reason far longer than anything in the closed vocabulary, " * 4,
    ],
)
def test_a_capture_reason_never_widens_the_segment_past_its_ceiling(
    reason, project, live, color
) -> None:
    """The reason is DATA, and data on a status line has to be bounded.

    Overflow wraps the line and reflows every other segment on it. The closed
    vocabulary is short today, but this renderer reads whatever a refresh hook
    of any vintage wrote into the marker, so the bound cannot rest on the
    vocabulary staying short.
    """
    out = session_marker.render(
        {"project": project, "capture": {"running": False, "reason": reason}},
        configured=True,
        tracking=True,
        live=live,
        color=color,
    )
    assert len(_visible(out)) <= session_marker.MAX_SEGMENT_CHARS, _visible(out)
    assert "\n" not in out


@pytest.mark.parametrize(
    ("session_state", "daemon_live", "expected"),
    [
        (session_marker.STATE_FULL, False, "tracking → folding"),
        (session_marker.STATE_DAEMON, True, "on (daemon) → folding"),
        (session_marker.STATE_DAEMON, False, "on (daemon degraded) → folding"),
    ],
)
def test_the_daemon_state_names_the_switch_position(session_state, daemon_live, expected) -> None:
    """In `daemon` the reader sees who records: `on (daemon)` while the daemon
    records, `on (daemon degraded)` while it holds no live lease (Richard 2026-09-29)."""
    out = session_marker.render(
        {"project": "folding"},
        configured=True,
        tracking=True,
        color=False,
        session_state=session_state,
        daemon_live=daemon_live,
    )
    assert out.strip().endswith(expected), out


@pytest.mark.parametrize("daemon_live", [False, True])
@pytest.mark.parametrize("live", [False, True])
@pytest.mark.parametrize("reason", [None, "halted", "interpreter too old"])
@pytest.mark.parametrize(
    "project", [None, "bird-sql-sft", "a-really-long-project-slug-that-keeps-going-forever"]
)
def test_the_daemon_labels_stay_under_the_ceiling(project, reason, live, daemon_live) -> None:
    """The daemon's labels are longer than `tracking`; the name pays, never the ceiling."""
    state: dict = {}
    if project:
        state["project"] = project
    if reason:
        state["capture"] = {"running": False, "reason": reason}
    out = session_marker.render(
        state,
        configured=True,
        tracking=True,
        live=live,
        color=True,
        session_state=session_marker.STATE_DAEMON,
        daemon_live=daemon_live,
    )
    assert len(_visible(out)) <= session_marker.MAX_SEGMENT_CHARS, _visible(out)
    assert "on (daemon" in out
    if reason:
        assert _visible(out).endswith("not capturing session transcript: " + reason), _visible(out)


def test_every_reason_in_the_closed_vocabulary_renders_whole_on_the_bare_line() -> None:
    """The ceiling is derived from the LONGEST reason, and this pins the number
    it is derived from against the vocabulary it stands for. A reason added to
    `capture_state.REASONS` that outgrows `_LONGEST_REASON_CHARS` would otherwise
    render as `interp…` -- the one thing on the line the reader can act on, cut.
    """
    from probe.cli import capture_state

    assert session_marker._LONGEST_REASON_CHARS == max(len(r) for r in capture_state.REASONS)
    for reason in capture_state.REASONS:
        if reason == "running":
            continue  # a running daemon renders no suffix at all
        out = session_marker.render(
            {
                "project": "a-really-long-project-slug-that-keeps-going",
                "capture": {"running": False, "reason": reason},
            },
            configured=True,
            tracking=True,
            color=False,
        )
        assert out.endswith("not capturing session transcript: " + reason), out
        assert len(out) <= session_marker.MAX_SEGMENT_CHARS, out


def test_the_name_yields_to_the_reason_and_not_the_other_way_round() -> None:
    """WHICH HALF SURVIVES. The reason names the thing to fix and is unavailable
    anywhere else on screen; the project name is on the dashboard, in
    `probe session status`, and usually in the previous turn's output. So the
    name elides first, and gives up entirely before a single character of the
    reason is cut.
    """
    out = session_marker.render(
        {
            "project": "a-really-long-project-slug-that-keeps-going",
            "capture": {"running": False, "reason": "interpreter too old"},
        },
        configured=True,
        tracking=True,
        color=False,
    )
    assert out.endswith("not capturing session transcript: interpreter too old")
    # Nothing of the name is left at this reason length, so the segment falls
    # back to the bare label this file already renders when nothing is filed.
    assert out.strip().startswith("◐ tracking ·")


def test_a_short_reason_leaves_room_for_the_name() -> None:
    out = session_marker.render(
        {"project": "rosetta", "capture": {"running": False, "reason": "halted"}},
        configured=True,
        tracking=True,
        color=False,
    )
    assert out.strip() == "◐ tracking → rosetta · not capturing session transcript: halted"


def test_only_the_degraded_dot_is_coloured() -> None:
    out = session_marker.render(
        {"project": "rosetta", "capture": {"running": False, "reason": "halted"}},
        configured=True,
        tracking=True,
        color=True,
    )
    assert "\033[32m◐\033[0m" in out, "green: the WORK is still landing"
    assert out.count("\033[") == 2, f"exactly one painted run: {out!r}"
    assert _visible(out) == session_marker.render(
        {"project": "rosetta", "capture": {"running": False, "reason": "halted"}},
        configured=True,
        tracking=True,
        color=False,
    )


def test_codex_notice_names_a_missing_capture() -> None:
    text = session_marker.message(
        {"project": "rosetta", "capture": {"running": False, "reason": "not installed"}},
        live=False,
        tracking=True,
    )
    assert text.endswith("but not capturing session transcript: not installed")


def test_codex_notice_is_unchanged_when_capture_runs() -> None:
    text = session_marker.message(
        {"project": "rosetta", "capture": {"running": True, "reason": "running"}},
        live=False,
        tracking=True,
    )
    assert "not capturing session transcript" not in text


def test_codex_notice_says_nothing_about_capture_when_tracking_is_off() -> None:
    text = session_marker.message(
        {"project": "rosetta", "capture": {"running": False, "reason": "halted"}},
        live=False,
        tracking=False,
    )
    assert "not capturing session transcript" not in text


def test_codex_notice_defaults_to_the_pre_change_shape() -> None:
    """`statusline_notify.py` calls this with `live=` only. The default must keep
    that call site correct rather than silently dropping the new half."""
    text = session_marker.message(
        {"project": "rosetta", "capture": {"running": False, "reason": "halted"}}, live=True
    )
    assert (
        text == "Probe: tracking → rosetta · running, but not capturing session transcript: halted"
    )


def test_an_untracked_notice_never_grows_a_capture_clause() -> None:
    """There is no project, so there is nothing being tracked to contrast with."""
    text = session_marker.message(
        {"capture": {"running": False, "reason": "halted"}}, tracking=True
    )
    assert text == "Probe: this session is not tracked yet."


# -- the tracking signal: two states, one determinant -------------------------


def test_nobody_has_decided_until_someone_decides(state_home) -> None:
    assert session_marker.tracking_signal(SESSION) is None


def test_the_signal_round_trips(state_home) -> None:
    assert session_marker.set_tracking(SESSION, False) is True
    assert session_marker.tracking_signal(SESSION) == "off"
    assert session_marker.set_tracking(SESSION, True) is True
    assert session_marker.tracking_signal(SESSION) == "on"


def test_the_decision_is_per_session(state_home) -> None:
    other = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    session_marker.set_tracking(SESSION, False)
    assert session_marker.tracking_signal(other) is None


def test_turning_it_off_does_not_touch_what_was_recorded(state_home) -> None:
    """Work that landed before the switch happened; removing it would rewrite the
    research record to match a later mood."""
    session_marker.write(SESSION, {"project": "folding", "run_ids": ["r1"]})
    session_marker.set_tracking(SESSION, False)
    assert session_marker.read(SESSION)["project"] == "folding"


def test_the_signal_is_refused_for_a_bad_session_id(state_home) -> None:
    assert session_marker.set_tracking("../escape", False) is False
    assert session_marker.tracking_signal("../escape") is None


def test_a_legacy_off_file_is_still_honoured(state_home) -> None:
    """0.27-0.29 wrote `<sid>.off`. A researcher who turned tracking off before
    upgrading must not silently come back ON because we renamed the file."""
    session_marker.sessions_dir().mkdir(parents=True, exist_ok=True)
    session_marker._legacy_off_path(SESSION).write_text("x", encoding="utf-8")
    assert session_marker.tracking_signal(SESSION) == "off"
    assert session_marker.is_tracking("off") is False


def test_turning_it_back_on_clears_the_legacy_file(state_home) -> None:
    """Otherwise the old file would keep answering `off` forever."""
    session_marker.sessions_dir().mkdir(parents=True, exist_ok=True)
    session_marker._legacy_off_path(SESSION).write_text("x", encoding="utf-8")
    session_marker.set_tracking(SESSION, True)
    assert session_marker.tracking_signal(SESSION) == "on"


# -- is_tracking: the one boolean the surface renders -------------------------


@pytest.mark.parametrize(
    ("signal", "default", "expected"),
    [
        ("off", True, False),  # an explicit off beats a machine default of on
        ("on", False, True),  # and an explicit on beats a default of off
        ("off", False, False),
        ("on", True, True),
        (None, True, True),  # undecided: the machine default answers
        (None, False, False),
    ],
)
def test_is_tracking_lets_the_session_outrank_the_machine(signal, default, expected) -> None:
    """A PER-SESSION DECISION WINS IN BOTH DIRECTIONS -- that is what makes the
    toggle a toggle, and it is why a researcher who turns tracking off stays off
    no matter what any default says. With no decision, the machine answers."""
    assert session_marker.is_tracking(signal, default=default) is expected


def test_tracking_ships_on(state_home, monkeypatch, tmp_path) -> None:
    """Tracking is the posture. An undecided session on a machine that has set
    nothing is tracked -- which is what stops tracking from depending on anyone
    remembering to ask for it."""
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "absent.json"))
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    assert session_marker.DEFAULT_TRACKING is True
    assert session_marker.default_tracking() is True
    assert session_marker.is_tracking(None) is True


def _write_config(path, **defaults) -> None:
    path.write_text(json.dumps({"version": 2, "defaults": defaults}), encoding="utf-8")


def test_the_machine_default_is_read_from_the_config(tmp_path, monkeypatch) -> None:
    config = tmp_path / "config.json"
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(config))
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    _write_config(config, session_tracking="off")
    assert session_marker.default_tracking() is False
    _write_config(config, session_tracking="on")
    assert session_marker.default_tracking() is True


def test_machine_default_read_remains_compatible_above_folder_size_limit(
    tmp_path, monkeypatch
) -> None:
    config = tmp_path / "config.json"
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(config))
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    config.write_text(
        json.dumps(
            {
                "defaults": {"session_tracking": "off"},
                "future_padding": "x" * 70_000,
            }
        ),
        encoding="utf-8",
    )

    assert session_marker.default_tracking() is False


def _write_folder_config(folder, data) -> None:
    config = folder / ".probe" / "config.json"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(json.dumps(data), encoding="utf-8")


def test_nearest_valid_folder_default_wins(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    machine = tmp_path / "machine.json"
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(machine))
    _write_config(machine, session_tracking="off")
    root = tmp_path / "work"
    child = root / "repo" / "src"
    child.mkdir(parents=True)
    _write_folder_config(root, {"defaults": {"session_tracking": "on"}})
    _write_folder_config(root / "repo", {"defaults": {"session_tracking": "off"}})

    value, source = session_marker.resolve_tracking_default(child)

    assert value is False
    assert source == str(root / "repo" / ".probe" / "config.json")


@pytest.mark.parametrize(
    ("child_data", "has_error"),
    [
        ({"other": "setting"}, False),
        ({"defaults": {"session_tracking": "maybe"}}, True),
        ("{not json", True),
    ],
)
def test_missing_invalid_or_malformed_child_folder_default_continues_to_parent(
    tmp_path, monkeypatch, child_data, has_error
) -> None:
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "machine.json"))
    root = tmp_path / "work"
    child = root / "repo"
    child.mkdir(parents=True)
    _write_folder_config(root, {"defaults": {"session_tracking": "on"}})
    child_config = child / ".probe" / "config.json"
    child_config.parent.mkdir()
    if isinstance(child_data, str):
        child_config.write_text(child_data, encoding="utf-8")
    else:
        child_config.write_text(json.dumps(child_data), encoding="utf-8")
    errors: list[str] = []

    value, source = session_marker.resolve_tracking_default(child, errors=errors)

    assert value is True
    assert source == str(root / ".probe" / "config.json")
    assert bool(errors) is has_error
    if errors:
        assert str(child_config) in errors[0]


def test_unreadable_folder_default_continues_to_parent(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "machine.json"))
    root = tmp_path / "work"
    child = root / "repo"
    child.mkdir(parents=True)
    _write_folder_config(root, {"defaults": {"session_tracking": "on"}})
    _write_folder_config(child, {"defaults": {"session_tracking": "off"}})
    child_config = child / ".probe" / "config.json"
    real_open = session_marker.os.open

    def unreadable(path, *args, **kwargs):
        if path == child_config:
            raise OSError("permission denied")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(session_marker.os, "open", unreadable)
    errors: list[str] = []

    value, source = session_marker.resolve_tracking_default(child, errors=errors)

    assert value is True
    assert source == str(root / ".probe" / "config.json")
    assert len(errors) == 1
    assert str(child_config) in errors[0]
    assert "permission denied" in errors[0]


def test_invalid_utf8_folder_default_continues_to_parent(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "machine.json"))
    root = tmp_path / "work"
    child = root / "repo"
    child.mkdir(parents=True)
    _write_folder_config(root, {"defaults": {"session_tracking": "off"}})
    child_config = child / ".probe" / "config.json"
    child_config.parent.mkdir()
    child_config.write_bytes(b'\xff{"defaults":{"session_tracking":"on"}}')
    errors: list[str] = []

    value, source = session_marker.resolve_tracking_default(child, errors=errors)

    assert value is False
    assert source == str(root / ".probe" / "config.json")
    assert len(errors) == 1
    assert str(child_config) in errors[0]


def _feed_fifo(path, payload: bytes):
    import errno
    import os
    import threading

    def feed() -> None:
        deadline = time.monotonic() + 0.5
        while time.monotonic() < deadline:
            try:
                fd = os.open(path, os.O_WRONLY | os.O_NONBLOCK)
            except OSError as exc:
                if exc.errno != errno.ENXIO:
                    return
                time.sleep(0.01)
                continue
            try:
                os.write(fd, payload)
            except OSError:
                pass
            finally:
                os.close(fd)
            return

    thread = threading.Thread(target=feed, daemon=True)
    thread.start()
    return thread


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="no FIFOs on Windows")
def test_machine_default_read_is_not_subject_to_folder_regular_file_policy(
    tmp_path, monkeypatch
) -> None:
    import os

    fifo = tmp_path / "machine-config.fifo"
    os.mkfifo(fifo)
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(fifo))
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    feeder = _feed_fifo(fifo, b'{"defaults":{"session_tracking":"off"}}')

    value = session_marker.default_tracking()
    feeder.join(timeout=1)

    assert not feeder.is_alive()
    assert value is False


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="no FIFOs on Windows")
def test_fifo_folder_default_is_rejected_without_blocking_and_parent_wins(
    tmp_path, monkeypatch
) -> None:
    import os

    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "machine.json"))
    root = tmp_path / "work"
    child = root / "repo"
    child.mkdir(parents=True)
    _write_folder_config(root, {"defaults": {"session_tracking": "on"}})
    child_config = child / ".probe" / "config.json"
    child_config.parent.mkdir()
    fifo = tmp_path / "folder-config.fifo"
    os.mkfifo(fifo)
    child_config.symlink_to(fifo)
    feeder = _feed_fifo(
        fifo, b'{"defaults":{"session_tracking":"off"}}'
    )
    errors: list[str] = []

    value, source = session_marker.resolve_tracking_default(child, errors=errors)
    feeder.join(timeout=1)

    assert value is True
    assert source == str(root / ".probe" / "config.json")
    assert len(errors) == 1
    assert "regular file" in errors[0]
    assert child_config.is_symlink()


def test_oversized_folder_default_is_rejected_and_parent_wins(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "machine.json"))
    root = tmp_path / "work"
    child = root / "repo"
    child.mkdir(parents=True)
    _write_folder_config(root, {"defaults": {"session_tracking": "on"}})
    child_config = child / ".probe" / "config.json"
    child_config.parent.mkdir()
    valid_but_large = b'{"defaults":{"session_tracking":"off"}}' + b" " * 70_000
    child_config.write_bytes(valid_but_large)
    errors: list[str] = []

    value, source = session_marker.resolve_tracking_default(child, errors=errors)

    assert value is True
    assert source == str(root / ".probe" / "config.json")
    assert len(errors) == 1
    assert "size limit" in errors[0]


def test_env_override_beats_folder_default(tmp_path, monkeypatch) -> None:
    folder = tmp_path / "repo"
    folder.mkdir()
    _write_folder_config(folder, {"defaults": {"session_tracking": "on"}})
    monkeypatch.setenv("PROBE_SESSION_TRACKING", "off")

    assert session_marker.resolve_tracking_default(folder) == (False, "environment")


def test_folder_default_beats_machine_default(tmp_path, monkeypatch) -> None:
    machine = tmp_path / "machine.json"
    _write_config(machine, session_tracking="off")
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(machine))
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    folder = tmp_path / "repo"
    folder.mkdir()
    _write_folder_config(folder, {"defaults": {"session_tracking": "on"}})

    assert session_marker.resolve_tracking_default(folder) == (
        True,
        str(folder / ".probe" / "config.json"),
    )


def test_resolve_tracking_default_reaches_root_then_uses_machine(tmp_path, monkeypatch) -> None:
    machine = tmp_path / "machine.json"
    _write_config(machine, session_tracking="off")
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(machine))
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    child = tmp_path / "one" / "two"
    child.mkdir(parents=True)

    assert session_marker.resolve_tracking_default(child) == (False, str(machine.absolute()))


def test_resolve_tracking_default_walks_a_deleted_lexical_cwd(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "machine.json"))
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    root = tmp_path / "work"
    deleted_parent = root / "repo"
    deleted_cwd = deleted_parent / "gone"
    deleted_cwd.mkdir(parents=True)
    _write_folder_config(root, {"defaults": {"session_tracking": "off"}})
    deleted_cwd.rmdir()
    deleted_parent.rmdir()

    assert session_marker.resolve_tracking_default(deleted_cwd) == (
        False,
        str(root / ".probe" / "config.json"),
    )


def test_folder_tracking_override_reads_only_the_exact_folder(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    root = tmp_path / "work"
    child = root / "repo"
    child.mkdir(parents=True)
    _write_folder_config(root, {"defaults": {"session_tracking": "off"}})

    assert session_marker.folder_config_path(child) == child / ".probe" / "config.json"
    assert session_marker.folder_tracking_override(child) is None
    assert session_marker.folder_tracking_override(root) is False


@pytest.mark.parametrize(
    ("stored", "expected"),
    [
        (True, True),
        (False, False),
        ("ON", True),
        ("1", True),
        ("enabled", True),
        ("OFF", False),
        ("0", False),
        ("disabled", False),
    ],
)
def test_folder_default_uses_the_shared_tracking_value_parser(
    tmp_path, monkeypatch, stored, expected
) -> None:
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    folder = tmp_path / "repo"
    folder.mkdir()
    _write_folder_config(folder, {"defaults": {"session_tracking": stored}})

    assert session_marker.folder_tracking_override(folder) is expected


@pytest.mark.parametrize(
    ("stored", "expected"),
    [("1", True), ("enabled", True), ("0", False), ("disabled", False)],
)
def test_machine_default_uses_the_shared_tracking_value_parser(
    tmp_path, monkeypatch, stored, expected
) -> None:
    machine = tmp_path / "machine.json"
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(machine))
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    _write_config(machine, session_tracking=stored)

    assert session_marker.default_tracking() is expected


def test_resolve_tracking_default_reports_shipped_source(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "absent-machine.json"))
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    folder = tmp_path / "repo"
    folder.mkdir()

    assert session_marker.resolve_tracking_default(folder) == (True, "shipped")


@pytest.mark.parametrize("value", ["mabye", "", 7, None, [], "ON!"])
def test_an_unrecognised_default_reads_as_shipped_not_as_off(tmp_path, monkeypatch, value) -> None:
    """A typo in a config file must not silently stop recording someone's
    research. Unknown reads as the shipped default, never as off."""
    config = tmp_path / "config.json"
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(config))
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    _write_config(config, session_tracking=value)
    assert session_marker.default_tracking() is session_marker.DEFAULT_TRACKING


def test_the_env_override_beats_the_file(tmp_path, monkeypatch) -> None:
    """Env-beats-file, matching the rest of the client -- but it is an OVERRIDE,
    never the home: a dock-launched agent sources no shell profile, so a default
    exported from a shell rc would answer differently there."""
    config = tmp_path / "config.json"
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(config))
    _write_config(config, session_tracking="on")
    monkeypatch.setenv("PROBE_SESSION_TRACKING", "off")
    assert session_marker.default_tracking() is False
    monkeypatch.setenv("PROBE_SESSION_TRACKING", "on")
    _write_config(config, session_tracking="off")
    assert session_marker.default_tracking() is True


def test_the_default_survives_logout(tmp_path, monkeypatch) -> None:
    """THE REASON IT IS TOP-LEVEL. `clear_context` replaces a context wholesale,
    so a preference stored inside one would be wiped by `probe logout` and
    tracking would silently come back on."""
    from probe.sdk import config as sdk_config

    path = tmp_path / "config.json"
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(path))
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    path.write_text(
        json.dumps(
            {
                "version": 2,
                "current_context": "default",
                "contexts": {"default": {"token": "probe_pat_x"}},
                "defaults": {"session_tracking": "off"},
            }
        ),
        encoding="utf-8",
    )
    sdk_config.clear_context()
    assert session_marker.default_tracking() is False


def test_the_writer_and_the_readers_address_the_same_file(tmp_path, monkeypatch) -> None:
    """`sdk.config.config_path` used to ignore PROBE_CONFIG_PATH while four
    readers honoured it, so a value written here landed in ~/.config while the
    readers looked elsewhere: it worked in the field and vanished under test."""
    from probe.cli import capabilities
    from probe.sdk import config as sdk_config

    target = tmp_path / "elsewhere.json"
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(target))
    assert sdk_config.config_path() == target
    assert session_marker.config_path() == target
    assert capabilities.probe_config_path() == target


def test_not_tracking_renders_as_one_state_however_it_got_there(state_home) -> None:
    """ "Turned off" and "nothing recorded" look identical on purpose: a reader
    does not care WHY nothing is being recorded, only whether anything is."""
    turned_off = session_marker.render(
        {"project": "folding"}, configured=True, tracking=False, color=False
    )
    nothing_yet = session_marker.render(None, configured=True, tracking=False, color=False)
    assert turned_off == nothing_yet == "  ● not tracking"


def test_tracking_with_nothing_recorded_yet_says_so_without_inventing_a_name(
    state_home,
) -> None:
    out = session_marker.render(None, configured=True, tracking=True, color=False)
    assert out.strip() == "● tracking"
