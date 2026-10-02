from enum import StrEnum

class ManagedAgentsEnvironmentSetupImageCaptureStatus(StrEnum):
    FAILED = "failed"

    def __str__(self) -> str:
        return str(self.value)
