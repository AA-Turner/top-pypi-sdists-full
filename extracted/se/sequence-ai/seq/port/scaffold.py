"""
`seq port scaffold`: a vectorized GPU benchmark's skeleton, written from an exported scene
.

In one sentence: the scene bundle says what the CPU benchmark built (its MJCF, every episode's start, what reset changed
per episode, its tasks, time limit and options) → the skeleton's constructor builds as many MuJoCo Warp worlds as an
eval runs (init='s "{num_worlds}", at most its @seq.concurrent size), sets the fields reset changed per world, pins the
options check-model found changed, captures one control step - 1 / policy.hz seconds of physics - as a CUDA graph and
writes each episode's start into its world → what only the benchmark knows (its controller, its observation, its
success) is left as marked functions, with the CPU benchmark's behaviour as the yardstick that `seq port compare` holds
its motion to.

WHY the skeleton runs without CUDA too: with no card the graphs are not captured and the same functions are called
directly, so a port can be smoke-tested on any machine before it is registered on one.
"""
from __future__ import annotations

import json
import os
import shutil
from typing import Any

import numpy as np

from seq.port.mujoco import PortError, write_new

_TEMPLATE = '''"""
{name}-gpu — the GPU version of `{name}`, scaffolded by `seq port scaffold` from its exported scene.
Each world is one MuJoCo Warp world on the card: its constructor builds as many as an eval runs, at most {worlds}.

Done: the scene (scene/, exported from {name} with MuJoCo {exported_mujoco}), the worlds, a control step - the physics
substeps of 1 / policy.hz seconds - captured as one CUDA graph, each episode's start written into its world, and the
fields that differ between the CPU benchmark's episodes ({per_world_text}) set per world.{shared_doc}
Yours (search for TODO): the controller, the observation and the success — then `seq port compare scene/` holds this
version's motion to `{name}`'s from the same starts.
"""
# No `from __future__ import annotations`: a kernel built inside a function (Warp is imported there, not at import, as
# _static_geom_pose does) has its annotations evaluated against only the names its own body uses, so a matrix type
# of the enclosing function in a signature would not resolve.
import json
import os

import numpy as np

import seq

{scene_line}
MODEL = "{key}"                                         # the scene's model this benchmark runs
# What MuJoCo {exported_mujoco} did and MuJoCo Warp's MuJoCo does differently (seq port check-model): each pin
# keeps the original. Drop one to take the new default — LIBERO's port kept NATIVECCD on, since MuJoCo Warp's own
# box-box routine threw a bowl off the cabinet.
PINS = {pins}
PER_WORLD = {per_world}                                 # model fields every world holds its own copy of
# Contacts and constraint rows one world may hold: 4x the busiest start the CPU benchmark exported ({contacts} contacts,
# {constraints} rows), at least LIBERO's 256 / 1024. MuJoCo Warp warns "overflow" when an episode needs more.
NCONMAX, NJMAX = {nconmax}, {njmax}


@seq.benchmark(
    name="{name}-gpu",
    gpu="L4",
{image_lines}
    # TODO: the same as {name} (copied from the scene's episodes; a seed the export did not run has no start)
    tasks={tasks},
    seeds={seeds},
    max_seconds={max_seconds},
    # built after the machine's snapshot: how many worlds this eval runs, and the evaluated policy's control rate
    init={{"worlds": "{{num_worlds}}", "hz": "{{policy.hz}}"}},
)
class {cls}:
    def __init__(self, worlds: int, hz=None) -> None:
        import mujoco
        import mujoco_warp as mjw
        import warp as wp

        self.wp, self.mjw, self.n = wp, mjw, worlds
        with open(os.path.join(SCENE, "manifest.json")) as f:
            man = json.load(f)
        entry = next(e for e in man["models"] if e["key"] == MODEL)
        mjm = mujoco.MjModel.from_xml_path(os.path.join(SCENE, entry["xml"]))
        _pin(mujoco, mjm, PINS)
        self.mjm = mjm
        # physics substeps per control step: a step plays 1 / hz seconds, as the robot does; at registration no policy
        # is evaluated (hz is None) and nothing steps: one substep, enough to compile the step's kernels
        self.substeps = max(1, int(round(1.0 / (float(hz) * mjm.opt.timestep)))) if hz else 1
        states = np.load(os.path.join(SCENE, "states.npz"))
        self.start = {{k[len(MODEL) + 1:]: states[k] for k in states.files if k.startswith(MODEL + ".")}}
        self.row = {{(e["task"], int(e["seed"])): e["row"] for e in man["episodes"] if e["model"] == MODEL}}
        self.m = mjw.put_model(mjm, batch_sizes={{f: worlds for f in PER_WORLD}})
        self.d = mjw.make_data(mjm, nworld=worlds, nconmax=NCONMAX, njmax=NJMAX)
        self.action = wp.zeros((worlds, max(1, mjm.nu)), dtype=float)
        # Geoms welded to the world are placed once for every world alike; a body reset moves per world needs its
        # geoms placed again after each reset (_static_geom_pose).
        moved = set()
        for f in ("body_pos", "body_quat"):
            rows = self.start.get(f"model.{{f}}")
            if rows is not None:           # bodies some episode starts away from where the MJCF puts them
                at = self.start.get(f"model.{{f}}.rows", np.arange(rows.shape[1]))
                off = np.any(rows != np.asarray(getattr(mjm, f))[at][None], axis=tuple(range(2, rows.ndim)))
                moved |= set(np.asarray(at)[off.any(0)].tolist())
        static = [g for g in range(mjm.ngeom) if mjm.body_weldid[mjm.geom_bodyid[g]] == 0
                  and _under(mjm, int(mjm.geom_bodyid[g]), moved)]
        self.static = wp.array(np.array(static or [0], np.int32), dtype=int) if static else None
        self._graphs()
        # every world gets a real scene before anything runs: idle worlds still collide every substep
        task, seed = next(iter(self.row))
        self.reset(list(range(worlds)), [task] * worlds, [seed] * worlds)

    def _graphs(self) -> None:
        wp, mjw, m, d = self.wp, self.mjw, self.m, self.d

        def refresh():                     # poses from qpos (+ the moved welded geoms), then what forward() derives
            mjw.kinematics(m, d)
            if self.static is not None:
                wp.launch(_static_geom_pose(), dim=(self.n, self.static.shape[0]),
                          inputs=[self.static, m.geom_bodyid, m.geom_pos, m.geom_quat, d.xpos, d.xquat],
                          outputs=[d.geom_xpos, d.geom_xmat])
            mjw.forward(m, d)

        def control_step():
            for i in range(self.substeps):
                mjw.step1(m, d)
                self.controller(i)
                mjw.step2(m, d)

        self._fns = {{"refresh": refresh, "step": control_step}}
        self._graph = {{}}
        if wp.get_device().is_cuda:        # on a card: each captured once, replayed as one launch
            for name, fn in self._fns.items():
                fn()                       # the first run compiles the kernels outside the capture
                with wp.ScopedCapture() as cap:
                    fn()
                self._graph[name] = cap.graph

    def _launch(self, name: str) -> None:
        if name in self._graph:
            self.wp.capture_launch(self._graph[name])
        else:
            self._fns[name]()

    def controller(self, substep: int) -> None:
        """TODO: turn self.action (one row per world, as the policy's adapter hands it) into self.d.ctrl, the way the
        CPU benchmark's controller does in each physics substep — robosuite's OSC, for example
        (robosuite/controllers/osc.py in robosuite 1.4), as a kernel. As written, an action is the actuators' ctrl."""
        if self.mjm.nu:
            self.wp.copy(self.d.ctrl, self.action)

    @seq.reset
    def reset(self, worlds: list[int], tasks: list[str], seeds: list[int]) -> list:
        """Each world starts its task at its seed where the CPU benchmark's reset started it (the scene's states);
        returns each one's first observation."""
        try:
            rows = np.array([self.row[(task, int(seed))] for task, seed in zip(tasks, seeds)])
        except KeyError as exc:
            raise ValueError(f"episode {{exc.args[0]}} has no start in the scene: export it (seq port export, "
                             "every episode or --trials N that reaches its seed)") from None
        s = np.asarray(worlds, dtype=np.int64)
        d, m = self.d, self.m
        for name in ("qpos", "qvel", "act", "time"):
            if self.start[name].size:
                _put(getattr(d, name), s, self.start[name][rows])
        for name in ("qacc_warmstart", "ctrl"):
            _put(getattr(d, name), s, 0.0)
        for f in PER_WORLD:
            _put(getattr(m, f), s, self.start[f"model.{{f}}"][rows], self.start.get(f"model.{{f}}.rows"))
        self._launch("refresh")
        return self.observe(worlds)

    def observe(self, worlds: list[int]) -> list[dict]:
        """TODO: what the CPU benchmark's environment returns as its observation (cameras: mujoco_warp's renderer, or
        the CPU benchmark's own renderer for pixel parity as LIBERO's port does). As written: the joint positions."""
        qpos = self.d.qpos.numpy()[np.asarray(worlds, dtype=np.int64)]
        return [{{"qpos": q}} for q in qpos]

    def success(self, worlds: list[int]) -> list[bool]:
        """TODO: the CPU benchmark's success, from each world's state. As written: never."""
        return [False for _ in worlds]

    @seq.step
    @seq.concurrent(sizes=[{worlds}])
    def step(self, worlds: list[int], actions: list) -> list:
        """One action for each world it is handed; each world's (observation, done, success) after it - done once it
        succeeded, as written."""
        a = self.action.numpy()
        a[np.asarray(worlds, dtype=np.int64)] = np.asarray(actions, dtype=np.float32).reshape(len(worlds), -1)
        self.action.assign(a)
        self._launch("step")
        won = self.success(worlds)
        return [(obs, ok, ok) for obs, ok in zip(self.observe(worlds), won)]


def _put(arr, slots, rows, at=None) -> None:
    """Write each slot's row into its world; `at`: the entries of the field the rows hold (the scene keeps only the ones
    some episode sets differently), else all of them."""
    a = arr.numpy()
    # MuJoCo Warp may lay a field out in its own shape (geom_aabb: MuJoCo's 6 numbers a geom, its 2 x vec3)
    if at is None:
        a[slots] = np.reshape(rows, a[slots].shape) if np.ndim(rows) else rows
    else:
        where = np.ix_(slots, np.asarray(at))
        a[where] = np.reshape(rows, a[where].shape)
    arr.assign(a)


def _under(mjm, b: int, moved: set) -> bool:
    while b:
        if b in moved:
            return True
        b = int(mjm.body_parentid[b])
    return False


def _pin(mujoco, mjm, pins: dict) -> None:
    for name, value in pins.items():
        if name == "flags":
            for flag, how in value.items():
                enum = mujoco.mjtDisableBit if hasattr(mujoco.mjtDisableBit, f"mjDSBL_{{flag.upper()}}") \\
                    else mujoco.mjtEnableBit
                bit = int(getattr(enum, ("mjDSBL_" if enum is mujoco.mjtDisableBit else "mjENBL_") + flag.upper()))
                field = "disableflags" if enum is mujoco.mjtDisableBit else "enableflags"
                on = (how == "enable") != (enum is mujoco.mjtDisableBit)
                setattr(mjm.opt, field, (getattr(mjm.opt, field) | bit) if on else (getattr(mjm.opt, field) & ~bit))
        else:
            setattr(mjm.opt, name, value)


_KERNEL = None


def _static_geom_pose():
    """Place geoms welded to the world from their body's per-world pose (MuJoCo Warp places them once for all)."""
    global _KERNEL
    if _KERNEL is None:
        import warp as wp
        from mujoco_warp._src import math as mjmath

        @wp.kernel(enable_backward=False)
        def kernel(geoms: wp.array(dtype=int), geom_bodyid: wp.array(dtype=int),
                   geom_pos: wp.array2d(dtype=wp.vec3), geom_quat: wp.array2d(dtype=wp.quat),
                   xpos: wp.array2d(dtype=wp.vec3), xquat: wp.array2d(dtype=wp.quat),
                   geom_xpos: wp.array2d(dtype=wp.vec3), geom_xmat: wp.array2d(dtype=wp.mat33)):
            w, k = wp.tid()
            g = geoms[k]
            b = geom_bodyid[g]
            geom_xpos[w, g] = xpos[w, b] + mjmath.rot_vec_quat(geom_pos[w % geom_pos.shape[0], g], xquat[w, b])
            geom_xmat[w, g] = mjmath.quat_to_mat(mjmath.mul_quat(xquat[w, b], geom_quat[w % geom_quat.shape[0], g]))

        _KERNEL = kernel
    return _KERNEL
'''

