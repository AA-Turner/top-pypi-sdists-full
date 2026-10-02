from enum import StrEnum

class ManagedAgentsHmacCustomEventSourceVerificationType(StrEnum):
    HMAC_SHA256 = "hmac_sha256"

    def __str__(self) -> str:
        return str(self.value)
