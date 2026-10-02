from enum import Enum


class AssignmentBatchListOEnum(str, Enum):
    CREATED = "created"
    EXPIRES_AT = "expires_at"
    SENT_AT = "sent_at"
    STATUS = "status"
    VALUE_0 = "-created"
    VALUE_1 = "-expires_at"
    VALUE_2 = "-sent_at"
    VALUE_3 = "-status"

    def __str__(self) -> str:
        return str(self.value)
