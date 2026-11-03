"""
The MuJoCo family's half of moving a benchmark to the GPU: find the model inside a benchmark
after its reset, write it out as a self-contained MJCF with its files, and compare two compiles of it.

In one sentence: a CPU benchmark, once its reset started an episode, is searched for its `mujoco.MjModel` → the MJCF it
was compiled from is written out with every file it reads (robosuite keeps that MJCF; anything else is saved with
mj_saveLastXML) → the copy is compiled again in the same MuJoCo and compared field by field with the live model, so an
export that lost something (mujoco 3.2.3's saver drops <compiler inertiagrouprange>, and LIBERO's bowl weighed 46 g
instead of 5.6 g) fails here rather than on the GPU → what the benchmark changed after compiling (robosuite places
fixtures per reset into body_pos / body_quat) is kept per episode, as state.

WHY a search instead of an interface: a CPU benchmark is ported as it is written, and the simulators it wraps keep
the model in different places (robosuite: env.sim.model._model, gymnasium: env.unwrapped.model, dm_control:
env.physics.model.ptr); the search names the path it found so a wrong find is visible.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Any

import numpy as np


from seq.port.errors import PortError




REF_FIELDS = ("body_mass", "body_inertia", "body_ipos", "body_iquat", "body_pos", "body_quat", "body_parentid",
              "jnt_type", "jnt_range", "jnt_axis", "jnt_stiffness", "dof_armature", "dof_damping", "dof_frictionloss",
              "geom_type", "geom_size", "geom_friction", "geom_solref", "geom_solimp", "geom_margin", "geom_gap",
              "geom_condim", "geom_contype", "geom_conaffinity", "geom_priority", "geom_group", "geom_rgba",
              "actuator_gainprm", "actuator_biasprm", "actuator_ctrlrange", "actuator_forcerange", "actuator_gear",
              "cam_fovy", "cam_pos", "cam_quat", "light_pos", "light_dir", "light_diffuse", "light_ambient",
              "light_specular", "light_castshadow")

MESH_FRAME_FIELDS = ("geom_size", "geom_pos", "geom_quat")

OPT_FIELDS = ("timestep", "integrator", "cone", "jacobian", "solver", "iterations", "tolerance", "ls_iterations",
              "ls_tolerance", "noslip_iterations", "noslip_tolerance", "ccd_iterations", "ccd_tolerance",
              "impratio", "disableflags", "enableflags", "gravity", "wind", "density", "viscosity", "o_margin")


PATH_FIELDS = frozenset({"mesh_pathadr", "tex_pathadr", "hfield_pathadr", "skin_pathadr", "paths", "npaths",
                         "nbuffer", "site_rgba", "names", "names_map", "nnames", "nnames_map", "signature"})


STATE_FIELDS = ("body_pos", "body_quat", "geom_rgba", "geom_friction", "body_mass", "geom_size", "geom_pos",
                "geom_quat", "light_pos", "light_dir", "cam_pos", "cam_quat")

_ATTRS = ("sim", "physics", "unwrapped", "env", "_env", "model", "data", "mj_model", "mj_data", "_model", "_data",
          "_physics")

_LEAVES = (str, bytes, int, float, bool, list, tuple, dict, set, np.ndarray)


def write_new(path: str, text: str, *, force: bool = False) -> None:
    """Write a skeleton's file unless one is there that says something else: scaffolding again replaced the TODOs the
    user had filled in. `force` writes over it."""
    if not force and os.path.exists(path):
        with open(path) as f:
            if f.read() != text:
                raise PortError(f"{path} is there and differs from the skeleton (what you changed in it would be lost): "
                                "pass --force to write over it, or scaffold into another --out")
    with open(path, "w") as f:
        f.write(text)


@dataclass
class Found:
    """A MuJoCo model found inside an environment handle."""

    model: Any
    data: Any | None
    xml: str | None
    source: str
    path: str
    owner: Any = field(default=None, repr=False)


def _mujoco():
    try:
        import mujoco
    except ImportError as exc:
        raise PortError('this step runs MuJoCo: for export, the version your benchmark uses (pip install mujoco==...); '
                        'for check-model, scaffold and compare, pip install "sequence-ai[port]"') from exc
    return mujoco


def quiet_warp(wp: Any) -> None:
    """Keep Warp's banner and its module-load lines out of a report: log_level from Warp 1.18 on (where `quiet` is
    gone and setting it does nothing), quiet before it."""
    if hasattr(wp, "LOG_WARNING"):
        wp.config.log_level = wp.LOG_WARNING
    else:
        wp.config.quiet = True


def _held(obj: Any, mujoco: Any) -> tuple[Any, Any, str] | None:
    """(model, data, path suffix) when `obj` holds a MuJoCo model itself, else None: a bare MjModel; robosuite's MjSim
    (sim.model._model, sim.data._data); dm_control's Physics (physics.model.ptr); anything with .model / .data."""
    if isinstance(obj, mujoco.MjModel):
        return obj, None, ""
    m, d = getattr(obj, "model", None), getattr(obj, "data", None)
    if isinstance(getattr(m, "_model", None), mujoco.MjModel):
        return m._model, getattr(d, "_data", None), ".model._model"
    if isinstance(getattr(m, "ptr", None), mujoco.MjModel):
        return m.ptr, getattr(d, "ptr", None), ".model.ptr"
    if isinstance(m, mujoco.MjModel):
        return m, (d if isinstance(d, mujoco.MjData) else None), ".model"
    return None


