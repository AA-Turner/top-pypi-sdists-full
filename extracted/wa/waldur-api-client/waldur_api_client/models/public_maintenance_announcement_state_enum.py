from enum import Enum


class PublicMaintenanceAnnouncementStateEnum(str, Enum):
    COMPLETED = "Completed"
    IN_PROGRESS = "In progress"
    SCHEDULED = "Scheduled"

    def __str__(self) -> str:
        return str(self.value)
