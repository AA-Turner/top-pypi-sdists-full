from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from langchain.agents.middleware import AgentMiddleware

if TYPE_CHECKING:
    from langchain_core.messages import ToolMessage
    from langgraph.prebuilt.tool_node import ToolCallRequest
    from langgraph.types import Command

    from bitfab.langgraph_integration import BitfabLangGraphIntegration


class BitfabAgentMiddleware(AgentMiddleware):
    """LangChain agent middleware that records each tool call as a replayable span.

    Get it from ``integration.middleware`` and pass it to ``create_agent`` or
    ``create_deep_agent`` through ``middleware=[...]``.
    """

    def __init__(self, integration: BitfabLangGraphIntegration) -> None:
        super().__init__()
        self._integration = integration

    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
    ) -> ToolMessage | Command:
        return self._integration.wrap_tool_call(request, handler)

    async def awrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], Awaitable[ToolMessage | Command]],
    ) -> ToolMessage | Command:
        return await self._integration.awrap_tool_call(request, handler)
