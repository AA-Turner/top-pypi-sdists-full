"""Pipeline-internals coverage: the bits between the adapter calls.

`build_game` orchestrates four phases:
  1. _decompose — LLM call → GamePlan (or a sanity-floor fallback plan)
  2. scaffold + emit_scripts — delegated to the adapter
  3. _generate_assets — parallel sprite/mesh/audio generation
  4. build + heal loop — retry the adapter's build() up to N times

These tests focus on the bits that aren't engine-specific: decomposer
robustness, parallel-asset error handling, the heal loop, and the report
shape we promise downstream (principal_builder reads from it directly).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from sage.games.engines import REGISTRY, get_adapter
from sage.games.engines.base import (
    BuildArtifact,
    EngineCapability,
    GamePlan,
    GameRequest,
)
from sage.games.exceptions import GameBuildIncomplete
from sage.games.pipeline import (
    GameBuildReport,
    _decompose,
    _generate_assets,
    _heal_round,
    build_game,
)


# ───────────────────────── helpers ────────────────────────────────────


def _req(engine: str = "godot", **overrides) -> GameRequest:
    base = {
        "task_type": "game", "engine": engine, "genre": "platformer",
        "perspective": "2d", "art_style": "pixel", "target": "web",
        "raw_prompt": "a test game",
    }
    base.update(overrides)
    return GameRequest(**base)


def _decompose_json(**overrides) -> str:
    base = {
        "title": "Decomposed Title",
        "description": "two sentence pitch",
        "features": ["jump", "dash", "win"],
        "sprites": [{"role": "player", "prompt": "hero sprite"}],
        "meshes": [],
        "audio": [{"role": "theme", "prompt": "loop", "kind": "music"}],
    }
    base.update(overrides)
    return json.dumps(base)


# ───────────────────────── _decompose ─────────────────────────────────


def test_decompose_happy_path_parses_llm_json():
    plan = _decompose(
        _req(), generate=lambda _p: _decompose_json(), log=lambda _: None,
    )
    assert plan.title == "Decomposed Title"
    assert plan.description == "two sentence pitch"
    assert plan.features == ["jump", "dash", "win"]
    assert plan.sprite_roles == [("player", "hero sprite")]
    assert plan.audio_roles == [("theme", "loop", "music")]
    # 2d game → no meshes asked for, sanity floor doesn't force any.
    assert plan.mesh_roles == []


def test_decompose_3d_request_no_synthetic_mesh():
    plan = _decompose(
        _req(perspective="3d"),
        generate=lambda _p: json.dumps({"title": "x", "meshes": []}),
        log=lambda _: None,
    )
    assert not plan.mesh_roles


def test_decompose_propagates_exception_when_llm_raises():
    def boom(_prompt: str) -> str:
        raise RuntimeError("provider down")
    with pytest.raises(RuntimeError, match="provider down"):
        _decompose(_req(), generate=boom, log=lambda _: None)


def test_decompose_raises_on_malformed_json():
    with pytest.raises(RuntimeError, match="decompose: LLM response had no JSON object"):
        _decompose(
            _req(),
            generate=lambda _p: "this is not JSON {{{",
            log=lambda _: None,
        )


def test_decompose_strips_surrounding_prose_around_json():
    """LLMs frequently wrap JSON in apologetic prose. We must still parse."""
    payload = "Sure, here you go:\n\n" + _decompose_json() + "\n\nHope this helps!"
    plan = _decompose(_req(), generate=lambda _p: payload, log=lambda _: None)
    assert plan.title == "Decomposed Title"


def test_decompose_ignores_malformed_list_entries():
    """If a sprite/audio entry isn't a dict (e.g. LLM emits a string), we
    must skip it cleanly rather than KeyError mid-build."""
    payload = json.dumps({
        "title": "Garbage In",
        "sprites": [{"role": "ok", "prompt": "ok prompt"}, "not a dict", 42],
        "audio": ["also bad", {"role": "music", "prompt": "p", "kind": "music"}],
    })
    plan = _decompose(_req(), generate=lambda _p: payload, log=lambda _: None)
    sprite_roles = [r for r, _ in plan.sprite_roles]
    audio_roles = [r for r, _, _ in plan.audio_roles]
    assert "ok" in sprite_roles
    assert "music" in audio_roles


# ───────────────────────── _generate_assets ───────────────────────────


def test_generate_assets_writes_manifest_files(tmp_path, monkeypatch):
    from sage.games.assets import sprites as s
    monkeypatch.setattr(s, "_vertex_available", lambda: True)
    monkeypatch.setattr(s, "_imagen_generate", lambda prompt, size, out_path, style: out_path.write_bytes(b"\x89PNG\r\n\x1a\n"))

    plan = GamePlan(
        request=_req(), title="x", description="x",
        sprite_roles=[("hero", "blue ninja"), ("enemy", "red slime")],
        mesh_roles=[],
        audio_roles=[("intro", "intro sound", "sfx")],
        target="web",
    )
    manifest = _generate_assets(plan, tmp_path, log=lambda _: None)
    assert set(manifest.sprites) == {"hero", "enemy"}
    assert set(manifest.audio) == {"intro"}
    # Files actually exist on disk and are non-zero (except possibly silent .ogg).
    for path in manifest.sprites.values():
        assert path.is_file() and path.stat().st_size > 0
    for path in manifest.audio.values():
        assert path.is_file()


def test_generate_assets_isolates_per_role_failures(tmp_path, monkeypatch):
    """If one of the parallel asset generators raises, the rest must still
    land in the manifest — the build shouldn't fail because one sprite
    couldn't be drawn."""
    from sage.games.assets import sprites as s
    monkeypatch.setattr(s, "_vertex_available", lambda: True)

    call_log: list[str] = []

    def selective(self, role, prompt, *, size=(256, 256)):
        call_log.append(role)
        if role == "broken":
            raise RuntimeError("simulated imagen quota")
        path = self.out_dir / f"{role}.png"
        path.write_bytes(b"\x89PNG\r\n\x1a\n")
        from sage.games.assets.sprites import SpriteResult
        return SpriteResult(role, path, "imagen", *size)

    monkeypatch.setattr(s.SpriteGenerator, "generate", selective)

    plan = GamePlan(
        request=_req(), title="x", description="x",
        sprite_roles=[("good", "blue square"), ("broken", "any"), ("alsoGood", "red square")],
        mesh_roles=[], audio_roles=[],
        target="web",
    )
    manifest = _generate_assets(plan, tmp_path, log=lambda _: None)

    assert set(manifest.sprites) == {"good", "alsoGood"}
    assert "broken" not in manifest.sprites
    assert set(call_log) == {"good", "broken", "alsoGood"}