_README = """# {name}-gpu

The GPU version of `{name}`, scaffolded by `seq port scaffold` from `scene/` (exported from {name} with MuJoCo
{exported_mujoco}). `benchmark.py` is vectorized: one call of its step plays every world it is handed, each a MuJoCo
Warp world, up to {worlds} (`@seq.concurrent(sizes=[{worlds}])`).

## What is done

- `scene/` (copied here): the MJCF `{name}` compiled ({nfiles} file(s) under `scene/assets/`), and every exported
  episode's start ({nconds} episode(s)).{scene_readme}
- A control step of 1 / policy.hz seconds: its physics substeps worked out in its constructor from the evaluated
  policy's hz, init='s `"{{policy.hz}}"` (one at registration, where no policy is evaluated and nothing steps),
  captured as one CUDA graph on a card.
- Per world: {per_world_text}.{shared_readme}
- Options pinned to MuJoCo {exported_mujoco}'s behaviour: {pins_text}.

## What is yours (TODO in benchmark.py)

1. `controller()` — the CPU benchmark's controller, per physics substep, as a kernel (robosuite's OSC, for example:
   `robosuite/controllers/osc.py` in robosuite 1.4).
2. `observe()` — the CPU benchmark's observation (its cameras: MuJoCo Warp's renderer, or its own for pixel parity).
3. `success()` — its success, from each world's state.
4. `tasks=`, `seeds=` and `max_seconds=`: the same as `{name}`.

Then: `seq port compare scene/` runs the same controls on MuJoCo and MuJoCo Warp from each start and
names the first step where they drift apart.
"""


