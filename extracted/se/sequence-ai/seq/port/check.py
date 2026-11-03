"""
`seq port check-model`: does the GPU engine's MuJoCo compile an exported scene into the same physics, and can the
GPU engine run it ?

In one sentence: every model of the bundle is compiled again with the MuJoCo installed here (the GPU engine's) → each
field the export recorded is compared with what this compile gives, object by object (mesh geoms by the box their
vertices span, since versions pick different mesh frames) → options that came out different say the same MJCF means
something else in this version (MULTICCD, ccd_iterations: LIBERO met both) → the model is handed to the GPU engine
(mujoco_warp.put_model, on the CPU: no card needed), which refuses what it cannot run in its own words → any finding
of the three kinds fails the check.

WHY tolerances and not equality: two MuJoCo versions compile the same inertia through different float paths; LIBERO's
port saw differences below 3e-8 m that change nothing. A real error (a wrong mass, a lost compiler option) is orders
of magnitude above them.
"""
from __future__ import annotations

import json
import os
from typing import Any

import numpy as np

from seq.port.mujoco import MESH_FRAME_FIELDS, OPT_FIELDS, REF_FIELDS, PortError, _mujoco, quiet_warp, reference

ENGINES = ("mujoco-warp", "sapien-gpu")
MUJOCO_ENGINES = ("mujoco-warp",)
RTOL, ATOL = 1e-6, 1e-7



INERTIA_RTOL = 1e-4

_KIND = {"body": "body", "jnt": "joint", "geom": "geom", "actuator": "actuator", "cam": "camera", "light": "light"}

_PIN = {"ccd_iterations": '<option ccd_iterations="{was}"/>', "ccd_tolerance": '<option ccd_tolerance="{was}"/>',
        "iterations": '<option iterations="{was}"/>', "ls_iterations": '<option ls_iterations="{was}"/>',
        "tolerance": '<option tolerance="{was}"/>', "impratio": '<option impratio="{was}"/>'}


def _load(scene: str) -> tuple[dict, dict]:
    try:
        with open(os.path.join(scene, "manifest.json")) as f:
            manifest = json.load(f)
    except FileNotFoundError:
        raise PortError(f"{scene} is not a scene bundle (no manifest.json): make one with seq port export") \
            from None
    if manifest.get("engine") != "mujoco":
        raise PortError(f"{scene} was exported from {manifest.get('engine')!r}; check-model --engine mujoco-warp "
                        "takes a MuJoCo scene")

    try:
        with np.load(os.path.join(scene, "reference.npz"), allow_pickle=False) as z:
            return manifest, {k: z[k] for k in z.files}
    except ValueError:
        raise PortError(f"{scene}/reference.npz holds an array only a pickle reads, which check-model does not read: "
                        "export the scene again with seq port export") from None


def _inertia_tensors(inertia: np.ndarray, iquat: np.ndarray) -> np.ndarray:
    """Each body's inertia in its own frame, R diag(I) R^T with R from the inertia frame's (w, x, y, z) quaternion."""
    w, x, y, z = (np.asarray(iquat, dtype=np.float64)[:, i] for i in range(4))
    rot = np.stack([1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y),
                    2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x),
                    2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)], axis=1).reshape(-1, 3, 3)
    return rot @ (np.asarray(inertia, dtype=np.float64)[:, :, None] * rot.transpose(0, 2, 1))


