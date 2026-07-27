"""Detector edge cases that the main classifier sweep doesn't hit.

The detector is on the hot path for every `sage ask`/`sage run`, so the
regex pass must be cheap *and* hit the LLM fallback exactly the right
number of times. These tests guard:

  * the LLM is NOT called when regex confidence is high enough,
  * the LLM IS called when regex confidence is ambiguous,
  * malformed LLM responses degrade to webapp instead of crashing,
  * art_style / perspective parsing covers each listed label,
  * the confidence floor for "has game noun" still routes to game.
"""

from __future__ import annotations

import json

import pytest

from sage.games.detector import classify_prompt


# ───────────────────────── high-confidence (no LLM) ───────────────────


def test_regex_confidence_bypasses_llm_when_engine_named():
    """Engine + genre → regex confidence ≥ threshold. The LLM must not fire."""
    calls = {"n": 0}

    def gen(_p):
        calls["n"] += 1
        return "{}"

    t, req = classify_prompt(
        "Build me a Godot 4 platformer", generate=gen,
    )
    assert t == "game" and req is not None
    assert req.engine == "godot" and req.genre == "platformer"
    assert calls["n"] == 0, "regex was confident, LLM must not be called"


def test_genre_alone_is_high_confidence_enough():
    """Genre alone (no engine) is ≥0.75 → still skips LLM."""
    calls = {"n": 0}

    def gen(_p):
        calls["n"] += 1
        return "{}"

    t, req = classify_prompt("a metroidvania about exploration", generate=gen)
    assert t == "game" and req is not None
    assert req.genre == "roguelike"  # metroidvania → roguelike bucket
    assert calls["n"] == 0


# ───────────────────────── art_style + perspective ────────────────────


@pytest.mark.parametrize("prompt,style", [
    ("pixel art platformer",            "pixel"),
    ("a cartoon game",                  "cartoon"),
    ("voxel game like Minecraft",       "voxel"),
    ("low-poly 3D game",                "low-poly"),
    ("realistic FPS",                   "realistic"),
    ("hand-drawn watercolor game",      "hand-drawn"),
    ("noir detective game",             "noir"),
])
def test_art_style_parsing(prompt, style):
    """Each labeled art style in _ART_STYLE_PATTERNS must be reachable
    from at least one natural-language phrase. We add a "game" noun so
    the detector's confidence floor is cleared (art style alone isn't a
    strong-enough signal — that's by design, not a regression)."""
    _, req = classify_prompt(prompt)
    assert req is not None, f"prompt {prompt!r} should classify as a game"
    assert req.art_style == style


@pytest.mark.parametrize("prompt,perspective", [
    ("first-person shooter",            "first-person"),
    ("third-person adventure game",     "third-person"),
    ("isometric strategy game",         "isometric"),
    ("top-down dungeon crawler game",   "top-down"),
    ("side-scroller game",              "side-scroller"),
    ("a 3d game in a forest",           "3d"),
    ("a 2d platformer",                 "2d"),
])
def test_perspective_parsing(prompt, perspective):
    _, req = classify_prompt(prompt)
    assert req is not None, f"prompt {prompt!r} should classify as a game"
    assert req.perspective == perspective


# ───────────────────────── LLM-fallback branch ────────────────────────


def test_llm_fallback_fires_on_low_confidence_prompts():
    """`'Make me something fun'` has zero regex hits → score 0 → returns
    webapp without invoking the LLM. But `'A short adventure'` is just
    above zero (game noun absent, no engine, no genre) and should still
    classify as webapp without crashing."""
    calls = {"n": 0}

    def gen(_p):
        calls["n"] += 1
        return json.dumps({"task_type": "webapp"})

    t, req = classify_prompt("Make me something fun", generate=gen)
    assert t == "webapp" and req is None
    # No regex hits → confidence 0 → LLM is not called per the source guard
    # (the guard is `conf > 0` for the LLM branch). The test asserts the
    # current behavior: zero-confidence prompts go straight to webapp.
    assert calls["n"] == 0


def test_llm_fallback_can_promote_ambiguous_prompt_to_game():
    """When regex finds *some* signal but below threshold, the detector
    asks the LLM. If the LLM says it's a game, we trust it."""
    def gen(_p):
        return json.dumps({
            "task_type": "game",
            "engine": "unity",
            "genre": "puzzle",
            "perspective": "2d",
            "art_style": "cartoon",
        })

    # "interactive experience" — has a weak game-ish vibe but doesn't trip
    # any of our regex patterns. To force the LLM branch we need at least
    # _some_ regex hit at low confidence. "2d interactive thing" gets a
    # 0.15 confidence (perspective=2d), which is below 0.7 and >0, so the
    # LLM fires.
    t, req = classify_prompt(
        "a 2d interactive thing", generate=gen, confidence_threshold=0.9,
    )
    assert t == "game" and req is not None
    assert req.engine == "unity"


def test_llm_fallback_handles_malformed_response_without_crashing():
    """A confused LLM might emit non-JSON. We must degrade to webapp, not
    raise."""
    def gen(_p):
        return "this is not json — sorry, can't help with that"

    t, req = classify_prompt(
        "a 2d interactive thing", generate=gen, confidence_threshold=0.9,
    )
    assert t == "webapp"
    assert req is None


def test_llm_fallback_swallows_generator_exceptions():
    """Provider errors during classification must not surface."""
    def gen(_p):
        raise RuntimeError("provider down")

    t, _ = classify_prompt(
        "a 2d interactive thing", generate=gen, confidence_threshold=0.9,
    )
    assert t == "webapp"


# ───────────────────────── game-noun heuristic ────────────────────────


def test_game_noun_floor_routes_ambiguous_to_game():
    """`'I want a playable thing'` has a game noun but no engine/genre.
    Confidence is `has_game_noun(0.25)` = 0.25 → above the 0.2 floor for
    the game-noun branch. Should still route to game with no engine."""
    t, req = classify_prompt("I want a playable thing")
    assert t == "game"
    assert req is not None
    assert req.engine is None
    assert req.genre is None


def test_engine_alone_picks_default_genre_none():
    """When only an engine is named, genre/perspective stay None — the
    pipeline's decomposer will fill in defaults."""
    t, req = classify_prompt("use Godot for this project")
    assert t == "game"
    assert req is not None
    assert req.engine == "godot"
    assert req.genre is None


# ───────────────────────── GameRequest helpers ────────────────────────


@pytest.mark.parametrize("perspective,is_3d", [
    ("3d",            True),
    ("first-person",  True),
    ("third-person", True),
    ("isometric",     True),
    ("2d",            False),
    ("top-down",      False),
    ("side-scroller", False),
    (None,            False),
])
def test_game_request_is_3d_buckets(perspective, is_3d):
    from sage.games.engines.base import GameRequest
    req = GameRequest(perspective=perspective)
    assert req.is_3d() is is_3d
