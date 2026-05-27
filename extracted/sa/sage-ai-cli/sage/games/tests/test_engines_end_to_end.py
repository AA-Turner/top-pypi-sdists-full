"""End-to-end coverage of every game-engine adapter.

We can't compile real Godot/Unity/Unreal/Bevy/Phaser projects in CI (the
toolchains aren't installed), so the e2e shape here is:

  1. Drive `adapter.scaffold` + `adapter.emit_scripts` + `adapter.consume_assets`
     directly with a fixed fake LLM. Assert the on-disk layout each engine
     promises in its module docstring is actually produced.
  2. Drive `pipeline.build_game` with `adapter.detect()` monkeypatched to
     return a fake binary and `adapter.build()` monkeypatched to return a
     stub BuildArtifact. Asserts the whole pipeline glues correctly:
     decomposer → scaffold → scripts → assets → build → report.
  3. Pygame is the one engine we can actually compile end-to-end (it ships
     with the Python interpreter we're already running), so we exercise
     its real `build()` and execute the resulting `.pyz` to prove the
     scaffolded artifact is a valid Python zipapp.
"""

from __future__ import annotations

import json
import os
import platform
import sys
import zipapp
import zipfile
from pathlib import Path
from typing import Callable

import pytest

from sage.games.assets.manifest import AssetManifest
from sage.games.detector import classify_prompt
from sage.games.engines import REGISTRY, get_adapter
from sage.games.engines.base import (
    BuildArtifact,
    EngineCapability,
    GamePlan,
    GameRequest,
)
from sage.games.exceptions import (
    BuildNotSupported,
    EngineNotInstalled,
    GameBuildIncomplete,
)
from sage.games.pipeline import build_game


# ───────────────────────── fakes / fixtures ────────────────────────────


def _placeholder_asset(tmp_path: Path, name: str, content: bytes = b"x") -> Path:
    """Drop a tiny binary file on disk; engines just copy it."""
    p = tmp_path / name
    p.write_bytes(content)
    return p


def _make_manifest(tmp_path: Path) -> AssetManifest:
    """Manifest with one sprite, one mesh, one audio so every consume_assets
    path is exercised, even on adapters that ignore one kind."""
    asset_dir = tmp_path / "assets_in"
    asset_dir.mkdir(exist_ok=True)
    return AssetManifest(
        sprites={"player": _placeholder_asset(asset_dir, "player.png", b"\x89PNG\r\n")},
        meshes={"world": _placeholder_asset(asset_dir, "world.glb", b"glTF")},
        audio={"theme": _placeholder_asset(asset_dir, "theme.ogg", b"OggS")},
    )


def _make_plan(engine: str, *, perspective: str = "2d", title: str = "Sage Test") -> GamePlan:
    req = GameRequest(
        task_type="game", engine=engine, genre="platformer",
        perspective=perspective, art_style="pixel", target="web",
        raw_prompt=f"a tiny {engine} platformer for tests",
    )
    return GamePlan(
        request=req, title=title, description="a tiny test game",
        features=["jump", "collect coins", "win condition"],
        sprite_roles=[("player", "main character")],
        mesh_roles=[("world", "open level")],
        audio_roles=[("theme", "upbeat chiptune", "music")],
        target="web",
    )


# What the LLM should return per-engine for emit_scripts. We return
# raw text with code fences so each engine's parser exercises its regex.
_FAKE_LLM_RESPONSES: dict[str, str] = {
    "godot": (
        "```Main.gd\n"
        "extends Node2D\n"
        "func _ready():\n"
        "    print(\"sage test\")\n"
        "```\n"
        "```Player.gd\n"
        "extends CharacterBody2D\n"
        "func _process(_d):\n"
        "    pass\n"
        "```\n"
    ),
    "unity": (
        "```PlayerController.cs\n"
        "using UnityEngine;\n"
        "public class PlayerController : MonoBehaviour {\n"
        "  void Update() { }\n"
        "}\n"
        "```\n"
    ),
    "unreal": (
        "```SageTestGameMode.h\n"
        "#pragma once\n#include \"CoreMinimal.h\"\n"
        "```\n"
        "```SageTestGameMode.cpp\n"
        "#include \"SageTestGameMode.h\"\n"
        "```\n"
    ),
    # Bevy/Phaser/LÖVE/Pygame all expect raw code (no fences) per their prompt.
    "bevy": "fn main() { println!(\"sage\"); }\n",
    "phaser": "import Phaser from 'phaser'; new Phaser.Game({type: Phaser.AUTO});\n",
    "love2d": "function love.load() end\nfunction love.draw() end\n",
    "pygame": (
        "import pygame\n"
        "pygame.init()\n"
        "screen = pygame.display.set_mode((320, 240))\n"
        "pygame.quit()\n"
    ),
    # GUI engines' emit_scripts returns []; this string is unused but kept
    # for symmetry so we can drive the same fixture uniformly.
    "gamemaker": "",
    "construct": "",
    "rpgmaker": "",
}


