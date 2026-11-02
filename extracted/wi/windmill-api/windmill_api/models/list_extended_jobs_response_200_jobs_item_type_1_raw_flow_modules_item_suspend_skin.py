from enum import Enum


class ListExtendedJobsResponse200JobsItemType1RawFlowModulesItemSuspendSkin(str, Enum):
    DETAILED = "detailed"
    MINIMAL = "minimal"

    def __str__(self) -> str:
        return str(self.value)
