from enum import Enum


class CourseAccountStateEnum(str, Enum):
    CLOSED = "Closed"
    ERRED = "Erred"
    OK = "OK"
    PENDING = "Pending"

    def __str__(self) -> str:
        return str(self.value)