def test_generate_assets_progress_reports_totals(tmp_path, monkeypatch):
    from sage.games.assets import sprites as s
    monkeypatch.setattr(s, "_vertex_available", lambda: True)
    monkeypatch.setattr(s, "_imagen_generate", lambda prompt, size, out_path, style: out_path.write_bytes(b"\x89PNG\r\n\x1a\n"))

    plan = GamePlan(
        request=_req(), title="x", description="x",
        sprite_roles=[("a", "x"), ("b", "y")],
        mesh_roles=[],
        audio_roles=[("c", "z", "sfx")],
        target="web",
    )
    msgs: list[str] = []
    _generate_assets(plan, tmp_path, log=msgs.append)
    summary = "\n".join(msgs)
    # The trailing summary line states a non-zero file count.
    assert "files" in summary
    assert "2 sprites" in summary
    assert "1 audio" in summary


# ───────────────────────── _heal_round ────────────────────────────────


def test_heal_round_passes_error_log_to_adapter(monkeypatch, tmp_path):
    """The heal pass must hand the build's error log into the augmented
    plan that emit_scripts sees — that's how the LLM knows what to fix."""
    captured_descriptions: list[str] = []

    class CaptureAdapter:
        name = "capture"

        def emit_scripts(self, plan, out_dir, *, generate, log):
            captured_descriptions.append(plan.description)
            return []

    plan = GamePlan(
        request=_req(), title="X", description="original desc",
        features=[], sprite_roles=[], mesh_roles=[], audio_roles=[],
        target="web",
    )

    _heal_round(
        plan,
        CaptureAdapter(),
        tmp_path,
        error_log="ERROR: undefined variable `velocity` at line 42",
        generate=lambda _p: "",
        log=lambda _: None,
    )

    assert captured_descriptions, "heal must call emit_scripts"
    augmented = captured_descriptions[0]
    assert "original desc" in augmented
    assert "PREVIOUS BUILD FAILED" in augmented
    assert "undefined variable" in augmented


# ───────────────────────── full pipeline → GameBuildReport ────────────


