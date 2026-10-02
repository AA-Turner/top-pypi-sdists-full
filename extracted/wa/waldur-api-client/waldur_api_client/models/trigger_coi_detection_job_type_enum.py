from enum import Enum


class TriggerCOIDetectionJobTypeEnum(str, Enum):
    FULL_CALL = "full_call"
    INCREMENTAL = "incremental"

    def __str__(self) -> str:
        return str(self.value)
