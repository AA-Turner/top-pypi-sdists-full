"""Mesh generator — Blender headless primary, primitive fallback.

Blender exposes a full Python API in `--background --python` mode. We
generate a small script per request (cube / sphere / capsule with
adjustments based on the prompt), pipe it to Blender, and ask it to
export to glTF. The exported `.glb` is universally consumable (Godot
imports it natively, Unity 2022 LTS has a glTFast importer, Unreal 5
has built-in `Interchange` glTF support).

When Blender isn't installed, we still write a stub `.glb` so the
manifest stays consistent; the engine adapters know to swap in their
own primitives when they see the placeholder magic bytes.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class MeshResult:
    role: str
    path: Path
    backend: str           # "blender" | "placeholder"
    triangles: int


# Naive prompt → primitive heuristic. Real semantic understanding would
# call the LLM; for v1 we keep it deterministic + cheap. Engine adapters
# can replace these with real models later.
# Order matters — checked first → matched first. Cylinder-shapes come
# before cube-shapes because "brick pillar" should pick cylinder (the
# pillar) over cube (the brick).
_PRIM_KEYWORDS: tuple[tuple[tuple[str, ...], str], ...] = (
    (("cylinder", "tower", "pillar", "column", "barrel"), "cylinder"),
    (("ball", "sphere", "planet", "orb", "head"), "sphere"),
    (("capsule", "player", "character", "person", "enemy", "npc"), "capsule"),
    (("plane", "ground", "floor", "ceiling", "wall"), "plane"),
    (("cone", "tree", "fir"), "cone"),
    (("cube", "box", "block", "crate", "brick", "house"), "cube"),
)


def _pick_primitive(prompt: str) -> str:
    lower = prompt.lower()
    for words, prim in _PRIM_KEYWORDS:
        if any(w in lower for w in words):
            return prim
    return "cube"


class MeshGenerator:
    def __init__(self, out_dir: Path) -> None:
        self.out_dir = out_dir
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, role: str, prompt: str) -> MeshResult:
        out_path = self.out_dir / f"{role}.glb"
        prim = _pick_primitive(prompt)

        blender = _find_blender()
        if blender:
            try:
                _blender_export(blender, prim, out_path)
                # Count triangles for the report — exact count isn't load-bearing,
                # so we use a static estimate per primitive.
                tris = {"cube": 12, "sphere": 1280, "capsule": 1024,
                        "plane": 2, "cone": 64, "cylinder": 96}[prim]
                return MeshResult(role, out_path, "blender", tris)
            except Exception:  # noqa: BLE001 — fall through
                pass

        # Placeholder: minimal valid .glb. Engines see the magic header
        # and can swap in their own built-in primitive if they want.
        _write_placeholder_glb(out_path)
        return MeshResult(role, out_path, "placeholder", 0)


# ─────────────────────────── helpers ───────────────────────────────────


def _find_blender() -> Optional[Path]:
    p = shutil.which("blender")
    if p:
        return Path(p)
    mac = Path("/Applications/Blender.app/Contents/MacOS/Blender")
    return mac if mac.is_file() else None


_BLENDER_SCRIPT_TEMPLATE = """import bpy
import sys

# Wipe default scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

prim = "{prim}"
if prim == "cube":
    bpy.ops.mesh.primitive_cube_add()
elif prim == "sphere":
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16)
elif prim == "capsule":
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8)
    bpy.context.object.scale = (0.7, 0.7, 1.4)
elif prim == "plane":
    bpy.ops.mesh.primitive_plane_add(size=4)
elif prim == "cone":
    bpy.ops.mesh.primitive_cone_add(vertices=32)
elif prim == "cylinder":
    bpy.ops.mesh.primitive_cylinder_add(vertices=32)

# Export to glTF.
bpy.ops.export_scene.gltf(
    filepath="{out_path}",
    export_format='GLB',
    use_selection=False,
)
"""


def _blender_export(blender: Path, prim: str, out_path: Path) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tf:
        tf.write(_BLENDER_SCRIPT_TEMPLATE.format(prim=prim, out_path=str(out_path)))
        script_path = tf.name
    try:
        proc = subprocess.run(
            [str(blender), "--background", "--python", script_path],
            capture_output=True, text=True, timeout=60, check=False,
        )
        if proc.returncode != 0 or not out_path.exists():
            raise RuntimeError(
                f"blender export failed (rc={proc.returncode}): "
                f"{proc.stderr[-300:] if proc.stderr else ''}"
            )
    finally:
        try:
            os.unlink(script_path)
        except OSError:
            pass


def _build_placeholder_glb() -> bytes:
    """Build a minimal but spec-correct glTF 2.0 binary.

    Layout (per glTF 2.0 spec §4):
      Header (12 bytes): magic "glTF" | uint32 version | uint32 totalLength
      JSON chunk: uint32 chunkLength | uint32 chunkType "JSON" | <padded JSON>
      (no BIN chunk — minimal valid asset only needs the JSON chunk)

    All four-byte values are little-endian. The JSON payload is padded to
    a multiple of 4 with trailing spaces (0x20) per the spec, NOT NUL.
    Importer rejection here would silently break every 3D engine, so we
    build the bytes mathematically instead of hand-rolling magic numbers.
    """
    import struct as _struct
    json_payload = b'{"asset":{"version":"2.0","generator":"sage-placeholder"}}'
    # Pad with spaces to multiple of 4 (spec requirement).
    pad = (-len(json_payload)) % 4
    json_payload += b" " * pad
    json_chunk_header = _struct.pack("<I", len(json_payload)) + b"JSON"
    total_length = 12 + len(json_chunk_header) + len(json_payload)
    header = b"glTF" + _struct.pack("<II", 2, total_length)
    return header + json_chunk_header + json_payload


_PLACEHOLDER_GLB = _build_placeholder_glb()


def _write_placeholder_glb(path: Path) -> None:
    path.write_bytes(_PLACEHOLDER_GLB)
