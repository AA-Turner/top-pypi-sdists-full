from enum import Enum


class TestAutoscalingJsonBodyIntegrationType(str, Enum):
    DRYRUN = "dryrun"
    KUBERNETES = "kubernetes"
    SCRIPT = "script"

    def __str__(self) -> str:
        return str(self.value)
