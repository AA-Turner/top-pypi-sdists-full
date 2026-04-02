from enum import Enum


class GuestPowerStateEnum(str, Enum):
    NOT_RUNNING = "NOT_RUNNING"
    RESETTING = "RESETTING"
    RUNNING = "RUNNING"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    STANDBY = "STANDBY"
    UNAVAILABLE = "UNAVAILABLE"

    def __str__(self) -> str:
        return str(self.value)
