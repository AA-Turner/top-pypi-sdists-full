from enum import Enum


class ManagedProjectAuditEntryEventTypeEnum(str, Enum):
    APPROVED = "approved"
    CREATED = "created"
    DELETED = "deleted"
    DETAILS_UPDATED = "details_updated"
    NOTE_ADDED = "note_added"
    PROJECT_ATTACHED = "project_attached"
    PROJECT_DETACHED = "project_detached"
    REJECTED = "rejected"

    def __str__(self) -> str:
        return str(self.value)
