"""Event-driven current feasibility for every model/worker pair.

Static model_worker_quants verdicts price each placement. This projector applies
the wrapper's live-room rules to those DB cells and writes only changed answers
to pair_live. The Fit Station calls the same evaluator with faux room changes;
it never inserts faux residents into the live tables.
"""
from __future__ import annotations

import logging
import threading

from fitevict.estimate import sizing

from hugpy_core.models import modeldb
from hugpy_core.registry import registry

logger = logging.getLogger("hugpy_core.gpu_live")
_cond = threading.Condition()
_pending = set()
_started = False
_answers = {}
_rows = {}
_dirty = set()


def _n(value):
    return max(0, int(value or 0))


def room(worker_name):
    """The wrapper's evictable room, from its mirrored GPU/host/resident rows."""
    with modeldb._conn() as conn:
        cards = conn.execute("SELECT usable,used,processes,hugpy_pids,probe_pids FROM gpu_state WHERE worker=%s",
                             (worker_name,)).fetchall()
        host = conn.execute("SELECT mem_available,swap_free,hugpy_ram FROM host_state WHERE worker=%s",
                            (worker_name,)).fetchone()
        cpu_row = conn.execute("SELECT free_cores,obtainable_cores FROM cpu_state WHERE worker=%s",
                               (worker_name,)).fetchone()
        residents = conn.execute("SELECT r.pid,m.user_settings FROM residents r LEFT JOIN model_workers m "
                                 "ON m.model_key=r.key AND m.worker_id=%s WHERE r.worker=%s AND r.pid IS NOT NULL",
                                 ((registry.lookup_worker(worker_name) or {}).get("id"), worker_name)).fetchall()
    static = {str(r["pid"]) for r in residents if (r.get("user_settings") or {}).get("residency") == "static"}
    gpu = sum(max(0, sizing.room_gpu({"usable": _n(card["usable"]), "used": _n(card["used"]),
                                       "processes": card["processes"] or {}},
                                      set(card["hugpy_pids"] or []), static,
                                      set(card["probe_pids"] or []), 0)) for card in cards)
    ram = sizing.room_ram(_n(host["mem_available"]), host["hugpy_ram"] or {}, static) if host else 0
    cores = (cpu_row or {}).get("obtainable_cores")
    if cores is None:
        cores = (cpu_row or {}).get("free_cores")
    return {"gpu": gpu, "ram": max(0, ram), "swap": _n(host["swap_free"]) if host else 0,
            "cpu": _n(cores)}


def _pairs(worker_id):
    with modeldb._conn() as conn:
        pairs = conn.execute("SELECT model_key,plan,user_settings FROM model_workers WHERE worker_id=%s",
                             (worker_id,)).fetchall()
        verdicts = conn.execute("SELECT model_key,file,memory,auto FROM model_worker_quants WHERE worker_id=%s",
                                (worker_id,)).fetchall()
    by_key = {}
    for row in verdicts:
        by_key.setdefault(row["model_key"], []).append(row)
    return [{**pair, "verdicts": by_key.get(pair["model_key"], [])} for pair in pairs]


def _candidates(pair):
    files = {v["file"]: v for v in pair["verdicts"]}
    settings = pair.get("user_settings") or {}
    default = (pair.get("plan") or {}).get("default_variant")
    preferred = settings.get("gguf_file") or default
    source = files.get(preferred) or next(iter(files.values()), None)
    if not source:
        return []
    pinned = settings.get("alloc_mode")
    if pinned and pinned not in ("auto", "automatic"):
        return [(source, pinned, None)]
    ladder = (source.get("auto") or {}).get("ladder") or []
    result = []
    for rung in ladder:
        # Availability was priced against a past swap/CPU snapshot. Presence
        # is structural; judge() decides current feasibility from live room.
        if not rung.get("present", True):
            continue
        mode = rung.get("mode")
        file = rung.get("variant") if mode == "quant-variant" else source["file"]
        if mode == "quant-variant":
            mode = "gpu-only"
        elif mode == "bnb_4bit":
            mode = "4bit:gpu-only"
        if file in files and mode:
            result.append((files[file], mode, rung))
    if not result:
        mode = ((source.get("auto") or {}).get("standard") or {}).get("mode") or "gpu-only"
        result = [(source, mode, None)]
    return result


def _cell(verdict, mode):
    memory = verdict.get("memory") or {}
    if mode.startswith("4bit:"):
        return (memory.get("bnb_4bit") or {}).get(mode[5:])
    return memory.get(mode)


def judge(cell, room, rung=None):
    """Use the wrapper's host-fit rule; no independent browser fit verdict."""
    if not isinstance(cell, dict) or cell.get("gpu_bytes") is None or cell.get("ram_bytes") is None:
        return None, None, "unpriced"
    if cell.get("supported") is False or cell.get("applicable") is False:
        return False, False, "placement unsupported"
    gpu_fit = _n(cell["gpu_bytes"]) <= room["gpu"]
    anon = max(0, _n(cell["ram_bytes"]) - _n(cell.get("weights_ram")))
    ram_fit, _ = sizing.host_fit({"ram": cell["ram_bytes"], "ram_anon": anon,
                                  "ram_file": cell.get("weights_ram") or 0}, room["ram"], room["swap"])
    cpu_fit = not (rung and rung.get("cpu") and _n(rung.get("cores_required")) > room["cpu"])
    reason = None if gpu_fit and ram_fit and cpu_fit else (
        "insufficient live GPU room" if not gpu_fit else "insufficient live RAM and swap room" if not ram_fit
        else "insufficient obtainable CPU cores")
    return gpu_fit, ram_fit, reason