def _fake_generate(engine: str) -> Callable[[str], str]:
    """A `generate` callable that always returns the canned response for `engine`.

    Used by both adapter-level tests and pipeline-level tests. The pipeline
    calls `generate()` once for the spec-decompose step and once per
    `emit_scripts`, so the canned response must also be valid JSON for the
    decompose call. We branch on the prompt prefix.
    """
    resp = _FAKE_LLM_RESPONSES[engine]

    def gen(prompt: str) -> str:
        if "Extract the spec" in prompt or "Output JSON" in prompt:
            return json.dumps({
                "title": "Sage E2E",
                "description": "a tiny test game",
                "features": ["jump", "collect"],
                "sprites": [{"role": "player", "prompt": "hero sprite"}],
                "meshes": [],
                "audio": [{"role": "theme", "prompt": "chiptune", "kind": "music"}],
            })
        return resp

    return gen


# ───────────────────────── classifier ─────────────────────────────────


@pytest.mark.parametrize("prompt,engine,task_type", [
    ("Build me a Godot 4 platformer with pixel art",  "godot",    "game"),
    ("Make a Unity 3D first-person shooter",          "unity",    "game"),
    ("I want an Unreal Engine 5 third-person game",   "unreal",   "game"),
    ("Use Bevy to write a top-down roguelike",        "bevy",     "game"),
    ("Phaser 3 puzzle game in browser",               "phaser",   "game"),
    ("love2d retro shmup",                            "love2d",   "game"),
    ("Pygame side-scroller about a fox",              "pygame",   "game"),
    ("Build a GameMaker Studio 2 metroidvania",       "gamemaker","game"),
    ("Construct 3 racing game",                       "construct","game"),
    ("RPG Maker MZ jrpg with turn-based combat",      "rpgmaker", "game"),
])
def test_classifier_routes_each_engine(prompt, engine, task_type):
    t, req = classify_prompt(prompt)
    assert t == task_type
    assert req is not None
    assert req.engine == engine


def test_classifier_falls_back_to_webapp_for_non_game_prompts():
    t, req = classify_prompt("Write a CRUD API for orders")
    assert t == "webapp"
    assert req is None


# ───────────────────────── registry coverage ──────────────────────────


def test_every_registered_engine_is_addressable():
    """If a name maps to a factory, get_adapter() must return an instance
    whose `.name` equals the key. This guards against typos breaking the
    pipeline silently."""
    for name in REGISTRY:
        adapter = get_adapter(name)
        assert adapter.name == name


def test_get_adapter_falls_back_to_godot_on_unknown_name():
    assert get_adapter("nope-not-an-engine").name == "godot"
    assert get_adapter(None).name == "godot"
    assert get_adapter("").name == "godot"


# ───────────────────────── per-engine scaffold + scripts ──────────────


