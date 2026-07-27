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
    PrincipalBuildReport must reflect file_count = scripts+sprites+meshes+audio.

    tests_ok is NOT simply "a build artifact exists". For a game the
    falsifiable claim is that its generated media assets are real files with
    correct magic bytes and a parseable container. This stub REPORTS asset
    counts but writes no asset files, so tests_ok must be False — reporting
    True here would be the "counted files it never verified" lie."""
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
    assert report.build_ok is True    # had a build_artifact
    assert report.tests_ok is False, (
        "the stub reported 3 sprites + 2 audio files but wrote none of them; "
        "tests_ok must not be True on the strength of a build artifact alone"
    )


def test_games_path_with_real_assets_reports_tests_ok(tmp_path, monkeypatch):
    """Positive control: when build_game actually WRITES valid assets and a
    build artifact, tests_ok is True. This is the same code path as the test
    above, so neither assertion is a constant compared with itself."""
    import struct
    import zlib

    monkeypatch.setattr(
        "sage.core.principal_builder.decompose_spec",
        lambda _spec, _gen: _stub_game_plan(),
    )

    def _write_real_png(path):
        def chunk(tag, data):
            return (
                struct.pack(">I", len(data))
                + tag
                + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
            )

        w = h = 4
        raw = b"".join(b"\x00" + bytes([0, 128, 255] * w) for _ in range(h))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(
            b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw))
            + chunk(b"IEND", b"")
        )

    def fake_build_game(req, out_dir, generate, *, progress=None, **kwargs):
        _write_real_png(out_dir / "assets" / "sprite.png")
        artifact = out_dir / "build" / "index.html"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("<html><body>game</body></html>")
        return GameBuildReport(
            engine="godot", out_dir=str(out_dir), target="web",
            sprite_count=1, mesh_count=0, audio_count=0,
            scripts_written=["scripts/Main.gd"],
            build_artifact=str(artifact), build_size_bytes=42,
            build_duration_s=0.1, heal_rounds=0,
        )

    monkeypatch.setattr("sage.games.pipeline.build_game", fake_build_game)
    report = build_project_principal(
        "anything", tmp_path, generate=lambda _p: "{}", progress=lambda _m: None,
    )
    assert report.tests_ok is True, (
        "a build artifact plus a genuinely valid PNG should verify"
    )


def test_games_path_with_stub_asset_fails_verification(tmp_path, monkeypatch):
    """A 4-byte `b"glTF"` stub asset must fail, even with a build artifact.

    This is the historical bug: the pipeline touched empty/near-empty files
    and reported success.
    """
    monkeypatch.setattr(
        "sage.core.principal_builder.decompose_spec",
        lambda _spec, _gen: _stub_game_plan(),
    )

    def fake_build_game(req, out_dir, generate, *, progress=None, **kwargs):
        (out_dir / "assets").mkdir(parents=True, exist_ok=True)
        (out_dir / "assets" / "model.glb").write_bytes(b"glTF")
        artifact = out_dir / "build" / "index.html"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("<html></html>")
        return GameBuildReport(
            engine="godot", out_dir=str(out_dir), target="web",
            sprite_count=0, mesh_count=1, audio_count=0,
            scripts_written=["scripts/Main.gd"],
            build_artifact=str(artifact),
        )

    monkeypatch.setattr("sage.games.pipeline.build_game", fake_build_game)
    report = build_project_principal(
        "anything", tmp_path, generate=lambda _p: "{}", progress=lambda _m: None,
    )
    assert report.tests_ok is False, "a 4-byte glTF stub asset must fail verification"


def test_games_path_success_without_build_artifact_is_not_green(tmp_path, monkeypatch):
    """Scaffold-only adapters (GUI engines) leave build_artifact as None.

    That used to surface as tests_ok=None, which the build pipeline then
    aggregated as "not a failure". Nothing was verified, so it is False.
    """
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
    assert report.tests_ok is False, (
        "no build artifact and no verified assets means nothing was proven"
    )


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
