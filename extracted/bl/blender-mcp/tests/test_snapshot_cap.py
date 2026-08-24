"""Tests for the trajectory snapshot object cap (no Blender required).

The cap decides how much of a scene each trajectory row can describe. When it
bites, the delta between two snapshots is only meaningful if both sides kept
the *same* subset, so these tests pin the cap, the truncation marker, and the
sorted-subset behaviour that makes deltas stable.
"""

from __future__ import annotations

import ast
import io
import json
import sys
import types
from contextlib import redirect_stdout

from blender_mcp.trajectory import (
    MAX_SNAPSHOT_OBJECTS,
    SCHEMA_VERSION,
    _SNAPSHOT_VIA_EXECUTE_CODE,
    _SNAPSHOT_VIA_EXECUTE_CODE_TEMPLATE,
)

from conftest import ROOT_ADDON


# --------------------------------------------------------------------------
# minimal bpy stand-ins
# --------------------------------------------------------------------------

class _Vec(list):
    def __init__(self, xs):
        super().__init__(xs)
        self.x, self.y, self.z = xs


class _Matrix:
    translation = _Vec([0.0, 0.0, 0.0])

    def __matmul__(self, other):
        return _Vec(list(other))


class _Obj:
    def __init__(self, name, obj_type="MESH"):
        self.name = name
        self.type = obj_type
        self.location = _Vec([1.0, 2.0, 3.0])
        self.rotation_euler = _Vec([0.0, 0.0, 0.0])
        self.scale = _Vec([1.0, 1.0, 1.0])
        self.dimensions = _Vec([1.0, 1.0, 1.0])
        self.bound_box = [(0, 0, 0), (1, 1, 1)]
        self.matrix_world = _Matrix()
        self.matrix_local = _Matrix()
        self.material_slots = []
        self.constraints = []
        self.modifiers = []
        self.parent = None
        self.data = None
        self.animation_data = None

    def visible_get(self):
        return True


def _fake_bpy(objects):
    scene = types.SimpleNamespace(
        name="Scene",
        objects=objects,
        camera=None,
        frame_current=1,
        frame_start=1,
        frame_end=250,
        render=types.SimpleNamespace(fps=24, fps_base=1.0),
    )
    bpy = types.ModuleType("bpy")
    bpy.context = types.SimpleNamespace(scene=scene, selected_objects=[])
    bpy.data = types.SimpleNamespace(materials=[])
    bpy.app = types.SimpleNamespace(version_string="5.2.0 LTS")
    mathutils = types.ModuleType("mathutils")
    mathutils.Vector = lambda c: _Vec(list(c))
    return bpy, mathutils


def _run_fallback_probe(objects):
    """Execute the execute_code fallback probe against a fake scene."""
    bpy, mathutils = _fake_bpy(objects)
    saved = {k: sys.modules.get(k) for k in ("bpy", "mathutils")}
    sys.modules["bpy"], sys.modules["mathutils"] = bpy, mathutils
    try:
        buf = io.StringIO()
        with redirect_stdout(buf):
            exec(compile(_SNAPSHOT_VIA_EXECUTE_CODE, "<probe>", "exec"), {})
        return json.loads(buf.getvalue().strip().splitlines()[-1])
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v


def _run_native_snapshot(objects):
    """Execute the addon's get_world_state_snapshot against a fake scene.

    addon.py cannot be imported without bpy, so lift just the snapshot methods
    out of the source and exec them against stubs.
    """
    tree = ast.parse(ROOT_ADDON.read_text(encoding="utf-8"))
    cls = next(
        n for n in ast.walk(tree)
        if isinstance(n, ast.ClassDef)
        and any(
            isinstance(f, ast.FunctionDef) and f.name == "get_world_state_snapshot"
            for f in n.body
        )
    )
    wanted = {
        "get_world_state_snapshot",
        "_snapshot_geometry",
        "_snapshot_relations",
        "_snapshot_animation",
    }
    methods = [
        f for f in cls.body if isinstance(f, ast.FunctionDef) and f.name in wanted
    ]
    module = ast.Module(
        body=[ast.ClassDef(
            name="S", bases=[], keywords=[], body=methods, decorator_list=[]
        )],
        type_ignores=[],
    )
    ast.fix_missing_locations(module)

    bpy, mathutils = _fake_bpy(objects)
    traceback_stub = types.ModuleType("traceback")
    traceback_stub.print_exc = lambda: None
    ns = {
        "bpy": bpy,
        "mathutils": mathutils,
        "traceback": traceback_stub,
        "MAX_SNAPSHOT_OBJECTS": MAX_SNAPSHOT_OBJECTS,
    }
    exec(compile(module, "<addon>", "exec"), ns)
    return ns["S"]().get_world_state_snapshot()


# --------------------------------------------------------------------------
# tests
# --------------------------------------------------------------------------

def test_schema_version_records_cap_change():
    # Consumers branch on this to know whether objects_truncated is present.
    assert SCHEMA_VERSION >= 4


def test_cap_covers_realistic_production_scenes():
    # The old cap of 50 truncated essentially every real session.
    assert MAX_SNAPSHOT_OBJECTS >= 1000


def test_probe_template_placeholder_is_substituted():
    assert "__MAX_OBJECTS__" in _SNAPSHOT_VIA_EXECUTE_CODE_TEMPLATE
    assert "__MAX_OBJECTS__" not in _SNAPSHOT_VIA_EXECUTE_CODE
    assert str(MAX_SNAPSHOT_OBJECTS) in _SNAPSHOT_VIA_EXECUTE_CODE


def test_addon_cap_matches_trajectory_cap():
    # Two independent producers must agree, or deltas across a fallback switch
    # would compare differently-sized object arrays.
    text = ROOT_ADDON.read_text(encoding="utf-8")
    assert f"MAX_SNAPSHOT_OBJECTS = {MAX_SNAPSHOT_OBJECTS}" in text


def test_snapshot_under_cap_is_complete():
    objects = [_Obj(f"Obj_{i:04d}") for i in range(904)]
    for snapshot in (_run_native_snapshot(objects), _run_fallback_probe(objects)):
        assert snapshot.get("error") is None
        assert snapshot["object_count"] == 904
        assert snapshot["objects_listed"] == 904
        assert snapshot["objects_truncated"] is False
        assert len(snapshot["objects"]) == 904


def test_snapshot_over_cap_is_marked_and_bounded():
    objects = [_Obj(f"Obj_{i:04d}") for i in range(MAX_SNAPSHOT_OBJECTS + 500)]
    for snapshot in (_run_native_snapshot(objects), _run_fallback_probe(objects)):
        assert snapshot["object_count"] == MAX_SNAPSHOT_OBJECTS + 500
        assert snapshot["objects_listed"] == MAX_SNAPSHOT_OBJECTS
        assert snapshot["objects_truncated"] is True
        assert len(snapshot["objects"]) == MAX_SNAPSHOT_OBJECTS


def test_truncated_subset_is_stable_across_iteration_order():
    """A truncated snapshot must keep the same objects regardless of the order
    scene.objects yields them, or a step's before/after would hold different
    subsets and state_delta would invent adds and removes."""
    names = [f"Obj_{i:04d}" for i in range(MAX_SNAPSHOT_OBJECTS + 500)]
    forward = [_Obj(n) for n in names]
    reverse = [_Obj(n) for n in reversed(names)]

    for run in (_run_native_snapshot, _run_fallback_probe):
        a = [o["name"] for o in run(forward)["objects"]]
        b = [o["name"] for o in run(reverse)["objects"]]
        assert a == b
        assert a == sorted(a)
