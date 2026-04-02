from enum import Enum


class EmailLogOEnum(str, Enum):
    SENT_AT = "sent_at"
    SUBJECT = "subject"
    VALUE_0 = "-sent_at"
    VALUE_1 = "-subject"

    def __str__(self) -> str:
        return str(self.value)
