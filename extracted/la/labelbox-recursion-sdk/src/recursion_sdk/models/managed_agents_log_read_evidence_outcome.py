from enum import StrEnum

class ManagedAgentsLogReadEvidenceOutcome(StrEnum):
    AUTHENTICATION_FAILED = "authentication_failed"
    DENIED = "denied"
    EMPTY = "empty"
    ENTRIES = "entries"
    READ_FAILED = "read_failed"

    def __str__(self) -> str:
        return str(self.value)
