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
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class MeshResult:
    role: str
    path: Path
    backend: str           # always "blender" — no other backend exists
    triangles: int
    animations: list[str] = field(default_factory=list)


class MeshMissingBackendError(RuntimeError):
    """Raised when Blender isn't installed. Carries an install hint.

    Sage refuses to ship a placeholder GLB — that would let engines
    "build" a 3D game with no meshes. The user installs Blender and
    re-runs."""

    def __init__(self) -> None:
        super().__init__(
            "Mesh generation requires Blender. Install one of:\n"
            "  • Windows: winget install -e --id BlenderFoundation.Blender\n"
            "  • macOS:   brew install --cask blender\n"
            "  • Linux:   apt install blender   (or snap install blender)\n"
            "Sage does NOT emit placeholder GLBs — empty meshes would "
            "produce invisible game objects, not a real 3D scene."
        )


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


# When a mesh role matches one of these character-ish keywords, the
# Blender export switches to a multi-piece armature + walk-cycle path so
# the engine adapters can hook up an AnimationPlayer. Roles like "rock"
# / "tree" / "wall" stay as static primitives — there's no point rigging
# a wall.
_CHARACTER_KEYWORDS = (
    "player", "character", "person", "hero", "enemy", "npc",
    "knight", "wizard", "mage", "warrior", "goblin", "ogre", "skeleton",
    "monster", "villager", "merchant",
)


def _pick_primitive(prompt: str) -> str:
    lower = prompt.lower()
    for words, prim in _PRIM_KEYWORDS:
        if any(w in lower for w in words):
            return prim
    return "cube"


def _is_character(role: str, prompt: str) -> bool:
    """True when this mesh should be rigged + animated.

    We match on EITHER role or prompt so the user can say:
      - role="player" (matches role)
      - prompt="3D capsule knight" (matches prompt)
    Either form triggers the character pipeline. Roles like `rock` /
    `tree` stay static — no point rigging a wall.
    """
    haystack = (role + " " + prompt).lower()
    return any(w in haystack for w in _CHARACTER_KEYWORDS)


class MeshGenerator:
    def __init__(self, out_dir: Path) -> None:
        self.out_dir = out_dir
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, role: str, prompt: str) -> MeshResult:
        out_path = self.out_dir / f"{role}.glb"

        blender = _find_blender()
        # Character roles: rigged armature + idle + walk animation, exported
        # as a single GLB with embedded animation tracks. The engine adapter
        # discovers tracks via the manifest's mesh_animations dict and can
        # wire an AnimationPlayer node up to play them.
        if blender is None:
            raise MeshMissingBackendError()

        # Character roles → rigged armature + idle/walk animations.
        if _is_character(role, prompt):
            _blender_export_character(blender, out_path)
            return MeshResult(
                role, out_path, "blender", 72,
                animations=["idle", "walk"],
            )

        # Static primitive — cube / sphere / cylinder / etc. picked by prompt.
        prim = _pick_primitive(prompt)
        _blender_export(blender, prim, out_path)
        tris = {"cube": 12, "sphere": 1280, "capsule": 1024,
                "plane": 2, "cone": 64, "cylinder": 96}[prim]
        return MeshResult(role, out_path, "blender", tris)


# ─────────────────────────── helpers ───────────────────────────────────


def _find_blender() -> Optional[Path]:
    """Locate the Blender executable across platforms.

    PATH first (cheapest), then platform-specific install locations.
    winget installs on Windows land under either `Program Files` or
    `%LOCALAPPDATA%` depending on install scope — we glob both because
    the version sub-directory ("Blender 4.5", "Blender 5.0", ...) shifts
    with each minor release.
    """
    p = shutil.which("blender")
    if p:
        return Path(p)

    import platform as _platform
    from glob import glob

    sysname = _platform.system()
    if sysname == "Darwin":
        mac = Path("/Applications/Blender.app/Contents/MacOS/Blender")
        return mac if mac.is_file() else None
    if sysname == "Windows":
        local_app = Path(os.environ.get("LOCALAPPDATA",
                                         str(Path.home() / "AppData" / "Local")))
        patterns = (
            r"C:\Program Files\Blender Foundation\Blender *\blender.exe",
            r"C:\Program Files (x86)\Blender Foundation\Blender *\blender.exe",
            str(local_app / "Programs" / "Blender Foundation"
                / "Blender *" / "blender.exe"),
        )
        for pat in patterns:
            hits = sorted(glob(pat), reverse=True)
            if hits:
                return Path(hits[0])
        return None
    # Linux: blender package installs into /usr/bin (covered by which),
    # or AppImage somewhere in $HOME. Nothing more to glob reliably.
    return None


