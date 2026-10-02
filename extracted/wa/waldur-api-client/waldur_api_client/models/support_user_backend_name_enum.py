from enum import Enum


class SupportUserBackendNameEnum(str, Enum):
    ATLASSIAN = "atlassian"
    BASIC = "basic"
    SMAX = "smax"
    ZAMMAD = "zammad"

    def __str__(self) -> str:
        return str(self.value)
