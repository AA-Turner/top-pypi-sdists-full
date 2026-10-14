from enum import Enum


class MetricDefinitionStateEnum(str, Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"

    def __str__(self) -> str:
        return str(self.value)
