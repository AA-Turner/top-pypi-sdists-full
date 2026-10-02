from enum import Enum


class RemoteProjectAuditEntryEventTypeEnum(str, Enum):
    AWARD_ATTEMPTED = "award_attempted"
    AWARD_CREATED = "award_created"
    AWARD_REJECTED = "award_rejected"
    AWARD_UPDATED = "award_updated"
    AWARD_UPDATE_CONFIRMED = "award_update_confirmed"
    AWARD_UPDATE_REJECTED = "award_update_rejected"
    RESOURCE_DELETED = "resource_deleted"
    STATE_CHANGED = "state_changed"

    def __str__(self) -> str:
        return str(self.value)
