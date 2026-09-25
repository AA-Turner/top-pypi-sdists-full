from enum import Enum


class TriggerKind(str, Enum):
    EVERY = "every"
    HTTP = "http"
    JOB_FAIL = "job.fail"
    JOB_SUCCESS = "job.success"
    MANUAL = "manual"
    ONCE = "once"
    SCHEDULE = "schedule"
    WEBHOOK = "webhook"

    def __str__(self) -> str:
        return str(self.value)
