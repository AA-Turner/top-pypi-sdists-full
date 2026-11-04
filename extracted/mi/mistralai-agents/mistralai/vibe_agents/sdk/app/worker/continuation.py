"""Serializable state carried between Unified Harness Workflow runs."""

from typing import Annotated, Literal

import temporalio.workflow
from pydantic import BaseModel, Field, JsonValue
from temporalio.exceptions import ApplicationError

from mistralai.vibe.harness.core import protocol as core_protocol
from mistralai.vibe.harness.runtime.agents.models import StartSessionRequest
from mistralai.vibe.harness.runtime.hosts.workflows import WorkflowHostedSessionState
from mistralai.vibe_agents import session_workflow as wire

# The key of ``WorkflowContinuationState`` in ``app_context["continue_as_new"]``.
CONTINUATION_STATE_KEY = "agents_sdk_continuation"
# Written by SDK versions before the Harness Runtime owned command intake; never restored.
_LEGACY_RUNTIME_STATE_KEY = "x-agents-sdk-harness-runtime-state"
INCOMPATIBLE_CONTINUATION_ERROR_TYPE = "INCOMPATIBLE_CONTINUATION"


class AdmittedWorkflowMessage(BaseModel):
    """The identity of an already-admitted Turn, without a second execution payload."""

    turn_id: str
    idempotency_key: str


class MessageCommandPublication(BaseModel):
    type: Literal["start_message", "steer_message"]
    command: wire.MessageCommand
    turn_id: str


class UserMessagePublication(BaseModel):
    """The user message row to publish for a ``send_message``, a ``start_turn`` or a first Turn.

    Holds no content and no Turn ID. The row is built from the accepted command, so a message
    carried across Continue-As-New travels once, in the Runtime's pending commands.
    """

    # Named before the first Turn used it. Continue-As-New carries this value, so it stays.
    type: Literal["send_message"] = "send_message"


class ScopedInterruptPublication(BaseModel):
    type: Literal["scoped_interrupt"] = "scoped_interrupt"


class UnscopedInterruptPublication(BaseModel):
    type: Literal["unscoped_interrupt"] = "unscoped_interrupt"


type CommandPublication = Annotated[
    MessageCommandPublication | UserMessagePublication | ScopedInterruptPublication | UnscopedInterruptPublication,
    Field(discriminator="type"),
]


class MessageReceiptRecord(BaseModel):
    """What a message Update decided for one command id, so a retry gets the same answer."""

    # Only on a send_message receipt: a start or steer replays by command id alone (ADR 0038).
    digest: str | None
    # Set once the Runtime admitted the message.
    turn_id: str | None = None
    # Set with turn_id: the message joined the running Turn rather than starting turn_id.
    steered: bool = False
    # Admitted while the Session stopped, so no Turn runs it and a retry stays refused.
    refused: bool = False
    # Rejected by Harness, which keeps that answer for the command id, so a retry is rejected too.
    rejected: bool = False
    # A steer committed while its row was not published, so its Turn is unset but the id is taken.
    committed: bool = False


class WorkflowPublicationState(BaseModel):
    """Product publications still owed for commands the Runtime has not yet answered."""

    commands: dict[str, CommandPublication] = Field(default_factory=dict)
    processed_callback_ids: list[str] = Field(default_factory=list)
    message_receipts: dict[str, MessageReceiptRecord] = Field(default_factory=dict)


class SessionLimitState(BaseModel):
    """Session limit clocks, carried so a new run does not restart them."""

    started_at_unix_ms: int
    idle_since_unix_ms: int | None = None
    # The limit that stopped the Session, when a limit did.
    end_cause: str | None = None


class WorkflowContinuationState(BaseModel):
    """Serializable state carried only by a genuine Continue-As-New run."""

    hosted: WorkflowHostedSessionState
    publications: WorkflowPublicationState = Field(default_factory=WorkflowPublicationState)
    stop_requested: bool = False
    limits: SessionLimitState | None = None
    bootstrap_metric_pending: bool = False
    # The saved values of the run's stateful objects, such as Hooks with fields, by state key.
    stateful_values: dict[str, JsonValue] = Field(default_factory=dict)
    sandbox_lifecycle: dict[str, JsonValue] | None = None


def build_continuation_state(
    params: wire.SessionWorkflowStartInput,
) -> WorkflowContinuationState | None:
    if not _is_genuine_continuation() or not isinstance(params.app_context, dict):
        return None
    continuation = params.app_context.get("continue_as_new")
    if not isinstance(continuation, dict):
        return None
    state = continuation.get(CONTINUATION_STATE_KEY)
    if state is None and _LEGACY_RUNTIME_STATE_KEY in continuation:
        # Silently starting fresh would drop the carried conversation and pending commands.
        raise ApplicationError(
            "Continuation written by an incompatible SDK version cannot be restored",
            type=INCOMPATIBLE_CONTINUATION_ERROR_TYPE,
            non_retryable=True,
        )
    if state is None:
        return None
    return WorkflowContinuationState.model_validate(state)


def build_continue_as_new_input(
    params: wire.SessionWorkflowStartInput,
    state: WorkflowContinuationState,
) -> wire.SessionWorkflowStartInput:
    app_context = dict(params.app_context) if isinstance(params.app_context, dict) else {}
    raw_carried = app_context.get("continue_as_new")
    carried = dict(raw_carried) if isinstance(raw_carried, dict) else {}
    # Keep explicit nulls: Runtime state has required nullable fields, such as max_iterations.
    carried[CONTINUATION_STATE_KEY] = state.model_dump(mode="json", by_alias=True)
    app_context["continue_as_new"] = carried
    # The restored Runtime already owns the child conversation; seeding it again would duplicate it.
    child_session = (
        StartSessionRequest.model_validate(params.child_session)
        .model_copy(update={"conversation": core_protocol.ConversationSeed()})
        .model_dump(mode="json")
        if params.child_session is not None
        else None
    )
    return params.model_copy(
        update={
            "app_context": app_context,
            "child_session": child_session,
            "initial_command": wire.SystemCommand(
                action="resume",
                reason="continue_as_new",
            ),
            # The first run started this Turn, so the Runtime state above already holds it.
            "initial_turn": None,
        }
    )


def _is_genuine_continuation() -> bool:
    try:
        return temporalio.workflow.info().continued_run_id is not None
    except Exception:
        return False


__all__ = [
    "CONTINUATION_STATE_KEY",
    "INCOMPATIBLE_CONTINUATION_ERROR_TYPE",
    "AdmittedWorkflowMessage",
    "CommandPublication",
    "MessageCommandPublication",
    "MessageReceiptRecord",
    "SessionLimitState",
    "ScopedInterruptPublication",
    "UserMessagePublication",
    "UnscopedInterruptPublication",
    "WorkflowContinuationState",
    "WorkflowPublicationState",
    "build_continuation_state",
    "build_continue_as_new_input",
]
