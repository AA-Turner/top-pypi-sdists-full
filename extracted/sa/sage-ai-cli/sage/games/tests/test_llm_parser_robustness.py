"""LLM-output parsing robustness for emit_scripts.

LLMs in production return messy output: prose preambles, apology paragraphs,
language tags on the fence, mid-response policy disclaimers, embedded
backticks inside code. The script parsers in each engine adapter run on
*every* build, so we need them to:

  * extract whatever IS parseable from a messy response,
  * fall back to a placeholder file when nothing parses (so the project
    still opens in the editor),
  * not error on empty / None responses.

These tests drive each engine's emit_scripts() directly with synthetic
"hostile" LLM responses and assert the surviving output.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from sage.games.engines import get_adapter
from sage.games.engines.base import GamePlan, GameRequest


# ───────────────────────── helpers ────────────────────────────────────


def _plan(perspective: str = "2d") -> GamePlan:
    req = GameRequest(
        task_type="game", engine="godot", genre="platformer",
        perspective=perspective, raw_prompt="x",
    )
    return GamePlan(
        request=req, title="Parser Test", description="x",
        features=[], sprite_roles=[], mesh_roles=[], audio_roles=[],
        target="web",
    )


# ───────────────────────── Godot parser ───────────────────────────────


def test_godot_parser_extracts_blocks_from_prose_response(tmp_path):
    adapter = get_adapter("godot")
    adapter.scaffold(_plan(), tmp_path, log=lambda _: None)

    raw = (
        "Sure! Here's a Godot platformer. Let me know if you want anything tweaked.\n\n"
        "```Main.gd\n"
        "extends Node2D\n"
        "func _ready(): print(\"ok\")\n"
        "```\n\n"
        "And the player controller:\n\n"
        "```Player.gd\n"
        "extends CharacterBody2D\n"
        "var speed := 200\n"
        "```\n\n"
        "Hope that helps!\n"
    )
    written = adapter.emit_scripts(_plan(), tmp_path, generate=lambda _: raw,
                                    log=lambda _: None)
    names = {p.name for p in written}
    assert names == {"Main.gd", "Player.gd"}


def test_godot_parser_raises_when_no_blocks_present(tmp_path):
    adapter = get_adapter("godot")
    adapter.scaffold(_plan(), tmp_path, log=lambda _: None)

    raw = "I can't help with that. Sorry."
    with pytest.raises(RuntimeError, match="godot: LLM response had no parseable"):
        adapter.emit_scripts(_plan(), tmp_path, generate=lambda _: raw,
                            log=lambda _: None)


def test_godot_parser_raises_on_empty_response(tmp_path):
    adapter = get_adapter("godot")
    adapter.scaffold(_plan(), tmp_path, log=lambda _: None)
    with pytest.raises(RuntimeError, match="godot: LLM response had no parseable"):
        adapter.emit_scripts(_plan(), tmp_path, generate=lambda _: "",
                            log=lambda _: None)


def test_godot_parser_accepts_extra_files_beyond_requested(tmp_path):
    """If the LLM helpfully writes Enemy.gd / Boss.gd / Pickup.gd in
    addition to Main + Player, sage should accept them all."""
    adapter = get_adapter("godot")
    adapter.scaffold(_plan(), tmp_path, log=lambda _: None)
    raw = (
        "```Main.gd\nextends Node2D\nfunc _ready(): pass\n```\n"
        "```Player.gd\nextends CharacterBody2D\n```\n"
        "```Enemy.gd\nextends CharacterBody2D\n```\n"
        "```Boss.gd\nextends Node\n```\n"
        "```Pickup.gd\nextends Area2D\n```\n"
    )
    written = adapter.emit_scripts(_plan(), tmp_path, generate=lambda _: raw,
                                    log=lambda _: None)
    names = {p.name for p in written}
    assert names == {"Main.gd", "Player.gd", "Enemy.gd", "Boss.gd", "Pickup.gd"}


def test_godot_parser_ignores_non_gd_fenced_blocks(tmp_path):
    """The parser keys on `.gd` filenames in the fence. Other-language
    blocks (csv config, json metadata) must be skipped, not crash."""
    adapter = get_adapter("godot")
    adapter.scaffold(_plan(), tmp_path, log=lambda _: None)
    raw = (
        "```python\nprint('not a godot file')\n```\n"
        "```Main.gd\nextends Node2D\nfunc _ready(): pass\n```\n"
        "```config.csv\nkey,value\n```\n"
    )
    written = adapter.emit_scripts(_plan(), tmp_path, generate=lambda _: raw,
                                    log=lambda _: None)
    names = {p.name for p in written}
    assert names == {"Main.gd"}


def test_godot_parser_raises_runtime_error_when_generate_raises(tmp_path):
    """The pipeline catches RuntimeError and triggers a heal round. If the
    adapter swallowed the exception silently, heal would never fire."""
    adapter = get_adapter("godot")
    adapter.scaffold(_plan(), tmp_path, log=lambda _: None)

    def boom(_p):
        raise ConnectionError("model unreachable")

    with pytest.raises(RuntimeError) as exc:
        adapter.emit_scripts(_plan(), tmp_path, generate=boom,
                            log=lambda _: None)
    assert "godot script generation failed" in str(exc.value)


# ───────────────────────── Unity parser ───────────────────────────────


def test_unity_parser_extracts_cs_blocks_from_prose(tmp_path):
    adapter = get_adapter("unity")
    adapter.scaffold(_plan(), tmp_path, log=lambda _: None)
    raw = (
        "Here's the Unity setup:\n\n"
        "```PlayerController.cs\n"
        "using UnityEngine;\n"
        "public class PlayerController : MonoBehaviour { void Update() {} }\n"
        "```\n"
        "And the AI:\n"
        "```EnemyAI.cs\n"
        "using UnityEngine;\n"
        "public class EnemyAI : MonoBehaviour {}\n"
        "```\n"
    )
    written = adapter.emit_scripts(_plan(), tmp_path, generate=lambda _: raw,
                                    log=lambda _: None)
    names = {p.name for p in written}
    assert names == {"PlayerController.cs", "EnemyAI.cs"}


def test_unity_parser_raises_on_empty_response(tmp_path):
    adapter = get_adapter("unity")
    adapter.scaffold(_plan(), tmp_path, log=lambda _: None)
    with pytest.raises(RuntimeError, match="unity: LLM response had no parseable"):
        adapter.emit_scripts(_plan(), tmp_path, generate=lambda _: "",
                            log=lambda _: None)


# ───────────────────────── Unreal parser ──────────────────────────────


def test_unreal_parser_extracts_paired_h_cpp(tmp_path):
    adapter = get_adapter("unreal")
    plan = _plan(perspective="3d")
    plan.title = "TestProject"
    adapter.scaffold(plan, tmp_path, log=lambda _: None)
    raw = (
        "```TestProjectGameMode.h\n"
        "#pragma once\n"
        "#include \"CoreMinimal.h\"\n"
        "#include \"GameFramework/GameModeBase.h\"\n"
        "```\n"
        "```TestProjectGameMode.cpp\n"
        "#include \"TestProjectGameMode.h\"\n"
        "```\n"
        "```TestProjectCharacter.h\n"
        "#pragma once\n"
        "```\n"
    )
    written = adapter.emit_scripts(plan, tmp_path, generate=lambda _: raw,
                                    log=lambda _: None)
    names = {p.name for p in written}
    assert names == {
        "TestProjectGameMode.h",
        "TestProjectGameMode.cpp",
        "TestProjectCharacter.h",
    }


@pytest.mark.parametrize("title,expected", [
    ("EmptyResp",       "EmptyResp"),
    ("MyAwesomeRPG",    "MyAwesomeRPG"),
    ("FPSGame",         "FPSGame"),
    ("my cool game",    "MyCoolGame"),       # lowercase → PascalCased
    ("my awesome rpg",  "MyAwesomeRpg"),
    ("123Numeric",      "Sage123Numeric"),    # starts with digit → prefix Sage
    ("hello world!!!",  "HelloWorld"),        # punctuation stripped
])
def test_unreal_sanitize_name_preserves_user_casing(title, expected):
    """The user's chosen PascalCase / acronyms must survive sanitization.
    A title of "MyAwesomeRPG" must stay PascalCase — not become
    "Myawesomerpg" via `.capitalize()` destroying the original casing."""
    from sage.games.engines.unreal import _sanitize_name
    assert _sanitize_name(title) == expected


def test_unreal_parser_raises_on_empty_response(tmp_path):
    adapter = get_adapter("unreal")
    plan = _plan(perspective="3d")
    plan.title = "EmptyResp"
    adapter.scaffold(plan, tmp_path, log=lambda _: None)

    with pytest.raises(RuntimeError, match="unreal: LLM response had no parseable"):
        adapter.emit_scripts(plan, tmp_path, generate=lambda _: "",
                            log=lambda _: None)


# ───────────────────────── Bevy / Phaser / LÖVE / Pygame (raw bodies) ─


@pytest.mark.parametrize("engine,filename", [
    ("bevy",   "src/main.rs"),
    ("phaser", "src/main.ts"),
    ("love2d", "main.lua"),
    ("pygame", "main.py"),
])
def test_raw_body_engines_strip_fences_and_prose(engine, filename, tmp_path):
    """For engines whose prompt asks the LLM to NOT use fences, we
    accept either form: raw code, or fences that should be stripped."""
    adapter = get_adapter(engine)
    plan = _plan()
    plan.title = "X"
    adapter.scaffold(plan, tmp_path, log=lambda _: None)
    raw = "fn main() { println!(\"hi\"); }\n"  # generic — engines just write whatever
    if engine == "phaser":
        raw = "import Phaser from 'phaser';\nnew Phaser.Game({});\n"
    elif engine == "love2d":
        raw = "function love.draw() love.graphics.print('hi', 10, 10) end\n"
    elif engine == "pygame":
        raw = "import pygame\npygame.init()\npygame.quit()\n"

    written = adapter.emit_scripts(plan, tmp_path, generate=lambda _: raw,
                                    log=lambda _: None)
    assert len(written) == 1
    target = tmp_path / filename
    assert target.is_file()
    body = target.read_text(encoding="utf-8")
    # Body must contain some of the meaningful raw content.
    if engine == "phaser":
        assert "Phaser" in body
    elif engine == "love2d":
        assert "love.draw" in body
    elif engine == "pygame":
        assert "pygame" in body


def test_pygame_raises_on_empty_response(tmp_path):
    adapter = get_adapter("pygame")
    plan = _plan()
    plan.title = "X"
    adapter.scaffold(plan, tmp_path, log=lambda _: None)
    with pytest.raises(RuntimeError, match="pygame: LLM returned empty body"):
        adapter.emit_scripts(plan, tmp_path, generate=lambda _: "",
                            log=lambda _: None)


def test_pygame_propagates_generate_exception_as_runtime_error(tmp_path):
    """Like Godot/Unity/Unreal, Pygame must raise RuntimeError so the
    pipeline's heal loop kicks in."""
    adapter = get_adapter("pygame")
    plan = _plan()
    adapter.scaffold(plan, tmp_path, log=lambda _: None)

    def boom(_p):
        raise OSError("transient network failure")

    with pytest.raises(RuntimeError) as exc:
        adapter.emit_scripts(plan, tmp_path, generate=boom,
                            log=lambda _: None)
    assert "pygame script generation failed" in str(exc.value)


# ───────────────────────── unicode + comments ─────────────────────────


def test_godot_parser_preserves_unicode_and_comments(tmp_path):
    """LLM output sometimes includes unicode (em-dashes, smart quotes,
    Japanese in dialogue strings). The parser must round-trip them."""
    adapter = get_adapter("godot")
    adapter.scaffold(_plan(), tmp_path, log=lambda _: None)
    raw = (
        "```Main.gd\n"
        "extends Node2D\n"
        "# This comment has em-dashes — like this — and \"smart quotes\".\n"
        "# Also some Japanese: こんにちは\n"
        "var greeting := \"Hello — 世界\"\n"
        "func _ready():\n"
        "    print(greeting)\n"
        "```\n"
    )
    adapter.emit_scripts(_plan(), tmp_path, generate=lambda _: raw,
                        log=lambda _: None)
    body = (tmp_path / "scripts" / "Main.gd").read_text(encoding="utf-8")
    assert "—" in body
    assert "こんにちは" in body
    assert "世界" in body
