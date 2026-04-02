from enum import Enum


class CustomerUserOEnum(str, Enum):
    CONCATENATED_NAME = "concatenated_name"
    VALUE_1 = "-concatenated_name"

    def __str__(self) -> str:
        return str(self.value)
