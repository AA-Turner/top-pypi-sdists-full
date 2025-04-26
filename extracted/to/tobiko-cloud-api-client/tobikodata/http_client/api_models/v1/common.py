from enum import Enum


class V1Status(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    SKIPPED = "skipped"
    SUCCESS = "success"
    FAILED = "failed"
    PREEMPTED = "preempted"
    ABORTED = "aborted"

    @property
    def complete(self) -> bool:
        return self.value in (
            V1Status.SUCCESS,
            V1Status.FAILED,
            V1Status.SKIPPED,
            V1Status.PREEMPTED,
            V1Status.ABORTED,
        )
