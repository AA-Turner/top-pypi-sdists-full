from enum import Enum


class ListScriptsSortType0Item(str, Enum):
    DATE_ADDED = "date_added"
    LAST_RUN_AT = "last_run_at"
    LAST_RUN_ENDED_AT = "last_run_ended_at"
    NAME = "name"
    NEXT_SCHEDULED_RUN = "next_scheduled_run"

    def __str__(self) -> str:
        return str(self.value)
