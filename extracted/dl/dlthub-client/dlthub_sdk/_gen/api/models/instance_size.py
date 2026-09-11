from enum import Enum


class InstanceSize(str, Enum):
    LARGE = "large"
    MEDIUM = "medium"
    SMALL = "small"
    XLARGE = "xlarge"

    def __str__(self) -> str:
        return str(self.value)
