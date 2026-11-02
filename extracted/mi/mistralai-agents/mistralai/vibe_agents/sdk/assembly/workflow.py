"""Agents SDK Workflow assembly."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mistralai.vibe.harness.runtime.agents.policy import SubagentPolicy
from mistralai.vibe.harness.runtime.session.intake import DEFAULT_SESSION_INTAKE_LIMITS, SessionIntakeLimits
from mistralai.vibe.harness.runtime.session.model_wait import DEFAULT_MODEL_WAIT_POLICY, ModelWaitPolicy
from mistralai.vibe.harness.runtime.session.programs import DEFAULT_PROGRAM_EXECUTION_POLICY, ProgramExecutionPolicy
from mistralai.vibe.harness.runtime.session.turn_policy import DEFAULT_TURN_EXECUTION_POLICY, TurnExecutionPolicy
from mistralai.vibe_agents.sdk.authoring import contracts
from mistralai.vibe_agents.sdk.authoring.agent import DEFAULT_AGENT_NAME, Agent, WorkflowType
from mistralai.vibe_agents.sdk.authoring.errors import UnsupportedAgentFeatureError

if TYPE_CHECKING:
    from mistralai.vibe_agents.sdk.app.worker.control_plane import WorkflowSessionControlPlaneBinding
    from mistralai.vibe_agents.sdk.app.worker.sandbox_lifecycle import SandboxLifecycleFactory


class WorkflowBuildError(ValueError):
    """Raised when Workflow authoring cannot be compiled."""


def build_workflow(
    agent: Agent,
    *,
    name: str | None,
    harness: contracts.Harness | None,
    type: WorkflowType = "session",
    subagent_policy: SubagentPolicy | None = None,
    session_control_plane: WorkflowSessionControlPlaneBinding | None = None,
    program_policy: ProgramExecutionPolicy = DEFAULT_PROGRAM_EXECUTION_POLICY,
    wait_policy: ModelWaitPolicy = DEFAULT_MODEL_WAIT_POLICY,
    turn_policy: TurnExecutionPolicy = DEFAULT_TURN_EXECUTION_POLICY,
    intake_limits: SessionIntakeLimits = DEFAULT_SESSION_INTAKE_LIMITS,
    sandbox_lifecycle_factory: SandboxLifecycleFactory | None = None,
) -> type:
    """Build the Workflow for the Unified Harness runtime."""

    if type == "chat":
        raise UnsupportedAgentFeatureError(
            "type=chat",
            "legacy chat Workflows are intentionally not part of the Unified Harness migration",
        )
    if type != "session":
        raise WorkflowBuildError(f'unknown to_workflow type {type!r}; expected "session"')
    agent._require_real_model()

    resolved_name = _resolve_name(agent, name)
    resolved_harness = _resolve_harness(agent, harness)
    from mistralai.vibe_agents.sdk.app.worker import session_binding  # noqa: PLC0415

    return session_binding.build_workflow_class(
        name=resolved_name,
        agent=agent,
        harness=resolved_harness or agent._resolve_harness(None),
        subagent_policy=subagent_policy,
        session_control_plane=session_control_plane,
        program_policy=program_policy,
        wait_policy=wait_policy,
        turn_policy=turn_policy,
        intake_limits=intake_limits,
        sandbox_lifecycle_factory=sandbox_lifecycle_factory,
    )


def _resolve_name(agent: Agent, name: str | None) -> str:
    resolved = name or _explicit_agent_name(agent)
    if not resolved:
        raise WorkflowBuildError(
            "Promoting an agent to a workflow needs a non-empty workflow name: pass name=... to "
            "to_workflow(), or set it on the agent with agents.Agent(model=..., name=...)."
        )
    return resolved


def _explicit_agent_name(agent: Agent) -> str | None:
    name = agent.name.strip()
    return None if name in ("", DEFAULT_AGENT_NAME) else name


def _resolve_harness(
    agent: Agent,
    harness: contracts.Harness | None,
) -> contracts.Harness | None:
    if harness is not None:
        return harness
    return agent._bundle.harness


__all__ = ["build_workflow"]
