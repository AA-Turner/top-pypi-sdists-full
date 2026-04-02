from enum import Enum


class KindEnum(str, Enum):
    COURSE = "course"
    DEFAULT = "default"
    PUBLIC = "public"

    def __str__(self) -> str:
        return str(self.value)
