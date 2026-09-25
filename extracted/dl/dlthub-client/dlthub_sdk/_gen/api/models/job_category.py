from enum import Enum


class JobCategory(str, Enum):
    BACKGROUND_AGENT = "background_agent"
    DASHBOARD = "dashboard"
    MCP = "mcp"
    NOTEBOOK = "notebook"
    PIPELINE = "pipeline"

    def __str__(self) -> str:
        return str(self.value)