def test_report_as_dict_round_trips():
    """principal_builder serializes the report as a dict — we lock the
    shape so a downstream rename doesn't silently break the API."""
    r = GameBuildReport(
        engine="godot", out_dir="/tmp/x", target="web",
        sprite_count=3, mesh_count=1, audio_count=2,
        scripts_written=["a.gd", "b.gd"],
        build_artifact="/tmp/x/build/index.html",
        build_size_bytes=12345, build_duration_s=2.5, heal_rounds=1,
    )
    d = r.as_dict()
    expected = {
        "engine", "out_dir", "target", "sprite_count", "mesh_count",
        "audio_count", "scripts_written", "build_artifact",
        "build_size_bytes", "build_duration_s", "heal_rounds", "install_hint",
    }
    assert set(d) == expected
    assert d["sprite_count"] == 3
    assert d["scripts_written"] == ["a.gd", "b.gd"]


def test_build_game_decompose_failure_propagates_exception(tmp_path, monkeypatch):
    """If the decompose LLM call raises, the pipeline should propagate the exception."""
    adapter = get_adapter("godot")
    monkeypatch.setattr(adapter, "detect", lambda: Path(sys.executable))

    def fake_build(out_dir, *, target, log):
        artifact = out_dir / "build" / "index.html"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_bytes(b"<html>")
        return BuildArtifact(
            output_path=artifact, target=target,
            size_bytes=artifact.stat().st_size, duration_s=0.0,
        )
    monkeypatch.setattr(adapter, "build", fake_build)
    monkeypatch.setitem(REGISTRY, "godot", lambda: adapter)

    def flaky_generate(prompt: str) -> str:
        if "Output JSON" in prompt:
            raise RuntimeError("decompose model offline")
        return "```Main.gd\nextends Node2D\nfunc _ready(): pass\n```\n"

    with pytest.raises(RuntimeError, match="decompose model offline"):
        build_game(
            _req(engine="godot"), tmp_path / "out", flaky_generate,
            progress=lambda _: None, heal_rounds=1,
        )


def test_build_game_buildnotsupported_returns_partial_report(tmp_path, monkeypatch):
    """If the adapter raises BuildNotSupported mid-build (rare but valid),
    we must still return the partial report, not raise."""
    from sage.games.exceptions import BuildNotSupported
    from sage.games.assets import sprites as s
    monkeypatch.setattr(s, "_vertex_available", lambda: True)
    monkeypatch.setattr(s, "_imagen_generate", lambda prompt, size, out_path, style: out_path.write_bytes(b"\x89PNG\r\n\x1a\n"))

    adapter = get_adapter("godot")
    monkeypatch.setattr(adapter, "detect", lambda: Path(sys.executable))

    def gui_only(out_dir, *, target, log):
        raise BuildNotSupported("godot", "simulated: editor required")
    monkeypatch.setattr(adapter, "build", gui_only)
    monkeypatch.setitem(REGISTRY, "godot", lambda: adapter)

    def gen(prompt: str) -> str:
        if "Output JSON" in prompt:
            return _decompose_json()
        return "```Main.gd\nextends Node2D\nfunc _ready(): pass\n```\n"

    report = build_game(
        _req(engine="godot"), tmp_path / "out", gen,
        progress=lambda _: None, heal_rounds=1,
    )
    # No artifact, but a real report carrying what got scaffolded.
    assert report.build_artifact is None
    assert report.sprite_count >= 1


def test_build_game_pipeline_carries_scripts_written_in_report(tmp_path, monkeypatch):
    """scripts_written should list the files relative to out_dir — the CLI
    prints these to the user as 'wrote N scripts'."""
    from sage.games.assets import sprites as s
    monkeypatch.setattr(s, "_vertex_available", lambda: True)
    monkeypatch.setattr(s, "_imagen_generate", lambda prompt, size, out_path, style: out_path.write_bytes(b"\x89PNG\r\n\x1a\n"))

    adapter = get_adapter("godot")
    monkeypatch.setattr(adapter, "detect", lambda: Path(sys.executable))

    def fake_build(out_dir, *, target, log):
        p = out_dir / "build" / "index.html"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"ok")
        return BuildArtifact(
            output_path=p, target=target, size_bytes=2, duration_s=0.0,
        )
    monkeypatch.setattr(adapter, "build", fake_build)
    monkeypatch.setitem(REGISTRY, "godot", lambda: adapter)

    def gen(prompt: str) -> str:
        if "Output JSON" in prompt:
            return _decompose_json()
        return (
            "```Main.gd\nextends Node2D\nfunc _ready(): pass\n```\n"
            "```Helper.gd\nextends Node\n```\n"
        )

    report = build_game(_req(engine="godot"), tmp_path / "out", gen,
                       progress=lambda _: None, heal_rounds=0)
    rel = {Path(p).as_posix() for p in report.scripts_written}
    assert rel == {"scripts/Main.gd", "scripts/Helper.gd"}