_BLENDER_SCRIPT_TEMPLATE = """import bpy
import sys

# Wipe default scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

prim = {prim!r}
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

# Export to glTF. We use !r on the path so Python repr-escapes Windows
# backslashes — otherwise `filepath="C:\\Users\\..."` becomes a unicode-
# escape SyntaxError ("\\U..." looked like a U+XXXXXXXX literal).
bpy.ops.export_scene.gltf(
    filepath={out_path!r},
    export_format='GLB',
    use_selection=False,
)
"""


def _blender_export(blender: Path, prim: str, out_path: Path) -> None:
    """Render a static primitive (cube/sphere/capsule/etc.) to GLB.

    Used for non-character roles. Character roles go through
    `_blender_export_character` for the rigged + animated path.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tf:
        # `format` with !r conversion repr-quotes the strings — handles
        # Windows backslashes and any embedded quotes correctly.
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


_BLENDER_CHARACTER_SCRIPT = r"""import bpy
import math

# Wipe default scene first.
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for action in list(bpy.data.actions):
    bpy.data.actions.remove(action)

# Build a 6-piece blocky character: head + torso + 2 arms + 2 legs.
# Each piece is a cube primitive scaled in place. Joining + parenting
# them to an armature gives the character a skeleton we can animate.

def cube(name, location, scale):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    return obj

head  = cube("Head",  ( 0.0, 0.0, 1.85), (0.35, 0.35, 0.35))
torso = cube("Torso", ( 0.0, 0.0, 1.25), (0.45, 0.30, 0.55))
arm_l = cube("ArmL",  ( 0.55, 0.0, 1.20), (0.15, 0.15, 0.45))
arm_r = cube("ArmR",  (-0.55, 0.0, 1.20), (0.15, 0.15, 0.45))
leg_l = cube("LegL",  ( 0.20, 0.0, 0.40), (0.18, 0.18, 0.45))
leg_r = cube("LegR",  (-0.20, 0.0, 0.40), (0.18, 0.18, 0.45))

# Join all body parts into one mesh so the GLB has a single skinned mesh.
bpy.ops.object.select_all(action='DESELECT')
for o in (head, torso, arm_l, arm_r, leg_l, leg_r):
    o.select_set(True)
bpy.context.view_layer.objects.active = torso
bpy.ops.object.join()
body = bpy.context.object
body.name = "Body"

# Now create the armature with one root + matching bones.
bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
arm_obj = bpy.context.object
arm_obj.name = "Armature"
arm = arm_obj.data
arm.edit_bones.remove(arm.edit_bones[0])

def bone(name, head_pos, tail_pos, parent=None):
    b = arm.edit_bones.new(name)
    b.head = head_pos
    b.tail = tail_pos
    if parent is not None:
        b.parent = parent
        b.use_connect = False
    return b

root  = bone("Root",  (0, 0, 0.95), (0, 0, 1.05))
spine = bone("Spine", (0, 0, 1.05), (0, 0, 1.65), root)
head_b = bone("HeadB", (0, 0, 1.65), (0, 0, 2.05), spine)
arml_b = bone("ArmLB", ( 0.40, 0.0, 1.45), ( 0.55, 0.0, 0.95), spine)
armr_b = bone("ArmRB", (-0.40, 0.0, 1.45), (-0.55, 0.0, 0.95), spine)
legl_b = bone("LegLB", ( 0.20, 0.0, 0.85), ( 0.20, 0.0, 0.10), root)
legr_b = bone("LegRB", (-0.20, 0.0, 0.85), (-0.20, 0.0, 0.10), root)

