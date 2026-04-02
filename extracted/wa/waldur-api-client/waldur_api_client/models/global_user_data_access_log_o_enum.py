from enum import Enum


class GlobalUserDataAccessLogOEnum(str, Enum):
    ACCESSOR_TYPE = "accessor_type"
    ACCESSOR_USERNAME = "accessor_username"
    TIMESTAMP = "timestamp"
    USER_USERNAME = "user_username"
    VALUE_0 = "-accessor_type"
    VALUE_1 = "-accessor_username"
    VALUE_2 = "-timestamp"
    VALUE_3 = "-user_username"

    def __str__(self) -> str:
        return str(self.value)
