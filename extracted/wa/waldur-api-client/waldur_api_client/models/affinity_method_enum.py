from enum import Enum


class AffinityMethodEnum(str, Enum):
    COMBINED = "combined"
    KEYWORD = "keyword"
    TFIDF = "tfidf"

    def __str__(self) -> str:
        return str(self.value)
