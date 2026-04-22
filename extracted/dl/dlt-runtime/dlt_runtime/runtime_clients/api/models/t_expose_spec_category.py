from enum import Enum


class TExposeSpecCategory(str, Enum):
    DASHBOARD = "dashboard"
    MCP = "mcp"
    NOTEBOOK = "notebook"
    PIPELINE = "pipeline"

    def __str__(self) -> str:
        return str(self.value)
