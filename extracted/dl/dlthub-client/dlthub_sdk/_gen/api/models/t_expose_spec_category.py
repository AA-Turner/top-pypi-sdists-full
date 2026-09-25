from enum import Enum


class TExposeSpecCategory(str, Enum):
    BACKGROUND_AGENT = "background_agent"
    DASHBOARD = "dashboard"
    MCP = "mcp"
    NOTEBOOK = "notebook"
    PIPELINE = "pipeline"

    def __str__(self) -> str:
        return str(self.value)
