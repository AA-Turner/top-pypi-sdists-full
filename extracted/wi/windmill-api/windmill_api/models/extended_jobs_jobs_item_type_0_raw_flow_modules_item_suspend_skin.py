from enum import Enum


class ExtendedJobsJobsItemType0RawFlowModulesItemSuspendSkin(str, Enum):
    DETAILED = "detailed"
    MINIMAL = "minimal"

    def __str__(self) -> str:
        return str(self.value)
