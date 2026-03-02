from enum import Enum


class InteractiveScriptType(str, Enum):
    MARIMO = "marimo"
    MCP = "mcp"
    STREAMLIT = "streamlit"

    def __str__(self) -> str:
        return str(self.value)
