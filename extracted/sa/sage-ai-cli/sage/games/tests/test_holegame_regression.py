"""Regression tests for the real-user HoleGame failure.

A user pasted a 14k-char "Hole.io clone" prompt that ended with
`Make this video game with Unity and make sure that it works on mobile
apps and web`. Sage produced a Godot web export instead of a Unity
mobile-targeted scaffold, then a re-run with Unity contaminated the
directory with mixed Godot+Unity files.

This file pins the five fixes so the bug class never regresses:

  1. Engine detector: explicit instruction phrase wins over keyword
     mentions in passing.
  2. FPS genre: "FPS ≥ 60" (perf metric) no longer triggers the
     first-person-shooter genre.
  3. 2D perspective: Unicode hyphens "2‑D" / "2–D" / "2—D" now match.
  4. Target detection: "mobile apps and web" → primary=android, set
     covers all named targets.
  5. ScaffoldPollution guard: a previous engine's scaffold in the dir
     refuses a new engine instead of mixing them.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pytest

from sage.games.detector import (
    _pick_engine,
    _pick_targets,
    classify_prompt,
)
from sage.games.engines.base import GameRequest
from sage.games.exceptions import ScaffoldPollution
from sage.games.pipeline import _detect_existing_engine, build_game


# ───────────────────────── engine: explicit-instruction wins ──────────


_HOLE_GAME_TAIL = (
    "...AI-Prompt – Hole-It Clone. All code should be Unity C# (2022 LTS) "
    "but also include a Godot 4 GDScript version in separate sections "
    "for developers who prefer Godot. Provide a single-file Unity prefab "
    "description...\n\n"
    "Make this video game with Unity and make sure that it works on "
    "mobile apps and web. Make sure the assets are interesting and "
    "fun to play."
)


def test_explicit_unity_instruction_beats_godot_mention_in_body():
    """The user's tail instruction wins over Godot/Unity-Copilot mentions
    in the body of a long copy-pasted spec. This is the exact bug the
    HoleGame user hit."""
    assert _pick_engine(_HOLE_GAME_TAIL) == "unity"


@pytest.mark.parametrize("prompt,expected", [
    ("Make this video game with Unity",       "unity"),
    ("Build this in Godot 4",                  "godot"),
    ("Use Unreal Engine 5 for this",           "unreal"),
    ("Create the game in Bevy",                "bevy"),
    ("Build it with Phaser 3",                 "phaser"),
    ("Make this with LÖVE 2D",                 "love2d"),
    ("Use Pygame for the implementation",      "pygame"),
    # Both mentioned, but only one is the explicit instruction
    ("Like Godot or Unity, but make it with Unity",   "unity"),
    ("Inspired by Unity tutorials, build it in Godot", "godot"),
])
def test_explicit_engine_instruction_phrases(prompt, expected):
    assert _pick_engine(prompt) == expected


def test_engine_picker_uses_mention_count_when_no_explicit_instruction():
    """Without an explicit "build/make with X" phrase, the engine with
    more mentions wins. Catches the original first-pattern-wins bug."""
    # Unity mentioned 3x, Godot mentioned 1x, no explicit instruction
    prompt = (
        "Some game design notes. Unity is good for mobile. "
        "Unity has good docs. Unity 2022 LTS is solid. "
        "Godot is also fine."
    )
    assert _pick_engine(prompt) == "unity"


def test_engine_picker_falls_back_to_first_when_tied():
    """When mention count is tied AND no explicit instruction, fall back
    to first-occurrence order so behavior is deterministic."""
    prompt = "Godot or Unity, your pick"
    # Both mentioned once → first occurrence (Godot) wins as a stable tie.
    assert _pick_engine(prompt) == "godot"


def test_engine_picker_returns_none_when_no_engine_named():
    assert _pick_engine("Build me a 2D platformer game") is None


# ───────────────────────── genre: FPS false positive ──────────────────


@pytest.mark.parametrize("prompt", [
    "FPS ≥ 60 on mid-range Android",
    "Target FPS: 60",
    "60 fps performance target",
    "Maintain 30fps minimum",
    "performance: fps ≤ 16ms frame time",
])
def test_fps_as_perf_metric_is_NOT_classified_as_fps_genre(prompt):
    """"FPS ≥ 60" is a perf budget, not the shooter genre. The detector
    must skip these so a Hole-style puzzle game prompt with a perf
    checklist doesn't get scaffolded as an FPS shooter."""
    _, req = classify_prompt(prompt + " — and make it a Unity puzzle game")
    assert req is not None
    assert req.genre != "fps", (
        f"prompt {prompt!r} was misclassified as fps shooter"
    )


