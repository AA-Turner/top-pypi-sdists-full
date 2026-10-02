from enum import Enum


class CustomerPermissionReviewOEnum(str, Enum):
    CLOSED = "closed"
    CREATED = "created"
    VALUE_0 = "-closed"
    VALUE_1 = "-created"

    def __str__(self) -> str:
        return str(self.value)
