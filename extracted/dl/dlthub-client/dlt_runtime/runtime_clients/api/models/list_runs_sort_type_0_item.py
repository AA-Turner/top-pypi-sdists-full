from enum import Enum


class ListRunsSortType0Item(str, Enum):
    DATE_ADDED = "date_added"
    DURATION = "duration"
    TIME_ENDED = "time_ended"
    TIME_STARTED = "time_started"

    def __str__(self) -> str:
        return str(self.value)
