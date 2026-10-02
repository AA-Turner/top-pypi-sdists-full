from enum import StrEnum

class GetAnalyticsScope(StrEnum):
    TENANT = "tenant"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)
