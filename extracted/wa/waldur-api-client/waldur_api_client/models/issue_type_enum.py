from enum import Enum


class IssueTypeEnum(str, Enum):
    CHANGE_REQUEST = "CHANGE_REQUEST"
    INCIDENT = "INCIDENT"
    INFORMATIONAL = "INFORMATIONAL"
    SERVICE_REQUEST = "SERVICE_REQUEST"

    def __str__(self) -> str:
        return str(self.value)
