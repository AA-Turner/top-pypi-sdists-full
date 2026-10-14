from enum import Enum


class PublishResultsEnum(str, Enum):
    IMMEDIATELY = "immediately"
    WITH_ROUND = "with_round"

    def __str__(self) -> str:
        return str(self.value)
