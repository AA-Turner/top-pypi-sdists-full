from enum import StrEnum

class ManagedAgentsActiveHandoffState(StrEnum):
    AWAITING_USER = "awaiting_user"
    RESOLVED = "resolved"
    USER_DRIVING = "user_driving"

    def __str__(self) -> str:
        return str(self.value)