def find_model(env: Any, depth: int = 6) -> Found:
    """The MuJoCo model inside `env` - the benchmark, after its reset: a breadth-first search through the attributes
    simulators keep it under, then through the instance attributes of each object met. Raises PortError when there is
    none (not a MuJoCo benchmark: the SAPIEN family has its own adapter; a GPU-native engine needs no port)."""
    mujoco = _mujoco()
    queue: list[tuple[Any, str]] = [(env, "benchmark")]
    seen: set[int] = set()
    for _ in range(depth):
        nxt: list[tuple[Any, str]] = []
        for obj, path in queue:
            if obj is None or id(obj) in seen:
                continue
            seen.add(id(obj))
            held = _held(obj, mujoco)
            if held is not None:
                model, data, suffix = held
                return Found(model=model, data=data, xml=None, source="mj_saveLastXML", path=path + suffix)
            for name in _ATTRS:
                try:
                    val = getattr(obj, name, None)
                except Exception:
                    val = None
                if val is not None and not isinstance(val, _LEAVES):
                    nxt.append((val, f"{path}.{name}"))
            for name, val in (vars(obj).items() if hasattr(obj, "__dict__") else ()):
                if name not in _ATTRS and val is not None and not isinstance(val, _LEAVES):
                    nxt.append((val, f"{path}.{name}"))
        queue = nxt
    raise PortError("no MuJoCo model inside the benchmark after its reset (searched sim, physics, unwrapped, env, model, "
                    "data and every instance attribute): this is not a MuJoCo benchmark")


def _own(obj: Any, name: str) -> bool:
    """`name` is obj's own attribute (its instance's or its class's), not one a wrapper forwards through __getattr__:
    gymnasium's wrappers forward sim and model to the environment inside but refuse its private _xml_processors, so
    the environment itself is the one whose edits the export must apply. {gymnasium core.py "ACCESSING PRIVATE
    ATTRIBUTE '{NAME}' IS PROHIBITED"}"""
    return name in getattr(obj, "__dict__", {}) or any(name in vars(k) for k in type(obj).__mro__)


def with_xml(found: Found, env: Any, depth: int = 6) -> Found:
    """Attach the MJCF the model was compiled from. robosuite keeps it: its environment's task model renders it
    (model.get_xml()), and the environment edits it before compiling — through every one of its _xml_processors
    (robosuite 1.5: edit_model_xml first, where RoboCasa adds its cameras) or its one _xml_processor (1.4). Anything
    else: mj_saveLastXML, which the export then proves by recompiling it.
    {robosuite@5ce6643 environments/base.py "SELF._XML_PROCESSORS = [SELF.EDIT_MODEL_XML]"}"""
    mujoco = _mujoco()
    queue, seen = [env], set()
    for _ in range(depth):
        nxt = []
        for obj in queue:
            if id(obj) in seen or obj is None:
                continue
            seen.add(id(obj))
            task = getattr(obj, "model", None) if _own(obj, "model") else None
            sim = getattr(obj, "sim", None) if _own(obj, "sim") else None
            if callable(getattr(task, "get_xml", None)) and getattr(getattr(sim, "model", None), "_model",
                                                                    None) is found.model:
                xml = task.get_xml()
                procs = getattr(obj, "_xml_processors", None)
                if procs is None:
                    proc = getattr(obj, "_xml_processor", None)
                    procs = [proc] if callable(proc) else []
                for proc in procs:
                    if callable(proc):
                        xml = proc(xml)
                found.xml, found.source, found.owner = xml, "robosuite", obj
                return found
            for name in ("env", "_env", "unwrapped"):
                val = getattr(obj, name, None)
                if val is not None:
                    nxt.append(val)
            for val in (vars(obj).values() if hasattr(obj, "__dict__") else ()):
                if val is not None and not isinstance(val, _LEAVES):
                    nxt.append(val)
        queue = nxt
    import tempfile

    with tempfile.NamedTemporaryFile("r", suffix=".xml") as f:
        mujoco.mj_saveLastXML(f.name, found.model)
        found.xml = f.read()
    found.source = "mj_saveLastXML"
    return found


