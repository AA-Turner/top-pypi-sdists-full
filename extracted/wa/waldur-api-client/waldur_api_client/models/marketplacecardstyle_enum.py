from enum import Enum


class MARKETPLACECARDSTYLEEnum(str, Enum):
    COMPACT = "compact"
    DETAILED = "detailed"
    LIST = "list"
    MINIMAL = "minimal"

    def __str__(self) -> str:
        return str(self.value)
