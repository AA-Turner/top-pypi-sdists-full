from datetime import datetime
from enum import Enum
from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import BeforeValidator, ConfigDict

from xpander_sdk.models.events import ToolCallRequestReasoning
from xpander_sdk.models.shared import XPanderSharedModel
from xpander_sdk.models.user import User
from xpander_sdk.modules.tools_repository.models.mcp import MCPOAuthGetTokenResponse


class AgentActivityThreadMessageContent(XPanderSharedModel):
    text: Optional[str] = None
    files: Optional[List[str]] = []


class AgentActivityThreadMessage(XPanderSharedModel):
    id: str
    created_at: datetime
    role: Literal["user", "agent"]
    content: AgentActivityThreadMessageContent
    sub_execution_result: Optional[bool] = False
    # originating user for this message — set on user turns so multi-user threads attribute each query correctly
    user: Optional[User] = None


class AgentActivityThreadToolCall(XPanderSharedModel):
    id: str
    created_at: datetime
    tool_name: str
    payload: Any
    is_error: Optional[bool] = False
    reasoning: Optional[ToolCallRequestReasoning] = None
    result: Optional[Any] = None
    plan_task_id: Optional[str] = None


class AgentActivityThreadReasoningType(str, Enum):
    Think = "think"
    Analyze = "analyze"


class AgentActivityThreadReasoning(XPanderSharedModel):
    id: str
    created_at: datetime
    type: AgentActivityThreadReasoningType
    title: str
    confidence: float
    thought: Optional[str] = None
    action: Optional[str] = None
    result: Optional[str] = None
    analysis: Optional[str] = None
    plan_task_id: Optional[str] = None


class AgentActivityThreadSubAgentTrigger(XPanderSharedModel):
    id: str
    created_at: datetime
    agent_id: str
    query: Optional[str] = None
    files: Optional[List[str]] = []
    reasoning: ToolCallRequestReasoning
    plan_task_id: Optional[str] = None


class AgentActivityThreadAuth(MCPOAuthGetTokenResponse):
    id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Agent gateway activity-log entries — one model per decision type.
# Mirrors `xpander_dev_utils.models.activity` in xpander-mono.
# ---------------------------------------------------------------------------
class _AgentActivityGatewayBase(XPanderSharedModel):
    id: str
    created_at: datetime
    agent_id: Optional[str] = None
    reasoning: str
    title: str = ""
    description: str = ""


class AgentActivityThreadGatewayCreateExecution(_AgentActivityGatewayBase):
    action: Literal["create_execution"] = "create_execution"
    created_execution_id: str
    query: str = ""
    is_async: Optional[bool] = False


class AgentActivityThreadGatewayAskExecution(_AgentActivityGatewayBase):
    action: Literal["ask_execution"] = "ask_execution"
    created_execution_id: str
    new_input: str
    rejected: Optional[str] = None


class AgentActivityThreadGatewayStopExecution(_AgentActivityGatewayBase):
    action: Literal["stop_execution"] = "stop_execution"
    created_execution_id: str


class AgentActivityThreadGatewayContinueExecution(_AgentActivityGatewayBase):
    action: Literal["continue_execution"] = "continue_execution"
    created_execution_id: str
    rejected: Optional[str] = None


class AgentActivityThreadGatewayExecutionResultEntry(XPanderSharedModel):
    created_execution_id: str
    status: Optional[str] = None
    result: Optional[str] = None


class AgentActivityThreadGatewayGetExecutionsResult(_AgentActivityGatewayBase):
    action: Literal["get_executions_result"] = "get_executions_result"
    executions: List[AgentActivityThreadGatewayExecutionResultEntry] = []


AgentActivityThreadGatewayDecisionType = Union[
    AgentActivityThreadGatewayCreateExecution,
    AgentActivityThreadGatewayAskExecution,
    AgentActivityThreadGatewayStopExecution,
    AgentActivityThreadGatewayContinueExecution,
    AgentActivityThreadGatewayGetExecutionsResult,
]


class AgentActivityThreadOtherEntry(XPanderSharedModel):
    """An entry kind this SDK version does not model.

    The platform adds activity kinds continuously - approval cards, questions, secret prompts,
    live surfaces - and an SDK pinned months earlier cannot know them. Without this, one unknown
    entry made the whole activity log unreadable rather than costing only its own detail, so the
    fields every entry shares are kept and the rest is preserved verbatim.
    """

    model_config = ConfigDict(extra="allow")

    id: Optional[str] = None
    created_at: Optional[datetime] = None
    agent_id: Optional[str] = None


AgentActivityThreadMessageType = Union[
    AgentActivityThreadMessage,
    AgentActivityThreadToolCall,
    AgentActivityThreadReasoning,
    AgentActivityThreadSubAgentTrigger,
    AgentActivityThreadAuth,
    AgentActivityThreadGatewayCreateExecution,
    AgentActivityThreadGatewayAskExecution,
    AgentActivityThreadGatewayStopExecution,
    AgentActivityThreadGatewayContinueExecution,
    AgentActivityThreadGatewayGetExecutionsResult,
    AgentActivityThreadOtherEntry,
]

# The gateway card kinds this version models; anything else is newer than this SDK.
_MODELLED_ACTIONS = frozenset(
    {
        "create_execution",
        "ask_execution",
        "stop_execution",
        "continue_execution",
        "get_executions_result",
    }
)


def _route_entry(value: Any) -> Any:
    """Send an entry naming an unmodelled action straight to the permissive kind."""
    if isinstance(value, dict):
        action = value.get("action")
        if isinstance(action, str) and action not in _MODELLED_ACTIONS:
            return AgentActivityThreadOtherEntry(**value)
    return value


class AgentActivityThread(XPanderSharedModel):
    id: str
    created_at: datetime
    messages: List[
        Annotated[AgentActivityThreadMessageType, BeforeValidator(_route_entry)]
    ]
    user: Optional[User] = None


class AgentActivityThreadListItem(XPanderSharedModel):
    id: str
    created_at: datetime
