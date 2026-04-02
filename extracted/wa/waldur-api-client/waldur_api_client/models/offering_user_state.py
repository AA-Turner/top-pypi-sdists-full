from enum import Enum


class OfferingUserState(str, Enum):
    CREATING = "Creating"
    DELETED = "Deleted"
    DELETING = "Deleting"
    ERROR_CREATING = "Error creating"
    ERROR_DELETING = "Error deleting"
    OK = "OK"
    PENDING_ACCOUNT_LINKING = "Pending account linking"
    PENDING_ADDITIONAL_VALIDATION = "Pending additional validation"
    REQUESTED = "Requested"
    REQUESTED_DELETION = "Requested deletion"

    def __str__(self) -> str:
        return str(self.value)
