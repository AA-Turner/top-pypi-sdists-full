from enum import Enum


class InvitationOEnum(str, Enum):
    CREATED = "created"
    CREATED_BY = "created_by"
    EMAIL = "email"
    STATE = "state"
    VALUE_0 = "-created"
    VALUE_1 = "-created_by"
    VALUE_2 = "-email"
    VALUE_3 = "-state"

    def __str__(self) -> str:
        return str(self.value)
