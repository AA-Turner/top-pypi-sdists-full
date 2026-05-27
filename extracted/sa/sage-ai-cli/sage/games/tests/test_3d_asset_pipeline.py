"""3D asset pipeline — Blender + glTF, plus 2D/3D sprite handling.

The user-facing promise: sage produces 3D meshes for 3D games using
Blender via headless `--background --python` calls, exports as glTF
(`.glb` binary), and engines consume those .glb files via their built-in
glTF importers (Godot 4 has native support; Unity 2022 LTS has glTFast;
Unreal 5 uses Interchange).

We can't run a real Blender in CI, so these tests:

  * Intercept the Blender subprocess call and assert the arguments are
    what Blender expects (`--background --python <script>`).
  * Parse the generated Python script and verify it uses the correct
    `bpy.ops.mesh.primitive_*_add()` per detected primitive.
  * Drive `_pick_primitive` against a wide vocabulary so the heuristic
    routes "tower"→cylinder, "tree"→cone, "house"→cube etc.
  * Assert each engine's consume_assets copies the .glb into the right
    engine-conventional directory (res://assets/meshes, Assets/Meshes,
    Content/Meshes).
  * Verify the placeholder .glb fallback is structurally a valid glTF
    2.0 binary (magic bytes + version field) so engines accept it.
"""

from __future__ import annotations

import shutil
import struct
import subprocess
from pathlib import Path

import pytest

from sage.games.assets import MeshGenerator, MeshResult
from sage.games.assets.manifest import AssetManifest
from sage.games.assets.meshes import (
    _BLENDER_SCRIPT_TEMPLATE,
    _PLACEHOLDER_GLB,
    _pick_primitive,
)
from sage.games.engines import get_adapter
from sage.games.engines.base import GamePlan, GameRequest


# ───────────────────────── primitive classifier ───────────────────────


@pytest.mark.parametrize("prompt,prim", [
    # Cylinder family — pillars, towers, columns, barrels.
    ("a tall stone tower",          "cylinder"),
    ("a marble column",              "cylinder"),
    ("a wooden barrel of ale",       "cylinder"),
    ("a rusty oil pillar",           "cylinder"),
    # Sphere family — orbs, planets, heads.
    ("a glowing orb of magic",       "sphere"),
    ("alien planet",                  "sphere"),
    ("the player's head",             "sphere"),
    # Capsule — characters / NPCs.
    ("the hero character",            "capsule"),
    ("an enemy goblin npc",           "capsule"),
    ("a friendly person",             "capsule"),
    # Cone — trees, fir.
    ("a pine tree",                   "cone"),
    ("a tall fir tree",               "cone"),
    # Plane — floors, ground, walls.
    ("flat ground",                   "plane"),
    ("a stone wall",                  "plane"),
    ("the floor of the dungeon",      "plane"),
    # Cube — generic blocky things.
    ("a wooden crate",                "cube"),
    ("a stone block",                 "cube"),
    ("a brick house",                 "cube"),
    # Unknown → default cube.
    ("something otherworldly",        "cube"),
])
def test_primitive_classifier_full_vocabulary(prompt, prim):
    assert _pick_primitive(prompt) == prim


# ───────────────────────── Blender script template ────────────────────


@pytest.mark.parametrize("prim,bpy_op", [
    ("cube",     "bpy.ops.mesh.primitive_cube_add"),
    ("sphere",   "bpy.ops.mesh.primitive_uv_sphere_add"),
    ("capsule",  "bpy.ops.mesh.primitive_uv_sphere_add"),  # uses sphere + scale
    ("plane",    "bpy.ops.mesh.primitive_plane_add"),
    ("cone",     "bpy.ops.mesh.primitive_cone_add"),
    ("cylinder", "bpy.ops.mesh.primitive_cylinder_add"),
])
def test_blender_script_template_uses_correct_bpy_op(prim, bpy_op, tmp_path):
    """The template branches on the primitive name. We render it for each
    primitive and grep for the right Blender Python API call — a typo
    here means Blender exits with `AttributeError: bpy.ops.mesh has no
    attribute 'primitive_cube_addd'`."""
    script = _BLENDER_SCRIPT_TEMPLATE.format(
        prim=prim, out_path=str(tmp_path / "out.glb"),
    )
    assert bpy_op in script
    # Always exports as glTF GLB
    assert "export_scene.gltf" in script
    assert "GLB" in script


