from enum import Enum


class COIDetectionJobOEnum(str, Enum):
    COMPLETED_AT = "completed_at"
    CREATED = "created"
    STARTED_AT = "started_at"
    STATE = "state"
    VALUE_0 = "-completed_at"
    VALUE_1 = "-created"
    VALUE_2 = "-started_at"
    VALUE_3 = "-state"

    def __str__(self) -> str:
        return str(self.value)
