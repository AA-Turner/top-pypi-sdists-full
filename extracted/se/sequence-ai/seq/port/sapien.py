"""
The SAPIEN side of the porting commands: where a CPU SAPIEN benchmark keeps its scene, what of
it a GPU port must start each episode from, what the scene is built of, and what SAPIEN's GPU pipeline cannot run.

In one sentence: the benchmark's own reset starts the episode → the sapien.Scene inside the benchmark is found → its
state (every dynamic body's pose and velocity, every articulation's root, joints and drive targets, in creation order —
the order a GPU port's own build makes them in) and its structure (each body's collision shapes, materials, mass, each
articulation's joints and drives) are written down → episodes that share a structure can be worlds of one GPU system
(a GPU system's worlds cannot change their shapes), the others need a system each.

WHY state and structure and not a scene file: a SAPIEN scene is built by the benchmark's own code (URDFs, meshes, task
logic placing them), so a GPU port builds its worlds with that same code and starts them from the recorded state —
which also carries what the benchmark's setup simulated (objects settling) — instead of rebuilding the scene from a
description. RoboTwin 2.0's port does exactly this.

Layout of a SAPIEN scene bundle (seq port export on a SAPIEN benchmark):
  manifest.json            engine "sapien", SAPIEN's version, the benchmark (its tasks and time limit), its episodes
                           and, per structure, its episodes, bodies, articulations and what the reset called that has no
                           GPU form
  structures/<key>.json    what that structure is built of (seq.port.sapien.structure_of)
  states.npz               per structure key: <key>.body_pose (n, B, 7), .body_vel (n, B, 6), .art_root (n, A, 7),
                           .art_qpos / .art_qvel / .art_target_q / .art_target_v (n, A, D)
"""
from __future__ import annotations

import hashlib
import json
import os
from typing import Any

import numpy as np

from seq.port.mujoco import PortError, write_new


_ATTRS = ("scene", "_scene", "sim", "env", "unwrapped", "_env", "task", "task_env", "_task_env", "base_env")

CPU_ONLY = ("compute_passive_force",)


def _sapien():
    try:
        import sapien
    except ImportError as exc:
        raise PortError("exporting a SAPIEN benchmark needs SAPIEN here (pip install sapien): it runs the "
                        "benchmark's own reset") from exc
    return sapien


def find_scene(env: Any, depth: int = 6) -> tuple[Any, str]:
    """The sapien.Scene `env` - the benchmark, after its reset - holds, and where it was found (benchmark.env.scene,
    benchmark.env.unwrapped._scene, ...): breadth first, the usual attribute names before the others."""
    sapien = _sapien()
    seen, frontier = set(), [(env, "benchmark")]
    for _ in range(depth):
        nxt = []
        for obj, path in frontier:
            if id(obj) in seen or obj is None:
                continue
            seen.add(id(obj))
            if isinstance(obj, sapien.Scene):
                return obj, path
            if isinstance(obj, (str, bytes, int, float, bool, np.ndarray)):
                continue
            names = [a for a in _ATTRS if a in getattr(obj, "__dict__", {})]
            names += [a for a in getattr(obj, "__dict__", {}) if a not in names]
            for a in names:
                try:
                    nxt.append((getattr(obj, a), f"{path}.{a}"))
                except Exception:
                    continue
        frontier = nxt
    raise PortError("no sapien.Scene inside the benchmark after its reset (looked through its attributes "
                    f"{depth} levels deep): export runs a benchmark that holds the scene its episode runs in")


def _pose(p) -> list[float]:
    return [float(x) for x in (*p.p, *p.q)]


