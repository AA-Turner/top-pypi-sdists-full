"""Per-platform build-invocation coverage for godot/unity/unreal.

We can't install three engines in CI just to verify a target string is
correct, so these tests intercept `subprocess.run` and assert the args
each adapter passes to its engine binary. If sage maps `target='mac'`
to the wrong Godot preset, this catches it without anyone needing a Mac.

What's covered per engine:

  Godot   → --export-release <preset> <out_path> with the right preset
            and the right output extension (.html / .exe / .app / .x86_64)
  Unity   → -executeMethod SageBuilder.Build<Target> for each platform
  Unreal  → -platform=<Win64|Mac|Linux|Android|IOS>; -web- raises
            BuildNotSupported up front (UE5 dropped HTML5)

Bevy/Phaser/LÖVE/Pygame don't take a platform — they produce one
artifact format regardless. They're covered by the existing e2e tests.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable

import pytest

from sage.games.engines import REGISTRY, get_adapter
from sage.games.engines.base import (
    BuildArtifact,
    GamePlan,
    GameRequest,
)
from sage.games.exceptions import BuildNotSupported, EngineNotInstalled
from sage.games.pipeline import build_game


@pytest.fixture(autouse=True)
def _force_offline_assets(monkeypatch):
    """These tests assert build-time subprocess invocations. The asset
    generator ALSO uses subprocess (ffmpeg for music/sfx) — if we let it
    run on a machine that has ffmpeg, the build-spy will intercept those
    calls too and the .ogg file ffmpeg would have written won't exist
    when the engine adapter tries to copy it. Forcing the audio fallback
    to write a silent file directly (no subprocess) keeps the test
    focused on what we actually care about: engine-binary invocations."""
    monkeypatch.setenv("SAGE_TESTING", "0")
    monkeypatch.setattr("sage.games.assets.audio._ffmpeg_available", lambda: False)
    monkeypatch.delenv("REPLICATE_API_TOKEN", raising=False)
    # Same logic for meshes — Blender shells out; mesh.placeholder is fine.
    monkeypatch.setattr("sage.games.assets.meshes._find_blender", lambda: None)


# ───────────────────────── intercept helpers ──────────────────────────


class _SubprocessSpy:
    """Records every `subprocess.run` call and replies with a stub that
    looks like a successful build. Each engine's `build()` reads
    `returncode` + checks that an artifact file exists; we satisfy both."""

    def __init__(self, write_artifact_at: Callable[[Path, list[str]], Path] | None = None):
        self.calls: list[list[str]] = []
        self.write_artifact_at = write_artifact_at

    def __call__(self, args, **kwargs):
        # Normalise the args list (subprocess accepts str or list).
        if isinstance(args, str):
            args_list = [args]
        else:
            args_list = list(args)
        self.calls.append(args_list)

        # If the caller specified `cwd`, we resolve artifact paths relative
        # to it (some adapters cd into out_dir before invoking the engine).
        cwd = Path(kwargs.get("cwd") or ".")

        # Each engine writes its artifact to a specific spot; the test
        # injects a callback that mimics this so adapter.build()'s
        # post-conditions pass.
        if self.write_artifact_at is not None:
            self.write_artifact_at(cwd, args_list)

        # Fake CompletedProcess. Engines check `.returncode` and read
        # `.stdout` / `.stderr` for log inspection on failure.
        class _Proc:
            returncode = 0
            stdout = ""
            stderr = ""
        return _Proc()


def _make_request(engine: str, target: str) -> GameRequest:
    return GameRequest(
        task_type="game", engine=engine, genre="platformer",
        perspective="3d" if engine == "unreal" else "2d",
        art_style="pixel", target=target,
        raw_prompt=f"a tiny {engine} {target} game",
    )


def _fake_generate(prompt: str) -> str:
    if "Output JSON" in prompt or "Extract the spec" in prompt:
        return (
            '{"title":"X","description":"x","features":["f"],'
            '"sprites":[{"role":"player","prompt":"p"}],'
            '"meshes":[],"audio":[{"role":"theme","prompt":"t","kind":"music"}]}'
        )
    # godot wants ```Main.gd``` fences; unity wants ```PlayerController.cs```;
    # unreal wants ```<Name>.h``` / `.cpp`. Provide ALL three so one fixture
    # serves every engine.
    return (
        "```Main.gd\nextends Node2D\nfunc _ready(): pass\n```\n"
        "```PlayerController.cs\nusing UnityEngine; public class PlayerController : MonoBehaviour {}\n```\n"
        "```XGameMode.h\n#pragma once\n```\n"
        "```XGameMode.cpp\n#include \"XGameMode.h\"\n```\n"
    )


# ───────────────────────── Godot per-platform ─────────────────────────


@pytest.mark.parametrize("target,preset,ext", [
    ("web",     "Web",             "html"),
    ("windows", "Windows Desktop", "exe"),
    ("mac",     "macOS",           "zip"),
    ("linux",   "Linux",           "x86_64"),
])
def test_godot_build_uses_correct_preset_and_extension(target, preset, ext, tmp_path, monkeypatch):
    """The Godot adapter exposes 4 export presets. The pipeline's `target`
    must map 1:1 to the right preset string and the right output extension
    (.html for web, .exe for windows, etc.)."""
    adapter = get_adapter("godot")
    fake_godot = tmp_path / "fake-godot"
    fake_godot.write_text("#!/bin/sh\n")
    monkeypatch.setattr(adapter, "detect", lambda: fake_godot)
    # Skip the export-template download by pretending templates exist.
    monkeypatch.setattr(
        "sage.games.engines.godot._ensure_export_templates", lambda *a, **k: None,
    )

    spy = _SubprocessSpy(
        write_artifact_at=lambda cwd, args: _write_godot_artifact(cwd, args),
    )
    monkeypatch.setattr("sage.games.engines.godot.subprocess.run", spy)
    monkeypatch.setitem(REGISTRY, "godot", lambda: adapter)

    report = build_game(_make_request("godot", target), tmp_path / "out",
                       _fake_generate, progress=lambda _: None, heal_rounds=0)

    # First call is `--import`, second is `--export-release`.
    export_call = next(
        (c for c in spy.calls if "--export-release" in c), None,
    )
    assert export_call is not None, "godot never invoked --export-release"
    assert preset in export_call, f"expected preset {preset!r} in {export_call}"

    assert report.build_artifact is not None
    artifact_name = Path(report.build_artifact).name
    if target == "web":
        # Web artifacts are emitted as index.html
        assert artifact_name == "index.html"
    else:
        assert artifact_name == f"game.{ext}"


def _write_godot_artifact(cwd: Path, args: list[str]) -> None:
    """Drop a placeholder file at the path Godot's export-release would write to."""
    if "--export-release" not in args:
        return
    # adapter passes the output path as the last positional arg.
    out_path = Path(args[-1])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(b"<stub-godot-build>")


