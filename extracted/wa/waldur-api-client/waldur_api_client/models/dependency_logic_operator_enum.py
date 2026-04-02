from enum import Enum


class DependencyLogicOperatorEnum(str, Enum):
    AND = "and"
    OR = "or"

    def __str__(self) -> str:
        return str(self.value)