def rewrite_assets(xml: str, out_dir: str, base_dir: str | None = None) -> tuple[str, int]:
    """Copy every file the MJCF reads into out_dir/assets/ (a short hash of its source path, then its name) and point
    the MJCF at the copies. A relative path resolves against the compiler's meshdir / texturedir / assetdir, under
    `base_dir`. Returns (the rewritten MJCF, files copied)."""
    root = ET.fromstring(xml)
    comp = root.find("compiler")
    dirs = {k: (comp.get(k) if comp is not None else None) for k in ("assetdir", "meshdir", "texturedir")}
    os.makedirs(os.path.join(out_dir, "assets"), exist_ok=True)
    copied: dict[str, str] = {}
    for el in root.iter():
        for attr, val in list(el.attrib.items()):
            if not attr.startswith("file"):
                continue
            if os.path.isabs(val):
                src = val
            else:
                d = (dirs["meshdir"] if el.tag in ("mesh", "skin") else
                     dirs["texturedir"] if el.tag in ("texture", "hfield") else None) or dirs["assetdir"] or ""
                if not os.path.isabs(d):
                    if base_dir is None:
                        raise PortError(f"the MJCF reads {val!r} relative to a directory the export cannot see; "
                                        "give the simulator absolute asset paths")
                    d = os.path.join(base_dir, d)
                src = os.path.join(d, val)
            if src not in copied:
                if not os.path.isfile(src):
                    raise PortError(f"the MJCF reads {src}, which does not exist")
                name = f"{hashlib.sha1(src.encode()).hexdigest()[:8]}_{os.path.basename(src)}"
                shutil.copyfile(src, os.path.join(out_dir, "assets", name))
                copied[src] = name
            el.set(attr, copied[src])
    if comp is None:
        comp = ET.SubElement(root, "compiler")
    for k in ("assetdir", "meshdir", "texturedir"):
        comp.attrib.pop(k, None)
    comp.set("meshdir", "../assets")
    comp.set("texturedir", "../assets")
    return ET.tostring(root, encoding="unicode"), len(copied)


def mesh_aabb(m: Any) -> np.ndarray:
    """Per mesh geom, the box its vertices span in the body frame (NaN rows for other geoms). Comparable across
    MuJoCo versions, which pick different frames for symmetric meshes and drop duplicate vertices differently."""
    mujoco = _mujoco()
    out = np.full((m.ngeom, 6), np.nan)
    for g in range(m.ngeom):
        k = m.geom_dataid[g]
        if m.geom_type[g] != mujoco.mjtGeom.mjGEOM_MESH or k < 0:
            continue
        v = m.mesh_vert[m.mesh_vertadr[k]: m.mesh_vertadr[k] + m.mesh_vertnum[k]]
        rot = np.zeros(9)
        mujoco.mju_quat2Mat(rot, m.geom_quat[g])
        w = v @ rot.reshape(3, 3).T + m.geom_pos[g]
        out[g] = np.r_[w.min(0), w.max(0)]
    return out


def reference(m: Any) -> dict[str, np.ndarray]:
    """What a compile is compared on, as arrays: REF_FIELDS, the mesh boxes, the options, and the object names."""
    mujoco = _mujoco()
    ref = {f: np.array(getattr(m, f)) for f in REF_FIELDS}
    ref["mesh_aabb"] = mesh_aabb(m)
    for f in OPT_FIELDS:
        ref[f"opt.{f}"] = np.array(getattr(m.opt, f))
    ref.update(flag_states(m))
    for kind, n in (("body", m.nbody), ("joint", m.njnt), ("geom", m.ngeom), ("actuator", m.nu), ("camera", m.ncam),
                    ("light", m.nlight)):
        obj = getattr(mujoco.mjtObj, f"mjOBJ_{kind.upper()}")

        ref[f"names.{kind}"] = np.array([mujoco.mj_id2name(m, obj, i) or f"#{i}" for i in range(n)], dtype=str)
    return ref


def flag_states(m: Any) -> dict[str, np.ndarray]:
    """Whether each optional feature is on, by name: an enable flag is on when set, a disable flag when not set. Two
    versions compare by these, not by the bit fields: mujoco 3.2.3 has MULTICCD, NATIVECCD and ISLAND as enable flags
    (off unless set) and 3.14 as disable flags (on unless set), so the same 0 means the opposite."""
    mujoco = _mujoco()
    out = {}
    for enum, bits, on_when_set in ((mujoco.mjtEnableBit, int(m.opt.enableflags), True),
                                    (mujoco.mjtDisableBit, int(m.opt.disableflags), False)):
        for name in dir(enum):
            if not (name.startswith("mjENBL_") or name.startswith("mjDSBL_")):
                continue
            bit = int(getattr(enum, name))
            if bit <= 0 or bit & (bit - 1):
                continue
            out[f"flag.{name[7:]}"] = np.array(int(bool(bits & bit) == on_when_set))
    return out