# ───────────────────────── Unity per-platform ─────────────────────────


@pytest.mark.parametrize("target,method", [
    ("web",     "SageBuilder.BuildWebGL"),
    ("windows", "SageBuilder.BuildWindows"),
    ("mac",     "SageBuilder.BuildMac"),
    ("linux",   "SageBuilder.BuildLinux"),
])
def test_unity_build_invokes_correct_executemethod(target, method, tmp_path, monkeypatch):
    """Unity batchmode calls one of four C# entry points in SageBuilder.cs.
    Every target must invoke the right method — a typo here means the
    build silently picks the default target instead."""
    adapter = get_adapter("unity")
    fake_unity = tmp_path / "fake-Unity.exe"
    fake_unity.write_text("#!/bin/sh\n")
    monkeypatch.setattr(adapter, "detect", lambda: fake_unity)

    _TARGET_TO_BUILDTARGET = {
        "web": "WebGL",
        "windows": "StandaloneWindows64",
        "mac": "StandaloneOSX",
        "linux": "StandaloneLinux64",
        "android": "Android",
        "ios": "iOS",
    }

    def write_unity_build(cwd, args):
        project_path = cwd
        for i, a in enumerate(args):
            if a == "-projectPath" and i + 1 < len(args):
                project_path = Path(args[i + 1])
                break
        build_subdir = project_path / "Build" / _TARGET_TO_BUILDTARGET[target]
        build_subdir.mkdir(parents=True, exist_ok=True)
        preferred_name = {
            "web": "index.html",
            "windows": "game.exe",
            "mac": "game.app",
            "linux": "game.x86_64",
            "android": "game.apk",
            "ios": "Unity-iPhone.xcodeproj",
        }[target]
        output = build_subdir / preferred_name
        if target in ("mac", "ios"):
            output.mkdir(parents=True, exist_ok=True)
            (output / "dummy_file").write_text("dummy", encoding="utf-8")
        else:
            output.write_text("dummy", encoding="utf-8")

    spy = _SubprocessSpy(write_artifact_at=write_unity_build)
    monkeypatch.setattr("sage.games.engines.unity.subprocess.run", spy)
    monkeypatch.setitem(REGISTRY, "unity", lambda: adapter)

    build_game(_make_request("unity", target), tmp_path / "out",
              _fake_generate, progress=lambda _: None, heal_rounds=0)

    call = spy.calls[0]
    assert "-batchmode" in call
    assert "-projectPath" in call
    assert "-executeMethod" in call
    method_idx = call.index("-executeMethod")
    assert call[method_idx + 1] == method


# ───────────────────────── Unreal per-platform ────────────────────────


