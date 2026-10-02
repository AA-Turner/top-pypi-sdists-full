from enum import StrEnum

class GradingConfigComputeExecType(StrEnum):
    COMPUTE_EXEC = "compute_exec"

    def __str__(self) -> str:
        return str(self.value)
