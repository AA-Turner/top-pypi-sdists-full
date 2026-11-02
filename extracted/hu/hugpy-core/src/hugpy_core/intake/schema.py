"""The schema between a wrapper's records and Core's tables.

A wrapper reports in its engine's vocabulary (alloc modes max-gpu / max-ram /
explicit, the old disk_mmap option, verdict cells keyed by those names). Core can
store the canonical placement terms instead (hugpy_resources PLACEMENTS /
PLACEMENT_TERMS), so the database and the console speak one vocabulary and the
console renders from the terms rather than a hand-kept list.

Enabled by HUGPY_PLACEMENT_SCHEMA=canonical (coredev). Otherwise every function passes
its input through unchanged, so a Core without the flag stores what it always did.
Readers stay correct either way through ``cell`` / ``canonical``.
"""
from __future__ import annotations

import os

# Engine / legacy names -> canonical placements. Mirrors hugpy_resources
# PLACEMENT_RENAMES; kept here too so a Core whose resources predate the
# canonical terms still reads both vocabularies.
_RENAMES = {
    "max-gpu": "gpu-max", "max-ram": "ram-max", "explicit": "moe", "moe_split": "moe",
    "spill": "moe", "disk_mmap": "disk_mmap-only", "4-bit": "4bit",
}


def enabled() -> bool:
    return os.environ.get("HUGPY_PLACEMENT_SCHEMA") == "canonical"


def renames() -> dict:
    try:
        from hugpy_resources.imports.constants import PLACEMENT_RENAMES
        return {**_RENAMES, **PLACEMENT_RENAMES}
    except ImportError:
        return dict(_RENAMES)


def canonical(name):
    """The canonical placement for any engine/legacy/canonical name."""
    return renames().get(name, name) if isinstance(name, str) else name


def cell(memory: dict, name: str):
    """A verdict cell by placement, whichever vocabulary the row was stored in."""
    memory = memory or {}
    if name in memory:
        return memory[name]
    want = canonical(name)
    for key, value in memory.items():
        if canonical(key) == want:
            return value
    return None


def memory(cells: dict) -> dict:
    """Verdict cells keyed by canonical placements (the bnb_4bit table too)."""
    if not enabled() or not isinstance(cells, dict):
        return cells
    out = {}
    for key, value in cells.items():
        if key == "bnb_4bit" and isinstance(value, dict):
            out[key] = {canonical(k): v for k, v in value.items()}
        else:
            out[canonical(key)] = value
    return out


def auto(picks: dict) -> dict:
    """Auto's picks per branch with canonical mode names."""
    if not enabled() or not isinstance(picks, dict):
        return picks
    return {branch: (dict(pick, mode=canonical(pick.get("mode"))) if isinstance(pick, dict) else pick)
            for branch, pick in picks.items()}


def settings(knobs: dict) -> dict:
    """Pair or box knobs with a canonical alloc_mode and Auto order."""
    if not enabled() or not isinstance(knobs, dict):
        return knobs
    out = dict(knobs)
    if out.get("alloc_mode"):
        out["alloc_mode"] = canonical(out["alloc_mode"])
    prefs = out.get("auto_preferences")
    if isinstance(prefs, dict) and isinstance(prefs.get("order"), list):
        out["auto_preferences"] = dict(prefs, order=[canonical(o) for o in prefs["order"]])
    return out


def document() -> dict:
    """The schema the console renders from: placements as terms (order, label,
    definition, engines, category), the knob schema, and the accepted renames."""
    from hugpy_resources.imports.constants import KNOB_SCHEMA, PLACEMENT_TERMS, PLACEMENTS
    return {"placements": [{"key": key, **PLACEMENT_TERMS[key]} for key in PLACEMENTS],
            "knobs": KNOB_SCHEMA, "renames": renames(), "canonical": enabled()}