def state_of(scene: Any) -> dict[str, Any]:
    """What a GPU port starts an episode from: dynamic bodies (not articulation links) and articulations, each in
    creation order."""
    bodies = list(scene.physx_system.get_rigid_dynamic_components())
    arts = list(scene.get_all_articulations())
    dof = max((a.dof for a in arts), default=0)
    out = {
        "body_names": [c.entity.get_name() for c in bodies],
        "body_pose": np.array([_pose(c.entity.get_pose()) for c in bodies], np.float64).reshape(-1, 7),
        "body_vel": np.array([[*c.get_linear_velocity(), *c.get_angular_velocity()] for c in bodies],
                             np.float64).reshape(-1, 6),
        "art_names": [a.get_name() for a in arts], "art_dof": [int(a.dof) for a in arts],
        "art_root": np.array([_pose(a.get_root_pose()) for a in arts], np.float64).reshape(-1, 7),
        "art_qpos": np.zeros((len(arts), dof)), "art_qvel": np.zeros((len(arts), dof)),
        "art_target_q": np.zeros((len(arts), dof)), "art_target_v": np.zeros((len(arts), dof)),
    }
    for i, a in enumerate(arts):
        out["art_qpos"][i, :a.dof] = a.get_qpos()
        out["art_qvel"][i, :a.dof] = a.get_qvel()
        for k, j in enumerate(a.get_active_joints()):
            out["art_target_q"][i, k] = float(np.asarray(j.get_drive_target()).reshape(-1)[0])
            out["art_target_v"][i, k] = float(np.asarray(j.get_drive_velocity_target()).reshape(-1)[0])
    return out


def _r(x, nd: int = 6):
    return [round(float(v), nd) for v in np.asarray(x, np.float64).reshape(-1)]


def _shape(s) -> dict[str, Any]:
    kind = type(s).__name__.replace("PhysxCollisionShape", "").lower()
    out: dict[str, Any] = {"kind": kind, "local_pose": _r(_pose(s.get_local_pose()))}
    for attr in ("half_size", "radius", "half_length", "scale"):
        if hasattr(s, attr):
            out[attr] = _r(getattr(s, attr))
    if hasattr(s, "get_vertices"):
        v = np.ascontiguousarray(np.asarray(s.get_vertices(), np.float32))
        out["vertices"] = int(v.shape[0])
        out["vertices_sha1"] = hashlib.sha1(v.tobytes()).hexdigest()[:12]
    m = s.get_physical_material()
    out["material"] = _r([m.static_friction, m.dynamic_friction, m.restitution])
    if hasattr(s, "density"):
        out["density"] = round(float(s.density), 6)
    return out


def _body(c) -> dict[str, Any]:
    out: dict[str, Any] = {"name": c.entity.get_name(), "shapes": [_shape(s) for s in c.get_collision_shapes()]}
    if hasattr(c, "mass"):
        out.update(mass=round(float(c.mass), 9), inertia=_r(c.inertia, 9),
                   cmass_local_pose=_r(_pose(c.cmass_local_pose)),
                   disable_gravity=bool(getattr(c, "disable_gravity", False)))
    if hasattr(c, "kinematic"):
        out["kinematic"] = bool(c.kinematic)
    return out


def structure_of(scene: Any) -> dict[str, Any]:
    """What the scene is built of, in creation order: static and dynamic bodies (collision shapes, materials, mass,
    inertia), articulations (links as bodies, joints with their kind, limits and drives). Two episodes with the same
    structure can be worlds of one GPU system."""
    px = scene.physx_system
    out = {"static": [_body(c) for c in px.get_rigid_static_components()],
           "dynamic": [_body(c) for c in px.get_rigid_dynamic_components()], "articulations": []}
    for a in scene.get_all_articulations():
        joints = []
        for j in a.get_joints():
            item = {"name": j.get_name(), "kind": str(j.type)}
            if j.get_dof():
                item.update(limits=_r(j.get_limits()), stiffness=round(float(j.stiffness), 6),
                            damping=round(float(j.damping), 6), force_limit=round(float(j.force_limit), 6))
            joints.append(item)
        out["articulations"].append({"name": a.get_name(), "links": [_body(link) for link in a.get_links()],
                                     "joints": joints})
    return out


def structure_key(structure: dict[str, Any]) -> str:
    return hashlib.sha1(json.dumps(structure, sort_keys=True).encode()).hexdigest()[:12]


class watch_cpu_only:
    """Counts the calls a benchmark makes, while it is open, to what SAPIEN's GPU pipeline has no form of
    (CPU_ONLY): a GPU port has to replace them."""

    def __init__(self) -> None:
        self.calls = {name: 0 for name in CPU_ONLY}

    def __enter__(self):
        sapien = _sapien()
        cls = sapien.physx.PhysxArticulation
        self.saved = []
        for name in CPU_ONLY:
            fn = getattr(cls, name, None)
            if fn is None:
                continue

            def counted(*args, _fn=fn, _name=name, **kw):
                self.calls[_name] += 1
                return _fn(*args, **kw)

            try:
                setattr(cls, name, counted)
                self.saved.append((cls, name, fn))
            except (TypeError, AttributeError):
                continue
        return self

    def __exit__(self, *exc):
        for cls, name, fn in self.saved:
            setattr(cls, name, fn)
        return False


