from enum import Enum


class BackendTypeEnum(str, Enum):
    ATLASSIAN = "atlassian"
    BASIC = "basic"
    EMAIL = "email"
    SMAX = "smax"
    ZAMMAD = "zammad"

    def __str__(self) -> str:
        return str(self.value)
