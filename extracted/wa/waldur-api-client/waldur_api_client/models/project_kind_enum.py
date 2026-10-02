from enum import Enum


class ProjectKindEnum(str, Enum):
    COURSE = "course"
    DEFAULT = "default"
    PUBLIC = "public"

    def __str__(self) -> str:
        return str(self.value)
