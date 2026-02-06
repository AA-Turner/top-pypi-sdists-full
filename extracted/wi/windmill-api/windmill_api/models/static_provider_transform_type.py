from enum import Enum


class StaticProviderTransformType(str, Enum):
    STATIC = "static"

    def __str__(self) -> str:
        return str(self.value)
