from enum import Enum


class ProtectedCallOEnum(str, Enum):
    CREATED = "created"
    MANAGER_CUSTOMER_NAME = "manager__customer__name"
    NAME = "name"
    VALUE_0 = "-created"
    VALUE_1 = "-manager__customer__name"
    VALUE_2 = "-name"

    def __str__(self) -> str:
        return str(self.value)
