from enum import Enum


class ScheduleResourceType(Enum):
    FUNCTION = "function"
    EXECUTION = "execution"
    MESSAGE = "message"
    BACKUP = "backup"
