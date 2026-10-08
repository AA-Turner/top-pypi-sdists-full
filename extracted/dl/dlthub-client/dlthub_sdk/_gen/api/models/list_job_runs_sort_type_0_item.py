from enum import Enum


class ListJobRunsSortType0Item(str, Enum):
    CREATED_AT = "created_at"
    DURATION_SECONDS = "duration_seconds"
    FINISHED_AT = "finished_at"
    NUMBER = "number"
    STARTED_AT = "started_at"

    def __str__(self) -> str:
        return str(self.value)
