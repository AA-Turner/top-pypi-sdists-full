from enum import Enum


class CreateAzureTriggerJsonBodyAzureMode(str, Enum):
    BASIC_PUSH = "basic_push"
    NAMESPACE_PULL = "namespace_pull"
    NAMESPACE_PUSH = "namespace_push"

    def __str__(self) -> str:
        return str(self.value)