def _identifier(name: str) -> str:
    parts = [p for p in "".join(ch if ch.isalnum() else " " for ch in name).split() if p]
    out = "".join(p[:1].upper() + p[1:] for p in parts) or "Benchmark"
    return (out if out[0].isalpha() else f"B{out}") + "Gpu"


def scaffold(scene: str, out: str, *, engine: str = "mujoco-warp", worlds: int = 64, model: str | None = None,
             check: dict | None = None, force: bool = False) -> dict:
    """Write out/benchmark.py, out/README.md and out/scene/ for the scene bundle: a vectorized benchmark whose step
    plays up to `worlds` worlds a call (@seq.concurrent(sizes=[worlds])). `check` (seq.port.check_model's report)
    supplies the option pins; without one the skeleton pins nothing. A benchmark.py or README.md already there that
    differs is left as it is unless `force`. Returns what was written."""
    if isinstance(worlds, bool) or not isinstance(worlds, int) or worlds < 1:
        raise PortError(f"--worlds {worlds!r}: the most worlds one step call plays, a whole number from 1")
    if engine == "sapien-gpu":
        from seq.port.sapien import scaffold_sapien

        return scaffold_sapien(scene, out, worlds=worlds, structure=model, check=check, force=force)
    if engine != "mujoco-warp":
        raise PortError(f"--engine {engine}: scaffold writes mujoco-warp and sapien-gpu skeletons")
    with open(os.path.join(scene, "manifest.json")) as f:
        man = json.load(f)
    groups = {}
    for e in man["models"]:
        groups.setdefault(e["physics"], []).append(e)
    if model is None:
        if len(groups) > 1:
            listing = ", ".join(f"{g[0]['key']} ({sum(e['episodes'] for e in g)} episodes)"
                                for g in groups.values())
            raise PortError(f"the scene holds {len(groups)} different physics models ({listing}): one GPU benchmark "
                            "runs one; scaffold each with --model KEY")
        entry = next(iter(groups.values()))[0]
    else:
        entry = next((e for e in man["models"] if e["key"] == model), None)
        if entry is None:
            raise PortError(f"no model {model!r} in the scene: {', '.join(e['key'] for e in man['models'])}")
    bench = man["benchmark"]
    per_world, shared, unused = _per_world(sorted(entry.get("changed_by_reset") or {}))
    pins = _pins(check, entry["key"]) if check else {}
    episodes = [e for e in man["episodes"] if e["model"] == entry["key"]]
    tasks, seeds, max_seconds = declared(bench, episodes)
    import mujoco_warp

    fill = {"name": bench["name"], "exported_mujoco": man["mujoco_version"],
            "key": entry["key"], "pins": repr(pins), "per_world": repr(tuple(per_world)),
            "per_world_text": ", ".join(per_world) or "nothing (no model field differs between episodes)",
            "shared_doc": (f"\nMuJoCo Warp holds one value of {', '.join(shared)} for every world: each world runs "
                           "the value the scene's MJCF compiles to." if shared else ""),
            "shared_readme": (f"\n- One value for every world (MuJoCo Warp holds no per-world copy): "
                              f"{', '.join(shared)}, as the scene's MJCF compiles it." if shared else ""),
            "worlds": int(worlds), "mujoco_warp": _version("mujoco-warp"), "tasks": repr(tasks), "seeds": repr(seeds),
            "max_seconds": repr(max_seconds), "cls": _identifier(bench["name"]),
            "contacts": int(entry.get("contacts_at_start") or 0), "constraints": int(entry.get("constraints_at_start")
                                                                                     or 0)}
    fill["nconmax"] = max(256, 4 * fill["contacts"])
    volume = None if _fits_beside_code(scene) else f"{bench['name']}-scene"
    if volume is None:
        fill.update(scene_line='SCENE = os.environ.get("SEQ_SCENE", "/opt/scene")        # where the image keeps the '
                               'bundle (see image= below)',
                    image_lines=f'    image=(seq.Image.debian_slim(python="3.11")\n'
                                f'           .uv_pip_install("mujoco-warp=={fill["mujoco_warp"]}")\n'
                                f'           .add_local_dir("scene", "/opt/scene")),',
                    scene_readme="")
    else:
        fill.update(scene_line=f"# The scene is past what a deploy ships beside the code: upload it as a volume first\n"
                               f"# (seq volume put --kind dataset {volume} scene/); assets= mounts it at /assets.\n"
                               f'SCENE = os.environ.get("SEQ_SCENE", "/assets")',
                    image_lines=f'    image=seq.Image.debian_slim(python="3.11").uv_pip_install("mujoco-warp=='
                                f'{fill["mujoco_warp"]}"),\n    assets=seq.Volume.from_name("{volume}"),',
                    scene_readme=f"\n  It is past what a deploy ships beside the code: upload it before registering, "
                                 f"`seq volume put --kind dataset {volume} scene/`; the benchmark mounts it at "
                                 "`/assets`.")
    fill["njmax"] = max(1024, 4 * fill["constraints"])
    os.makedirs(out, exist_ok=True)
    write_new(os.path.join(out, "benchmark.py"), _TEMPLATE.format(**fill), force=force)
    write_new(os.path.join(out, "README.md"), _README.format(
        **fill, nfiles=entry["files"], nconds=len(episodes),
        pins_text=", ".join(f"{k}={v}" for k, v in pins.items()) or "none"), force=force)
    dst = os.path.join(out, "scene")
    if os.path.abspath(dst) != os.path.abspath(scene):
        shutil.copytree(scene, dst, dirs_exist_ok=True)
    return {"out": out, "model": entry["key"], "worlds": int(worlds), "per_world": per_world, "shared": shared,
            "unused": unused, "volume": volume, "pins": pins, "episodes": len(episodes)}


