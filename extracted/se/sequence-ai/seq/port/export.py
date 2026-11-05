"""
`seq port export`: a CPU MuJoCo or SAPIEN benchmark's scenes as a self-contained bundle for its GPU port
. A SAPIEN benchmark's bundle is described in seq.port.sapien; what follows is the MuJoCo one.

In one sentence: the benchmark is built as an eval's machine builds it after the snapshot - its constructor, init=
filled with no policy evaluated, as at a registration check → for each episode (a task at a seed) its own reset starts
it, exactly as an eval does → the MuJoCo model inside the benchmark is written out once per structure (with every file
it reads) and proved by compiling the copy again in this MuJoCo → the episode's start is kept: qpos, qvel, act, mocap
and whatever differs in its model (what reset changed after compiling, or the other numbers its own MJCF compiled to) →
scene/ holds the MJCF files, the assets, those starts and what this MuJoCo compiled, for `check-model` to hold a GPU
engine's compile against.

WHY the benchmark's own reset and not a re-implementation: the starts a GPU port must reproduce are the ones this
benchmark's evals start from (LIBERO's cabinet and stove are placed by its reset, per seed); calling it is the only way
to get them without rewriting the benchmark.

Layout of scene/:
  manifest.json           what was exported: engine and MuJoCo version, the benchmark (its tasks and time limit), its
                          models and episodes
  models/<key>.xml        one MJCF per structure, its files rewritten to ../assets/; an episode that compiled the
                          same structure with other numbers (robosuite's Lift draws the cube's size per episode)
                          is kept as those numbers per episode, its MJCF's hash under the model's "merged"
  assets/                 every mesh / texture / height field the MJCFs read
  states.npz              per model key: <key>.qpos (n, nq), .qvel, .act, .mocap_pos, .mocap_quat, .time, .ncon, .nefc,
                          and for each model field that differs between the episodes (reset changed it after
                          compiling, or the episode's own compile made it other numbers): <key>.model.<field>.rows,
                          the entries (first axis) some episode sets differently, and <key>.model.<field>
                          (n, len(rows), ...), every episode's values of them. Bundle 1 kept every entry and no
                          .rows; Lift's 363,667-row bvh_aabb, one row of which the cube changes, made it 17 MB an
                          episode
  reference.npz           per model key: <key>.<field> as this MuJoCo compiled the MJCF (seq.port.mujoco.reference)
  rollout.npz             per model key: <key>.ctrl (n, steps, nu) float32 and <key>.qpos (n, steps, nq) - each
                          episode run from its start on this MuJoCo under compare's seeded controls, which
                          `seq port compare` holds the engines to (manifest "rollout": its steps and seed)
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from typing import Any, Callable, NamedTuple

import numpy as np

from seq.port.motion import ROLLOUT, ROLLOUT_SEED, STEPS, rollout
from seq.port.mujoco import (SAVED_RTOL, STATE_FIELDS, PortError, _mujoco, find_model, model_diff, physics_signature,
                             reference, rewrite_assets, same_structure, with_xml)



BUNDLE_VERSION = 3


class Episode(NamedTuple):
    """One episode an export starts: a task at a seed, as an eval's @seq.reset is handed them."""

    task: str
    seed: int


def _select(reg: Any, trials: int | None, tasks: list[str] | None) -> list[Episode]:
    """The episodes to export: each task at each of the benchmark's seeds, or at its first `trials`, of `tasks` only."""
    unknown = [t for t in tasks or [] if t not in reg.tasks]
    if unknown:
        raise PortError(f"--tasks {unknown[0]}: not a task of {reg.name} ({', '.join(reg.tasks)})")
    seeds = list(reg.seeds)[:trials] if trials is not None else list(reg.seeds)
    out = [Episode(t, int(s)) for t in reg.tasks if not tasks or t in tasks for s in seeds]
    if not out:
        raise PortError("no episode matches the export's --tasks / --trials")
    return out