@pytest.mark.parametrize("target,platform_arg", [
    ("windows", "Win64"),
    ("mac",     "Mac"),
    ("linux",   "Linux"),
    ("android", "Android"),
    ("ios",     "IOS"),
])
def test_unreal_uat_uses_correct_platform_arg(target, platform_arg, tmp_path, monkeypatch):
    """Unreal's UAT BuildCookRun takes `-platform=<...>`. We assert the
    mapping per target — wrong platform string fails 30 minutes into the
    cook with a generic UAT error, so catching it here saves real users
    half an hour."""
    adapter = get_adapter("unreal")
    fake_uat = tmp_path / "RunUAT.bat"
    fake_uat.write_text("@echo off\n")
    monkeypatch.setattr(adapter, "detect", lambda: fake_uat)

    spy = _SubprocessSpy()
    monkeypatch.setattr("sage.games.engines.unreal.subprocess.run", spy)
    monkeypatch.setitem(REGISTRY, "unreal", lambda: adapter)

    build_game(_make_request("unreal", target), tmp_path / "out",
              _fake_generate, progress=lambda _: None, heal_rounds=0)

    call = spy.calls[0]
    assert any(arg == f"-platform={platform_arg}" for arg in call), \
        f"expected -platform={platform_arg} in {call}"
    # UAT essentials — if these change, downstream automation breaks.
    assert any("BuildCookRun" in arg for arg in call)
    assert any("-clientconfig=Development" in arg for arg in call)


def test_unreal_web_target_raises_build_not_supported(tmp_path, monkeypatch):
    """UE5 dropped HTML5 in 4.24. Don't let users wait 30 min for UAT
    to fail — raise BuildNotSupported up front pointing them at Godot."""
    adapter = get_adapter("unreal")
    fake_uat = tmp_path / "RunUAT.bat"
    fake_uat.write_text("@echo off\n")
    monkeypatch.setattr(adapter, "detect", lambda: fake_uat)

    spy = _SubprocessSpy()
    monkeypatch.setattr("sage.games.engines.unreal.subprocess.run", spy)
    monkeypatch.setitem(REGISTRY, "unreal", lambda: adapter)

    # Drive the adapter directly so we get the typed exception (the
    # pipeline catches BuildNotSupported and returns the partial report).
    plan = GamePlan(
        request=_make_request("unreal", "web"),
        title="X", description="x", features=[],
        sprite_roles=[], mesh_roles=[], audio_roles=[],
        target="web",
    )
    out = tmp_path / "out"
    out.mkdir()
    adapter.scaffold(plan, out, log=lambda _: None)

    with pytest.raises(BuildNotSupported) as exc:
        adapter.build(out, target="web", log=lambda _: None)

    assert exc.value.engine == "unreal"
    assert "HTML5" in exc.value.reason or "web" in exc.value.reason.lower()
    # Critical: UAT must NOT have been invoked. Cold cooks are 30 min.
    assert spy.calls == []


def test_pipeline_unreal_web_returns_partial_report_without_running_uat(tmp_path, monkeypatch):
    """When the pipeline catches BuildNotSupported it returns the partial
    report. Users still get the scaffold, just not a binary."""
    adapter = get_adapter("unreal")
    fake_uat = tmp_path / "RunUAT.bat"
    fake_uat.write_text("@echo off\n")
    monkeypatch.setattr(adapter, "detect", lambda: fake_uat)
    spy = _SubprocessSpy()
    monkeypatch.setattr("sage.games.engines.unreal.subprocess.run", spy)
    monkeypatch.setitem(REGISTRY, "unreal", lambda: adapter)

    report = build_game(_make_request("unreal", "web"), tmp_path / "out",
                       _fake_generate, progress=lambda _: None,
                       heal_rounds=2)
    # Pipeline returns the partial report on BuildNotSupported.
    assert report.engine == "unreal"
    assert report.build_artifact is None
    assert spy.calls == []
    # But scaffolding DID happen — uproject file is present.
    assert list((tmp_path / "out").glob("*.uproject"))


# ───────────────────────── target → output path ───────────────────────


def test_godot_web_target_emits_index_html(tmp_path, monkeypatch):
    """Web targets MUST land at build/index.html so static-site serving
    works without an extra rename step. This is the de-facto contract
    every web embed (itch.io, Steam, GitHub Pages) expects."""
    adapter = get_adapter("godot")
    fake = tmp_path / "fake-godot"
    fake.write_text("#!/bin/sh\n")
    monkeypatch.setattr(adapter, "detect", lambda: fake)
    monkeypatch.setattr(
        "sage.games.engines.godot._ensure_export_templates", lambda *a, **k: None,
    )

    spy = _SubprocessSpy(
        write_artifact_at=lambda cwd, args: _write_godot_artifact(cwd, args),
    )
    monkeypatch.setattr("sage.games.engines.godot.subprocess.run", spy)
    monkeypatch.setitem(REGISTRY, "godot", lambda: adapter)

    report = build_game(
        _make_request("godot", "web"), tmp_path / "out",
        _fake_generate, progress=lambda _: None, heal_rounds=0,
    )
    assert Path(report.build_artifact).name == "index.html"
    assert Path(report.build_artifact).parent.name == "build"