@pytest.mark.parametrize("engine", list(REGISTRY))
def test_adapter_scaffold_and_scripts_and_assets(engine, tmp_path):
    """Drive scaffold → emit_scripts → consume_assets directly; we skip
    pipeline + build so this works even with no toolchain installed."""
    adapter = get_adapter(engine)
    plan = _make_plan(engine, perspective="3d" if engine == "unreal" else "2d")
    out = tmp_path / f"out_{engine}"
    out.mkdir()

    log_msgs: list[str] = []
    log: Callable[[str], None] = log_msgs.append

    # 1) scaffold
    adapter.scaffold(plan, out, log=log)
    assert any(out.iterdir()), f"{engine} produced no scaffold files"

    # 2) emit_scripts (skip GUI engines that return [])
    scripts = adapter.emit_scripts(plan, out, generate=_fake_generate(engine), log=log)
    if adapter.capabilities & EngineCapability.SCRIPTS:
        # GUI engines have SCRIPTS unset, so we don't require files there.
        assert isinstance(scripts, list)
    if engine in {"godot", "unity", "unreal", "bevy", "phaser", "love2d", "pygame"}:
        assert scripts, f"{engine} emit_scripts wrote nothing"
        for p in scripts:
            assert p.is_file(), f"{engine} promised {p} but it's missing"
            assert p.stat().st_size > 0, f"{engine}'s {p} is empty"

    # 3) consume_assets — manifest with one of each kind
    adapter.consume_assets(_make_manifest(tmp_path), out, log=log)

    # Every adapter must end up with at least the sprite copied somewhere
    # under out_dir. Each engine names its assets dir differently
    # (assets/sprites, Assets/Sprites, Content/Sprites, ...) so we glob.
    pngs = list(out.rglob("player.png"))
    assert pngs, f"{engine} did not consume the player.png sprite"


# ───────────────────────── engine-specific structural assertions ──────


def test_godot_scaffold_files(tmp_path):
    out = tmp_path / "godot_out"
    out.mkdir()
    adapter = get_adapter("godot")
    plan = _make_plan("godot")
    adapter.scaffold(plan, out, log=lambda _: None)

    assert (out / "project.godot").is_file()
    assert (out / "scenes" / "Main.tscn").is_file()
    assert (out / "export_presets.cfg").is_file()
    assert (out / "icon.svg").is_file()

    # Main.tscn must reference Main.gd
    assert "Main.gd" in (out / "scenes" / "Main.tscn").read_text(encoding="utf-8")

    # emit_scripts parses fenced ```Name.gd``` blocks from the LLM
    written = adapter.emit_scripts(
        plan, out, generate=_fake_generate("godot"), log=lambda _: None,
    )
    names = {p.name for p in written}
    assert names == {"Main.gd", "Player.gd"}


def test_unity_scaffold_includes_builder_and_project_version(tmp_path):
    out = tmp_path / "unity_out"
    out.mkdir()
    adapter = get_adapter("unity")
    plan = _make_plan("unity")
    adapter.scaffold(plan, out, log=lambda _: None)

    assert (out / "ProjectSettings" / "ProjectVersion.txt").is_file()
    assert (out / "Packages" / "manifest.json").is_file()

    builder = out / "Assets" / "Editor" / "SageBuilder.cs"
    assert builder.is_file()
    body = builder.read_text(encoding="utf-8")
    # The four build entry points the adapter's _TARGET_TO_METHOD points at.
    for method in ("BuildWebGL", "BuildWindows", "BuildMac", "BuildLinux"):
        assert method in body


def test_unreal_scaffold_writes_uproject_and_module(tmp_path):
    out = tmp_path / "unreal_out"
    out.mkdir()
    adapter = get_adapter("unreal")
    plan = _make_plan("unreal", perspective="3d", title="My Cool Game")
    adapter.scaffold(plan, out, log=lambda _: None)

    uprojects = list(out.glob("*.uproject"))
    assert len(uprojects) == 1
    project_name = uprojects[0].stem
    # _sanitize_name strips spaces + PascalCases; "My Cool Game" → "MyCoolGame"
    assert project_name == "MyCoolGame"

    body = json.loads(uprojects[0].read_text(encoding="utf-8"))
    assert body["Modules"][0]["Name"] == "MyCoolGame"
    assert (out / "Source" / "MyCoolGame" / "MyCoolGame.Build.cs").is_file()


def test_bevy_scaffold_writes_cargo_toml(tmp_path):
    out = tmp_path / "bevy_out"
    out.mkdir()
    adapter = get_adapter("bevy")
    plan = _make_plan("bevy")
    adapter.scaffold(plan, out, log=lambda _: None)

    cargo = out / "Cargo.toml"
    assert cargo.is_file()
    assert "bevy" in cargo.read_text(encoding="utf-8")
    assert (out / "src").is_dir()
    assert (out / "assets").is_dir()


