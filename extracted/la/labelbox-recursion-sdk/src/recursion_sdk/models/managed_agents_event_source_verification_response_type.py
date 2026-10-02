from enum import StrEnum

class ManagedAgentsEventSourceVerificationResponseType(StrEnum):
    HMAC_SHA256 = "hmac_sha256"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