def export(ref: str, out: str, *, trials: int | None = None, tasks: list[str] | None = None,
           progress: Callable[[str], None] | None = None, rollout_steps: int = STEPS) -> dict:
    """Export `ref` (file.py:Class, or module:Class), a CPU MuJoCo or SAPIEN benchmark stepping one world at a time, to
    the scene bundle `out`. Runs where the benchmark's simulator is installed (its own image, or your machine): its
    constructor with no policy evaluated - init='s "{policy.<field>}" left to its defaults, as at the platform's
    registration check - then its @seq.reset for each episode. A MuJoCo benchmark's episodes are also run
    `rollout_steps` physics steps on this MuJoCo (0: not) for `seq port compare`. Returns the manifest it wrote."""
    from sequence_base.contract.flags import SeqFlags

    from sequence_base.construct import build

    from seq.benchmark_registry import benchmark_registration
    from seq.loading import load_kind
    from seq.named import _folder

    say = progress or (lambda msg: None)
    cls = load_kind(ref, "benchmark")
    reg = benchmark_registration(cls)
    if reg.worlds is not None:
        raise PortError(f"{reg.name} is already vectorized (@seq.concurrent(sizes=[{reg.worlds}]) on its @seq.step); "
                        "export runs a CPU benchmark that steps one world at a time (reset(task, seed))")
    episodes = _select(reg, trials, tasks)
    started = time.monotonic()

    bench = build(cls, reg.constructor, base_dir=_folder(cls)) if reg.constructor is not None else cls()
    reset = getattr(bench, reg.bindings[SeqFlags.RESET])
    if _engine_of(bench, reset, episodes[0]) == "sapien":
        from seq.port.sapien import export_sapien

        manifest = export_sapien(reg, bench, reset, episodes, out, say)
        manifest["time_s"] = round(time.monotonic() - started, 1)
        with open(os.path.join(out, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=1)
        return manifest
    mujoco = _mujoco()
    os.makedirs(os.path.join(out, "models"), exist_ok=True)
    models: dict[str, dict[str, Any]] = {}
    merged: dict[str, str] = {}
    rows: list[tuple[str, dict[str, np.ndarray]]] = []
    for i, ep in enumerate(episodes):
        reset(ep.task, ep.seed)
        found = find_model(bench)
        with_xml(found, bench)
        m = found.model
        sha = hashlib.sha1(found.xml.encode()).hexdigest()[:12]
        if sha in models:
            key, own = sha, models[sha]["compiled"]
        else:
            xml, nfiles = rewrite_assets(found.xml, out)
            path = os.path.join(out, "models", f"{sha}.xml")
            with open(path, "w") as f:
                f.write(xml)
            own = mujoco.MjModel.from_xml_path(path)


            key = merged.get(sha) or next((k for k, info in models.items()
                                           if same_structure(own, info["compiled"])), None)
            if key is None:
                key = sha
                models[key] = {"compiled": own, "source": found.source, "path": found.path, "files": nfiles,
                               "episodes": [], "merged": []}
                say(f"model {key}: {found.source} at {found.path}, {nfiles} file(s)")
            else:
                os.remove(path)
                if sha not in merged:
                    merged[sha] = key
                    models[key]["merged"].append(sha)
                    say(f"model {sha}: {key} with other numbers "
                        f"({', '.join(model_diff(own, models[key]['compiled']))}), kept per episode")



        saved = found.source == "mj_saveLastXML"
        lost = [f for f in model_diff(m, own, rtol=SAVED_RTOL if saved else 0.0) if f not in STATE_FIELDS]
        if lost:
            dropped = (", or the save dropped them (mujoco 3.2.3's mj_saveLastXML drops <compiler inertiagrouprange>)"
                       if saved and mujoco.__version__ == "3.2.3" else "")
            raise PortError(f"the exported MJCF does not reproduce the model reset() built ({found.source}): "
                            f"{', '.join(lost)} differ. The simulator changed them after compiling{dropped}")


        changed = model_diff(m, models[key]["compiled"])
        row = len(models[key]["episodes"])
        d = found.data if found.data is not None else _data_of(bench, m)
        state = {"qpos": np.array(d.qpos), "qvel": np.array(d.qvel), "act": np.array(d.act),
                 "mocap_pos": np.array(d.mocap_pos), "mocap_quat": np.array(d.mocap_quat),
                 "time": np.array(d.time), "ncon": np.array(d.ncon), "nefc": np.array(d.nefc)}
        base = models[key]["compiled"]
        state.update({f"model.{f}": _rows_apart(np.array(getattr(m, f)), np.array(getattr(base, f)))
                      for f in changed})
        if rollout_steps > 0:

            state["rollout.ctrl"], state["rollout.qpos"] = rollout(mujoco, m, state, rollout_steps,
                                                                   ROLLOUT_SEED + row)
        models[key]["episodes"].append(i)
        rows.append((key, state))
        if (i + 1) % 25 == 0 or i + 1 == len(episodes):
            say(f"{i + 1}/{len(episodes)} episode(s) exported")
    manifest = _write(out, reg, episodes, models, rows)
    if rollout_steps > 0:
        manifest["rollout"] = {"file": ROLLOUT, "steps": int(rollout_steps), "seed": ROLLOUT_SEED,
                               "controls": "uniform within each actuator's ctrlrange, a draw a physics step, float32"}
    manifest["time_s"] = round(time.monotonic() - started, 1)
    with open(os.path.join(out, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    return manifest


def _engine_of(bench: Any, reset: Any, episode: Episode) -> str:
    """Which simulator the benchmark holds: MuJoCo (a model among its attributes) or SAPIEN (a sapien.Scene), after one
    reset of the first episode."""
    reset(episode.task, episode.seed)
    try:
        find_model(bench)
        return "mujoco"
    except (PortError, ImportError):
        pass
    try:
        from seq.port.sapien import find_scene

        find_scene(bench)
        return "sapien"
    except (PortError, ImportError):
        pass
    raise PortError("after its reset the benchmark holds neither a MuJoCo model nor a sapien.Scene: export ports "
                    "MuJoCo and SAPIEN benchmarks")


def _sdk_version() -> str:
    """This SDK's version, as pip installed it (the seq module carries none)."""
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version("sequence-ai")
    except PackageNotFoundError:
        return "?"


def _data_of(bench: Any, m: Any) -> Any:
    """The MjData beside a model found without one: searched like the model (seq.port.mujoco.find_model)."""
    mujoco = _mujoco()
    queue, seen = [bench], set()
    for _ in range(6):
        nxt = []
        for obj in queue:
            if obj is None or id(obj) in seen:
                continue
            seen.add(id(obj))
            for cand in (obj, getattr(obj, "data", None), getattr(getattr(obj, "data", None), "_data", None),
                         getattr(getattr(obj, "data", None), "ptr", None)):
                if isinstance(cand, mujoco.MjData) and cand.qpos.shape[0] == m.nq:
                    return cand
            nxt += [v for v in (vars(obj).values() if hasattr(obj, "__dict__") else ())
                    if v is not None and not isinstance(v, (str, bytes, int, float, bool, list, tuple, dict))]
            nxt += [getattr(obj, n, None) for n in ("sim", "physics", "unwrapped", "env", "_env")]
        queue = nxt
    raise PortError("found the MuJoCo model but not its MjData beside it")


def _rows_apart(a: np.ndarray, base: np.ndarray) -> tuple[np.ndarray | None, np.ndarray]:
    """The rows (entries of the first axis) where an episode's field differs from its model's, and its values there;
    a scalar whole."""
    if not a.ndim:
        return None, a
    apart = a != base
    if a.dtype.kind in "fc":
        apart &= ~(np.isnan(a) & np.isnan(base))
    idx = np.flatnonzero(apart.any(axis=tuple(range(1, a.ndim))))
    return idx, a[idx]


def _write(out: str, reg: Any, episodes: list[Episode], models: dict, rows: list) -> dict:
    """states.npz, reference.npz and the manifest (returned) for what export collected."""
    mujoco = _mujoco()
    states: dict[str, np.ndarray] = {}
    refs: dict[str, np.ndarray] = {}
    entries, where = [], {}
    for key, info in models.items():
        mine = [rows[i][1] for i in info["episodes"]]
        rec = info["compiled"]
        fields = sorted({f for s in mine for f in s if f.startswith("model.")})
        for f in ("qpos", "qvel", "act", "mocap_pos", "mocap_quat", "time", "ncon", "nefc"):
            states[f"{key}.{f}"] = np.stack([s[f] for s in mine])
        varying = {}
        for f in fields:
            base = np.array(getattr(rec, f[len("model."):]))
            if not base.ndim:
                states[f"{key}.{f}"] = np.stack([s[f][1] if f in s else base for s in mine])
                varying[f[len("model."):]] = None
                continue


            at = np.unique(np.concatenate([s[f][0] for s in mine if f in s]))
            values = np.repeat(base[at][None], len(mine), axis=0)
            for r, s in enumerate(mine):
                if f in s:
                    values[r, np.searchsorted(at, s[f][0])] = s[f][1]
            states[f"{key}.{f}"], states[f"{key}.{f}.rows"] = values, at
            varying[f[len("model."):]] = np.isin(np.arange(base.shape[0]), at)
        for f, arr in reference(rec).items():
            refs[f"{key}.{f}"] = arr
        for r, i in enumerate(info["episodes"]):
            where[i] = (key, r)
        cams = [mujoco.mj_id2name(rec, mujoco.mjtObj.mjOBJ_CAMERA, k) for k in range(rec.ncam)]
        entries.append({"key": key, "xml": f"models/{key}.xml", "source": info["source"], "found_at": info["path"],
                        "files": info["files"], "episodes": len(info["episodes"]),
                        "physics": physics_signature(rec, {f: v for f, v in varying.items() if v is not None}),
                        "sizes": {n: int(getattr(rec, n)) for n in ("nq", "nv", "nu", "na", "nbody", "ngeom",
                                                                    "nmocap", "ncam")},
                        "cameras": cams, "timestep": float(rec.opt.timestep),

                        "contacts_at_start": int(max(int(s["ncon"]) for s in mine)),
                        "constraints_at_start": int(max(int(s["nefc"]) for s in mine)),

                        "changed_by_reset": {f: int(v.sum()) for f, v in varying.items() if v is not None},
                        "merged": info["merged"]})
    np.savez_compressed(os.path.join(out, "states.npz"), **states)
    np.savez_compressed(os.path.join(out, "reference.npz"), **refs)
    runs = {f"{key}.{f}": np.stack([rows[i][1][f"rollout.{f}"] for i in info["episodes"]])
            for key, info in models.items() for f in ("ctrl", "qpos")
            if all(f"rollout.{f}" in rows[i][1] for i in info["episodes"])}
    if runs:
        np.savez_compressed(os.path.join(out, ROLLOUT), **runs)

    return {"bundle": BUNDLE_VERSION, "engine": "mujoco", "mujoco_version": mujoco.__version__,
            "exported_with": f"sequence-ai {_sdk_version()}",
            "benchmark": benchmark_entry(reg),
            "models": entries,
            "episodes": [{"index": i, "task": ep.task, "seed": ep.seed, "model": where[i][0], "row": where[i][1]}
                         for i, ep in enumerate(episodes)]}


def benchmark_entry(reg: Any) -> dict:
    """What a bundle says of the benchmark it came from: its name and class, its tasks ({name: description}) and how
    long an episode may run - what its GPU port declares the same (seq port scaffold copies them)."""
    limit = reg.max_seconds
    return {"name": reg.name, "handler_ref": reg.handler_ref, "tasks": dict(reg.tasks),
            "max_seconds": dict(limit) if isinstance(limit, dict) else float(limit)}
