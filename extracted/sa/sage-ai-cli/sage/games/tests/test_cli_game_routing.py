"""CLI routing for game prompts.

`sage ask` and `sage run` are the entry points users actually type. For
game prompts to route through the games pipeline at all, the prompt
must pass `looks_like_build_request()` — otherwise the simple-QA path
sends it to the LLM as a chat message and the user gets a description
of a game instead of a built game.

Before the keyword fix, "Build me a Godot platformer" silently fell
through to chat. These tests lock down the build-request detector
recognizes every supported engine + every common game genre as a
build-style prompt.
"""

from __future__ import annotations

import pytest

from sage.core.principal_engineer import (
    decompose_multi_build_request,
    looks_like_build_request,
)


# ───────────────────────── must classify as build ─────────────────────


@pytest.mark.parametrize("prompt", [
    # Each supported engine, in a natural-language build prompt
    "Build me a Godot 4 platformer with pixel art",
    "Make a Unity 3D first-person shooter with multiplayer",
    "Create an Unreal Engine 5 third-person action game",
    "Build a Bevy roguelike with procedural dungeons",
    "Make a Phaser 3 puzzle game with 20 levels",
    "Create a LÖVE 2D shmup with bullet-hell mechanics",
    "Build a pygame top-down shooter with waves",
    "Make a GameMaker Studio 2 metroidvania",
    "Build me a Construct 3 racing game",
    "Create an RPG Maker MZ JRPG with turn-based combat",
    # Genre-only prompts (no engine named) — still must route to build pipeline
    "Build a metroidvania about a robot ninja",
    "Create a roguelike with permadeath",
    "Make a 2D platformer with double-jump",
    "Build a 3D game with combat and crafting",
])
def test_game_build_prompts_route_to_build_pipeline(prompt):
    """The build-request detector must recognize these as buildable so the
    CLI routes them through `_route_to_principal_pipeline` rather than
    treating them as chat questions."""
    assert looks_like_build_request(prompt), (
        f"prompt did not route to build pipeline: {prompt!r}"
    )


# ───────────────────────── must NOT classify as build ─────────────────


@pytest.mark.parametrize("prompt", [
    "What is the difference between Godot 3 and Godot 4?",
    "How do I install Unity on Linux?",
    "Explain how to use Phaser physics",
    "Can you describe metroidvania level design principles?",
    "What is itertools.groupby in Python?",
    "Hello, how are you?",
])
def test_question_prompts_about_games_stay_chat(prompt):
    """Questions ABOUT games (vs. requests to BUILD them) must stay in
    chat. Catch the regression where "explain godot physics" accidentally
    triggers a full project build."""
    assert not looks_like_build_request(prompt), (
        f"question prompt incorrectly classified as build: {prompt!r}"
    )


# ───────────────────────── multi-build decomposition ──────────────────


def test_multi_build_prompt_with_mixed_game_and_webapp():
    """Sage supports compound prompts producing sub-projects when each
    "Build X" header starts its own line. A mixed prompt — webapp + game
    — must split cleanly so each sub-task routes to its own pipeline.

    The detector requires line-start anchors to avoid false splits on
    sentences like "Build something good. The kind of game that..." so
    the test uses the documented multi-task form (one header per line)."""
    prompt = (
        "Build a FastAPI backend for user authentication.\n"
        "Build a Godot 4 platformer with the same theme."
    )
    sub_tasks = decompose_multi_build_request(prompt)
    # decompose_multi_build_request returns [(label, sub_task), ...]
    assert len(sub_tasks) == 2, f"expected 2 sub-tasks, got {len(sub_tasks)}"
    sub_texts = [t[1].lower() for t in sub_tasks]
    # The split keeps engine + framework keywords together with their task.
    assert any("fastapi" in t for t in sub_texts)
    assert any("godot" in t for t in sub_texts)


# ───────────────────────── full CLI → pipeline → games path ───────────


