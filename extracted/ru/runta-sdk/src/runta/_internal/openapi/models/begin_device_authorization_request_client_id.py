from enum import Enum


class BeginDeviceAuthorizationRequestClientId(str, Enum):
    FOXDEN = "foxden"
    FOXDEN_MCP = "foxden_mcp"
    RUNTA_AGENT = "runta_agent"
    RUNTA_CLI = "runta_cli"
    RUNTA_CREW = "runta_crew"

    def __str__(self) -> str:
        return str(self.value)