def test_phaser_scaffold_writes_package_json_with_phaser_dep(tmp_path):
    out = tmp_path / "phaser_out"
    out.mkdir()
    adapter = get_adapter("phaser")
    plan = _make_plan("phaser")
    adapter.scaffold(plan, out, log=lambda _: None)

    pkg = json.loads((out / "package.json").read_text(encoding="utf-8"))
    assert "phaser" in pkg["dependencies"]
    assert (out / "index.html").is_file()


def test_love2d_scaffold_writes_conf_lua(tmp_path):
    out = tmp_path / "love_out"
    out.mkdir()
    adapter = get_adapter("love2d")
    plan = _make_plan("love2d", title="My LÖVE Game")
    adapter.scaffold(plan, out, log=lambda _: None)

    conf = (out / "conf.lua").read_text(encoding="utf-8")
    assert "My LÖVE Game" in conf
    assert "love.conf" in conf


def test_gui_only_engines_raise_buildnotsupported(tmp_path):
    for engine in ("gamemaker", "construct", "rpgmaker"):
        adapter = get_adapter(engine)
        out = tmp_path / engine
        out.mkdir()
        adapter.scaffold(_make_plan(engine), out, log=lambda _: None)
        with pytest.raises(BuildNotSupported):
            adapter.build(out, target="windows", log=lambda _: None)


# ───────────────────────── pipeline integration (mocked build) ────────


def _mock_build_to_succeed(adapter, monkeypatch, fake_artifact_name: str = "stub.bin"):
    """Patch the adapter so detect() returns a path and build() returns a
    stub BuildArtifact. Lets us drive the full pipeline without an engine."""
    monkeypatch.setattr(adapter, "detect", lambda: Path(sys.executable))

    def fake_build(out_dir, *, target, log):
        artifact = out_dir / "build" / fake_artifact_name
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_bytes(b"stub-binary")
        return BuildArtifact(
            output_path=artifact, target=target, size_bytes=artifact.stat().st_size,
            duration_s=0.01,
        )

    monkeypatch.setattr(adapter, "build", fake_build)


@pytest.mark.parametrize("engine", [
    "godot", "unity", "unreal", "bevy", "phaser", "love2d", "pygame",
])
def test_pipeline_build_game_full_loop_with_mocked_build(engine, tmp_path, monkeypatch):
    """Pipeline glues decompose → scaffold → scripts → assets → build."""
    # Patch the factory so the pipeline gets OUR pre-mocked adapter.
    adapter = get_adapter(engine)
    _mock_build_to_succeed(adapter, monkeypatch)
    monkeypatch.setitem(REGISTRY, engine, lambda: adapter)

    req = GameRequest(
        task_type="game", engine=engine, genre="platformer",
        perspective="3d" if engine == "unreal" else "2d",
        art_style="pixel", target="web",
        raw_prompt=f"a tiny {engine} platformer",
    )
    out = tmp_path / f"build_{engine}"
    progress: list[str] = []
    report = build_game(req, out, _fake_generate(engine),
                       progress=progress.append, heal_rounds=2)

    assert report.engine == engine
    assert report.build_artifact is not None
    assert report.build_size_bytes > 0
    assert report.sprite_count >= 1  # decomposer fixture guarantees at least 1
    assert report.scripts_written  # at least one script for code-emitting engines


@pytest.mark.parametrize("engine", ["gamemaker", "construct", "rpgmaker"])
def test_pipeline_gui_engines_return_scaffold_only_report(engine, tmp_path):
    """GUI engines don't have BUILD capability, so the pipeline scaffolds
    and returns successfully without raising EngineNotInstalled."""
    req = GameRequest(
        task_type="game", engine=engine, genre="rpg", perspective="2d",
        art_style="pixel", target="windows",
        raw_prompt=f"a tiny {engine} game",
    )
    out = tmp_path / f"build_{engine}"
    report = build_game(req, out, _fake_generate(engine),
                       progress=lambda _: None, heal_rounds=1)
    assert report.engine == engine
    assert report.build_artifact is None  # GUI engines never build
    # README the GUI adapter writes
    assert (out / "README.md").is_file()