def test_blender_subprocess_invocation_uses_correct_flags(tmp_path, monkeypatch):
    """When Blender is detected, sage runs `<blender> --background --python <script>`.
    Wrong flags → Blender opens a GUI window. Catch this by intercepting
    subprocess.run and asserting the args."""
    from sage.games.assets import meshes as m

    fake_blender = tmp_path / "fake-blender"
    fake_blender.write_text("#!/bin/sh\n")
    monkeypatch.setattr(m, "_find_blender", lambda: fake_blender)

    captured: list[list[str]] = []

    def fake_run(args, **kwargs):
        captured.append(list(args))
        # Pretend Blender wrote the glb so the path passes the post-condition.
        for i, a in enumerate(args):
            if a == "--python" and i + 1 < len(args):
                # Read the script and find the out_path.
                script_text = Path(args[i + 1]).read_text(encoding="utf-8")
                for line in script_text.splitlines():
                    if 'filepath="' in line:
                        out = line.split('filepath="', 1)[1].split('"', 1)[0]
                        Path(out).write_bytes(_PLACEHOLDER_GLB)
                        break

        class _P:
            returncode = 0
            stdout = ""
            stderr = ""
        return _P()

    monkeypatch.setattr(m.subprocess, "run", fake_run)

    gen = MeshGenerator(tmp_path / "meshes")
    result = gen.generate("hero", "the hero character")

    assert captured, "Blender was never invoked"
    args = captured[0]
    # First arg is the binary; then --background, --python, <script.py>.
    assert str(fake_blender) in args[0]
    assert "--background" in args
    assert "--python" in args
    # The script path passed must be a real file (Blender requires this).
    py_idx = args.index("--python")
    script_path = Path(args[py_idx + 1])
    assert script_path.suffix == ".py"
    assert result.backend == "blender"
    assert result.path.read_bytes().startswith(b"glTF")


# ───────────────────────── placeholder .glb validity ──────────────────


def test_placeholder_glb_is_valid_gltf_2_binary():
    """Engines parse .glb headers strictly: 12-byte file header (magic +
    version + length), then JSON chunk + optional BIN chunk. We assert
    the placeholder matches that layout — otherwise Godot/Unity import
    fails with "invalid glTF" rather than gracefully substituting."""
    blob = _PLACEHOLDER_GLB
    assert blob.startswith(b"glTF"), "missing glTF magic"
    version = struct.unpack("<I", blob[4:8])[0]
    assert version == 2, f"placeholder declares glTF version {version}, must be 2"
    declared_length = struct.unpack("<I", blob[8:12])[0]
    assert declared_length == len(blob), (
        f"declared length {declared_length} ≠ actual {len(blob)}"
    )
    # First chunk must be JSON (type 0x4E4F534A = 'JSON').
    json_chunk_len = struct.unpack("<I", blob[12:16])[0]
    chunk_type = blob[16:20]
    assert chunk_type == b"JSON", f"first chunk must be JSON, got {chunk_type!r}"
    # The JSON must be parseable.
    import json as _json
    json_bytes = blob[20:20 + json_chunk_len].rstrip(b" ")
    parsed = _json.loads(json_bytes)
    assert parsed["asset"]["version"] == "2.0"


# ───────────────────────── per-engine 3D consumption ──────────────────


def _make_plan(engine: str) -> GamePlan:
    req = GameRequest(
        task_type="game", engine=engine, genre="rpg",
        perspective="3d", art_style="low-poly",
        target="windows", raw_prompt="3D rpg",
    )
    return GamePlan(
        request=req, title="3D Test", description="x",
        features=[],
        sprite_roles=[("player_portrait", "2D player portrait")],
        mesh_roles=[("hero", "character mesh"),
                    ("tree", "pine tree mesh"),
                    ("rock", "boulder mesh")],
        audio_roles=[],
        target="windows",
    )


def _make_manifest_with_3d(tmp_path: Path) -> AssetManifest:
    """Manifest with 3 .glb files + a 2D portrait .png. Mimics a typical
    3D game's asset spread."""
    mesh_dir = tmp_path / "meshes_in"
    mesh_dir.mkdir(exist_ok=True)
    sprite_dir = tmp_path / "sprites_in"
    sprite_dir.mkdir(exist_ok=True)

    meshes = {}
    for role in ("hero", "tree", "rock"):
        p = mesh_dir / f"{role}.glb"
        p.write_bytes(_PLACEHOLDER_GLB)
        meshes[role] = p

    sprites = {}
    portrait = sprite_dir / "player_portrait.png"
    portrait.write_bytes(b"\x89PNG\r\n\x1a\nstub")
    sprites["player_portrait"] = portrait

    return AssetManifest(sprites=sprites, meshes=meshes, audio={})


