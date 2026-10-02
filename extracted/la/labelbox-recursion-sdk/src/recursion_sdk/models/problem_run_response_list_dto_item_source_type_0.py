from enum import StrEnum

class ProblemRunResponseListDtoItemSourceType0(StrEnum):
    EVALUATION = "evaluation"
    INTERACTIVE = "interactive"
    INTERACTIVE_LOCAL_DOCKER = "interactive_local_docker"
    JOB = "job"

    def __str__(self) -> str:
        return str(self.value)
