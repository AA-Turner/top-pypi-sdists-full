from enum import Enum


class MemberSyncStatusEntryScopeTypeEnum(str, Enum):
    RESOURCE = "resource"
    RESOURCE_PROJECT = "resource_project"

    def __str__(self) -> str:
        return str(self.value)