def _compare_inertia(was: dict[str, np.ndarray], now: dict[str, np.ndarray]) -> dict | None:
    """body_inertia and body_iquat compared as the one thing they describe, each body's inertia tensor in its own
    frame. Apart they flag noise: a body whose principal moments are (nearly) equal has no preferred principal axes,
    and two MuJoCo versions pick different ones (RoboCasa's stove knobs and handles: iquat off by 3e-7, the tensor
    the same). The tolerance is relative to the body's largest moment (INERTIA_RTOL)."""
    a, b = np.asarray(was.get("body_inertia")), np.asarray(now.get("body_inertia"))
    qa, qb = np.asarray(was.get("body_iquat")), np.asarray(now.get("body_iquat"))
    if a.shape != b.shape or qa.shape != qb.shape:
        return {"field": "body_inertia", "what": f"{a.shape[0] if a.ndim else a} → {b.shape[0] if b.ndim else b} "
                                                 "entries", "objects": []}
    ta, tb = _inertia_tensors(a, qa), _inertia_tensors(b, qb)
    scale = np.maximum(np.abs(a).max(1, initial=0.0), np.abs(b).max(1, initial=0.0))
    bad = np.flatnonzero(np.abs(ta - tb).reshape(len(ta), -1).max(1) > INERTIA_RTOL * scale + 1e-12)
    if not len(bad):
        return None
    names = was.get("names.body")
    objects = [{"name": str(names[i]) if names is not None and i < len(names) else f"#{i}",
                "was": np.round(a[i], 9).tolist(), "now": np.round(b[i], 9).tolist()} for i in bad[:8]]
    return {"field": "body_inertia", "what": f"{len(bad)} differ (the inertia tensor in the body's frame)",
            "objects": objects}


def compare_reference(was: dict[str, np.ndarray], now: dict[str, np.ndarray]) -> list[dict]:
    """Every field of REF_FIELDS that differs beyond tolerance, with the objects it differs on."""
    found: list[dict] = []
    inertia = _compare_inertia(was, now)
    if inertia is not None:
        found.append(inertia)
    mesh = ~np.isnan(was["mesh_aabb"][:, 0]) if "mesh_aabb" in was else None
    for f in (*REF_FIELDS, "mesh_aabb"):
        if f in ("body_inertia", "body_iquat"):
            continue
        a, b = np.asarray(was.get(f)), np.asarray(now.get(f))
        if a.shape != b.shape:
            found.append({"field": f, "what": f"{a.shape[0] if a.ndim else a} → {b.shape[0] if b.ndim else b} "
                                              "entries", "objects": []})
            continue
        if f in MESH_FRAME_FIELDS and mesh is not None and a.shape[:1] == mesh.shape:
            a, b, rows = a[~mesh], b[~mesh], np.flatnonzero(~mesh)
        else:
            rows = np.arange(a.shape[0]) if a.ndim else None
        if a.dtype.kind in "fc":
            close = np.isclose(a, b, rtol=RTOL, atol=ATOL, equal_nan=True)
        else:
            close = a == b


        bad = ~close if close.ndim <= 1 else ~close.all(axis=tuple(range(1, close.ndim)))
        if not np.any(bad):
            continue
        idx = rows[np.flatnonzero(bad)] if rows is not None else []
        kind = _KIND.get(f.split("_")[0], "geom" if f == "mesh_aabb" else None)
        names = was.get(f"names.{kind}") if kind else None
        objects = []
        for i in list(idx)[:8]:
            label = str(names[i]) if names is not None and i < len(names) else f"#{i}"
            ai, bi = np.asarray(was[f])[i], np.asarray(now[f])[i]
            objects.append({"name": label, "was": np.round(ai, 9).tolist(), "now": np.round(bi, 9).tolist()})
        found.append({"field": f, "what": f"{int(np.sum(bad))} differ", "objects": objects})
    return found


def compare_options(was: dict[str, np.ndarray], now: dict[str, np.ndarray]) -> list[dict]:
    """The options that came out different: the same MJCF means something else in this MuJoCo."""
    out = []
    for f in OPT_FIELDS:
        if f in ("enableflags", "disableflags"):
            continue
        a, b = np.asarray(was.get(f"opt.{f}")), np.asarray(now.get(f"opt.{f}"))
        if a.shape == b.shape and np.allclose(a, b, rtol=RTOL, atol=0, equal_nan=True):
            continue
        item = {"option": f, "was": a.tolist(), "now": b.tolist()}
        if f in _PIN:
            item["fix"] = _PIN[f].format(was=a.item() if a.ndim == 0 else a.tolist())
        out.append(item)

    for key in sorted(k for k in was if k.startswith("flag.") and k in now):
        a, b = int(was[key]), int(now[key])
        if a != b:
            name = key[len("flag."):]
            out.append({"option": f"flag {name}", "was": "on" if a else "off", "now": "on" if b else "off",
                        "fix": f'<option><flag {name.lower()}="{"enable" if a else "disable"}"/></option>'})
    return out


