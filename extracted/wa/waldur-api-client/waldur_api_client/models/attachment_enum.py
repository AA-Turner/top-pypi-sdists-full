from enum import Enum


class AttachmentEnum(str, Enum):
    CROSS_PLATFORM = "cross-platform"
    PLATFORM = "platform"

    def __str__(self) -> str:
        return str(self.value)
