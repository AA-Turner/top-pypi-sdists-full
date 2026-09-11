from enum import Enum


class TriggerType(str, Enum):
    JOB_RUN_FAILURE = "job-run-failure"
    JOB_RUN_SUCCESS = "job-run-success"

    def __str__(self) -> str:
        return str(self.value)
