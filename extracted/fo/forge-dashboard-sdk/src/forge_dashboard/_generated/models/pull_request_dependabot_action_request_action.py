from enum import StrEnum

class PullRequestDependabotActionRequestAction(StrEnum):
    REBASE = "rebase"
    RECREATE = "recreate"

    def __str__(self) -> str:
        return str(self.value)
