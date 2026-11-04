from enum import Enum


class TExposeSpecInterfaceType0(str, Enum):
    GUI = "gui"
    MCP = "mcp"
    REST_API = "rest_api"

    def __str__(self) -> str:
        return str(self.value)