@pytest.mark.parametrize("prompt", [
    "Build me a Unity FPS shooter",
    "Make a first-person shooter game",
    "Create an FPS game with deathmatch",
    "Unity FPS with multiplayer",
])
def test_genuine_fps_genre_still_detected(prompt):
    """Don't break the real FPS case while fixing the false positive."""
    _, req = classify_prompt(prompt)
    assert req is not None
    assert req.genre == "fps"


# ───────────────────────── perspective: 2D unicode hyphens ────────────


@pytest.mark.parametrize("prompt", [
    "a 2D puzzle game",
    "a 2-D puzzle game",       # ASCII hyphen
    "a 2‑D puzzle game",  # U+2011 non-breaking hyphen
    "a 2‐D puzzle game",  # U+2010 hyphen
    "a 2–D puzzle game",  # U+2013 en dash
    "a 2—D puzzle game",  # U+2014 em dash
    "Build a 2 D mobile puzzle game",  # space-separated
])
def test_2d_detection_handles_all_hyphen_variants(prompt):
    """The HoleGame user's prompt had "2‑D" with a U+2011 non-breaking
    hyphen. The old regex only matched "2d". Now all common hyphen
    variants resolve to perspective=2d."""
    _, req = classify_prompt(prompt + " — build with Unity")
    assert req is not None
    assert req.perspective == "2d", f"prompt {prompt!r} → {req.perspective}"


# ───────────────────────── target: mobile + web detection ─────────────


@pytest.mark.parametrize("prompt,expected_primary,expected_in_set", [
    ("Build a Unity game for mobile apps and web",     "android", {"android", "web"}),
    ("Build a Unity Android game",                     "android", {"android"}),
    ("Build a Unity iOS app",                          "ios",     {"ios"}),
    ("Build a Unity game for the App Store",           "ios",     {"ios"}),
    ("Build a Unity game for Google Play Store",       "android", {"android"}),
    ("Build a Unity game for Steam",                   "windows", {"windows"}),
    ("Build a Unity macOS game",                       "mac",     {"mac"}),
    ("Build a Unity Linux game",                       "linux",   {"linux"}),
    ("Build a Unity browser game in WebGL",            "web",     {"web"}),
    # "desktop" alone is ambiguous (Win/Mac/Linux) so the picker only
    # catches the mobile half. Naming a specific desktop OS (windows,
    # mac, linux) is how users get desktop into the target set.
    ("Build a Unity game for both mobile and Windows", "android",
        {"android", "windows"}),
])
def test_target_picker_recognises_mobile_and_web(prompt, expected_primary,
                                                   expected_in_set):
    """The HoleGame user said "mobile apps and web" — sage defaulted to
    web. Now mobile wins primary (most-engaged platform) and the full
    set covers everything the user named."""
    primary, full = _pick_targets(prompt)
    assert primary == expected_primary, (
        f"prompt {prompt!r} → primary={primary!r}, expected {expected_primary!r}"
    )
    assert set(full) >= expected_in_set, (
        f"prompt {prompt!r} → targets={set(full)!r}, "
        f"missing {expected_in_set - set(full)!r}"
    )


def test_classify_prompt_threads_target_into_game_request():
    """The detector's target choice must end up on the GameRequest so
    the pipeline can pass it to the engine adapter's build()."""
    _, req = classify_prompt(
        "Build a Unity puzzle game for mobile apps and web"
    )
    assert req is not None
    assert req.target == "android"


def test_default_target_stays_web_when_no_platform_named():
    """When the prompt doesn't name a platform, default to web — the
    safest, most-shareable target."""
    _, req = classify_prompt("Build a Unity 2D puzzle game")
    assert req is not None
    assert req.target == "web"


# ───────────────────────── scaffold pollution guard ───────────────────


def test_scaffold_pollution_detected_when_godot_scaffold_exists(tmp_path):
    """Mimic the HoleGame disaster: existing Godot scaffold, then a new
    Unity run wants the same directory. The guard must catch it."""
    # Drop the Godot signature files
    (tmp_path / "project.godot").write_text("config_version=5\n")
    (tmp_path / ".godot").mkdir()
    (tmp_path / ".godot" / ".gdignore").write_text("")

    assert _detect_existing_engine(tmp_path) == "godot"

    req = GameRequest(
        task_type="game", engine="unity", genre="puzzle",
        perspective="2d", target="android",
        raw_prompt="build a unity game",
    )

    with pytest.raises(ScaffoldPollution) as exc:
        build_game(req, tmp_path, lambda _p: "{}",
                   progress=lambda _: None, heal_rounds=0)
    assert exc.value.requested_engine == "unity"
    assert exc.value.existing_engine == "godot"


