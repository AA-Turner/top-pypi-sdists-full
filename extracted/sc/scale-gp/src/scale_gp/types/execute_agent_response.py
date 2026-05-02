# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ExecuteAgentResponse", "Context", "ContextToolRequest"]


class ContextToolRequest(BaseModel):
    """The tool request if the agent needs more information."""

    arguments: str
    """Arguments to pass to the tool.

    The format must be a JSON Schema-compliant object serialized into a string.
    """

    name: str
    """Name of the tool that the AI wants the client to use."""


class Context(BaseModel):
    """Context object containing the output payload.

    This will contain a key for all actions that the agent can perform. However, only the key corresponding to the action that the agent performed have a populated value. The rest of the values will be `null`.
    """

    content: Optional[str] = None
    """The final output of the agent when it no longer needs any tools"""

    tool_request: Optional[ContextToolRequest] = None
    """The tool request if the agent needs more information."""


class ExecuteAgentResponse(BaseModel):
    action: Literal["tool_request", "content"]
    """The action that the agent performed.

    The context will contain a key for each action that the agent can perform.
    However, only the key corresponding to the action that the agent actually
    performed will have a populated value. The rest of the values will be `null`.
    """

    context: Context
    """Context object containing the output payload.

    This will contain a key for all actions that the agent can perform. However,
    only the key corresponding to the action that the agent performed have a
    populated value. The rest of the values will be `null`.
    """
