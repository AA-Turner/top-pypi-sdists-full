from enum import Enum


class DynamicInputDataRunnableRefType1Source(str, Enum):
    INLINE = "inline"

    def __str__(self) -> str:
        return str(self.value)
