from enum import Enum


class OfferingState(str, Enum):
    ACTIVE = "Active"
    ARCHIVED = "Archived"
    DRAFT = "Draft"
    PAUSED = "Paused"
    UNAVAILABLE = "Unavailable"

    def __str__(self) -> str:
        return str(self.value)
