from enum import Enum


class TExposeSpecInterface(str, Enum):
    GUI = "gui"
    MCP = "mcp"
    REST_API = "rest_api"

    def __str__(self) -> str:
        return str(self.value)
