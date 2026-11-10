"""samples: `run.samples`, one producer's RL samples on a run; `attach_producer`, a producer process joining the
run (RL plan §4); `ProxySidecar`, the rollout proxy as a process of its own (`probe samples proxy`). DESIGN.md.
Names load on first use: the sample contract costs about 80 ms to import, and a run that never logs a sample
should not pay it."""

from __future__ import annotations

import importlib
from typing import Any

_HOMES = {
    "CommandRefused": ".live",
    "Phase": ".phases",
    "ProxySidecar": ".live.proxy",
    "RunSamples": ".samples",
    "attach_producer": ".producer",
    "generated_by": ".refs",
    "parse_generated_by": ".refs",
}
__all__ = sorted(_HOMES)


def __getattr__(name: str) -> Any:
    home = _HOMES.get(name)
    if home is None:
        raise AttributeError(name)
    return getattr(importlib.import_module(home, __name__), name)