def test_same_engine_in_existing_dir_proceeds(tmp_path, monkeypatch):
    """Re-running with the SAME engine on an existing scaffold must
    proceed (the heal loop is a legitimate use case for this) — it
    should get PAST the pollution check, not be blocked by it."""
    (tmp_path / "project.godot").write_text("config_version=5\n")
    (tmp_path / ".godot").mkdir()
    assert _detect_existing_engine(tmp_path) == "godot"

    # Force the Godot adapter factory to return an instance with detect
    # patched to None — so the build raises EngineNotInstalled (proves
    # the pollution check passed) instead of ScaffoldPollution.
    from sage.games.engines import REGISTRY
    from sage.games.engines.godot import GodotAdapter
    from sage.games.exceptions import EngineNotInstalled

    class _StubGodot(GodotAdapter):
        def detect(self): return None

    monkeypatch.setitem(REGISTRY, "godot", _StubGodot)

    req = GameRequest(task_type="game", engine="godot",
                      raw_prompt="continue building")
    with pytest.raises(EngineNotInstalled):
        build_game(req, tmp_path, lambda _p: "{}",
                   progress=lambda _: None, heal_rounds=0)


def test_empty_directory_no_pollution(tmp_path):
    """A clean directory must not trigger pollution detection."""
    assert _detect_existing_engine(tmp_path) is None


def test_unity_signature_detected(tmp_path):
    (tmp_path / "Assets" / "Editor").mkdir(parents=True)
    (tmp_path / "Assets" / "Editor" / "SageBuilder.cs").write_text("// stub")
    (tmp_path / "ProjectSettings").mkdir()
    (tmp_path / "ProjectSettings" / "ProjectVersion.txt").write_text(
        "m_EditorVersion: 2022.3.17f1\n"
    )
    assert _detect_existing_engine(tmp_path) == "unity"


def test_polluted_directory_returns_higher_match_engine(tmp_path):
    """If a dir has BOTH Godot + Unity files (the HoleGame mess), the
    detector returns whichever engine has more signature hits. This
    lets the guard surface 'existing engine = whichever-is-more-present'
    rather than randomly picking one."""
    # Godot: 2 signatures (project.godot + .godot/)
    (tmp_path / "project.godot").write_text("config_version=5\n")
    (tmp_path / ".godot").mkdir()
    # Unity: 1 signature (ProjectVersion only — no SageBuilder.cs)
    (tmp_path / "ProjectSettings").mkdir()
    (tmp_path / "ProjectSettings" / "ProjectVersion.txt").write_text(
        "m_EditorVersion: 2022.3.17f1\n"
    )
    assert _detect_existing_engine(tmp_path) == "godot"


# ───────────────────────── real Hole prompt end-to-end ────────────────


_REAL_HOLE_PROMPT = """\
Hole it: Black Hole Puzzle Game. Swallow the world, one puzzle at a time!
Get ready for Hole it, the most satisfying brain game of the year. Dive into
a universe of colorful puzzles where you are the all-powerful black hole.

Technical Stack: Unity 2022 LTS + URP, optional Godot 4, LeanTouch.
Testing Checklist: FPS ≥ 60 on mid-range Android, memory < 150 MB.

All code should be Unity C# (2022 LTS) but also include a Godot 4 GDScript
version. Mention Unity‑Copilot, Godot‑AI, Game‑Maker‑AI as
tools to consider.

This is a 2‑D mobile puzzle‑action game.

Make this video game with Unity and make sure that it works on mobile apps
and web. Make sure the assets are interesting. Build with ads for free users.
"""


def test_real_hole_game_prompt_now_classifies_correctly():
    """The end-to-end fix. Locking in the exact classification we want
    for the user's actual prompt."""
    task_type, req = classify_prompt(_REAL_HOLE_PROMPT)
    assert task_type == "game"
    assert req is not None
    assert req.engine == "unity",       f"engine = {req.engine}"
    assert req.genre == "puzzle",       f"genre = {req.genre}"
    assert req.perspective == "2d",     f"perspective = {req.perspective}"
    assert req.target == "android",     f"target = {req.target}"
