"""Intervention registry — plain dict of ActionType → Intervention subclass.

Adding a new action type is one new file in this package plus one entry below.
"""

from __future__ import annotations

from aigie.autonomous.adapters import ActionType
from aigie.autonomous.directives import Directive
from aigie.autonomous.interventions.base import (
    CallIntervention,
    Intervention,
    WorkflowIntervention,
)
from aigie.autonomous.interventions.break_loop import BreakLoopIntervention
from aigie.autonomous.interventions.force_fallback import ForceFallbackIntervention
from aigie.autonomous.interventions.retry import RetryIntervention
from aigie.autonomous.interventions.rewrite_args import RewriteArgsIntervention

__all__ = [
    "INTERVENTIONS",
    "BreakLoopIntervention",
    "CallIntervention",
    "ForceFallbackIntervention",
    "Intervention",
    "RetryIntervention",
    "RewriteArgsIntervention",
    "WorkflowIntervention",
    "resolve",
]


# NEXT_STEP_INJECT_MESSAGE and TRAJECTORY_REWRITE_OUTPUT remain unwired —
# the autonomous-v2 plan does not map any flow action onto them yet.
INTERVENTIONS: dict[ActionType, type[Intervention]] = {
    ActionType.IN_STEP_RETRY: RetryIntervention,
    ActionType.IN_STEP_REWRITE_ARGS: RewriteArgsIntervention,
    ActionType.TRAJECTORY_FORCE_FALLBACK: ForceFallbackIntervention,
    ActionType.TRAJECTORY_BREAK_LOOP: BreakLoopIntervention,
}


def resolve(directive: Directive) -> Intervention | None:
    """Return the Intervention for a directive, or None if action_type is unknown."""
    cls = INTERVENTIONS.get(directive.action_type)
    return cls(directive) if cls else None
