from enum import StrEnum

class ProblemVersionListDtoItemWorldsimConfigType0EnvType(StrEnum):
    COMPUTER = "computer"
    MCP = "mcp"

    def __str__(self) -> str:
        return str(self.value)
