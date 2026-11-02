from enum import StrEnum

class CheckSubjectKind(StrEnum):
    MAIN_BRANCH = "main_branch"
    PULL_REQUEST = "pull_request"

    def __str__(self) -> str:
        return str(self.value)
