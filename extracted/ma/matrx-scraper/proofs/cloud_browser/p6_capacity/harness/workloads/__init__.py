"""Workload registry — PLAN.md's six workloads, in PLAN.md's order.

Nothing may be added here that PLAN.md does not name. A seventh workload is a plan
change, which goes to DECISIONS.md, not into this file.
"""

from __future__ import annotations

from .browser import HeavyApp, IdleTab, NavigationWork, RestoreStartStorm
from .streaming import InteractiveStream, SandboxPlusStream, TurnRelayedStream


def all_workloads() -> list:
    return [
        IdleTab(),  # PLAN workload 1
        NavigationWork(),  # PLAN workload 2
        HeavyApp(),  # PLAN workload 3
        InteractiveStream(hardware=False),  # PLAN workload 4 (x264)
        InteractiveStream(hardware=True),  # PLAN workload 4 (hardware encoding)
        SandboxPlusStream(),  # PLAN workload 5
        RestoreStartStorm(),  # PLAN workload 6 (storm half)
        TurnRelayedStream(),  # PLAN workload 6 (TURN half)
    ]


def by_id(workload_id: str):
    for workload in all_workloads():
        if workload.id == workload_id:
            return workload
    raise KeyError(workload_id)


__all__ = ["all_workloads", "by_id"]