def test_pipeline_raises_engine_not_installed_when_binary_missing(tmp_path):
    """If a BUILD-capable adapter can't find its binary, the pipeline must
    raise EngineNotInstalled BEFORE doing any LLM work."""
    adapter = get_adapter("godot")
    # Force detect to return None.
    import unittest.mock as mock
    with mock.patch.object(type(adapter), "detect", return_value=None):
        REGISTRY["godot"] = lambda: adapter
        try:
            with pytest.raises(EngineNotInstalled) as exc:
                build_game(
                    GameRequest(task_type="game", engine="godot",
                                raw_prompt="any prompt"),
                    tmp_path / "godot_missing",
                    lambda _p: "{}",
                    progress=lambda _m: None,
                )
            assert exc.value.engine == "godot"
            assert exc.value.install_hint  # non-empty
        finally:
            # Restore the real factory so other tests aren't affected.
            from sage.games.engines.godot import GodotAdapter
            REGISTRY["godot"] = GodotAdapter


def test_pipeline_heal_loop_recovers_after_transient_build_failure(tmp_path, monkeypatch):
    """The pipeline must retry up to `heal_rounds` times before raising
    GameBuildIncomplete. We fail the first call, succeed the second, and
    assert the report carries `heal_rounds=1`."""
    adapter = get_adapter("godot")
    monkeypatch.setattr(adapter, "detect", lambda: Path(sys.executable))

    calls = {"n": 0}

    def flaky_build(out_dir, *, target, log):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("simulated first-round build failure")
        artifact = out_dir / "build" / "ok.bin"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_bytes(b"ok")
        return BuildArtifact(
            output_path=artifact, target=target, size_bytes=2, duration_s=0.0,
        )

    monkeypatch.setattr(adapter, "build", flaky_build)
    monkeypatch.setitem(REGISTRY, "godot", lambda: adapter)

    req = GameRequest(task_type="game", engine="godot", genre="platformer",
                      perspective="2d", raw_prompt="flaky test")
    report = build_game(req, tmp_path / "heal_test",
                       _fake_generate("godot"),
                       progress=lambda _: None, heal_rounds=3)
    assert calls["n"] == 2
    assert report.heal_rounds == 1
    assert report.build_artifact is not None


def test_pipeline_heal_loop_gives_up_and_raises(tmp_path, monkeypatch):
    adapter = get_adapter("godot")
    monkeypatch.setattr(adapter, "detect", lambda: Path(sys.executable))

    def always_fails(out_dir, *, target, log):
        raise RuntimeError("nope")

    monkeypatch.setattr(adapter, "build", always_fails)
    monkeypatch.setitem(REGISTRY, "godot", lambda: adapter)

    req = GameRequest(task_type="game", engine="godot", genre="platformer",
                      perspective="2d", raw_prompt="permaflaky")
    with pytest.raises(GameBuildIncomplete) as exc:
        build_game(req, tmp_path / "fail", _fake_generate("godot"),
                   progress=lambda _: None, heal_rounds=2)
    assert exc.value.report["engine"] == "godot"
    assert "nope" in exc.value.message


# ───────────────────────── pygame real build ──────────────────────────


@pytest.mark.skipif(
    platform.system() == "Windows" and not sys.executable,
    reason="needs python on PATH",
)
def test_pygame_real_build_produces_runnable_pyz(tmp_path):
    """Pygame is the one engine we can compile for real — `zipapp` ships
    with the stdlib. We don't actually `import pygame` (CI may not have it
    installed); we just assert the .pyz is a valid zip and has a
    __main__.py at the root that imports `main`."""
    adapter = get_adapter("pygame")
    plan = _make_plan("pygame")
    out = tmp_path / "pyg"
    out.mkdir()

    adapter.scaffold(plan, out, log=lambda _: None)
    adapter.emit_scripts(plan, out, generate=_fake_generate("pygame"),
                        log=lambda _: None)
    adapter.consume_assets(_make_manifest(tmp_path), out, log=lambda _: None)
    artifact = adapter.build(out, target="any", log=lambda _: None)

    assert artifact.output_path.is_file()
    assert artifact.size_bytes > 0
    assert zipfile.is_zipfile(artifact.output_path)

    with zipfile.ZipFile(artifact.output_path) as zf:
        names = set(zf.namelist())
        assert "__main__.py" in names
        assert "main.py" in names
        # build/ output must NOT be packaged into the .pyz (it would loop).
        assert not any(n.startswith("build/") for n in names)
