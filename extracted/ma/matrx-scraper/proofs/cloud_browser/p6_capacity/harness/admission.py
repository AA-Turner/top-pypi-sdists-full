"""Admission-control arithmetic, computed FOR the operator. Phase-0 proof (NOT shipped).

PLAN.md, verbatim:
    "Production admission is 70% of the lowest measured failure/guardrail count, rounded
     down, and reserves capacity for one worker/node failure. Browser Manager queues or
     rejects above that limit; it never relies on optimistic oversubscription."

Two readings of "failure/guardrail count" are possible and they differ by one step:
  (a) the concurrency at which a guardrail was FIRST CROSSED  (the failure count), or
  (b) the last level that PASSED.
This module computes (a) -- "the failure count" is the count at which it failed -- and
also prints (b) with the alternative number, so the operator can see the gap rather than
discovering later that the harness silently chose. See README, ambiguity A2.

Per-class, never pooled: PLAN.md Phase 4 requires the limits be "applied ... independently
to browser-only, streamed-browser, and full-UI-sandbox workloads".

Fleet reserve: with N nodes each admitting L, the fleet admits L * (N - 1), so a single
node loss is absorbed without evicting anyone. N = 1 therefore admits ZERO at fleet level
-- that is not a bug in the arithmetic, it is what "reserve capacity for one node failure"
means on a one-node fleet, and it is reported as such.
"""

from __future__ import annotations

import math

from . import config


def per_node_limit(failure_level: int | None, last_passing_level: int | None) -> dict:
    """The 70% rule. `failure_level` is the concurrency at which a guardrail crossed."""
    result: dict[str, object] = {
        "fraction": config.ADMISSION_FRACTION,
        "failure_level": failure_level,
        "last_passing_level": last_passing_level,
        "limit_from_failure_level": None,
        "limit_from_last_passing_level": None,
        "limit": None,
        "basis": None,
        "note": None,
    }
    if failure_level:
        result["limit_from_failure_level"] = math.floor(config.ADMISSION_FRACTION * failure_level)
    if last_passing_level:
        result["limit_from_last_passing_level"] = math.floor(
            config.ADMISSION_FRACTION * last_passing_level
        )
    if failure_level:
        result["limit"] = result["limit_from_failure_level"]
        result["basis"] = "70% of the concurrency at which a guardrail was first crossed"
    elif last_passing_level:
        result["limit"] = result["limit_from_last_passing_level"]
        result["basis"] = (
            "70% of the highest level tested (NO guardrail was crossed -- the ramp ran out "
            "of levels, so this is a FLOOR, not a measured ceiling)"
        )
        result["note"] = "raise --max-concurrency and re-run to find the real ceiling"
    else:
        result["note"] = "no completed level: nothing to compute"
    return result


def fleet_limit(limit: int | None, nodes: int) -> dict:
    if limit is None:
        return {"nodes": nodes, "fleet_limit": None, "note": "no per-node limit"}
    if nodes <= 1:
        return {
            "nodes": nodes,
            "fleet_limit": 0,
            "note": (
                "a 1-node fleet reserving one node failure admits 0; run >=2 nodes before "
                "promising any concurrency, or accept that a node loss drops every session"
            ),
        }
    return {
        "nodes": nodes,
        "fleet_limit": limit * (nodes - 1),
        "note": f"{nodes} nodes x {limit} minus one node held in reserve",
    }


def compute(class_results: dict[str, dict], nodes: int) -> dict:
    """class_results: capacity_class -> {failure_level, last_passing_level, workloads:[..]}"""
    out: dict[str, dict] = {}
    for capacity_class, data in class_results.items():
        node = per_node_limit(data.get("failure_level"), data.get("last_passing_level"))
        out[capacity_class] = {
            **node,
            "capacity_class": capacity_class,
            "binding_workload": data.get("binding_workload"),
            "workloads_considered": data.get("workloads", []),
            "fleet": fleet_limit(node["limit"], nodes),
        }
    return out