bpy.ops.object.mode_set(mode='OBJECT')

# Parent the body mesh to the armature with automatic weights so vertices
# follow nearest bones — good enough for a chunky walk cycle. Real games
# would hand-paint weights, but this is sage's fallback.
body.select_set(True)
arm_obj.select_set(True)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

# Animation: 24 fps walk cycle, 24 frames = 1 second loop. Arms swing
# opposite to legs (classic bipedal); spine sways slightly side-to-side.
# Frame 1 = neutral, 7 = left foot fwd, 13 = neutral, 19 = right foot fwd.
scene = bpy.context.scene
scene.render.fps = 24

def set_pose(action, frame, bone_name, rotation_xyz):
    pb = arm_obj.pose.bones[bone_name]
    pb.rotation_mode = 'XYZ'
    pb.rotation_euler = rotation_xyz
    pb.keyframe_insert(data_path="rotation_euler", frame=frame)

# IDLE: subtle breath sway, 24 frames.
bpy.ops.object.mode_set(mode='POSE')
idle = bpy.data.actions.new(name="idle")
arm_obj.animation_data_create()
arm_obj.animation_data.action = idle
for f, sway in ((1, 0.0), (12, 0.05), (24, 0.0)):
    set_pose(idle, f, "Spine", (sway, 0, 0))
idle.use_fake_user = True

# WALK: arm + leg cycle, 24 frames.
walk = bpy.data.actions.new(name="walk")
arm_obj.animation_data.action = walk
import math as _m
def keys(name, frames_rots):
    for f, rxyz in frames_rots:
        set_pose(walk, f, name, rxyz)

# Legs (X = forward/back swing). 24-frame loop.
keys("LegLB", [(1, (0,0,0)), (7, ( 0.6,0,0)), (13, (0,0,0)), (19, (-0.6,0,0)), (24, (0,0,0))])
keys("LegRB", [(1, (0,0,0)), (7, (-0.6,0,0)), (13, (0,0,0)), (19, ( 0.6,0,0)), (24, (0,0,0))])
# Arms opposite to legs.
keys("ArmLB", [(1, (0,0,0)), (7, (-0.5,0,0)), (13, (0,0,0)), (19, ( 0.5,0,0)), (24, (0,0,0))])
keys("ArmRB", [(1, (0,0,0)), (7, ( 0.5,0,0)), (13, (0,0,0)), (19, (-0.5,0,0)), (24, (0,0,0))])
# Spine: tiny side sway.
keys("Spine", [(1, (0,0,0)), (12, (0, 0.1, 0)), (24, (0,0,0))])
walk.use_fake_user = True

bpy.ops.object.mode_set(mode='OBJECT')
scene.frame_end = 24

# Select everything we want exported.
bpy.ops.object.select_all(action='SELECT')

# glTF needs `export_animations=True` and the actions present in
# bpy.data.actions get baked into the GLB. NLA strips aren't required
# when use_fake_user is True (the export sees the actions explicitly).
bpy.ops.export_scene.gltf(
    filepath={out_path!r},
    export_format='GLB',
    use_selection=False,
    export_animations=True,
    export_animation_mode='ACTIONS',
    export_nla_strips=False,
    export_apply=False,
)
"""


def _blender_export_character(blender: Path, out_path: Path) -> None:
    """Run the rigged-character export script in Blender headless.

    Produces a single GLB with: one skinned mesh + an armature + two
    actions named "idle" and "walk". Engine adapters look these up by
    name to wire AnimationPlayer / Animator transitions.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tf:
        tf.write(_BLENDER_CHARACTER_SCRIPT.format(out_path=str(out_path)))
        script_path = tf.name
    try:
        proc = subprocess.run(
            [str(blender), "--background", "--python", script_path],
            capture_output=True, text=True, timeout=120, check=False,
        )
        if proc.returncode != 0 or not out_path.exists():
            raise RuntimeError(
                f"blender character export failed (rc={proc.returncode}): "
                f"{proc.stderr[-400:] if proc.stderr else ''}"
            )
    finally:
        try:
            os.unlink(script_path)
        except OSError:
            pass


