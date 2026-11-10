from enum import Enum


class ResourceTemplateSelectionModeEnum(str, Enum):
    MULTIPLE = "multiple"
    SINGLE = "single"

    def __str__(self) -> str:
        return str(self.value)
