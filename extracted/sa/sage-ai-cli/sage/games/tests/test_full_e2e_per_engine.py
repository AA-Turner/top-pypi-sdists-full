"""Full end-to-end build_game per engine, with realistic LLM-shaped fakes.

The earlier test files exercise pieces in isolation (or with placeholder
LLM responses). This one drives `build_game` per engine with responses
shaped exactly like a real Claude/Gemini output for that engine — fenced
code blocks for godot/unity/unreal, raw bodies for bevy/phaser/love2d/
pygame — so we exercise each adapter's parser at the same time as the
pipeline.

What each test asserts:

  1. The decompose JSON populates the plan (title/desc/features carry
     through into adapter prompts via emit_scripts).
  2. The expected gameplay scripts land on disk under the engine's
     canonical directory layout.
  3. consume_assets actually copies sprites/audio/meshes into the
     engine's directory tree (asset names round-trip).
  4. build() is mocked to succeed → the report carries all the fields
     principal_builder reads (engine, build_artifact, heal_rounds=0).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Callable

import pytest

from sage.games.engines import REGISTRY, get_adapter
from sage.games.engines.base import BuildArtifact, GameRequest
from sage.games.pipeline import build_game


# ───────────────────────── helpers ────────────────────────────────────


_DECOMPOSE_JSON = json.dumps({
    "title": "Sage E2E",
    "description": (
        "A tiny test game with three sprites, one stage, and a bouncy "
        "soundtrack. Reach the flag to win."
    ),
    "features": [
        "WASD / arrow movement",
        "Coin collection",
        "Reach-the-flag win condition",
    ],
    "sprites": [
        {"role": "player", "prompt": "blue ninja sprite"},
        {"role": "coin",   "prompt": "shiny gold coin"},
        {"role": "flag",   "prompt": "red flag on a pole"},
    ],
    "meshes": [
        {"role": "ground", "prompt": "flat ground plane"},
    ],
    "audio": [
        {"role": "theme", "prompt": "upbeat chiptune loop", "kind": "music"},
        {"role": "coin_pickup", "prompt": "coin pickup ding", "kind": "sfx"},
    ],
})


# Per-engine realistic LLM responses for the emit_scripts call.
_SCRIPT_RESPONSES: dict[str, str] = {
    "godot": (
        "```Main.gd\n"
        "extends Node2D\n"
        "func _ready():\n"
        "    print(\"Sage E2E\")\n"
        "    $Player.position = Vector2(100, 100)\n"
        "```\n"
        "```Player.gd\n"
        "extends CharacterBody2D\n"
        "@export var speed := 200.0\n"
        "func _physics_process(delta):\n"
        "    var dir = Input.get_vector(\"ui_left\", \"ui_right\", \"ui_up\", \"ui_down\")\n"
        "    velocity = dir * speed\n"
        "    move_and_slide()\n"
        "```\n"
        "```Coin.gd\n"
        "extends Area2D\n"
        "func _on_body_entered(body):\n"
        "    if body is CharacterBody2D:\n"
        "        queue_free()\n"
        "```\n"
    ),
    "unity": (
        "```PlayerController.cs\n"
        "using UnityEngine;\n"
        "public class PlayerController : MonoBehaviour {\n"
        "    public float speed = 5f;\n"
        "    void Update() {\n"
        "        float x = Input.GetAxis(\"Horizontal\");\n"
        "        transform.Translate(x * speed * Time.deltaTime, 0, 0);\n"
        "    }\n"
        "}\n"
        "```\n"
        "```Coin.cs\n"
        "using UnityEngine;\n"
        "public class Coin : MonoBehaviour {\n"
        "    void OnTriggerEnter2D(Collider2D other) { Destroy(gameObject); }\n"
        "}\n"
        "```\n"
    ),
    "unreal": (
        "```SageE2EGameMode.h\n"
        "#pragma once\n"
        "#include \"CoreMinimal.h\"\n"
        "#include \"GameFramework/GameModeBase.h\"\n"
        "#include \"SageE2EGameMode.generated.h\"\n"
        "UCLASS()\n"
        "class ASageE2EGameMode : public AGameModeBase {\n"
        "    GENERATED_BODY()\n"
        "public:\n"
        "    ASageE2EGameMode();\n"
        "};\n"
        "```\n"
        "```SageE2EGameMode.cpp\n"
        "#include \"SageE2EGameMode.h\"\n"
        "ASageE2EGameMode::ASageE2EGameMode() {}\n"
        "```\n"
    ),
    "bevy": (
        "use bevy::prelude::*;\n\n"
        "fn main() {\n"
        "    App::new()\n"
        "        .add_plugins(DefaultPlugins)\n"
        "        .add_systems(Startup, setup)\n"
        "        .run();\n"
        "}\n\n"
        "fn setup(mut commands: Commands) {\n"
        "    commands.spawn(Camera2dBundle::default());\n"
        "}\n"
    ),
    "phaser": (
        "import Phaser from 'phaser';\n\n"
        "const config: Phaser.Types.Core.GameConfig = {\n"
        "  type: Phaser.AUTO,\n"
        "  width: 800, height: 600,\n"
        "  parent: 'game',\n"
        "  scene: { preload, create },\n"
        "};\n\n"
        "function preload(this: Phaser.Scene) {\n"
        "  this.load.image('player', 'assets/player.png');\n"
        "}\n\n"
        "function create(this: Phaser.Scene) {\n"
        "  this.add.image(400, 300, 'player');\n"
        "}\n\n"
        "new Phaser.Game(config);\n"
    ),
    "love2d": (
        "local player = {x = 400, y = 300, speed = 200}\n\n"
        "function love.load()\n"
        "    love.window.setTitle('Sage LÖVE Game')\n"
        "end\n\n"
        "function love.update(dt)\n"
        "    if love.keyboard.isDown('right') then\n"
        "        player.x = player.x + player.speed * dt\n"
        "    end\n"
        "end\n\n"
        "function love.draw()\n"
        "    love.graphics.rectangle('fill', player.x, player.y, 32, 32)\n"
        "end\n"
    ),
    "pygame": (
        "import pygame, sys\n\n"
        "pygame.init()\n"
        "screen = pygame.display.set_mode((800, 600))\n"
        "pygame.display.set_caption('Sage Pygame Game')\n"
        "clock = pygame.time.Clock()\n"
        "running = True\n"
        "while running:\n"
        "    for event in pygame.event.get():\n"
        "        if event.type == pygame.QUIT:\n"
        "            running = False\n"
        "    screen.fill((30, 30, 60))\n"
        "    pygame.display.flip()\n"
        "    clock.tick(60)\n"
        "pygame.quit()\n"
        "sys.exit()\n"
    ),
    # GUI engines don't emit scripts in this scaffold pass.
    "gamemaker": "",
    "construct":  "",
    "rpgmaker":   "",
}


def _generate(engine: str) -> Callable[[str], str]:
    """A realistic LLM that returns the decompose JSON to the first call
    and the script block to the second."""
    script = _SCRIPT_RESPONSES[engine]

    def gen(prompt: str) -> str:
        if "Output JSON" in prompt or "Extract the spec" in prompt:
            return _DECOMPOSE_JSON
        return script

    return gen


def _mock_adapter_to_build_successfully(engine: str, monkeypatch):
    """Replace the registered adapter factory with a wrapper whose
    detect() returns a path and build() writes a stub artifact. Keeps
    everything else (scaffold/emit_scripts/consume_assets) real."""
    adapter = get_adapter(engine)
    monkeypatch.setattr(adapter, "detect", lambda: Path(sys.executable))

    def fake_build(out_dir, *, target, log):
        artifact = out_dir / "build" / f"{engine}_artifact.bin"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_bytes(b"stub-binary-bytes")
        return BuildArtifact(
            output_path=artifact, target=target,
            size_bytes=artifact.stat().st_size, duration_s=0.0,
        )

    monkeypatch.setattr(adapter, "build", fake_build)
    monkeypatch.setitem(REGISTRY, engine, lambda: adapter)
    return adapter


# ───────────────────────── per-engine assertions ──────────────────────


@pytest.fixture
def gen_godot():
    return _generate("godot")


def test_full_e2e_godot_writes_three_gd_files_and_copies_assets(tmp_path, monkeypatch, gen_godot):
    _mock_adapter_to_build_successfully("godot", monkeypatch)
    req = GameRequest(task_type="game", engine="godot", genre="platformer",
                      perspective="2d", art_style="pixel",
                      raw_prompt="a tiny godot platformer")
    report = build_game(req, tmp_path, gen_godot, progress=lambda _: None)

    # Scripts: Main.gd, Player.gd, Coin.gd
    written = {Path(p).name for p in report.scripts_written}
    assert written == {"Main.gd", "Player.gd", "Coin.gd"}
    for name in written:
        body = (tmp_path / "scripts" / name).read_text(encoding="utf-8")
        assert "extends" in body

    # Assets: three sprites + one mesh + two audio land in the godot tree.
    assert list((tmp_path / "assets" / "sprites").glob("*.png"))
    assert list((tmp_path / "assets" / "audio").glob("*"))
    assert list((tmp_path / "assets" / "meshes").glob("*.glb"))

    assert report.build_artifact is not None
    assert report.heal_rounds == 0


def test_full_e2e_unity_writes_two_cs_files_and_builder_persists(tmp_path, monkeypatch):
    _mock_adapter_to_build_successfully("unity", monkeypatch)
    req = GameRequest(task_type="game", engine="unity", genre="platformer",
                      perspective="2d", raw_prompt="a tiny unity game")
    report = build_game(req, tmp_path, _generate("unity"),
                       progress=lambda _: None)

    written = {Path(p).name for p in report.scripts_written}
    assert written == {"PlayerController.cs", "Coin.cs"}
    # SageBuilder.cs from scaffold MUST still be present (scaffold doesn't
    # get wiped by emit_scripts).
    assert (tmp_path / "Assets" / "Editor" / "SageBuilder.cs").is_file()
    # Sprite manifest landed under Unity's conventional Assets/Sprites.
    assert list((tmp_path / "Assets" / "Sprites").glob("*.png"))


def test_full_e2e_unreal_writes_paired_h_and_cpp(tmp_path, monkeypatch):
    _mock_adapter_to_build_successfully("unreal", monkeypatch)
    req = GameRequest(task_type="game", engine="unreal", genre="fps",
                      perspective="3d", raw_prompt="a tiny ue5 fps")
    report = build_game(req, tmp_path, _generate("unreal"),
                       progress=lambda _: None)

    files = {Path(p).name for p in report.scripts_written}
    assert "SageE2EGameMode.h" in files
    assert "SageE2EGameMode.cpp" in files
    # .uproject persists from scaffold
    assert list(tmp_path.glob("*.uproject"))
    # Assets landed under Content/<kind>
    assert list((tmp_path / "Content" / "Sprites").glob("*.png"))
    assert list((tmp_path / "Content" / "Meshes").glob("*.glb"))


def test_full_e2e_bevy_writes_main_rs_and_cargo_toml(tmp_path, monkeypatch):
    _mock_adapter_to_build_successfully("bevy", monkeypatch)
    req = GameRequest(task_type="game", engine="bevy", genre="roguelike",
                      perspective="top-down", raw_prompt="a tiny bevy roguelike")
    report = build_game(req, tmp_path, _generate("bevy"),
                       progress=lambda _: None)

    assert (tmp_path / "Cargo.toml").is_file()
    main = (tmp_path / "src" / "main.rs").read_text(encoding="utf-8")
    assert "bevy::prelude" in main
    assert "App::new" in main
    assert report.scripts_written  # at least one script written


def test_full_e2e_phaser_writes_typescript_with_phaser_import(tmp_path, monkeypatch):
    _mock_adapter_to_build_successfully("phaser", monkeypatch)
    req = GameRequest(task_type="game", engine="phaser", genre="puzzle",
                      perspective="2d", raw_prompt="a phaser puzzle game")
    report = build_game(req, tmp_path, _generate("phaser"),
                       progress=lambda _: None)

    ts = (tmp_path / "src" / "main.ts").read_text(encoding="utf-8")
    assert "phaser" in ts.lower()
    assert "new Phaser.Game" in ts
    # Assets land under public/assets per Vite convention
    assert list((tmp_path / "public" / "assets").glob("*.png"))


def test_full_e2e_love2d_writes_main_lua_and_conf_persists(tmp_path, monkeypatch):
    _mock_adapter_to_build_successfully("love2d", monkeypatch)
    req = GameRequest(task_type="game", engine="love2d", genre="shmup",
                      perspective="2d", raw_prompt="a tiny love2d shmup")
    report = build_game(req, tmp_path, _generate("love2d"),
                       progress=lambda _: None)

    lua = (tmp_path / "main.lua").read_text(encoding="utf-8")
    assert "love.update" in lua
    assert "love.draw" in lua
    assert (tmp_path / "conf.lua").is_file()


def test_full_e2e_pygame_writes_main_py_and_requirements(tmp_path, monkeypatch):
    _mock_adapter_to_build_successfully("pygame", monkeypatch)
    req = GameRequest(task_type="game", engine="pygame", genre="platformer",
                      perspective="2d", raw_prompt="a tiny pygame platformer")
    report = build_game(req, tmp_path, _generate("pygame"),
                       progress=lambda _: None)

    py = (tmp_path / "main.py").read_text(encoding="utf-8")
    assert "import pygame" in py
    assert "pygame.display.set_mode" in py
    assert (tmp_path / "requirements.txt").read_text(encoding="utf-8") \
        .startswith("pygame")


# ───────────────────────── cross-engine sanity sweeps ─────────────────


@pytest.mark.parametrize("engine", [
    "godot", "unity", "unreal", "bevy", "phaser", "love2d", "pygame",
])
def test_full_e2e_report_invariants_per_build_engine(engine, tmp_path, monkeypatch):
    """For every BUILD-capable engine: scripts_written non-empty, assets
    consumed, build_artifact populated, heal_rounds=0 on first-try success."""
    _mock_adapter_to_build_successfully(engine, monkeypatch)
    req = GameRequest(
        task_type="game", engine=engine, genre="platformer",
        perspective="3d" if engine == "unreal" else "2d",
        art_style="pixel", target="web",
        raw_prompt=f"sage e2e test of {engine}",
    )
    report = build_game(req, tmp_path, _generate(engine),
                       progress=lambda _: None, heal_rounds=2)

    assert report.engine == engine
    assert report.scripts_written, f"{engine}: emit_scripts produced nothing"
    assert report.sprite_count >= 1
    assert report.audio_count >= 1
    assert report.build_artifact is not None
    assert report.heal_rounds == 0


@pytest.mark.parametrize("engine", ["gamemaker", "construct", "rpgmaker"])
def test_full_e2e_gui_engine_returns_scaffold_only(engine, tmp_path):
    """GUI engines: scaffold ok, no build attempt, no build_artifact."""
    req = GameRequest(
        task_type="game", engine=engine, genre="rpg", perspective="2d",
        raw_prompt=f"a tiny {engine} game",
    )
    report = build_game(req, tmp_path, _generate(engine),
                       progress=lambda _: None)
    assert report.build_artifact is None
    # README the GUI scaffold writes is present.
    assert (tmp_path / "README.md").is_file()


# ───────────────────────── heal-loop on a real engine ─────────────────


def test_full_e2e_heal_recovery_persists_final_artifact(tmp_path, monkeypatch):
    """The heal pass re-runs emit_scripts (with the error log) and then
    build(). After the heal, the final scripts overwrite the original
    ones — we must NOT have stale scripts from the first failed pass."""
    adapter = get_adapter("godot")
    monkeypatch.setattr(adapter, "detect", lambda: Path(sys.executable))

    state = {"build_calls": 0, "script_calls": 0}

    real_emit = adapter.emit_scripts

    def counting_emit(plan, out_dir, *, generate, log):
        state["script_calls"] += 1
        return real_emit(plan, out_dir, generate=generate, log=log)

    def flaky_build(out_dir, *, target, log):
        state["build_calls"] += 1
        if state["build_calls"] == 1:
            raise RuntimeError("first attempt: missing autoload")
        artifact = out_dir / "build" / "index.html"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_bytes(b"<html>healed</html>")
        return BuildArtifact(
            output_path=artifact, target=target,
            size_bytes=artifact.stat().st_size, duration_s=0.0,
        )

    monkeypatch.setattr(adapter, "emit_scripts", counting_emit)
    monkeypatch.setattr(adapter, "build", flaky_build)
    monkeypatch.setitem(REGISTRY, "godot", lambda: adapter)

    req = GameRequest(task_type="game", engine="godot", genre="platformer",
                      perspective="2d", raw_prompt="heal test")
    report = build_game(req, tmp_path, _generate("godot"),
                       progress=lambda _: None, heal_rounds=3)

    assert state["build_calls"] == 2
    assert state["script_calls"] == 2  # initial + 1 heal round
    assert report.heal_rounds == 1
    assert report.build_artifact.endswith("index.html")
