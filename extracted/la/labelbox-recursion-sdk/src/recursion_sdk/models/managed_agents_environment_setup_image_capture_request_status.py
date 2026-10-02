from enum import StrEnum

class ManagedAgentsEnvironmentSetupImageCaptureRequestStatus(StrEnum):
    FAILED = "failed"

    def __str__(self) -> str:
        return str(self.value)
