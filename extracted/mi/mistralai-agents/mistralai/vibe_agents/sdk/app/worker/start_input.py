"""What a Session Workflow takes from its start input, and how it refuses one.

Anyone allowed to start the Workflow writes the whole start input. Reading it is one step that either
returns what the Session runs with or refuses the input. A refusal answers its caller with an error
id only; the reason stays in the worker's log under that id, and only as fixed text or structure,
never as values the caller wrote.
"""

from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import cast
from uuid import UUID, uuid4

import structlog
import temporalio.workflow
from pydantic import ValidationError

from mistralai.vibe.harness.runtime.agents.control_plane import SessionControlPlaneError
from mistralai.vibe.harness.runtime.agents.models import ChildLineage, StartSessionRequest
from mistralai.vibe.harness.runtime.agents.policy import SubagentPolicy
from mistralai.vibe.harness.runtime.hosts.workflows import WorkflowHarnessDefinition, workflow_is_replaying
from mistralai.vibe_agents import session_workflow as wire
from mistralai.vibe_agents.sdk.app.worker import child_definition
from mistralai.vibe_agents.sdk.app.worker import control_plane as worker_control_plane
from mistralai.vibe_agents.sdk.assembly import assemble, sandbox_skills
from mistralai.vibe_agents.sdk.authoring.errors import UnsupportedAgentFeatureError

logger = structlog.get_logger(__name__)

# The only customization a completion can refuse is a model or reasoning effort override; its own
# reason names the worker's completion provider, so the caller reads this one instead.
_UNSUPPORTED_OVERRIDE = "This agent does not support a model or reasoning_effort override for its completion provider"


class StartInputRefusal(ValueError):
    """A start input the worker refuses, with a fixed reason that never quotes the input."""


class StartInputRejectedError(Exception):
    """The answer to a refused start input: an id, whose reason is in the worker's log.

    A refusal the caller can act on adds a fixed reason, written by the worker, never quoting the input
    or naming the worker's configuration.
    """

    def __init__(self, error_id: UUID, reason: str | None = None) -> None:
        message = f"This Session's start input was rejected (error id {error_id})"
        super().__init__(f"{message}: {reason}" if reason else message)
        self.error_id = error_id


@dataclass(frozen=True, slots=True)
class StartInput:
    """What a Session runs with, once its start input is accepted."""

    definition: WorkflowHarnessDefinition
    child_session: StartSessionRequest | None
    subagent_policy: SubagentPolicy | None
    lineage: ChildLineage
    session_v1: bool


def read_start_input(
    params: wire.SessionWorkflowStartInput,
    definition: WorkflowHarnessDefinition,
    *,
    static_subagent_policy: SubagentPolicy | None,
    bound: bool,
    skill_files: sandbox_skills.SandboxSkillFiles | None = None,
) -> StartInput:
    """Accept the start input against this worker's own `definition`, or raise `StartInputRejectedError`.

    `bound` says whether the Workflow has a Session-control-plane binding, which only a Workflow that
    serves subagents has.
    """

    try:
        return _read(
            params, definition, static_subagent_policy=static_subagent_policy, bound=bound, skill_files=skill_files
        )
    except (ValueError, SessionControlPlaneError) as error:
        # Pydantic's ValidationError is a ValueError, and so is the UnsupportedAgentFeatureError of a
        # customization the agent's completion cannot take.
        raise reject_start_input(params, error) from error


def _read(
    params: wire.SessionWorkflowStartInput,
    definition: WorkflowHarnessDefinition,
    *,
    static_subagent_policy: SubagentPolicy | None,
    bound: bool,
    skill_files: sandbox_skills.SandboxSkillFiles | None = None,
) -> StartInput:
    child_session = (
        StartSessionRequest.model_validate(params.child_session) if params.child_session is not None else None
    )
    subagent_policy = session_subagent_policy(params, static_subagent_policy, bound=bound)
    if child_session is not None:
        if subagent_policy is None or not bound:
            raise StartInputRefusal("Child Session requires the configured Session-control-plane binding")
        definition = child_definition.verified_child_definition(definition, child_session, skill_files)
    lineage = (
        # Set: the check above refuses a child request without a lineage.
        cast(ChildLineage, child_session.lineage)
        if child_session is not None
        else ChildLineage(root_customization=params.agent.model_dump(mode="json") if params.agent is not None else None)
    )
    session_v1 = is_session_v1(params)
    if not session_v1 and (subagent_policy is not None or child_session is not None):
        # Legacy Task Protocol history has no shape for agent context messages.
        raise StartInputRefusal("Subagents run only on Session v1; a legacy-protocol Session cannot run them")
    return StartInput(
        definition=with_session_agent_customization(definition, params.agent),
        child_session=child_session,
        subagent_policy=subagent_policy,
        lineage=lineage,
        session_v1=session_v1,
    )


