"""
`seq port compare`: does the GPU engine move a scene the way the CPU benchmark's MuJoCo does, step by
step?

In one sentence: each episode of the scene bundle starts where the CPU benchmark's reset started it (the bundle's
states) → one control sequence (uniform within each actuator's range, from a seed) drives MuJoCo on the reference
scene and the GPU engine (MuJoCo Warp, on this machine's CPU when it has no card) on the port's scene, each running on
from its own last step → after every step their joint positions are compared → the report names, per episode, the
first step where a joint is further apart than the tolerance, the joint and its body, and the furthest apart it got.

WHY each side runs on and is not reset to the reference every step: one 2 ms step moves a joint by ½·Δa·dt², so a body
whose mass is wrong is ~1e-6 rad off after one step, inside the engines' own float differences; run on, the gap grows
with the square of the time and stands out within a few hundred steps, while the two engines on the same physics stay
within the tolerance.

WHY the export's own MuJoCo too: check-model compares what two MuJoCo versions compile and the options they read,
and the reference runs this machine's MuJoCo, so a version that steps the same model differently (robosuite Lift's
cube lands 1.2 mm apart on MuJoCo 3.3.1 and 3.15) is seen by neither. `seq port export` records each episode
under these controls on the benchmark's own MuJoCo (rollout.npz); when the bundle has that record, the reference is
held to it as well, and a difference there that MuJoCo Warp shares is the MuJoCo version, not the port.

WHY the GPU engine runs here and not on a card: MuJoCo Warp runs its kernels on the CPU too (check-model already
compiles with it there), and what is compared is the physics, not the speed.
"""
from __future__ import annotations

import json
import os
from typing import Any

import numpy as np

from seq.port.mujoco import PortError, _mujoco, quiet_warp





STEPS = 200
ATOL = 1e-3
EPISODES = 3
_STATE = ("qpos", "qvel", "act", "mocap_pos", "mocap_quat")

ROLLOUT, ROLLOUT_SEED = "rollout.npz", 0
_COMPONENTS = {0: ("x", "y", "z", "qw", "qx", "qy", "qz"), 1: ("qw", "qx", "qy", "qz")}


def _bundle(scene: str) -> tuple[dict, Any]:
    try:
        with open(os.path.join(scene, "manifest.json")) as f:
            manifest = json.load(f)
    except FileNotFoundError:
        raise PortError(f"{scene} is not a scene bundle (no manifest.json): make one with seq port export") \
            from None
    if manifest.get("engine") != "mujoco":
        raise PortError(f"{scene} was exported from {manifest.get('engine')!r}; compare takes a MuJoCo scene")
    return manifest, np.load(os.path.join(scene, "states.npz"))


def _model(mujoco: Any, scene: str, manifest: dict, key: str) -> Any:
    entry = next((e for e in manifest["models"] if e["key"] == key), None)
    if entry is None:
        raise PortError(f"{scene} has no model {key!r}: the port's scene must come from the same export")
    return mujoco.MjModel.from_xml_path(os.path.join(scene, entry["xml"]))


def _start(mujoco: Any, m: Any, states: Any, key: str, row: int) -> Any:
    """An episode's start, as the scaffold's reset writes it: the model fields it changes, then the state."""
    d = mujoco.MjData(m)
    for k in states.files:
        if not k.startswith(key + ".") or k.endswith(".rows"):
            continue
        name, value = k[len(key) + 1:], states[k][row]
        if name.startswith("model."):
            field = getattr(m, name[len("model."):])
            if k + ".rows" in states.files:
                field[states[k + ".rows"]] = value
            else:
                field[...] = value
        elif name in _STATE and np.size(value):
            getattr(d, name)[...] = value
        elif name == "time":
            d.time = float(value)
    mujoco.mj_forward(m, d)
    return d


