from enum import StrEnum

class ManagedAgentsEventSourceLastDeliveryResponseType0Disposition(StrEnum):
    ADMITTED = "admitted"
    IGNORED = "ignored"

    def __str__(self) -> str:
        return str(self.value)
