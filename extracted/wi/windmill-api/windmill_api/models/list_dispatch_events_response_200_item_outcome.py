from enum import Enum


class ListDispatchEventsResponse200ItemOutcome(str, Enum):
    DISPATCHED = "dispatched"
    JOIN_PENDING = "join_pending"
    SKIPPED = "skipped"

    def __str__(self) -> str:
        return str(self.value)
