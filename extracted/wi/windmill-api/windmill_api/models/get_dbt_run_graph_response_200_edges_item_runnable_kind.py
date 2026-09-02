from enum import Enum


class GetDbtRunGraphResponse200EdgesItemRunnableKind(str, Enum):
    FLOW = "flow"
    JOB = "job"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
