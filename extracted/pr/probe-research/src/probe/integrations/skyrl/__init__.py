"""SkyRL on Probe (RL plan §6.3): launch with `trainer.override_entrypoint=probe.integrations.skyrl.entrypoint`,
or run `ProbeExp(cfg)` yourself. DESIGN.md. Names that import SkyRL load on first use."""

from __future__ import annotations

import importlib
from typing import Any

from .runs import get_rewind_step, read_resume_step

_HOMES = {"ProbeExp": ".skyrl", "ProbeTracking": ".skyrl", "main": ".entrypoint"}
__all__ = ["ProbeExp", "ProbeTracking", "get_rewind_step", "main", "read_resume_step"]


def __getattr__(name: str) -> Any:
    home = _HOMES.get(name)
    if home is None:
        raise AttributeError(name)
    return getattr(importlib.import_module(home, __name__), name)