def export_sapien(reg: Any, bench: Any, reset: Any, episodes: list, out: str, say) -> dict[str, Any]:
    """The SAPIEN half of seq.port.export: each episode started by the benchmark's own reset, the structure and state of
    the scene it holds recorded (episodes grouped by structure), the bundle written. Returns the manifest."""
    sapien = _sapien()
    os.makedirs(os.path.join(out, "structures"), exist_ok=True)
    groups: dict[str, dict[str, Any]] = {}
    rows: dict[str, list[dict[str, Any]]] = {}
    for i, ep in enumerate(episodes):
        with watch_cpu_only() as watch:
            reset(ep.task, ep.seed)
        scene, path = find_scene(bench)
        structure = structure_of(scene)
        key = structure_key(structure)
        if key not in groups:
            with open(os.path.join(out, "structures", f"{key}.json"), "w") as f:
                json.dump(structure, f, indent=1)
            groups[key] = {"key": key, "found_at": path, "episodes": [], "cpu_only_calls": {}}
            say(f"structure {key}: {len(structure['dynamic'])} dynamic bodies, "
                f"{len(structure['articulations'])} articulation(s), at {path}")
        st = state_of(scene)
        g = groups[key]
        g["episodes"].append(i)
        g["bodies"], g["articulations"], g["art_dof"] = st["body_names"], st["art_names"], st["art_dof"]
        for name, n in watch.calls.items():
            if n:
                g["cpu_only_calls"][name] = g["cpu_only_calls"].get(name, 0) + n
        rows.setdefault(key, []).append(st)
        if (i + 1) % 25 == 0 or i + 1 == len(episodes):
            say(f"{i + 1}/{len(episodes)} episode(s) exported")
    arrays = {}
    for key, rs in rows.items():
        for f in ("body_pose", "body_vel", "art_root", "art_qpos", "art_qvel", "art_target_q", "art_target_v"):
            arrays[f"{key}.{f}"] = np.stack([r[f] for r in rs])
    np.savez_compressed(os.path.join(out, "states.npz"), **arrays)
    from seq.port.export import _sdk_version, benchmark_entry


    return {"version": 2, "engine": "sapien", "sapien_version": sapien.__version__, "sdk_version": _sdk_version(),
            "benchmark": benchmark_entry(reg),
            "episodes": [{"task": ep.task, "seed": ep.seed} for ep in episodes], "structures": list(groups.values())}


def check_sapien(scene: str, engine: str = "sapien-gpu") -> dict[str, Any]:
    """Can SAPIEN's GPU pipeline run what the bundle holds, and how many GPU systems does it take? A dynamic triangle
    mesh fails (PhysX's GPU pipeline simulates dynamic bodies with convex shapes only); a task whose episodes build
    different structures needs a system per structure, and a reset that calls what has no GPU form needs it replaced
    (both reported, neither fails)."""
    with open(os.path.join(scene, "manifest.json")) as f:
        man = json.load(f)
    if man.get("engine") != "sapien":
        raise PortError(f"{scene} was exported from {man.get('engine')!r}; --engine {engine} takes a SAPIEN scene")
    report: dict[str, Any] = {"engine": engine, "exported_with_sapien": man["sapien_version"], "structures": [],
                              "tasks": {}, "ok": True}
    for g in man["structures"]:
        with open(os.path.join(scene, "structures", f"{g['key']}.json")) as f:
            st = json.load(f)
        fails = []
        for b in st["dynamic"] + [link for a in st["articulations"] for link in a["links"]]:
            if b.get("kinematic"):
                continue
            meshes = [s for s in b["shapes"] if s["kind"] in ("trianglemesh", "nonconvexmesh")]
            if meshes:
                fails.append(f"{b['name']}: a dynamic body with a triangle mesh (PhysX's GPU pipeline simulates dynamic "
                             "bodies with convex shapes only): give it a convex hull or a convex decomposition")
        notes = []
        for name, n in g.get("cpu_only_calls", {}).items():
            if name == "compute_passive_force":
                notes.append(f"the reset calls compute_passive_force ({n} times): it has no GPU form; turning the links' "
                             "gravity off replaces its gravity term, its Coriolis term is lost")
        item = {"key": g["key"], "episodes": len(g["episodes"]), "dynamic": len(st["dynamic"]),
                "articulations": [(a["name"], sum(1 for j in a["joints"] if "limits" in j)) for a in st["articulations"]],
                "unsupported": fails, "notes": notes, "ok": not fails}
        report["ok"] &= item["ok"]
        report["structures"].append(item)
        for i in g["episodes"]:
            task = man["episodes"][i]["task"]
            report["tasks"].setdefault(task, set()).add(g["key"])
    report["tasks"] = {t: sorted(keys) for t, keys in report["tasks"].items()}
    return report


