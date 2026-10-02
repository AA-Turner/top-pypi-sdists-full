from enum import StrEnum

class ManagedAgentsSessionListItemAccessPolicy(StrEnum):
    ADMIN_ONLY = "admin_only"
    PLATFORM_INTERNAL = "platform_internal"

    def __str__(self) -> str:
        return str(self.value)
