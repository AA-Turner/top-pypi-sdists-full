from enum import Enum


class ResourceProjectsLimitPolicyEnum(str, Enum):
    AGGREGATE = "aggregate"
    NONE = "none"
    PER_PROJECT = "per_project"

    def __str__(self) -> str:
        return str(self.value)
