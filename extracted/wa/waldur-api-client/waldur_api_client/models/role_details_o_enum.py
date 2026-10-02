from enum import Enum


class RoleDetailsOEnum(str, Enum):
    IS_ACTIVE = "is_active"
    NAME = "name"
    ORIGIN = "origin"
    SCOPE = "scope"
    USERS_COUNT = "users_count"
    VALUE_0 = "-is_active"
    VALUE_1 = "-name"
    VALUE_2 = "-origin"
    VALUE_3 = "-scope"
    VALUE_4 = "-users_count"

    def __str__(self) -> str:
        return str(self.value)
