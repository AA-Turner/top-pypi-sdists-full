from enum import Enum


class ProviderTicketOEnum(str, Enum):
    CREATED = "created"
    MODIFIED = "modified"
    PRIORITY = "priority"
    STATUS = "status"
    VALUE_0 = "-created"
    VALUE_1 = "-modified"
    VALUE_2 = "-priority"
    VALUE_3 = "-status"

    def __str__(self) -> str:
        return str(self.value)
