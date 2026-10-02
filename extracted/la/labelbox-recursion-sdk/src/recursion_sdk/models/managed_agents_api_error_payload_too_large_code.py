from enum import StrEnum

class ManagedAgentsApiErrorPayloadTooLargeCode(StrEnum):
    PAYLOAD_TOO_LARGE = "payload_too_large"

    def __str__(self) -> str:
        return str(self.value)
