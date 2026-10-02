from enum import StrEnum

class ManagedAgentsPushDevicePushEnvironment(StrEnum):
    PRODUCTION = "production"
    SANDBOX = "sandbox"

    def __str__(self) -> str:
        return str(self.value)