def reject_start_input(
    params: wire.SessionWorkflowStartInput, error: ValueError | SessionControlPlaneError
) -> StartInputRejectedError:
    """The answer to a start input refused with `error`, logged under a new id without the input's values."""

    error_id = temporalio.workflow.uuid4() if temporalio.workflow.in_workflow() else uuid4()
    if not workflow_is_replaying():
        # A start input can hold Session inputs, and an error message, even a validation message, can
        # quote what its caller wrote.
        detail: dict[str, object] = {}
        if isinstance(error, StartInputRefusal | child_definition.ChildDefinitionRefusal):
            detail["error_message"] = str(error)
        elif isinstance(error, ValidationError):
            detail["errors"] = [{"loc": entry["loc"], "type": entry["type"]} for entry in error.errors()]
        elif isinstance(error, SessionControlPlaneError):
            detail["error_code"] = error.code
        elif isinstance(error, UnsupportedAgentFeatureError):
            detail["error_feature"] = error.feature
        logger.warning(
            "session_start_input_rejected",
            session_id=str(params.session_id),
            error_id=str(error_id),
            error_type=type(error).__name__,
            **detail,
        )
    reason = _UNSUPPORTED_OVERRIDE if isinstance(error, UnsupportedAgentFeatureError) else None
    return StartInputRejectedError(error_id, reason)


_UNANSWERED = "The Agents API could not be asked whether it started this child Session"
_CHILD_REFUSALS: Mapping[worker_control_plane.ChildVerificationOutcome, str] = {
    "no_row": "Child Session was not started by the Agents API",
    "mismatch": "Child Session start input does not match the Session the Agents API started",
    "unsupported": "The Agents API cannot verify child Sessions: deploy it before workers on this SDK run subagents",
    "refused": "The Agents API refused to verify this child Session",
}


async def verify_child_session(
    params: wire.SessionWorkflowStartInput,
    child: StartSessionRequest,
    control_plane: worker_control_plane.ActivitySessionControlPlane,
) -> None:
    """Run a child only once the Agents API says it started it, at the place its start input claims.

    The start input, which anyone allowed to start the Workflow writes, names the child's root, parent
    and path; the sandbox it borrows is bound to that root. The Agents API recorded every child it
    started, keyed by its Workflow id, which the caller of a direct start cannot borrow from a running
    Session. Any answer but yes refuses the child, and an Agents API that cannot answer is no yes.
    """

    workflow_id = (
        temporalio.workflow.info().workflow_id if temporalio.workflow.in_workflow() else str(params.session_id)
    )
    if workflow_id != str(params.session_id) or workflow_id != str(child.session_id):
        reason = "Child Session does not run under its own Session id"
    else:
        try:
            verification = await control_plane.verify_child_session(
                wire.VerifyChildSessionRequest(
                    session_id=child.session_id,
                    root_session_id=child.root_session_id,
                    parent_session_id=child.parent_session_id,
                    agent_path=child.agent_path,
                )
            )
        except Exception as error:
            # The Activity has already retried; a cancellation still stops the Session.
            if temporalio.exceptions.is_cancelled_exception(error):
                raise
            raise reject_start_input(params, StartInputRefusal(_UNANSWERED)) from error
        if verification.outcome == "ok":
            return
        reason = _CHILD_REFUSALS[verification.outcome]
    raise reject_start_input(params, StartInputRefusal(reason))


def is_session_v1(params: wire.SessionWorkflowStartInput) -> bool:
    # Fixed at creation and carried across continue-as-new, so the shape never changes mid-session.
    return params.session_protocol == "session_v1"


def with_session_agent_customization(
    definition: WorkflowHarnessDefinition,
    customization: wire.SessionAgentCustomization | None,
) -> WorkflowHarnessDefinition:
    if customization is None:
        return definition
    return definition.model_copy(
        update={"agent_config": assemble.with_session_agent_customization(definition.agent_config, customization)}
    )


def session_subagent_policy(
    params: wire.SessionWorkflowStartInput,
    static: SubagentPolicy | None,
    *,
    bound: bool,
) -> SubagentPolicy | None:
    """The Session's subagent policy: its start input's, else the Workflow's static one.

    The Agents API writes the start input's policy for every Session of a tree that has one, so it
    governs on a deployed worker. Without a Session-control-plane binding, which only a Workflow
    that serves subagents passes, the Session runs without subagents.
    """

    session = params.subagent_policy
    if session is None or not bound:
        return static
    # Operator-only limits, such as the child interrupt timeout, stay the Workflow's.
    return replace(
        static or SubagentPolicy(concurrent_child_turn_limit=session.concurrent_child_turn_limit),
        concurrent_child_turn_limit=session.concurrent_child_turn_limit,
        idle_message_starts=session.idle_message_starts,
        max_depth=session.max_depth,
    )


__all__ = [
    "StartInput",
    "StartInputRefusal",
    "StartInputRejectedError",
    "is_session_v1",
    "read_start_input",
    "reject_start_input",
    "session_subagent_policy",
    "verify_child_session",
    "with_session_agent_customization",
]
