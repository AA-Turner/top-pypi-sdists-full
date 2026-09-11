from enum import Enum


class UsageInstanceBucket(str, Enum):
    LARGE = "large"
    MEDIUM = "medium"
    SMALL = "small"
    UNSIZED = "unsized"
    XLARGE = "xlarge"

    def __str__(self) -> str:
        return str(self.value)
