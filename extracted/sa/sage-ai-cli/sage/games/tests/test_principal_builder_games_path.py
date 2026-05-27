"""principal_builder games-path integration.

`build_project_principal` is the function the CLI calls. When the spec
classifies as a game, it must:

  - delegate to `sage.games.pipeline.build_game`,
  - translate the resulting GameBuildReport into a PrincipalBuildReport,
  - catch EngineNotInstalled and produce a report with install_ok=False,
  - catch BuildNotSupported / GameBuildIncomplete and produce a report
    with install_ok=True but tests_ok=False (sage tried; the engine
    can't build it for us).

The fixture mocks `decompose_spec` so we don't pay LLM cost for the
classifier round-trip — that part is covered by the detector tests.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sage.core.principal_builder import (
    PrincipalBuildReport,
    build_project_principal,
)
from sage.core.spec_decomposer import ProjectPlan, StackProfile
from sage.games.engines.base import GameRequest
from sage.games.exceptions import (
    BuildNotSupported,
    EngineNotInstalled,
    GameBuildIncomplete,
)
from sage.games.pipeline import GameBuildReport


# ───────────────────────── helpers ────────────────────────────────────


def _stub_game_plan(engine: str = "godot") -> ProjectPlan:
    """Force decompose_spec to return a game-task ProjectPlan."""
    return ProjectPlan(
        title="Test Game",
        features=[],
        stack=StackProfile(),
        task_type="game",
        game_request=GameRequest(
            task_type="game", engine=engine, genre="platformer",
            perspective="2d", art_style="pixel", target="web",
            raw_prompt="test prompt",
        ),
    )


# ───────────────────────── happy path ─────────────────────────────────


def test_games_path_success_translates_to_principal_report(tmp_path, monkeypatch):
    """build_game returns a GameBuildReport with a build_artifact → the
    PrincipalBuildReport must reflect file_count = scripts+sprites+meshes+audio
    and tests_ok=True."""
    monkeypatch.setattr(
        "sage.core.principal_builder.decompose_spec",
        lambda _spec, _gen: _stub_game_plan(),
    )

    def fake_build_game(req, out_dir, generate, *, progress=None, **kwargs):
        progress and progress("[stub] running fake build")
        return GameBuildReport(
            engine="godot",
            out_dir=str(out_dir),
            target="web",
            sprite_count=3,
            mesh_count=0,
            audio_count=2,
            scripts_written=["scripts/Main.gd", "scripts/Player.gd"],
            build_artifact=str(out_dir / "build" / "index.html"),
            build_size_bytes=12345,
            build_duration_s=1.5,
            heal_rounds=0,
        )

    monkeypatch.setattr("sage.games.pipeline.build_game", fake_build_game)

    report = build_project_principal(
        "doesn't matter — decompose is mocked", tmp_path,
        generate=lambda _p: "{}", progress=lambda _m: None,
    )
    assert isinstance(report, PrincipalBuildReport)
    assert report.title == "Test Game"
    assert report.stack == {"engine": "godot"}
    # file_count = len(scripts_written) + sprite_count + mesh_count + audio_count
    assert report.file_count == 2 + 3 + 0 + 2
    assert report.install_ok is True
    assert report.tests_ok is True   # had a build_artifact


def test_games_path_success_without_build_artifact_marks_tests_none(tmp_path, monkeypatch):
    """Scaffold-only adapters (GUI engines) succeed but leave build_artifact
    as None — that must surface as tests_ok=None, not False."""
    monkeypatch.setattr(
        "sage.core.principal_builder.decompose_spec",
        lambda _spec, _gen: _stub_game_plan("gamemaker"),
    )

    def fake_build_game(req, out_dir, generate, *, progress=None, **kwargs):
        return GameBuildReport(
            engine="gamemaker", out_dir=str(out_dir), target="windows",
            sprite_count=1, scripts_written=[], build_artifact=None,
        )

    monkeypatch.setattr("sage.games.pipeline.build_game", fake_build_game)

    report = build_project_principal(
        "anything", tmp_path, generate=lambda _p: "{}",
        progress=lambda _m: None,
    )
    assert report.install_ok is True
    assert report.tests_ok is None  # no build_artifact → undetermined


# ───────────────────────── error translation ──────────────────────────


def test_games_path_engine_not_installed_returns_install_failed(tmp_path, monkeypatch):
    """EngineNotInstalled is a system-config issue, not a sage bug. We
    return a report with install_ok=False, no exception."""
    monkeypatch.setattr(
        "sage.core.principal_builder.decompose_spec",
        lambda _spec, _gen: _stub_game_plan("unreal"),
    )

    def raises_not_installed(*a, **kw):
        raise EngineNotInstalled("unreal", "Install UE5 first")

    monkeypatch.setattr("sage.games.pipeline.build_game", raises_not_installed)

    msgs: list[str] = []
    report = build_project_principal(
        "build me an unreal game", tmp_path,
        generate=lambda _p: "{}", progress=msgs.append,
    )
    assert report.install_ok is False
    assert report.tests_ok is False
    assert report.stack == {"engine": "unreal"}
    # The user-facing log mentions the failure.
    assert any("unreal" in m.lower() and "not installed" in m.lower()
               for m in msgs)


def test_games_path_build_not_supported_returns_install_ok_tests_failed(tmp_path, monkeypatch):
    """A GUI engine that raises BuildNotSupported during build still
    scaffolded successfully — install_ok=True, tests_ok=False."""
    monkeypatch.setattr(
        "sage.core.principal_builder.decompose_spec",
        lambda _spec, _gen: _stub_game_plan("gamemaker"),
    )

    def raises_build_not_supported(*a, **kw):
        raise BuildNotSupported("gamemaker", "editor required")

    monkeypatch.setattr(
        "sage.games.pipeline.build_game", raises_build_not_supported,
    )
    report = build_project_principal(
        "anything", tmp_path, generate=lambda _p: "{}",
        progress=lambda _m: None,
    )
    assert report.install_ok is True
    assert report.tests_ok is False
    assert report.stack == {"engine": "gamemaker"}


def test_games_path_build_incomplete_returns_install_ok_tests_failed(tmp_path, monkeypatch):
    """The heal loop exhausted without a passing build. Translate to
    install_ok=True (we got to the build step) but tests_ok=False."""
    monkeypatch.setattr(
        "sage.core.principal_builder.decompose_spec",
        lambda _spec, _gen: _stub_game_plan("godot"),
    )

    def raises_incomplete(*a, **kw):
        raise GameBuildIncomplete("build never converged", report={})

    monkeypatch.setattr("sage.games.pipeline.build_game", raises_incomplete)
    report = build_project_principal(
        "anything", tmp_path, generate=lambda _p: "{}",
        progress=lambda _m: None,
    )
    assert report.install_ok is True
    assert report.tests_ok is False


# ───────────────────────── decompose stays untouched ──────────────────


def test_games_path_does_not_invoke_webapp_pipeline(tmp_path, monkeypatch):
    """Critical guarantee: when task_type='game', we MUST NOT call into
    plan_layout / resolve_dependencies / emit_node_package_json — those
    are webapp-only. Catch any leakage by failing-fast if invoked."""
    monkeypatch.setattr(
        "sage.core.principal_builder.decompose_spec",
        lambda _spec, _gen: _stub_game_plan("phaser"),
    )

    def _explode(*a, **kw):
        raise AssertionError("webapp-only path leaked into games branch")

    monkeypatch.setattr("sage.core.principal_builder.plan_layout", _explode)
    monkeypatch.setattr(
        "sage.core.principal_builder.resolve_dependencies", _explode,
    )

    def fake_build_game(*a, **kw):
        return GameBuildReport(
            engine="phaser", out_dir=".", target="web",
            sprite_count=0, scripts_written=[],
        )

    monkeypatch.setattr("sage.games.pipeline.build_game", fake_build_game)
    report = build_project_principal(
        "anything", tmp_path, generate=lambda _p: "{}",
        progress=lambda _m: None,
    )
    assert report.stack == {"engine": "phaser"}
