"""Durable callback requests and results for the Session API."""

from typing import Annotated, Literal

from pydantic import Field, JsonValue, TypeAdapter

from .base import JsonSchema, SessionModel
from .common import CallbackId, ProtocolError, ToolCallId, TurnId
from .configuration import AgentConfig
from .content import ContentBlock


class BaseSessionCallback(SessionModel):
    id: CallbackId
    turn_id: TurnId | None = None


class ApprovalCallback(BaseSessionCallback):
    kind: Literal["approval"] = "approval"
    tool_call_id: ToolCallId
    title: str
    description: str = ""
    input: JsonValue = None


class UserInputCallback(BaseSessionCallback):
    kind: Literal["user_input"] = "user_input"
    message: list[ContentBlock] = Field(default_factory=list)
    response_schema: JsonSchema | None = None


class AskEnableConnectorCallback(BaseSessionCallback):
    kind: Literal["ask_enable_connector"] = "ask_enable_connector"
    connector_name: str
    reason: str = ""
    requirements: JsonValue = None


class ClientToolCallback(BaseSessionCallback):
    kind: Literal["client_tool"] = "client_tool"
    name: str
    input: JsonValue = None


class ClientHookCallback(BaseSessionCallback):
    kind: Literal["client_hook"] = "client_hook"
    name: str
    input: JsonValue = None


class ExecuteCodeCallback(BaseSessionCallback):
    kind: Literal["execute_code"] = "execute_code"
    code: str


class StartSubagentCallback(BaseSessionCallback):
    kind: Literal["start_subagent"] = "start_subagent"
    agent_config: AgentConfig


type SessionCallback = Annotated[
    ApprovalCallback
    | UserInputCallback
    | AskEnableConnectorCallback
    | ClientToolCallback
    | ClientHookCallback
    | ExecuteCodeCallback
    | StartSubagentCallback,
    Field(discriminator="kind"),
]

SessionCallbackAdapter: TypeAdapter[SessionCallback] = TypeAdapter(SessionCallback)


class CallbackResult(SessionModel):
    """Answer a durable callback by its stable identity."""

    callback_id: CallbackId
    output: JsonValue = None
    annotations: dict[str, JsonValue] = Field(default_factory=dict)
    error: ProtocolError | None = None
