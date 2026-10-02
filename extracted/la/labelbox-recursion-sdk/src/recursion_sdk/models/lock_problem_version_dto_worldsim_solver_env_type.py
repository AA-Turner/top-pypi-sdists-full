from enum import StrEnum

class LockProblemVersionDtoWorldsimSolverEnvType(StrEnum):
    COMPUTER = "computer"
    MCP = "mcp"

    def __str__(self) -> str:
        return str(self.value)
