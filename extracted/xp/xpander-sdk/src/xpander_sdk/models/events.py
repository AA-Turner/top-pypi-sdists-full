from enum import Enum
from typing import Any, List, Optional

from pydantic import Field
from xpander_sdk.models.shared import XPanderSharedModel
from datetime import datetime


class TaskStatus(str, Enum):
    READY = "ready"
    RUNNING = "running"
    FAILED = "failed"
    DONE = "done"


class Task(XPanderSharedModel):
    id: str = Field(..., description="task id")
    title: str = Field(..., description="Short task title, max 120 chars")
    description: Optional[str] = Field(
        None, description="Optional short step description, max 120 chars"
    )
    status: TaskStatus = Field(..., description="Task status")
    created_at: datetime = Field(..., description="Creation timestamp (ISO 8601)")
    started_at: Optional[datetime] = Field(
        None, description="Start timestamp (ISO 8601)"
    )
    finished_at: Optional[datetime] = Field(
        None, description="Finish timestamp (ISO 8601)"
    )
    error: Optional[str] = Field(None, description="Error message if failed")
    parent_id: Optional[str] = Field(None, description="Parent task id if related")


class ToolCallRequestReasoning(XPanderSharedModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ToolCallRequest(XPanderSharedModel):
    request_id: str
    operation_id: str
    tool_call_id: Optional[str] = None
    graph_node_id: Optional[str] = None
    tool_name: Optional[str] = None
    payload: Optional[Any] = None
    reasoning: Optional[ToolCallRequestReasoning] = None
    plan_task_id: Optional[str] = None


class ToolCallResult(ToolCallRequest):
    operation_id: str
    tool_call_id: Optional[str] = None
    tool_name: Optional[str] = None
    payload: Optional[Any] = None
    result: Optional[Any] = None
    is_error: Optional[bool] = False


class TaskUpdateEventType(str, Enum):
    # SSE-level handshake — emitted as the very first event on any
    # streaming response, before any persistence work runs server-side.
    # Lets the client switch UI state to "live" immediately instead of
    # waiting for `TaskCreated` (which is gated on persist + claim lock).
    Connected = "connected"

    # tasks
    TaskCreated = "task_created"
    TaskUpdated = "task_updated"
    TaskFinished = "task_finished"

    # streaming
    Chunk = "chunk"

    # MCP Auth
    AuthEvent = "auth_event"

    # tool calls
    ToolCallRequest = "tool_call_request"
    ToolCallResult = "tool_call_result"

    # multi agents
    SubAgentTrigger = "sub_agent_trigger"

    # reasoning
    Think = "think"
    Analyze = "analyze"

    # deep planning
    PlanUpdated = "plan_updated"

    # task compaction
    TaskCompactization = "task_compactization"

    # context window status (per-turn snapshot, delta-gated)
    ContextStatus = "context_status"

    # agent gateway
    AgentGatewayDecision = "agent_gateway_decision"

    # a steer reached this task's model at a tool-call boundary
    GatewaySteerApplied = "gateway_steer_applied"

    # omni gateway asks the user one or more questions, rendered as an
    # interactive card; the turn ends and resumes when answers are submitted
    AskUserQuestions = "ask_user_questions"

    # sub-task lifecycle mirrored onto the parent (gateway) stream
    SubTaskCreated = "sub_task_created"
    SubTaskUpdated = "sub_task_updated"
    SubTaskFinished = "sub_task_finished"

    # omni gateway offers to invite a teammate (admin/super-admin only),
    # rendered as an interactive card; the turn resumes once the user confirms
    InviteMember = "invite_member"
    # a member invite was sent, rendered as a confirmation chip
    MemberInvited = "member_invited"
    # omni gateway asks the user to provide one or more secrets a downstream
    # skill / custom code needs, rendered as an interactive card
    AskForSecret = "ask_for_secret"
    # secrets were saved, rendered as a confirmation chip (names only, no values)
    SecretSaved = "secret_saved"
    # an agent generated/updated a Live Surface; rendered as an in-chat preview card
    LiveSurfaceCreated = "live_surface_created"
    # an agent upserted an inline chat card (live-surface-styled manifest rendered
    # in the message flow, not openable); updates in place by card_id
    InlineCard = "inline_card"
