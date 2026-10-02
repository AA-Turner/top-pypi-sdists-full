from enum import StrEnum

class CreateCheckFixCycleDtoTargetType0Kind(StrEnum):
    GIT_FORK = "git_fork"

    def __str__(self) -> str:
        return str(self.value)
