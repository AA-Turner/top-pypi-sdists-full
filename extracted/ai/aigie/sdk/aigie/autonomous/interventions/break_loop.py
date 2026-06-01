"""BreakLoopIntervention — WorkflowIntervention for TRAJECTORY_BREAK_LOOP.

Flow actions ``skip_and_log`` and ``circuit_break`` resolve here.
The FrameworkAdapter stops the agent loop / circuit-breaks the trajectory
using the carried reason for telemetry.
"""

from __future__ import annotations

from aigie.autonomous.interventions.base import WorkflowIntervention


class BreakLoopIntervention(WorkflowIntervention):
    """Stop the running agent loop; carries a reason string for telemetry."""

    @property
    def reason(self) -> str:
        return str(self.action_params.get("reason", "") or "")