def evaluate(pairs, current_room, own=None):
    """One current answer per pair, plus every variant/mode for the station."""
    answers, variants = {}, {}
    for pair in pairs:
        key = pair["model_key"]
        room_for_pair = {name: current_room[name] + (own or {}).get(key, {}).get(name, 0)
                         for name in current_room}
        chosen = None
        modes = {}
        for verdict in pair["verdicts"]:
            cells = verdict.get("memory") or {}
            ladder = (verdict.get("auto") or {}).get("ladder") or []
            indexed = {}
            for mode, cell in cells.items():
                if mode == "bnb_4bit":
                    continue
                rung = next((entry for entry in ladder if entry.get("mode") == mode), None)
                g, r, why = judge(cell, room_for_pair, rung)
                indexed[mode] = {"gpu_fit": g, "ram_fit": r, "why": why,
                                 "fits": g is True and r is True and why is None,
                                 "gpuRoom": room_for_pair["gpu"], "hostRoom": room_for_pair["ram"] + room_for_pair["swap"],
                                 "cpuRoom": room_for_pair["cpu"]}
            for mode, cell in (cells.get("bnb_4bit") or {}).items():
                g, r, why = judge(cell, room_for_pair)
                indexed[f"4bit:{mode}"] = {"gpu_fit": g, "ram_fit": r, "why": why,
                                             "fits": g is True and r is True and why is None,
                                             "gpuRoom": room_for_pair["gpu"], "hostRoom": room_for_pair["ram"] + room_for_pair["swap"],
                                             "cpuRoom": room_for_pair["cpu"]}
            modes[verdict["file"]] = indexed
        for verdict, mode, rung in _candidates(pair):
            cell = _cell(verdict, mode)
            gpu_fit, ram_fit, why = judge(cell, room_for_pair, rung)
            candidate = {"worker_id": None, "model_key": key, "file": verdict["file"], "mode": mode,
                         "gpu_fit": gpu_fit, "ram_fit": ram_fit,
                         "gpu_bytes": cell.get("gpu_bytes") if isinstance(cell, dict) else None,
                         "ram_bytes": cell.get("ram_bytes") if isinstance(cell, dict) else None,
                         "room_gpu": room_for_pair["gpu"], "room_ram": room_for_pair["ram"],
                         "room_swap": room_for_pair["swap"], "why": why, "source": "live-room"}
            if chosen is None:
                chosen = candidate
            if gpu_fit and ram_fit and why is None:
                chosen = candidate
                break
        answers[key] = chosen or {"worker_id": None, "model_key": key, "file": None, "mode": None,
                                  "gpu_fit": None, "ram_fit": None, "gpu_bytes": None, "ram_bytes": None,
                                  "room_gpu": room_for_pair["gpu"], "room_ram": room_for_pair["ram"],
                                  "room_swap": room_for_pair["swap"], "why": "unpriced", "source": "live-room"}
        variants[key] = modes
    return answers, variants


def project(worker_name, faux=None):
    worker = registry.lookup_worker(worker_name)
    if not worker:
        raise ValueError("Unknown worker")
    wid = worker["id"]
    with _cond:
        if wid in _dirty or wid not in _rows:
            _rows[wid] = _pairs(wid)
            _dirty.discard(wid)
        pairs = _rows[wid]
    current = room(worker_name)
    own = {}
    for item in faux or []:
        key = item.get("key")
        pair = next((p for p in pairs if p["model_key"] == key), None)
        if not pair:
            continue
        file = item.get("file") or (pair.get("plan") or {}).get("default_variant")
        verdict = next((v for v in pair["verdicts"] if v["file"] == file), None)
        mode = item.get("mode") or ((((verdict or {}).get("auto") or {}).get("standard") or {}).get("mode")) or "gpu-only"
        cell = _cell(verdict or {}, mode)
        if not isinstance(cell, dict):
            continue
        gpu_use = min(current["gpu"], _n(cell.get("gpu_bytes")))
        current["gpu"] -= gpu_use
        anon = max(0, _n(cell.get("ram_bytes")) - _n(cell.get("weights_ram")))
        used_ram = min(current["ram"], anon)
        current["ram"] -= used_ram
        swap_use = min(current["swap"], max(0, anon - used_ram))
        current["swap"] -= swap_use
        own[key] = {"gpu": gpu_use, "ram": used_ram, "swap": swap_use, "cpu": 0}
    answers, variants = evaluate(pairs, current, own)
    return {"worker_id": wid, "room": current, "pairs": answers, "variants": variants}


def refresh(worker_name):
    """Live feasibility comes from the wrapper; project() is for simulations."""
    from hugpy_core.brain import planner
    planner.replan(worker_name)
    return 0


def invalidate(worker_id):
    with _cond:
        _dirty.add(worker_id)


def schedule(worker_name, *, pair_change=False):
    from hugpy_core.brain import planner
    worker = registry.lookup_worker(worker_name)
    if worker:
        planner.maybe_refresh(worker)
