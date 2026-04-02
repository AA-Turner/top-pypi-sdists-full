from enum import Enum


class RobotAccountStates(str, Enum):
    CREATING = "Creating"
    DELETED = "Deleted"
    ERROR = "Error"
    OK = "OK"
    REQUESTED = "Requested"
    REQUESTED_DELETION = "Requested deletion"

    def __str__(self) -> str:
        return str(self.value)
