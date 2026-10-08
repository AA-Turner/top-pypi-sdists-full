from enum import Enum


class ListJobsSortType0Item(str, Enum):
    CREATED_AT = "created_at"
    LAST_RUN_AT = "last_run_at"
    LAST_RUN_ENDED_AT = "last_run_ended_at"
    NAME = "name"
    NEXT_SCHEDULED_RUN_AT = "next_scheduled_run_at"

    def __str__(self) -> str:
        return str(self.value)
