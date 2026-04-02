from enum import Enum


class COIDetectionJobJobTypeEnum(str, Enum):
    FULL_CALL = "full_call"
    INCREMENTAL = "incremental"
    SINGLE_PAIR = "single_pair"

    def __str__(self) -> str:
        return str(self.value)