@pytest.mark.parametrize("engine,mesh_subdir", [
    ("godot",  "assets/meshes"),
    ("unity",  "Assets/Meshes"),
    ("unreal", "Content/Meshes"),
])
def test_3d_engines_consume_glb_into_canonical_directory(engine, mesh_subdir, tmp_path):
    """Each 3D-capable engine has its own conventional path for meshes.
    Godot uses res://assets/meshes, Unity uses Assets/Meshes, Unreal uses
    Content/Meshes. Verify the .glb files land in the right place — wrong
    location means the engine's importer never sees them."""
    adapter = get_adapter(engine)
    adapter.scaffold(_make_plan(engine), tmp_path, log=lambda _: None)
    manifest = _make_manifest_with_3d(tmp_path)
    adapter.consume_assets(manifest, tmp_path, log=lambda _: None)

    target_dir = tmp_path / mesh_subdir
    glbs = list(target_dir.glob("*.glb"))
    assert len(glbs) == 3, (
        f"{engine}: expected 3 .glb files in {target_dir}, got {glbs}"
    )
    # Same .glb bytes round-trip — engine must see the exact file we generated.
    for p in glbs:
        assert p.read_bytes().startswith(b"glTF")


def test_3d_mesh_pipeline_handles_billboards_via_2d_sprite_path(tmp_path):
    """2D and 3D sprite handling: a "3D sprite" in many engines is a 2D
    image on a quad/billboard. Sage handles this by keeping sprites in
    the SpriteGenerator pipeline (always PNG) and using the MeshGenerator
    only for actual 3D geometry. We assert a manifest with both sprite
    + mesh roles consumes them into separate engine directories."""
    adapter = get_adapter("godot")
    adapter.scaffold(_make_plan("godot"), tmp_path, log=lambda _: None)
    manifest = _make_manifest_with_3d(tmp_path)
    adapter.consume_assets(manifest, tmp_path, log=lambda _: None)

    # 2D portrait → assets/sprites (PNG)
    pngs = list((tmp_path / "assets" / "sprites").glob("*.png"))
    assert len(pngs) == 1
    assert pngs[0].name == "player_portrait.png"
    # 3D meshes → assets/meshes (GLB)
    glbs = list((tmp_path / "assets" / "meshes").glob("*.glb"))
    assert len(glbs) == 3


# ───────────────────────── 3D pipeline end-to-end ─────────────────────


def test_3d_request_decomposer_forces_mesh_role(tmp_path, monkeypatch):
    """A 3D request (perspective=first-person / third-person / 3d) MUST
    end up with at least one mesh role in the plan, even if the LLM
    doesn't supply any. This is the sanity floor in _decompose."""
    monkeypatch.setattr("sage.games.assets.meshes._find_blender", lambda: None)

    from sage.games.pipeline import _decompose
    req = GameRequest(
        task_type="game", engine="unity", genre="fps",
        perspective="first-person", target="windows",
        raw_prompt="an FPS",
    )
    # Empty decompose JSON → plan should still floor in a mesh role.
    plan = _decompose(req, generate=lambda _p: '{"title":"X","meshes":[]}',
                     log=lambda _: None)
    assert plan.mesh_roles, "3D request must seed at least one mesh role"
    assert plan.mesh_roles[0][0] == "player"


def test_3d_request_skips_audio_floor_when_provided(tmp_path):
    """The decomposer floor doesn't *overwrite* what the LLM provided
    — it only fills in gaps. If the LLM gives 5 meshes, the plan keeps
    all 5; the floor doesn't reduce to 1."""
    from sage.games.pipeline import _decompose
    req = GameRequest(
        task_type="game", engine="unreal", genre="rpg",
        perspective="3d", target="windows", raw_prompt="3D rpg",
    )
    import json
    payload = json.dumps({
        "title": "X", "meshes": [
            {"role": "m1", "prompt": "p1"},
            {"role": "m2", "prompt": "p2"},
            {"role": "m3", "prompt": "p3"},
            {"role": "m4", "prompt": "p4"},
            {"role": "m5", "prompt": "p5"},
        ],
    })
    plan = _decompose(req, generate=lambda _p: payload, log=lambda _: None)
    assert len(plan.mesh_roles) == 5
    assert [r for r, _ in plan.mesh_roles] == ["m1", "m2", "m3", "m4", "m5"]
