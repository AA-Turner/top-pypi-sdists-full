from enum import Enum


class OfferingUserOEnum(str, Enum):
    CREATED = "created"
    MODIFIED = "modified"
    USERNAME = "username"
    USER_FIRST_NAME = "user_first_name"
    USER_LAST_NAME = "user_last_name"
    VALUE_0 = "-created"
    VALUE_1 = "-modified"
    VALUE_2 = "-user_first_name"
    VALUE_3 = "-user_last_name"
    VALUE_4 = "-username"

    def __str__(self) -> str:
        return str(self.value)