def _apply_pins(mujoco: Any, m: Any, pins: dict) -> None:
    """The options check-model found this MuJoCo reads differently from the export's, set back to the original's - as
    the scaffold's setup pins them (_pin there) - so both engines run the CPU benchmark's physics."""
    for name, value in pins.items():
        if name != "flags":
            setattr(m.opt, name, value)
            continue
        for flag, how in value.items():
            disable = hasattr(mujoco.mjtDisableBit, f"mjDSBL_{flag.upper()}")
            enum, prefix, field = ((mujoco.mjtDisableBit, "mjDSBL_", "disableflags") if disable
                                   else (mujoco.mjtEnableBit, "mjENBL_", "enableflags"))
            bit = int(getattr(enum, prefix + flag.upper()))
            on = (how == "enable") != disable
            setattr(m.opt, field, (getattr(m.opt, field) | bit) if on else (getattr(m.opt, field) & ~bit))


def _joint_of(m: Any) -> np.ndarray:
    """For each qpos index, the joint it belongs to."""
    widths = {0: 7, 1: 4, 2: 1, 3: 1}
    out = np.zeros(m.nq, dtype=np.int64)
    for j in range(m.njnt):
        a = int(m.jnt_qposadr[j])
        out[a:a + widths[int(m.jnt_type[j])]] = j
    return out


def _name(mujoco: Any, m: Any, kind: Any, i: int, what: str) -> str:
    return mujoco.mj_id2name(m, kind, int(i)) or f"{what} {int(i)}"


def _controls(m: Any, steps: int, seed: int) -> np.ndarray:
    """One control per actuator per step, uniform within its range (or [-1, 1] when it has none)."""
    lo = np.where(m.actuator_ctrllimited, m.actuator_ctrlrange[:, 0], -1.0)
    hi = np.where(m.actuator_ctrllimited, m.actuator_ctrlrange[:, 1], 1.0)
    return np.random.default_rng(seed).uniform(lo, hi, size=(steps, m.nu))


