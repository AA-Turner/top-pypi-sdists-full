from enum import Enum


class PolicyTypeEnum(str, Enum):
    ACCESS_AS_EXTERNAL = "access_as_external"
    ACCESS_AS_SHARED = "access_as_shared"

    def __str__(self) -> str:
        return str(self.value)
