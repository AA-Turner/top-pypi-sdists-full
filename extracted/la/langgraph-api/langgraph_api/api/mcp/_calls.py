import mcp_types as types
from pydantic import JsonValue

from langgraph_api.api.mcp._digest import digest


class ToolCallParams(types.CallToolRequestParams):
    arguments: dict[str, JsonValue] | None = None
    context: dict[str, JsonValue] | None = None

    @property
    def input(self) -> dict[str, JsonValue]:
        return self.arguments or {}

    @property
    def answers(self) -> types.InputResponses:
        return self.input_responses or {}

    def digest(self, assistant_id: str) -> str:
        return digest(assistant_id, self.name, self.input)
