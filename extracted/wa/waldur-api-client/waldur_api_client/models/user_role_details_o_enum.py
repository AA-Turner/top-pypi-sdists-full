from enum import Enum


class UserRoleDetailsOEnum(str, Enum):
    CREATED = "created"
    EMAIL = "email"
    EXPIRATION_TIME = "expiration_time"
    FULL_NAME = "full_name"
    NATIVE_NAME = "native_name"
    ROLE = "role"
    USERNAME = "username"

    def __str__(self) -> str:
        return str(self.value)
