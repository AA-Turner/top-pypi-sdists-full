"""ForceFallbackIntervention — WorkflowIntervention for TRAJECTORY_FORCE_FALLBACK.

Flow actions ``switch_model`` and ``fallback_tool`` both resolve here.
The intervention only carries the typed payload; the FrameworkAdapter is
responsible for actually swapping the model/tool on the running workflow.
"""

from __future__ import annotations

from aigie.autonomous.interventions.base import WorkflowIntervention


class ForceFallbackIntervention(WorkflowIntervention):
    """Force a fallback model or tool on the trajectory.

    Exactly one of ``model`` / ``tool`` is expected to be non-empty per
    directive — actions.py's resolver fills in whichever the flow step
    specified. Adapters can read both and choose what to apply.
    """

    @property
    def model(self) -> str:
        return str(self.action_params.get("model", "") or "")

    @property
    def tool(self) -> str:
        return str(self.action_params.get("tool", "") or "")