def rollout(mujoco: Any, m: Any, state: dict, steps: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """What `seq port export` records of its own MuJoCo: from an episode's start (set as _start sets it),
    `steps` physics steps under the seeded controls, rounded to float32 as MuJoCo Warp takes them. Returns the
    controls (steps, nu) and qpos after each step (steps, nq)."""
    d = mujoco.MjData(m)
    for name in _STATE:
        value = state.get(name)
        if value is not None and np.size(value):
            getattr(d, name)[...] = value
    d.time = float(state.get("time", 0.0))
    mujoco.mj_forward(m, d)
    u = _controls(m, steps, seed).astype(np.float32)
    q = np.empty((steps, m.nq))
    for t in range(steps):
        d.ctrl[:] = u[t]
        mujoco.mj_step(m, d)
        q[t] = d.qpos
    return u, q


def _apart(mujoco: Any, m: Any, joint: np.ndarray, i: int, t: int, gap: float, **values: float) -> dict:
    """Where two runs are first further apart than the tolerance: the step, the joint (and which of a free or ball
    joint's numbers), its body, both values."""
    j = int(joint[i])
    names = _COMPONENTS.get(int(m.jnt_type[j]), ())
    k = i - int(m.jnt_qposadr[j])
    return {"step": t + 1, "time_s": round((t + 1) * float(m.opt.timestep), 4),
            "joint": _name(mujoco, m, mujoco.mjtObj.mjOBJ_JOINT, j, "joint"),
            "component": names[k] if k < len(names) else None,
            "body": _name(mujoco, m, mujoco.mjtObj.mjOBJ_BODY, m.jnt_bodyid[j], "body"), "qpos_index": i,
            **{name: float(v) for name, v in values.items()}, "gap": float(gap)}


def _record(scene: str, manifest: dict) -> tuple[Any, dict]:
    """The export's record of its own MuJoCo (rollout.npz) and what it says of it, or (None, {}) for a bundle
    without one (exported before sequence-ai 0.33.57, or with --rollout-steps 0)."""
    info = manifest.get("rollout") or {}
    path = os.path.join(scene, info.get("file") or ROLLOUT)
    return (np.load(path), info) if info and os.path.exists(path) else (None, {})


def compare(reference: str, port: str | None = None, *, engine: str = "mujoco-warp", steps: int = STEPS,
            atol: float = ATOL, episodes: int = EPISODES, seed: int = 0) -> dict:
    """`seq port compare`: the same controls on the reference scene (MuJoCo) and the port's scene (the GPU engine; the
    reference's own when no port is named), the bundle's first `episodes`. Returns the report; its "ok" is False when
    any episode diverged. Named as
    its command is - replay before 0.37.17, a word an eval's 3D replay holds.
"""
    if engine != "mujoco-warp":
        raise PortError("compare runs MuJoCo Warp (--engine mujoco-warp); a SAPIEN port is compared by evals")
    mujoco = _mujoco()
    try:
        import warp as wp

        quiet_warp(wp)
        import mujoco_warp as mjw
    except ImportError as exc:
        raise PortError('compare needs MuJoCo Warp: pip install "sequence-ai[port]" (the versions these '
                        "commands are tested with), or mujoco-warp at the version your GPU benchmark uses") from exc
    from seq.port.check import check_model
    from seq.port.scaffold import _pins

    port = port or reference
    ref_manifest, ref_states = _bundle(reference)

    check = check_model(reference, engine=engine)
    port_manifest, port_states = _bundle(port)
    device = "cuda" if wp.get_cuda_device_count() else "cpu"
    record, record_info = _record(reference, ref_manifest)
    if record is not None and seed != record_info.get("seed", ROLLOUT_SEED):
        record = None
    out = []
    for c in ref_manifest["episodes"][:max(1, episodes)]:
        key, row = c["model"], int(c["row"])
        m_ref = _model(mujoco, reference, ref_manifest, key)
        m_port = _model(mujoco, port, port_manifest, key)
        if (m_ref.nq, m_ref.nu) != (m_port.nq, m_port.nu):
            raise PortError(f"model {key}: the port's has {m_port.nq} joint positions and {m_port.nu} actuators, the "
                            f"reference's {m_ref.nq} and {m_ref.nu} - not the same scene")
        pins = _pins(check, key)
        _apply_pins(mujoco, m_ref, pins)
        _apply_pins(mujoco, m_port, pins)
        d_ref = _start(mujoco, m_ref, ref_states, key, row)
        d_port = _start(mujoco, m_port, port_states, key, row)
        u = _controls(m_ref, steps, seed + row).astype(np.float32)
        rec = None
        if record is not None and f"{key}.qpos" in record.files:
            rec = record[f"{key}.qpos"][row][:steps]
            u[:len(rec)] = record[f"{key}.ctrl"][row][:len(rec)]
        joint = _joint_of(m_ref)
        worst, first = 0.0, None
        v_worst, v_first, o_worst = 0.0, None, 0.0
        with wp.ScopedDevice(device):
            mw, dw = mjw.put_model(m_port), mjw.put_data(m_port, d_port)
            for t in range(steps):
                d_ref.ctrl[:] = u[t]
                mujoco.mj_step(m_ref, d_ref)
                dw.ctrl.assign(u[t][None].astype(np.float32))
                mjw.step(mw, dw)
                q_port = dw.qpos.numpy()[0].astype(np.float64)
                gap = np.abs(q_port - d_ref.qpos)
                i = int(np.argmax(gap)) if gap.size else 0
                worst = max(worst, float(gap[i]) if gap.size else 0.0)
                if first is None and gap.size and gap[i] > atol:
                    first = _apart(mujoco, m_ref, joint, i, t, gap[i], reference=d_ref.qpos[i], port=q_port[i])
                if rec is not None and t < len(rec) and gap.size:

                    v_gap = np.abs(d_ref.qpos - rec[t])
                    k = int(np.argmax(v_gap))
                    v_worst, o_worst = max(v_worst, float(v_gap[k])), max(o_worst, float(np.abs(q_port - rec[t]).max()))
                    if v_first is None and v_gap[k] > atol:
                        v_first = _apart(mujoco, m_ref, joint, k, t, v_gap[k], original=rec[t][k], this=d_ref.qpos[k])
        item = {"task": c.get("task"), "seed": c.get("seed"), "model": key, "steps": steps, "pins": pins,
                "max_gap": worst, "diverged": first}
        if rec is not None:
            item["original"] = {"steps": len(rec), "max_gap": v_worst, "diverged": v_first, "port_max_gap": o_worst}
        out.append(item)
    original = None
    if record is not None:
        original = {"mujoco": ref_manifest.get("mujoco_version"), "this": mujoco.__version__,
                    "steps": record_info.get("steps"), "seed": record_info.get("seed", ROLLOUT_SEED),
                    "apart": sum(1 for r in out if (r.get("original") or {}).get("diverged"))}
    elif record_info:
        original = {"mujoco": ref_manifest.get("mujoco_version"), "this": mujoco.__version__,
                    "seed": record_info.get("seed", ROLLOUT_SEED), "apart": None}
    return {"ok": all(r["diverged"] is None for r in out), "reference": reference, "port": port, "engine": engine,
            "device": device, "atol": atol, "seed": seed, "original": original, "episodes": out}


def lines(report: dict) -> list[str]:
    """The report as `seq port compare` prints it."""
    head = (f"compare: {report['reference']} on MuJoCo against "
            f"{report['port'] if report['port'] != report['reference'] else 'the same scene'} on MuJoCo Warp "
            f"({report['device']}), tolerance {report['atol']:g}")
    o = report.get("original") or {}
    was, this = f"MuJoCo {o.get('mujoco')}", f"MuJoCo {o.get('this')}"
    rows = []
    if o and o.get("apart") is None:
        rows.append(f"  (the export recorded its {was} under --seed {o.get('seed')}: nothing of it to compare with "
                    f"--seed {report['seed']})")
    for r in report["episodes"]:
        what = f"{r['task']} seed {r['seed']}"
        d = r["diverged"]
        if d is None:
            rows.append(f"  {what}: within tolerance for {r['steps']} steps (furthest {r['max_gap']:.2e})")
        else:
            rows.append(f"  {what}: diverged at step {d['step']} ({d['time_s']} s): {_where(d)} - "
                        f"{d['reference']:.6f} on MuJoCo, {d['port']:.6f} on MuJoCo Warp ({d['gap']:.2e} apart)")
        ro = r.get("original")
        if ro is None:
            continue
        v = ro["diverged"]
        if v is None:
            rows.append(f"    {this} against the export's {was}: within tolerance for {ro['steps']} steps "
                        f"(furthest {ro['max_gap']:.2e})")
        else:
            rows.append(f"    {this} against the export's {was}: apart at step {v['step']} ({v['time_s']} s): "
                        f"{_where(v)} - {v['original']:.6f} on {o.get('mujoco')}, {v['this']:.6f} on {o.get('this')} "
                        f"({v['gap']:.2e}; furthest {ro['max_gap']:.2e}, MuJoCo Warp's {ro['port_max_gap']:.2e})")
    n, apart = len(report["episodes"]), o.get("apart")
    if not report["ok"]:
        verdict = "they move differently: check-model the port's scene"
    elif apart and o.get("mujoco") == o.get("this"):
        verdict = (f"MuJoCo Warp moves as this MuJoCo does, but this MuJoCo, the export's own version, moves apart from "
                   f"the export's record on {apart} of {n} episode(s): the bundle does not reproduce its starts")
    elif apart:
        first = min(r["original"]["diverged"]["step"] for r in report["episodes"]
                    if (r.get("original") or {}).get("diverged"))
        furthest = max(r["original"]["max_gap"] for r in report["episodes"] if r.get("original"))
        verdict = (f"MuJoCo Warp moves as {this} does; {this} moves apart from the export's {was} on {apart} of {n} "
                   f"episode(s), from step {first}, {furthest:.2e} at the furthest: the MuJoCo version, not the port")
    elif apart == 0:
        verdict = f"the same motion, on MuJoCo Warp, {this} and the export's {was}"
    else:
        verdict = "the same motion"
    return [head, *rows, f"verdict: {verdict}"]


def _where(d: dict) -> str:
    part = f" ({d['component']})" if d.get("component") else ""
    return f"joint {d['joint']}{part} of body {d['body']}"
