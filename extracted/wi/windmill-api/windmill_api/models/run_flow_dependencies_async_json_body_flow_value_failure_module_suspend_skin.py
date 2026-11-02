from enum import Enum


class RunFlowDependenciesAsyncJsonBodyFlowValueFailureModuleSuspendSkin(str, Enum):
    DETAILED = "detailed"
    MINIMAL = "minimal"

    def __str__(self) -> str:
        return str(self.value)
