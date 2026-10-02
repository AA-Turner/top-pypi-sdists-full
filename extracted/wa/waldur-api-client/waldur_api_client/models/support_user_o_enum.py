from enum import Enum


class SupportUserOEnum(str, Enum):
    BACKEND_ID = "backend_id"
    BACKEND_NAME = "backend_name"
    IS_ACTIVE = "is_active"
    NAME = "name"
    VALUE_0 = "-backend_id"
    VALUE_1 = "-backend_name"
    VALUE_2 = "-is_active"
    VALUE_3 = "-name"

    def __str__(self) -> str:
        return str(self.value)
