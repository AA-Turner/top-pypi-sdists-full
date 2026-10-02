from enum import StrEnum

class CreateProblemWithVersionResponseDtoVersionWorldsimConfigType0EnvType(StrEnum):
    COMPUTER = "computer"
    MCP = "mcp"

    def __str__(self) -> str:
        return str(self.value)
