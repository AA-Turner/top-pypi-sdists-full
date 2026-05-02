from enum import Enum


class DynamicInputDataRunnableRefType0Source(str, Enum):
    DEPLOYED = "deployed"

    def __str__(self) -> str:
        return str(self.value)
