from enum import StrEnum

class ManagedAgentsSessionAccessPolicy(StrEnum):
    ADMIN_ONLY = "admin_only"
    PLATFORM_INTERNAL = "platform_internal"

    def __str__(self) -> str:
        return str(self.value)
