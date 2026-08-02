"""Modes + /help UX overhaul — proofs.

Covers the four asks: (a) /help regrouped by intent + end marker; (b) the input-bar
prefix is no longer deletable (readline-protected prompt); (c) /worlds demoted to a
footer mention; (d) modes match canonical Nexplora (Partner · Autopilot · Study ·
Refine · Customize · Flight), retire the voices, and each posture still changes how
NX reasons. Run: python3 nx/cli/tests/test_modes_ux.py
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import builtins


def _strip(s):
    return re.sub(r"\033\[[0-9;]*m", "", s)


# ── (d) modes: registry, gates, normalization, behavior wiring ───────────────
def test_gates_are_the_four_postures():
    import nx_prompts as P
    assert set(P.NX_MODE_GATES) == {"PARTNER", "AUTOPILOT", "STUDY", "REFINE"}
    assert P.NX_VOICE_GATES is P.NX_MODE_GATES  # back-compat alias, same object
    assert P.MODE_POSTURES == ("PARTNER", "AUTOPILOT", "STUDY", "REFINE")
    assert set(P.MODE_ACTIONS) == {"CUSTOMIZE", "FLIGHT"}


def test_normalize_folds_legacy_and_defaults():
    from nx_prompts import normalize_mode as nm
    assert nm("PEER") == nm("advisor") == nm("Challenger") == "PARTNER"
    assert nm("OPERATOR") == "AUTOPILOT"
    assert nm("teacher") == "STUDY"
    assert nm("Refine") == "REFINE" and nm("PARTNER") == "PARTNER"
    assert nm("") == "PARTNER" and nm("garbage") == "PARTNER" and nm(None) == "PARTNER"


def test_changing_mode_changes_the_system_prompt():
    """The load-bearing claim: switching mode injects a DIFFERENT gate — so NX reasons
    differently. Includes legacy values folding to the right successor gate."""
    from nx_prompts import build_system_prompt as bsp
    needles = {
        "PARTNER": "one step at a time",
        "AUTOPILOT": "Report back",
        "STUDY": "show the proof",
        "REFINE": "DRAFT to make better",
        "PEER": "one step at a time",      # legacy → Partner gate
        "OPERATOR": "Report back",         # legacy → Autopilot gate
        "TEACHER": "show the proof",       # legacy → Study gate
    }
    for mode, needle in needles.items():
        assert needle in bsp(world="cowork", voice=mode), f"{mode} missing {needle!r}"
    # And the four postures are pairwise-distinct prompts (not cosmetic).
    prompts = {m: bsp(world="cowork", voice=m) for m in ("PARTNER", "AUTOPILOT", "STUDY", "REFINE")}
    for a in prompts:
        for b in prompts:
            if a < b:
                assert prompts[a] != prompts[b], f"{a} and {b} produce identical prompts"


def test_world_defaults_are_all_real_postures():
    import nx_routing as R
    from nx_prompts import MODE_POSTURES
    bad = {w: c["default_voice"] for w, c in R.WORLD_CONFIG.items() if c["default_voice"] not in MODE_POSTURES}
    assert not bad, f"non-posture world defaults: {bad}"
    # spot-check the semantic mapping
    assert R.WORLD_CONFIG["research"]["default_voice"] == "STUDY"
    assert R.WORLD_CONFIG["knowledge"]["default_voice"] == "STUDY"
    assert R.WORLD_CONFIG["ops"]["default_voice"] == "AUTOPILOT"
    assert R.WORLD_CONFIG["code"]["default_voice"] == "AUTOPILOT"
    assert R.WORLD_CONFIG["cowork"]["default_voice"] == "PARTNER"


def test_auto_shift_returns_new_postures():
    import nx_routing as R
    assert R.detect_voice_shift("go build this now", "PARTNER", "cowork") == "AUTOPILOT"
    assert R.detect_voice_shift("explain how does x work", "PARTNER", "cowork") == "STUDY"
    assert R.detect_voice_shift("tighten and polish this", "PARTNER", "cowork") == "REFINE"
    assert R.detect_voice_shift("hey what's up", "PARTNER", "cowork") == "PARTNER"  # default
    assert R.detect_voice_shift("whatever", "PARTNER", "ops") == "AUTOPILOT"        # locked
    assert R.detect_voice_shift("whatever", "STUDY", "legal") == "PARTNER"          # locked


def test_mode_registry_shape():
    import nx_slash_menu as S
    names = [m["name"] for m in S.MODES]
    assert names == ["Partner", "Autopilot", "Study", "Refine", "Customize", "Flight"]
    postures = [m["name"] for m in S.MODES if m["kind"] == "mode"]
    actions = [m["name"] for m in S.MODES if m["kind"] == "action"]
    assert postures == ["Partner", "Autopilot", "Study", "Refine"]
    assert actions == ["Customize", "Flight"]


def test_mode_display_chip_label():
    import nx_slash_menu as S
    assert S._mode_display("", "cowork") == "Partner"     # world default
    assert S._mode_display("", "ops") == "Autopilot"      # world default
    assert S._mode_display("PEER", "cowork") == "Partner"  # legacy fold
    assert S._mode_display("STUDY", "cowork") == "Study"   # explicit
    assert S._mode_display("refine", "cowork") == "Refine"


# ── (b) the deletable-prefix bug: prompt is now a readline prompt, not buffer text ──
def test_readline_line_nontty_keeps_first_char():
    """Non-TTY path: _readline_line must recombine the pre-read first char with the
    rest of the line (piped/CI). Proves no char is dropped by the readline handoff."""
    import nx_slash_menu as S
    orig = builtins.input
    try:
        builtins.input = lambda *a, **k: "ello"
        assert S._readline_line("  > ", "h") == "hello"
        def _raise(*a, **k):
            raise EOFError
        builtins.input = _raise
        assert S._readline_line("  > ", "h") == "/exit"
    finally:
        builtins.input = orig


def test_input_bar_uses_prompt_toolkit_footer():
    """slash_input reads via _read_input_bar, which renders the status BELOW the input as a
    prompt_toolkit bottom_toolbar (the shaded footer) — not a hand-drawn stacking chip."""
    import inspect
    import nx_slash_menu as S
    slash_src = inspect.getsource(S.slash_input)
    assert "_read_input_bar(" in slash_src, "slash_input must read via _read_input_bar"
    bar_src = inspect.getsource(S._read_input_bar)
    assert "bottom_toolbar" in bar_src, "the footer must render below the input via bottom_toolbar"
    assert "◈" not in bar_src and "◈" not in slash_src, "no tofu glyph anywhere"


# ── (a) + (c) /help grouped, /worlds demoted to footer with an end marker ─────
def test_help_is_grouped_with_worlds_footer_and_end_marker():
    import nx_cli as C
    plain = _strip(C.HELP)
    for header in ("TALK & THINK", "DO WORK", "CONNECT", "BUILD", "ACCOUNT", "WORLDS"):
        assert header in plain, f"missing group {header}"
    assert "end of commands" in plain, "missing end-of-list marker"
    assert "Partner · Autopilot · Study · Refine" in plain, "/mode blurb not updated"
    # /worlds is NOT a first-class grouped command...
    assert not [cmd for _h, cmds in C.HELP_GROUPS for cmd, _d in cmds if cmd == "/worlds"]
    # ...only a footer mention
    assert "/worlds switches context" in plain
    # HELP_LINES is derived + carries no standalone /worlds row
    assert isinstance(C.HELP_LINES, tuple)
    assert not any(x.startswith("/worlds") for x in C.HELP_LINES)
    assert any(x.startswith("/mode ") for x in C.HELP_LINES)


def test_slash_menu_dropped_worlds():
    import nx_slash_menu as S
    cmds = [c["cmd"] for sec in S.SECTIONS for c in sec["commands"]]
    assert "/worlds" not in cmds, "/worlds should be gone from the '/' menu"
    assert "/mode" in cmds
    mode_desc = [c["desc"] for sec in S.SECTIONS for c in sec["commands"] if c["cmd"] == "/mode"][0]
    assert "Partner" in mode_desc and "PEER" not in mode_desc


def test_action_helpers_exist():
    import nx_cli as C
    assert callable(C._run_flight) and callable(C.print_customize_panel)


# ── review-follow-up regressions ─────────────────────────────────────────────
def test_route_override_normalizes_legacy_voice():
    """A legacy voice_override in config must resolve to a real posture in
    RouteResult.voice (not just at gate-lookup) so status/chip stay consistent."""
    import nx_routing as R
    assert R.route("cowork", "hi", override_voice="PEER").voice == "PARTNER"
    assert R.route("cowork", "hi", override_voice="operator").voice == "AUTOPILOT"
    assert R.route("cowork", "hi", override_voice="teacher").voice == "STUDY"
    assert R.route("cowork", "hi", override_voice="Refine").voice == "REFINE"


def test_readline_line_recovers_first_char_when_hook_fails():
    """If the readline startup hook can't pre-insert the first char (broken/libedit
    readline), _readline_line must still not drop it — it prepends it to the result."""
    import nx_slash_menu as S
    from unittest import mock

    class _FakeRL:
        def set_startup_hook(self, fn=None):
            if fn:
                fn()  # run the hook now; insert_text raises → inserted stays False

        def insert_text(self, s):
            raise RuntimeError("libedit has no insert_text")

        def redisplay(self):
            pass

    real_import = builtins.__import__

    def fake_import(name, *a, **k):
        if name == "readline":
            return _FakeRL()
        return real_import(name, *a, **k)

    orig_input = builtins.input
    try:
        builtins.__import__ = fake_import
        builtins.input = lambda *a, **k: "ello"  # rest only; hook failed to insert 'h'
        with mock.patch.object(S.sys.stdin, "isatty", return_value=True), \
             mock.patch.object(S.sys.stdout, "isatty", return_value=True):
            assert S._readline_line("  > ", "h") == "hello", "first char must be recovered"
    finally:
        builtins.__import__ = real_import
        builtins.input = orig_input


def test_footer_text_codex_shape():
    """The status footer is `nx  <world · Mode>  ·  <cwd>` (· skills) — FULL words, not the
    old cryptic 'C·P' initials — cwd is the folder nx is run in (os.getcwd), truncated when long."""
    import nx_slash_menu as S
    label, cwd = S._status_bits("cowork", "")
    assert label == "cowork · Partner", label
    assert S._status_bits("strategy", "AUTOPILOT")[0] == "strategy · Autopilot"
    assert S._status_bits("research", "")[0] == "research · Study"     # research default = STUDY
    assert S._status_bits("cowork", "PEER")[0] == "cowork · Partner"   # legacy fold → Partner
    assert S._status_bits("nx-code", "AUTOPILOT")[0] == "nx-code · Autopilot"  # the old 'N·A' — now legible
    assert isinstance(cwd, str) and len(cwd) <= 24
    f = S._footer_text("cowork", "", [])
    assert f.strip().startswith("nx") and "cowork · Partner" in f and cwd in f
    assert "$brain" in S._footer_text("cowork", "", ["$brain"])   # active skills shown in footer


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for t in tests:
        t()
        print("  ✓ " + t.__name__)
        passed += 1
    print(f"\n{passed}/{len(tests)} modes-UX proofs pass")