SAVED_DIGITS = 6





SAVED_RTOL = 10 * 0.5 * 10.0 ** (1 - SAVED_DIGITS)


COMPILE_NOISE = 1e-12


def _same(x: Any, y: Any, rtol: float) -> bool:
    """Two arrays alike: exactly, or - `rtol`, a float field of a save compiled again - each element within rtol of
    itself and COMPILE_NOISE of the field's largest value."""
    x, y = np.asarray(x), np.asarray(y)
    if rtol <= 0 or not (np.issubdtype(x.dtype, np.floating) and np.issubdtype(y.dtype, np.floating)):
        return bool(np.array_equal(x, y, equal_nan=True))
    finite = np.abs(x[np.isfinite(x)])
    scale = float(finite.max()) if finite.size else 0.0
    return bool(np.allclose(x, y, rtol=rtol, atol=COMPILE_NOISE * scale, equal_nan=True))


def model_diff(a: Any, b: Any, ignore: frozenset[str] | set[str] = frozenset(), rtol: float = 0.0) -> list[str]:
    """Every MjModel array / scalar and option that differs between two compiles in the same MuJoCo: exactly, or with
    `rtol` - a model compiled again from its 6-digit save (SAVED_RTOL) - a float field within that of itself."""
    bad = []
    for f in dir(a):
        if f.startswith("_") or f in PATH_FIELDS or f in ignore:
            continue
        try:
            x, y = getattr(a, f, None), getattr(b, f, None)
        except Exception:
            continue
        if isinstance(x, np.ndarray):
            if not isinstance(y, np.ndarray) or x.shape != y.shape or not _same(x, y, rtol):
                bad.append(f)
        elif isinstance(x, (int, float, bytes)) and not (x == y or isinstance(x, float) and isinstance(y, float)
                                                         and _same(x, y, rtol)):
            bad.append(f)
    for f in dir(a.opt):
        if not f.startswith("_") and isinstance(getattr(a.opt, f), (int, float, np.ndarray)):
            if not _same(getattr(a.opt, f), getattr(b.opt, f), rtol):
                bad.append(f"opt.{f}")
    return bad


def same_structure(a: Any, b: Any) -> bool:
    """Whether two compiles are one model with other numbers: the same names, every count and integer array (types,
    ids, addresses, flags) and option alike, and what differs only float arrays of the same shape. robosuite's Lift
    compiles each episode's MJCF again with the cube's size drawn for it; MuJoCo Warp runs those episodes as one model
    with the numbers set per world."""
    if bytes(a.names) != bytes(b.names):
        return False
    for f in model_diff(a, b):
        x, y = getattr(a, f, None), getattr(b, f, None)
        if not (isinstance(x, np.ndarray) and isinstance(y, np.ndarray) and x.shape == y.shape and x.dtype.kind == "f"):
            return False
    return True


def physics_signature(m: Any, varying: dict[str, np.ndarray] | None = None) -> str:
    """A hash of what shapes the physics and the picture. Sites are left out (a task's regions, no physics), and so is
    every entry that differs between episodes (`varying`: field -> a mask of the entries that vary), so tasks that
    compile to the same physics share one GPU model."""
    mujoco = _mujoco()

    free = np.zeros(m.nbody, bool)
    free[m.jnt_bodyid[m.jnt_type == mujoco.mjtJoint.mjJNT_FREE]] = True
    varying = dict(varying or {})
    for f in ("body_pos", "body_quat"):
        varying[f] = (varying[f] | free) if f in varying else free
    h = hashlib.sha1()
    for name in ("nq", "nv", "nu", "na", "nbody", "njnt", "ngeom", "nmesh", "nmeshvert", "nmat", "ntex", "ncam",
                 "nlight", "neq", "ntendon", "nsensor"):
        h.update(f"{name}={getattr(m, name)};".encode())
    for kind, n in (("body", m.nbody), ("joint", m.njnt), ("geom", m.ngeom), ("actuator", m.nu), ("camera", m.ncam)):
        obj = getattr(mujoco.mjtObj, f"mjOBJ_{kind.upper()}")
        h.update("|".join(str(mujoco.mj_id2name(m, obj, i)) for i in range(n)).encode())
    for f in REF_FIELDS:
        arr = np.array(getattr(m, f))
        mask = varying.get(f)
        if mask is not None:
            arr = arr[~mask]
        h.update(f.encode())
        h.update(np.ascontiguousarray(arr).tobytes())
    for f in OPT_FIELDS:
        h.update(np.ascontiguousarray(np.array(getattr(m.opt, f))).tobytes())
    return h.hexdigest()[:16]
