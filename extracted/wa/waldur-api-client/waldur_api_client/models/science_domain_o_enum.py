from enum import Enum


class ScienceDomainOEnum(str, Enum):
    CODE = "code"
    NAME = "name"
    VALUE_0 = "-code"
    VALUE_1 = "-name"

    def __str__(self) -> str:
        return str(self.value)
