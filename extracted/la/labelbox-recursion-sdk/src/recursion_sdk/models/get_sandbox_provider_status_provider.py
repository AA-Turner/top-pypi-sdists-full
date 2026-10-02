from enum import StrEnum

class GetSandboxProviderStatusProvider(StrEnum):
    DOCKER = "docker"
    RUNS = "runs"
    SELF_HOSTED = "self_hosted"

    def __str__(self) -> str:
        return str(self.value)