def lines(report: dict[str, Any]) -> list[str]:
    out = [f"check-model: {report['engine']} (exported with SAPIEN {report['exported_with_sapien']})"]
    for item in report["structures"]:
        arts = ", ".join(f"{n or '(unnamed)'} {d} dof" for n, d in item["articulations"]) or "none"
        out.append(f"structure {item['key']} ({item['episodes']} episode(s), {item['dynamic']} dynamic bodies, "
                   f"articulations: {arts}): " + ("supported" if item["ok"] else "FAILS"))
        out += [f"  engine   {u}" for u in item["unsupported"]]
        out += [f"  note     {n}" for n in item["notes"]]
    for task, keys in report["tasks"].items():
        if len(keys) > 1:
            out.append(f"task {task}: {len(keys)} structures — worlds of one GPU system share their bodies, so it takes a "
                       "system per structure")
    out.append("ok" if report["ok"] else "not ok: fix the findings above before porting (exit 1)")
    return out


_TEMPLATE = '''"""
{name}-gpu — {name} on SAPIEN's GPU pipeline: written by `seq port scaffold` from scene/ (exported with SAPIEN
{sapien}), structure {key} ({nconds} episode(s)).

A world of this benchmark is a sub-scene of one PhysxGpuSystem, built by {name}'s own scene code and started from the
state its CPU reset left (scene/states.npz); its constructor builds as many as an eval runs, at most {worlds}. What is
written here is what every SAPIEN port does the same way: the sub-scenes, gpu_init and the state written back after it
(as ManiSkill does: poses at each body's gpu_pose_index, every velocity zero, joints set, all applied), a reset from the
recorded state. What is yours (TODO): the scene code that builds a world (build_world), what an action sets at each
physics step (step), the observation and the success.
"""
import json
import os

import numpy as np

import seq

SCENE = "/opt/scene" if os.path.isdir("/opt/scene") else os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                          "scene")
KEY = "{key}"
SPACING = 4.0            # metres between sub-scenes: more than a world spans


def build_world(scene) -> None:
    """TODO: build one world into `scene` (a sub-scene of the GPU system) with {name}'s own code, creating its bodies
    in the order its CPU reset creates them: {bodies} and articulations {arts}. Nothing may step or read a pose here:
    a GPU system holds its worlds only after gpu_init."""
    raise NotImplementedError("build_world: {name}'s scene code, pointed at the given sub-scene")


@seq.benchmark(
    name="{name}-gpu",
    gpu="L4",
    # TODO: {name}'s own code and assets too (build_world runs them); SAPIEN as the export ran it, CUDA torch for the
    # GPU system's buffers
    image=(seq.Image.debian_slim(python="3.11")
           .uv_pip_install("sapien=={sapien}")
           .run_commands("python -m pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cu121")
           .add_local_dir("scene", "/opt/scene")),
    # TODO: the same as {name} (copied from the structure's episodes; a seed the export did not run has no start)
    tasks={tasks},
    seeds={seeds},
    max_seconds={max_seconds},
    # built after the machine's snapshot: how many worlds this eval runs, and the evaluated policy's control rate
    init={{"worlds": "{{num_worlds}}", "hz": "{{policy.hz}}"}},
)
class {cls}Gpu:
    def __init__(self, worlds: int, hz=None) -> None:
        import sapien
        import torch

        with open(os.path.join(SCENE, "manifest.json")) as f:
            man = json.load(f)
        self.group = next(g for g in man["structures"] if g["key"] == KEY)
        self.index = {{(e["task"], e["seed"]): i for i, e in enumerate(man["episodes"])}}
        with np.load(os.path.join(SCENE, "states.npz")) as z:
            self.st = {{k[len(KEY) + 1:]: z[k] for k in z.files if k.startswith(KEY + ".")}}
        # TODO: the physics steps an action takes - a step plays 1 / hz seconds, as the robot does:
        # round(1 / (hz x the timestep your scene code sets)); at registration no policy is evaluated (hz is None)
        # and nothing steps
        self.hz, self.substeps = (float(hz) if hz else None), 1
        sapien.physx.enable_gpu()
        self.px = px = sapien.physx.PhysxGpuSystem()
        self.n = int(worlds)
        for i in range(self.n):
            scene = sapien.Scene([px])
            px.set_scene_offset(scene, [i * SPACING, 0.0, 0.0])
            build_world(scene)
        comps = px.get_rigid_dynamic_components()
        initial = [(c, c.entity.get_pose()) for c in comps]
        initial += [(c, c.entity.get_pose()) for c in px.get_articulation_link_components() if c.articulation.root is c]
        arts = [l.articulation for l in px.get_articulation_link_components() if l.articulation.root is l]
        nb, na = len(self.group["bodies"]), len(self.group["articulations"])
        px.gpu_init()
        self.dev = px.cuda_rigid_body_data.torch().device
        self.body_idx = torch.tensor([c.gpu_pose_index for c in comps], device=self.dev).reshape(self.n, nb)
        self.art_idx = torch.tensor([a.gpu_index for a in arts], device=self.dev).reshape(self.n, na)
        self.root_idx = torch.tensor([a.root.gpu_pose_index for a in arts], device=self.dev).reshape(self.n, na)
        rbd = px.cuda_rigid_body_data.torch()
        for c, pose in initial:
            rbd[c.gpu_pose_index, :7] = torch.tensor([*pose.p, *pose.q], dtype=rbd.dtype, device=self.dev)
        rbd[:, 7:] = 0
        self._apply()
        self.episode = np.zeros(self.n, np.int64)

    def _apply(self) -> None:
        px = self.px
        for fn in ("rigid_dynamic_data", "articulation_qpos", "articulation_qvel", "articulation_root_pose",
                   "articulation_root_velocity", "articulation_target_position", "articulation_target_velocity"):
            getattr(px, f"gpu_apply_{{fn}}")()
        px.gpu_update_articulation_kinematics()
        for fn in ("rigid_dynamic_data", "articulation_link_pose", "articulation_qpos", "articulation_qvel",
                   "articulation_target_qpos", "articulation_target_qvel"):
            getattr(px, f"gpu_fetch_{{fn}}")()

    @seq.reset
    def reset(self, worlds: list[int], tasks: list[str], seeds: list[int]) -> list:
        """Each world starts its task at its seed from the state {name}'s CPU reset left; each one's first
        observation."""
        import torch

        px, st = self.px, self.st
        rbd = px.cuda_rigid_body_data.torch()
        q, qv = px.cuda_articulation_qpos.torch(), px.cuda_articulation_qvel.torch()
        tq, tv = px.cuda_articulation_target_qpos.torch(), px.cuda_articulation_target_qvel.torch()
        f = lambda a: torch.as_tensor(np.asarray(a), dtype=rbd.dtype, device=self.dev)  # noqa: E731
        for w, task, seed in zip(worlds, tasks, seeds):
            e = self.group["episodes"].index(self.index[(task, int(seed))])      # its row in states.npz
            rbd[self.body_idx[w], :7], rbd[self.body_idx[w], 7:] = f(st["body_pose"][e]), f(st["body_vel"][e])
            for a, d in enumerate(self.group["art_dof"]):
                rbd[self.root_idx[w, a], :7], rbd[self.root_idx[w, a], 7:] = f(st["art_root"][e, a]), 0
                row = self.art_idx[w, a]
                q[row, :d], qv[row, :d] = f(st["art_qpos"][e, a, :d]), f(st["art_qvel"][e, a, :d])
                tq[row, :d], tv[row, :d] = f(st["art_target_q"][e, a, :d]), f(st["art_target_v"][e, a, :d])
            self.episode[w] = e
        self._apply()
        return self.observe(worlds)

    def observe(self, worlds: list[int]) -> list[dict]:
        """TODO: what a policy reads: px.sync_poses_gpu_to_cpu() brings the poses back to the sub-scenes' entities, for
        their cameras and your own state readout."""
        raise NotImplementedError

    def success(self, worlds: list[int]) -> list[bool]:
        """TODO: {name}'s success on the poses after the step (px.sync_poses_gpu_to_cpu(), then its own check)."""
        raise NotImplementedError

    @seq.step
    @seq.concurrent(sizes=[{worlds}])
    def step(self, worlds: list[int], actions: list) -> list:
        """TODO: an action's drive targets at each physics step, written to cuda_articulation_target_qpos / _qvel at
        self.art_idx rows, applied, then px.step() self.substeps times; then each world's (observation, done,
        success): [(obs, ok, ok) for obs, ok in zip(self.observe(worlds), self.success(worlds))]."""
        raise NotImplementedError
'''

