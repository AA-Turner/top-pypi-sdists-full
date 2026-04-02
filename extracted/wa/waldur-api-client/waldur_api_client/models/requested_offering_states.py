from enum import Enum


class RequestedOfferingStates(str, Enum):
    ACCEPTED = "accepted"
    CANCELED = "canceled"
    REQUESTED = "requested"

    def __str__(self) -> str:
        return str(self.value)