def declared(bench: dict, episodes: list[dict]) -> tuple[dict[str, str], list[int], Any]:
    """What a port declares the same as the benchmark it came from, for the episodes it runs: their tasks with the
    benchmark's descriptions ({name: description}), their seeds, and the time limit - one number, or each task's."""
    names = sorted({e["task"] for e in episodes})
    tasks = {t: (bench.get("tasks") or {}).get(t, "") for t in names}
    seeds = sorted({int(e["seed"]) for e in episodes})
    limit = bench.get("max_seconds")
    if isinstance(limit, dict):
        limit = {t: limit[t] for t in names if t in limit}
    return tasks, seeds, limit


def _fits_beside_code(scene: str) -> bool:
    """Whether a deploy can ship the scene beside the benchmark's code (add_local_dir): within seq.code_bundle's limit
    once packed. robosuite Lift's, its Panda meshes as OBJ, packs to 10.5 MB, past the 8 MB."""
    from pathlib import Path

    from seq.code_bundle import _MAX_RAW_BYTES, _pack, _walk
    from seq.errors import PolicyDefinitionError

    files = _walk(Path(scene), "scene")
    if sum(p.stat().st_size for p, _ in files) > _MAX_RAW_BYTES:
        return False
    try:
        _pack(files, "the scene", "")
    except PolicyDefinitionError:
        return False
    return True


