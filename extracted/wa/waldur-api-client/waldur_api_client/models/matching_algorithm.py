from enum import Enum


class MatchingAlgorithm(str, Enum):
    FAIRFLOW = "fairflow"
    HUNGARIAN = "hungarian"
    MINMAX = "minmax"

    def __str__(self) -> str:
        return str(self.value)
