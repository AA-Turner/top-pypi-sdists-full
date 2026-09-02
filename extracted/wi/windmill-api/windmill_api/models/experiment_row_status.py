from enum import Enum


class ExperimentRowStatus(str, Enum):
    CANCELED = "canceled"
    FAILURE = "failure"
    RUNNING = "running"
    SKIPPED = "skipped"
    SUCCESS = "success"
    UNAVAILABLE = "unavailable"

    def __str__(self) -> str:
        return str(self.value)
