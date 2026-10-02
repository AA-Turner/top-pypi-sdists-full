from enum import Enum


class MaintenanceAnnouncementOEnum(str, Enum):
    CREATED = "created"
    NAME = "name"
    OVERRUN_MINUTES = "overrun_minutes"
    SCHEDULED_END = "scheduled_end"
    SCHEDULED_START = "scheduled_start"
    START_DELTA_MINUTES = "start_delta_minutes"
    VALUE_0 = "-created"
    VALUE_1 = "-name"
    VALUE_2 = "-overrun_minutes"
    VALUE_3 = "-scheduled_end"
    VALUE_4 = "-scheduled_start"
    VALUE_5 = "-start_delta_minutes"

    def __str__(self) -> str:
        return str(self.value)
