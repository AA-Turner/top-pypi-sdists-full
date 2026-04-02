from enum import Enum


class BroadcastMessageOEnum(str, Enum):
    AUTHOR_FULL_NAME = "author_full_name"
    CREATED = "created"
    SUBJECT = "subject"
    VALUE_0 = "-author_full_name"
    VALUE_1 = "-created"
    VALUE_2 = "-subject"

    def __str__(self) -> str:
        return str(self.value)
