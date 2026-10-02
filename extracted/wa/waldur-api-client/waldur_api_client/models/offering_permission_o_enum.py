from enum import Enum


class OfferingPermissionOEnum(str, Enum):
    CREATED = "created"
    EMAIL = "email"
    EXPIRATION_TIME = "expiration_time"
    FULL_NAME = "full_name"
    NATIVE_NAME = "native_name"
    ROLE = "role"
    USERNAME = "username"
    VALUE_0 = "-created"
    VALUE_1 = "-email"
    VALUE_2 = "-expiration_time"
    VALUE_3 = "-full_name"
    VALUE_4 = "-native_name"
    VALUE_5 = "-role"
    VALUE_6 = "-username"

    def __str__(self) -> str:
        return str(self.value)