def test_principal_pipeline_routes_godot_game_prompt_through_games(monkeypatch, tmp_path):
    """End-to-end: a game prompt entered as text goes through:
      looks_like_build_request → _route_to_principal_pipeline →
      build_project_principal → decompose_spec (classifier) → build_game.

    We mock build_game itself so this is fast — we're proving the WIRING
    works, not the build itself (which the other test files cover)."""
    from sage.core.principal_builder import build_project_principal
    from sage.core.spec_decomposer import ProjectPlan, StackProfile
    from sage.games.engines.base import GameRequest
    from sage.games.pipeline import GameBuildReport

    # Stub decompose_spec to return a game-task ProjectPlan unconditionally
    # (the real one would route the prompt through the games detector,
    # but that's covered elsewhere).
    def stub_decompose(spec, _gen):
        assert "godot" in spec.lower(), "test prompt should mention godot"
        return ProjectPlan(
            title="CLI Test Game",
            features=[], stack=StackProfile(),
            task_type="game",
            game_request=GameRequest(
                task_type="game", engine="godot", genre="platformer",
                perspective="2d", target="web",
                raw_prompt=spec,
            ),
        )

    monkeypatch.setattr(
        "sage.core.principal_builder.decompose_spec", stub_decompose,
    )

    build_calls: list[dict] = []

    def stub_build_game(req, out_dir, generate, *, progress=None, **kwargs):
        build_calls.append({
            "engine": req.engine, "genre": req.genre, "out_dir": str(out_dir),
        })
        return GameBuildReport(
            engine="godot", out_dir=str(out_dir), target="web",
            sprite_count=2, audio_count=1,
            scripts_written=["scripts/Main.gd"],
            build_artifact=str(out_dir / "build" / "index.html"),
        )

    monkeypatch.setattr("sage.games.pipeline.build_game", stub_build_game)

    report = build_project_principal(
        "Build me a Godot 4 platformer", tmp_path,
        generate=lambda _p: "{}", progress=lambda _m: None,
    )

    # The games pipeline was reached.
    assert len(build_calls) == 1
    assert build_calls[0]["engine"] == "godot"
    # The PrincipalBuildReport carries the games-pipeline result.
    assert report.stack == {"engine": "godot"}
    assert report.install_ok is True


def test_game_prompts_dont_invoke_webapp_specific_helpers(monkeypatch, tmp_path):
    """Critical: a game prompt MUST NOT trigger plan_layout /
    resolve_dependencies / emit_node_package_json. These functions are
    webapp-shaped and would emit FastAPI/React files into a game project."""
    from sage.core.principal_builder import build_project_principal
    from sage.core.spec_decomposer import ProjectPlan, StackProfile
    from sage.games.engines.base import GameRequest
    from sage.games.pipeline import GameBuildReport

    monkeypatch.setattr(
        "sage.core.principal_builder.decompose_spec",
        lambda _s, _g: ProjectPlan(
            title="T", features=[], stack=StackProfile(),
            task_type="game",
            game_request=GameRequest(
                task_type="game", engine="phaser", target="web",
                raw_prompt="test",
            ),
        ),
    )

    def _trap(*a, **kw):
        raise AssertionError(
            "webapp helper invoked on a game prompt — pipeline routing leak"
        )

    monkeypatch.setattr("sage.core.principal_builder.plan_layout", _trap)
    monkeypatch.setattr("sage.core.principal_builder.resolve_dependencies", _trap)
    monkeypatch.setattr(
        "sage.core.principal_builder.emit_node_package_json", _trap,
    )

    monkeypatch.setattr(
        "sage.games.pipeline.build_game",
        lambda *a, **kw: GameBuildReport(
            engine="phaser", out_dir=".", target="web",
            sprite_count=0, scripts_written=[],
        ),
    )

    # Must complete without raising AssertionError.
    report = build_project_principal(
        "build a phaser puzzle game", tmp_path,
        generate=lambda _p: "{}", progress=lambda _m: None,
    )
    assert report.stack == {"engine": "phaser"}