def _per_world(fields: list[str]) -> tuple[list[str], list[str], list[str]]:
    """Of the model fields that differ between episodes: the ones MuJoCo Warp holds a copy of per world (its Model's
    arrays declared with a leading world axis), the ones it holds once for every world (dof_length: only sleeping
    reads it), and the ones it does not hold at all (bvh_aabb, dof_M0: it never reads them)."""
    import dataclasses

    import mujoco_warp as mjw

    spec = {f.name: tuple(getattr(f.type, "shape", None) or ()) for f in dataclasses.fields(mjw.Model)}
    batched = [f for f in fields if spec.get(f, ())[:1] == ("*",)]
    return batched, [f for f in fields if f in spec and f not in batched], [f for f in fields if f not in spec]


def _pins(report: dict, key: str) -> dict[str, Any]:
    """The options check-model found changed, as the values that keep the original."""
    item = next((m for m in report.get("models", []) if m["key"] == key), None)
    pins: dict[str, Any] = {}
    for o in (item or {}).get("options", []):
        if o["option"].startswith("flag "):
            pins.setdefault("flags", {})[o["option"][5:].lower()] = "enable" if o["was"] == "on" else "disable"
        else:
            was = o["was"]
            pins[o["option"]] = was if not isinstance(was, list) else np.asarray(was).tolist()
    return pins


def _version(dist: str) -> str:
    from importlib.metadata import version

    return version(dist)