_README = '''# {name}-gpu

{name} on SAPIEN's GPU pipeline, scaffolded from its scene bundle (`scene/`, exported with SAPIEN {sapien}):
structure {key}, {nconds} episode(s), {nbodies} dynamic bodies, articulations {arts}. `benchmark.py` is vectorized: one
call of its step plays every world it is handed, up to {worlds} (`@seq.concurrent(sizes=[{worlds}])`).

What check-model found: {findings}

Fill in the TODOs in `benchmark.py` (the world's scene code, an action's targets, the observation, the success), then
register it and run an eval of it beside one of the CPU version, on the same tasks and seeds (`seq eval run`).
'''


def scaffold_sapien(scene: str, out: str, *, worlds: int = 64, structure: str | None = None,
                    check: dict | None = None, force: bool = False) -> dict[str, Any]:
    """Write out/benchmark.py, out/README.md and out/scene/ for one structure of a SAPIEN scene bundle (one GPU system
    runs one structure's episodes): a vectorized benchmark whose step plays up to `worlds` worlds a call. Returns what
    was written."""
    import re
    import shutil

    from seq.port.scaffold import declared

    with open(os.path.join(scene, "manifest.json")) as f:
        man = json.load(f)
    groups = man["structures"]
    if structure is None:
        if len(groups) > 1:
            listing = ", ".join(f"{g['key']} ({len(g['episodes'])} episodes)" for g in groups)
            raise PortError(f"the scene holds {len(groups)} structures ({listing}): a GPU system's worlds share theirs, "
                            "so one GPU benchmark runs one; scaffold each with --model KEY")
        g = groups[0]
    else:
        g = next((x for x in groups if x["key"] == structure), None)
        if g is None:
            raise PortError(f"no structure {structure!r} in the scene: {', '.join(x['key'] for x in groups)}")
    episodes = [man["episodes"][i] for i in g["episodes"]]
    bench = man["benchmark"]
    tasks, seeds, max_seconds = declared(bench, episodes)
    cls = re.sub(r"\W|^(?=\d)", "_", bench["name"].title().replace("-", "").replace("_", "")) or "Ported"
    findings = "nothing" if not check else "; ".join(
        u for s in check["structures"] if s["key"] == g["key"] for u in s["unsupported"] + s["notes"]) or "nothing"
    fill = {"name": bench["name"], "sapien": man["sapien_version"], "key": g["key"], "nconds": len(episodes),
            "worlds": int(worlds), "tasks": repr(tasks), "seeds": repr(seeds), "max_seconds": repr(max_seconds),
            "cls": cls,
            "bodies": ", ".join(g["bodies"]) or "none", "arts": ", ".join(a or "(unnamed)" for a in g["articulations"])
            or "none"}
    os.makedirs(out, exist_ok=True)
    write_new(os.path.join(out, "benchmark.py"), _TEMPLATE.format(**fill), force=force)
    write_new(os.path.join(out, "README.md"), _README.format(**fill, nbodies=len(g["bodies"]), findings=findings),
              force=force)
    dst = os.path.join(out, "scene")
    if os.path.abspath(dst) != os.path.abspath(scene):
        shutil.copytree(scene, dst, dirs_exist_ok=True)
    return {"out": out, "model": g["key"], "worlds": int(worlds), "per_world": ["body_pose", "art_qpos"],
            "episodes": len(episodes)}
