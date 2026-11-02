"""Per-Session model token usage for the datalake.

Two paths attribute a model call's tokens to its Agents SDK Session:

- The completion request's ``metadata`` carries the Session ids, so a call that reaches the Mistral
  completion API lands them on the gateway's own usage event (``quota.request_done``).
- ``ModelUsageObservationPort`` runs in the completion activity and emits ``agents.completion.done``
  with the usage the Harness measured, for every provider, including those the gateway never sees.

``agents.completion.done`` is the source of truth for per-Session token usage. Do not rely on it for
billing: delivery is best effort, so events can be dropped. ``metadata.session_id`` on the gateway's
event is a join key to billing, not a second count to add to it.

Both read the attribution the Session binding builds with ``completion_attribution``: it travels to the
activity in the Harness ``ObservationContext``, which is why every value is a short string.
"""

import contextlib
from collections.abc import AsyncIterator
from dataclasses import dataclass
from uuid import UUID

from mistralai.vibe.harness.runtime.hosts.workflows import add_workflow_activity_observation_port
from mistralai.vibe.harness.runtime.observability import (
    AbandonedToolObservation,
    CancelledToolObservation,
    ModelAttemptFinished,
    ModelAttemptStarted,
    ObservationContext,
    TerminalToolObservation,
    ToolExecutionStarted,
)
from mistralai.vibe_agents import session_workflow as wire
from mistralai.vibe_agents.sdk.transport import telemetry

__all__ = [
    "CompletionAttribution",
    "ModelUsageObservationPort",
    "completion_attribution",
    "worker_usage_telemetry",
]

# The gateway stores a request's metadata as `metadata.*` on its usage event; these are the keys its
# readers already join on.
_COMPLETION_METADATA_KEYS = ("session_id", "parent_session_id")


@dataclass(frozen=True, slots=True)
class CompletionAttribution:
    """Who a Session's model calls are made for, in both shapes the Harness Host accepts."""

    metadata: dict[str, str]
    observation_context: ObservationContext


def completion_attribution(
    *,
    session_id: str,
    principal: wire.Principal,
    parent_session_id: UUID | None = None,
    root_session_id: UUID | None = None,
    agent_id: UUID | None = None,
    application_id: UUID | None = None,
    correlation_id: str | None = None,
) -> CompletionAttribution:
    attributes = {
        "session_id": session_id,
        "customer_id": str(principal.customer_id),
        "organization_id": str(principal.organization_id),
        "workspace_id": str(principal.workspace_id),
    }
    optional = {
        "parent_session_id": parent_session_id,
        "root_session_id": root_session_id,
        "user_id": principal.user_id,
        "agent_id": agent_id,
        "application_id": application_id,
        "correlation_id": wire.known_correlation_id(correlation_id),
    }
    attributes.update({key: str(value) for key, value in optional.items() if value is not None})
    return CompletionAttribution(
        metadata={key: attributes[key] for key in _COMPLETION_METADATA_KEYS if key in attributes},
        observation_context=ObservationContext(attributes=attributes),
    )


class ModelUsageObservationPort:
    """Emit one ``agents.completion.done`` per model attempt a Session's completion activity makes.

    Registered process-wide, so it holds no per-Session state: the Session is read from each
    observation's context. Delivery runs in the background, so no datalake request sits on the Turn.
    An activity retry is a second call to the model, so it is reported as a second attempt.
    """

    async def model_attempt_started(self, observation: ModelAttemptStarted) -> None:
        del observation

    async def model_attempt_finished(self, observation: ModelAttemptFinished) -> None:
        attributes = observation.context.attributes
        session_id = attributes.get("session_id")
        if session_id is None:
            # Not a Session this binding attributed; there is nothing to aggregate it under.
            return
        usage = observation.usage
        telemetry.completion_done(
            telemetry.CompletionDone(
                session_id=session_id,
                parent_session_id=attributes.get("parent_session_id"),
                agent_id=attributes.get("agent_id"),
                turn_id=observation.turn_id,
                action_id=observation.action_id,
                model=observation.model,
                provider=observation.provider,
                purpose=observation.purpose,
                call_type=observation.call_type,
                status=_status(observation),
                error_type=observation.error_type,
                duration_ms=int(observation.duration_seconds * 1_000),
                input_tokens=usage.input_tokens,
                output_tokens=usage.output_tokens,
                cache_read_tokens=usage.cache_read_tokens,
                cache_write_tokens=usage.cache_write_tokens,
                reasoning_tokens=usage.reasoning_tokens,
                total_tokens=usage.total_tokens,
                correlation_id=attributes.get("correlation_id"),
                customer_id=attributes.get("customer_id"),
                workspace_id=attributes.get("workspace_id"),
                user_id=attributes.get("user_id"),
            )
        )

    async def tool_execution_started(self, observation: ToolExecutionStarted) -> None:
        del observation

    async def tool_result_committed(self, observation: TerminalToolObservation) -> None:
        del observation

    async def tool_execution_cancelled(self, observation: CancelledToolObservation) -> None:
        del observation

    async def tool_execution_abandoned(self, observation: AbandonedToolObservation) -> None:
        del observation


@contextlib.asynccontextmanager
async def worker_usage_telemetry() -> AsyncIterator[None]:
    """Report this worker's model usage for as long as it serves; wrap every worker entrypoint in it.

    Adds the usage port to the completion activities next to any observer already installed (the same
    port is installed once), starts the delivery before the worker serves, and drains it on exit.
    With telemetry turned off it does nothing.
    """
    if not telemetry.telemetry_enabled():
        yield
        return
    add_workflow_activity_observation_port(_PORT)
    telemetry.start_background_deliveries()
    try:
        yield
    finally:
        await telemetry.drain_background_deliveries()


def _status(observation: ModelAttemptFinished) -> telemetry.CompletionStatus:
    # A stream that finished but failed to close still consumed its tokens.
    match observation.outcome:
        case "completed" | "completed_close_failed":
            return "success"
        case "cancelled":
            return "cancelled"
        case "failed":
            return "error"


_PORT = ModelUsageObservationPort()
