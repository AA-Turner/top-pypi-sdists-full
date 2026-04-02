from enum import Enum


class MaintenanceAnnouncementOEnum(str, Enum):
    CREATED = "created"
    NAME = "name"
    SCHEDULED_END = "scheduled_end"
    SCHEDULED_START = "scheduled_start"
    VALUE_0 = "-created"
    VALUE_1 = "-name"
    VALUE_2 = "-scheduled_end"
    VALUE_3 = "-scheduled_start"

    def __str__(self) -> str:
        return str(self.value)
