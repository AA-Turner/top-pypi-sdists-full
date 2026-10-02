from enum import StrEnum

class ClaimNextWithVersionResponseDtoVersionWorldsimConfigType0EnvType(StrEnum):
    COMPUTER = "computer"
    MCP = "mcp"

    def __str__(self) -> str:
        return str(self.value)
