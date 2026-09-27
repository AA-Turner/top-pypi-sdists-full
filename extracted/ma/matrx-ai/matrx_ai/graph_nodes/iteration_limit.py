"""How many agent-loop iterations one workflow step may take — an ORGANIZATION'S setting.

Every agent-running workflow node (``ai.agent.start``, ``ai.mandate.start``,
``ai.agent.produce``, ``ai.agent.tool_calling``, ``ai.agent.react``, ``ai.chat``,
``ai.conversation.continue``, ``ai.agent.assign``) used to carry
``max_iterations: int = 100`` in its input schema — an opinion frozen in code, so no
organization could say "our workflow agents stop at 20". It is now the knob
``workflow.run_limits / agent_max_iterations`` (seeded 100 by aidream
``db/migrations/wf_071_workflow_agent_max_iterations_knob.sql``, overridable per
ORGANIZATION, admin-editable), read on EVERY step run through the host resolver
aidream installs at boot (``package_integration._workflow_agent_max_iterations``).

Precedence, lowest → highest:
  1. the organization's setting (else the platform value; standalone: 100)
  2. the step's own ``max_iterations`` when its author set one

The node input's ``le=500`` stays a constant: it is the SAFETY ceiling a runaway loop
can never pass whatever anyone sets, not a behavioural choice.

When a step stops at a limit that came from the SETTING, the failure says so and names
the setting — a person reading the run knows which knob to turn, instead of reading a
bare "Stopped after 20 iterations" and hunting for a 20 nobody wrote on the step.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from matrx_utils import vcprint

#: The knob address in ``platform.feature_knob``.
AGENT_MAX_ITERATIONS_KNOB: tuple[str, str] = ("workflow.run_limits", "agent_max_iterations")
#: What a person sees in Settings for it.
AGENT_MAX_ITERATIONS_LABEL = "Workflows › Agent step iteration limit"
#: The standalone (no-host) posture only — hosted, the knob row is the value.
STANDALONE_AGENT_MAX_ITERATIONS = 100
#: The safety ceiling every node input carries as ``le=``. Never a knob.
AGENT_MAX_ITERATIONS_CEILING = 500

#: ``async (organization_id) -> int``.
AgentMaxIterationsResolver = Callable[[str | None], Awaitable[int]]

_RESOLVER: AgentMaxIterationsResolver | None = None


def set_agent_max_iterations_resolver(resolver: AgentMaxIterationsResolver | None) -> None:
    """Install the host's per-organization knob reader (``None`` = standalone)."""
    global _RESOLVER
    _RESOLVER = resolver


def setting_sentence(value: int) -> str:
    knob = "/".join(AGENT_MAX_ITERATIONS_KNOB)
    return (
        f"This step stopped at {value} agent iterations because that is your "
        f"organization's setting “{AGENT_MAX_ITERATIONS_LABEL}” ({knob} = {value}). "
        "Raise that setting, or set Max iterations on this step, to let it run longer."
    )


@dataclass(frozen=True, slots=True)
class StepIterationLimit:
    """The limit one step runs under, and whether the organization's setting chose it."""

    value: int
    from_setting: bool

    def name_on(self, result: Any) -> Any:
        """Name the setting on a failure that stopped AT this limit; pass anything else through."""
        if not self.from_setting:
            return result
        from matrx_graph.types.result import Failure, failure

        if not isinstance(result, Failure):
            return result
        details = dict(result.error.details or {})
        if details.get("status") != "max_iterations_exceeded":
            return result
        details["iteration_limit_setting"] = {
            "feature": AGENT_MAX_ITERATIONS_KNOB[0],
            "key": AGENT_MAX_ITERATIONS_KNOB[1],
            "label": AGENT_MAX_ITERATIONS_LABEL,
            "value": self.value,
        }
        return failure(
            result.error.code,
            f"{setting_sentence(self.value)} {result.error.message}",
            details=details,
        )


async def organization_agent_max_iterations(organization_id: str | None) -> int:
    """This organization's workflow agent-step iteration limit.

    A resolver failure (the host's ``KnobNotRegisteredError``, a database blip) is
    announced in red with its remedy and the standalone value applies — a step never
    fails because a setting could not be read."""
    resolver = _RESOLVER
    if resolver is None:
        return STANDALONE_AGENT_MAX_ITERATIONS
    try:
        value = int(await resolver(organization_id))
    except Exception as exc:  # noqa: BLE001 — one failure shape, said out loud
        vcprint(
            f"[workflow agent step] {'/'.join(AGENT_MAX_ITERATIONS_KNOB)} could not be resolved "
            f"for organization {organization_id!r} ({type(exc).__name__}: {exc}); using "
            f"{STANDALONE_AGENT_MAX_ITERATIONS}. Fix the knob row or the host resolver.",
            color="red",
        )
        return STANDALONE_AGENT_MAX_ITERATIONS
    return max(1, min(value, AGENT_MAX_ITERATIONS_CEILING))


async def resolve_step_iteration_limit(ctx: Any, authored: int | None) -> StepIterationLimit:
    """The limit for this step run: the author's value when set, else the organization's."""
    if authored is not None:
        return StepIterationLimit(value=int(authored), from_setting=False)
    organization_id = getattr(ctx, "organization_id", None)
    value = await organization_agent_max_iterations(
        str(organization_id) if organization_id else None
    )
    return StepIterationLimit(value=value, from_setting=True)


#: The field every agent-running node input declares, so all eight say the same thing.
MAX_ITERATIONS_DESCRIPTION = (
    "Maximum agent reasoning/tool-loop iterations for this step. Leave empty to use your "
    f"organization's setting “{AGENT_MAX_ITERATIONS_LABEL}” (100 unless changed)."
)