def engine_support(m: Any, engine: str) -> list[str]:
    """What the GPU engine refuses in this model, in its own words (empty: it runs it)."""
    if engine not in MUJOCO_ENGINES:
        raise PortError(f"--engine is one of {', '.join(MUJOCO_ENGINES)} for a MuJoCo scene (sapien-gpu takes a "
                        "SAPIEN one)")
    try:
        import warp as wp

        quiet_warp(wp)
        import mujoco_warp as mjw
    except ImportError as exc:
        raise PortError('check-model --engine mujoco-warp needs MuJoCo Warp: pip install "sequence-ai[port]" (the '
                        "versions these commands are tested with), or mujoco-warp at the version your GPU benchmark "
                        "will use") from exc
    try:
        with wp.ScopedDevice("cpu"):
            mjw.put_model(m)
    except NotImplementedError as exc:
        return [str(exc)]
    except Exception as exc:
        return [f"{type(exc).__name__}: {exc}"]
    return []


def check_model(scene: str, engine: str = "mujoco-warp") -> dict:
    """Check every model of the scene bundle against this MuJoCo and the GPU engine. Returns the report; its "ok" is
    False when anything differs or is unsupported. A SAPIEN bundle goes to seq.port.sapien.check_sapien."""
    if engine == "sapien-gpu":
        from seq.port.sapien import check_sapien

        return check_sapien(scene, engine)
    if engine not in ENGINES:
        raise PortError(f"--engine {engine}: the engines are {', '.join(ENGINES)}")
    mujoco = _mujoco()
    manifest, ref = _load(scene)
    report: dict[str, Any] = {"engine": engine, "mujoco": mujoco.__version__,
                              "exported_with_mujoco": manifest["mujoco_version"], "models": [], "ok": True}
    for entry in manifest["models"]:
        key = entry["key"]
        m = mujoco.MjModel.from_xml_path(os.path.join(scene, entry["xml"]))
        was = {f[len(key) + 1:]: ref[f] for f in ref if f.startswith(f"{key}.")}
        now = reference(m)
        item = {"key": key, "episodes": entry["episodes"], "compile": compare_reference(was, now),
                "options": compare_options(was, now), "unsupported": engine_support(m, engine)}
        item["ok"] = not (item["compile"] or item["options"] or item["unsupported"])
        report["ok"] &= item["ok"]
        report["models"].append(item)
    return report


def lines(report: dict) -> list[str]:
    """The report as the CLI prints it: one block per model, every finding with its fix."""
    if report["engine"] == "sapien-gpu":
        from seq.port.sapien import lines as sapien_lines

        return sapien_lines(report)
    out = [f"check-model: {report['engine']}, MuJoCo {report['mujoco']} (exported with MuJoCo "
           f"{report['exported_with_mujoco']})"]
    for item in report["models"]:
        out.append(f"model {item['key']} ({item['episodes']} episode(s)): "
                   + ("same physics, supported" if item["ok"] else "FAILS"))
        for c in item["compile"]:
            out.append(f"  compile  {c['field']}: {c['what']}")
            for o in c["objects"]:
                out.append(f"           {o['name']}: {o['was']} → {o['now']}")
        for o in item["options"]:
            out.append(f"  option   {o['option']}: {o['was']} → {o['now']}" + (f"  ({o['flags']})" if "flags" in o
                                                                              else ""))
            if o.get("fix"):
                out.append(f"           keep the original: {o['fix']}")
        for u in item["unsupported"]:
            out.append(f"  engine   {u}")
    out.append("ok" if report["ok"] else "not ok: fix the findings above before porting (exit 1)")
    return out
