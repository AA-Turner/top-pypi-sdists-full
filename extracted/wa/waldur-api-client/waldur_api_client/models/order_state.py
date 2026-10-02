from enum import Enum


class OrderState(str, Enum):
    CANCELED = "canceled"
    DONE = "done"
    ERRED = "erred"
    EXECUTING = "executing"
    PENDING_CONSUMER = "pending-consumer"
    PENDING_PROJECT = "pending-project"
    PENDING_PROVIDER = "pending-provider"
    PENDING_START_DATE = "pending-start-date"
    REJECTED = "rejected"

    def __str__(self) -> str:
        return str(self.value)
