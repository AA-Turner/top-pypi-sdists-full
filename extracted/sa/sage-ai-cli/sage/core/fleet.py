"""Item #20 — Multi-machine fleet awareness."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["Machine", "Fleet", "load_fleet", "pick_machine_for_model"]


@dataclass
class Machine:
    name: str
    host: str
    ram_gb: float = 0.0
    has_gpu: bool = False


@dataclass
class Fleet:
    machines: list[Machine] = field(default_factory=list)


def _config_path() -> Path:
    return Path.home() / ".sage" / "fleet.json"


def load_fleet() -> Fleet:
    p = _config_path()
    if not p.exists():
        return Fleet()
    try:
        data = json.loads(p.read_text("utf-8"))
    except (json.JSONDecodeError, OSError):
        return Fleet()
    machines: list[Machine] = []
    for m in data.get("machines", []):
        try:
            machines.append(Machine(
                name=m["name"],
                host=m["host"],
                ram_gb=float(m.get("ram_gb", 0)),
                has_gpu=bool(m.get("has_gpu", False)),
            ))
        except (KeyError, ValueError):
            continue
    return Fleet(machines=machines)


def pick_machine_for_model(fleet: Fleet, *,
                            model_size_gb: float) -> Machine | None:
    """Pick the smallest machine that has enough RAM for the model.
    Returns None if no machine has enough RAM."""
    eligible = [m for m in fleet.machines if m.ram_gb >= model_size_gb * 0.8]
    if not eligible:
        return None
    return min(eligible, key=lambda m: m.ram_gb)
